---
url: https://www.ignorance.ai/p/the-emerging-harness-engineering
title: "The Emerging \"Harness Engineering\" Playbook"
description: "The converging best practices for building with coding agents, from OpenAI to Stripe to OpenClaw."
author: "Charlie Guo"
published: "2026-02-22T23:30:20+08:00"
coverImage: "imgs/img-001-https-substack-post-media-s3-amazonaws-com-publi.jpg"
language: "en"
captured_at: "2026-04-14T06:14:51.496Z"
---

# The Emerging "Harness Engineering" Playbook

### The converging best practices for building with coding agents, from OpenAI to Stripe to OpenClaw.

Earlier this month, Greg Brockman [published a thread](https://x.com/gdb/status/2019566641491963946) about how OpenAI is retooling its engineering teams to make them more effective with agents. The initiative was kicked off because of how much things have changed internally:

> Some great engineers at OpenAI yesterday told me that their job has fundamentally changed since December. Prior to then, they could use Codex for unit tests; now it writes essentially all the code and does a great deal of their operations and debugging. Not everyone has yet made that leap, but it’s usually because of factors besides the capability of the model.

I’ve [previously mapped the progression](https://www.ignorance.ai/p/idle-thoughts-on-programming-and-ai) from Copilot to chatbots to agents to background agents to agent fleets. Each step happened faster than the last. But in the last few months, something qualitatively different has started to emerge - yes, the models have gotten better, but we’re also seeing concrete evidence of what happens when entire teams reorganize around them.

Consider the following data points:

- Peter Steinberger, creator of OpenClaw, [told the Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-creator-of-clawd-i-ship-code) he ships code he doesn’t read. One person, 6,600+ commits in a month, running 5-10 agents simultaneously.
- An OpenAI team [built a million-line internal product](https://openai.com/index/harness-engineering/) over five months with three engineers. Zero lines of hand-written code (by design). An average throughput of 3.5 PRs per engineer per day - and the throughput increased as the team grew.
- Stripe’s internal coding agents, called [Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents), now produce over a thousand merged pull requests per week. A developer posts a task in Slack; the agent writes the code, passes CI, and opens a PR ready for human review, with no interaction in between.

To me, it’s clear we’re past the point of demos and side projects; these are production systems at real scale. And while the specifics differ - Steinberger is a solo practitioner, the OpenAI team is a small squad, Stripe is a 10,000-person company - the patterns they’ve converged on are remarkably similar.[^1]

This post is my attempt to map those patterns. The practices are still emerging and will undoubtedly evolve, but they’re converging fast enough that it’s worth writing down what’s becoming clear.

## The Engineer’s Job Is Splitting In Two

In this moment, I’m seeing the AI space reflect and evolve my own observations on [the shift from a maker’s schedule to a manager’s schedule](https://www.ignorance.ai/p/the-ai-managers-schedule):

> I’m moving away from chatting with AIs and moving towards managing them. You can see the progression of these tools. Today, they’re primarily designed around coding, but it’s a very short leap to augment them for general-purpose knowledge work. Which means those of us at the cutting edge will shift our schedules and workflows from those of makers to those of managers.

The framing still holds, but watching these teams work has sharpened it. The engineer’s job isn’t just becoming a “manager” in a generic sense - it’s splitting into two distinct halves, and you need both.

The first half is building the environment. The OpenAI team put this plainly: the bottleneck was never the agent’s ability to write code, but rather the lack of structure, tools, and feedback mechanisms surrounding it. Their focus shifted from implementation to enablement: when Codex got stuck, they treated it as an environment design problem and asked what was missing for the agent to proceed reliably. And this is, I think, a key piece missing from my earlier writeup.

The second half is managing the work. This is what Steinberger does when he spends extensive time planning with an agent before kicking off execution, or when he acts as the “benevolent dictator” of OpenClaw’s architecture while shipping code he hasn’t read. It’s what Brockman means when he recommends that every team designate an “agents captain” - someone responsible for thinking about how agents fit into the team’s workflow.

These two halves aren’t sequential (at least for now). You don’t build the environment and then manage agents within it. You do both at the same time, and each one informs the other. The agent’s failures tell you what the environment is missing; a better environment lets you manage with less friction.

## Building the Harness

There isn’t an official term for this yet, but I’ve appreciated the name Mitchell Hashimoto (creator of Terraform, Ghostty, and many other software tools) has used: “ [harness engineering](https://mitchellh.com/writing/my-ai-adoption-journey).” A harness is the set of constraints, tools, documentation, and feedback loops that keep an agent productive and on track. Think of it as the difference between dropping a new hire into a company with no onboarding versus one with clear architecture docs, linting rules, a fast CI pipeline, and well-defined module boundaries.

According to Hashimoto, “it is the idea that anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.” And across the examples I’ve been seeing, four practices keep showing up.

### Architecture as Guardrails

The OpenAI team enforced a strict layered architecture in which code within each domain had very rigid dependencies and interfaces. Anything outside of the architecture was disallowed and enforced mechanically:

> Agents are most effective in environments with [strict boundaries and predictable structure⁠](https://bits.logic.inc/p/ai-is-forcing-us-to-write-good-code), so we built the application around a rigid architectural model. Each business domain is divided into a fixed set of layers, with strictly validated dependency directions and a limited set of permissible edges. These constraints are enforced mechanically via custom linters (Codex-generated, of course!) and structural tests.
>
> ...
>
> In a human-first workflow, these rules might feel pedantic or constraining. With agents, they become multipliers: once encoded, they apply everywhere at once.

And as Birgitta Böckeler [noted on Martin Fowler’s site](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html), this suggests a counterintuitive future: increasing trust and reliability in AI-generated code requires constraining the solution space rather than expanding it. We might end up choosing tech stacks and codebase structures not because they’re the most flexible, but because they’re the most harness-friendly.

Stripe takes a different but complementary approach. Their Minions run in isolated, pre-warmed “devboxes” - the same development environments human engineers use, but sandboxed from production and the internet. The agents have access to over 400 internal tools via MCP servers. The key insight: agents need the same context and tooling as human engineers, not a bolted-on, afterthought integration.

### Tools as Both Foundation and Feedback

Brockman’s recommendation to teams is direct: “Maintain a list of tools that your team relies on, and make sure someone takes point on making it agent-accessible (such as via a CLI or MCP server).” If agents can’t access your tools, they can’t help.

Stripe’s implementation is arguably the most mature example of this. Their Minions connect to the 400+ internal tools through a centralized MCP integration called Toolshed. The agents run in the same development environments as human engineers - same tools, same context, same access.

But making tools accessible is only the beginning. The bigger point is that the right tools don’t just expand what an agent can do - they improve the reliability of everything it already does.

In my own experience, having clear instructions for Codex on which linters and test suites to run before committing increases my confidence in every single one of its diffs. Without those tools, I’m flying blind and relying on myself to catch things in a manual review. Similar to teams at OpenAI and Anthropic, I’ve found that prompting agents to use browser automation tools for end-to-end testing dramatically improved thoroughness and accuracy - the agent could catch bugs that weren’t visible from the code alone.

The OpenAI team took this a step further with what might be the cleverest idea in any of these writeups: custom linter error messages that double as remediation instructions. When an agent violates an architectural constraint, the error message doesn’t just flag the violation - it tells the agent how to fix it. The tooling teaches the agent while it works. In Brockman’s words: “Write tests which are quick to run, and create high-quality interfaces between components.”

### Documentation as the System of Record

But how do you turn these processes into repeatable *systems*? Once again, Brockman’s thread includes a specific recommendation: “Create and maintain an AGENTS.md for any project you work on; update the AGENTS.md whenever the agent does something wrong or struggles with a task.” This turns documentation into a feedback loop rather than a static artifact.

For the unfamiliar: AGENTS.md is an emerging open convention - essentially a README for AI agents [^2]. It’s a Markdown file at the root of your repository that coding agents automatically read at the start of every session. It tells the agent what it needs to know about your project: build steps, testing commands, coding conventions, architectural constraints, and common pitfalls.

But what makes AGENTS.md load-bearing infrastructure rather than just another doc that rots is the usage pattern Brockman and Hashimoto describe. You don’t write it once and forget it. You update it every time the agent does something wrong.

> Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

For simple things - the agent running the wrong commands or finding the wrong APIs - that means updating the AGENTS.md. Hashimoto points to [an example from his terminal emulator Ghostty](https://github.com/ghostty-org/ghostty/blob/ca07f8c3f775fe437d46722db80a755c2b6e6399/src/inspector/AGENTS.md), where each line in the file corresponds to a specific past agent failure that’s now prevented.

But the OpenAI team takes this further. Rather than maintaining a single giant instruction file, they built a small AGENTS.md that pointed to deeper sources of truth - design docs, architecture maps, execution plans, quality grades - all versioned and maintained in the repository. A background agent periodically scanned for stale documentation and opened cleanup PRs: documentation *for* agents, *by* agents.

Anthropic’s engineering team, in a post on [effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), found a similar pattern from the opposite direction. Their core problem was that each new agent session started with no memory of what had come before. The solution was structured progress files and feature lists that let a new agent quickly understand the state of work, analogous to a shift handoff between engineers who’ve never met. They even found that using JSON for feature tracking worked better than Markdown, because agents were less likely to edit or overwrite structured data inappropriately.

## Becoming The AI Manager

But of course, the harness is only half the equation. The other half is the day-to-day practice of directing agent work - what I’ve been calling [the AI manager’s schedule](https://www.ignorance.ai/p/the-ai-managers-schedule). Here too, the bleeding-edge practitioners are converging on similar approaches.

### Planning Is the New Coding

Many, many developers at this point emphasize extensive upfront planning when working with AI - so much so that most AI coding tools include a dedicated “plan mode” at this point. Only when they’re satisfied do the engineers kick off execution and move to the next task.

Boris Tane, head of Workers observability at Cloudflare, has [an entire blog post](https://boristane.com/blog/how-i-use-claude-code/) dedicated to this one principle: never let agents write code until you’ve reviewed and approved a written plan. In his words:

> This separation of planning and execution is the single most important thing I do. It prevents wasted effort, keeps me in control of architecture decisions, and produces significantly better results with minimal token usage than jumping straight to code.

Anthropic’s approach to long-running agents formalizes this even further. Their “initializer agent” generates a comprehensive feature list from a high-level prompt - over 200 individual features for a single web app, each with explicit test steps, all initially marked as “failing.” This up-front decomposition is what prevents the agent from trying to one-shot the entire project or prematurely declaring victory.

I’ve [experienced this shift myself](https://www.ignorance.ai/p/the-codex-app-has-upended-my-daily). When the Codex App upended my daily workflow, I stopped spending time implementing and started spending it scoping, directing, and reviewing. The work that matters most now happens before any code is written.

### Say No to Slop

Brockman’s recommendation #5 is blunt:

> Ensure that some human is accountable for any code that gets merged. As a code reviewer, maintain at least the same bar as you would for human-written code, and make sure the author understands what they’re submitting.

This is the “say no to slop” principle, and it runs counter to the temptation of speed. When agents can produce PRs faster than you can review them, the instinct is to lower the bar. Every source I’ve read argues against this.

Steinberger, despite shipping code he doesn’t read line by line, deeply cares about architecture and extensibility. He acts as the architectural gatekeeper for OpenClaw. In his Discord with contributors, he doesn’t talk code - only architecture and big decisions. The Pragmatic Engineer’s Gergely Orosz observed that Steinberger “strikes me as a software architect who keeps the high-level structure of his project in his head.”

I’ve been grappling with this [for a while](https://www.ignorance.ai/p/idle-thoughts-on-programming-and-ai), but as the models get good enough, I’m finding that it’s easier to treat them like experienced subcontractors:

> I like to use the analogy of a woodworker or carpenter. For a junior carpenter (i.e., an “apprentice”), the job might just be about the output - taking designs or ideas and making them into finished pieces. But for someone more senior (a “journeyman” or “craftsman”), their job is often about understanding what the client wants, understanding the realities of what’s possible with the materials, and designing things to fit the brief.
>
> Ultimately, if I’m working with an advanced carpenter to help me design something, I don’t particularly care if they’re the one doing the actual sawing and gluing. I’m working with them for the final product, not the specific mechanical steps.

That’s what Steinberger is doing. He’s the master carpenter. The agents are doing the sawing and gluing. His job is knowing what good looks like and rejecting what doesn’t meet the standard - some might call this ability “taste.”

I call it “ [bullshit detection](https://www.ignorance.ai/p/the-ai-managers-schedule),” and it becomes more critical, not less, as the volume of output increases. You’re reviewing at a higher level of abstraction now. Does the code feel too clever, or too repetitive? Are there patterns here that will cause maintenance headaches in six months? Is the abstraction at the right level?

### Orchestration, Not Just Delegation

The final management skill is parallelization, though to be clear, not everyone gets here (or needs to). Steinberger runs 5-10 agents simultaneously. Stripe engineers kick off multiple Minions from Slack in parallel. I’ve been doing the same with worktrees in the Codex App - three sessions going at once on different features, context-switching between them as a reviewer rather than an implementer [^3].

But there’s an important distinction emerging between two modes of parallel work. What Steinberger and I do is attended parallelization - you’re actively managing several agent sessions, checking in on each, redirecting when needed. What Stripe’s Minions represent is something closer to unattended parallelization - a developer posts a task and walks away. The agent handles everything through CI, and the human only re-enters the loop at the review stage.

These are genuinely different management styles with different tradeoffs. Attended parallelization gives you more control and catches problems earlier, but it’s cognitively demanding. Unattended parallelization scales better but requires much more investment in the environment - the harness has to be good enough that you trust the agent to get from task to PR without supervision. Stripe can do this because they’ve built Toolshed, pre-warmed devboxes, and tight CI integration. Most teams aren’t there yet.

Where your team falls on that spectrum depends on two things: how mature your harness is, and how much you trust the agent with your codebase. As harnesses improve and models get better at sustaining longer tasks without derailing, I expect the balance to shift toward unattended work. But for now, most of us are somewhere in the middle - attended for complex tasks, unattended for well-scoped ones.

## What’s Still Hard

The practices above represent genuine convergence. But there are several open problems where no one has convincing answers yet.

The first is Brockman’s closing question: how do you prevent “functionally-correct but poorly-maintainable code” from creeping into codebases? The Harness Engineering post calls this entropy - agent-generated code accumulates cruft differently than human-written code. They’ve started running periodic “garbage collection” agents to find inconsistencies and violations, but they acknowledge this is still an emerging practice.

The second is verification at scale. Böckeler’s critique of the Harness post was pointed: the write-up lacked verification of functionality and behavior. Anthropic’s long-running agent research found the same gap - agents would mark features as complete without proper end-to-end testing, and absent explicit prompting, they’d fail to recognize that something didn’t work. Even with browser automation, limitations in vision and tool access mean some bugs slip through.[^4]

The third is the retrofit problem. All of these success stories involve either greenfield projects or teams that built their harnesses from scratch. Applying these techniques to a ten-year-old codebase with no architectural constraints, inconsistent testing, and patchy documentation is a much more complex problem. Böckeler compared it to running a static analysis tool on a codebase that’s never had one - you’d drown in alerts. How harness engineering works for brownfield projects is an open question.

And the fourth, and perhaps biggest, is cultural adoption.

Reading through all of these examples, one thing becomes clear: none of this happens by accident. **Someone has to build this stuff**. Someone at each of these organizations had to do the work of figuring out how agents fit into their team’s workflow - creating the harness, defining the processes, and updating based on what works.

The good news is that the investment compounds. Every AGENTS.md update prevents a class of future failures. Every custom linter teaches every future agent session. Every tool you expose via MCP makes every subsequent task faster. The upfront cost is significant, but the returns accelerate.

![](https://substackcdn.com/image/fetch/$s_!_cYj!,%20https://www.ignorance.ai/p/w_424,%20https://www.ignorance.ai/p/c_limit,%20https://www.ignorance.ai/p/f_webp,%20https://www.ignorance.ai/p/q_auto:good,%20https://www.ignorance.ai/p/fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd07968e8-4a9b-4801-86bc-69b7e3e080e5_1456x816.jpeg)

## The Shape of the Thing

Steinberger observed that engineers who love solving algorithmic puzzles struggle to go agent-native, while those who love shipping products adapt quickly [^5]. This tracks with something I’ve seen firsthand - I’ve had to learn to let go of the craft of software engineering as I drift from writing the code with my own hands.

But despite the [bittersweet aspects](https://nolanlawson.com/2026/02/07/we-mourn-our-craft/), I’m fascinated by what’s happening here. This is a genuinely new discipline forming in real-time - it draws from classic challenges in software architecture and team management, while throwing context engineering into the mix. The playbook is still being written, but for the first time, I think the shape of the thing is becoming legible.

---

[^1]: It’s also worth noting that each of these operates at very different scales and risk tolerances. Steinberger is building an experimental open-source project; the Harness team is building an internal tool; Stripe is shipping to production in one of the industry’s most demanding codebases. That they’re arriving at similar conclusions despite these differences makes the signal stronger.

[^2]: The convention emerged from a collaborative effort across multiple AI tool vendors, starting with tool-specific files and converging on a single standard. You can read more at [agents.md](https://agents.md/). Claude Code still uses CLAUDE.md by default, which causes mild ongoing friction in the ecosystem.

[^3]: In practice, I’ve found that I can handle 3-4 active sessions at once. More than that, and I’m the bottleneck, which I imagine I will have to find some way around in the coming months.

[^4]: Anthropic found, for example, that their agents couldn’t see browser-native alert modals with Puppeteer, and features that relied on those modals ended up buggier as a result. The tools themselves introduce their own jagged frontier.

[^5]: He also admits that even he spends a significant chunk of his time on the meta-work of making his agents more effective rather than on the product itself.