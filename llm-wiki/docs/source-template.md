# Source 页模板

> Source 页的标准结构。适用于 `wiki/<shelf>/sources/` 下所有页面。
>
> **与 concept-template 的关系**：concept 页是原子化的知识解释页；source 页是素材消化后的摘要页。Source 侧重于忠实还原素材的核心主张，不做额外解释（那是 concept/synthesis 的职责）。

---

## Frontmatter

```yaml
---
title: "Source Title"
type: source
tags: [tag1, tag2]
last_updated: YYYY-MM-DD
source_file: raw/<shelf>/...
source_url: https://...       # 可选，原文链接
# sources: []                 # 如果有参考来源则填入，留空则不写此字段
---
```

| field | 必填 | 说明 |
|-------|------|------|
| `title` | 是 | 文章/论文/报告标题 |
| `type` | 是 | 固定为 `source` |
| `tags` | 是 | 归属话题，可参考 taxonomy |
| `last_updated` | 是 | 格式 `YYYY-MM-DD` |
| `source_file` | 是 | 指向 `raw/` 下的源文件路径 |
| `source_url` | 否 | 原文链接（PDF/论文/网页） |
| `sources` | 否 | 仅当本文引用了其他 source 时填写 |

> **注意**：不要在 frontmatter 中写 `sources: []`（空数组）。有则填，无则省略此字段。

---

## 标准结构

### 1. Summary（必须）

用 2–4 句话概括素材的核心内容。第一句是结论先行，不能是"本文研究了…"。

```
## Summary

[结论先行的一句话] + [为什么重要 + 主要发现/贡献]
```

### 2. Key Claims（论文/技术文章必须有）

素材的核心论点列表。每个 claim 应该是可独立引用的断言。

```
## Key Claims

- **主张 1** — 结论
- **主张 2** — 结论
```

### 3. Key Contributions（报告/综述类可选）

适用于年度报告、Survey、综述文章。与 Key Claims 的区别：Claims 是论点，Contributions 是贡献/亮点。

```
## Key Contributions

- **贡献 1** — 说明
- **贡献 2** — 说明
```

### 4. 数据支撑（表格，可选）

| 类型 | 适用场景 | 示例 |
|------|----------|------|
| Architecture | 论文中的模型/系统结构 | 组件 + 描述表格 |
| Key Milestones | 历史/综述类的时间线 | Year + Event 表格 |
| Report Focus Areas | 年度报告的章节框架 | Area + Description 表格 |
| Benchmarks | 论文的实验结果对比 | Model + Score + Condition 表格 |
| Specifications | 技术报告的参数列表 | Parameter + Value 表格 |

```
## [表格标题]

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| ... | ... | ... |
```

### 5. Key Quotes（可选）

原文中特别重要的引文。每个 quote 必须注明上下文。

```
## Key Quotes

> "引文原文" — 上下文说明
```

### 6. Connections（必须有）

本文与其他 wiki 页的关联。使用 WikiLink，不重复内容。

```
## Connections

- [[shelf/sources/other-source|Source Name]] — 关联说明
- [[shelf/concepts/ConceptName]] — 关联说明
- [[shelf/entities/EntityName]] — 关联说明
```

### 7. Contradictions（仅在有矛盾时添加）

```
## Contradictions

- 与 [[shelf/sources/other-source]] 的矛盾点说明
```

---

## 不同素材类型的 section 选用指南

| 素材类型 | 必须有的 section | 可选的 section |
|----------|-----------------|----------------|
| 论文（Paper） | Summary, Key Claims, Connections | Architecture 表格, Key Quotes, Benchmarks 表格 |
| 博客/教程（Blog/Tutorial） | Summary, Connections | Key Claims（如果技术内容丰富） |
| 报告（Report） | Summary, Key Contributions, Connections | Report Focus Areas 表格, Key Finding（引文） |
| 综述（Survey） | Summary, Key Contributions/Claims, Connections | Taxonomy 表格, Key Quotes |
| Wikipedia/百科 | Abstract, Key Milestones 表格, Connections | — |

---

## 写作原则

1. **结论先行**：Summary 第一句必须是核心结论，不能以"本文研究了…"开头
2. **不重复原始素材**：source 页是摘要，不是全文复述；详细的推导/证明放在 raw 文件中
3. **不越界做解释**：额外解释、与其他概念的关联分析是 concept/synthesis 页的事
4. **WikiLink 不带重复文本**：`[[path|显示文本]]` 的显示文本不能和标题重复
5. **来源可靠**：Key Claims 应该有原文支撑，模糊的"据说"不应作为 claim

---

## 检查清单

写完 source 页后自检：

- [ ] frontmatter 有 `title`、`type`、`tags`、`last_updated`、`source_file`
- [ ] `source_file` 指向的文件确实存在于 `raw/` 下
- [ ] Summary 结论先行，不是"本文研究了…"
- [ ] Connections 中的 WikiLink 格式为 `[[path|name]]`，不是裸 `[[path]]`
- [ ] 没有孤立的变量名标题或碎片化小标题
- [ ] 如果是空 `sources: []` 字段已删除
