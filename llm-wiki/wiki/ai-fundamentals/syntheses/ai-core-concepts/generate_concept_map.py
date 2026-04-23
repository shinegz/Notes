#!/usr/bin/env python3
"""Generate AI Core Concepts concept map SVG — clean grid-aligned layout."""

# Node: (id, label, x, y, w, h, fill, stroke, is_hub)
# Grid: columns at 100, 280, 460, 640, 820, 1000
#       rows at 80, 190, 300, 410, 520, 630

nodes = [
    # Row 1: Input preprocessing
    ("token", "Token", 100, 80, 100, 40, "#fdf2f8", "#ec4899", False),
    ("tokenization", "Tokenization", 280, 80, 120, 40, "#fdf2f8", "#ec4899", False),
    ("embedding", "Embedding", 480, 80, 110, 40, "#faf5ff", "#8b5cf6", False),
    ("prompt", "Prompt", 680, 80, 100, 40, "#fff7ed", "#f97316", False),
    ("cot-react", "CoT / ReAct", 860, 80, 120, 40, "#fefce8", "#fbbf24", False),
    # Row 2: Architecture
    ("context", "Context", 100, 190, 100, 40, "#f5f3ff", "#a78bfa", False),
    ("attention", "Attention", 300, 190, 110, 40, "#eff6ff", "#1e40af", False),
    ("transformer", "Transformer", 480, 190, 120, 40, "#eff6ff", "#3b82f6", False),
    ("tool", "Tool / Function", 700, 190, 130, 40, "#ecfeff", "#06b6d4", False),
    ("mcp", "MCP", 900, 190, 80, 40, "#ecfeff", "#06b6d4", False),
    ("skill", "Skill", 1020, 190, 90, 40, "#fefce8", "#eab308", False),
    # Row 3: Core hub
    ("llm", "LLM", 520, 300, 140, 56, "#dbeafe", "#2563eb", True),
    # Row 4: Training & memory
    ("vector-db", "Vector DB", 100, 410, 110, 40, "#faf5ff", "#8b5cf6", False),
    ("memory", "Memory", 280, 410, 100, 40, "#f0fdf4", "#22c55e", False),
    ("scaling-laws", "Scaling Laws", 460, 410, 130, 40, "#ecfeff", "#06b6d4", False),
    ("fine-tuning", "Fine-tuning", 640, 410, 120, 40, "#eff6ff", "#60a5fa", False),
    ("alignment", "Alignment / RLHF", 820, 410, 150, 40, "#f0fdf4", "#22c55e", False),
    # Row 5: Agent & RAG
    ("rag", "RAG", 190, 520, 80, 40, "#fdf4ff", "#c026d3", False),
    ("agent", "Agent", 520, 520, 140, 56, "#dcfce7", "#16a34a", True),
]

# Edge: (from, to, label, style)
# style: "h" = horizontal, "v" = vertical, "hv" = horizontal then vertical, "vh" = vertical then horizontal
edges = [
    ("token", "tokenization", "切分", "h"),
    ("tokenization", "embedding", "向量化", "h"),
    ("embedding", "transformer", "输入", "vh"),
    ("attention", "transformer", "Self-Attention", "h"),
    ("transformer", "llm", "架构基础", "v"),
    ("context", "llm", "工作记忆", "vh"),
    ("llm", "scaling-laws", "规模化", "v"),
    ("llm", "fine-tuning", "微调", "v"),
    ("fine-tuning", "alignment", "RLHF/DPO", "h"),
    ("llm", "prompt", "交互接口", "vh"),
    ("prompt", "cot-react", "推理链", "h"),
    ("llm", "tool", "Function Calling", "vh"),
    ("tool", "mcp", "标准化", "h"),
    ("mcp", "skill", "封装", "h"),
    ("llm", "agent", "大脑", "v"),
    ("tool", "agent", "执行", "vh"),
    ("cot-react", "agent", "ReAct 循环", "vh"),
    ("context", "memory", "短期记忆", "v"),
    ("vector-db", "memory", "长期记忆", "h"),
    ("memory", "agent", "记忆组件", "vh"),
    ("llm", "rag", "检索增强", "vh"),
    ("vector-db", "rag", "语义检索", "vh"),
    ("rag", "agent", "知识增强", "vh"),
]

node_map = {n[0]: n for n in nodes}


def get_anchor(node_id, side):
    """Get anchor point on a specific side of a node."""
    _, _, x, y, w, h, _, _, _ = node_map[node_id]
    if side == "left":
        return x, y + h/2
    elif side == "right":
        return x + w, y + h/2
    elif side == "top":
        return x + w/2, y
    elif side == "bottom":
        return x + w/2, y + h
    return x + w/2, y + h/2


def draw_manhattan_edge(fx, fy, tx, ty, style):
    """Generate path data for Manhattan-routed edge."""
    if style == "h":
        # Straight horizontal
        mid_y = (fy + ty) / 2
        return f"M {fx:.0f},{fy:.0f} L {tx:.0f},{ty:.0f}", (fx + tx)/2, mid_y
    elif style == "v":
        # Straight vertical
        mid_x = (fx + tx) / 2
        return f"M {fx:.0f},{fy:.0f} L {tx:.0f},{ty:.0f}", mid_x, (fy + ty)/2
    elif style == "hv":
        # Horizontal first, then vertical
        mid_x = tx
        mid_y = fy
        return f"M {fx:.0f},{fy:.0f} L {mid_x:.0f},{mid_y:.0f} L {tx:.0f},{ty:.0f}", (fx + mid_x)/2, fy
    elif style == "vh":
        # Vertical first, then horizontal
        mid_x = fx
        mid_y = ty
        return f"M {fx:.0f},{fy:.0f} L {mid_x:.0f},{mid_y:.0f} L {tx:.0f},{ty:.0f}", fx, (fy + mid_y)/2
    else:
        # Default: direct line
        return f"M {fx:.0f},{fy:.0f} L {tx:.0f},{ty:.0f}", (fx + tx)/2, (fy + ty)/2


def get_connection(from_id, to_id, style):
    """Determine connection points based on relative positions."""
    _, _, fx, fy, fw, fh, _, _, _ = node_map[from_id]
    _, _, tx, ty, tw, th, _, _, _ = node_map[to_id]
    
    fcx, fcy = fx + fw/2, fy + fh/2
    tcx, tcy = tx + tw/2, ty + th/2
    
    dx = tcx - fcx
    dy = tcy - fcy
    
    if style == "h":
        if dx > 0:
            return get_anchor(from_id, "right") + get_anchor(to_id, "left")
        else:
            return get_anchor(from_id, "left") + get_anchor(to_id, "right")
    elif style == "v":
        if dy > 0:
            return get_anchor(from_id, "bottom") + get_anchor(to_id, "top")
        else:
            return get_anchor(from_id, "top") + get_anchor(to_id, "bottom")
    elif style == "hv":
        if dx > 0:
            return (fx + fw, fcy, tx, fcy)
        else:
            return (fx, fcy, tx + tw, fcy)
    elif style == "vh":
        if dy > 0:
            return (fcx, fy + fh, fcx, ty)
        else:
            return (fcx, fy, fcx, ty + th)
    
    return fcx, fcy, tcx, tcy


# Build SVG
lines = []
lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 680">')

# Defs
lines.append('  <defs>')
lines.append('    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">')
lines.append('      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.08"/>')
lines.append('    </filter>')
lines.append('  </defs>')

# Background
lines.append('  <rect width="1200" height="680" fill="#fafafa" rx="12"/>')

# Title
lines.append('  <text x="600" y="36" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="600" fill="#1f2937">AI 核心概念关系网络图</text>')
lines.append('  <text x="600" y="56" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="12" fill="#9ca3af">基于 llm-wiki source 资料的概念关联地图 — 连线表示概念关系，非层级依赖</text>')

# Draw edges
for from_id, to_id, label, style in edges:
    fx, fy, tx, ty = get_connection(from_id, to_id, style)
    path_data, lx, ly = draw_manhattan_edge(fx, fy, tx, ty, style)
    
    lines.append(f'  <path d="{path_data}" fill="none" stroke="#d1d5db" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    
    # Label
    lw = len(label) * 11 + 10
    lh = 18
    lines.append(f'  <rect x="{lx-lw/2:.1f}" y="{ly-lh/2:.1f}" width="{lw:.0f}" height="{lh}" rx="4" fill="#fafafa" opacity="0.95"/>')
    lines.append(f'  <text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="10" fill="#6b7280">{label}</text>')

# Draw nodes
for node_id, label, x, y, w, h, fill, stroke, is_hub in nodes:
    if is_hub:
        filter_attr = ' filter="url(#shadow)"'
        stroke_w = "2.5"
        font_size = "15"
        font_weight = "700"
    else:
        filter_attr = ""
        stroke_w = "1.5"
        font_size = "12"
        font_weight = "600"
    
    # Main rectangle
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" ry="6" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"{filter_attr}/>')
    
    # Left accent bar
    lines.append(f'  <rect x="{x}" y="{y}" width="4" height="{h}" rx="6" ry="6" fill="{stroke}"/>')
    
    # Text
    tcx = x + w/2 + 2
    tcy = y + h/2 + 1
    lines.append(f'  <text x="{tcx:.1f}" y="{tcy+4:.1f}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="{font_size}" font-weight="{font_weight}" fill="#1f2937">{label}</text>')

# Legend
lines.append('  <rect x="860" y="600" width="310" height="56" rx="8" fill="white" stroke="#e5e7eb" stroke-width="1"/>')
lines.append('  <text x="875" y="622" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="11" font-weight="600" fill="#6b7280">图例</text>')
legend_items = [
    ("#2563eb", "核心枢纽"),
    ("#ec4899", "输入层"),
    ("#3b82f6", "架构层"),
    ("#06b6d4", "工具/训练"),
    ("#f97316", "交互层"),
    ("#22c55e", "Agent/对齐"),
    ("#8b5cf6", "记忆/检索"),
]
leg_x = 875
for color, text in legend_items:
    lines.append(f'  <rect x="{leg_x}" y="630" width="10" height="10" rx="3" fill="{color}"/>')
    lines.append(f'  <text x="{leg_x+14}" y="639" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="9" fill="#6b7280">{text}</text>')
    leg_x += len(text) * 9 + 28

lines.append('</svg>')

# Write output
out_path = "/Users/jiangchuan/Desktop/projects/Notes/llm-wiki/wiki/ai-fundamentals/syntheses/ai-core-concepts/concept-network.svg"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"SVG generated: {out_path}")
print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")
