# sessions/

## Collect（收集）流程

1. Agent 根据你的**学习目标**做多轮检索 / 打开链接（不自动批量落盘）。
2. Agent 在本目录新建 `sessions/YYYYMMDD-HHMM-<slug>/candidates.md`，填写候选表。
3. **你确认**行首勾选或回复「采纳1,3,5」等后，Agent 再将 URL/文件写入 `raw/<门类>/…` 并执行 **ingest**。
4. 任何**新建门类**必须先更新提案（发在对话里），你同意后再创建 `raw/<新门类>/` 与 `wiki/<新门类>/` 并更新 `taxonomy.md`。

## 模板

复制 `_template/candidates.md` 开始新会话。
