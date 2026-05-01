# ProMem 设计文档

> **版本**：v1.0  
> **日期**：2026-03-17  
> **状态**：设计完成

---

## 一、产品定位

### 1.1 基本信息

- **名称**：ProMem —— 面向小型研发团队（3-8人）的知识飞轮引擎
- **灵感来源**：OpenClaw 的自我进化机制（沉淀→压缩→检索→进化）
- **核心理念**：让项目知识自动沉淀、压缩、检索、进化，并以此为基座驱动需求功能测试全流程

### 1.2 核心能力

| 能力 | 描述 |
|------|------|
| **项目上下文记忆系统** | 自动捕获、结构化存储、智能检索项目中的决策、踩坑、规则等知识 |

---

## 二、核心架构：技能层模式

### 2.1 设计哲学

ProMem **不是独立工具**，而是融入 Claude/Cursor/Qoder 等现有 AI 工具的**技能层**。

- **零配置**：不需要用户配置 API Key，复用宿主工具的 LLM 能力
- **数据层**：`.promem/` 目录在项目中，Git 追踪，人类可读
- **跨工具兼容**：通过 `integrations/` 目录为不同宿主工具提供适配

### 2.2 架构图：源码/数据分离

**npm 包结构（源码）：**
```
promem/                     # npm 包
├── package.json
├── bin/promem.js
└── src/
    ├── commands/           # CLI 命令（init/search/capture/compact/evolve/score/hooks）
    ├── utils.js
    ├── scripts/            # Python 核心脚本
    └── templates/          # init 模板 + hooks + 集成模板
```

**用户项目（npx promem init 后）：**
```
project/
├── .promem/
│   ├── memory/
│   │   ├── decisions/      # 技术决策
│   │   ├── bugs/           # Bug 修复记录
│   │   ├── rules/          # 隐式规则
│   │   ├── entities/       # 配置实体
│   │   ├── summaries/      # 压缩摘要（compact 生成）
│   │   ├── suggestions/    # 进化建议（evolve 生成）
│   │   └── archive/        # 归档记忆（不参与检索）
│   ├── config.yaml
│   ├── RULES.md
│   ├── PATTERNS.md
│   └── .gitignore
├── .cursorrules            # Cursor 集成（可选）
├── CLAUDE.md               # Claude 集成（可选）
└── .git/hooks/             # Git Hooks
```

### 2.3 两个设计原则

| 原则 | 说明 |
|------|------|
| **记忆即文件** | Markdown 存储，Git 追踪，人类可读 |
| **网关即宿主** | 宿主工具本身就是协调者，无需额外网关层 |

### 2.4 宿主工具适配

| 宿主工具 | 适配文件 | 路径 |
|----------|---------|------|
| Qoder | qoder-skill.tpl | 项目根目录 `.agents/skills/` |
| Cursor | .cursorrules | 项目根目录 `.cursorrules` |
| Claude | CLAUDE.md | 项目根目录 `CLAUDE.md` |

### 2.5 CLI 命令接口

7 个命令：

| 命令 | 说明 |
|------|------|
| `npx promem init` | 交互式初始化（选择 AI 工具、hooks 配置） |
| `npx promem search "keyword"` | 混合检索 |
| `npx promem capture` | 从 Git commit 捕获知识 |
| `npx promem compact --category decisions` | 结构化压缩 |
| `npx promem evolve --check` | 进化分析 |
| `npx promem score --score` | 重要性评分 |
| `npx promem score --archive` | 自动归档低价值记忆 |
| `npx promem hooks` | 安装 Git Hooks |

---

## 三、记忆引擎：四阶段闭环

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Capture   │ ──▶ │   Compact   │ ──▶ │   Recall    │ ──▶ │   Evolve    │
│   自动沉淀   │     │  结构化压缩  │     │   混合检索   │     │   规则进化   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                                                            │
       └────────────────────── 闭环反馈 ──────────────────────────────┘
```

### 3.1 阶段一：自动沉淀（Capture）

#### 三种触发方式

| 触发方式 | 机制 | 示例 |
|----------|------|------|
| **Git Hook 自动捕获** | commit/merge 时自动提取 | `post-commit` 分析提交信息和 diff |
| **宿主工具对话识别** | Prompt 指令引导 LLM 自动识别 | 检测到"我们决定..."模式时触发 |
| **技能产出回写** | 测试发现的 Bug 模式自动沉淀 | 测试失败时自动记录失败模式 |

#### 沉淀物分类

| 目录 | 内容类型 | 示例 |
|------|---------|------|
| `decisions/` | 技术决策 | "选择 Zustand 作为状态管理方案" |
| `bugs/` | 踩坑与解法 | "Safari Date.parse 不支持 YYYY-MM-DD 格式" |
| `rules/` | 业务规则 | "V3 及以上会员才显示专属价格" |
| `entities/` | 关键实体 | "User 实体的 phone 字段已脱敏" |
| `summaries/` | 压缩摘要 | compact 生成的结构化摘要 |
| `suggestions/` | 进化建议 | evolve 生成的规则建议（pending→approved） |

#### Memory 目录更新机制

| 目录 | 写入来源 | 触发时机 | 说明 |
|------|----------|----------|------|
| decisions/ | capture_from_commit.py | 自动（post-commit） | 检测到依赖变更或接口变更 |
| bugs/ | capture_from_commit.py | 自动（post-commit） | 检测到 fix/bugfix/hotfix 关键词 |
| rules/ | 手动/宿主工具 | 手动 | 对话中发现的隐式规则 |
| entities/ | capture_from_commit.py | 自动（post-commit） | 配置文件变更 |
| summaries/ | compact.py | 手动/阈值触发 | 记忆压缩摘要 |
| suggestions/ | evolve.py | 手动分析 | 进化建议（pending→approved） |
| archive/ | compact.py / importance.py | 自动 | 归档记忆，不参与检索 |

#### 安全守卫

| 守卫机制 | 阈值/规则 |
|----------|---------|
| **语义去重** | 相似度 > 0.95 自动合并 |
| **敏感信息过滤** | 自动识别并脱敏 API Key、密码等 |
| **单次上限** | 每次沉淀最多 5 条，防止信息过载 |

#### 接口定义

**capture_from_commit.py**
- 调用方式：`python .promem/scripts/capture_from_commit.py [--since <commit>]`
- 输入：读取最近一次 commit 的 diff 和 message（或指定 commit）
- 输出：写入 `.promem/memory/{category}/YYYY-MM-{slug}.md`
- 返回码：0 成功，1 无有效知识提取，2 执行错误

**Prompt 级沉淀协议**（宿主工具调用）：
- 触发：LLM 识别到知识模式
- 动作：将结构化内容追加到对应分类的 Markdown 文件
- 格式：遵循附录 A 中的模板

### 3.2 阶段二：结构化压缩（Compact）

#### 触发条件

- **手动触发**：用户显式调用压缩命令
- **自动触发**：原始记录超过阈值（默认 50 条）

#### 压缩模板必填字段

```yaml
# summaries/{module}_summary.md

## 关键决策
- [决策1]: 原因及适用范围
- [决策2]: 原因及适用范围

## 活跃约束
- [约束1]: 适用场景
- [约束2]: 适用场景

## 待办 & 未决
- [ ] 未解决问题1
- [ ] 未解决问题2

## 高频 Bug 模式
- [模式1]: 触发条件 → 解法
- [模式2]: 触发条件 → 解法

## 关键标识符
- entity: User, Order, Payment
- api: /api/v1/users, /api/v1/orders
```

#### 压缩策略

- **原始记录不删除**：归档到 `archive/` 目录
- **压缩摘要位置**：放在分类目录顶层（`summaries/`）
- **版本追踪**：每次压缩生成新版本，保留历史
- **自动归档**：压缩后保留最近 N 条，其余移入 `archive/`

#### 生命周期管理

压缩操作完成后，自动执行归档：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `compact_keep_recent` | 10 | 压缩后保留最近 N 条原始记录 |

#### 接口定义

**compact.py**
- 调用方式：`python .promem/scripts/compact.py [--category <decisions|bugs|rules|entities>] [--force]`
- 输入：读取指定分类下的所有原始记录
- 输出：生成/更新 `.promem/memory/summaries/{category}_summary.md`
- 行为：--force 忽略阈值强制压缩；无参数时检查所有分类
- 返回码：0 成功（有压缩发生），1 未达阈值跳过，2 执行错误
- 压缩后自动将旧记录移入 `archive/`（可通过 `--no-archive` 跳过）

### 3.3 阶段三：混合检索（Recall）

> **注意**：检索自动跳过 `archive/` 目录，归档记忆不参与搜索和排名。

#### 三种检索方式

| 检索方式 | 触发时机 | 用途 |
|----------|---------|------|
| **自动注入** | 技能运行前 | 根据上下文自动检索 top-3 注入 LLM prompt |
| **主动搜索** | 用户手动 | 响应用户的知识查询请求 |
| **上下文关联** | Git diff 触发 | 关联该模块的历史知识 |

#### 混合搜索引擎

**最终得分计算公式**：

```
Score = α × BM25_关键词分 + β × 向量_语义分 + γ × 时间_衰减分
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| α | 0.3 | 关键词匹配权重 |
| β | 0.5 | 语义相似度权重 |
| γ | 0.2 | 时间衰减权重（新内容更相关） |

**MMR 去重**：确保返回结果多样性，避免重复相似内容。

#### 接口定义

**index_memory.py**
- 调用方式：`python .promem/scripts/index_memory.py [--incremental | --full]`
- 输入：扫描 `.promem/memory/` 下所有 Markdown 文件
- 输出：更新 `.promem/.index.db`（SQLite + 向量索引）
- 行为：--incremental 仅索引新增/修改的文件；--full 全量重建
- 返回码：0 成功，2 执行错误

**检索查询接口**（供宿主工具 Prompt 调用）：
- 调用方式：`python .promem/scripts/index_memory.py --query "关键词" [--top-k 3]`
- 输出格式：JSON 数组，每项包含 {file, title, snippet, score}

### 3.4 阶段四：规则进化（Evolve）

#### 进化载体

| 文件 | 内容 | 更新频率 |
|------|------|---------|
| `RULES.md` | 团队研发规则 | 低（需审核） |
| `PATTERNS.md` | 常见模式库 | 中（自动建议） |
| `SKILLS.md` | 技能配置 | 低（手动调整） |

#### 进化机制

| 触发条件 | 进化动作 |
|----------|---------|
| 同类决策 **3 次以上** | 建议提炼为规则，写入 `RULES.md` |
| 同类 Bug **2 次以上** | 建议写入 `PATTERNS.md` |
| 规则被多次引用 | 权重提升，优先展示 |

#### 人工审核门

```
进化流程：
  自动检测 → 生成建议 → PR/MR → 至少一人 approve → 规则生效
```

---

## 四、交互式初始化流程

### 4.1 `npx promem init` 交互过程

```
$ npx promem init

🚀 ProMem 初始化向导

? 选择要集成的 AI 工具（多选）:
  ◉ Cursor (.cursorrules)
  ◉ Claude (CLAUDE.md)
  ◯ Qoder (qoder-skill.tpl)

? 是否安装 Git Hooks？
  ◉ 是（推荐）
  ◯ 否

✅ 初始化完成！
   - 创建 .promem/ 目录结构
   - 生成 .cursorrules
   - 生成 CLAUDE.md
   - 安装 Git Hooks
```

### 4.2 非交互模式

```bash
# 使用默认配置，跳过所有交互
npx promem init --yes

# 指定 AI 工具
npx promem init --yes --tools cursor,claude

# 跳过 hooks 安装
npx promem init --yes --no-hooks
```

### 4.3 init 生成的文件

| 文件 | 条件 | 说明 |
|------|------|------|
| `.promem/` | 必选 | 记忆数据目录 |
| `.promem/config.yaml` | 必选 | 配置文件 |
| `.promem/RULES.md` | 必选 | 团队规则模板 |
| `.promem/PATTERNS.md` | 必选 | 模式库模板 |
| `.cursorrules` | 选择 Cursor | Cursor 集成 |
| `CLAUDE.md` | 选择 Claude | Claude 集成 |
| `.git/hooks/*` | 选择安装 hooks | Git Hooks |

---

## 五、自动触发机制：三层协作

### 5.1 第一层：Prompt 级自动触发

在宿主工具系统指令中植入自动行为：

| 时机 | 自动行为 |
|------|---------|
| **对话开始前** | 自动检索 `.promem/` 注入上下文 |
| **对话中检测到决策** | 识别"我们决定..."等模式时自动沉淀 |
| **编辑代码时** | 自动关联该模块历史知识 |

**局限性**：靠 Prompt 引导 LLM，偶尔可能遗漏。

### 5.2 第二层：Git Hook 自动触发

| Hook | 触发时机 | 执行动作 |
|------|---------|---------|
| `post-commit` | 提交后 | 分析 commit，自动沉淀 + 更新索引 |
| `pre-push` | 推送前 | 回归分析，提醒影响范围 |
| `post-merge` | 合并后 | 更新记忆索引 |

**优势**：确定性执行，100% 可靠。

### 5.2.1 错误处理与降级策略

| Hook / 脚本 | 失败行为 | 降级策略 |
|-------------|---------|----------|
| post-commit | **不阻塞** commit | 仅 stderr 输出告警，跳过本次沉淀 |
| pre-push | **可配置**（config.yaml: `hooks.pre_push_blocking: false`） | 默认不阻塞，仅输出回归建议；可设为阻塞模式 |
| post-merge | **不阻塞** merge | 跳过索引更新，下次 commit 时自动补建 |
| index_memory.py | 索引损坏时自动检测 | 删除 `.index.db` 并全量重建 |
| compact.py | 压缩失败 | 保留原始记录不变，下次触发时重试 |

### 5.3 第三层：定时/条件脚本

| 触发条件 | 执行动作 |
|----------|---------|
| 记忆条数超阈值（默认 50） | 自动触发压缩 |
| 手动调用 | 按需执行各类维护任务 |

### 5.4 自动化程度评估

| 能力 | 自动化程度 | 实现机制 |
|------|-----------|---------|
| 记忆检索 | ★★★★☆ 高 | Prompt + 文件读取 |
| 决策沉淀 | ★★★☆☆ 中 | Prompt 引导，偶尔遗漏 |
| Commit 沉淀 | ★★★★★ 确定性 | Git Hook |
| 回归分析 | ★★★★★ 确定性 | Git Hook + 脚本 |
| 压缩 | ★★★★☆ 高 | 条件脚本 |
| 规则进化 | ★★★☆☆ 中 | LLM + 人工审核 |

---

## 六、知识智能层

### 6.1 知识重要性判断模型

**核心公式**：

```
重要性 = 复用概率 × 遗忘风险 × 踩坑代价
```

### 6.2 六类核心工程知识

| 优先级 | 知识类型 | 示例 |
|--------|---------|------|
| **P0** | 决策+原因 | "选 Zustand 因为团队小、学习成本低" |
| **P0** | 踩坑+解法 | "Safari Date.parse 不支持 YYYY-MM-DD，需用 YYYY/MM/DD" |
| **P1** | 隐式约束 | "支付接口幂等靠 request_id 字段" |
| **P1** | 业务规则 | "V3 及以上会员才显示专属价格" |
| **P2** | 架构边界 | "UserService 返回的 phone 字段已脱敏" |
| **P2** | 环境差异 | "测试环境短信接口是 mock，验证码固定 123456" |

### 6.3 四种捕获信号源

#### 信号源①：对话模式识别

识别关键模式并提取三元组：

| 检测模式 | 示例 |
|----------|------|
| "我们决定..." | "我们决定用 PostgreSQL 因为需要 JSON 支持" |
| "这个 bug 是因为..." | "这个 bug 是因为时区转换没处理" |
| "必须要..." | "必须要先调用 init 方法" |
| "不能..." | "不能直接修改 state，要用 setState" |

**提取三元组**：`事实 + 原因 + 适用范围`

#### 信号源②：代码变更分析

Git Hook 层自动分析：

| 变更类型 | 分析内容 |
|----------|---------|
| Config 变更 | 配置项增删改 |
| 接口变更 | API 签名变化 |
| Fix commit | 修复了什么问题 |
| 依赖变更 | 新增/升级/移除依赖 |

#### 信号源③：重复行为检测

| 检测条件 | 动作 |
|----------|------|
| 同一主题被搜索 **2 次以上** | 标记为知识缺口 |
| 同一问题被问 **3 次以上** | 建议沉淀为文档 |



### 6.4 六种供给时机

| 开发者动作 | 供给内容 | 供给方式 |
|-----------|---------|---------|
| **编辑文件** | 该模块约束、踩坑、决策 | 上下文自动注入 |
| **讨论需求变更** | 历史约束+影响范围 | 主动提醒 |
| **首次接触模块** | 模块知识摘要 | 一次性推送 |
| **提交代码** | 规则合规检查 | Git Hook 提醒 |
| **测试失败** | 相似 Bug 历史+解法 | 自动关联 |
| **搜索知识** | 精准结果+相关推荐 | 检索响应 |

### 6.5 精准度闭环

| 信号 | 动作 |
|------|------|
| 被引用的知识 | 权重提升 |
| 被标记“已过时” | 归档不再推送 |
| 符合归档条件 | 自动移入 archive/ |
| 多次搜索未命中 | 提示知识缺口 |
| 团队 approve/reject | 训练捕获规则，优化识别准确率 |

---

## 七、团队协作

### 7.1 共享机制

`.promem/` 目录跟随 Git 仓库同步，**零额外基础设施**。

```
仓库
├── src/
├── tests/
├── .promem/    ← Git 追踪，团队共享
│   ├── memory/
│   ├── RULES.md
│   └── ...
└── .gitignore  ← 排除 .index.db 等本地文件
```

### 7.2 冲突处理策略

| 文件类型 | 冲突概率 | 处理策略 |
|----------|---------|---------|
| 记忆文件 | 极低 | append-only 设计，几乎不冲突 |
| 压缩摘要 | 低 | 保留双方版本，下次 compact 自动去重 |
| 规则文件 | 中 | 需人工 resolve，确保规则一致性 |

### 7.3 权限模型（轻量级）

| 操作 | 权限要求 |
|------|---------|
| 沉淀知识 | 任何人 |
| 标记"已过时" | 任何人 |
| 规则进化 | 至少一人 approve |
| 删除记忆 | 不允许（只能标记过时） |

---

## 八、技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| **记忆存储** | Markdown | 人类可读、Git 友好、无需额外工具查看 |
| **搜索索引** | SQLite + sqlite-vec | 嵌入式、零配置、支持向量检索 |
| **辅助脚本** | Python | 跨平台、NLP 生态丰富 |
| **Git Hook** | Shell + Python | 标准 Git 机制，无需额外依赖 |
| **向量嵌入** | 宿主 LLM / 本地小模型 | 优先复用宿主能力，降级用 all-MiniLM-L6-v2 |

### 向量嵌入降级策略

```
首选：宿主 LLM 的 embedding API
  ↓ (不可用)
降级：本地 all-MiniLM-L6-v2
  ↓ (资源受限)
兜底：纯 BM25 关键词搜索
```

---

## 九、目录结构

### npm 包结构（promem 源码）

```
promem/                          # npm 包
├── package.json
├── bin/promem.js                # CLI 入口
└── src/
    ├── commands/                # CLI 命令实现
    │   ├── init.js              # 交互式初始化
    │   ├── search.js            # 混合检索
    │   ├── capture.js           # 知识捕获
    │   ├── compact.js           # 结构化压缩
    │   ├── evolve.js            # 进化分析
    │   ├── score.js             # 重要性评分
    │   └── hooks.js             # Git Hooks 安装
    ├── utils.js                 # 公共工具
    ├── scripts/                 # Python 核心脚本
    │   ├── capture_from_commit.py
    │   ├── index_memory.py
    │   ├── compact.py
    │   ├── evolve.py
    │   ├── importance.py
    │   └── memory_utils.py
    └── templates/               # 初始化模板
        ├── config.yaml
        ├── RULES.md
        ├── PATTERNS.md
        ├── gitignore
        ├── hooks/               # Git Hook 模板
        │   ├── post-commit
        │   ├── pre-push
        │   └── post-merge
        └── integrations/        # AI 工具集成模板
            ├── cursorrules.tpl
            ├── claude-md.tpl
            └── qoder-skill.tpl
```

### 用户项目结构（npx promem init 后）

```
project/
├── .promem/                     # 记忆数据目录
│   ├── memory/                  # 记忆存储
│   │   ├── decisions/           # 技术决策
│   │   │   └── 2026-03-auth-zustand.md
│   │   ├── bugs/                # 踩坑与解法
│   │   │   └── 2026-02-safari-date-parse.md
│   │   ├── rules/               # 业务规则
│   │   │   └── membership-pricing.md
│   │   ├── entities/            # 关键实体
│   │   │   └── user-entity.md
│   │   ├── summaries/           # 压缩摘要（compact 生成）
│   │   ├── suggestions/         # 进化建议（evolve 生成）
│   │   │   └── 2026-03-SUG-001.md
│   │   └── archive/             # 归档记忆（不参与检索）
│   ├── config.yaml              # 配置文件
│   ├── RULES.md                 # 团队研发规则
│   ├── PATTERNS.md              # 常见模式库
│   ├── .index.db                # 搜索索引（.gitignore）
│   └── .gitignore
│
├── .cursorrules                 # Cursor 集成（可选）
├── CLAUDE.md                    # Claude 集成（可选）
└── .git/hooks/                  # Git Hooks（可选）
    ├── post-commit
    ├── pre-push
    └── post-merge
```

### config.yaml 示例

```yaml
# ProMem 配置文件

# 沉淀配置
capture:
  max_per_session: 5          # 单次会话最大沉淀条数
  similarity_threshold: 0.95  # 去重相似度阈值
  sensitive_patterns:         # 敏感信息正则
    - "(?i)api[_-]?key"
    - "(?i)password"
    - "(?i)secret"

# 压缩配置
compact:
  auto_threshold: 50          # 自动压缩阈值
  keep_original: true         # 保留原始记录

# 检索配置
recall:
  top_k: 3                    # 自动注入的记忆条数
  weights:
    bm25: 0.3
    semantic: 0.5
    recency: 0.2

# Hook 配置
hooks:
  pre_push_blocking: false    # pre-push 失败是否阻塞推送
  fail_silent: true           # Hook 失败时静默（仅 stderr），不弹窗

# 生命周期配置
lifecycle:
  archive_after_months: 6     # 超过此月数的记忆可被归档
  min_importance: 0.3         # 重要性低于此值可被归档
  inactive_months: 3          # 未引用超过此月数可被归档
  compact_keep_recent: 10     # compact 后保留最近 N 条

# 进化配置
evolve:
  decision_threshold: 3       # 同类决策次数 → 规则
  bug_threshold: 2            # 同类 Bug 次数 → 模式
  require_approval: true      # 规则变更需审批
```

---

## 附录 A：记忆文件格式规范

### 决策记录模板

```markdown
# [标题]: 简短描述

## 日期
2026-03-17

## 背景
为什么需要做这个决策？

## 决策
具体决定了什么？

## 原因
为什么这样决定？考虑了哪些因素？

## 替代方案
考虑过但未采用的方案及原因。

## 影响范围
这个决策影响哪些模块/功能？

## 相关链接
- PR/MR 链接
- 讨论文档链接
```

### Bug 记录模板

```markdown
# [Bug]: 简短描述

## 日期
2026-03-17

## 症状
表现出什么问题？

## 根因
问题的根本原因是什么？

## 解法
如何修复的？

## 预防
如何避免再次发生？

## 相关代码
- 文件路径
- 关键代码片段

## 相关链接
- Issue 链接
- PR/MR 链接
```

---

## 附录 B：Git Hook 安装指南

### 使用 CLI 安装（推荐）

```bash
# 在项目根目录执行
npx promem hooks
```

### 初始化时安装

```bash
# init 时会询问是否安装 hooks
npx promem init

# 或直接确认安装
npx promem init --yes
```

---

## 附录 C：快速开始

### 1. 初始化 ProMem

```bash
# 克隆/创建项目后
cd your-project
npx promem init
```

### 2. 交互式选择

初始化向导会引导你：
- 选择要集成的 AI 工具（Cursor/Claude/Qoder）
- 是否安装 Git Hooks

或使用非交互模式：
```bash
npx promem init --yes --tools cursor,claude
```

### 3. 开始使用

正常使用宿主工具开发即可，ProMem 会自动：
- 在对话中注入相关知识
- 识别并沉淀重要决策
- 通过 Git Hook 捕获变更知识

### 4. 常用命令

```bash
# 搜索记忆
npx promem search "zustand 状态管理"

# 手动捕获知识
npx promem capture

# 压缩决策记录
npx promem compact --category decisions

# 检查进化建议
npx promem evolve --check

# 重要性评分
npx promem score --score
```

---

**文档结束**
