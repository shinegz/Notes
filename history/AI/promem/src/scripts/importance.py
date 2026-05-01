#!/usr/bin/env python3
"""
ProMem Knowledge Importance & Supply Strategy

为每条记忆计算重要性分数，并实现智能供给策略——在正确的时机向开发者推送正确的知识。

公式: importance = reuse_probability × forget_risk × pitfall_cost
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, date as date_type
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# 导入共享日志模块
try:
    from history.AI.promem.src.scripts.memory_utils import write_log
except ImportError:
    def write_log(*args, **kwargs):
        pass

# ============================================================================
# 常量定义
# ============================================================================

# 分类权重（用于 reuse_probability）
CATEGORY_WEIGHTS = {
    "decisions": 0.8,
    "rules": 0.9,
    "bugs": 0.7,
    "entities": 0.6,
    "journal": 0.3,
    "summaries": 0.5,
    "uncategorized": 0.4,
}

# 分类代价（用于 pitfall_cost）
CATEGORY_COSTS = {
    "bugs": 1.0,
    "decisions": 0.8,
    "rules": 0.7,
    "entities": 0.5,
    "journal": 0.2,
    "summaries": 0.4,
    "uncategorized": 0.3,
}

# 隐式程度（用于 forget_risk）
IMPLICITNESS_SCORES = {
    "rules": 0.9,
    "entities": 0.8,
    "decisions": 0.5,
    "bugs": 0.6,
    "journal": 0.3,
    "summaries": 0.4,
    "uncategorized": 0.5,
}

# 供给时机检测关键词
TIMING_KEYWORDS = {
    "editing_file": ["编辑", "修改", "改", "文件", "edit", "modify", "更新", "update"],
    "module_first_contact": ["第一次", "首次", "不熟悉", "新模块", "first time", "new module", "初次", "初识"],
    "making_decision": ["选型", "决策", "方案", "对比", "选择", "decide", "choose", "比较", "评估"],
    "fixing_bug": ["Bug", "bug", "报错", "失败", "crash", "error", "fix", "修复", "问题", "异常", "排查"],
    "code_review": ["评审", "review", "CR", "代码检查", "code review", "审查"],
    "pre_release": ["发布", "上线", "部署", "release", "deploy", "上线前", "发布前"],
}

# 高代价关键词（用于修复难度评估）
HIGH_COST_KEYWORDS = ["困难", "复杂", "生产", "严重", "critical", "production", "hard", "complex", "紧急"]

# ============================================================================
# 工具函数
# ============================================================================

def load_yaml_simple(content: str) -> Dict[str, Any]:
    """简单的 YAML 解析（避免依赖 pyyaml）"""
    config = {}
    section_stack = []
    
    for line in content.split("\n"):
        line_stripped = line.rstrip()
        if not line_stripped or line_stripped.lstrip().startswith("#"):
            continue
        
        indent = len(line_stripped) - len(line_stripped.lstrip())
        indent_level = indent // 2
        
        if ":" not in line_stripped:
            continue
        
        key = line_stripped.split(":")[0].strip()
        value_part = line_stripped.split(":", 1)[1].strip()
        
        if "#" in value_part:
            value_part = value_part.split("#")[0].strip()
        
        def parse_value(v: str):
            if not v:
                return None
            try:
                if "." in v:
                    return float(v)
                return int(v)
            except ValueError:
                if v.lower() == "true":
                    return True
                elif v.lower() == "false":
                    return False
                return v
        
        parsed_value = parse_value(value_part)
        
        while section_stack and section_stack[-1][0] >= indent_level:
            section_stack.pop()
        
        if not section_stack:
            target_dict = config
        else:
            target_dict = section_stack[-1][1]
        
        if parsed_value is None:
            target_dict[key] = {}
            section_stack.append((indent_level, target_dict[key]))
        else:
            target_dict[key] = parsed_value
    
    return config


def load_config(promem_root: Path) -> Dict[str, Any]:
    """加载配置文件"""
    config_path = promem_root / "config.yaml"
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return load_yaml_simple(f.read())
    except Exception:
        return {}


def load_citations(memory_root: Path) -> Dict[str, Any]:
    """加载引用记录"""
    citations_path = memory_root / ".citations.json"
    if not citations_path.exists():
        return {}
    
    try:
        with open(citations_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_citations(memory_root: Path, citations: Dict[str, Any]):
    """保存引用记录"""
    citations_path = memory_root / ".citations.json"
    with open(citations_path, "w", encoding="utf-8") as f:
        json.dump(citations, f, ensure_ascii=False, indent=2)


def scan_memory_files(memory_root: Path) -> List[Path]:
    """扫描所有记忆文件"""
    files = []
    if not memory_root.exists():
        return files
    
    for path in memory_root.rglob("*.md"):
        if path.name != ".gitkeep" and not path.name.startswith("."):
            files.append(path)
    
    return files


def parse_memory_file(file_path: Path, memory_root: Path) -> Dict[str, Any]:
    """解析记忆文件，提取元数据"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        content = ""
    
    # 提取标题
    title = ""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            break
    
    if not title:
        title = file_path.stem
    
    # 提取日期
    date = None
    date_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})")
    match = date_pattern.match(file_path.name)
    if match:
        date = match.group(1)
    else:
        date_section_pattern = re.compile(r"##\s*日期\s*\n+(.+)", re.MULTILINE)
        match = date_section_pattern.search(content)
        if match:
            potential_date = match.group(1).strip()
            if re.match(r"\d{4}-\d{2}-\d{2}", potential_date):
                date = potential_date[:10]
    
    # 提取分类
    try:
        relative = file_path.relative_to(memory_root)
        parts = relative.parts
        category = parts[0] if len(parts) > 1 else "uncategorized"
    except ValueError:
        category = "uncategorized"
    
    # 相对路径
    try:
        relative_path = str(file_path.relative_to(memory_root))
    except ValueError:
        relative_path = file_path.name
    
    # 提取标签（从内容中查找 ## 标签 部分）
    tags = []
    tags_pattern = re.compile(r"##\s*标签\s*\n(.+?)(?=\n##|\Z)", re.DOTALL)
    match = tags_pattern.search(content)
    if match:
        tags_text = match.group(1)
        tags = [t.strip().strip("-").strip() for t in tags_text.split("\n") if t.strip().startswith("-")]
    
    # 检查是否已归档
    is_archived = "[ARCHIVED]" in content or "[已归档]" in content
    
    return {
        "file_path": relative_path,
        "title": title,
        "content": content,
        "date": date,
        "category": category,
        "tags": tags,
        "is_archived": is_archived,
        "content_length": len(content),
    }


def get_days_old(date_str: Optional[str]) -> int:
    """计算记忆的天数年龄"""
    if not date_str:
        return 60  # 默认给一个较大的值
    
    try:
        mem_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        return (date_type.today() - mem_date).days
    except (ValueError, TypeError):
        return 60


# ============================================================================
# 重要性评分模型
# ============================================================================

def calc_reuse_probability(memory: Dict[str, Any], citations: Dict[str, Any], max_citations: int = 10) -> Tuple[float, Dict[str, Any]]:
    """
    计算复用概率。
    
    因子：
    1. 分类权重 (40%): decisions(0.8), rules(0.9), bugs(0.7), entities(0.6), journal(0.3)
    2. 被引用次数 (30%): citation_count / max_citations（归一化）
    3. 关联记忆数 (20%): 有关联的记忆更容易被引用
    4. 标签活跃度 (10%): 标签与近期活动的匹配度
    """
    category = memory.get("category", "uncategorized")
    file_path = memory.get("file_path", "")
    tags = memory.get("tags", [])
    
    # 1. 分类权重
    category_weight = CATEGORY_WEIGHTS.get(category, 0.4)
    
    # 2. 被引用次数
    citation_info = citations.get(file_path, {})
    citation_count = citation_info.get("citation_count", 0)
    citation_normalized = min(citation_count / max_citations, 1.0) if max_citations > 0 else 0
    
    # 3. 关联记忆数（基于内容中的链接）
    content = memory.get("content", "")
    link_pattern = re.compile(r"\[.+?\]\(.+?\.md\)")
    related_count = len(link_pattern.findall(content))
    relation_score = min(related_count / 5, 1.0)  # 5个关联为满分
    
    # 4. 标签活跃度（简化：有标签得分高）
    tag_activity = 0.5 + 0.5 * min(len(tags) / 3, 1.0) if tags else 0.3
    
    score = (
        0.4 * category_weight +
        0.3 * citation_normalized +
        0.2 * relation_score +
        0.1 * tag_activity
    )
    
    factors = {
        "category_weight": category_weight,
        "citation_count": citation_count,
        "citation_normalized": round(citation_normalized, 3),
        "related_count": related_count,
        "relation_score": round(relation_score, 3),
        "has_active_tags": len(tags) > 0,
        "tag_activity": round(tag_activity, 3),
    }
    
    return round(score, 3), factors


def calc_forget_risk(memory: Dict[str, Any], team_size: int = 5) -> Tuple[float, Dict[str, Any]]:
    """
    计算遗忘风险。
    
    因子：
    1. 时间衰减 (30%): 越久远越容易遗忘（30天半衰期）
    2. 复杂度 (30%): 内容越长/越复杂越容易遗忘部分细节
    3. 隐式程度 (20%): rules/entities 比 decisions 更隐式，更容易遗忘
    4. 团队规模修正 (20%): 团队越大，知识传递损耗越大
    """
    category = memory.get("category", "uncategorized")
    date_str = memory.get("date")
    content_length = memory.get("content_length", 0)
    
    # 1. 时间衰减（30天半衰期）
    days_old = get_days_old(date_str)
    half_life = 30
    time_decay = 1.0 - (0.5 ** (days_old / half_life))  # 越久越容易遗忘
    
    # 2. 复杂度（基于内容长度）
    # 500字以下简单，2000字以上复杂
    complexity = min(content_length / 2000, 1.0)
    
    # 3. 隐式程度
    implicitness = IMPLICITNESS_SCORES.get(category, 0.5)
    
    # 4. 团队规模修正（3人为基准，每增加1人增加5%损耗）
    team_factor = min(0.2 + 0.1 * (team_size - 3), 1.0)
    team_factor = max(team_factor, 0.2)  # 最小20%
    
    score = (
        0.3 * time_decay +
        0.3 * complexity +
        0.2 * implicitness +
        0.2 * team_factor
    )
    
    factors = {
        "age_days": days_old,
        "time_decay": round(time_decay, 3),
        "content_length": content_length,
        "complexity": round(complexity, 3),
        "implicitness": round(implicitness, 3),
        "team_size": team_size,
        "team_factor": round(team_factor, 3),
    }
    
    return round(score, 3), factors


def calc_pitfall_cost(memory: Dict[str, Any], all_bugs: List[Dict[str, Any]] = None) -> Tuple[float, Dict[str, Any]]:
    """
    计算踩坑代价。
    
    因子：
    1. 分类代价 (40%): bugs(1.0), decisions(0.8), rules(0.7), entities(0.5), journal(0.2)
    2. 影响范围 (30%): 关联文件数
    3. 修复难度 (20%): 从内容中推断（关键词检测）
    4. 重复发生次数 (10%): 如果类似问题多次出现
    """
    category = memory.get("category", "uncategorized")
    content = memory.get("content", "")
    
    # 1. 分类代价
    category_cost = CATEGORY_COSTS.get(category, 0.3)
    
    # 2. 影响范围（基于内容中提到的文件/路径）
    file_pattern = re.compile(r"[\w/\\]+\.(py|js|ts|tsx|jsx|java|go|rs|md|yaml|json|sql)")
    mentioned_files = file_pattern.findall(content.lower())
    impact_scope = min(len(mentioned_files) / 10, 1.0)  # 10个文件为满分
    
    # 3. 修复难度（关键词检测）
    fix_difficulty = 0.3  # 基础分
    for keyword in HIGH_COST_KEYWORDS:
        if keyword in content.lower():
            fix_difficulty += 0.1
    fix_difficulty = min(fix_difficulty, 1.0)
    
    # 4. 重复发生次数（简化：基于标题相似度）
    recurrence = 0.0
    if all_bugs and category == "bugs":
        title = memory.get("title", "").lower()
        similar_count = 0
        for bug in all_bugs:
            if bug.get("file_path") != memory.get("file_path"):
                other_title = bug.get("title", "").lower()
                # 简单的词重叠检测
                words1 = set(title.split())
                words2 = set(other_title.split())
                if len(words1 & words2) >= 2:
                    similar_count += 1
        recurrence = min(similar_count / 3, 1.0)
    
    score = (
        0.4 * category_cost +
        0.3 * impact_scope +
        0.2 * fix_difficulty +
        0.1 * recurrence
    )
    
    factors = {
        "category_cost": category_cost,
        "mentioned_files_count": len(mentioned_files),
        "impact_scope": round(impact_scope, 3),
        "fix_difficulty": round(fix_difficulty, 3),
        "recurrence": round(recurrence, 3),
    }
    
    return round(score, 3), factors


def calculate_importance(memory: Dict[str, Any], citations: Dict[str, Any], 
                          all_bugs: List[Dict[str, Any]] = None, 
                          team_size: int = 5) -> Dict[str, Any]:
    """
    计算单条记忆的重要性分数。
    
    公式: importance = reuse_prob × forget_risk × pitfall_cost
    （使用几何平均以避免单一因子过低导致总分过低）
    
    实际使用加权平均更合理：importance = 0.4*reuse + 0.3*forget + 0.3*pitfall
    """
    reuse_prob, reuse_factors = calc_reuse_probability(memory, citations)
    forget_risk, forget_factors = calc_forget_risk(memory, team_size)
    pitfall_cost, pitfall_factors = calc_pitfall_cost(memory, all_bugs)
    
    # 使用加权平均（比乘法更稳定）
    importance = 0.4 * reuse_prob + 0.3 * forget_risk + 0.3 * pitfall_cost
    
    # 归档的记忆降权
    if memory.get("is_archived"):
        importance *= 0.3
    
    return {
        "file": memory.get("file_path", ""),
        "title": memory.get("title", ""),
        "importance": round(importance, 3),
        "breakdown": {
            "reuse_probability": reuse_prob,
            "forget_risk": forget_risk,
            "pitfall_cost": pitfall_cost,
        },
        "factors": {
            **reuse_factors,
            **forget_factors,
            **pitfall_factors,
            "is_archived": memory.get("is_archived", False),
        },
    }


# ============================================================================
# 引用追踪
# ============================================================================

def cite_memory(file_path: str, context: str, memory_root: Path) -> Dict[str, Any]:
    """记录一次引用，提升该记忆权重"""
    citations = load_citations(memory_root)
    
    if file_path not in citations:
        citations[file_path] = {
            "citation_count": 0,
            "last_cited": None,
            "cited_in_contexts": [],
        }
    
    citations[file_path]["citation_count"] += 1
    citations[file_path]["last_cited"] = datetime.now().isoformat()
    
    # 保留最近10个上下文
    contexts = citations[file_path]["cited_in_contexts"]
    if context and context not in contexts:
        contexts.append(context)
        citations[file_path]["cited_in_contexts"] = contexts[-10:]
    
    save_citations(memory_root, citations)
    
    return citations[file_path]


def archive_memory(file_path: str, memory_root: Path) -> bool:
    """标记过时，在记忆文件头部添加 [ARCHIVED] 标记"""
    full_path = memory_root / file_path
    if not full_path.exists():
        return False
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "[ARCHIVED]" in content or "[已归档]" in content:
            return True  # 已经归档
        
        # 在标题后添加归档标记
        lines = content.split("\n")
        new_lines = []
        archived = False
        
        for line in lines:
            new_lines.append(line)
            if not archived and line.startswith("# "):
                new_lines.append("")
                new_lines.append(f"**[ARCHIVED]** - 此记忆已于 {datetime.now().strftime('%Y-%m-%d')} 标记为过时")
                new_lines.append("")
                archived = True
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        
        return True
    except Exception:
        return False


def move_to_archive(file_path: str, memory_root: Path) -> bool:
    """
    将记忆文件移动到 archive 目录
    
    保留原始分类子目录结构：
    memory/decisions/xxx.md -> memory/archive/decisions/xxx.md
    """
    full_path = memory_root / file_path
    if not full_path.exists():
        return False
    
    # 解析原始分类
    parts = Path(file_path).parts
    if len(parts) < 2:
        # 没有分类目录，跳过
        return False
    
    category = parts[0]
    filename = parts[-1]
    
    # 已经在 archive 目录中，跳过
    if 'archive' in parts:
        return True
    
    # 目标路径
    archive_dir = memory_root / 'archive' / category
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest_path = archive_dir / filename
    
    # 如果目标已存在，跳过
    if dest_path.exists():
        return False
    
    try:
        shutil.move(str(full_path), str(dest_path))
        return True
    except Exception:
        return False


def get_months_old(date_str: Optional[str]) -> float:
    """计算记忆的月龄"""
    if not date_str:
        return 12.0  # 默认给一个较大的值
    
    try:
        mem_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        days_old = (date_type.today() - mem_date).days
        return days_old / 30.0
    except (ValueError, TypeError):
        return 12.0


def should_auto_archive(
    memory: Dict[str, Any],
    importance_score: float,
    citations: Dict[str, Any],
    config: Dict[str, Any]
) -> Tuple[bool, str]:
    """
    检查记忆是否应被自动归档
    
    归档条件（全部满足）：
    1. 文件年龄 > lifecycle.archive_after_months
    2. 重要性评分 < lifecycle.min_importance
    3. 最近 lifecycle.inactive_months 内未被引用
    
    Returns:
        (should_archive, reason)
    """
    lifecycle = config.get('lifecycle', {})
    archive_after_months = lifecycle.get('archive_after_months', 6)
    min_importance = lifecycle.get('min_importance', 0.3)
    inactive_months = lifecycle.get('inactive_months', 3)
    
    file_path = memory.get('file_path', '')
    date_str = memory.get('date')
    
    # 检查 1: 文件年龄
    months_old = get_months_old(date_str)
    if months_old < archive_after_months:
        return False, f"文件年龄 {months_old:.1f} 月 < {archive_after_months} 月"
    
    # 检查 2: 重要性评分
    if importance_score >= min_importance:
        return False, f"重要性 {importance_score:.2f} >= {min_importance}"
    
    # 检查 3: 最近引用时间
    citation_info = citations.get(file_path, {})
    last_cited = citation_info.get('last_cited')
    
    if last_cited:
        try:
            last_cited_date = datetime.fromisoformat(last_cited).date()
            days_since_cited = (date_type.today() - last_cited_date).days
            months_since_cited = days_since_cited / 30.0
            if months_since_cited < inactive_months:
                return False, f"最近 {months_since_cited:.1f} 月内有引用"
        except (ValueError, TypeError):
            pass
    
    # 所有条件满足
    reason = f"文件年龄 {months_old:.1f} 月, 重要性 {importance_score:.2f}, 未被引用"
    return True, reason


def auto_archive_memories(
    memory_root: Path,
    config: Dict[str, Any],
    dry_run: bool = False
) -> List[Dict[str, Any]]:
    """
    自动归档低价值老旧记忆
    
    Args:
        memory_root: 记忆根目录
        config: 配置
        dry_run: 仅预览，不实际操作
    
    Returns:
        归档结果列表
    """
    files = scan_memory_files(memory_root)
    citations = load_citations(memory_root)
    
    # 收集所有 bug 用于重要性计算
    bugs = []
    memories = []
    for file_path in files:
        memory = parse_memory_file(file_path, memory_root)
        # 跳过已在 archive 目录的文件
        if 'archive' in memory.get('file_path', '').split('/'):
            continue
        # 跳过 summaries 目录
        if 'summaries' in memory.get('file_path', '').split('/'):
            continue
        memories.append(memory)
        if memory.get('category') == 'bugs':
            bugs.append(memory)
    
    results = []
    
    # 获取归档条件配置
    lifecycle = config.get('lifecycle', {})
    archive_after_months = lifecycle.get('archive_after_months', 6)
    min_importance = lifecycle.get('min_importance', 0.3)
    inactive_months = lifecycle.get('inactive_months', 3)
    
    for memory in memories:
        # 计算重要性
        importance_result = calculate_importance(memory, citations, bugs)
        importance_score = importance_result['importance']
        
        # 检查是否应归档
        should_archive, reason = should_auto_archive(
            memory, importance_score, citations, config
        )
        
        if should_archive:
            file_path = memory.get('file_path', '')
            result = {
                'file': file_path,
                'title': memory.get('title', ''),
                'importance': importance_score,
                'reason': reason,
                'archived': False,
            }
            
            if not dry_run:
                # 实际移动文件
                success = move_to_archive(file_path, memory_root)
                result['archived'] = success
                
                # 记录归档日志
                if success:
                    months_old = get_months_old(memory.get('date'))
                    write_log('ARCHIVE', 'importance', f'{file_path}',
                              memory_root=str(memory_root),
                              file=file_path,
                              importance=importance_score,
                              age_months=round(months_old, 1),
                              reason=reason[:50])
            
            results.append(result)
    
    # 记录汇总日志
    if results and not dry_run:
        archived_count = sum(1 for r in results if r.get('archived', False))
        write_log('ARCHIVE', 'importance', f'mode=auto archived={archived_count}',
                  memory_root=str(memory_root),
                  mode='auto',
                  archived=archived_count,
                  conditions=f'age>{archive_after_months}m importance<{min_importance} inactive>{inactive_months}m')
    
    return results


# ============================================================================
# 智能供给策略
# ============================================================================

def detect_timing(context: str) -> str:
    """检测供给时机"""
    context_lower = context.lower()
    
    for timing, keywords in TIMING_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in context_lower:
                return timing
    
    return "general"


def get_supply_reason(timing: str, memory: Dict[str, Any], context: str) -> str:
    """生成供给理由"""
    category = memory.get("category", "")
    title = memory.get("title", "")
    
    reasons = {
        "editing_file": f"你正在编辑相关文件，这是相关的{category}记录",
        "module_first_contact": f"你首次接触这个模块，这是关键的{category}信息",
        "making_decision": f"你正在做技术决策，这是历史决策参考",
        "fixing_bug": f"你正在排查问题，这是相关的历史Bug记录",
        "code_review": f"代码评审中，这是相关的规则和约束",
        "pre_release": f"发布前提醒，这是需要关注的历史记录",
        "general": f"这是与当前讨论相关的{category}记录",
    }
    
    return reasons.get(timing, reasons["general"])


def suggest_knowledge(context: str, memory_root: Path, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    根据当前开发上下文，推荐最相关且最重要的知识。
    
    综合分 = relevance(检索相关度) × importance(重要性分数)
    """
    # 检测供给时机
    timing = detect_timing(context)
    
    # 加载所有记忆
    files = scan_memory_files(memory_root)
    if not files:
        return []
    
    citations = load_citations(memory_root)
    
    # 解析所有记忆并计算重要性
    memories = []
    bugs = []
    
    for file_path in files:
        memory = parse_memory_file(file_path, memory_root)
        if memory.get("category") == "bugs":
            bugs.append(memory)
        memories.append(memory)
    
    # 计算相关度（简单的关键词匹配）
    context_words = set(context.lower().split())
    
    results = []
    for memory in memories:
        if memory.get("is_archived"):
            continue
        
        # 计算相关度
        title = memory.get("title", "").lower()
        content = memory.get("content", "").lower()
        category = memory.get("category", "")
        
        title_words = set(title.split())
        content_words = set(content.split())
        
        # 关键词匹配
        title_match = len(context_words & title_words) / max(len(context_words), 1)
        content_match = len(context_words & content_words) / max(len(context_words), 1)
        
        relevance = 0.6 * title_match + 0.4 * min(content_match * 10, 1.0)
        
        # 时机加成
        timing_bonus = 0.0
        if timing == "fixing_bug" and category == "bugs":
            timing_bonus = 0.2
        elif timing == "making_decision" and category == "decisions":
            timing_bonus = 0.2
        elif timing == "code_review" and category == "rules":
            timing_bonus = 0.2
        elif timing == "module_first_contact" and category == "summaries":
            timing_bonus = 0.3
        
        relevance = min(relevance + timing_bonus, 1.0)
        
        if relevance < 0.05:  # 过滤不相关的
            continue
        
        # 计算重要性
        importance_result = calculate_importance(memory, citations, bugs)
        importance = importance_result["importance"]
        
        # 综合分
        combined_score = relevance * 0.5 + importance * 0.5
        
        results.append({
            "file": memory.get("file_path", ""),
            "title": memory.get("title", ""),
            "importance": importance,
            "relevance": round(relevance, 3),
            "combined_score": round(combined_score, 3),
            "supply_reason": get_supply_reason(timing, memory, context),
            "timing": timing,
            "category": category,
        })
    
    # 排序
    results.sort(key=lambda x: x["combined_score"], reverse=True)
    
    return results[:top_k]


# ============================================================================
# 知识缺口检测
# ============================================================================

def detect_knowledge_gaps(memory_root: Path) -> List[Dict[str, Any]]:
    """
    检测团队可能存在的知识缺口。
    
    信号：
    1. 模块覆盖不均
    2. Bug 重复模式
    3. 规则缺失
    4. 记忆过时
    """
    files = scan_memory_files(memory_root)
    citations = load_citations(memory_root)
    
    gaps = []
    
    # 分析各分类记忆数量
    category_counts = {}
    memories_by_category = {}
    old_memories = []
    
    for file_path in files:
        memory = parse_memory_file(file_path, memory_root)
        category = memory.get("category", "uncategorized")
        
        if category not in category_counts:
            category_counts[category] = 0
            memories_by_category[category] = []
        
        category_counts[category] += 1
        memories_by_category[category].append(memory)
        
        # 检查过时记忆
        days_old = get_days_old(memory.get("date"))
        citation_info = citations.get(memory.get("file_path"), {})
        citation_count = citation_info.get("citation_count", 0)
        
        if days_old > 90 and citation_count == 0 and not memory.get("is_archived"):
            old_memories.append(memory)
    
    # 1. 检测分类缺失
    expected_categories = ["decisions", "bugs", "rules", "entities"]
    for cat in expected_categories:
        if cat not in category_counts or category_counts[cat] == 0:
            gaps.append({
                "type": "missing_category",
                "description": f"分类 '{cat}' 没有任何记忆记录",
                "severity": "medium",
                "recommendation": f"建议为项目补充 {cat} 类型的知识记录",
            })
    
    # 2. 检测 Bug 重复模式
    bugs = memories_by_category.get("bugs", [])
    if len(bugs) >= 2:
        # 检测标题相似的 Bug
        similar_bugs = []
        for i, bug1 in enumerate(bugs):
            title1 = bug1.get("title", "").lower()
            words1 = set(title1.split())
            for bug2 in bugs[i+1:]:
                title2 = bug2.get("title", "").lower()
                words2 = set(title2.split())
                overlap = len(words1 & words2)
                if overlap >= 2:
                    similar_bugs.append((bug1.get("title"), bug2.get("title")))
        
        if similar_bugs:
            gaps.append({
                "type": "recurring_bugs",
                "description": f"发现 {len(similar_bugs)} 对相似的 Bug 记录，可能存在重复问题",
                "severity": "high",
                "recommendation": "建议分析这些重复 Bug 的根因，并沉淀为规则或模式",
                "details": [f"{b1} <-> {b2}" for b1, b2 in similar_bugs[:3]],
            })
    
    # 3. 检测决策无规则
    decisions = memories_by_category.get("decisions", [])
    rules = memories_by_category.get("rules", [])
    
    if len(decisions) > 0 and len(rules) == 0:
        gaps.append({
            "type": "rules_missing",
            "description": f"有 {len(decisions)} 条决策记录，但没有对应的规则记录",
            "severity": "medium",
            "recommendation": "建议将重要决策提炼为可执行的规则",
        })
    
    # 4. 检测过时记忆
    if old_memories:
        gaps.append({
            "type": "stale_memories",
            "description": f"有 {len(old_memories)} 条记忆超过 90 天未被引用",
            "severity": "low",
            "recommendation": "建议检查这些记忆是否仍然有效，考虑归档过时内容",
            "details": [m.get("file_path") for m in old_memories[:5]],
        })
    
    # 5. 检测覆盖不均
    if category_counts:
        avg_count = sum(category_counts.values()) / len(category_counts)
        for cat, count in category_counts.items():
            if count < avg_count * 0.3 and cat in expected_categories:
                gaps.append({
                    "type": "uneven_coverage",
                    "description": f"分类 '{cat}' 记录数量({count})明显低于平均值({avg_count:.1f})",
                    "severity": "low",
                    "recommendation": f"建议关注 {cat} 类型知识的沉淀",
                })
    
    return gaps


# ============================================================================
# 命令行接口
# ============================================================================

def print_score_table(results: List[Dict[str, Any]]):
    """打印评分表格"""
    print("\n[ProMem] 📊 知识重要性评分")
    print("=" * 80)
    print(f"| {'排名':^4} | {'文件':^35} | {'重要性':^6} | {'复用':^4} | {'遗忘':^4} | {'代价':^4} | {'引用':^4} |")
    print("|" + "-" * 6 + "|" + "-" * 37 + "|" + "-" * 8 + "|" + "-" * 6 + "|" + "-" * 6 + "|" + "-" * 6 + "|" + "-" * 6 + "|")
    
    for i, r in enumerate(results, 1):
        file_name = r["file"][:33] + ".." if len(r["file"]) > 35 else r["file"]
        breakdown = r["breakdown"]
        citation = r["factors"].get("citation_count", 0)
        print(f"| {i:^4} | {file_name:<35} | {r['importance']:^6.2f} | {breakdown['reuse_probability']:^4.2f} | {breakdown['forget_risk']:^4.2f} | {breakdown['pitfall_cost']:^4.2f} | {citation:^4} |")
    
    print("=" * 80)
    
    # 统计
    total = len(results)
    high = len([r for r in results if r["importance"] > 0.7])
    medium = len([r for r in results if 0.4 <= r["importance"] <= 0.7])
    low = len([r for r in results if r["importance"] < 0.4])
    
    print(f"\n总计: {total} 条记忆")
    print(f"高重要性(>0.7): {high} 条")
    print(f"中重要性(0.4-0.7): {medium} 条")
    print(f"低重要性(<0.4): {low} 条")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="ProMem Knowledge Importance & Supply Strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 计算所有记忆的重要性分数
  python3 importance.py --score
  
  # 根据上下文推荐知识
  python3 importance.py --suggest --context "正在开发登录模块"
  
  # 标记记忆被引用
  python3 importance.py --cite decisions/2026-03-17-zustand.md
  
  # 标记记忆过时
  python3 importance.py --archive decisions/old-decision.md
  
  # 检测知识缺口
  python3 importance.py --gaps
        """
    )
    
    # 操作模式
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--score", action="store_true", help="计算所有记忆的重要性分数")
    mode_group.add_argument("--suggest", action="store_true", help="根据上下文推荐知识")
    mode_group.add_argument("--cite", type=str, metavar="FILE", help="标记记忆被引用")
    mode_group.add_argument("--archive", nargs='?', const='auto', metavar="FILE", help="归档记忆（无参数时自动归档低价值记忆，指定文件时归档单个）")
    mode_group.add_argument("--gaps", action="store_true", help="检测知识缺口")
    
    parser.add_argument("--context", type=str, default="", help="当前开发上下文（用于 --suggest）")
    parser.add_argument("--memory-root", type=str, default=None, help="记忆目录路径")
    parser.add_argument("--top-k", type=int, default=5, help="返回结果数量（用于 --suggest）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不实际执行（用于 --archive）")
    
    args = parser.parse_args()
    
    try:
        # 确定路径
        script_dir = Path(__file__).parent.resolve()
        promem_root = script_dir.parent
        
        if args.memory_root:
            memory_root = Path(args.memory_root).resolve()
        else:
            memory_root = promem_root / "memory"
        
        if not memory_root.exists():
            print(f"Error: Memory root not found: {memory_root}", file=sys.stderr)
            sys.exit(2)
        
        # 执行操作
        if args.score:
            files = scan_memory_files(memory_root)
            if not files:
                print("[ProMem] No memory files found.", file=sys.stderr)
                sys.exit(1)
            
            citations = load_citations(memory_root)
            
            # 收集所有 bug
            bugs = []
            memories = []
            for file_path in files:
                memory = parse_memory_file(file_path, memory_root)
                memories.append(memory)
                if memory.get("category") == "bugs":
                    bugs.append(memory)
            
            # 计算重要性
            results = []
            for memory in memories:
                result = calculate_importance(memory, citations, bugs)
                results.append(result)
            
            # 排序
            results.sort(key=lambda x: x["importance"], reverse=True)
            
            if args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                print_score_table(results)
            
            sys.exit(0)
        
        elif args.suggest:
            if not args.context:
                print("Error: --context is required for --suggest", file=sys.stderr)
                sys.exit(2)
            
            results = suggest_knowledge(args.context, memory_root, args.top_k)
            
            if not results:
                print("[ProMem] No relevant knowledge found.", file=sys.stderr)
                sys.exit(1)
            
            if args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                print(f"\n[ProMem] 📚 知识供给建议 (时机: {results[0]['timing']})")
                print("=" * 70)
                for i, r in enumerate(results, 1):
                    print(f"\n{i}. [{r['category']}] {r['title']}")
                    print(f"   文件: {r['file']}")
                    print(f"   综合分: {r['combined_score']:.2f} (相关度: {r['relevance']:.2f}, 重要性: {r['importance']:.2f})")
                    print(f"   理由: {r['supply_reason']}")
                print("\n" + "=" * 70)
            
            sys.exit(0)
        
        elif args.cite:
            result = cite_memory(args.cite, args.context, memory_root)
            if args.json:
                print(json.dumps({"status": "ok", "file": args.cite, "citation": result}, ensure_ascii=False, indent=2))
            else:
                print(f"[ProMem] ✓ 已记录引用: {args.cite}")
                print(f"   累计引用: {result['citation_count']} 次")
                print(f"   最后引用: {result['last_cited']}")
            
            sys.exit(0)
        
        elif args.archive:
            if args.archive == 'auto':
                # 自动归档模式
                config = load_config(promem_root)
                results = auto_archive_memories(memory_root, config, dry_run=args.dry_run)
                
                if not results:
                    if args.json:
                        print(json.dumps({"status": "ok", "archived": [], "message": "No memories to archive"}, ensure_ascii=False))
                    else:
                        print("[ProMem] ✓ 未发现需要归档的记忆")
                    sys.exit(0)
                
                if args.json:
                    print(json.dumps({
                        "status": "ok",
                        "dry_run": args.dry_run,
                        "archived": results
                    }, ensure_ascii=False, indent=2))
                else:
                    mode = "预览" if args.dry_run else "执行"
                    print(f"\n[ProMem] 📦 自动归档{mode}结果")
                    print("=" * 70)
                    for r in results:
                        status = "✓" if r.get('archived', False) or args.dry_run else "✗"
                        print(f"  {status} {r['file']}")
                        print(f"      重要性: {r['importance']:.2f}, 原因: {r['reason']}")
                    print("=" * 70)
                    if args.dry_run:
                        print(f"\n预览完成：{len(results)} 个文件将被归档")
                        print("运行 `npx promem score --archive` 执行实际归档")
                    else:
                        archived_count = sum(1 for r in results if r.get('archived', False))
                        print(f"\n归档完成：{archived_count} 个文件已移动到 archive/")
                
                sys.exit(0)
            else:
                # 单文件归档模式（移动到 archive 目录）
                success = move_to_archive(args.archive, memory_root)
                if success:
                    if args.json:
                        print(json.dumps({"status": "ok", "file": args.archive, "archived": True}, ensure_ascii=False))
                    else:
                        print(f"[ProMem] ✓ 已归档: {args.archive}")
                    sys.exit(0)
                else:
                    print(f"Error: Failed to archive {args.archive}", file=sys.stderr)
                    sys.exit(2)
        
        elif args.gaps:
            gaps = detect_knowledge_gaps(memory_root)
            
            if not gaps:
                if args.json:
                    print(json.dumps([], ensure_ascii=False))
                else:
                    print("[ProMem] ✓ 未检测到明显的知识缺口")
                sys.exit(0)
            
            if args.json:
                print(json.dumps(gaps, ensure_ascii=False, indent=2))
            else:
                print("\n[ProMem] 🔍 知识缺口检测报告")
                print("=" * 70)
                for gap in gaps:
                    severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(gap["severity"], "⚪")
                    print(f"\n{severity_icon} [{gap['type']}] {gap['description']}")
                    print(f"   建议: {gap['recommendation']}")
                    if "details" in gap:
                        for detail in gap["details"]:
                            print(f"   - {detail}")
                print("\n" + "=" * 70)
            
            sys.exit(0)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
