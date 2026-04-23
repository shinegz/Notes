# Wiki 成稿风格指南（Ingest Style Guide）

> llm-wiki 成稿的**风格层**指南：在确定页面类型和结构（见 `ingest-structure-guide.md`）之后，润色表达质量、视觉呈现与可读性。
> **使用顺序**：先读 `ingest-structure-guide.md` 确定"写什么类型、按什么结构"，再读本指南润色"怎么写得好"。

---

## 1. 核心表达原则

### 1.1 结论先行（倒金字塔）

开篇 30 秒内给出核心结论，用一句话概括全文主旨。这是**所有页面类型**的通用要求——每页都必须以 Epitome 开头。

```
❌ 差：在深入探讨之前，我们需要先了解一些背景知识...
✅ 好：React Fiber 让渲染可中断，解决了大型应用卡顿问题。
```

**科学依据**：倒金字塔结构（Inverted Pyramid）来自新闻学，符合读者扫描式阅读习惯。根据 Well-Shaped Words 的推荐，每个段落的第一句也应该是该段最重要的信息。

---

### 1.2 一图胜千言

复杂概念必须可视化，但**每个图表只讲一个核心概念**。图表后必须加「读图结论」。

**何时需要视觉**：

| 情况 | 建议 | 示例 |
|------|------|------|
| 流程/时序复杂 | ✅ 用图表 | 算法的多步流程、Agent 调用链路 |
| 概念之间有关系 | ✅ 用图表 | 组件依赖、数据流向、概念网络 |
| 结构/层级清晰 | ✅ 用图表 | 模块结构、架构分层 |
| 简单因果/对比 | ❌ 不需要 | "A 导致 B"、表格对比即可 |

**何时不需要视觉**：
- 能用一句话说清的因果关系
- 纯数值对比（用表格更高效）
- 读者已熟悉的简单结构

---

### 1.3 简单、精准、犀利

删除所有冗余词汇，用具体数字替代模糊描述。

```
❌ 差：此外，值得注意的是，这个系统的设计在很大程度上体现了其对于可扩展性的高度重视。
✅ 好：系统支持水平扩展，单集群可处理 100万 QPS。
```

**具体做法**：
- 删掉"此外"、"值得注意的是"、"综上所述"等填充词
- 把"不仅...而且..."拆成两句或只留重点
- 把"XX 是 YY 的 ZZ"换成主动句
- 用具体数字：不是"很快"，是"200ms"；不是"很大"，是"1TB"

---

### 1.4 展示概念层级

明确区分核心概念与从属概念，用层级结构展示依赖关系。

在 `concepts/` 页中，用 heading 层级（## / ### / ####）展示概念的从属关系。
在 `syntheses/` 框架综合中，用图表或表格展示概念间的层级和依赖。

---

## 2. 视觉增强规范

### 2.1 工具选择

| 场景 | Skill | 安装命令 | 输出 |
|------|-------|---------|------|
| 架构图、流程图、时序图、概念图 | `fireworks-tech-graph` | `npx skills add https://github.com/yizhiyanhua-ai/fireworks-tech-graph --skill fireworks-tech-graph` | SVG + PNG |
| 用户要求导出演示 | `html-ppt-skill` | 见 https://skills.sh/lewislulu/html-ppt-skill/html-ppt | HTML slides |

### 2.2 `fireworks-tech-graph` 调用规范

**触发词**：`draw diagram`、`generate chart`、`visualize architecture`、`生成图表`

**调用流程**：
1. 分析需要可视化的内容
2. 组织自然语言描述（主题、组件、关系）
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

### 2.3 `html-ppt-skill` 调用规范

**触发词**：`export to slides`、`create presentation`、`导出演示`

**调用流程**：
1. 用户请求导出演示
2. 读取 wiki 内容结构
3. 调用 html-ppt-skill 生成 HTML 演示文稿
4. 输出到 `wiki/<shelf>/slides/<topic>/`

### 2.4 依赖安装

成稿阶段如需视觉增强，**必须强制检查** agent 环境是否已安装对应 skill。若缺失，**必须询问用户是否安装**，**未安装完成前不得使用对应功能**：

```bash
# 图表生成（解释复杂概念时必需考虑）
npx skills add https://github.com/yizhiyanhua-ai/fireworks-tech-graph --skill fireworks-tech-graph

# 演示导出（按需）
# 见 https://skills.sh/lewislulu/html-ppt-skill/html-ppt
```

> **强制规则**：执行任何依赖外部 skill 的操作前，必须先检查该 skill 是否已安装。若缺失，必须询问用户是否安装，未获得用户明确确认前不得继续。不允许跳过检查。

---

## 3. 去 AI 味

修订或撰写成稿时，**调用** agent 环境中的 **`humanizer-zh`** skill：检测并改掉典型 AI 痕迹，并遵循其「删除填充、打破公式、变化节奏、信任读者」等原则。

**边界**：去 AI 味**不等于**编造个人经历；wiki 仍须 **`[[wikilink]]`** 与来源页对齐，不牺牲可追溯性。

### 3.1 去 AI 味速查表

| 问题 | 修复 |
|------|------|
| 有"此外"、"值得注意的是"开头 | 直接删掉 |
| 有"不仅...而且..." | 拆成两句或只留重点 |
| 每段都是"XX 是 YY 的 ZZ" | 换成主动句 |
| 结尾都是总结句 | 变化结尾方式 |
| 听起来像名言警句 | 重写 |

### 3.2 `humanizer-zh` 安装

```bash
npx skills add https://github.com/op7418 --skill humanizer-zh
```

> **强制规则**：调用 `humanizer-zh` 前，**必须强制检查**该 skill 是否已安装。若缺失，**必须询问用户是否安装**，**未安装完成前不得执行去 AI 味操作**。不允许跳过检查。

---

## 4. 成稿前自检

用 yes/no 快速过一遍，**不必写入正文**：

- [ ] 删掉这段话，读者是否仍少知道关键信息？若是，考虑删或改写
- [ ] 是否有「具有重要意义 / 值得一提的是 / 综上所述」等可删拐杖？
- [ ] 主张是否都能回到本 wiki 页或 `sources/`？
- [ ] 是否把不确定处标出来了？
- [ ] 复杂概念是否都有可视化？
- [ ] 图表真的必要吗？（如果不需要就删掉）
- [ ] 页面是否在处理**一个**认知任务？（检查原子化）

---

## 5. 与相关文档的关系

| 操作 | 先读 | 再读 | 最后 |
|------|------|------|------|
| 新建/大改 concept | `ingest-structure-guide.md`（确定结构） | 本指南（润色风格） | 自检清单 |
| 新建/大改 synthesis | `ingest-structure-guide.md`（选体裁） | 本指南（润色风格） | humanizer-zh + 自检 |
| 新建/大改 comparison | `ingest-structure-guide.md` | 本指南 | 自检清单 |
| 写完 source 页 | `CLAUDE.md` Source 格式 | 本指南第 3 节（检查腔调） | — |
| 需要可视化 | 本指南第 2 节 | — | — |
| 去 AI 味 | 本指南第 3 节 | — | — |
