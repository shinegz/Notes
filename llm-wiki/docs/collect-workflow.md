# llm-wiki Collect 工作流

**不要**为已登记来源临时换工具链：按 **`tools/source_registry.tsv`** 的 **`adapter_name`**、**`source_category`** 使用 agent 环境中已安装的对应 skill（见下表）。

## 路径

- **`WIKI_ROOT`**：已 `cd` 到本 pack 根（含 `CLAUDE.md`）时为 **`$PWD`**；若当前在父目录且子目录名为 `llm-wiki/`，则为 **`$PWD/llm-wiki`**（目录名可不同，指向同一结构即可）。
- 登记表：**`$WIKI_ROOT/tools/source_registry.tsv`**（改表后 **`python3 tools/source_registry_cli.py validate "$WIKI_ROOT"`**；终端可用 **`match-url` / `match-file`** 对齐行）
- 字段契约（Collect 记录）：**`$WIKI_ROOT/tools/source_record_contract.tsv`**
- 外部能力：由 agent 在自身 skill 系统中按 **`adapter_name`** 查找匹配 skill

## 登记表列（结合本 pack 约定）

| 列 | 含义 |
|----|------|
| **`raw_dir`** | 以 TSV 为准（如 **`raw/articles`**）；落盘时去掉前缀 **`raw/`** 接到 **`raw/<门类>/[<子主题>/]`** 后面。介质/平台**命名含义**见 **`raw/README.md`**，勿在别处维护第二张「来源类型 → 目录」对照表。 |
| **`source_category`** | **`core`**：本地文件/粘贴，无 adapter；**`optional`**：需 agent 环境中有对应 skill；**`manual`**：仅人工。 |
| **`match_rule`** | 文件：`file_ext:…`；URL：显式 **`host:…`**；兜底 **`default`** 仅用于 **`web_article`**（须在 host 规则**之后**匹配）。 |
| **`adapter_name`** | agent skill 系统的标识符；**`-`** 表示无自动抓取 skill。 |

## 路由

- **查全表**（含每条 `source_id`、`adapter_name`、`raw_dir`）：`python3 tools/source_registry_cli.py list`（可加 `--category core|optional|manual`）。
- **查一行**：`python3 tools/source_registry_cli.py get <source_id>`。
- **规则**：**`adapter_name`** 为 **`-`** → 无 skill，按 **`fallback_hint`** 手动落盘；**否则** agent 在自身 skill 系统中查找匹配 skill。
- **流程**：匹配 **`match_rule`**（先具体 **host**，最后 **`default`**）→ 读 **`adapter_name`** → 非 `-` 则调用对应 skill → 写入 **`raw/<门类>/[<子主题>/]<raw_dir 去掉 raw/ 前缀>/`**。

## 外部 Skill 依赖

| Skill | 用途 | 安装命令 |
|-------|------|---------|
| **`tavily-search`** | Web 搜索预验证 | `npx skills add https://github.com/tavily-ai/skills --skill tavily-search` |
| **`baoyu-url-to-markdown`** | 网页抓取（含 X/Twitter、知乎） | `npx skills add https://github.com/jimliu/baoyu-skills --skill baoyu-url-to-markdown` |
| **`wechat-article-to-markdown`** | 微信文章抓取 | `npx skills add https://github.com/jackwener/wechat-article-to-markdown --skill wechat-article-to-markdown` |
| **`baoyu-youtube-transcript`** | YouTube 字幕提取 | `npx skills add https://github.com/jimliu/baoyu-skills --skill baoyu-youtube-transcript` |

> Agent 在执行 Collect 前，**必须强制检查**环境中是否已安装对应 skill。若缺失，**必须询问用户是否安装**，**未安装完成前不得执行 Collect 操作**。不允许跳过检查。

## 与 Ingest 成稿的分工

- **Collect**：本文件 + agent 环境中的 capture skills
- **ingest 成稿**：**`docs/ingest-writing-guide.md`** + agent 环境中的 **`humanizer-zh`**
