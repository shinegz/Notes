#!/usr/bin/env python3
"""
capture_from_commit.py - 从 Git commit 中自动提取工程知识并写入记忆分类目录

返回码：
  0 - 成功，有知识被提取
  1 - 成功，但无有效知识（commit 内容不匹配任何捕获规则）
  2 - 执行错误
  3 - 内容重复，跳过写入
  4 - 已达单次上限，跳过写入
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

# 导入共享模块
from history.AI.promem.src.scripts.memory_utils import (
    load_config as load_config_utils,
    sanitize_sensitive,
    is_duplicate,
    generate_filename,
    check_global_session_limit,
    log_info as log_info_utils,
    log_warn,
    write_log,
    DEFAULT_SENSITIVE_PATTERNS,
)

# ==================== Diff 分析配置 ====================
MAX_DIFF_LINES = 500       # 最大分析行数
MAX_DIFF_PER_FILE = 200    # 单文件最大 diff 行数

# 需要跳过详细 diff 的文件模式
SKIP_FILE_PATTERNS = [
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'Pipfile.lock', 'Cargo.lock', 'Gemfile.lock', 'composer.lock',
    'go.sum', '.min.js', '.min.css', '.map',
    '__pycache__', '.pyc',
]


# ==================== Diff 分析函数 ====================
def should_skip_file(file_path: str) -> bool:
    """判断是否跳过文件的详细 diff"""
    return any(p in file_path for p in SKIP_FILE_PATTERNS)


def split_diff_by_file(lines: List[str]) -> List[Tuple[str, List[str]]]:
    """
    按文件分割 diff 内容
    返回 [(file_path, [lines...]), ...]
    """
    files = []
    current_file = None
    current_lines: List[str] = []

    for line in lines:
        # 匹配 diff --git a/path b/path
        if line.startswith('diff --git '):
            if current_file is not None:
                files.append((current_file, current_lines))
            # 提取文件路径 (b/path)
            parts = line.split(' b/')
            current_file = parts[-1] if len(parts) > 1 else 'unknown'
            current_lines = [line]
        elif current_file is not None:
            current_lines.append(line)

    if current_file is not None:
        files.append((current_file, current_lines))

    return files


def extract_important_lines(file_lines: List[str], max_lines: int) -> List[str]:
    """
    智能提取重要行：优先保留函数/类定义、注释、import 变更
    """
    important = []
    normal = []

    for line in file_lines:
        stripped = line.lstrip('+').lstrip('-').strip()
        # 优先保留的内容
        is_important = (
            line.startswith('diff --git') or
            line.startswith('---') or
            line.startswith('+++') or
            line.startswith('@@') or
            is_function_definition(stripped) or
            is_import_statement(stripped) or
            is_comment(stripped)
        )
        if is_important:
            important.append(line)
        else:
            normal.append(line)

    # 组合：优先取 important，剩余空间取 normal
    result = important[:max_lines]
    remaining = max_lines - len(result)
    if remaining > 0:
        result.extend(normal[:remaining])

    return result


def truncate_diff(diff_content: str, max_lines: int = MAX_DIFF_LINES, max_per_file: int = MAX_DIFF_PER_FILE) -> Tuple[str, bool]:
    """
    智能裁剪 diff 内容
    返回 (裁剪后的 diff, 是否被裁剪)
    """
    if not diff_content:
        return diff_content, False

    lines = diff_content.split('\n')
    if len(lines) <= max_lines:
        return diff_content, False

    # 按文件分割 diff
    files = split_diff_by_file(lines)

    result_lines: List[str] = []
    truncated = False

    for file_path, file_lines in files:
        # 跳过 lock 文件和 auto-generated 文件
        if should_skip_file(file_path):
            result_lines.append(f"diff --git a/{file_path} b/{file_path}")
            result_lines.append(f"  (skipped: auto-generated/lock file, {len(file_lines)} lines)")
            truncated = True
            continue

        if len(file_lines) > max_per_file:
            # 智能截取：保留函数签名、类定义、注释
            important_lines = extract_important_lines(file_lines, max_per_file)
            result_lines.extend(important_lines)
            result_lines.append(f"  ... (truncated: {len(file_lines) - max_per_file} more lines)")
            truncated = True
        else:
            result_lines.extend(file_lines)

    return '\n'.join(result_lines), truncated


def is_function_definition(line: str) -> bool:
    """判断是否是函数/方法定义"""
    patterns = [
        r'^\s*def\s+\w+',                           # Python
        r'^\s*(async\s+)?function\s+\w+',           # JavaScript
        r'^\s*(export\s+)?(default\s+)?(async\s+)?function',  # JS export
        r'^\s*(const|let|var)\s+\w+\s*=\s*(async\s+)?\(',     # JS arrow
        r'^\s*(public|private|protected)?\s*(static\s+)?\w+\s*\(',  # Java/TS
        r'^\s*func\s+\w+',                          # Go
        r'^\s*(pub\s+)?fn\s+\w+',                   # Rust
        r'^\s*class\s+\w+',                         # class 定义
    ]
    return any(re.match(p, line) for p in patterns)


def extract_function_name(line: str) -> str:
    """提取函数名"""
    # Python: def func_name(
    m = re.match(r'.*(?:def|function|func|fn|class)\s+(\w+)', line)
    if m:
        return m.group(1)
    # Arrow function: const name =
    m = re.match(r'.*(?:const|let|var)\s+(\w+)\s*=', line)
    if m:
        return m.group(1)
    return line[:60].strip()


def is_import_statement(line: str) -> bool:
    """判断是否是 import/require 语句"""
    return bool(re.match(r'^\s*(import|from|require|use|include)\s', line))


def is_comment(line: str) -> bool:
    """判断是否是注释"""
    stripped = line.strip()
    return stripped.startswith(('#', '//', '/*', '*', '"""', "'''"))


def extract_hunk_context(hunk_line: str) -> Optional[str]:
    """从 @@ -x,y +a,b @@ context 中提取函数上下文"""
    m = re.match(r'^@@.*@@\s+(.+)$', hunk_line)
    if m:
        return m.group(1).strip()
    return None


def analyze_diff(diff_content: str) -> Dict[str, Any]:
    """
    分析 diff 内容，提取有价值信息
    """
    analysis: Dict[str, Any] = {
        'added_functions': [],      # 新增的函数/方法
        'removed_functions': [],    # 删除的函数/方法
        'modified_functions': [],   # 修改的函数（出现在 @@ 行中）
        'key_changes': [],          # 关键变更描述
        'comments': [],             # 新增/修改的注释（可能含 why/reason）
        'imports_changed': [],      # 依赖变更
        'total_additions': 0,
        'total_deletions': 0,
    }

    if not diff_content:
        return analysis

    for line in diff_content.split('\n'):
        # 统计增删
        if line.startswith('+') and not line.startswith('+++'):
            analysis['total_additions'] += 1
        elif line.startswith('-') and not line.startswith('---'):
            analysis['total_deletions'] += 1

        # 提取函数定义（新增）
        if line.startswith('+'):
            content = line[1:].strip()
            if is_function_definition(content):
                func_name = extract_function_name(content)
                if func_name and func_name not in analysis['added_functions']:
                    analysis['added_functions'].append(func_name)
            if is_import_statement(content):
                analysis['imports_changed'].append(content)
            # 提取注释（可能包含决策原因）
            if is_comment(content) and len(content) > 5:
                analysis['comments'].append(content)

        # 提取函数定义（删除）
        elif line.startswith('-'):
            content = line[1:].strip()
            if is_function_definition(content):
                func_name = extract_function_name(content)
                if func_name and func_name not in analysis['removed_functions']:
                    analysis['removed_functions'].append(func_name)

        # 提取 @@ 行中的函数上下文
        elif line.startswith('@@'):
            func_context = extract_hunk_context(line)
            if func_context and func_context not in analysis['modified_functions']:
                analysis['modified_functions'].append(func_context)

    return analysis


def log_error(msg: str) -> None:
    """输出错误日志到 stderr"""
    print(f"[ERROR] {msg}", file=sys.stderr)


def log_info(msg: str) -> None:
    """输出信息日志到 stderr"""
    print(f"[INFO] {msg}", file=sys.stderr)


def load_config(repo_root: Path) -> Dict[str, Any]:
    """
    加载 .promem/config.yaml 配置
    委托给 memory_utils.load_config
    """
    return load_config_utils(repo_root)


def run_git_command(args: List[str], cwd: Path) -> Tuple[bool, str]:
    """
    运行 Git 命令
    返回 (成功, 输出内容)
    """
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, "Git 命令超时"
    except Exception as e:
        return False, str(e)


def get_commit_info(repo_root: Path, commit: str) -> Tuple[bool, Dict[str, Any]]:
    """
    获取 commit 信息
    返回 (成功, 信息字典)
    """
    info: Dict[str, Any] = {}

    # 获取 commit message
    success, output = run_git_command(
        ['log', '-1', '--format=%B', commit],
        repo_root
    )
    if not success:
        return False, {'error': f'获取 commit message 失败: {output}'}
    info['message'] = output.strip()

    # 获取 commit hash
    success, output = run_git_command(
        ['log', '-1', '--format=%H', commit],
        repo_root
    )
    if not success:
        return False, {'error': f'获取 commit hash 失败: {output}'}
    info['hash'] = output.strip()

    # 获取短 hash
    success, output = run_git_command(
        ['log', '-1', '--format=%h', commit],
        repo_root
    )
    if success:
        info['short_hash'] = output.strip()
    else:
        info['short_hash'] = info['hash'][:7]

    # 获取日期
    success, output = run_git_command(
        ['log', '-1', '--format=%ci', commit],
        repo_root
    )
    if success:
        # 格式: 2024-01-15 10:30:00 +0800
        date_str = output.strip().split()[0]
        info['date'] = date_str
    else:
        info['date'] = datetime.now().strftime('%Y-%m-%d')

    # 获取 diff stat
    success, output = run_git_command(
        ['show', '--stat', '--format=', commit],
        repo_root
    )
    if not success:
        return False, {'error': f'获取 diff stat 失败: {output}'}
    info['diff_stat'] = output.strip()

    # 解析变更的文件列表
    info['changed_files'] = []
    for line in info['diff_stat'].split('\n'):
        line = line.strip()
        if line and '|' in line:
            file_part = line.split('|')[0].strip()
            if file_part:
                info['changed_files'].append(file_part)

    # 获取 diff 内容（限制大小）
    success, output = run_git_command(
        ['diff', f'{commit}~1..{commit}', '--unified=3'],
        repo_root
    )
    if success:
        info['diff_content'] = output
    else:
        # 可能是首次 commit，没有父提交
        info['diff_content'] = ''

    return True, info


def classify_commit(commit_info: Dict[str, Any]) -> Optional[Tuple[str, str]]:
    """
    根据规则分类 commit
    返回 (分类目录, 模板类型) 或 None
    """
    message = commit_info.get('message', '').lower()
    changed_files = commit_info.get('changed_files', [])
    diff_stat = commit_info.get('diff_stat', '')

    # 1. Fix commit - message 包含 fix/bugfix/hotfix
    fix_patterns = [r'\bfix\b', r'\bbugfix\b', r'\bhotfix\b']
    for pattern in fix_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return ('bugs', 'bug')

    # 2. 依赖变更 - diff 包含依赖文件
    dependency_files = [
        'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        'requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile',
        'go.mod', 'go.sum',
        'Cargo.toml', 'Cargo.lock',
        'pom.xml', 'build.gradle', 'build.gradle.kts',
        'Gemfile', 'Gemfile.lock',
        'composer.json', 'composer.lock'
    ]
    for file in changed_files:
        file_name = os.path.basename(file)
        if file_name in dependency_files:
            return ('decisions', 'decision')

    # 3. Config 变更 - 配置文件（排除 .promem/ 下的）
    config_patterns = [
        r'\.env',
        r'\.config\.',
        r'docker',
        r'\.yml$',
        r'\.yaml$',
        r'Dockerfile',
        r'\.toml$',  # 通用配置
        r'\.ini$',
        r'\.conf$',
    ]
    for file in changed_files:
        # 排除 .promem/ 目录下的文件
        if '.promem/' in file or file.startswith('.promem'):
            continue
        for pattern in config_patterns:
            if re.search(pattern, file, re.IGNORECASE):
                return ('entities', 'config')

    # 4. 接口变更 - 文件名含 api/service/controller/handler
    api_patterns = [r'api', r'service', r'controller', r'handler', r'route']
    for file in changed_files:
        file_lower = file.lower()
        for pattern in api_patterns:
            if pattern in file_lower:
                return ('decisions', 'decision')

    # ===== 新增：diff 分析辅助分类 =====
    analysis = commit_info.get('diff_analysis', {})

    # 如果删除了函数并新增了替代函数 → 可能是重构决策
    if analysis.get('removed_functions') and analysis.get('added_functions'):
        return ('decisions', 'decision')

    # 如果有大量新增注释 → 可能包含规则/约束
    if len(analysis.get('comments', [])) >= 3:
        # 检查注释中是否含决策性关键词
        decision_keywords = ['because', 'reason', 'why', 'decision', '因为', '原因', '决定', '选择']
        for comment in analysis['comments']:
            if any(kw in comment.lower() for kw in decision_keywords):
                return ('decisions', 'decision')

    return None


def sanitize_content(content: str, patterns: List[str]) -> str:
    """
    使用敏感信息正则进行脱敏
    委托给 memory_utils.sanitize_sensitive
    """
    return sanitize_sensitive(content, patterns)


def generate_slug(message: str) -> str:
    """
    从 commit message 生成 slug
    取前 50 字符，去除特殊字符，空格转 -，全小写
    """
    # 取第一行作为标题
    first_line = message.split('\n')[0].strip()

    # 取前 50 字符
    slug = first_line[:50]

    # 去除特殊字符，保留字母、数字、空格、中文
    slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', slug)

    # 空格转 -
    slug = re.sub(r'\s+', '-', slug)

    # 全小写
    slug = slug.lower()

    # 去除首尾的 -
    slug = slug.strip('-')

    # 如果为空，使用默认值
    if not slug:
        slug = 'commit'

    return slug


def generate_bug_record(commit_info: Dict[str, Any]) -> str:
    """生成 Bug 记录 Markdown"""
    message = commit_info.get('message', '')
    first_line = message.split('\n')[0].strip()
    rest_lines = '\n'.join(message.split('\n')[1:]).strip()

    # 尝试从 message 提取症状和根因
    symptom = rest_lines if rest_lines else "从 commit 信息推断"
    root_cause = "从代码变更推断"

    changed_files = commit_info.get('changed_files', [])
    files_list = '\n'.join([f'- {f}' for f in changed_files]) if changed_files else '- 无'

    # ===== 新增：diff 分析增强 =====
    analysis = commit_info.get('diff_analysis', {})

    # 变更统计
    stats = f"+{analysis.get('total_additions', 0)} / -{analysis.get('total_deletions', 0)}"

    # 修改的函数
    modified_funcs_section = ""
    if analysis.get('modified_functions'):
        modified_funcs_section = "\n### 修改的函数\n"
        for func in analysis['modified_functions'][:10]:
            modified_funcs_section += f"- `{func}`\n"

    # 新增的函数
    added_funcs_section = ""
    if analysis.get('added_functions'):
        added_funcs_section = "\n### 新增的函数\n"
        for func in analysis['added_functions'][:10]:
            added_funcs_section += f"- `{func}`\n"

    # 删除的函数
    removed_funcs_section = ""
    if analysis.get('removed_functions'):
        removed_funcs_section = "\n### 删除的函数\n"
        for func in analysis['removed_functions'][:10]:
            removed_funcs_section += f"- `{func}`\n"

    # 相关注释（可能含修复原因）
    comments_section = ""
    if analysis.get('comments'):
        relevant_comments = [c for c in analysis['comments'] if len(c) > 10][:5]
        if relevant_comments:
            comments_section = "\n### 相关注释\n"
            for comment in relevant_comments:
                comments_section += f"> {comment}\n"

    # 组合 diff 分析部分
    diff_analysis_section = ""
    if modified_funcs_section or added_funcs_section or removed_funcs_section or comments_section:
        diff_analysis_section = f"""\n## 代码变更分析\n变更量: {stats}\n{modified_funcs_section}{added_funcs_section}{removed_funcs_section}{comments_section}"""

    return f"""# [Bug]: {first_line}

## 日期
{commit_info.get('date', datetime.now().strftime('%Y-%m-%d'))}

## 症状
{symptom}

## 根因
{root_cause}

## 解法
{commit_info.get('short_hash', '')} - {first_line}

变更文件:
{files_list}{diff_analysis_section}

## 相关代码
{files_list}

## 相关链接
- Commit: {commit_info.get('hash', '')}
"""


def generate_decision_record(commit_info: Dict[str, Any]) -> str:
    """生成决策记录 Markdown"""
    message = commit_info.get('message', '')
    first_line = message.split('\n')[0].strip()
    rest_lines = '\n'.join(message.split('\n')[1:]).strip()

    background = rest_lines if rest_lines else "从 commit 上下文推断"

    changed_files = commit_info.get('changed_files', [])
    files_list = '\n'.join([f'- {f}' for f in changed_files]) if changed_files else '- 无'

    # ===== 新增：diff 分析增强 =====
    analysis = commit_info.get('diff_analysis', {})

    # 依赖变更
    imports_section = ""
    if analysis.get('imports_changed'):
        imports_section = "\n## 依赖变更\n"
        for imp in analysis['imports_changed'][:10]:
            imports_section += f"- `{imp}`\n"

    # 新增的函数
    added_funcs_section = ""
    if analysis.get('added_functions'):
        added_funcs_section = "\n## 新增的函数/类\n"
        for func in analysis['added_functions'][:10]:
            added_funcs_section += f"- `{func}`\n"

    # 删除的函数
    removed_funcs_section = ""
    if analysis.get('removed_functions'):
        removed_funcs_section = "\n## 删除的函数/类\n"
        for func in analysis['removed_functions'][:10]:
            removed_funcs_section += f"- `{func}`\n"

    # 相关注释（可能含决策原因）
    comments_section = ""
    if analysis.get('comments'):
        relevant_comments = [c for c in analysis['comments'] if len(c) > 10][:5]
        if relevant_comments:
            comments_section = "\n## 相关注释\n"
            for comment in relevant_comments:
                comments_section += f"> {comment}\n"

    return f"""# [决策]: {first_line}

## 日期
{commit_info.get('date', datetime.now().strftime('%Y-%m-%d'))}

## 背景
{background}

## 决策
{first_line}

## 影响范围
{files_list}{imports_section}{added_funcs_section}{removed_funcs_section}{comments_section}

## 相关链接
- Commit: {commit_info.get('hash', '')}
"""


def generate_config_record(commit_info: Dict[str, Any]) -> str:
    """生成配置变更记录 Markdown"""
    message = commit_info.get('message', '')
    first_line = message.split('\n')[0].strip()

    changed_files = commit_info.get('changed_files', [])
    # 找出配置相关的文件
    config_files = [f for f in changed_files if any(
        p in f.lower() for p in ['.env', '.config', 'docker', '.yml', '.yaml', '.toml', '.ini', '.conf']
    )]
    config_file_name = config_files[0] if config_files else (changed_files[0] if changed_files else 'config')

    files_list = '\n'.join([f'- {f}' for f in changed_files]) if changed_files else '- 无'

    return f"""# [配置变更]: {os.path.basename(config_file_name)}

## 日期
{commit_info.get('date', datetime.now().strftime('%Y-%m-%d'))}

## 变更内容
{first_line}

## 影响范围
{files_list}

## 相关链接
- Commit: {commit_info.get('hash', '')}
"""


def write_record(
    repo_root: Path,
    category: str,
    template_type: str,
    commit_info: Dict[str, Any],
    sensitive_patterns: List[str],
    similarity_threshold: float = 0.95,
    skip_duplicate_check: bool = False
) -> Tuple[int, str]:
    """
    写入记录文件
    
    返回 (状态码, 消息)
    状态码:
      0 - 成功写入
      1 - 内容重复，跳过
      2 - 写入失败
    """
    # 生成内容
    if template_type == 'bug':
        content = generate_bug_record(commit_info)
    elif template_type == 'decision':
        content = generate_decision_record(commit_info)
    elif template_type == 'config':
        content = generate_config_record(commit_info)
    else:
        return 2, f"未知的模板类型: {template_type}"

    # 脱敏（对 commit message 和生成内容都进行脱敏）
    content = sanitize_content(content, sensitive_patterns)

    # 目标目录
    target_dir = repo_root / '.promem' / 'memory' / category

    # 语义去重检查
    if not skip_duplicate_check:
        is_dup, similar_file, similarity = is_duplicate(
            content, str(target_dir), similarity_threshold
        )
        if is_dup:
            return 1, f"内容与 {similar_file} 重复（相似度 {similarity:.2%}），跳过写入"

    # 生成文件名
    date = commit_info.get('date', datetime.now().strftime('%Y-%m-%d'))
    slug = generate_slug(commit_info.get('message', ''))
    filename = f"{date}-{slug}.md"

    target_file = target_dir / filename

    try:
        # 确保目录存在
        target_dir.mkdir(parents=True, exist_ok=True)

        # 写入文件
        target_file.write_text(content, encoding='utf-8')
        return 0, str(target_file)
    except Exception as e:
        return 2, str(e)


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description='从 Git commit 中自动提取工程知识并写入记忆分类目录',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
返回码：
  0 - 成功，有知识被提取
  1 - 成功，但无有效知识（commit 内容不匹配任何捕获规则）
  2 - 执行错误
  3 - 内容重复，跳过写入
  4 - 已达单次上限，跳过写入

示例:
  %(prog)s                           # 分析 HEAD commit
  %(prog)s --since abc123            # 分析指定 commit
  %(prog)s --repo-root /path/to/repo # 指定仓库路径
        """
    )
    parser.add_argument(
        '--since',
        default='HEAD',
        help='指定分析的 commit（默认 HEAD）'
    )
    parser.add_argument(
        '--repo-root',
        default='.',
        help='Git 仓库根目录（默认当前目录）'
    )
    parser.add_argument(
        '--skip-duplicate-check',
        action='store_true',
        help='跳过语义去重检查'
    )
    parser.add_argument(
        '--skip-limit-check',
        action='store_true',
        help='跳过单次上限检查'
    )
    parser.add_argument(
        '--memory-root',
        type=str,
        default=None,
        help='记忆目录路径（默认 .promem/memory）'
    )

    args = parser.parse_args()

    # 解析仓库路径
    repo_root = Path(args.repo_root).resolve()

    if not repo_root.exists():
        log_error(f"仓库路径不存在: {repo_root}")
        return 2

    # 检查是否是 Git 仓库
    success, output = run_git_command(['rev-parse', '--git-dir'], repo_root)
    if not success:
        log_error(f"不是有效的 Git 仓库: {repo_root}")
        return 2

    # 加载配置
    config = load_config(repo_root)
    capture_config = config.get('capture', {})
    max_per_session = capture_config.get('max_per_session', 5)
    similarity_threshold = capture_config.get('similarity_threshold', 0.95)
    sensitive_patterns = capture_config.get('sensitive_patterns', DEFAULT_SENSITIVE_PATTERNS)
    # diff 分析配置
    analyze_diff_enabled = capture_config.get('analyze_diff', True)
    max_diff_lines = capture_config.get('max_diff_lines', MAX_DIFF_LINES)
    max_diff_per_file = capture_config.get('max_diff_per_file', MAX_DIFF_PER_FILE)

    # 检查单次上限
    if args.memory_root:
        memory_root = Path(args.memory_root).resolve()
    else:
        memory_root = repo_root / '.promem' / 'memory'
    if not args.skip_limit_check:
        is_exceeded, current_count = check_global_session_limit(
            str(memory_root), max_per_session
        )
        if is_exceeded:
            log_warn(f"今日沉淀已达上限 ({current_count}/{max_per_session})，跳过本次写入")
            write_log('SKIP', 'capture', '达到会话上限',
                      memory_root=str(memory_root),
                      reason='session_limit',
                      current=current_count,
                      max=max_per_session)
            return 4

    # 获取 commit 信息
    log_info(f"分析 commit: {args.since}")
    success, commit_info = get_commit_info(repo_root, args.since)
    if not success:
        log_error(commit_info.get('error', '获取 commit 信息失败'))
        return 2

    # 对 commit message 进行脱敏（用于日志输出）
    sanitized_message = sanitize_content(
        commit_info.get('message', ''), sensitive_patterns
    )
    log_info(f"Commit: {commit_info.get('short_hash', '')} - {sanitized_message.split(chr(10))[0][:50]}")

    # ===== 新增：Diff 内容分析 =====
    if analyze_diff_enabled:
        diff_content = commit_info.get('diff_content', '')
        if diff_content:
            # 智能裁剪
            truncated_diff, was_truncated = truncate_diff(
                diff_content, max_diff_lines, max_diff_per_file
            )
            # 分析
            commit_info['diff_analysis'] = analyze_diff(truncated_diff)
            commit_info['diff_truncated'] = was_truncated
            if was_truncated:
                log_info(f"Diff 已裁剪（原始 {len(diff_content.split(chr(10)))} 行）")
        else:
            commit_info['diff_analysis'] = {}
            commit_info['diff_truncated'] = False
    else:
        commit_info['diff_analysis'] = {}
        commit_info['diff_truncated'] = False

    # 分类 commit
    classification = classify_commit(commit_info)
    if not classification:
        log_info("无匹配的捕获规则，跳过")
        write_log('SKIP', 'capture', '无匹配规则',
                  memory_root=str(memory_root),
                  commit=commit_info.get('short_hash', ''),
                  msg=sanitized_message.split(chr(10))[0][:30],
                  reason='no_matching_rule',
                  files=len(commit_info.get('changed_files', [])))
        return 1

    category, template_type = classification
    log_info(f"分类: {category} ({template_type})")
    
    # 记录分类决策日志
    analysis = commit_info.get('diff_analysis', {})
    write_log('CLASSIFY', 'capture', f'{category}/{template_type}',
              memory_root=str(memory_root),
              commit=commit_info.get('short_hash', ''),
              msg=sanitized_message.split(chr(10))[0][:30],
              files=len(commit_info.get('changed_files', [])),
              category=category,
              diff_stats=f"+{analysis.get('total_additions', 0)}/-{analysis.get('total_deletions', 0)}",
              functions_modified=analysis.get('modified_functions', [])[:3],
              functions_added=analysis.get('added_functions', [])[:3],
              truncated=commit_info.get('diff_truncated', False))

    # 写入记录（包含去重检查和脱敏）
    status, result = write_record(
        repo_root,
        category,
        template_type,
        commit_info,
        sensitive_patterns,
        similarity_threshold=similarity_threshold,
        skip_duplicate_check=args.skip_duplicate_check
    )

    if status == 1:  # 重复
        log_warn(result)
        # 提取相似文件名和相似度
        similar_match = re.search(r'与\s+([\w.-]+)\s+重复.*相似度\s+([\d.]+)%', result)
        similar_file = similar_match.group(1) if similar_match else ''
        similarity = float(similar_match.group(2)) / 100 if similar_match else 0.0
        write_log('DUPLICATE', 'capture', '内容重复',
                  memory_root=str(memory_root),
                  commit=commit_info.get('short_hash', ''),
                  reason='duplicate',
                  similarity=similarity,
                  similar_to=similar_file)
        return 3
    elif status == 2:  # 写入失败
        log_error(f"写入记录失败: {result}")
        write_log('ERROR', 'capture', '写入失败',
                  memory_root=str(memory_root),
                  commit=commit_info.get('short_hash', ''),
                  error=result[:100])
        return 2

    log_info(f"成功写入: {result}")
    
    # 记录成功捕获日志
    write_log('CAPTURE', 'capture', '成功捕获',
              memory_root=str(memory_root),
              commit=commit_info.get('short_hash', ''),
              file=Path(result).name,
              category=category,
              diff_lines=analysis.get('total_additions', 0) + analysis.get('total_deletions', 0),
              functions_modified=len(analysis.get('modified_functions', [])),
              functions_added=len(analysis.get('added_functions', [])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
