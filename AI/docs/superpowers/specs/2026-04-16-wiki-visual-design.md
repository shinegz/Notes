# Wiki Visual Enhancement Design

## 1. 背景

当前 `wiki-writing` skill 专注于文本质量（去 AI 味、来源追溯、wikilink），但缺乏视觉表达能力。对比 `learning-writer` 丰富的图表规范和外部参考项目，需要升级 wiki 的图文能力。

### 目标

- 让 wiki 页面图文并茂
- 复用成熟工具生态，避免重复造轮子
- 保持单一入口，降低协调复杂度

## 2. 决策

### 2.1 视觉类型

| 类型 | 工具 | 输出格式 |
|------|------|---------|
| 图表生成 | fireworks-tech-graph | SVG + PNG |
| 动态内容 | remotion-best-practices | MP4 / iframe |
| 演示导出 | html-ppt-skill | HTML slides |

### 2.2 集成方式

外部工具调用，通过 skill 编排协作，不复制功能代码。

### 2.3 生成时机

写作时同步生成，而非事后批量补充。

### 2.4 结构

扩展现有 `wiki-writing` SKILL.md，保持单一入口：
- 新增「视觉增强」章节
- 融入 learning-writer 写作精华

## 3. 架构

```
┌──────────────────────────────────────────────────────────────────┐
│                       wiki-writing skill                          │
│                      (调度中心，单一入口)                          │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐    │
│  │  写作原则   │  │  视觉增强   │  │  去 AI 味 (humanizer) │    │
│  │  (from lw)  │  │  (新)       │  │                      │    │
│  └─────────────┘  └─────────────┘  └──────────────────────┘    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────────┐ ┌────────────────────┐ ┌──────────────────┐
│ fireworks-tech-   │ │ remotion-best-     │ │ html-ppt-skill   │
│ graph             │ │ practices          │ │                  │
│ (图表生成)        │ │ (视频/动画生成)     │ │ (演示文稿导出)   │
└───────────────────┘ └────────────────────┘ └──────────────────┘
```

## 4. wiki-writing 扩展内容

### 4.1 视觉增强（新增章节）

#### 何时需要视觉

| 情况 | 建议 | 示例 |
|------|------|------|
| 流程/时序复杂 | ✅ 用图表 | 算法的多步流程 |
| 概念之间有关系 | ✅ 用图表 | 组件依赖、数据流向 |
| 结构/层级清晰 | 可选 | 模块结构 |
| 简单因果/对比 | ❌ 不需要 | "A 导致 B"、表格对比 |

#### 工具选择

| 场景 | 工具 | 调用方式 |
|------|------|---------|
| 架构图、流程图、时序图 | fireworks-tech-graph | 自然语言描述 → SVG/PNG |
| 动态演示、算法动画 | remotion-best-practices | React 代码 → MP4 |
| 用户要求导出演示 | html-ppt-skill | wiki 内容 → HTML slides |

#### fireworks-tech-graph 调用规范

**触发词**：`draw diagram`、`generate chart`、`visualize architecture`

**调用流程**：
1. 分析需要可视化的内容
2. 组织自然语言描述（包含主题、组件、关系）
3. 指定风格（Flat Icon / Dark Terminal / Blueprint / Notion Clean / Glassmorphism / Claude Official / OpenAI Official）
4. 生成 SVG，导出 PNG（1920px）
5. 嵌入 wiki：`![alt](/path/to/diagram.png)`

**样式选择**：
- 技术文档 → Flat Icon / Blueprint
- AI/Agent 系统 → Dark Terminal / Glassmorphism
- 正式报告 → Claude Official / OpenAI Official

#### remotion 调用规范

**触发词**：`generate video`、`create animation`、`visualize algorithm`

**调用流程**：
1. 确定需要动态展示的内容
2. 编写 Remotion composition 代码
3. 渲染 MP4
4. 嵌入 wiki：`![video](/path/to/video.mp4)` 或 `<iframe>`

#### html-ppt-skill 调用规范

**触发词**：`export to slides`、`create presentation`、`导出演示`

**调用流程**：
1. 用户请求导出演示
2. 读取 wiki 内容结构
3. 调用 html-ppt-skill 生成 HTML 演示文稿
4. 输出到 `llm-wiki/slides/<topic>/`

### 4.2 写作原则（from learning-writer）

#### 核心原则

1. **结论先行** - 开篇 30 秒内给出核心结论
2. **一图胜千言** - 复杂概念必须可视化，每个图表只讲一个核心概念
3. **简单、精准、犀利** - 删除所有冗余词汇
4. **展示概念层级** - 明确区分核心概念与从属概念

#### 文章结构模式

**技术/算法类**：
```
1. 问题是什么（为什么需要这个）
2. 核心思想（一句话概括）
3. 逐步拆解（配合图示）
4. 内部实现（数据结构 + 算法 + 代码）
5. 实际应用
6. 常见误区
```

**概念/框架类**：
```
1. 30 秒心智模型
2. 不是什么 vs 是什么（边界澄清）
3. 核心概念逐个解析
4. 概念间关系图
5. 何时使用/何时不用
```

#### 去 AI 味速查

| 问题 | 修复 |
|------|------|
| 有"此外"、"值得注意的是"开头 | 直接删掉 |
| 有"不仅...而且..." | 拆成两句或只留重点 |
| 每段都是"XX 是 YY 的 ZZ" | 换成主动句 |
| 结尾都是总结句 | 变化结尾方式 |
| 听起来像名言警句 | 重写 |

## 5. 实施计划

### Phase 1: 下载外部 skill

```bash
npx skills add https://github.com/yizhiyanhua-ai/fireworks-tech-graph
npx skills add https://github.com/remotion-dev/skills --skill remotion-best-practices
npx skills add https://github.com/lewislulu/html-ppt-skill
```

### Phase 2: 扩展 wiki-writing SKILL.md

- 新增「5. 视觉增强」章节
- 新增「6. 写作原则（from learning-writer）」章节
- 整合 humanizer-zh 调用说明

### Phase 3: 测试验证

- 编写测试用例验证图表生成
- 验证与现有 wiki 流程的兼容性

## 6. 文件改动

| 文件 | 操作 |
|------|------|
| `llm-wiki/skills/wiki-writing/SKILL.md` | 扩展 + 新增章节 |

## 7. 依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| fireworks-tech-graph | latest | 图表生成 |
| remotion | latest | 视频生成 |
| html-ppt-skill | latest | 演示导出 |
| librsvg | latest | PNG 导出（macOS: `brew install librsvg`）|
