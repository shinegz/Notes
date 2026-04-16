# LLM Wiki — Agent 入口

流程与目录约定以 **`CLAUDE.md`** 为准。

## 每次会话先读

1. `CLAUDE.md`（schema + 工作流）
2. `taxonomy.md`（当前门类）
3. `wiki/index.md` 与 `wiki/overview.md`

## 按任务追加

- **Collect**（URL → `raw/`）：`skills/collect/SKILL.md`，并按 `tools/source_registry.tsv` 的 **`adapter_name`** 进入 `skills/<adapter_name>/`（`-` 表示仅手动）
- **撰写或修订** `concepts/`、`syntheses/`、`overview`：`skills/wiki-writing/SKILL.md` + `skills/humanizer-zh/SKILL.md`（见 `skills/README.md`）

## 根路径（`WIKI_ROOT`）

**本 pack 根目录** = 含 `CLAUDE.md`、`tools/` 的目录（拷贝或克隆后 `cd` 到该目录即可）。

```bash
export WIKI_ROOT="$PWD"
```

若工作区根在上一级、且本 pack 是其子目录 `llm-wiki/`：

```bash
export WIKI_ROOT="$PWD/llm-wiki"
```

## 工具（无 API Key）

```bash
pip install -r requirements.txt
bash tools/check_all.sh "$WIKI_ROOT"
python3 tools/build_graph.py --wiki-root "$WIKI_ROOT"
```

可选：`python3 tools/build_graph.py --wiki-root "$WIKI_ROOT" --open`

## 参考上游（设计理念）

- [llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) — 目录、ingest/query/lint/graph 分工
- [llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) — 来源登记表思路（本 pack 的 `tools/source_registry.tsv` 列名与上游略有差异，见表头）
- [graphify](https://github.com/safishamsi/graphify) — 以图与社区结构理解语料（本库工具为轻量 deterministic 子集）
