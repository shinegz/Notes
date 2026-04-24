---
title: "Say Hello to Your New QA Teammate: E2E Test AI Agent"
url: "https://dev.to/robin_xuan_nl/5-minutes-of-human-ai-interaction-from-requirements-to-e2e-test-result-1o71"
requestedUrl: "https://dev.to/robin_xuan_nl/5-minutes-of-human-ai-interaction-from-requirements-to-e2e-test-result-1o71"
author: "@"
coverImage: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4n2pfwux4mvklv2x45p3.png"
siteName: "DEV Community"
publishedAt: "2025-11-06T20:51:01Z"
summary: "For some background, see The Past Story about using UI-Tars for AI Testing, which shows practical AI... Tagged with ai, qa, playwright, testing."
adapter: "generic"
capturedAt: "2026-04-24T04:51:50.455Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# Say Hello to Your New QA Teammate: E2E Test AI Agent

*For some background, see [The Past Story about using UI-Tars for AI Testing](https://dev.to/robin_xuan_nl/practical-applications-of-ai-in-test-automation-context-demo-with-ui-tars-llm-midscene-part-1-5dbh), which shows practical AI applications in test automation using UI-Tars and Midscene.js.*

---

> Last updated: 2025-09-11

## What you’ll gain from this blog

1️⃣ **You’ll see how AI can supercharge End-to-End testing — not in theory, but through real-world practical demos.** I’ll walk you through with a real-world demo which solves a few day-to-day use cases, and demonstrate the following **KEY features of this E2E Test AI-Agent**:

- Write tests entirely in natural language — no coding required
- Create tests interactively, like pair-testing with a QA engineer
- AI Agent handles all test data preparation(ex: users, product etc)
- Generated test can be executed later as part of the existing Regression Test suite
- Automatically heal broken element locators and test steps
- Achieve higher stability with less flakiness than manually written scripts
- Identify elements by image prompts
- Run tests at the same speed as Playwright scripts

2️⃣ I will introduce **the architecture** of this E2E Test AI Agent **on top of your own E2E automation framework with [Midscene.js](https://midscenejs.com/)**, to enable you can have your own Agent.

3️⃣ **In conclusion**, I’ll share future steps and upcoming challenges, drawing on insights gathered from a real workshop with a UX designer, a Product Manager, and a QA engineer.

🚀 **At the end, you can build your own E2E Test AI Agent in your organization, and benefit from it as your new teammate, to achieve a Shift-lefted scalable, stable, fast, low-maintenance, and cheap AI-Based E2E test Solution.**

---

## Let's see the Demo first

- 00:00 Interactive generate a test by reading acceptance criteria
- 01:50 Run the generated test from the beginning

---

## Use cases will be demonstrated via the E2E test AI Agent

These are the goals I would like to achieve by applying LLM in E2E automation testing.

- Make E2E test automation writing and maintenance more efficient
	- from **~30 minutes** to write 2/3 similar E2E tests to **0 minutes**
		- from **endless maintenance** to **a few hours** of maintenance per week.
- Shift E2E automation testing left
	- from **QA drafting test cases** to **reusing PM's acceptance criteria & UX's design as test cases**
- Unblock Product managers and UX designers in E2E automation testing
	- from **coding skills required** to **no coding skills required**

---

## Key features with Support Use cases

#### 1\. Principals

![ ](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F15d86nnvv4j93vbiwwkm.png)

Imagine every Quality participant has an E2E Test AI Agent sitting beside you, listening closely as you walk through the acceptance criteria for each feature you want to validate, almost like pair testing with an AI partner.

As a human: you describe your acceptance criteria step by step, feature by feature, aligning them with the UX design, while collaborating with the AI Agent.

As the E2E Test AI Agent: it listens to each request in sequence, generating code along the way, and eventually assembling them into a complete, reusable E2E test script to be executed in the CI repeatedly.

#### 2\. Natural language creates tests interactively

![ ](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fcyew9xqf9yo17eq3y8z6.gif)

The E2E Test AI Agent we developed at CreativeFabrica has knowledge of the application’s context and was able to interpret the contex such as what “Home page” means.

#### 3\. Handles Test data preparation

![ ](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F6hc0hqqw0e8s2crfjf8p.gif)

Unlike typical QA AI agents, the solution we developed integrates with our existing E2E automation framework. As a result, it can go beyond simple browser interactions to perform backend operations, such as preparing test data without relying on the UI.

#### 4\. Generated Less flaky & self-healing test code

![ ](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fmxb1gw9ozgcz2gsr78wk.png)

Rather than simply translating natural language into [Midscene.js](https://midscenejs.com/) calls, we designed our code generation to follow testing best practices. This way, we avoid the flaky behavior you’d often see with plain midscene.js, especially around async waits and lazy loading.

For example, when Human said: "Click the 1st Product", it will generate the following code:

```
await aiWaitFor("1st product is visible")
await Promise.all([
  cleanPage.waitForURL(url => {
    return url.href.includes("/product/autopub-graphic/")
  }),
  aiTap("1st product")
])
```

It leverages AI to identify and click the “1st product,” but the action is wrapped with our best-practice code to ensure the generated test remains stable while it is self-healing.

#### 5\. Locate elements by screenshot

![ ](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F0f2i72iu5wuqcmcce901.gif)

Thanks to the new feature in [Midscene.js](https://midscenejs.com/), our E2E Test AI Agent can now use images as locators! Instead of relying only on traditional selectors, we can simply take a screenshot of the application or even a UI design and use it directly as a locator.

This makes it much easier to test complex systems, especially those built with Canvas or even AI-driven interfaces—where conventional locators often fall short.

#### 6\. Fast test execution & low cost relatively

Thanks to the [Midscene.js](https://midscenejs.com/) caching mechanism, once a test case is generated, most elements used during AI actions are stored. This means we don’t need to call the LLM on every CI execution(save budget), only when elements change or when the planned steps are updated. The basic test execution is Playwright-based, you will enjoy the execution velocity from Playwright.

---

## E2E Test AI Agent Architecture

![ ](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fc8lb9o27qxxvyv1vp6xi.png)

At the heart of our design is a “plug-and-play” philosophy. We treat existing tools like midscene.js functions, Playwright functions, and our in-house E2E automation framework as interchangeable modules that the AI agent can call, almost like snapping together Lego blocks.

But we didn’t stop there. Both midscene.js and our framework are repackaged with best practices baked right into the code generation process, so the generated code is stable and reliable by design.

To boost the agent’s reasoning ability, we also added a dual-layer RAG setup:

- The first layer helps the agent with semantic understanding from the Human's input.
- The second layer supports LLM action planning of each step from the function `aiAction()` exposed by midscene.js

This way, the agent doesn’t just execute blindly, it understands the intent, makes a plan, and then carries it out with solid testing practices behind it.

### Key Component/Layers

**\- Layer 1: From Human Language to Defined Tools**
Translate natural-language acceptance criteria into structured actions and assertions that can be executed, and get different format outputs.

**\- Layer 2: Framework Integration**
Wrap your existing E2E test framework, Midscene.js functions, and Playwright native functions as LLM tools, and keep all LLM Tools can share a single Playwright Browser Context.

**\- Layer 3: AI-Driven Planning**
Midscene.js orchestrates the rest: planning AI steps, interpreting the current screenshot and HTML DOM, and deciding the next best action autonomously.

### The test case metadata

In the current paradigm, a test case created and autonomously executed by an E2E-Test AI Agent contains 3 core metadata layers:

1. Acceptance Criteria (Human Input):
	The intent, expressed directly in natural language by humans.
2. Executable Test Code (Auto-generated):
	Playwright-based code that integrates seamlessly with your existing E2E framework.
3. Element Locator Cache (AI-generated by Midscene.js):
	Cached mappings of HTML elements for fast execution. Only when the cache expires or is missing does the agent call the LLM again to resolve new locators.

With these three, a test case is no longer a static artifact, but a self-adaptive entity that balances human intent, system execution, and AI-assisted resilience.

Here are the exported files from the demo in the video:
![Exported files](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzbearc6xu07ewlktjfcp.png)

## My Conclusions

- AI in E2E automation testing is poised to grow rapidly and inevitably expand into many other areas of testing. This is not just a possibility, but a clear and unstoppable trend.
- With the current state of AI, relying solely on LLMs to handle complex automated testing is still challenging. However, when combined with existing E2E test automation frameworks, it can deliver a much better and more practical experience.
- We will undoubtedly see more AI-powered practical testing tools emerging. But I strongly recommend using Midscene.js when it comes to integration with Playwright. We may soon see a new solution called Vibium (which, as I understand, is still under development and has been proposed by the creator of Selenium).
- For QA engineering, this is more than just the development of a new tool, it represents a transformation in how we approach the entire testing process and quality management.

## Challenges

I set up a workshop together with a QA engineer, a Product manager, and a UX designer to join a 1-hour workshop session to play with this E2E Test AI Agent with LLM Gemini 2.5-Flash. I collected the following challenges:

- Intelligence: Can the system accurately understand the intent of a test step? To achieve this, we need well-defined acceptance criteria, along with clear guidelines on how to write acceptance criteria in a way that can be interpreted by an LLM.
- Accuracy: Can the LLM’s vision correctly determine the coordinates of elements to interact with? When using gemini-2.5-flash, this model can accurately locate around 80% of larger HTML elements, but about 20% have coordinate deviations. For smaller elements, like checkboxes, it often fails to locate them entirely. To address this, we employ different models for different tasks: a smaller model for semantic analysis, a “deep-thinking” model such as DeepSeek R3 for planning, and a vision-optimized model like UI-Tars for precise element localization.
- Step Interactivity, Repeatability, Reversibility, and Stability: Each interaction between the human and the AI should be repeatable, reversible, and stable. We observed that the AI sometimes performs unnecessary actions, which can still generate code. Humans may need to correct previous mistakes, so every step must be atomic to ensure reliability and proper rollback.

## I’d love to hear from you!

Feel free to like, comment, or share this blog, your feedback means a lot!

### Big thanks to these guys:

```
@software{Midscene.js,
  author = {Zhou, Xiao and Yu, Tao},
  title = {Midscene.js: Let AI be your browser operator.},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/web-infra-dev/midscene%7D
}
```[Sonar](https://dev.to/sonar)Promoted

[![State of Code Developer Survey report](https://media2.dev.to/dynamic/image/width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fucarecdn.com%2F2f2ce9b0-68e0-48a1-bf3e-46c08831a9be%2F)](https://www.sonarsource.com/sem/the-state-of-code/developer-survey-report/?utm_medium=paid&utm_source=dev&utm_campaign=ss-state-of-code-developer-survey26&utm_content=report-devsurvey-banner-x-2&utm_term=ww-all-x&s_category=Paid&s_source=Paid+Social&s_origin=dev&bb=260505)

## State of Code Developer Survey report

Did you know 96% of developers don't fully trust that AI-generated code is functionally correct, yet only 48% always check it before committing? Check out Sonar's new report on the real-world impact of AI on development teams.