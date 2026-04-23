# tools/

| 脚本 | 作用 |
|------|------|
| **`source_registry.tsv`** | Collect 路由：来源类型、`raw_dir`、`adapter_name`、`dependency_*` |
| **`source_record_contract.tsv`** | Collect → ingest 前「来源记录」建议字段（来自 [llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) 契约思路，按本库列名收紧） |
| **`source_registry_cli.py`** | 登记表 CLI：`validate` / **`match-url`** / **`match-file`** / `list` / `get` / **`deps`** / **`layout`**（含 taxonomy顶层 `raw/<shelf>`、`wiki/<shelf>` 核对） |
| **`validate_source_registry.py`** | 兼容入口，等价于 `source_registry_cli.py validate` |
| **`lint_wiki.py`** | 断链、孤儿启发式、**source 页 `source_file` 存在性**、**frontmatter**（含 `type:` 的页须 **`last_updated`**、禁 **`date:`**；source 另须 title/source_file）、**`thin_key_claims`** 统计；**`--strict-ingest`** 时对仍含「ingest 占位」的 Key claims **失败退出** |
| **`check_all.sh`** | 依次执行 **layout → validate → lint**（本目录为 `llm-wiki` 根时：`bash tools/check_all.sh .`） |
| **`build_graph.py`** | 从 wikilink 生成 `graph/graph.json` + `graph/graph.html` |

```bash
export WIKI_ROOT="$PWD"   # 本目录为 llm-wiki 根时
bash tools/check_all.sh "$WIKI_ROOT"
python3 tools/build_graph.py --wiki-root "$WIKI_ROOT"
# 可选：精读完成后再开 CI 门槛
# python3 tools/lint_wiki.py --strict-ingest "$WIKI_ROOT"
```

```bash
# 终端快速查 URL / 路径对应哪一行登记表（agent 按 adapter_name 在自身 skill 系统中查找）
python3 tools/source_registry_cli.py match-url "https://mp.weixin.qq.com/s/xxx"
python3 tools/source_registry_cli.py match-file "./raw/agent/harness-engineering/pdfs/paper.pdf"
```
