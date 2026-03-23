#!/usr/bin/env python3
"""ProMem 记忆系统通用工具

提供记忆沉淀流程中的共享功能：
- 敏感信息过滤
- 语义去重
- 配置读取
- 文件命名
- 会话上限检查
- 结构化运行日志
"""

import fcntl  # 文件锁，防止并发写入冲突
import os
import re
import sys
from difflib import SequenceMatcher
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def log_warn(msg: str) -> None:
    """输出警告日志到 stderr"""
    print(f"[WARN] {msg}", file=sys.stderr)


def log_info(msg: str) -> None:
    """输出信息日志到 stderr"""
    print(f"[INFO] {msg}", file=sys.stderr)


# ============== 结构化运行日志系统 ==============

# 日志配置
MAX_LOG_SIZE = 1 * 1024 * 1024  # 1MB 轮转
MAX_LOG_FILES = 3                # 保留 3 个历史日志


def get_log_path(memory_root: str = None) -> Optional[Path]:
    """
    获取日志文件路径
    
    Args:
        memory_root: 记忆目录路径 (.promem/memory)
    
    Returns:
        日志文件路径或 None
    """
    if memory_root:
        # memory_root 是 .promem/memory，取 .promem/
        promem_dir = Path(memory_root).parent
        if promem_dir.name == '.promem':
            return promem_dir / 'promem.log'
        # 如果传入的不是 memory 目录，尝试直接使用
        if promem_dir.exists() and (promem_dir / '.promem').is_dir():
            return promem_dir / '.promem' / 'promem.log'
        # 可能传入的就是 .promem 目录
        if Path(memory_root).name == '.promem':
            return Path(memory_root) / 'promem.log'
    
    # 从 cwd 向上查找 .promem/
    cwd = Path.cwd()
    while cwd != cwd.parent:
        if (cwd / '.promem').is_dir():
            return cwd / '.promem' / 'promem.log'
        cwd = cwd.parent
    
    return None


def rotate_log(log_path: Path) -> None:
    """
    日志轮转
    
    当日志文件超过 MAX_LOG_SIZE 时，进行轮转：
    .log.2 → .log.3, .log.1 → .log.2, .log → .log.1
    """
    if not log_path.exists():
        return
    
    try:
        if log_path.stat().st_size < MAX_LOG_SIZE:
            return
    except Exception:
        return
    
    # 轮转: .log.2 → .log.3, .log.1 → .log.2, .log → .log.1
    for i in range(MAX_LOG_FILES, 0, -1):
        old = log_path.parent / f'{log_path.stem}.log.{i}'
        new = log_path.parent / f'{log_path.stem}.log.{i+1}'
        if i == MAX_LOG_FILES and old.exists():
            try:
                old.unlink()
            except Exception:
                pass
        elif old.exists():
            try:
                old.rename(new)
            except Exception:
                pass
    
    try:
        log_path.rename(log_path.parent / f'{log_path.stem}.log.1')
    except Exception:
        pass


def write_log(
    event_type: str,
    module: str,
    summary: str,
    memory_root: str = None,
    **kwargs
) -> None:
    """
    写入结构化日志
    
    格式: [时间戳] 事件类型 模块 | 摘要 | key1=value1 key2=value2 ...
    
    Args:
        event_type: CAPTURE/SKIP/CLASSIFY/DUPLICATE/SEARCH/COMPACT/ARCHIVE/EVOLVE/ERROR
        module: capture/index/compact/evolve/importance
        summary: 事件摘要
        memory_root: 记忆目录路径
        **kwargs: 结构化字段（key=value）
    
    日志写入失败不影响主流程
    """
    log_path = get_log_path(memory_root)
    if not log_path:
        return
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 构建 key=value 部分
    kv_parts = []
    for k, v in kwargs.items():
        if v is None:
            continue
        if isinstance(v, list):
            # 列表最多显示 5 项
            v_str = '[' + ','.join(str(i) for i in v[:5])
            if len(v) > 5:
                v_str += ',...'
            v_str += ']'
            kv_parts.append(f'{k}={v_str}')
        elif isinstance(v, float):
            kv_parts.append(f'{k}={v:.2f}')
        else:
            kv_parts.append(f'{k}={v}')
    kv_str = ' '.join(kv_parts)
    
    line = f'[{timestamp}] {event_type} {module} | {summary}'
    if kv_str:
        line += f' | {kv_str}'
    line += '\n'
    
    try:
        # 确保日志目录存在
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 检查是否需要轮转
        rotate_log(log_path)
        
        # 写入日志（使用文件锁防止并发冲突）
        with open(log_path, 'a', encoding='utf-8') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(line)
            fcntl.flock(f, fcntl.LOCK_UN)
    except Exception:
        pass  # 日志写入失败不影响主流程


# ============== 内置默认敏感信息模式 ==============
DEFAULT_SENSITIVE_PATTERNS = [
    r'(?i)api[_-]?key\s*[:=]\s*\S+',
    r'(?i)password\s*[:=]\s*\S+',
    r'(?i)secret\s*[:=]\s*\S+',
    r'(?i)token\s*[:=]\s*\S+',
    r'(?i)auth[_-]?token\s*[:=]\s*\S+',
    r'(?i)access[_-]?key\s*[:=]\s*\S+',
    r'(?i)private[_-]?key\s*[:=]\s*\S+',
    r'(?i)credentials?\s*[:=]\s*\S+',
    # AWS
    r'AKIA[0-9A-Z]{16}',
    r'(?i)aws[_-]?secret\s*[:=]\s*\S+',
    # 通用密钥格式
    r'["\']?[a-zA-Z0-9_-]*(?:key|secret|token|password|pwd|passwd)["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
]


def parse_yaml_simple(content: str) -> Dict[str, Any]:
    """
    简单的 YAML 解析器，仅支持基础格式
    支持：嵌套字典、列表、字符串、数字、布尔值
    """
    result: Dict[str, Any] = {}
    current_section: Optional[str] = None
    current_subsection: Optional[str] = None
    current_list: Optional[List[str]] = None

    for line in content.split('\n'):
        # 跳过空行和注释
        if not line.strip() or line.strip().startswith('#'):
            continue

        # 计算缩进级别
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # 处理列表项
        if stripped.startswith('- '):
            if current_list is not None:
                value = stripped[2:].strip().strip('"\'')
                current_list.append(value)
            continue

        # 检查是否是键值对
        if ':' in stripped:
            key_part = stripped.split(':', 1)
            key = key_part[0].strip()
            value = key_part[1].strip() if len(key_part) > 1 else ''

            # 顶级 section (无缩进)
            if indent == 0:
                current_section = key
                current_subsection = None
                current_list = None
                if value:
                    result[key] = _parse_value(value)
                else:
                    result[key] = {}
            # 二级 section (2 空格缩进)
            elif indent == 2 and current_section:
                current_subsection = key
                current_list = None
                if value:
                    if isinstance(result.get(current_section), dict):
                        result[current_section][key] = _parse_value(value)
                else:
                    # 可能是列表的开始
                    if isinstance(result.get(current_section), dict):
                        result[current_section][key] = []
                        current_list = result[current_section][key]
            # 三级 section (4 空格缩进)
            elif indent == 4 and current_section and current_subsection:
                if isinstance(result.get(current_section), dict):
                    if isinstance(result[current_section].get(current_subsection), dict):
                        result[current_section][current_subsection][key] = _parse_value(value)
                    else:
                        result[current_section][current_subsection] = {key: _parse_value(value)}

    return result


def _parse_value(value: str) -> Any:
    """解析 YAML 值"""
    value = value.strip()

    # 去除注释
    if '#' in value:
        value = value.split('#')[0].strip()

    # 去除引号
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]

    # 布尔值
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False

    # 数字
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    return value


def load_config(promem_root: Path) -> Dict[str, Any]:
    """
    加载 ProMem 配置
    
    Args:
        promem_root: .promem 目录路径或仓库根目录
    
    Returns:
        配置字典，包含 capture 等配置节
    """
    default_config = {
        'capture': {
            'max_per_session': 5,
            'similarity_threshold': 0.95,
            'sensitive_patterns': DEFAULT_SENSITIVE_PATTERNS.copy()
        }
    }

    # 支持传入 .promem 目录或仓库根目录
    if promem_root.name == '.promem':
        config_path = promem_root / 'config.yaml'
    else:
        config_path = promem_root / '.promem' / 'config.yaml'

    if not config_path.exists():
        log_info("config.yaml 不存在，使用默认配置")
        return default_config

    try:
        content = config_path.read_text(encoding='utf-8')
        # 尝试使用 PyYAML
        try:
            import yaml
            config = yaml.safe_load(content)
            if config:
                # 确保 capture 配置有默认值
                if 'capture' not in config:
                    config['capture'] = {}
                capture = config['capture']
                if 'sensitive_patterns' not in capture or not capture['sensitive_patterns']:
                    capture['sensitive_patterns'] = DEFAULT_SENSITIVE_PATTERNS.copy()
                if 'similarity_threshold' not in capture:
                    capture['similarity_threshold'] = 0.95
                if 'max_per_session' not in capture:
                    capture['max_per_session'] = 5
                return config
        except ImportError:
            pass

        # 回退到简单解析
        config = parse_yaml_simple(content)
        if config:
            if 'capture' not in config:
                config['capture'] = {}
            capture = config['capture']
            if 'sensitive_patterns' not in capture or not capture['sensitive_patterns']:
                capture['sensitive_patterns'] = DEFAULT_SENSITIVE_PATTERNS.copy()
            if 'similarity_threshold' not in capture:
                capture['similarity_threshold'] = 0.95
            if 'max_per_session' not in capture:
                capture['max_per_session'] = 5
            return config

        return default_config
    except Exception as e:
        log_info(f"读取 config.yaml 失败: {e}，使用默认配置")
        return default_config


def sanitize_sensitive(text: str, patterns: Optional[List[str]] = None) -> str:
    """
    脱敏敏感信息
    
    Args:
        text: 待脱敏文本
        patterns: 敏感信息正则模式列表，为 None 时使用默认模式
    
    Returns:
        脱敏后的文本，敏感信息被替换为 [REDACTED]
    """
    if patterns is None:
        patterns = DEFAULT_SENSITIVE_PATTERNS
    
    result = text
    redacted_count = 0
    
    for pattern in patterns:
        try:
            new_result = re.sub(pattern, '[REDACTED]', result)
            if new_result != result:
                redacted_count += 1
            result = new_result
        except re.error as e:
            log_warn(f"敏感信息正则模式无效: {pattern} - {e}")
            continue
    
    if redacted_count > 0:
        log_info(f"已脱敏 {redacted_count} 处敏感信息")
    
    return result


def extract_content_summary(content: str, max_chars: int = 200) -> str:
    """
    提取内容摘要用于相似度比较
    
    提取标题（# 开头的行）+ 前 N 字符正文
    """
    lines = content.split('\n')
    title = ""
    body_start = 0
    
    # 查找第一个标题
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#'):
            title = stripped.lstrip('#').strip()
            body_start = i + 1
            break
    
    # 提取正文前 N 字符
    body_lines = lines[body_start:]
    body_text = '\n'.join(body_lines)
    # 去除 Markdown 语法噪音
    body_text = re.sub(r'[#*_`\[\]()>-]', ' ', body_text)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    body_text = body_text[:max_chars]
    
    return f"{title} {body_text}".strip()


def calculate_similarity(text1: str, text2: str) -> float:
    """
    计算两段文本的相似度
    
    使用 difflib.SequenceMatcher（标准库，无需额外依赖）
    
    Returns:
        相似度分数 0.0 ~ 1.0
    """
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def is_duplicate(
    new_content: str,
    category_dir: str,
    threshold: float = 0.95
) -> Tuple[bool, Optional[str], float]:
    """
    检查新内容是否与已有记忆重复
    
    策略（M2 阶段，无向量时的简化方案）：
    1. 遍历 category_dir 下所有 .md 文件
    2. 提取每个文件的标题和核心内容
    3. 使用文本相似度（基于 SequenceMatcher）判断
    4. 如果相似度 > threshold，视为重复
    
    注意：M2 后续有了向量索引后可以升级为向量相似度。
    
    Args:
        new_content: 新内容
        category_dir: 分类目录路径
        threshold: 相似度阈值（默认 0.95）
    
    Returns:
        (is_dup: bool, similar_file: str or None, similarity: float)
    """
    category_path = Path(category_dir)
    
    if not category_path.exists():
        return (False, None, 0.0)
    
    new_summary = extract_content_summary(new_content)
    
    if not new_summary:
        return (False, None, 0.0)
    
    highest_similarity = 0.0
    most_similar_file: Optional[str] = None
    
    for md_file in category_path.glob('*.md'):
        try:
            existing_content = md_file.read_text(encoding='utf-8')
            existing_summary = extract_content_summary(existing_content)
            
            similarity = calculate_similarity(new_summary, existing_summary)
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_file = md_file.name
                
            # 如果已找到重复，可以提前返回
            if similarity > threshold:
                log_warn(f"发现重复内容: 与 {md_file.name} 相似度 {similarity:.2%}")
                return (True, md_file.name, similarity)
                
        except Exception as e:
            log_warn(f"读取文件 {md_file.name} 失败: {e}")
            continue
    
    return (False, most_similar_file, highest_similarity)


def generate_filename(description: str, date: Optional[str] = None) -> str:
    """
    生成标准文件名 YYYY-MM-DD-{slug}.md
    
    Args:
        description: 描述文本（用于生成 slug）
        date: 日期字符串，为 None 时使用当前日期
    
    Returns:
        标准格式的文件名
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # 取第一行作为标题
    first_line = description.split('\n')[0].strip()
    
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
        slug = 'memory'
    
    return f"{date}-{slug}.md"


def check_session_limit(
    category_dir: str,
    max_per_session: int = 5,
    session_date: Optional[str] = None
) -> Tuple[bool, int]:
    """
    检查今日沉淀是否已达上限
    
    统计 category_dir 下今日创建的文件数
    
    Args:
        category_dir: 分类目录路径
        max_per_session: 单次会话最大沉淀条数（默认 5）
        session_date: 会话日期，为 None 时使用当前日期
    
    Returns:
        (is_exceeded: bool, current_count: int)
    """
    if session_date is None:
        session_date = datetime.now().strftime('%Y-%m-%d')
    
    category_path = Path(category_dir)
    
    if not category_path.exists():
        return (False, 0)
    
    # 统计今日文件数
    today_count = 0
    for md_file in category_path.glob('*.md'):
        # 文件名格式: YYYY-MM-DD-xxx.md
        if md_file.name.startswith(session_date):
            today_count += 1
    
    is_exceeded = today_count >= max_per_session
    
    if is_exceeded:
        log_warn(f"今日沉淀已达上限: {today_count}/{max_per_session}")
    
    return (is_exceeded, today_count)


def check_global_session_limit(
    memory_root: str,
    max_per_session: int = 5,
    session_date: Optional[str] = None
) -> Tuple[bool, int]:
    """
    检查今日全局沉淀是否已达上限
    
    统计 memory_root 下所有子目录今日创建的文件总数
    
    Args:
        memory_root: 记忆根目录路径（.promem/memory）
        max_per_session: 单次会话最大沉淀条数（默认 5）
        session_date: 会话日期，为 None 时使用当前日期
    
    Returns:
        (is_exceeded: bool, current_count: int)
    """
    if session_date is None:
        session_date = datetime.now().strftime('%Y-%m-%d')
    
    memory_path = Path(memory_root)
    
    if not memory_path.exists():
        return (False, 0)
    
    # 统计所有子目录今日文件数
    today_count = 0
    for category_dir in memory_path.iterdir():
        if category_dir.is_dir():
            for md_file in category_dir.glob('*.md'):
                if md_file.name.startswith(session_date):
                    today_count += 1
    
    is_exceeded = today_count >= max_per_session
    
    if is_exceeded:
        log_warn(f"今日全局沉淀已达上限: {today_count}/{max_per_session}")
    
    return (is_exceeded, today_count)


# ============== 导出的公共接口 ==============
__all__ = [
    'load_config',
    'sanitize_sensitive',
    'is_duplicate',
    'generate_filename',
    'check_session_limit',
    'check_global_session_limit',
    'calculate_similarity',
    'extract_content_summary',
    'log_info',
    'log_warn',
    'write_log',
    'get_log_path',
    'DEFAULT_SENSITIVE_PATTERNS',
]
