# ProMem

> AI Agent 的项目记忆系统 — 让你的 AI 编程助手拥有项目长期记忆

## 为什么需要 ProMem？

AI 编程工具虽然强大，但每次对话都从零开始，没有项目上下文记忆。团队踩过的坑、做过的技术决策、隐式规则——这些宝贵经验无法沉淀，导致 AI 反复给出不符合项目实际的建议。ProMem 让 AI 工具拥有项目长期记忆，越用越懂你的项目。

## 特性

- 🧠 **自动知识捕获** — Git commit 时自动提取技术决策、Bug 修复、配置变更
- 🔍 **混合检索** — BM25 全文 + 向量语义 + 时间衰减，精准召回
- 📦 **智能压缩** — 记忆过多时自动生成结构化摘要
- 🧬 **知识进化** — 检测重复模式，提炼为团队规则
- 🔌 **多工具支持** — Cursor / Claude Code / Qoder 一键集成
- 📝 **Git 同步** — 所有知识以 Markdown 存储，随代码库共享
- ⚡ **零依赖** — 无需 API Key，无需外部服务

## 快速开始

```bash
npx promem init
```

交互式选择你的 AI 编程工具，自动完成初始化：

```
🧠 ProMem - Project Memory for AI Agents

? Select your AI coding tools: (Space to toggle, Enter to confirm)
❯ ◉ Cursor
  ◉ Claude Code
  ◯ Qoder

? Enable auto-capture on git commit? (Y/n)

✅ ProMem initialized successfully!
```

## 生成的文件

```
your-project/
├── .promem/                # 知识存储（Git 同步）
│   ├── memory/
│   │   ├── decisions/      # 技术决策
│   │   ├── bugs/           # Bug 修复记录
│   │   ├── rules/          # 隐式规则
│   │   ├── entities/       # 配置实体
│   │   ├── summaries/      # 压缩摘要
│   │   ├── suggestions/    # 进化建议
│   │   └── archive/        # 归档记忆（自动管理，不参与检索）
│   ├── config.yaml
│   ├── RULES.md            # 团队规则
│   └── PATTERNS.md         # Bug 模式库
├── .cursorrules            # Cursor 集成（如选择）
├── CLAUDE.md               # Claude 集成（如选择）
└── AGENTS.md               # Qoder 集成（如选择）
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `npx promem init` | 初始化项目（交互式选择工具和 hooks） |
| `npx promem search "关键词"` | 搜索项目记忆 |
| `npx promem capture` | 从最近 commit 捕获知识 |
| `npx promem compact --all` | 压缩所有分类的记忆（压缩后自动归档旧文件） |
| `npx promem evolve --check` | 检查进化建议 |
| `npx promem score --score` | 计算知识重要性 |
| `npx promem score --archive` | 自动归档低价值记忆 |
| `npx promem hooks install` | 安装 Git Hooks |
| `npx promem log` | 查看运行日志 |
| `npx promem log --stats` | 查看运行统计摘要 |

## 工作原理

ProMem 基于四循环知识飞轮：

```
Capture → Compact → Recall → Evolve
  捕获       压缩      召回      进化
```

1. **Capture（捕获）**：Git commit 后自动分析 diff，按规则沉淀到对应分类
2. **Compact（压缩）**：记忆积累到阈值后，生成结构化摘要
3. **Recall（召回）**：AI 工具编码时自动检索相关记忆，注入上下文
4. **Evolve（进化）**：检测重复模式，提炼为团队规则，经人工审核后生效

## 记忆自动捕获

ProMem 通过 Git Hooks 自动捕获：

| Hook | 触发时机 | 动作 |
|------|---------|------|
| post-commit | 每次 commit | 分析 diff，沉淀决策/Bug/配置变更 |
| pre-push | 推送前 | 检查记忆完整性 |
| post-merge | 合并后 | 增量重建索引 |

## 知识进化

```bash
# 检查是否有新的进化建议
npx promem evolve --check

# 查看建议详情
npx promem evolve --history

# 应用建议（写入 RULES.md 或 PATTERNS.md）
npx promem evolve --apply SUG-001
```

进化流程：检测模式 → 生成建议（pending）→ 人工审核 → 应用（approved）

## 记忆生命周期

ProMem 自动管理记忆的生命周期，避免记忆无限膨胀：

### 归档机制

| 触发方式 | 条件 | 行为 |
|----------|------|------|
| compact 后自动归档 | 压缩生成摘要后 | 旧文件移入 `archive/`，保留最近 10 条 |
| 低价值记忆归档 | 超过 6 个月 + 评分 < 0.3 + 3 个月未引用 | 自动移入 `archive/` |

### 归档特性

- **archive/ 不参与检索**：索引和搜索自动跳过归档目录
- **归档是移动非删除**：可手动从 `archive/` 恢复到原目录

### 命令

```bash
# 预览将归档的文件
npx promem score --archive --dry-run

# 执行自动归档
npx promem score --archive

# 压缩后自动归档（默认行为）
npx promem compact --all

# 压缩时跳过归档
npx promem compact --all --no-archive
```

## 配置

`.promem/config.yaml` 支持自定义：

```yaml
capture:
  max_per_session: 5          # 每次 commit 最多沉淀条数
  similarity_threshold: 0.95  # 去重阈值
  
compact:
  threshold: 50               # 触发压缩的文件数阈值

evolve:
  decision_threshold: 3       # 决策规则提取阈值
  bug_threshold: 2            # Bug 模式提取阈值

lifecycle:
  archive_after_months: 6     # 超过此月数的记忆可被归档
  min_importance: 0.3         # 重要性低于此值可被归档
  inactive_months: 3          # 未引用超过此月数可被归档
  compact_keep_recent: 10     # compact 后保留最近 N 条
```

## 团队使用

```bash
# 1. 团队成员 clone 项目后
git clone your-project && cd your-project

# 2. 初始化 ProMem（选择自己的 AI 工具）
npx promem init

# 3. 正常开发，知识自动积累和共享
```

`.promem/memory/` 通过 Git 同步，团队共享同一份项目记忆。

## 非交互模式

适用于 CI 或脚本：

```bash
# 使用默认配置，指定工具
npx promem init --yes --tool cursor,claude

# 跳过 hooks 安装
npx promem init --skip-hooks

# 强制重新初始化
npx promem init --force
```

## 环境要求

- Node.js >= 14
- Python >= 3.6
- Git

## 本地开发与调试

```bash
# 1. 注册为全局命令（符号链接，修改源码后立即生效）
cd promem
npm link

# 2. 在任意 Git 项目中试用
cd /path/to/your-project
promem init
promem search "关键词"
promem capture

# 3. 直接调用 Python 脚本查看详细输出（调试用）
python3 promem/src/scripts/capture_from_commit.py --memory-root .promem/memory

# 4. 取消全局注册
npm unlink -g promem
```

## 灵感来源

ProMem 的知识飞轮设计灵感来自 [OpenClaw](https://github.com/openclawai/openclaw) 的自我进化机制。

## License

MIT
