# raw/agent/harness-engineering/

Harness Engineering 子主题的 **immutable 素材**根目录。

子目录按 **`tools/source_registry.tsv`** 的 **`raw_dir`** 组织（见上级 **`raw/README.md`**），常见包括：

- **通用**：`articles/`、`pdfs/`、`notes/`、`refs/`、`transcripts/`
- **平台**：`zhihu/`、`xiaohongshu/`、`tweets/`、`wechat/`（按需创建）

历史上若存在 **`papers/`**，可与 **`pdfs/`** 并存：`pdfs/` 放登记表 **`local_pdf`**；`papers/` 可作论文摘录 md 等人工约定。

Collect 确认后，将快照或摘录落入对应子目录，再对该路径执行 **ingest**（见 **`CLAUDE.md`**）。
