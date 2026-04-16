---
name: wiki-writing
description: >
  Karpathy-style llm-wiki prose for concepts/, syntheses/, and overview.md—grounded in sources, [[wikilinks]], honest claims, no marketing filler. Use when editing or drafting wiki pages, de-AI passes on Chinese technical notes, ingest summary tone, or principle-first knowledge-base writing. **支持视觉增强**：自动生成图表（fireworks-tech-graph）、动态内容（remotion）、演示导出（html-ppt-skill）。当需要可视化概念、生成架构图/流程图、或导出演示文稿时使用。继承 learning-writer 写作精华。Always pair with skills/humanizer-zh for Chinese de-AI.
---

# Wiki 写作（llm-wiki）

> 升级版 wiki 写作技能：继承 wiki-writing 的文字质量 + 融入 learning-writer 写作精华 + 视觉增强能力。
> 不是固定段落模版，而是 Agent 在写 **`concepts/`、`syntheses/`、实质性修订 `overview.md`** 时的原则。  
> **`sources/`** 以摘要、主张、摘录与回链为主，避免宣传腔与长篇散文。

## 路径约定

- **Wiki 根**：环境变量 **`WIKI_ROOT`**（本 pack 根目录，定义见 **`AGENTS.md`**）。下文 **`skills/`** 指 **`$WIKI_ROOT/skills/`**。
- **视觉资源**：`$WIKI_ROOT/graph/`（存放生成的图表和视频）
- **演示资源**：`$WIKI_ROOT/slides/`（存放导出的 HTML 演示）
- 去 AI 味（中文）：**`skills/humanizer-zh/SKILL.md`**（见 **`skills/README.md`**）。

## 1. 核心原则（from learning-writer）

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

## 3. 视觉增强（核心新增）

### 3.1 何时需要视觉

| 情况 | 建议 | 示例 |
|------|------|------|
| 流程/时序复杂 | ✅ 用图表 | 算法的多步流程 |
| 概念之间有关系 | ✅ 用图表 | 组件依赖、数据流向 |
| 结构/层级清晰 | 可选 | 模块结构 |
| 简单因果/对比 | ❌ 不需要 | "A 导致 B"、表格对比 |

### 3.2 工具选择

| 场景 | 工具 | 输出 |
|------|------|------|
| 架构图、流程图、时序图 | fireworks-tech-graph | SVG + PNG |
| 动态演示、算法动画 | remotion-best-practices | MP4 / iframe |
| 用户要求导出演示 | html-ppt-skill | HTML slides |

### 3.3 fireworks-tech-graph 调用规范

**触发词**：`draw diagram`、`generate chart`、`visualize architecture`、`生成图表`

**调用流程**：
1. 分析需要可视化的内容
2. 组织自然语言描述（包含主题、组件、关系）
3. 指定风格
4. 生成 SVG，导出 PNG（1920px）
5. 保存到 `$WIKI_ROOT/graph/`
6. 嵌入 wiki：`![alt](/graph/xxx.png)`

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

### 3.4 remotion 调用规范

**触发词**：`generate video`、`create animation`、`visualize algorithm`、`生成动画`

**调用流程**：
1. 确定需要动态展示的内容
2. 编写 Remotion composition 代码
3. 渲染 MP4
4. 保存到 `$WIKI_ROOT/graph/`
5. 嵌入 wiki：`![video](/graph/xxx.mp4)` 或 `<video controls>`

### 3.5 html-ppt-skill 调用规范

**触发词**：`export to slides`、`create presentation`、`导出演示`

**调用流程**：
1. 用户请求导出演示
2. 读取 wiki 内容结构
3. 调用 html-ppt-skill 生成 HTML 演示文稿
4. 输出到 `$WIKI_ROOT/slides/<topic>/`

### 3.6 依赖

使用前确保已安装：
```bash
# 图表生成
npx skills add yizhiyanhua-ai/fireworks-tech-graph

# 视频生成
npx skills add remotion-dev/skills --skill remotion-best-practices

# 演示导出
npx skills add lewislulu/html-ppt-skill

# PNG 导出（macOS）
brew install librsvg
```

## 4. 去 AI 味（必读配合）

修订或撰写成稿时，**对照** **`skills/humanizer-zh/SKILL.md`**：检测并改掉典型 AI 痕迹（夸大象征、宣传语、肤浅 -ing 分析、模糊归因、破折号堆砌、三段式、套话连接词、否定排比等），并遵循其「删除填充、打破公式、变化节奏、信任读者」等原则。

**边界**：去 AI 味**不等于**编造个人经历；wiki 仍须 **`[[wikilink]]`** 与来源页对齐，不牺牲可追溯性。

### 4.1 去 AI 味速查

| 问题 | 修复 |
|------|------|
| 有"此外"、"值得注意的是"开头 | 直接删掉 |
| 有"不仅...而且..." | 拆成两句或只留重点 |
| 每段都是"XX 是 YY 的 ZZ" | 换成主动句 |
| 结尾都是总结句 | 变化结尾方式 |
| 听起来像名言警句 | 重写 |

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
- **`query` → syntheses`**、**新建/大改 concept**：写作前读本技能；定稿前建议按 humanizer-zh 过一遍或至少做第 5 节自检。

**Collect（拉取素材）**：见 **`skills/collect/SKILL.md`** 与 **`tools/source_registry.tsv`**（adapter 列表以 TSV / `source_registry_cli.py list` 为准，不在此枚举）。

**本 skill 与其他操作的关系**：

| 操作 | 本 skill 职责 |
|------|--------------|
| `ingest` | 写完 source 页后检查腔调 |
| `query` → syntheses | 写作前读本 skill；定稿前 humanizer-zh |
| 新建/大改 concept | 完整应用本 skill（包括视觉增强）|
| 需要可视化 | 自动调用 fireworks-tech-graph / remotion |
| 需要导出演示 | 自动调用 html-ppt-skill |
