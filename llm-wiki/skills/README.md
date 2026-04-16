# skills/

内置 **Agent 能力包**：以 **`SKILL.md`** 为入口，随本 pack 分发；路径仅相对 **`WIKI_ROOT`**（见 **`AGENTS.md`**）。

与本 pack 根下 **`tools/`** 分工：`tools/` 偏 wiki 全域运维（lint、graph 等）；**`skills/<name>/`** 偏「某一类任务」的流程说明 + 可选脚本/CLI。

## 目录一览

| 目录 | 用途 |
|------|------|
| **`collect/`** | Collect 总路由：读 **`tools/source_registry.tsv`**，按 **`adapter_name`** / **`dependency_type`** 选用下列 skill |
| **`baoyu-url-to-markdown/`** | 网页 / X / 知乎等 URL → Markdown（Chrome CDP）；**`dependency_type=bundled`** |
| **`wechat-article-to-markdown/`** | 微信公众号 → Markdown（需 `uv tool install wechat-article-to-markdown`） |
| **`youtube-transcript/`** | YouTube 字幕/逐字稿（`uv run scripts/get_transcript.py`） |
| **`wiki-writing/`** | `concepts/`、`syntheses/`、`overview` 成稿原则 |
| **`humanizer-zh/`** | 中文去 AI 味修订 |

新增来源类型时：更新 **`tools/source_registry.tsv`**（含 **`raw_dir`**、**`adapter_name`**、**`dependency_name`**、**`dependency_type`**），必要时在 **`skills/`** 下增加子目录，并扩展 **`collect/SKILL.md`** 路由表。

## 上游与许可证

| 组件 | 来源 |
|------|------|
| `baoyu-url-to-markdown` | [JimLiu / baoyu-skills](https://github.com/JimLiu/baoyu-skills)（随 [llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) 常见打包方式 vendored） |
| `youtube-transcript` | 自 [llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) `deps` 迁入本 pack；脚本使用 [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) |
| `wechat-article-to-markdown` | [jackwener/wechat-article-to-markdown](https://github.com/jackwener/wechat-article-to-markdown)（MIT；此处仅为 `SKILL.md` 副本 + 说明） |
| `humanizer-zh` | 项目内技能副本，见该目录 `SKILL.md` |
