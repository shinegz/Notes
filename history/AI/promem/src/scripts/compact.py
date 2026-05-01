#!/usr/bin/env python3
"""
compact.py - 结构化压缩记忆文件

当某一类别的记忆文件数量超过阈值时，生成结构化摘要模板。
这是 OpenClaw 自我进化机制中"压缩（Compact）"阶段的实现。

注意：compact.py 本身不调用 LLM，它生成的是结构化模板，
由宿主 AI 工具（Qoder/Cursor/Claude）来填充智能摘要。

返回码：
  0 - 成功执行压缩
  1 - 未达阈值，无需压缩
  2 - 执行错误
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 导入共享模块
from history.AI.promem.src.scripts.memory_utils import (
    load_config,
    log_info,
    log_warn,
    write_log,
)


def log_error(msg: str) -> None:
    """输出错误日志到 stderr"""
    print(f"[ERROR] {msg}", file=sys.stderr)


def archive_after_compact(
    memory_root: Path,
    category: str,
    keep_recent: int = 10
) -> int:
    """
    压缩后归档旧文件
    
    将已被摘要覆盖的原始文件移到 archive/{category}/
    保留最近 keep_recent 条不归档，确保最新记忆仍可检索
    
    Args:
        memory_root: 记忆根目录
        category: 分类名称
        keep_recent: 保留最近的文件数量
    
    Returns:
        归档的文件数量
    """
    source_dir = memory_root / category
    archive_dir = memory_root / 'archive' / category
    
    if not source_dir.exists():
        return 0
    
    # 创建归档目录
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取所有 .md 文件，按修改时间排序（最新的在前面）
    files = sorted(
        [f for f in source_dir.glob('*.md') if f.is_file()],
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    
    # 保留最近 N 条，剩余的归档
    to_archive = files[keep_recent:]
    
    archived_count = 0
    for f in to_archive:
        dest = archive_dir / f.name
        # 如果目标已存在，跳过
        if dest.exists():
            log_warn(f"归档目标已存在，跳过: {f.name}")
            continue
        try:
            shutil.move(str(f), str(dest))
            log_info(f"已归档: {category}/{f.name} -> archive/{category}/{f.name}")
            # 记录归档日志
            write_log('ARCHIVE', 'compact', f'{category}/{f.name}',
                      memory_root=str(memory_root),
                      file=f'{category}/{f.name}',
                      dest=f'archive/{category}/{f.name}')
            archived_count += 1
        except Exception as e:
            log_warn(f"归档失败 {f.name}: {e}")
    
    return archived_count


# ============== 分类目录配置 ==============
CATEGORIES = ['decisions', 'bugs', 'rules', 'entities', 'journal']

# 分类中文映射
CATEGORY_NAMES = {
    'decisions': '决策记录',
    'bugs': 'Bug 修复记录',
    'rules': '隐式约束',
    'entities': '关键实体',
    'journal': '未分类日志',
}


def extract_memory_info(file_path: Path) -> Dict[str, Any]:
    """
    从记忆文件提取结构化信息
    
    Returns:
        dict: {
            'title': 标题,
            'date': 日期,
            'file_name': 文件名,
            'key_content': 核心内容（前500字符）,
            'tags': 标签列表,
            'full_content': 完整内容
        }
    """
    info: Dict[str, Any] = {
        'title': '',
        'date': '',
        'file_name': file_path.name,
        'key_content': '',
        'tags': [],
        'full_content': '',
    }
    
    try:
        content = file_path.read_text(encoding='utf-8')
        info['full_content'] = content
        lines = content.split('\n')
        
        # 从文件名提取日期 (YYYY-MM-DD-xxx.md)
        name_match = re.match(r'^(\d{4}-\d{2}-\d{2})', file_path.name)
        if name_match:
            info['date'] = name_match.group(1)
        
        # 解析内容
        body_lines: List[str] = []
        in_frontmatter = False
        frontmatter_count = 0
        
        for line in lines:
            stripped = line.strip()
            
            # 处理 YAML frontmatter
            if stripped == '---':
                frontmatter_count += 1
                if frontmatter_count == 1:
                    in_frontmatter = True
                elif frontmatter_count == 2:
                    in_frontmatter = False
                continue
            
            if in_frontmatter:
                # 提取 tags
                if stripped.startswith('tags:'):
                    tag_value = stripped[5:].strip()
                    if tag_value:
                        # 行内标签格式: tags: [tag1, tag2]
                        tag_match = re.findall(r'[\w\u4e00-\u9fff-]+', tag_value)
                        info['tags'].extend(tag_match)
                elif stripped.startswith('- ') and info['tags']:
                    # 列表格式的标签
                    info['tags'].append(stripped[2:].strip())
                # 提取日期
                elif stripped.startswith('date:'):
                    date_value = stripped[5:].strip()
                    if date_value and not info['date']:
                        info['date'] = date_value
                continue
            
            # 提取标题（# 开头的行）
            if stripped.startswith('#') and not info['title']:
                info['title'] = stripped.lstrip('#').strip()
                # 清理标题中的 Markdown 格式
                info['title'] = re.sub(r'\[([^\]]+)\]:', r'\1:', info['title'])
                continue
            
            # 收集正文内容（排除元数据区块）
            if stripped and not stripped.startswith('## 日期') and not stripped.startswith('## 相关链接'):
                body_lines.append(stripped)
        
        # 提取核心内容（前500字符）
        body_text = ' '.join(body_lines)
        # 清理 Markdown 语法噪音
        body_text = re.sub(r'[#*_`\[\]()>]', ' ', body_text)
        body_text = re.sub(r'\s+', ' ', body_text).strip()
        info['key_content'] = body_text[:500]
        
        # 如果没有日期，使用文件修改时间
        if not info['date']:
            mtime = os.path.getmtime(file_path)
            info['date'] = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        
        # 如果没有标题，从文件名生成
        if not info['title']:
            slug = file_path.stem
            if name_match:
                slug = slug[11:]  # 去除日期前缀
            info['title'] = slug.replace('-', ' ').title()
            
    except Exception as e:
        log_warn(f"读取文件 {file_path.name} 失败: {e}")
    
    return info


def get_category_files(memory_root: Path, category: str) -> List[Path]:
    """获取分类目录下的所有 .md 文件"""
    category_dir = memory_root / category
    if not category_dir.exists():
        return []
    
    files = list(category_dir.glob('*.md'))
    return sorted(files, key=lambda f: f.name)


def count_category_files(memory_root: Path, category: str) -> int:
    """统计分类目录下的 .md 文件数量"""
    return len(get_category_files(memory_root, category))


def get_version_suffix(summaries_dir: Path, category: str) -> str:
    """
    获取摘要文件的版本后缀
    如果已存在同名文件，追加 _v2, _v3 等
    """
    base_name = f"{category}_summary"
    existing = list(summaries_dir.glob(f"{base_name}*.md"))
    
    if not existing:
        return ""
    
    # 找出最大版本号
    max_version = 1
    for f in existing:
        # 匹配 _v2, _v3 等
        match = re.search(r'_v(\d+)\.md$', f.name)
        if match:
            version = int(match.group(1))
            max_version = max(max_version, version)
        elif f.name == f"{base_name}.md":
            # 无版本号的原始文件
            pass
    
    return f"_v{max_version + 1}"


def generate_decisions_summary(memories: List[Dict[str, Any]]) -> str:
    """生成决策分类的摘要内容"""
    lines = ["## 关键决策", ""]
    lines.append("| 日期 | 决策 | 原因 | 状态 | 来源文件 |")
    lines.append("|------|------|------|------|----------|")
    
    for mem in memories:
        title = mem['title'].replace('决策:', '').replace('[决策]:', '').strip()
        date = mem['date']
        # 从 key_content 中尝试提取原因
        reason = "待填充"
        if '因为' in mem['key_content']:
            reason_match = re.search(r'因为[：:]\s*(.{,50})', mem['key_content'])
            if reason_match:
                reason = reason_match.group(1)
        elif '原因' in mem['key_content']:
            reason_match = re.search(r'原因[：:]\s*(.{,50})', mem['key_content'])
            if reason_match:
                reason = reason_match.group(1)
        status = "活跃"
        source = f"decisions/{mem['file_name']}"
        lines.append(f"| {date} | {title[:30]} | {reason[:30]} | {status} | {source} |")
    
    return '\n'.join(lines)


def generate_bugs_summary(memories: List[Dict[str, Any]]) -> str:
    """生成 Bug 分类的摘要内容"""
    lines = ["## 高频 Bug 模式", ""]
    lines.append("| 模式 | 出现次数 | 最近出现 | 典型案例 | 来源文件 |")
    lines.append("|------|----------|----------|----------|----------|")
    
    # 简单聚合：按标题分组（实际项目中可能需要更智能的聚类）
    pattern_count: Dict[str, List[Dict[str, Any]]] = {}
    for mem in memories:
        title = mem['title'].replace('Bug:', '').replace('[Bug]:', '').strip()
        # 提取关键词作为模式标识
        key = title[:20]
        if key not in pattern_count:
            pattern_count[key] = []
        pattern_count[key].append(mem)
    
    for pattern, mems in pattern_count.items():
        count = len(mems)
        latest = max(m['date'] for m in mems)
        typical = mems[0]['title'][:25]
        source = f"bugs/{mems[0]['file_name']}"
        lines.append(f"| {pattern} | {count} | {latest} | {typical} | {source} |")
    
    return '\n'.join(lines)


def generate_rules_summary(memories: List[Dict[str, Any]]) -> str:
    """生成规则分类的摘要内容"""
    lines = ["## 活跃约束", ""]
    
    for mem in memories:
        title = mem['title'].replace('规则:', '').replace('[规则]:', '').strip()
        key_content = mem['key_content'][:80] if mem['key_content'] else "待填充描述"
        source = f"rules/{mem['file_name']}"
        lines.append(f"- **{title}**: {key_content}... (来源: {source})")
    
    return '\n'.join(lines)


def generate_entities_summary(memories: List[Dict[str, Any]]) -> str:
    """生成实体分类的摘要内容"""
    lines = ["## 关键标识符", ""]
    
    for mem in memories:
        title = mem['title'].replace('配置变更:', '').replace('[配置变更]:', '').strip()
        key_content = mem['key_content'][:80] if mem['key_content'] else "待填充描述"
        source = f"entities/{mem['file_name']}"
        lines.append(f"- **{title}**: {key_content}... (来源: {source})")
    
    return '\n'.join(lines)


def generate_journal_summary(memories: List[Dict[str, Any]]) -> str:
    """生成日志分类的摘要内容"""
    lines = ["## 时间线摘要", ""]
    
    # 按日期分组
    by_date: Dict[str, List[Dict[str, Any]]] = {}
    for mem in memories:
        date = mem['date']
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(mem)
    
    for date in sorted(by_date.keys(), reverse=True):
        mems = by_date[date]
        lines.append(f"### {date}")
        lines.append("")
        for mem in mems:
            title = mem['title'][:40]
            source = f"journal/{mem['file_name']}"
            lines.append(f"- {title} (来源: {source})")
        lines.append("")
    
    return '\n'.join(lines)


def generate_summary(
    category: str,
    memories: List[Dict[str, Any]],
    earliest_date: str,
    latest_date: str
) -> str:
    """
    生成分类摘要 Markdown
    
    根据不同分类使用不同的摘要模板
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    count = len(memories)
    category_name = CATEGORY_NAMES.get(category, category)
    
    # 头部信息
    header = f"""# {category_name} 知识摘要

> 自动压缩生成于 {now}
> 原始记录数: {count}，涵盖时间: {earliest_date} ~ {latest_date}

"""
    
    # 根据分类生成不同的摘要内容
    if category == 'decisions':
        body = generate_decisions_summary(memories)
    elif category == 'bugs':
        body = generate_bugs_summary(memories)
    elif category == 'rules':
        body = generate_rules_summary(memories)
    elif category == 'entities':
        body = generate_entities_summary(memories)
    elif category == 'journal':
        body = generate_journal_summary(memories)
    else:
        # 通用格式
        body = "## 记录列表\n\n"
        for mem in memories:
            body += f"- **{mem['title']}** ({mem['date']}) - {mem['file_name']}\n"
    
    # 待办/未决事项（模板占位）
    todos = """
## 待办/未决事项

- [ ] 从记忆中提取的待办...
- [ ] 需要进一步验证的问题...
"""
    
    # 尾部说明
    footer = """
---
*原始记录保留在各分类目录中，此摘要用于快速检索*
"""
    
    return header + body + todos + footer


def compact_category(
    memory_root: Path,
    category: str,
    threshold: int,
    force: bool = False,
    do_archive: bool = True,
    keep_recent: int = 10
) -> Tuple[int, str, int]:
    """
    压缩单个分类
    
    Returns:
        (状态码, 消息, 归档数量)
        状态码: 0 成功, 1 未达阈值, 2 错误
    """
    category_dir = memory_root / category
    
    if not category_dir.exists():
        return (2, f"分类目录不存在: {category}", 0)
    
    # 统计文件数
    files = get_category_files(memory_root, category)
    count = len(files)
    
    log_info(f"[{category}] 文件数: {count}")
    
    # 检查阈值
    if count < threshold and not force:
        return (1, f"[{category}] 未达阈值 ({count}/{threshold})，跳过", 0)
    
    if count == 0:
        return (1, f"[{category}] 无文件，跳过", 0)
    
    # 提取所有记忆信息
    memories: List[Dict[str, Any]] = []
    for f in files:
        info = extract_memory_info(f)
        if info['title']:  # 只收集有效记忆
            memories.append(info)
    
    if not memories:
        return (2, f"[{category}] 无有效记忆可提取", 0)
    
    # 按日期排序
    memories.sort(key=lambda m: m['date'])
    earliest_date = memories[0]['date']
    latest_date = memories[-1]['date']
    
    # 生成摘要
    summary_content = generate_summary(category, memories, earliest_date, latest_date)
    
    # 确保 summaries 目录存在
    summaries_dir = memory_root / 'summaries'
    try:
        summaries_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return (2, f"创建 summaries 目录失败: {e}")
    
    # 获取版本后缀
    version_suffix = get_version_suffix(summaries_dir, category)
    summary_filename = f"{category}_summary{version_suffix}.md"
    summary_path = summaries_dir / summary_filename
    
    # 写入摘要文件
    try:
        summary_path.write_text(summary_content, encoding='utf-8')
    except Exception as e:
        return (2, f"写入摘要文件失败: {e}", 0)
    
    # 压缩后归档旧文件
    archived_count = 0
    if do_archive:
        archived_count = archive_after_compact(memory_root, category, keep_recent)
        if archived_count > 0:
            log_info(f"[{category}] 已归档 {archived_count} 个文件")
    
    # 记录压缩日志
    write_log('COMPACT', 'compact', f'{category} -> {summary_filename}',
              memory_root=str(memory_root),
              category=category,
              source_files=count,
              summary=summary_filename,
              archived=archived_count,
              kept_recent=keep_recent if do_archive else count)
    
    return (0, f"[{category}] 已生成摘要: {summary_path}", archived_count)


def check_all_categories(memory_root: Path, threshold: int) -> None:
    """检查所有分类的文件统计"""
    print(f"\n{'='*50}")
    print(f"分类统计 (阈值: {threshold})")
    print(f"{'='*50}")
    print(f"{'分类':<15} {'文件数':<10} {'状态':<15}")
    print(f"{'-'*50}")
    
    total_files = 0
    need_compact = 0
    
    for category in CATEGORIES:
        count = count_category_files(memory_root, category)
        total_files += count
        
        if count >= threshold:
            status = "⚠️  需要压缩"
            need_compact += 1
        elif count > 0:
            status = "✓ 正常"
        else:
            status = "- 空目录"
        
        print(f"{category:<15} {count:<10} {status:<15}")
    
    print(f"{'-'*50}")
    print(f"{'总计':<15} {total_files:<10}")
    
    if need_compact > 0:
        print(f"\n建议运行: python compact.py --all")
    else:
        print(f"\n所有分类均未达压缩阈值")
    print(f"{'='*50}\n")


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description='结构化压缩记忆文件，生成摘要模板',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
返回码：
  0 - 成功执行压缩
  1 - 未达阈值，无需压缩
  2 - 执行错误

示例:
  %(prog)s --check                           # 检查各分类统计
  %(prog)s --category decisions              # 压缩决策分类
  %(prog)s --category bugs --force           # 强制压缩 Bug 分类
  %(prog)s --all                             # 压缩所有分类
  %(prog)s --all --memory-root /path/to/memory  # 指定记忆目录
        """
    )
    
    # 互斥参数组
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--category',
        choices=CATEGORIES,
        help='指定要压缩的分类'
    )
    group.add_argument(
        '--all',
        action='store_true',
        help='压缩所有分类'
    )
    group.add_argument(
        '--check',
        action='store_true',
        help='仅检查统计，不执行压缩'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='强制压缩（忽略阈值）'
    )
    parser.add_argument(
        '--no-archive',
        action='store_true',
        help='跳过归档步骤，仅生成摘要'
    )
    parser.add_argument(
        '--memory-root',
        help='记忆根目录路径（默认 .promem/memory）'
    )
    
    args = parser.parse_args()
    
    # 确定记忆根目录
    if args.memory_root:
        memory_root = Path(args.memory_root).resolve()
    else:
        # 默认从当前目录查找 .promem
        current = Path.cwd()
        memory_root = current / '.promem' / 'memory'
        
        # 如果当前目录没有，尝试向上查找
        if not memory_root.exists():
            for parent in current.parents:
                candidate = parent / '.promem' / 'memory'
                if candidate.exists():
                    memory_root = candidate
                    break
    
    if not memory_root.exists():
        log_error(f"记忆目录不存在: {memory_root}")
        return 2
    
    log_info(f"记忆目录: {memory_root}")
    
    # 加载配置
    promem_root = memory_root.parent
    config = load_config(promem_root)
    compact_config = config.get('compact', {})
    threshold = compact_config.get('auto_threshold', 50)
    
    # 获取生命周期配置
    lifecycle_config = config.get('lifecycle', {})
    keep_recent = lifecycle_config.get('compact_keep_recent', 10)
    do_archive = not args.no_archive
    
    log_info(f"压缩阈值: {threshold}")
    if do_archive:
        log_info(f"归档模式: 开启 (保留最近 {keep_recent} 条)")
    else:
        log_info(f"归档模式: 关闭")
    
    # 执行操作
    if args.check:
        # 仅检查模式
        check_all_categories(memory_root, threshold)
        return 0
    
    if not args.category and not args.all:
        # 无参数时显示帮助
        parser.print_help()
        return 1
    
    # 确定要处理的分类
    if args.all:
        categories_to_process = CATEGORIES
    else:
        categories_to_process = [args.category]
    
    # 执行压缩
    success_count = 0
    skip_count = 0
    error_count = 0
    total_archived = 0
    
    for category in categories_to_process:
        status, message, archived = compact_category(
            memory_root,
            category,
            threshold,
            force=args.force,
            do_archive=do_archive,
            keep_recent=keep_recent
        )
        
        if status == 0:
            log_info(message)
            success_count += 1
            total_archived += archived
        elif status == 1:
            log_info(message)
            skip_count += 1
        else:
            log_error(message)
            error_count += 1
    
    # 输出总结
    summary = f"\n压缩完成: 成功 {success_count}, 跳过 {skip_count}, 错误 {error_count}"
    if total_archived > 0:
        summary += f", 归档 {total_archived} 个文件"
    print(summary)
    
    # 确定返回码
    if error_count > 0:
        return 2
    elif success_count > 0:
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
