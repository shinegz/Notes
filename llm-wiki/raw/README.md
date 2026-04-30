# raw/

> ⚠️ **宪法铁律**：本目录是**原始素材库**，只存储未经过任何加工的原始内容。
> - **原始性**：必须完整保存原始资料，不得摘要、缩写或改写
> - **Immutable**：素材只增不改，发现错误可另存勘误篇，不覆盖原文件
> - **工具链**：`articles/` 必须用 `baoyu-url-to-markdown` 完整抓取网页原文

素材**只增不改**（发现错误可另存勘误篇，不覆盖原文件）。

## 单一事实来源

**每条 `source_id` 对应哪一段 `raw_dir`（如 `raw/zhihu`）以 `tools/source_registry.tsv` 为准。**本文件只说明 **命名含义** 与 **为何分桶**，避免与 TSV 逐行重复；Agent 路由以 **`docs/collect-workflow.md`** + **`list` / `get` CLI** 为准。

## `raw_dir` 怎么读

TSV 里 **`raw_dir`** 形如 **`raw/pdfs`**：落盘时在 **`raw/<shelf>/`** 或 **`raw/<shelf>/<子主题>/`** 下接 **去掉前缀 `raw/`** 的一段（例：`pdfs/`）。

分桶采用 **「介质 / 平台」粗分**（网页与社媒分开、PDF 与网页稿分开、视频转写单独一桶），便于检索与权限直觉；**不在 `raw/` 层做论文章节级细分**。

## 介质与平台名（与 TSV 中 `raw_dir` 后缀一致）

### 通用介质

| 目录后缀 | 含义 |
|----------|------|
| **`articles/`** | 通用网页、博客、文档站等快照 |
| **`pdfs/`** | 原始 PDF |
| **`notes/`** | 自有笔记、本地 md/txt/html、无平台 URL 的剪贴 |
| **`refs/`** | 链接/书目占位、大文件指针、**GitHub 源码指针** |
| **`transcripts/`** | 视频字幕/逐字稿（与 `articles/` 分离） |

### 平台桶

| 目录后缀 | 含义 |
|----------|------|
| **`zhihu/`** | 知乎 |
| **`xiaohongshu/`** | 小红书（常手动） |
| **`tweets/`** | X / Twitter |
| **`wechat/`** | 微信公众号 |

### 可选：`papers/`（非登记表必填）

若你希望 **「已摘录成 md 的论文正文」** 与 **`pdfs/` 里原始 PDF** 分开，可继续使用或新建 **`papers/`**，由人工约定；**`local_pdf` 仍以 `pdfs/`为准**。

## 与 taxonomy 的关系

- **新建 / 改名 / 删除门类**（`raw/<新 shelf>/`）必须经 **`taxonomy.md`** 审批。
- 子主题下（如 `raw/agent/harness-engineering/`）：至少可含上表中出现过的子目录；**首次**从某平台 Collect 时再创建对应文件夹即可。

## 示例

```text
raw/agent/harness-engineering/
  articles/
  pdfs/
  notes/
  refs/          # GitHub 仓库指针、大文件引用
  transcripts/   # 有 YouTube 再建
  zhihu/
  xiaohongshu/
  tweets/
  wechat/

### `refs/` 中 GitHub 源码指针的格式

用于 Ingest 阶段进行源码分析，不下载完整仓库：

```markdown
# owner/repo 源码指针

- 仓库地址：https://github.com/owner/repo
- 核心目录与文件（待 ingest 阶段通过 gh api / curl 确认并补充）
  - `README.md` — 项目介绍
  - `src/` — 核心源码目录
  - `docs/` — 文档
```
```

门类名与 **`taxonomy.md`** 一致。
