---
title: "Harness engineering for coding agent users"
type: source
tags: [harness-engineering, agent, control-theory]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/martin-fowler-harness-engineering.md
source_url: https://martinfowler.com/articles/harness-engineering.html
---

## Summary

Martin Fowler（Birgitta Böckeler 执笔）在「编码智能体用户」的边界语境里收窄 harness：**Agent = Model + Harness**，但外层 harness 的目标是同时提高一次做对概率，并在到达人类之前尽可能自校正。文章用控制论隐喻组织工具：feedforward vs feedback，以及 computational vs inferential（确定性工具 vs LLM 评判）。进一步把监管目标分成 **可维护性、架构契合、行为正确性** 三类 harness，并讨论 harnessability（绿场可预埋、棕场更难）、以及在 CI 时间轴上如何左移质量信号。

## Key claims

- 外层 harness 需要同时有 **引导（guides）** 与 **传感器（sensors）**；只有反馈会重复踩坑，只有前馈不知道是否生效。
- 计算型传感器（lint、测试、结构规则）应尽可能高频、便宜；推断型（LLM review）更贵更噪，但在合适模型/任务上能提升信任。
- 「 steering loop」：人类通过迭代 harness 把重复问题变成低概率事件；也可以用 agent 帮助生成规则/测试/静态分析。
- 更可信的 AI 生成代码可能需要 **缩小解空间**（更硬边界、更可检查），这与传统「灵活性优先」选型可能冲突。
- 行为类 harness 仍最难：很多人把信心寄托在 AI 生成的测试上，但作者认为这还不够。

## Key quotes

> Ultimately it should reduce the review toil and increase the system quality, all with the added benefit of fewer wasted tokens along the way.

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI 中文]] — 自定义 linter 错误信息即「可消费的反馈」示例
- [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]] — 长程交接工件与验证

## Contradictions

- OpenAI/Stripe 等案例强调速度与吞吐；本文强调 **质量信号分布与人类审查责任**，两者 tone 不同但可在同一仓库里并存（取决于风险阈值）。
