# Collect session — <short-title>

- **Goal**: <一句话学习目标>
- **Default shelf**: `<门类/子主题>`（须已在 `taxonomy.md` 登记，或先走门类审批）
- **Created**: YYYY-MM-DD

## 工具路由（Collect 前必读）

路由查 **`source_registry.tsv`**（`match_rule` 列，先 host 精确匹配，后 default 兜底）。

## Candidate sources（待你确认）

| OK | Type | URL | 建议 raw 路径 | Fetch 方法 | 一行理由 |
|----|------|-----|--------------|------------|----------|
| [ ] | arxiv-pdf | `https://arxiv.org/pdf/<id>.pdf` | `pdfs/<slug>.pdf` | `curl -L` | |
| [ ] | web-article | | `articles/<slug>.md` | `baoyu-fetch` | |
| [ ] | github-repo | | `refs/<slug>.md` | `baoyu-fetch` | |

## 你的批复

（在此打勾或聊天回复采纳序号 / 修改 shelf）

## Fetched（确认后由 Agent 填写）

| raw 路径 | 状态 | Fetch 方法 |
|----------|------|------------|
| | | |