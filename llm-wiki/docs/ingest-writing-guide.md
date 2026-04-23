# Wiki 写作指南（Ingest 成稿）

> llm-wiki Ingest 成稿写作指南：以 source 真实性为前提，追求结论先行、一图胜千言、简单精准的表达，配合视觉增强。
> 不是固定段落模版，而是 Agent 在写 **`concepts/`、`syntheses/`、实质性修订 `overview.md`** 时的原则。
> **`sources/`** 以摘要、主张、摘录与回链为主，避免宣传腔与长篇散文。

## 路径约定

- **Wiki 根**：环境变量 **`WIKI_ROOT`**（本 pack 根目录，即含 `CLAUDE.md` 的目录）。下文技能调用均指向 agent 自身 skill 系统中的对应 skill。
- **视觉资源**：与文章同名的子目录下（如 `wiki/<shelf>/syntheses/<article-name>/`），引用时用 `./<article-name>/xxx.svg`
- **演示资源**：`wiki/<shelf>/slides/<topic>/`
- 去 AI 味（中文）：调用 agent 环境中的 **`humanizer-zh`** skill。

## 1. 核心原则

### 1.1 结论先行

开篇 30 秒内给出核心结论，用一句话概括全文主旨。

```
❌ 差：在深入探讨之前，我们需要先了解一些背景知识...
✅ 好：React Fiber 让渲染可中断，解决了大型应用卡顿问题。
```

### 1.2 一图胜千言

复杂概念必须可视化，每个图表只讲一个核心概念，图表后加「读图结论」。

### 1.3 简单、精准、犀利

删除所有冗余词汇，用具体数字替代模糊描述。

```
❌ 差：此外，值得注意的是，这个系统的设计在很大程度上体现了其对于可扩展性的高度重视。
✅ 好：系统支持水平扩展，单集群可处理 100万 QPS。
```

### 1.4 展示概念层级

明确区分核心概念与从属概念，用层级结构展示依赖关系。

## 2. 文章结构模式

### 2.1 技术/算法类

```
1. 问题是什么（为什么需要这个）
2. 核心思想（一句话概括）
3. 逐步拆解（配合图示）
4. 内部实现（数据结构 + 算法 + 代码）
5. 实际应用
6. 常见误区
```

### 2.2 概念/框架类

```
1. 30 秒心智模型
2. 不是什么 vs 是什么（边界澄清）
3. 核心概念逐个解析
4. 概念间关系图
5. 何时使用/何时不用
```

### 2.3 历史/演进类

```
1. 时间线总览
2. 关键人物与转折点
3. 每个阶段的痛点与解决方案
4. 对现在的影响
5. 未来趋势
```

## 3. 视觉增强（写作时必需考虑）

### 3.1 何时需要视觉

| 情况 | 建议 | 示例 |
|------|------|------|
| 流程/时序复杂 | ✅ 用图表 | 算法的多步流程 |
| 概念之间有关系 | ✅ 用图表 | 组件依赖、数据流向 |
| 结构/层级清晰 | ✅ 用图表 | 模块结构 |
| 简单因果/对比 | ❌ 不需要 | "A 导致 B"、表格对比 |

### 3.2 工具选择

| 场景 | Skill | 安装命令 | 输出 |
|------|-------|---------|------|
| 架构图、流程图、时序图 | `fireworks-tech-graph` | `npx skills add https://github.com/yizhiyanhua-ai/fireworks-tech-graph --skill fireworks-tech-graph` | SVG + PNG |
| 用户要求导出演示 | `html-ppt-skill` | `https://skills.sh/lewislulu/html-ppt-skill/html-ppt` | HTML slides |

### 3.3 fireworks-tech-graph 调用规范

**触发词**：`draw diagram`、`generate chart`、`visualize architecture`、`生成图表`

**调用流程**：
1. 分析需要可视化的内容
2. 组织自然语言描述（包含主题、组件、关系）
3. 指定风格
4. 生成 SVG，导出 PNG（1920px）
5. 保存到与文章同名的子目录下（如 `wiki/<shelf>/syntheses/<article-name>/`）
6. 嵌入 wiki：`![alt](./<article-name>/xxx.png)`

**样式选择**：
| 样式 | 适用场景 |
|------|---------|
| Flat Icon | 技术文档、简单架构 |
| Dark Terminal | AI/Agent 系统、终端风格 |
| Blueprint | 工程文档、蓝图风 |
| Notion Clean | 简约文档 |
| Glassmorphism | 现代 UI、渐变效果 |
| Claude Official | 正式报告、温暖风格 |
| OpenAI Official | API 文档、品牌风格 |

### 3.4 html-ppt-skill 调用规范

**触发词**：`export to slides`、`create presentation`、`导出演示`

**调用流程**：
1. 用户请求导出演示
2. 读取 wiki 内容结构
3. 调用 html-ppt-skill 生成 HTML 演示文稿
4. 输出到 `wiki/<shelf>/slides/<topic>/`

### 3.5 依赖安装

Ingest 成稿阶段如需视觉增强，**必须强制检查** agent 环境是否已安装对应 skill。若缺失，**必须询问用户是否安装**，**未安装完成前不得使用对应功能**：

```bash
# 图表生成（解释复杂概念时必需考虑）
npx skills add https://github.com/yizhiyanhua-ai/fireworks-tech-graph --skill fireworks-tech-graph

# 演示导出（按需）
# 见 https://skills.sh/lewislulu/html-ppt-skill/html-ppt
```

> **强制规则**：执行任何依赖外部 skill 的操作前，必须先检查该 skill 是否已安装。若缺失，必须询问用户是否安装，未获得用户明确确认前不得继续。不允许跳过检查。

## 4. 去 AI 味（ingest 阶段必需考虑）

修订或撰写成稿时，**调用** agent 环境中的 **`humanizer-zh`** skill：检测并改掉典型 AI 痕迹（夸大象征、宣传语、肤浅 -ing 分析、模糊归因、破折号堆砌、三段式、套话连接词、否定排比等），并遵循其「删除填充、打破公式、变化节奏、信任读者」等原则。

**边界**：去 AI 味**不等于**编造个人经历；wiki 仍须 **`[[wikilink]]`** 与来源页对齐，不牺牲可追溯性。

### 4.1 去 AI 味速查

| 问题 | 修复 |
|------|------|
| 有"此外"、"值得注意的是"开头 | 直接删掉 |
| 有"不仅...而且..." | 拆成两句或只留重点 |
| 每段都是"XX 是 YY 的 ZZ" | 换成主动句 |
| 结尾都是总结句 | 变化结尾方式 |
| 听起来像名言警句 | 重写 |

### 4.2 humanizer-zh 安装

```bash
npx skills add https://github.com/op7418 --skill humanizer-zh
```

> **强制规则**：调用 `humanizer-zh` 前，**必须强制检查**该 skill 是否已安装。若缺失，**必须询问用户是否安装**，**未安装完成前不得执行去 AI 味操作**。不允许跳过检查。

## 5. 成稿前自检

用 yes/no 快速过一遍即可，**不必写入正文**：

- [ ] 删掉这段话，读者是否仍少知道关键信息？若是，考虑删或改写
- [ ] 是否有「具有重要意义 / 值得一提的是 / 综上所述」等可删拐杖？
- [ ] 主张是否都能回到本 wiki 页或 `sources/`？
- [ ] 是否把不确定处标出来了？
- [ ] 复杂概念是否都有可视化？
- [ ] 图表真的必要吗？（如果不需要就删掉）

## 6. 与 `CLAUDE.md` 操作的关系

- **`ingest`**：写完 source 页后，可对照第 4 节检查 Summary/Claims 是否腔调过重。
- **`query` → syntheses`**、**新建/大改 concept**：写作前读本指南；定稿前建议调用 humanizer-zh 过一遍或至少做第 5 节自检。

**Collect（拉取素材）**：见 **`docs/collect-workflow.md`** 与 **`tools/source_registry.tsv`**（adapter 列表以 TSV / `source_registry_cli.py list` 为准，不在此枚举）。

**本指南与其他操作的关系**：

| 操作 | 本指南职责 |
|------|------------|
| `ingest` | 写完 source 页后检查腔调 |
| `query` → syntheses | 写作前读本指南；定稿前 humanizer-zh |
| 新建/大改 concept | 完整应用本指南（包括视觉增强）|
| 需要可视化 | 调用 fireworks-tech-graph |
| 需要导出演示 | 调用 html-ppt-skill |
