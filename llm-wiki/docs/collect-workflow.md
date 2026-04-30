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
| **`baoyu-url-to-markdown`** | 网页抓取（含 X/Twitter、知乎、通用网页） | `npx skills add https://github.com/jimliu/baoyu-skills --skill baoyu-url-to-markdown` |
| **`wechat-article-to-markdown`** | 微信文章抓取 | `npx skills add https://github.com/jackwener/wechat-article-to-markdown --skill wechat-article-to-markdown` |
| **`baoyu-youtube-transcript`** | YouTube 字幕提取 | `npx skills add https://github.com/jimliu/baoyu-skills --skill baoyu-youtube-transcript` |
| **`pdf`** | 学术论文 PDF 处理（提取文本/表格、OCR） | `npx skills add https://github.com/anthropics/skills --skill pdf` |

**下载 PDF**：无需 skill，直接用 `curl` 即可：
```bash
curl -L -o raw/<shelf>/pdfs/<slug>.pdf "https://arxiv.org/pdf/<id>.pdf"
```

### Skill 工具调用后的执行流程

当调用 `Skill` 工具获取 skill 说明后：

1. **读取**返回的 SKILL.md 文档
2. **找到** CLI 命令（通常在 `## CLI Setup` 或 `## Usage` 部分）
3. **手动执行**该命令，而非寻找其他工具
4. 如命令需要参数（URL、output path），从 candidates.md 或用户提供的信息中获取

**错误示例**：
```
Skill tool 返回 SKILL.md → 误以为没有可用工具 → 使用 fetch_content
```

**正确流程**：
```
Skill tool 返回 SKILL.md → 找到 CLI 命令 → 在终端执行该命令
```

### 特殊来源处理规则

| 来源类型 | 处理方式 | 工具 | URL 要求 |
|---------|---------|------|---------|
| 通用网页 | HTML 转 Markdown | `baoyu-url-to-markdown` | 直接使用原始 URL |
| **学术论文（arXiv、IEEE、ACM 等）** | **下载 PDF 原文** | **`curl` 直接下载** | 使用 `/pdf/` 链接；存入 `pdfs/` |
| 视频字幕 | 提取字幕 | `baoyu-youtube-transcript` | YouTube 视频 URL |
| 微信文章 | 专用抓取 | `wechat-article-to-markdown` | 微信文章链接 |
| GitHub README | 下载源码/文档 | `baoyu-url-to-markdown` | GitHub 仓库 URL |
| GitHub 仓库源码 | 结构/文件分析 | `gh api` / `curl` | 公开仓库 URL；指针存 `refs/` |

**特别注意**：
- arXiv 论文使用 `https://arxiv.org/pdf/<id>.pdf` 下载 PDF
- 不要只抓取摘要页（`/abs/<id>`），摘要信息不完整
- Collect 阶段仅下载 PDF，不转换；PDF 处理在 ingest 阶段按需进行
- **GitHub 仓库源码分析**：不下载完整仓库，在 `raw/<shelf>/refs/` 创建指针文件，Ingest 阶段通过 `gh api` 或 `curl` 实时读取关键文件（详见 `CLAUDE.md` Ingest 阶段 "GitHub 资源获取"）

> Agent 在执行 Collect 前，**必须强制检查**环境中是否已安装对应 skill。若缺失，**必须询问用户是否安装**，**未安装完成前不得执行 Collect 操作**。不允许跳过检查。

### GitHub 资源获取

当 Ingest 涉及 GitHub 仓库源码分析时，按以下优先级获取仓库结构和文件内容：

| 优先级 | 工具 | 命令示例 | 适用场景 |
|--------|------|---------|---------|
| 1 | `gh CLI` | `gh api repos/<owner>/<repo>/contents/<path>` | 首选，输出格式友好，支持认证提升 rate limit |
| 2 | `gh CLI` | `gh api repos/<owner>/<repo>/git/trees/<branch>?recursive=1` | 获取完整目录树 |
| 3 | `curl` | `curl -s https://api.github.com/repos/<owner>/<repo>/contents/` | gh 不可用时回退 |

**认证**：`gh auth login` 或设置 `GH_TOKEN` 环境变量。公开仓库无认证也可访问，但 rate limit 较低（60 req/hour），认证后提升至 5000 req/hour。
**存储**：仓库指针放 `raw/<shelf>/refs/<repo-name>-repo.md`，不下载完整源码。详见 `raw/README.md`。

## 与 Ingest 成稿的分工

- **Collect**：本文件 + agent 环境中的 capture skills
- **ingest 成稿**：**`docs/ingest-writing-guide.md`** + agent 环境中的 **`humanizer-zh`**
