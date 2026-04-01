---
title: OpenClaw `.openclaw` 目录与多 Agent 配置地图
description: 基于 openclaw 源码与 docs.openclaw.ai 整理的速查手册，帮助定位配置与排障
updated: 2026-03-30
---

# OpenClaw `.openclaw` 目录与多 Agent 配置地图

> **本文目标**：读完能对「OpenClaw 有哪些能力、各能力对应的**磁盘位置**与 **`openclaw.json` 键路径**」有整体印象；日常出问题时能按表快速跳到正确文件或文档章节。

---

## 阅读路径

| 你想… | 建议阅读顺序 |
|--------|----------------|
| **5 分钟建立整体图景** | [30 秒心智模型](#30-秒心智模型) → [环境变量与路径优先级](#环境变量与路径优先级) → [`.openclaw` 目录一览](#openclaw-目录一览状态根目录) |
| **配置多 Agent / 路由** | [多 Agent 在磁盘上长什么样](#多-agent-在磁盘上长什么样) → [`openclaw.json` 里该改哪里](#openclawjson-网关主配置) → [官方 Multi-Agent 文档](https://docs.openclaw.ai/concepts/multi-agent) |
| **改人格、规则、工具说明（给模型看的）** | [Workspace（工作区）](#workspace工作区) — 改 `AGENTS.md`、`SOUL.md` 等 |
| **会话丢了 / 串了 / 想备份** | [`agents/<agentId>/sessions`](#agentsagentidagents-子目录) |
| **认证、OAuth、各通道密钥** | [`credentials/`](#credentialsoauth--通道凭据) |

---

## 30 秒心智模型

把 OpenClaw 想成一家**同时接待多个客户的咨询公司**：

| 真实概念 | 类比 |
|-----------|------|
| **状态根目录** `~/.openclaw` | 公司总机 + 档案室（配置、凭据、会话存档都在这里） |
| **`openclaw.json`** | 公司章程：谁接哪条线、默认行为、通道账号 |
| **Workspace** | 每位顾问的**办公桌**：上面有便签（`AGENTS.md`…）、项目笔记，是「给 AI 看的上下文」 |
| **`agents/<id>/agent`** | 这位顾问的**私有抽屉**：认证配置、模型侧状态等，**不要多人共用** |
| **`agents/<id>/sessions`** | 与每位客户对话的**卷宗柜**：聊天记录与会话元数据 |
| **`bindings`** | 来电转接规则：哪个号码/群/账号进线 → 交给哪位顾问 |

---

## 阅读指南

### 本文语境

- **Gateway**：本机或服务器上运行的 OpenClaw 网关进程，统一连接聊天应用与 Agent。
- **多 Agent**：多个 `agentId`，各自可有独立 **workspace**、**agentDir**、**会话命名空间**；入站消息通过 **`bindings`** 路由到对应 `agentId`。
- 文中默认状态目录为 **`~/.openclaw`**；若你改了环境变量，路径以前缀 **`$OPENCLAW_STATE_DIR`** 理解即可。

### 术语表（含「落点」）

| 术语 | 一句话 | 在本文中的落点 |
|------|--------|----------------|
| **State dir / 状态目录** | 可变数据根路径 | `~/.openclaw` 或 `OPENCLAW_STATE_DIR` |
| **Workspace** | Agent 默认工作目录与「人格/规则」文件所在处 | 配置：`agents.defaults.workspace` 或 `agents.list[].workspace`；默认磁盘：`~/.openclaw/workspace` |
| **agentDir** | 每 Agent 的私有状态（含 auth 等） | 配置：`agents.list[].agentDir`；默认：`~/.openclaw/agents/<id>/agent` |
| **Session store** | 会话存储 | 默认：`~/.openclaw/agents/<id>/sessions/` |
| **bindings** | 入站路由规则 | 仅存在于 `openclaw.json` 根级 `bindings` 数组 |

### 约定

- 路径统一用正斜杠；Windows 下亦为概念路径。
- 配置格式为 **JSON5**（可注释、尾逗号等），文件名为 **`openclaw.json`**。

---

## 环境变量与路径优先级

与「文件在哪」强相关的变量（摘自源码 `src/config/paths.ts`、`src/agents/workspace.ts`、`src/agents/agent-scope.ts`）：

| 变量 | 作用 |
|------|------|
| **`OPENCLAW_STATE_DIR`**（或旧名 `CLAWDBOT_STATE_DIR`） | 状态根目录；不设则默认为 `~/.openclaw`，若不存在则可能回退到旧目录名 `.clawdbot` 等（迁移兼容）。 |
| **`OPENCLAW_CONFIG_PATH`**（或 `CLAWDBOT_CONFIG_PATH`） | 主配置文件绝对路径；覆盖「状态目录下的 `openclaw.json`」默认。 |
| **`OPENCLAW_HOME`** | 解析 `~` 与 home-relative 路径时使用的 home（与部分路径拼接有关）。 |
| **`OPENCLAW_PROFILE`** | 非 `default` 时，**默认 workspace** 变为 `~/.openclaw/workspace-<profile>`（见 `resolveDefaultAgentWorkspaceDir`）。 |
| **`OPENCLAW_OAUTH_DIR`** | OAuth 目录覆盖；否则 OAuth 相关在 `$STATE_DIR/credentials` 下。 |

**配置候选路径**：若未指定 `OPENCLAW_CONFIG_PATH`，会按存在性在状态目录中查找 `openclaw.json` 及旧文件名 `clawdbot.json` / `moldbot.json` / `moltbot.json`（`resolveDefaultConfigCandidates`）。

---

## `.openclaw` 目录一览（状态根目录）

下面是 **典型安装** 下你会关心的结构（非穷举；插件与运行时会再生成缓存、日志等）。

```text
~/.openclaw/                          # 状态根目录（STATE）
├── openclaw.json                     # ★ 主配置（JSON5）
├── credentials/                      # OAuth、各通道凭据等（勿提交到 git）
│   └── oauth.json                  # OAuth 汇总（路径可由 OPENCLAW_OAUTH_DIR 影响）
├── agents/
│   ├── main/                       # agentId = main（默认）
│   │   ├── agent/                  # ★ 该 Agent 的 agentDir（认证配置等）
│   │   │   └── auth-profiles.json  # 多 Agent 时：每 Agent 独立，勿跨 Agent 复用目录
│   │   └── sessions/               # ★ 该 Agent 的会话存储
│   │       └── sessions.json       # 会话索引（具体设计见 session 子系统）
│   └── <其他 agentId>/             # 例如 work、coding…
│       ├── agent/
│       └── sessions/
├── workspace/                      # ★ 默认主工作区（可被 agents.defaults.workspace 覆盖）
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── USER.md
│   ├── ...
│   ├── skills/                     # 工作区级 skills（可选）
│   ├── memory/                     # 按日记忆（可选）
│   └── .openclaw/
│       └── workspace-state.json    # 工作区引导状态（源码 workspace.ts）
├── workspace-<profile>/            # OPENCLAW_PROFILE 非 default 时的默认 workspace 名模式
├── skills/                         # 用户/托管层 skills（与 workspace/skills 层级不同，见官方 Skills 文档）
└── sandboxes/                      # 启用沙箱时可能使用的沙箱工作区根（见 gateway/sandboxing 文档）
```

### 与「功能」的对应关系（速查）

| 功能域 | 优先看的配置键 | 优先看的磁盘位置 |
|--------|----------------|------------------|
| 网关端口 / 认证 / 对外 Web | `gateway.*`、`web.*` | `openclaw.json`；令牌常在 env 或 `gateway.auth` |
| 通道（WhatsApp/Telegram/…） | `channels.*` | `openclaw.json`；凭据在 `credentials/` 或通道专属子目录 |
| 多 Agent 定义 | `agents.list[]`、`agents.defaults` | `openclaw.json` |
| 入站路由 | `bindings` | 仅 `openclaw.json` |
| 模型与工具策略 | `agents.list[].model`、`agents.list[].tools`、`tools.*` | `openclaw.json`；每 Agent 的 `agentDir` 内有模型/认证相关状态 |
| 会话与历史 | `session.*`（全局策略） | `agents/<agentId>/sessions/` |
| 人格与提示词材料 | — | **Workspace** 下 `AGENTS.md`、`SOUL.md` 等 |
| Skills | `skills.*` | `~/.openclaw/skills` + 各 workspace 的 `skills/` |

---

## `openclaw.json`（网关主配置）

### 文件位置

- 默认：**`$OPENCLAW_STATE_DIR/openclaw.json`**，常见即 **`~/.openclaw/openclaw.json`**。
- 覆盖：**`OPENCLAW_CONFIG_PATH`**。

### 行为要点（排障时常用）

- 配置需通过 **严格 Schema 校验**；不合法时 **Gateway 可能拒绝启动**（官方 [Configuration](https://docs.openclaw.ai/gateway/configuration)）。
- 直接编辑文件后，Gateway 通常支持 **热重载**（以官方文档「config hot reload」为准）。
- CLI 辅助：`openclaw config get` / `set` / `unset`（见官方 Configuration 页）。

### 与多 Agent 强相关的键（根级）

| 键 | 作用 |
|----|------|
| **`agents`** | `defaults`：全局默认（如默认 workspace、模型、心跳、沙箱默认值等）；`list`：多个 Agent 条目。 |
| **`bindings`** | 路由：把 `(channel, accountId, peer, guildId, …)` 映射到 `agentId`。匹配优先级与「最具体优先」规则见 [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)。 |
| **`channels`** | 各通道账号、安全策略（allowlist、群规则等）；多账号时用 `accountId` 与 bindings 联合。 |
| **`tools`** | 全局工具策略；例如 `tools.agentToAgent` 控制 Agent 间协作（默认常关，需显式允许）。 |

**类型定义参考（源码）**：`OpenClawConfig` 见 `src/config/types.openclaw.ts`；`agents` 见 `src/config/types.agents.ts`。

### `agents.list[]` 常用字段（每个 Agent）

| 字段 | 含义 |
|------|------|
| **`id`** | `agentId`（如 `main`、`work`）。 |
| **`default`** | 是否为默认 Agent（多个 `default: true` 时取第一个并告警）。 |
| **`workspace`** | 该 Agent 的工作区路径；**未配置时的解析规则见下一节**。 |
| **`agentDir`** | 该 Agent 私有状态目录；**未配置时默认为** `$STATE/agents/<id>/agent`。 |
| **`model`** | 主模型及 fallback（可为字符串或对象）。 |
| **`tools` / `sandbox` / `skills` / `groupChat` / `identity`** | 每 Agent 工具策略、沙箱、技能过滤、群聊 mention、对外身份等。 |

---

## 多 Agent 在磁盘上长什么样

### 默认单 Agent（最常见）

- **`agentId`**：未显式配置时视为 **`main`**（见 `DEFAULT_AGENT_ID` 与 `listAgentIds` 逻辑）。
- **Workspace**：`~/.openclaw/workspace`（或 profile 下的 `workspace-<profile>`），除非 `agents.defaults.workspace` 或 `agents.list` 中覆盖。
- **agentDir**：`~/.openclaw/agents/main/agent`。
- **Sessions**：`~/.openclaw/agents/main/sessions`。

### 多 Agent（`openclaw agents add ...` 或手写 `agents.list`）

每一格「大脑」具备（官方 [Multi-Agent](https://docs.openclaw.ai/concepts/multi-agent)）：

- **独立 workspace**（文件工具默认 cwd、上下文注入）。
- **独立 agentDir**（含 **`auth-profiles.json`** 等）；**不要**把同一 `agentDir` 绑给两个 `agentId`。
- **独立 sessions** 目录：`agents/<agentId>/sessions`。

**Workspace 路径解析（源码 `resolveAgentWorkspaceDir`）要点**：

1. 若该 Agent 在 `agents.list[].workspace` 中显式配置 → 用它。
2. 否则若该 Agent 是 **默认 Agent** → 使用 `agents.defaults.workspace`（若有），否则使用 `resolveDefaultAgentWorkspaceDir()`（`~/.openclaw/workspace` 或带 profile 的目录）。
3. 否则（非默认且无显式 workspace）→ **`$STATE/workspace-<agentId>`**。

**agentDir 解析（`resolveAgentDir`）**：显式 `agents.list[].agentDir`，否则 **`$STATE/agents/<agentId>/agent`**。

---

## `agents/<agentId>/`（agents 子目录）

| 路径 | 用途 | 出问题时的线索 |
|------|------|------------------|
| **`.../agent/`** | 该 Agent 的私有运行时状态；**认证配置文件**如 `auth-profiles.json`（路径以你机子为准）。 | 两个 Agent 「抢」同一登录态 → 检查是否错误共用 `agentDir`。 |
| **`.../sessions/`** | 会话 transcript 与 `sessions.json` 等。 | 「换 Agent 后历史不见了」→ 历史在 **按 agentId 分目录** 的 sessions 下；不是 workspace。 |

---

## Workspace（工作区）

### 定位：和 `~/.openclaw` 的关系

- **Workspace**：Agent 的「家」— **文件工具默认 cwd**、**`AGENTS.md` 等注入上下文**的地方（官方 [Agent Workspace](https://docs.openclaw.ai/concepts/agent-workspace)）。
- **`~/.openclaw`**：**配置、凭据、会话**；与 workspace **分离**。
- **不是硬沙箱**：相对路径以 workspace 为锚点；绝对路径仍可能访问全机 — 需要隔离请用 **sandbox**（`agents.defaults.sandbox` / 每 Agent `sandbox`）。

### 配置入口

- 全局默认：`agents.defaults.workspace`
- 每 Agent：`agents.list[].workspace`

### 常见文件（启动时注入 / 引导）

下列文件名来自源码 `src/agents/workspace.ts` 中的默认常量与官方文档说明：

| 文件 | 角色 |
|------|------|
| **`AGENTS.md`** | 操作说明、规则、优先级 |
| **`SOUL.md`** | 人格、语气、边界 |
| **`USER.md`** | 用户画像与称呼偏好 |
| **`IDENTITY.md`** | 名称、风格、展示用信息 |
| **`TOOLS.md`** | 本地工具与习惯（**不**决定工具是否启用，是指引） |
| **`HEARTBEAT.md`** | 心跳任务简短清单 |
| **`BOOTSTRAP.md`** | 首次引导；完成后可删（官方文档） |
| **`MEMORY.md` / `memory.md`** | 长期记忆摘要（策略见 Memory 文档） |
| **`memory/YYYY-MM-DD.md`** | 按日记忆日志 |
| **`skills/`** | 工作区级 skills，与全局 `~/.openclaw/skills` 并存（名称冲突时遵循官方 Skills 说明） |
| **`canvas/`** | 节点端 Canvas 等（如 `canvas/index.html`） |

**体积限制**：超长引导文会被截断；可调 `agents.defaults.bootstrapMaxChars` / `bootstrapTotalMaxChars`（默认值见官方 Agent Workspace 页）。

### 工作区内 `.openclaw/workspace-state.json`

- 记录引导/种子状态等元数据（见 `workspace.ts` 中 `WORKSPACE_STATE_FILENAME`），**不属于**给模型阅读的主材料，一般无需手改。

---

## 排障：现象 → 去哪看

| 现象 | 先检查 |
|------|--------|
| Gateway 起不来 | `openclaw doctor`；校验 `openclaw.json` Schema；看日志 `openclaw logs`（CLI 以官方为准） |
| 消息进了「错误的 Agent」 | `bindings` 顺序与 specificity；`openclaw agents list --bindings`；官方路由优先级表 |
| 同一通道多账号混乱 | `channels.*.accounts` 与 binding 里的 **`accountId`** 是否一致 |
| 模型/认证串了 | 每 Agent 的 **`agentDir`** 是否被共用；`auth-profiles.json` 是否在预期目录 |
| 找不到聊天记录 | **`agents/<agentId>/sessions`**；确认会话 key 是否带 `agent:<id>:` 前缀（见 Session 概念文档） |
| 改了人格不生效 | 是否改在 **正确 workspace**；是否有多份 `~/openclaw` 旧目录（官方建议 `openclaw doctor` 会提示多余 workspace） |

---

## 核心结论（3 条）

1. **`openclaw.json`** 管 **路由、通道、Agent 清单与默认值**；**人格长文**主要在 **workspace 里的 Markdown**。
2. **每 Agent 的「私有状态」在 `agents/<agentId>/agent`，会话在 `agents/<agentId>/sessions`** — 与 workspace 路径无关，三者不要混作一谈。
3. **多 Agent 路由靠 `bindings` + 通道 `accountId`/`peer`**；更具体的匹配优先（详见官方 Multi-Agent）。

---

## 参考资料（溯源）

- 官方文档索引：<https://docs.openclaw.ai/llms.txt>
- [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)
- [Agent Workspace](https://docs.openclaw.ai/concepts/agent-workspace)
- [Configuration](https://docs.openclaw.ai/gateway/configuration)
- [Channel Routing](https://docs.openclaw.ai/channels/channel-routing)
- 本地源码（路径以你克隆为准）：`src/config/paths.ts`、`src/agents/agent-scope.ts`、`src/agents/workspace.ts`、`src/config/types.openclaw.ts`、`src/config/types.agents.ts`

---

*文档由学习助手流程根据上述源码与官方页面整理，若上游变更请以官方文档与当前版本源码为准。*
