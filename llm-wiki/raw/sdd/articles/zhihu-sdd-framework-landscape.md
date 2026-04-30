---
title: "95% 的 Vibe Coding 项目活不过两周——Spec-Driven Development 能拯救它吗？"
url: "https://zhuanlan.zhihu.com/p/2009360235362526486"
requestedUrl: "https://zhuanlan.zhihu.com/p/2009360235362526486"
siteName: "知乎专栏"
summary: "TL;DR：Vibe Coding 在原型阶段效率惊人，但 90-95% 的 AI 编码项目死于&#34;规模化陷阱&#34;——代码能跑但没人敢改 Spec-Driven Development（SDD）是 2025-2026 年最重要的工程化趋势，五大框架（Spec Kit、Ope…"
adapter: "generic"
capturedAt: "2026-04-29T07:28:38.989Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "zh"
---

# 95% 的 Vibe Coding 项目活不过两周——Spec-Driven Development 能拯救它吗？

## TL;DR：

1. Vibe Coding 在原型阶段效率惊人，但 90-95% 的 AI 编码项目死于"规模化陷阱"——代码能跑但没人敢改
2. Spec-Driven Development（SDD）是 2025-2026 年最重要的工程化趋势，五大框架（Spec Kit、OpenSpec、Superpowers、Kiro、Tessl）各有取舍
3. 正确的姿势是"渐进式 Spec"——小项目别折腾，中等项目用 OpenSpec 或 Superpowers，企业级项目才需要 Spec Kit 的完整流水线

---

![](https://picx.zhimg.com/v2-f9f1093ada6f48686da1ee3c7d1daec1_1440w.jpg)

### 一、背景：Vibe Coding 的蜜月期结束了

2025 年 2 月，Andrej Karpathy 发了一条推文，造了一个词叫"Vibe Coding"——大意是"别想了，直接让 AI 写，能跑就行"。这条推文获得了 10 万+转发，整个技术圈为之兴奋。

一年后的数据给所有人泼了冷水。Rand Group 2026 年的调研显示，90-95% 的企业 AI 项目未能从试点进入生产。McKinsey 2025 年底的报告更直接：65% 的企业反馈 AI 生成的代码"在原型阶段表现很好，但无法满足生产环境的可维护性要求"。Gartner 的数据补了一刀——仅 6% 的技术决策者"完全信任" AI Agent 的输出。

问题出在哪？不是 AI 写不好代码，而是 **没人告诉 AI "为什么"要写这段代码** 。Vibe Coding 的本质是"输入模糊意图，输出可执行代码"。当项目复杂度超过一个文件、一个功能的边界时，模糊意图产生的是模糊代码——能跑，但没人知道它为什么这么写，更没人敢改。

这就是 Spec-Driven Development 登场的背景。

### 二、五大 SDD 框架横评：谁在重新定义 AI 编程？

SDD 的核心思想并不新鲜——"先写规范，再写代码"。但在 AI 时代，这个古老原则获得了全新的意义： **规范不再只是给人看的文档，而是给 AI 的执行指令** 。

2025 年下半年到 2026 年初，至少五个主要框架涌现。它们的设计哲学和适用场景差异巨大。

### 2.1. GitHub Spec Kit：官方标准的野心与包袱

Spec Kit 是 GitHub 在 2025 年 8 月发布的官方 SDD 工具包（MIT 许可），发布后迅速获得 50,000+ Stars。

**四阶段流水线：**

1. **Specify** — 描述目标和用户旅程，Agent 起草详细规格文档
2. **Plan** — 声明架构、技术栈和约束，Agent 生成技术方案
3. **Tasks** — Agent 将工作拆解为小粒度、可独立验证的任务单元
4. **Implement** — 逐任务实现并验证

**优势：** GitHub 官方背书，兼容 17+ AI 工具（Copilot、Claude Code、Gemini CLI、Cursor、Windsurf 等），跨平台支持 Unix Shell 和 Windows PowerShell。

**问题：** Martin Fowler 团队的 Birgitta Böckeler 在深度评测中指出，Spec Kit 生成了"过多重复的 Markdown 文件"，审查体验很差——"I'd rather review code than all these markdown files"。更值得关注的是，社区已经出现对其维护活跃度的质疑（GitHub Discussion #1482）。

**适用场景：** 大型团队的新项目启动、需要标准化流程的企业环境。

### 2.2. OpenSpec：轻量级的"Brownfield-First"哲学

OpenSpec 由 Fission-AI 开发，定位完全不同——它专门为 **已有代码库的演进** 而设计。

**核心差异化：** 大多数团队面对的不是从零开始的绿地项目，而是已有数万行代码的"棕地"（Brownfield）。OpenSpec 的 Spec 文件与代码同仓库存储，按能力（capability）组织，上下文不会随聊天会话结束而丢失。

**工作流：** 发起变更 → 创建 artifact（提案、规格、设计、任务）→ 实现任务 → 归档并合并 Spec。

**优势：** 无需 API Key，无需 MCP，安装即用。支持 20+ 工具。轻量灵活，不强制完整流水线。

**问题：** 轻量的代价是缺乏强制约束——对纪律性不足的团队，"可选的规范"等于没有规范。

**适用场景：** 已有代码库的持续演进、快速迭代的中小团队。

### 2.3. Superpowers：Claude Code 生态的全栈工作流引擎

Superpowers 是 Jesse Vincent（Best Practical Solutions 创始人，RT 工单系统作者）为 Claude Code 打造的技能框架。它不只是 Spec 工具，而是一套 **完整的开发工作流引擎** 。

**核心机制：**

- **可组合技能（Composable Skills）：** 技能自动激活，引导开发流程
- **Spec 提取与审查：** 从对话中提取 Spec，分段展示给人审阅确认
- **强制 TDD：** 严格执行 RED-GREEN-REFACTOR 循环——写失败测试 → 看到失败 → 写最小代码 → 看到通过 → 提交
- **双阶段审查：** 每个子任务完成后，先检查 Spec 合规性，再检查代码质量
- **子 Agent 调度：** 自动创建 git worktree，并行分发任务给子 Agent

**独特之处：** Vincent 用 Cialdini 的说服力原则（权威、承诺、互惠）测试了 Skills 在压力场景下是否仍被 Agent 遵守——结论是"Claude went hard"，Skills 确实被当作权威参考而非可选建议。

**问题：** 深度绑定 Claude Code 生态，不支持其他 AI 工具。

**适用场景：** Claude Code 重度用户、追求高代码质量的个人开发者和小团队。

### 2.4. AWS Kiro：IDE 集成的务实路线

Kiro 是 AWS 推出的 AI 编码 IDE，将 SDD 直接嵌入开发环境。

**最轻量的 SDD 实现：** 整个流程只生成 3 个 Markdown 文件（Requirements、Design、Tasks），不像 Spec Kit 那样创建大量文件。

**工作流：** Requirements → Design → Tasks，每一步由 AI 生成、人类审查确认。

**优势：** 集成在 VS Code 体验中，学习成本最低。Spec 即"super-prompt"——规范文件直接作为 AI 的执行上下文。

**问题：** Martin Fowler 团队指出，Kiro 的工作流对小 Bug 修复显得过度设计——"一个 CSS 颜色修改也要走完整的 Requirements → Design → Tasks 流程"。

**适用场景：** AWS 生态用户、偏好 IDE 集成体验的团队。

### 2.5. Tessl：Spec-as-Source 的激进实验

Tessl 是唯一尝试 **Spec-as-Source** 路线的商业化平台——规范即源代码，人类只编辑规范，代码完全由 AI 生成。

**激进在哪：** 传统开发是"写代码，文档随缘"。SDD 是"先写规范，再写代码"。Tessl 更进一步——"只写规范，代码是规范的副产品"。

**Martin Fowler 的类比：** 他将 Tessl 与 2000 年代的 Model-Driven Development（MDD）做了平行对比。MDD 曾承诺"画 UML 就能生成代码"，最终失败于"笨重的抽象层级"。LLM 消除了 MDD 的某些约束，但引入了非确定性风险——Martin Fowler 用一个精准的评价总结："可能兼具两者的缺点：Inflexibility *and* non-determinism。"

**适用场景：** 愿意押注前沿实验的早期采用者。

### 2.6. 框架对比一览

```
重型 + 规范即代码轻型 + 规范即代码轻型 + 规范辅助重型 + 规范驱动TesslKiroSuperpowersOpenSpecSpec Kit轻量灵活重量标准化Spec-First（规范可丢弃）Spec-as-Source（规范即代码）五大 SDD 框架定位图
```

| 维度 | Spec Kit | OpenSpec | Superpowers | Kiro | Tessl |
| --- | --- | --- | --- | --- | --- |
| Spec 级别 | Spec-First | Spec-First | Spec-Anchored | Spec-First | Spec-as-Source |
| 工具兼容 | 17+ | 20+ | 仅 Claude Code | VS Code | 专有平台 |
| 学习成本 | 中 | 低 | 中高 | 低 | 高 |
| 适合项目 | 大型/新建 | 中小型/已有 | 中型/质量优先 | 各规模 | 实验性 |
| 强制约束 | 强 | 弱 | 强（TDD） | 中 | 极强 |
| 社区活跃度 | 高（50K Stars） | 中 | 中高 | 中 | 低（Beta） |
| 核心哲学 | 标准化流水线 | Brownfield 优先 | TDD + Skills | IDE 原生 | 规范即代码 |

### 三、Martin Fowler 的警告：SDD 可能是"Verschlimmbesserung"

在一片叫好声中，Martin Fowler 团队的 Birgitta Böckeler 写了一篇冷静到刺骨的分析。她用了一个德语词 **Verschlimmbesserung** ——意思是"越改越坏"的改进。

### 3.1. 三个层级的真相

Böckeler 将 SDD 分为三个递进层级：

- **Spec-First** ：先写规范再写代码，完成后规范可丢弃。大多数工具（Spec Kit、OpenSpec、Kiro）都在这个层级。
- **Spec-Anchored** ：规范保留用于后续维护和演进。Superpowers 的 Skills 体系接近这个层级。
- **Spec-as-Source** ：规范即源文件，只有人编辑规范。目前只有 Tessl 在尝试。

她的核心发现是： **层级越高，理论收益越大，但实践问题也越多** 。

### 3.2. 审查过载："我宁愿审查代码"

Spec Kit 的四阶段流水线在每个阶段都生成大量 Markdown 文件。Böckeler 的实测体验是——审查这些规范文件比审查代码本身更耗时、更无聊。

这指向一个根本矛盾： **SDD 的目的是减少返工，但如果审查规范的成本超过审查代码的成本，那 SDD 就成了额外负担** 。

### 3.3. AI 可控性悖论

更反直觉的发现是： **规范越详细，AI 并不会越听话** 。Böckeler 发现 AI 仍然会忽视指令或过度执行。用她的话说，"规范的冗长程度和 AI 的遵从程度之间，没有线性关系"。

这解释了为什么 Superpowers 选择了一条不同的路——不是写更多规范，而是用 TDD 机制和双阶段审查来 **强制验证结果** 。与其希望 AI 读懂规范，不如用测试证明 AI 做对了。

### 3.4. 工作流通用性问题

Böckeler 最尖锐的批评是： **现有工具都假设每个任务需要完整的 SDD 流水线，但现实中大多数编码任务不需要** 。

一个 CSS 颜色修改不需要 Requirements → Design → Tasks。一个单函数的 Bug 修复不需要完整的 Spec。缺乏根据任务复杂度自动调整工作流深度的能力，是当前所有 SDD 工具的共同盲点。

### 四、数据说话：SDD 到底有没有用？

### 4.1. 正面数据

来自多个独立来源的数据描绘了一致的趋势：

| 指标 | 改善幅度 | 来源 |
| --- | --- | --- |
| 生产 Bug 数量 | 减少 40-60% | Hoko Blog 2026 |
| 重构时间 | 降低 50% | Hoko Blog 2026 |
| 交付速度 | 提升 30% | Hoko Blog 2026 |
| 编程时间 | 减少 56% | Augment Code 2026 |
| 上市时间 | 缩短 30-40% | Augment Code 2026 |
| 开发成本（2年内） | 降低 20-30% | Cortex 2026 |

### 4.2. 正面数据的局限

这些数据有三个需要警惕的地方：

1. **样本偏差** ：报告数据的多为 SDD 工具厂商或其合作伙伴。独立第三方（如 Martin Fowler 团队）的评价明显更保守。
2. **项目类型偏差** ：大多数成功案例是中大型新建项目。对已有代码库的改造，数据稀缺。
3. **对照组模糊** ：减少 40-60% Bug 是和"完全没有规范的 Vibe Coding"比，还是和"传统软件工程流程"比？结论完全不同。

### 4.3. 关键变量：不是"要不要 SDD"，而是"什么时候要"

SDD 的效果取决于三个变量的交叉：

- **项目规模** ：单文件脚本 → 完全不需要。多模块系统 → 高度需要。
- **团队经验** ：资深工程师自带"脑中的 Spec"→ 轻量级就够。新手 → 需要强制约束。
- **AI 工具成熟度** ：2026 年的 Claude 和 GPT 在 Spec 遵从性上已明显优于 2024 年，但仍不完美。

### 五、我的判断

**SDD 方向正确，但当前工具集体犯了"过度设计"的老毛病。**

这不是新鲜事。软件工程史上每隔十年就会出现一次"用更多流程解决流程不足"的循环——瀑布模型、RUP、CMMI 都走过这条路。SDD 有重蹈覆辙的风险。

**"渐进式 Spec"是我认为正确的姿势：**

![](https://pic2.zhimg.com/v2-721888944b348d273b1d468207bd111f_1440w.jpg)

| 项目阶段/规模 | 推荐策略 | 工具选择 |
| --- | --- | --- |
| 原型验证（< 1000 行） | Vibe Coding，别折腾 | Claude Code / Cursor 裸用 |
| 功能迭代（1000-10000 行） | 轻量 Spec + TDD | OpenSpec 或 Superpowers |
| 系统构建（> 10000 行） | 完整 SDD 流水线 | Spec Kit 或 Kiro |
| 已有代码库改造 | Brownfield-First | OpenSpec |

为什么不推荐所有项目都用 Spec Kit？因为 **过度的流程是创造力的敌人** 。原型阶段的核心任务是"验证想法是否可行"，这时候写一堆规范文档是在用流程杀死速度。当项目验证了可行性、开始进入工程化阶段，再引入 Spec 约束——这才是务实的选择。

**对 Tessl 的 Spec-as-Source 路线，我持谨慎观望态度。** Martin Fowler 对 MDD 的历史类比很有说服力——当年"画 UML 就能生成代码"的承诺没有兑现，今天"写 Spec 就能生成代码"的承诺也需要更多实践验证。但 LLM 确实消除了 MDD 的某些根本性约束（抽象层级的僵化），所以这条路不是完全没戏，只是现在下注为时过早。

**如果只能选一个工具：**

- Claude Code 用户 → **Superpowers** （TDD 强制约束 + Skills 可组合 + 双阶段审查）
- 多工具混用团队 → **OpenSpec** （轻量、兼容性好、Brownfield-First）
- 大型企业标准化 → **Spec Kit** （GitHub 官方背书、17+ 工具兼容）

### 六、对不同人的影响

**技术负责人 / CTO：** SDD 不是"要不要采用"的问题，而是"在哪个阶段引入"的问题。如果团队还在用 Vibe Coding 写原型，别急着推 SDD——等项目进入工程化阶段再说。如果团队已经在为 AI 生成的代码质量发愁，那 SDD 是当前最成熟的解药，但选对工具很关键。

**工程师 / 架构师：** 先试 Superpowers 或 OpenSpec，体验"Spec 如何改变开发节奏"。不要一上来就搭完整流水线。SDD 最大的价值不是流程本身，而是 **强迫你在写代码前想清楚要做什么** ——这其实是所有优秀工程师本来就在做的事，只是现在有了工具支持。

**普通用户（AI 编程爱好者）：** 如果你用 AI 写代码感觉"第一版很惊艳，改着改着就崩了"——这不是 AI 的问题，是你没给 AI 足够的上下文和约束。SDD 的核心理念——"先想清楚做什么，再让 AI 动手"——即使不用任何工具，写一个简单的需求文档就能显著改善 AI 编码质量。

### 参考资料

1. Martin Fowler 团队. *Understanding SDD: Kiro, spec-kit, and Tessl*. martinfowler.com, 2025.
2. Addy Osmani. *How to Write a Good Spec for AI Agents*. addyosmani.com, 2026.
3. Addy Osmani. *Going into 2026: My LLM coding workflow*. addyosmani.com, 2026.
4. Jesse Vincent. *Superpowers*. blog.fsck.com, 2025.
5. GitHub. *Spec Kit — Spec-Driven Development*. [github.com/github/spec-](https://link.zhihu.com/?target=http%3A//github.com/github/spec-kit).
6. Fission-AI. *OpenSpec — A Spec-Driven Workflow for AI Coding Assistants*. [github.com/Fission-AI/O](https://link.zhihu.com/?target=http%3A//github.com/Fission-AI/OpenSpec).
7. Hoko Team. *Spec-Driven Development Frameworks: AIDD 2026*. hoko.team/blog, 2026.
8. Augment Code. *AI Coding Agents for Spec-Driven Development Automation*. augmentcode.com, 2026.
9. Cortex. *The Engineering Leader's Guide to AI Tools for Developers in 2026*. cortex.io, 2026.
10. Rand Group. *Enterprise AI Project Success Rates 2026*. 2026.

编辑于 2026-02-23 20:14・辽宁[阿里云 ×OpenClaw【一键】让 AI 自动帮你干琐事！](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3661015%26si%3D8e85acec-3fe8-4fda-ac7c-b6bc9f29b2f3%26ts%3D1777447711%26zid%3D1629)

[

轻松省下一台Mac Mini！

](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3661015%26si%3D8e85acec-3fe8-4fda-ac7c-b6bc9f29b2f3%26ts%3D1777447711%26zid%3D1629)