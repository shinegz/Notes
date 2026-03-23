#!/usr/bin/env python3
"""
evolve.py - ProMem 规则进化引擎

分析记忆中的重复模式，发现可以提炼为团队规则或模式的知识。
实现 OpenClaw 自我进化机制中的"进化（Evolve）"阶段。

返回码：
  0 - 有建议生成
  1 - 无建议
  2 - 执行错误
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 导入共享模块
from memory_utils import (
    load_config as load_config_utils,
    calculate_similarity,
    extract_content_summary,
    log_info,
    log_warn,
    write_log,
)


# ============================================================================
# 日志函数
# ============================================================================

def log_error(msg: str) -> None:
    """输出错误日志到 stderr"""
    print(f"[ERROR] {msg}", file=sys.stderr)


# ============================================================================
# 配置加载
# ============================================================================

def load_config(promem_root: Path) -> Dict[str, Any]:
    """
    加载 ProMem 配置，返回 evolve 相关配置
    """
    default_config = {
        'evolve': {
            'decision_threshold': 3,
            'bug_threshold': 2,
            'require_approval': True,
        }
    }
    
    config = load_config_utils(promem_root)
    
    # 确保 evolve 配置存在
    if 'evolve' not in config:
        config['evolve'] = default_config['evolve']
    else:
        evolve = config['evolve']
        if 'decision_threshold' not in evolve:
            evolve['decision_threshold'] = 3
        if 'bug_threshold' not in evolve:
            evolve['bug_threshold'] = 2
        if 'require_approval' not in evolve:
            evolve['require_approval'] = True
    
    return config


# ============================================================================
# 文件解析
# ============================================================================

def parse_memory_file(file_path: Path) -> Dict[str, Any]:
    """
    解析单个记忆文件，提取元数据
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        content = ""
    
    # 提取标题：第一个 # 开头的行
    title = ""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    if not title:
        title = file_path.stem
    
    # 提取日期：从文件名 YYYY-MM-DD 前缀提取
    date = None
    date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})')
    match = date_pattern.match(file_path.name)
    if match:
        date = match.group(1)
    else:
        # 尝试从内容中提取日期
        date_section_pattern = re.compile(r'##\s*日期\s*\n+(.+)', re.MULTILINE)
        match = date_section_pattern.search(content)
        if match:
            potential_date = match.group(1).strip()
            if re.match(r'\d{4}-\d{2}-\d{2}', potential_date):
                date = potential_date[:10]
    
    # 提取标签（如果有 ## 标签 部分）
    tags = []
    tags_pattern = re.compile(r'##\s*标签\s*\n+([\s\S]*?)(?=\n##|\Z)', re.MULTILINE)
    match = tags_pattern.search(content)
    if match:
        tags_text = match.group(1)
        for line in tags_text.split('\n'):
            line = line.strip()
            if line.startswith('-'):
                tags.append(line[1:].strip())
    
    # 提取关键词（从标题和内容）
    keywords = extract_keywords(title + ' ' + content[:500])
    
    return {
        'file_path': str(file_path),
        'file_name': file_path.name,
        'title': title,
        'content': content,
        'date': date,
        'tags': tags,
        'keywords': keywords,
    }


def extract_keywords(text: str) -> List[str]:
    """
    从文本中提取关键词（简单分词）
    """
    # 去除 Markdown 语法
    text = re.sub(r'[#*_`\[\]()>-]', ' ', text)
    # 分词
    words = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
    # 过滤停用词
    stopwords = {'的', '是', '在', '和', '了', '与', '或', '等', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'for', 'of', 'in', 'on', 'at'}
    keywords = [w for w in words if len(w) > 1 and w not in stopwords]
    # 去重并保持顺序
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    return unique_keywords[:20]


# ============================================================================
# 相似度聚类
# ============================================================================

def cluster_by_similarity(
    items: List[Dict[str, Any]],
    threshold: float = 0.4
) -> List[List[Dict[str, Any]]]:
    """
    用简单的贪心聚类：
    1. 对每个 item，计算与已有聚类中心的相似度
    2. 如果最高相似度 > threshold，加入该聚类
    3. 否则创建新聚类
    
    使用 difflib.SequenceMatcher 计算相似度
    """
    if not items:
        return []
    
    clusters: List[List[Dict[str, Any]]] = []
    cluster_centers: List[str] = []  # 每个聚类的中心文本
    
    for item in items:
        # 构建用于比较的文本（标题 + 关键词）
        item_text = item.get('title', '') + ' ' + ' '.join(item.get('keywords', []))
        
        best_cluster_idx = -1
        best_similarity = 0.0
        
        # 找到最相似的聚类
        for idx, center in enumerate(cluster_centers):
            similarity = calculate_similarity(item_text, center)
            if similarity > best_similarity:
                best_similarity = similarity
                best_cluster_idx = idx
        
        # 如果相似度超过阈值，加入该聚类
        if best_similarity >= threshold and best_cluster_idx >= 0:
            clusters[best_cluster_idx].append(item)
            # 更新聚类中心（简单追加）
            cluster_centers[best_cluster_idx] += ' ' + item_text
        else:
            # 创建新聚类
            clusters.append([item])
            cluster_centers.append(item_text)
    
    return clusters


# ============================================================================
# 模式检测
# ============================================================================

def scan_category_files(memory_root: Path, category: str) -> List[Dict[str, Any]]:
    """扫描指定分类目录下的所有记忆文件"""
    category_dir = memory_root / category
    files = []
    
    if not category_dir.exists():
        return files
    
    for file_path in category_dir.glob('*.md'):
        if file_path.name != '.gitkeep':
            doc = parse_memory_file(file_path)
            doc['category'] = category
            files.append(doc)
    
    return files


def detect_decision_patterns(
    memory_root: Path,
    threshold: int = 3,
    similarity_threshold: float = 0.4
) -> List[Dict[str, Any]]:
    """
    检测重复的决策模式。
    
    流程：
    1. 遍历 memory/decisions/ 下所有文件
    2. 提取每个决策的标题和关键词
    3. 用文本相似度聚类（SequenceMatcher）
    4. 同一聚类中决策数 >= threshold → 生成规则建议
    """
    decisions = scan_category_files(memory_root, 'decisions')
    
    if len(decisions) < threshold:
        return []
    
    # 聚类
    clusters = cluster_by_similarity(decisions, similarity_threshold)
    
    # 筛选达到阈值的聚类
    suggestions = []
    for cluster in clusters:
        if len(cluster) >= threshold:
            # 提取共同模式
            pattern = extract_common_pattern(cluster)
            
            suggestion = {
                'id': generate_suggestion_id(),
                'type': 'rule',
                'pattern': pattern,
                'evidence': [
                    {
                        'file': doc['file_name'],
                        'title': doc['title'],
                        'date': doc.get('date', ''),
                    }
                    for doc in cluster
                ],
                'suggested_rule': generate_rule_suggestion(pattern, cluster),
                'confidence': calculate_confidence(cluster),
                'target': 'RULES.md',
            }
            suggestions.append(suggestion)
    
    return suggestions


def detect_bug_patterns(
    memory_root: Path,
    threshold: int = 2,
    similarity_threshold: float = 0.4
) -> List[Dict[str, Any]]:
    """
    检测重复的 Bug 模式。
    
    流程：
    1. 遍历 memory/bugs/ 下所有文件
    2. 提取 Bug 标题、原因、标签
    3. 聚类相似 Bug
    4. 同一聚类中 Bug 数 >= threshold → 生成模式建议
    """
    bugs = scan_category_files(memory_root, 'bugs')
    
    if len(bugs) < threshold:
        return []
    
    # 聚类
    clusters = cluster_by_similarity(bugs, similarity_threshold)
    
    # 筛选达到阈值的聚类
    suggestions = []
    for cluster in clusters:
        if len(cluster) >= threshold:
            # 提取共同模式
            pattern = extract_common_pattern(cluster)
            
            suggestion = {
                'id': generate_suggestion_id(),
                'type': 'pattern',
                'pattern': pattern,
                'evidence': [
                    {
                        'file': doc['file_name'],
                        'title': doc['title'],
                        'date': doc.get('date', ''),
                    }
                    for doc in cluster
                ],
                'suggested_pattern': generate_pattern_suggestion(pattern, cluster),
                'confidence': calculate_confidence(cluster),
                'target': 'PATTERNS.md',
            }
            suggestions.append(suggestion)
    
    return suggestions


def detect_rule_candidates(
    memory_root: Path,
    threshold: int = 2,
    similarity_threshold: float = 0.5
) -> List[Dict[str, Any]]:
    """
    从 rules/ 目录检测可以提升为正式规则的隐式约束。
    
    如果同一约束在多个文件中出现，建议写入 RULES.md。
    """
    rules = scan_category_files(memory_root, 'rules')
    
    if len(rules) < threshold:
        return []
    
    # 聚类
    clusters = cluster_by_similarity(rules, similarity_threshold)
    
    # 筛选达到阈值的聚类
    suggestions = []
    for cluster in clusters:
        if len(cluster) >= threshold:
            pattern = extract_common_pattern(cluster)
            
            suggestion = {
                'id': generate_suggestion_id(),
                'type': 'rule',
                'pattern': pattern,
                'evidence': [
                    {
                        'file': doc['file_name'],
                        'title': doc['title'],
                        'date': doc.get('date', ''),
                    }
                    for doc in cluster
                ],
                'suggested_rule': generate_rule_suggestion(pattern, cluster),
                'confidence': calculate_confidence(cluster),
                'target': 'RULES.md',
            }
            suggestions.append(suggestion)
    
    return suggestions


def extract_common_pattern(cluster: List[Dict[str, Any]]) -> str:
    """从聚类中提取共同模式描述"""
    if not cluster:
        return "未知模式"
    
    # 收集所有关键词
    all_keywords: Dict[str, int] = {}
    for doc in cluster:
        for kw in doc.get('keywords', []):
            all_keywords[kw] = all_keywords.get(kw, 0) + 1
    
    # 按频率排序，取前 3 个最常见的
    sorted_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, _ in sorted_keywords[:3]]
    
    # 如果有足够的关键词，生成模式描述
    if top_keywords:
        return ' - '.join(top_keywords)
    
    # 回退：使用第一个文档的标题
    return cluster[0].get('title', '未知模式')[:50]


def generate_rule_suggestion(pattern: str, cluster: List[Dict[str, Any]]) -> str:
    """生成规则建议文本"""
    # 从聚类中提取共同主题
    titles = [doc.get('title', '') for doc in cluster]
    
    # 简单的规则生成：基于模式描述
    return f"团队规则: {pattern}"


def generate_pattern_suggestion(pattern: str, cluster: List[Dict[str, Any]]) -> str:
    """生成模式建议文本"""
    return f"常见问题模式: {pattern}"


def calculate_confidence(cluster: List[Dict[str, Any]]) -> float:
    """计算建议的置信度"""
    # 简单的置信度计算：基于聚类大小和相似度
    base_confidence = 0.6
    
    # 聚类越大，置信度越高
    size_bonus = min(len(cluster) * 0.1, 0.3)
    
    # 计算聚类内部的平均相似度
    if len(cluster) > 1:
        similarities = []
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                text_i = cluster[i].get('title', '') + ' '.join(cluster[i].get('keywords', []))
                text_j = cluster[j].get('title', '') + ' '.join(cluster[j].get('keywords', []))
                similarities.append(calculate_similarity(text_i, text_j))
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0.5
        similarity_bonus = avg_similarity * 0.1
    else:
        similarity_bonus = 0
    
    confidence = base_confidence + size_bonus + similarity_bonus
    return min(round(confidence, 2), 0.99)


# ============================================================================
# 建议生成与存储
# ============================================================================

_suggestion_counter = 0

def generate_suggestion_id() -> str:
    """生成唯一的建议 ID"""
    global _suggestion_counter
    _suggestion_counter += 1
    return f"SUG-{_suggestion_counter:03d}"


def reset_suggestion_counter() -> None:
    """重置建议计数器（用于测试）"""
    global _suggestion_counter
    _suggestion_counter = 0


def save_suggestion(suggestion: Dict[str, Any], memory_root: Path) -> str:
    """
    将建议保存为 Markdown 文件。
    
    返回保存的文件路径
    """
    suggestions_dir = memory_root / 'suggestions'
    suggestions_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', suggestion['pattern'])
    slug = re.sub(r'\s+', '-', slug).lower()[:30]
    filename = f"{date_str}-{suggestion['id']}-{slug}.md"
    
    file_path = suggestions_dir / filename
    
    # 生成内容
    content = generate_suggestion_markdown(suggestion)
    
    # 写入文件
    file_path.write_text(content, encoding='utf-8')
    
    return str(file_path)


def generate_suggestion_markdown(suggestion: Dict[str, Any]) -> str:
    """生成建议的 Markdown 内容"""
    suggestion_type = '规则' if suggestion['type'] == 'rule' else '模式'
    target = suggestion.get('target', 'RULES.md')
    confidence = suggestion.get('confidence', 0.0)
    
    # 证据表格
    evidence_rows = []
    for idx, ev in enumerate(suggestion.get('evidence', []), 1):
        evidence_rows.append(
            f"| {idx} | {ev.get('file', '')} | {ev.get('title', '')[:40]} | {ev.get('date', '')} |"
        )
    evidence_table = '\n'.join(evidence_rows)
    
    # 建议内容
    if suggestion['type'] == 'rule':
        suggestion_content = suggestion.get('suggested_rule', '')
    else:
        suggestion_content = suggestion.get('suggested_pattern', '')
    
    content = f"""# 进化建议: {suggestion['pattern']}

- ID: {suggestion['id']}
- 类型: {suggestion_type}
- 目标: {target}
- 置信度: {confidence:.0%}
- 状态: pending
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 证据

| # | 来源文件 | 标题 | 日期 |
|---|---------|------|------|
{evidence_table}

## 建议内容

{suggestion_content}
"""
    return content


def load_suggestion(file_path: Path) -> Optional[Dict[str, Any]]:
    """从文件加载建议"""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return None
    
    suggestion: Dict[str, Any] = {
        'file_path': str(file_path),
        'file_name': file_path.name,
    }
    
    # 解析 ID
    id_match = re.search(r'- ID:\s*(\S+)', content)
    if id_match:
        suggestion['id'] = id_match.group(1)
    
    # 解析类型
    type_match = re.search(r'- 类型:\s*(\S+)', content)
    if type_match:
        type_str = type_match.group(1)
        suggestion['type'] = 'rule' if type_str == '规则' else 'pattern'
    
    # 解析目标
    target_match = re.search(r'- 目标:\s*(\S+)', content)
    if target_match:
        suggestion['target'] = target_match.group(1)
    
    # 解析置信度
    conf_match = re.search(r'- 置信度:\s*(\d+)%', content)
    if conf_match:
        suggestion['confidence'] = int(conf_match.group(1)) / 100
    
    # 解析状态
    status_match = re.search(r'- 状态:\s*(\S+)', content)
    if status_match:
        suggestion['status'] = status_match.group(1)
    
    # 解析生成时间
    time_match = re.search(r'- 生成时间:\s*(.+)', content)
    if time_match:
        suggestion['created_at'] = time_match.group(1).strip()
    
    # 解析模式（从标题）
    title_match = re.search(r'^# 进化建议:\s*(.+)', content, re.MULTILINE)
    if title_match:
        suggestion['pattern'] = title_match.group(1).strip()
    
    # 解析建议内容
    content_match = re.search(r'## 建议内容\s*\n+([\s\S]*?)(?=\n##|\Z)', content)
    if content_match:
        suggestion['content'] = content_match.group(1).strip()
    
    # 解析证据数量
    evidence_count = len(re.findall(r'\|\s*\d+\s*\|', content))
    suggestion['evidence_count'] = evidence_count
    
    return suggestion


def list_suggestions(memory_root: Path) -> List[Dict[str, Any]]:
    """列出所有建议"""
    suggestions_dir = memory_root / 'suggestions'
    
    if not suggestions_dir.exists():
        return []
    
    suggestions = []
    for file_path in sorted(suggestions_dir.glob('*.md')):
        suggestion = load_suggestion(file_path)
        if suggestion:
            suggestions.append(suggestion)
    
    return suggestions


def update_suggestion_status(file_path: Path, new_status: str) -> bool:
    """更新建议状态"""
    try:
        content = file_path.read_text(encoding='utf-8')
        new_content = re.sub(
            r'(- 状态:\s*)\S+',
            f'\\1{new_status}',
            content
        )
        file_path.write_text(new_content, encoding='utf-8')
        return True
    except Exception:
        return False


# ============================================================================
# 应用建议
# ============================================================================

def apply_suggestion(
    suggestion_id: str,
    memory_root: Path,
    promem_root: Path
) -> int:
    """
    将审核通过的建议写入 RULES.md 或 PATTERNS.md。
    
    返回：
      0 - 成功
      1 - 建议不存在或状态不是 pending
      2 - 写入失败
    """
    # 查找建议文件
    suggestions_dir = memory_root / 'suggestions'
    target_file = None
    suggestion = None
    
    for file_path in suggestions_dir.glob('*.md'):
        loaded = load_suggestion(file_path)
        if loaded and loaded.get('id') == suggestion_id:
            target_file = file_path
            suggestion = loaded
            break
    
    if not suggestion or not target_file:
        log_error(f"找不到建议: {suggestion_id}")
        return 1
    
    # 检查状态
    if suggestion.get('status') != 'pending':
        log_error(f"建议状态不是 pending: {suggestion.get('status')}")
        return 1
    
    # 确定目标文件
    target_name = suggestion.get('target', 'RULES.md')
    target_path = promem_root / target_name
    
    # 生成要追加的内容
    if suggestion['type'] == 'rule':
        append_content = generate_rule_content(suggestion)
    else:
        append_content = generate_pattern_content(suggestion)
    
    # 写入目标文件
    try:
        if target_path.exists():
            existing_content = target_path.read_text(encoding='utf-8')
        else:
            existing_content = ""
        
        # 确保有换行分隔
        if existing_content and not existing_content.endswith('\n'):
            existing_content += '\n'
        
        new_content = existing_content + '\n' + append_content
        target_path.write_text(new_content, encoding='utf-8')
        
        # 更新建议状态
        update_suggestion_status(target_file, 'approved')
        
        log_info(f"已将建议 {suggestion_id} 写入 {target_name}")
        return 0
    
    except Exception as e:
        log_error(f"写入失败: {e}")
        return 2


def generate_rule_content(suggestion: Dict[str, Any]) -> str:
    """生成要写入 RULES.md 的内容"""
    pattern = suggestion.get('pattern', '未知规则')
    content = suggestion.get('content', '')
    confidence = suggestion.get('confidence', 0.0)
    evidence_count = suggestion.get('evidence_count', 0)
    
    return f"""## {pattern}

> 来源: 从 {evidence_count} 条决策记录中提炼
> 置信度: {confidence:.0%}
> 添加时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{content}

---
"""


def generate_pattern_content(suggestion: Dict[str, Any]) -> str:
    """生成要写入 PATTERNS.md 的内容"""
    pattern = suggestion.get('pattern', '未知模式')
    content = suggestion.get('content', '')
    confidence = suggestion.get('confidence', 0.0)
    evidence_count = suggestion.get('evidence_count', 0)
    
    return f"""## {pattern}

> 来源: 从 {evidence_count} 条 Bug 记录中提炼
> 置信度: {confidence:.0%}
> 添加时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**模式**: {pattern}
**建议**: {content}

---
"""


# ============================================================================
# 输出格式化
# ============================================================================

def print_check_report(
    memory_root: Path,
    suggestions: List[Dict[str, Any]],
    stats: Dict[str, int]
) -> None:
    """打印 --check 报告"""
    print("[ProMem] 📊 进化分析报告")
    print("================================")
    print()
    print("🔍 分析范围:")
    for category, count in stats.items():
        print(f"  - {category}/: {count} 条记录")
    print()
    
    if not suggestions:
        print("📋 未发现进化建议")
    else:
        print(f"📋 发现 {len(suggestions)} 条进化建议:")
        print()
        
        for sug in suggestions:
            type_label = '规则' if sug['type'] == 'rule' else '模式'
            confidence = sug.get('confidence', 0) * 100
            evidence_count = len(sug.get('evidence', []))
            
            print(f"  {sug['id']} [{type_label}] 置信度: {confidence:.0f}%")
            print(f"  模式: {sug['pattern']}")
            print(f"  证据: {evidence_count} 条{'决策' if sug['type'] == 'rule' else 'Bug'}记录")
            print(f"  目标: {sug.get('target', 'RULES.md')}")
            print()
    
    print("💡 使用 `python3 evolve.py --apply SUG-001` 将建议写入规则文件")
    print("================================")


def print_history_report(suggestions: List[Dict[str, Any]]) -> None:
    """打印 --history 报告"""
    print("[ProMem] 📜 进化建议历史")
    print("================================")
    print()
    
    if not suggestions:
        print("暂无历史建议")
    else:
        print("| ID | 类型 | 模式 | 状态 | 日期 |")
        print("|----|------|------|------|------|")
        
        for sug in suggestions:
            sug_id = sug.get('id', 'N/A')
            sug_type = 'rule' if sug.get('type') == 'rule' else 'pattern'
            pattern = sug.get('pattern', '')[:20]
            status = sug.get('status', 'pending')
            created_at = sug.get('created_at', '')[:10] if sug.get('created_at') else 'N/A'
            
            print(f"| {sug_id} | {sug_type} | {pattern} | {status} | {created_at} |")
    
    print()
    print("================================")


# ============================================================================
# 主函数
# ============================================================================

def run_check(memory_root: Path, config: Dict[str, Any]) -> Tuple[int, List[Dict[str, Any]]]:
    """运行检查模式"""
    evolve_config = config.get('evolve', {})
    decision_threshold = evolve_config.get('decision_threshold', 3)
    bug_threshold = evolve_config.get('bug_threshold', 2)
    
    # 统计各分类记录数
    stats = {}
    for category in ['decisions', 'bugs', 'rules']:
        category_dir = memory_root / category
        if category_dir.exists():
            count = len(list(category_dir.glob('*.md')))
            stats[category] = count
        else:
            stats[category] = 0
    
    # 检测模式
    reset_suggestion_counter()
    suggestions = []
    
    # 决策模式
    decision_suggestions = detect_decision_patterns(
        memory_root, threshold=decision_threshold
    )
    suggestions.extend(decision_suggestions)
    
    # Bug 模式
    bug_suggestions = detect_bug_patterns(
        memory_root, threshold=bug_threshold
    )
    suggestions.extend(bug_suggestions)
    
    # 规则候选
    rule_suggestions = detect_rule_candidates(
        memory_root, threshold=2
    )
    suggestions.extend(rule_suggestions)
    
    # 打印报告
    print_check_report(memory_root, suggestions, stats)
    
    # 保存建议
    for sug in suggestions:
        save_suggestion(sug, memory_root)
    
    # 记录进化检查日志
    if suggestions:
        write_log('EVOLVE', 'evolve', f'mode=check found={len(suggestions)}',
                  memory_root=str(memory_root),
                  mode='check',
                  patterns_found=len(suggestions),
                  suggestions_generated=len(suggestions),
                  ids=[s.get('id', '') for s in suggestions])
    
    return (0 if suggestions else 1, suggestions)


def run_analyze(memory_root: Path, config: Dict[str, Any]) -> int:
    """运行全量分析"""
    log_info("开始全量分析...")
    
    exit_code, suggestions = run_check(memory_root, config)
    
    if suggestions:
        log_info(f"分析完成，生成 {len(suggestions)} 条建议")
    else:
        log_info("分析完成，未发现可提炼的模式")
    
    return exit_code


def run_apply(suggestion_id: str, memory_root: Path, promem_root: Path) -> int:
    """运行应用模式"""
    log_info(f"应用建议: {suggestion_id}")
    result = apply_suggestion(suggestion_id, memory_root, promem_root)
    
    # 记录应用日志
    if result == 0:
        write_log('EVOLVE', 'evolve', f'mode=apply id={suggestion_id}',
                  memory_root=str(memory_root),
                  mode='apply',
                  id=suggestion_id,
                  status='approved')
    
    return result


def run_history(memory_root: Path) -> int:
    """运行历史查看"""
    suggestions = list_suggestions(memory_root)
    print_history_report(suggestions)
    return 0


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description='ProMem 规则进化引擎 - 分析记忆中的重复模式，提炼团队规则',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
返回码：
  0 - 有建议生成 / 操作成功
  1 - 无建议
  2 - 执行错误

示例:
  %(prog)s --check                          # 检查模式，输出进化建议
  %(prog)s --analyze                        # 全量分析所有分类
  %(prog)s --apply SUG-001                  # 将建议写入规则文件
  %(prog)s --history                        # 查看历史建议
  %(prog)s --check --memory-root .promem/memory  # 指定记忆目录
        """
    )
    
    # 互斥的操作模式
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--check',
        action='store_true',
        help='检查模式：分析记忆，输出进化建议（不修改任何文件）'
    )
    mode_group.add_argument(
        '--analyze',
        action='store_true',
        help='全量分析：分析所有分类'
    )
    mode_group.add_argument(
        '--apply',
        type=str,
        metavar='SUGGESTION_ID',
        help='应用模式：将已审核的建议写入 RULES.md / PATTERNS.md'
    )
    mode_group.add_argument(
        '--history',
        action='store_true',
        help='查看历史建议'
    )
    
    parser.add_argument(
        '--memory-root',
        type=str,
        default=None,
        help='记忆目录路径（默认 .promem/memory）'
    )
    
    args = parser.parse_args()
    
    try:
        # 确定路径
        script_dir = Path(__file__).parent.resolve()
        promem_root = script_dir.parent  # .promem/
        
        # 确定 memory_root
        if args.memory_root:
            memory_root = Path(args.memory_root).resolve()
        else:
            memory_root = promem_root / 'memory'
        
        # 检查目录是否存在
        if not memory_root.exists():
            log_warn(f"记忆目录不存在: {memory_root}")
            memory_root.mkdir(parents=True, exist_ok=True)
            log_info(f"已创建记忆目录: {memory_root}")
        
        # 加载配置
        config = load_config(promem_root)
        
        # 执行对应操作
        if args.check:
            exit_code, _ = run_check(memory_root, config)
            return exit_code
        
        elif args.analyze:
            return run_analyze(memory_root, config)
        
        elif args.apply:
            return run_apply(args.apply, memory_root, promem_root)
        
        elif args.history:
            return run_history(memory_root)
        
        return 0
    
    except Exception as e:
        log_error(str(e))
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
