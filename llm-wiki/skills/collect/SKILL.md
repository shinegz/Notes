---
name: llm-wiki-collect
description: >
  Collect llm-wiki raw material from URLs or files: read tools/source_registry.tsv, pick adapter_name, open the matching skill under skills/ (baoyu-url-to-markdown, wechat-article-to-markdown, youtube-transcript) and follow it. Use when adding candidates to sessions/, fetching web articles, X/Twitter, Zhihu, WeChat, YouTube, or any Collect step before writing raw/<shelf>/.
---

# llm-wiki Collect（按来源选 skill）

**不要**为已登记来源临时换工具链：按 **`tools/source_registry.tsv`** 的 **`adapter_name`**、**`dependency_type`** 使用 **`skills/<adapter_name>/`**（见下表）。

## 路径

- **`WIKI_ROOT`**：已 `cd` 到本 pack 根（含 `CLAUDE.md`）时为 **`$PWD`**；若当前在父目录且子目录名为 `llm-wiki/`，则为 **`$PWD/llm-wiki`**（目录名可不同，指向同一结构即可）。
- 登记表：**`$WIKI_ROOT/tools/source_registry.tsv`**（改表后 **`python3 tools/source_registry_cli.py validate "$WIKI_ROOT"`**；终端可用 **`match-url` / `match-file`** 对齐行）
- 字段契约（Collect 记录）：**`$WIKI_ROOT/tools/source_record_contract.tsv`**
- 能力包：**`$WIKI_ROOT/skills/<adapter_name>/SKILL.md`**（**`adapter_name`** 为 `-` 时无此步）

## 登记表列（结合本 pack 约定）

| 列 | 含义 |
|----|------|
| **`raw_dir`** | 以 TSV 为准（如 **`raw/articles`**）；落盘时去掉前缀 **`raw/`** 接到 **`raw/<门类>/[<子主题>/]`** 后面。介质/平台**命名含义**见 **`raw/README.md`**，勿在别处维护第二张「来源类型 → 目录」对照表。 |
| **`source_category`** | **`core`**：本地文件/粘贴，无 adapter；**`optional`**：可走 bundled/install_time adapter；**`manual`**：仅人工。 |
| **`match_rule`** | 文件：`file_ext:…`；URL：显式 **`host:…`**；兜底 **`default`** 仅用于 **`web_article`**（须在 host 规则**之后**匹配）。 |
| **`adapter_name` / `dependency_name` / `dependency_type`** | 与 **`skills/`** 目录及安装方式一致：**`bundled`** 已随本 pack；**`install_time`** 见对应 SKILL；**`none`** 无自动抓取。 |

## 路由（不重复粘贴整张表）

- **查全表**（含每条 `source_id`、`adapter_name`、`raw_dir`）：`python3 tools/source_registry_cli.py list`（可加 `--category core|optional|manual`）。
- **查一行**：`python3 tools/source_registry_cli.py get <source_id>`。
- **规则**：**`adapter_name`** 为 **`-`** → 无 skill，按 **`fallback_hint`** 手动落盘；**否则** 与 **`skills/<adapter_name>/`** 目录**同名**（改 TSV 时须保证该目录存在）。
- **流程**：匹配 **`match_rule`**（先具体 **host**，最后 **`default`**）→ 读 **`adapter_name`** → 非 `-` 则打开对应 **`SKILL.md`** → 写入 **`raw/<门类>/[<子主题>/]<raw_dir 去掉 raw/ 前缀>/`**。

## 依赖备忘

- **`baoyu-url-to-markdown`**：`skills/baoyu-url-to-markdown/scripts/` 内首次 **`bun install`**（或 **`npm install`**）；Chrome CDP。详见该 skill。
- **`wechat-article-to-markdown`**：**`install_time`** — `uv tool install wechat-article-to-markdown`（或 pipx）。
- **`youtube-transcript`**：`uv run scripts/get_transcript.py "<URL>"`。

## 与写作 skill 的分工

- **Collect**：本文件 + **`skills/<adapter_name>/`**
- **ingest 成稿**：**`skills/wiki-writing/`** + **`skills/humanizer-zh/`**
