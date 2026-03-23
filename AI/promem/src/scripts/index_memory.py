#!/usr/bin/env python3
"""
ProMem Memory Index & Search Tool

SQLite + FTS5 索引引擎版本。
支持全量/增量索引构建，以及基于 BM25 的全文检索。
可选支持 sentence-transformers 向量嵌入（M2 混合检索预留）。
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Callable

# 导入共享日志模块
try:
    from memory_utils import write_log
except ImportError:
    def write_log(*args, **kwargs):
        pass


# ============================================================================
# CJK 中文分词支持
# ============================================================================

def has_cjk(text: str) -> bool:
    """检查文本是否包含 CJK 字符"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def prepare_for_fts(text: str) -> str:
    """
    将 CJK 字符逐字加空格，方便 FTS5 分词。
    
    FTS5 的 unicode61 tokenizer 按 Unicode 词边界分词，中文字符之间没有空格，
    整个中文字符串被当作一个 token。通过在每个 CJK 字符前后加空格，可以让
    FTS5 正确分词。
    
    例如："状态管理选型" → "状 态 管 理 选 型"
    """
    if not text or not has_cjk(text):
        return text
    result = []
    for char in text:
        if re.match(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', char):
            result.append(f' {char} ')
        else:
            result.append(char)
    return re.sub(r' +', ' ', ''.join(result)).strip()


# ============================================================================
# 配置加载
# ============================================================================

def load_config(config_path: Path) -> Dict[str, Any]:
    """
    加载配置文件，支持三级嵌套（如 recall.weights.bm25）
    
    使用简单字符串解析，避免依赖 pyyaml
    """
    default_config = {
        "recall": {
            "top_k": 3,
            "weights": {
                "bm25": 0.3,
                "semantic": 0.5,
                "recency": 0.2
            }
        }
    }
    
    if not config_path.exists():
        return default_config
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 简单的 YAML 解析（支持三级嵌套，避免依赖 pyyaml）
        config = {}
        section_stack = []  # [(indent_level, section_dict)]
        
        for line in content.split("\n"):
            line_stripped = line.rstrip()
            if not line_stripped or line_stripped.lstrip().startswith("#"):
                continue
            
            # 计算缩进级别（2空格为一级）
            indent = len(line_stripped) - len(line_stripped.lstrip())
            indent_level = indent // 2
            
            if ":" not in line_stripped:
                continue
            
            key = line_stripped.split(":")[0].strip()
            value_part = line_stripped.split(":", 1)[1].strip()
            
            # 去掉注释
            if "#" in value_part:
                value_part = value_part.split("#")[0].strip()
            
            # 解析值
            def parse_value(v: str):
                if not v:
                    return None  # 表示这是一个嵌套 section
                try:
                    if "." in v:
                        return float(v)
                    return int(v)
                except ValueError:
                    return v
            
            parsed_value = parse_value(value_part)
            
            # 清理超出当前缩进级别的栈
            while section_stack and section_stack[-1][0] >= indent_level:
                section_stack.pop()
            
            # 确定当前要写入的字典
            if not section_stack:
                target_dict = config
            else:
                target_dict = section_stack[-1][1]
            
            if parsed_value is None:
                # 这是一个新的嵌套 section
                target_dict[key] = {}
                section_stack.append((indent_level, target_dict[key]))
            else:
                target_dict[key] = parsed_value
        
        # 合并默认值（确保 weights 存在）
        if "recall" not in config:
            config["recall"] = default_config["recall"]
        elif "weights" not in config.get("recall", {}):
            config["recall"]["weights"] = default_config["recall"]["weights"]
        
        return config
    except Exception:
        return default_config


# ============================================================================
# 向量嵌入支持（三级降级）
# ============================================================================

def get_embedding_func() -> Tuple[Optional[Callable], int]:
    """
    尝试加载向量嵌入功能，返回 (embed_func, dimension) 或 (None, 0)
    
    三级降级策略：
    1. 首选：sentence-transformers + all-MiniLM-L6-v2
    2. 兜底：无向量能力，仅用 FTS5
    """
    # 尝试 sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("[ProMem] Using sentence-transformers for embeddings (dim=384)", file=sys.stderr)
        return model.encode, 384
    except ImportError:
        pass
    except Exception as e:
        print(f"[ProMem] Warning: Failed to load sentence-transformers: {e}", file=sys.stderr)
    
    # 兜底：无向量能力
    print("[ProMem] Warning: No embedding model available. Using BM25 only.", file=sys.stderr)
    return None, 0


# ============================================================================
# SQLite 数据库管理
# ============================================================================

class MemoryIndex:
    """SQLite 索引管理器"""
    
    def __init__(self, db_path: Path, memory_root: Path):
        self.db_path = db_path
        self.memory_root = memory_root
        self.conn: Optional[sqlite3.Connection] = None
        self.embed_func: Optional[Callable] = None
        self.embed_dim: int = 0
        self._vec_available: bool = False
    
    def connect(self) -> sqlite3.Connection:
        """连接数据库，必要时初始化表结构"""
        if self.conn is not None:
            return self.conn
        
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            self._init_schema()
            return self.conn
        except sqlite3.DatabaseError as e:
            # 数据库损坏，删除并重建
            print(f"[ProMem] Database corrupted, rebuilding: {e}", file=sys.stderr)
            if self.db_path.exists():
                self.db_path.unlink()
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            self._init_schema()
            return self.conn
    
    def _init_schema(self):
        """初始化数据库表结构"""
        cursor = self.conn.cursor()
        
        # 主表：记忆文件元数据
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                title TEXT,
                category TEXT,
                date TEXT,
                content TEXT,
                content_hash TEXT,
                indexed_at TEXT
            )
        """)
        
        # FTS5 全文索引（BM25）
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                title, content,
                content='memories',
                content_rowid='id'
            )
        """)
        
        # FTS5 触发器：只保留删除触发器，插入和更新由 Python 代码手动管理
        # 这样可以在 Python 端对 CJK 内容进行预处理后再写入 FTS
        # 删除旧的触发器（如果存在）
        cursor.execute("DROP TRIGGER IF EXISTS memories_ai")
        cursor.execute("DROP TRIGGER IF EXISTS memories_au")
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, title, content) 
                VALUES ('delete', old.id, old.title, old.content);
            END
        """)
        
        # 尝试加载 sqlite-vec 扩展（可选）
        self._try_init_vec_table(cursor)
        
        self.conn.commit()
    
    def _try_init_vec_table(self, cursor):
        """尝试初始化向量索引表（sqlite-vec 扩展）"""
        try:
            # 检查是否有 sqlite-vec 扩展
            self.conn.enable_load_extension(True)
            # 常见的扩展路径
            vec_paths = [
                "vec0",
                "/usr/local/lib/sqlite-vec/vec0",
                "/opt/homebrew/lib/sqlite-vec/vec0.dylib",
            ]
            for vec_path in vec_paths:
                try:
                    self.conn.load_extension(vec_path)
                    self._vec_available = True
                    break
                except Exception:
                    continue
        except Exception:
            pass
        
        if self._vec_available and self.embed_dim > 0:
            try:
                cursor.execute(f"""
                    CREATE VIRTUAL TABLE IF NOT EXISTS memories_vec USING vec0(
                        embedding float[{self.embed_dim}]
                    )
                """)
                print(f"[ProMem] sqlite-vec available, vector index enabled (dim={self.embed_dim})", file=sys.stderr)
            except Exception as e:
                print(f"[ProMem] Warning: Failed to create vector table: {e}", file=sys.stderr)
                self._vec_available = False
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def init_embedding(self):
        """初始化嵌入功能"""
        self.embed_func, self.embed_dim = get_embedding_func()


# ============================================================================
# 文件解析
# ============================================================================

def scan_memory_files(memory_root: Path) -> List[Path]:
    """递归扫描 memory 目录下所有 .md 文件（排除 .gitkeep 和 archive 目录）"""
    files = []
    if not memory_root.exists():
        return files
    
    for path in memory_root.rglob("*.md"):
        # 跳过 .gitkeep 文件
        if path.name == ".gitkeep":
            continue
        # 跳过 archive 目录（归档的记忆不参与日常检索）
        if 'archive' in path.parts:
            continue
        # 跳过 summaries 目录（摘要单独处理）
        if 'summaries' in path.parts:
            continue
        files.append(path)
    
    return files


def parse_memory_file(file_path: Path, memory_root: Path) -> Dict[str, Any]:
    """
    解析单个 Markdown 文件，提取元数据
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        content = ""
    
    # 提取标题：第一个 # 开头的行
    title = ""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            break
    
    if not title:
        title = file_path.stem
    
    # 提取日期：从文件名 YYYY-MM-DD 前缀提取
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
    
    # 提取分类：从文件所在目录名推断
    try:
        relative = file_path.relative_to(memory_root)
        parts = relative.parts
        category = parts[0] if len(parts) > 1 else "uncategorized"
    except ValueError:
        category = "uncategorized"
    
    # 计算相对路径
    try:
        relative_path = str(file_path.relative_to(memory_root))
    except ValueError:
        relative_path = file_path.name
    
    # 计算内容哈希
    content_hash = hashlib.md5(content.encode()).hexdigest()
    
    return {
        "file_path": relative_path,
        "title": title,
        "content": content,
        "date": date,
        "category": category,
        "content_hash": content_hash,
    }


# ============================================================================
# 索引构建
# ============================================================================

def needs_reindex(file_path: str, content_hash: str, cursor: sqlite3.Cursor) -> bool:
    """检查文件是否需要重新索引"""
    cursor.execute("SELECT content_hash FROM memories WHERE file_path = ?", (file_path,))
    row = cursor.fetchone()
    if row is None:
        return True  # 新文件
    return row[0] != content_hash  # 内容有变化


def build_full_index(index: MemoryIndex) -> int:
    """
    全量重建索引
    
    返回：索引的文件数量
    """
    conn = index.connect()
    cursor = conn.cursor()
    
    # 清空现有数据
    cursor.execute("DELETE FROM memories")
    # 手动清空 FTS 表（因为删除触发器只处理单条删除）
    cursor.execute("DELETE FROM memories_fts")
    
    # 扫描文件
    files = scan_memory_files(index.memory_root)
    indexed_count = 0
    now = datetime.now().isoformat()
    
    for file_path in files:
        doc = parse_memory_file(file_path, index.memory_root)
        
        # 插入主表（保留原始内容）
        cursor.execute("""
            INSERT INTO memories (file_path, title, category, date, content, content_hash, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            doc["file_path"],
            doc["title"],
            doc["category"],
            doc["date"],
            doc["content"],
            doc["content_hash"],
            now
        ))
        
        # 获取刚插入的 ID
        mem_id = cursor.lastrowid
        
        # 手动插入 FTS 表（使用 CJK 预处理后的内容）
        fts_title = prepare_for_fts(doc["title"])
        fts_content = prepare_for_fts(doc["content"])
        cursor.execute("""
            INSERT INTO memories_fts(rowid, title, content)
            VALUES (?, ?, ?)
        """, (mem_id, fts_title, fts_content))
        
        indexed_count += 1
    
    conn.commit()
    return indexed_count


def build_incremental_index(index: MemoryIndex) -> Tuple[int, int, int]:
    """
    增量更新索引
    
    返回：(新增数, 更新数, 删除数)
    """
    conn = index.connect()
    cursor = conn.cursor()
    
    # 获取当前索引的所有文件
    cursor.execute("SELECT file_path FROM memories")
    indexed_files = {row[0] for row in cursor.fetchall()}
    
    # 扫描文件系统
    files = scan_memory_files(index.memory_root)
    current_files = set()
    
    added = 0
    updated = 0
    now = datetime.now().isoformat()
    
    for file_path in files:
        doc = parse_memory_file(file_path, index.memory_root)
        current_files.add(doc["file_path"])
        
        if doc["file_path"] not in indexed_files:
            # 新文件：插入主表
            cursor.execute("""
                INSERT INTO memories (file_path, title, category, date, content, content_hash, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                doc["file_path"],
                doc["title"],
                doc["category"],
                doc["date"],
                doc["content"],
                doc["content_hash"],
                now
            ))
            
            # 获取刚插入的 ID，手动插入 FTS 表（使用 CJK 预处理）
            mem_id = cursor.lastrowid
            fts_title = prepare_for_fts(doc["title"])
            fts_content = prepare_for_fts(doc["content"])
            cursor.execute("""
                INSERT INTO memories_fts(rowid, title, content)
                VALUES (?, ?, ?)
            """, (mem_id, fts_title, fts_content))
            
            added += 1
        elif needs_reindex(doc["file_path"], doc["content_hash"], cursor):
            # 内容有变化：获取现有 ID
            cursor.execute("SELECT id FROM memories WHERE file_path = ?", (doc["file_path"],))
            row = cursor.fetchone()
            mem_id = row[0] if row else None
            
            # 更新主表
            cursor.execute("""
                UPDATE memories 
                SET title = ?, category = ?, date = ?, content = ?, content_hash = ?, indexed_at = ?
                WHERE file_path = ?
            """, (
                doc["title"],
                doc["category"],
                doc["date"],
                doc["content"],
                doc["content_hash"],
                now,
                doc["file_path"]
            ))
            
            # 手动更新 FTS 表（先删除再插入）
            if mem_id:
                fts_title = prepare_for_fts(doc["title"])
                fts_content = prepare_for_fts(doc["content"])
                cursor.execute("""
                    INSERT INTO memories_fts(memories_fts, rowid, title, content)
                    VALUES ('delete', ?, ?, ?)
                """, (mem_id, doc["title"], doc["content"]))  # 删除旧的
                cursor.execute("""
                    INSERT INTO memories_fts(rowid, title, content)
                    VALUES (?, ?, ?)
                """, (mem_id, fts_title, fts_content))  # 插入新的
            
            updated += 1
    
    # 删除不存在的文件
    deleted_files = indexed_files - current_files
    deleted = len(deleted_files)
    for file_path in deleted_files:
        cursor.execute("DELETE FROM memories WHERE file_path = ?", (file_path,))
    
    conn.commit()
    return added, updated, deleted


# ============================================================================
# 搜索查询
# ============================================================================

# ----------------------------------------------------------------------------
# 混合检索通道
# ----------------------------------------------------------------------------

def bm25_search(query: str, cursor: sqlite3.Cursor, top_n: int = 20) -> List[Tuple[int, float]]:
    """
    BM25 检索通道（α 通道）
    
    返回: [(memory_id, normalized_bm25_score), ...]
    FTS5 的 bm25() 返回负值（越小越相关），需要归一化到 [0, 1]
    """
    # 对查询进行 CJK 分词处理
    if has_cjk(query):
        # 将中文字符逐字加空格，与索引时的处理保持一致
        processed_query = prepare_for_fts(query)
    else:
        processed_query = query
    
    # 将查询分词，用 OR 连接
    keywords = processed_query.strip().split()
    if not keywords:
        return []
    
    fts_query = " OR ".join(f'"{kw}"' for kw in keywords)
    
    try:
        cursor.execute("""
            SELECT m.id, bm25(memories_fts) as score 
            FROM memories_fts fts
            JOIN memories m ON fts.rowid = m.id
            WHERE memories_fts MATCH ?
            ORDER BY score
            LIMIT ?
        """, (fts_query, top_n))
        results = cursor.fetchall()
    except sqlite3.OperationalError:
        return []
    
    if not results:
        return []
    
    # 归一化：最相关的为 1.0
    min_score = results[0][1]  # 最好的（最负的）
    max_score = results[-1][1] if len(results) > 1 else min_score - 1
    range_ = max_score - min_score if max_score != min_score else 1.0
    
    return [(r[0], 1.0 - (r[1] - min_score) / range_) for r in results]


def recency_score(date_str: Optional[str], half_life_days: int = 30) -> float:
    """
    时间衰减分（γ 通道）
    
    指数衰减：score = 0.5 ^ (days_old / half_life)
    30 天前的记忆分数约 0.5
    """
    from datetime import date as date_type
    
    if not date_str:
        return 0.3  # 无日期的给基础分
    
    try:
        mem_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        days_old = (date_type.today() - mem_date).days
        if days_old < 0:
            days_old = 0  # 未来日期当作今天
        return 0.5 ** (days_old / half_life_days)
    except (ValueError, TypeError):
        return 0.3


def semantic_search(
    query: str,
    embed_func: Optional[Callable],
    cursor: sqlite3.Cursor,
    index: 'MemoryIndex',
    top_n: int = 20
) -> List[Tuple[int, float]]:
    """
    向量语义检索通道（β 通道）
    
    返回: [(memory_id, cosine_similarity), ...]
    如果没有嵌入能力，返回空列表
    """
    if embed_func is None:
        return []
    
    # 检查是否有向量索引表
    if not getattr(index, '_vec_available', False):
        return []
    
    try:
        # 生成查询向量
        query_vec = embed_func([query])[0]
        
        # 查询向量索引（sqlite-vec 语法）
        cursor.execute("""
            SELECT rowid, distance
            FROM memories_vec
            WHERE embedding MATCH ?
            ORDER BY distance
            LIMIT ?
        """, (query_vec.tobytes(), top_n))
        results = cursor.fetchall()
        
        if not results:
            return []
        
        # 将距离转换为相似度（假设是余弦距离）
        # cosine_similarity = 1 - cosine_distance
        return [(r[0], 1.0 - r[1]) for r in results]
    except Exception:
        return []


def simple_text_similarity(text1: str, text2: str) -> float:
    """
    简单的文本相似度计算（基于共同词比例）
    用于无向量时的 MMR 去重
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1 & words2
    union = words1 | words2
    
    return len(intersection) / len(union) if union else 0.0


def mmr_rerank(
    candidates: List[Dict[str, Any]],
    lambda_param: float = 0.7,
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    MMR 去重（Maximal Marginal Relevance）
    
    在相关性和多样性之间平衡。
    简化版本（无向量时）：基于标题/分类去重
    - 同一分类下标题相似度 > 0.8 的，保留分数最高的
    
    参数:
        candidates: [{"file": ..., "title": ..., "score": ..., "category": ..., ...}]
        lambda_param: 相关性权重 (0.7 = 偏重相关性, 0.3 = 偏重多样性)
        top_k: 返回数量
    
    返回: 去重后的结果列表
    """
    if len(candidates) <= top_k:
        return candidates
    
    selected = []
    remaining = candidates.copy()
    
    while len(selected) < top_k and remaining:
        best_idx = -1
        best_mmr_score = -float('inf')
        
        for i, candidate in enumerate(remaining):
            # 相关性分数
            relevance = candidate.get("score", 0)
            
            # 计算与已选结果的最大相似度
            max_similarity = 0.0
            for sel in selected:
                # 同分类内比较标题相似度
                if candidate.get("category") == sel.get("category"):
                    title_sim = simple_text_similarity(
                        candidate.get("title", ""),
                        sel.get("title", "")
                    )
                    max_similarity = max(max_similarity, title_sim)
            
            # MMR 分数 = λ * 相关性 - (1 - λ) * 最大相似度
            mmr_score = lambda_param * relevance - (1 - lambda_param) * max_similarity
            
            if mmr_score > best_mmr_score:
                best_mmr_score = mmr_score
                best_idx = i
        
        if best_idx >= 0:
            selected.append(remaining.pop(best_idx))
    
    return selected


def hybrid_search(
    query: str,
    index: 'MemoryIndex',
    config: Dict[str, Any],
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    混合检索主函数
    
    综合分 = α × BM25分 + β × 向量语义分 + γ × 时间衰减分
    
    返回: [{"file": ..., "title": ..., "snippet": ..., "score": ..., "category": ..., "date": ...}]
    """
    start_time = time.time()
    
    conn = index.connect()
    cursor = conn.cursor()
    
    # 1. 检查索引是否存在数据
    cursor.execute("SELECT COUNT(*) FROM memories")
    count = cursor.fetchone()[0]
    if count == 0:
        print("[ProMem] Index empty, building full index...", file=sys.stderr)
        build_full_index(index)
    
    # 2. 获取配置权重
    weights = config.get("recall", {}).get("weights", {})
    alpha = weights.get("bm25", 0.3)
    beta = weights.get("semantic", 0.5)
    gamma = weights.get("recency", 0.2)
    
    # 3. BM25 检索
    bm25_results = bm25_search(query, cursor, top_n=20)
    
    # 4. 向量检索（如果可用）
    semantic_results = []
    has_vectors = False
    if index.embed_func is not None and getattr(index, '_vec_available', False):
        semantic_results = semantic_search(query, index.embed_func, cursor, index, top_n=20)
        has_vectors = len(semantic_results) > 0
    
    # 5. 权重重分配（如果向量不可用）
    if not has_vectors:
        effective_alpha = alpha + beta  # 吸收语义权重
        effective_beta = 0
        effective_gamma = gamma
        print("[ProMem] No vector index available, using BM25 + recency only", file=sys.stderr)
    else:
        effective_alpha = alpha
        effective_beta = beta
        effective_gamma = gamma
    
    # 6. 收集所有候选 ID
    candidate_ids = set()
    bm25_scores = {}
    semantic_scores = {}
    
    for mem_id, score in bm25_results:
        candidate_ids.add(mem_id)
        bm25_scores[mem_id] = score
    
    for mem_id, score in semantic_results:
        candidate_ids.add(mem_id)
        semantic_scores[mem_id] = score
    
    if not candidate_ids:
        # 记录搜索日志（无结果）
        elapsed_ms = int((time.time() - start_time) * 1000)
        try:
            write_log('SEARCH', 'index', f'query="{query[:30]}"',
                      memory_root=str(index.memory_root),
                      query=query[:50],
                      top_k=top_k,
                      results=0,
                      bm25_hits=0,
                      time_ms=elapsed_ms)
        except Exception:
            pass
        return []
    
    # 7. 获取候选记忆的元数据
    placeholders = ",".join("?" for _ in candidate_ids)
    cursor.execute(f"""
        SELECT id, file_path, title, content, category, date
        FROM memories
        WHERE id IN ({placeholders})
    """, list(candidate_ids))
    
    memory_data = {}
    for row in cursor.fetchall():
        memory_data[row[0]] = {
            "id": row[0],
            "file_path": row[1],
            "title": row[2],
            "content": row[3],
            "category": row[4],
            "date": row[5]
        }
    
    # 8. 计算综合分
    keywords = query.strip().split()
    candidates = []
    
    for mem_id in candidate_ids:
        if mem_id not in memory_data:
            continue
        
        data = memory_data[mem_id]
        
        # BM25 分数（默认 0 如果不在 BM25 结果中）
        bm25_s = bm25_scores.get(mem_id, 0)
        
        # 语义分数
        semantic_s = semantic_scores.get(mem_id, 0)
        
        # 时间衰减分
        recency_s = recency_score(data["date"])
        
        # 综合分
        combined_score = (
            effective_alpha * bm25_s +
            effective_beta * semantic_s +
            effective_gamma * recency_s
        )
        
        candidates.append({
            "file": data["file_path"],
            "title": data["title"],
            "snippet": generate_snippet(data["content"], keywords),
            "score": round(combined_score, 3),
            "category": data["category"],
            "date": data["date"],
            # 保留分项分数用于调试
            "_bm25": round(bm25_s, 3),
            "_semantic": round(semantic_s, 3),
            "_recency": round(recency_s, 3)
        })
    
    # 9. 按综合分排序
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # 10. MMR 去重
    final_results = mmr_rerank(candidates, lambda_param=0.7, top_k=top_k)
    
    # 11. 移除内部调试字段
    for result in final_results:
        result.pop("_bm25", None)
        result.pop("_semantic", None)
        result.pop("_recency", None)
    
    # 记录搜索日志
    elapsed_ms = int((time.time() - start_time) * 1000)
    try:
        write_log('SEARCH', 'index', f'query="{query[:30]}"',
                  memory_root=str(index.memory_root),
                  query=query[:50],
                  top_k=top_k,
                  results=len(final_results),
                  bm25_hits=len(bm25_results),
                  time_ms=elapsed_ms)
    except Exception:
        pass
    
    return final_results


# ----------------------------------------------------------------------------
# 辅助函数
# ----------------------------------------------------------------------------

def generate_snippet(content: str, keywords: List[str], context_chars: int = 50) -> str:
    """生成匹配片段"""
    if not keywords or not content:
        return content[:100] + "..." if len(content) > 100 else content
    
    content_lower = content.lower()
    
    first_match_pos = -1
    for keyword in keywords:
        pos = content_lower.find(keyword.lower())
        if pos != -1:
            if first_match_pos == -1 or pos < first_match_pos:
                first_match_pos = pos
    
    if first_match_pos == -1:
        return content[:100] + "..." if len(content) > 100 else content
    
    start = max(0, first_match_pos - context_chars)
    end = min(len(content), first_match_pos + context_chars + len(keywords[0]))
    
    snippet = content[start:end]
    
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."
    
    snippet = snippet.replace("\n", " ").strip()
    
    return snippet


def search_from_index(
    index: MemoryIndex,
    query: str,
    top_k: int = 3,
    config: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    从 SQLite 索引搜索（混合检索版本）
    
    使用混合检索算法：
    综合分 = α × BM25分 + β × 向量语义分 + γ × 时间衰减分
    """
    if config is None:
        config = {
            "recall": {
                "top_k": top_k,
                "weights": {"bm25": 0.5, "semantic": 0, "recency": 0.5}
            }
        }
    
    return hybrid_search(query, index, config, top_k)


def search_memories(
    memory_root: Path,
    query: str,
    top_k: int = 3,
    db_path: Optional[Path] = None,
    config: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    搜索记忆文件（混合检索版本）
    
    底层使用 hybrid_search 实现多信号混合排序
    """
    if db_path is None:
        db_path = memory_root.parent / ".index.db"
    
    if config is None:
        config_path = memory_root.parent / "config.yaml"
        config = load_config(config_path)
    
    index = MemoryIndex(db_path, memory_root)
    try:
        return search_from_index(index, query, top_k, config)
    finally:
        index.close()


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    """主函数：解析命令行参数，执行索引构建或搜索"""
    parser = argparse.ArgumentParser(
        description="ProMem Memory Index & Search Tool - SQLite 索引引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 全量重建索引
  python index_memory.py --full
  
  # 增量更新索引
  python index_memory.py --incremental
  
  # 搜索（自动使用索引）
  python index_memory.py --query "状态管理"
  python index_memory.py --query "zustand react" --top-k 5

输出格式 (JSON):
  [{"file": "...", "title": "...", "snippet": "...", "score": 0.85, "category": "...", "date": "..."}]
        """
    )
    
    # 索引模式
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--full",
        action="store_true",
        help="全量重建索引"
    )
    mode_group.add_argument(
        "--incremental",
        action="store_true",
        help="增量更新索引（只处理新增/修改的文件）"
    )
    mode_group.add_argument(
        "--query", "-q",
        type=str,
        help="搜索关键词"
    )
    
    parser.add_argument(
        "--top-k", "-k",
        type=int,
        default=None,
        help="返回结果数量（默认从 config.yaml 读取，fallback 为 3）"
    )
    
    parser.add_argument(
        "--memory-root", "-m",
        type=str,
        default=None,
        help="记忆目录路径（默认 .promem/memory/）"
    )
    
    args = parser.parse_args()
    
    # 至少需要一个操作
    if not args.full and not args.incremental and not args.query:
        parser.error("请指定 --full, --incremental, 或 --query 参数")
    
    try:
        # 确定路径
        script_dir = Path(__file__).parent.resolve()
        promem_root = script_dir.parent  # .promem/
        
        # 加载配置
        config_path = promem_root / "config.yaml"
        config = load_config(config_path)
        
        # 确定 top_k
        if args.top_k is not None:
            top_k = args.top_k
        else:
            top_k = config.get("recall", {}).get("top_k", 3)
        
        # 确定 memory_root
        if args.memory_root:
            memory_root = Path(args.memory_root).resolve()
        else:
            memory_root = promem_root / "memory"
        
        # 数据库路径
        db_path = promem_root / ".index.db"
        
        # 创建索引管理器
        index = MemoryIndex(db_path, memory_root)
        
        try:
            if args.full:
                # 全量索引
                index.init_embedding()
                count = build_full_index(index)
                print(f"[ProMem] Full index built: {count} files indexed", file=sys.stderr)
                print(json.dumps({"status": "ok", "indexed": count}))
                sys.exit(0)
            
            elif args.incremental:
                # 增量索引
                index.init_embedding()
                added, updated, deleted = build_incremental_index(index)
                print(f"[ProMem] Incremental update: +{added} ~{updated} -{deleted}", file=sys.stderr)
                print(json.dumps({
                    "status": "ok",
                    "added": added,
                    "updated": updated,
                    "deleted": deleted
                }))
                sys.exit(0)
            
            elif args.query:
                # 搜索（使用混合检索）
                results = search_from_index(index, args.query, top_k, config)
                print(json.dumps(results, ensure_ascii=False, indent=2))
                sys.exit(0)
        
        finally:
            index.close()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
