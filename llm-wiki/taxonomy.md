# Taxonomy（书架 · 动态维护）

> **规则**：新建 / 重命名 / 合并 / 删除「门类」文件夹前，必须由你明确同意；Agent 只提案，不擅自改磁盘结构。

## 与 Collect / raw 的分工（降低重复维护）

| 材料 | 职责 |
|------|------|
| **本文件 `taxonomy.md`** | **有哪些顶层门类**（及可选子主题说明）；人审门槛；`layout` 会核对 `raw/<shelf>/`、`wiki/<shelf>/` 是否存在 |
| **`tools/source_registry.tsv`** | **每条来源类型**的匹配规则、**`raw_dir`**、**adapter**（机器与 Agent 路由的单一事实来源） |
| **`raw/README.md`** | **`raw_dir` 分桶含义**（介质 vs 平台）；不复制 TSV 逐行映射 |
| **`docs/collect-workflow.md`** | Collect **操作顺序**、CLI 用法；**不**维护第二张 adapter 对照表 |

新增来源类型：改 TSV +（如需）新 skill 目录；**仅**当新开顶层书架时才改本文件并建 `raw/<shelf>/`、`wiki/<shelf>/`。

## 当前门类（shelves）

| shelf_id | 说明 | raw根路径 | wiki 根路径 |
|----------|------|------------|-------------|
| ai-fundamentals | AI 理论基础：历史脉络、重要论文、技术演进、LLM 原理 | `raw/ai-fundamentals/` | `wiki/ai-fundamentals/` |
| agent | 编码智能体、Harness、工具链与仓库治理 | `raw/agent/` | `wiki/agent/` |
| software-fundamentals | 软件工程基础理论：经典书籍、设计原则、架构方法论 | `raw/software-fundamentals/` | `wiki/software-fundamentals/` |
| sdd | 规范驱动开发（Spec-Driven Development）：框架生态、源码实现、Agentic Skills | `raw/sdd/` | `wiki/sdd/` |

### 子主题（可选）

在 shelf 下可用**固定子文件夹**收窄主题（与 `raw/README.md` 约定一致），例如：

| 子路径 | 说明 |
|--------|------|
| `harness-engineering/` | Harness Engineering 相关素材与编译页 |
| `core-architecture/` | Agent 核心架构设计：架构模式、记忆系统、工具集成、多 Agent 协调 |

**raw 子目录**：在子主题（或直接 shelf）下，按 TSV 的 **`raw_dir`** 落盘；命名含义见 **`raw/README.md`**。

对应 wiki：`wiki/agent/harness-engineering/{sources,entities,concepts,syntheses}/`。

## 变更记录

- 2026-04-30 — 新增门类 `software-fundamentals`（软件工程基础理论）；调整 `sdd` 说明（移除"理论基础"）
- 2026-04-29 — 新增门类 `sdd`（规范驱动开发：框架生态、源码实现、Agentic Skills）
- 2026-04-19 — 新增门类 `ai-fundamentals`（AI 理论基础）
- 2026-04-14 — 新增门类 `agent`；子主题 `harness-engineering/`（用户确认）
- （历史）— 初始化 taxonomy；移除占位 `_example` 行
