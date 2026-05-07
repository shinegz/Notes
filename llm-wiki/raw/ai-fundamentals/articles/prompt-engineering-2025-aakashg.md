---
title: "Prompt Engineering in 2025: The Latest Best Practices"
url: "https://www.news.aakashg.com/p/prompt-engineering"
requestedUrl: "https://www.news.aakashg.com/p/prompt-engineering"
author: "Aakash Gupta"
coverImage: "https://substack-post-media.s3.amazonaws.com/public/images/3da10f37-9143-4c08-b17f-7e813449a6c7_1200x800.png"
publishedAt: "2025-07-10T07:12:17+08:00"
summary: "Research-backed prompt engineering techniques from $50M ARR AI companies. Latest 2025 frameworks, templates & strategies for product teams."
adapter: "generic"
capturedAt: "2026-05-06T11:20:12.078Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# Prompt Engineering in 2025: The Latest Best Practices

### You've seen a million guides on prompts, here's the guide you actually need to build great products right NOW.

###### This article was updated on April 19, 2026#

##### Updated for GPT-5

Prompt engineering seems so “old news.” By now, we’ve all seen a million [prompting guides.](https://x.com/heyrobinai/status/1939651116935123429)

Some tell you to use LLMs to improve the prompt. Others tell you that’s over-engineering.

![](https://substack-post-media.s3.amazonaws.com/public/images/6aca65ed-a322-454c-80cb-539101925e0b_1050x1412.png)

There’s a lot of noise about prompts, so it’s hard to find signal.

Meanwhile, when you talk to AI for your own tasks, it often feels like **you barely even need to engineer your prompts**.

Sure, you can add “act as,” give a goal, use “###” a lot… but it leads to a few percentage points improvement.

*For most use cases, it feels like it doesn’t even matter!*

---

### Back with Miqdad Jaffer

*To explore prompts further, I’m [back](https://www.news.aakashg.com/p/ai-product-strategy) [with](https://www.news.aakashg.com/p/rag-vs-fine-tuning-vs-prompt-engineering) Director of PM at OpenAI Miqdad Jaffer.*

![](https://substack-post-media.s3.amazonaws.com/public/images/80917af9-195f-4f4f-a6af-92f71c5d6268_1536x864.jpeg)

*I took Miqdad’s AI PM Certification course and it’s excellent. The next cohort starts July 13th. Here’s a special $500 discount for my community:*

---

### It turns out, for products, prompt engineering is everything

But as I have learned studying the best AI products, there’s a *big difference* between personal use and products.

The best AI companies **are obsessed with prompt engineering**.

Take two of the recent CEOs I’ve talked with, [Bolt](https://www.youtube.com/watch?v=FE20SlPGSMw&t=3630s) and [Cluely](https://www.youtube.com/watch?v=CoRJEXzMiMA&t=1731s). For both of them, the system prompt plays a huge role.

This is the [system prompt](https://gist.github.com/cablej/ccfe7fe097d8bbb05519bacfeb910038) for [Cluely](https://app.cluely.com/login):

![](https://substack-post-media.s3.amazonaws.com/public/images/0e9ca35f-9f8d-42d5-bf33-9197fcc1e7a5_1366x714.png)

It’s a longer prompt but we’re focusing on the beginning.

There’s a lot of interesting things to notice here:

1. The use of brackets, like code
2. Never and always lists
3. Display instructions
4. If/then edge cases

This prompt, plus Cluely’s liquid glass UX, is doing a lot of the heavy lifting behind reaching $6M ARR in just 2 months.

This is the [system prompt](https://github.com/stackblitz/bolt.new/blob/main/app/lib/.server/llm/prompts.ts) for [Bolt](https://bolt.new/):

![](https://substack-post-media.s3.amazonaws.com/public/images/f43fec3a-e7ef-4f59-92e0-7fa5ea47f493_1368x1596.png)

There’s a lot of repeated patterns from Cluely, like code formatting and long lists of what to do with all caps.

There’s also some Bolt specific stuff like extremely detailed handling of errors they likely faced in the past testing the product.

Aman Khan (Director of AI PM at Arize) went so far as [to say](https://youtu.be/Ej4pBDaHspk?si=YAvHO6EgCBu_BLef&t=5555) that **this is one of the keys to Bolt’s success**. They likely wouldn’t have achieved **$50M ARR in 5 months** without such a powerful prompt.

The point being: **great prompt engineering can be the difference between AI product success and failure**.

---

### Prompt Engineering is a Key Part of Context Engineering

People will say: “ *the new hotness is context engineering*!” And they’re right: it is!

![](https://substack-post-media.s3.amazonaws.com/public/images/423f7be9-fd4d-4314-afb8-0a1797fcd156_1302x1362.png)

I went in-depth into [context engineering](https://www.news.aakashg.com/p/rag-vs-fine-tuning-vs-prompt-engineering) last week. One of the key takeaways? P **rompt engineering is almost always a part of the picture.**

And in many cases, it can do 85% of the heavy lifting.

---

### Key PM Skill

So - welcome to 2025, **where every PM needs to be good at prompt engineering**.

It’s **not something you can just outsource** to engineering. You want to be an *active contributor* to the process. *There’s at least 4 reasons*.

![](https://substack-post-media.s3.amazonaws.com/public/images/4871cae5-d024-4d0c-a951-2f923a732fe1_3600x4500.png)

1. PMs understand user intent better than anyone
2. When you can modify prompts yourself rather than waiting for engineering cycles, you can iterate faster
3. Prompt engineering is product strategy in disguise **\-** every instruction you write into a system prompt is a product decision
4. You'll spot opportunities others miss **\-** you'll recognize when a user complaint isn't actually a model limitation, it's a prompt engineering opportunity

In fact, when I shipped the AI e-mail writer at Apollo.io, I was *regularly* working with the team to iterate on the prompts. I learned it’s not just **necessary** - it’s **exciting**.

The best AI PMs are using the AI wave to get more into the technical implementation: and **I encourage you to as well**! It’s an opportunity to get closer to the “bare metal.”

*So, for all these reasons, I figured the PMs of the world needed an **authoritative** guide to prompt engineering.*

---

## Today’s Deep Dive

*We’ve put together the most up-to-date and practical guide on prompt engineering out there:*

1. **Do You Really Need Prompt Engineering?**
2. **The Hidden Economics of Prompt Engineering**
3. **What the Research Says About Good Prompts**
4. **The 6-Layer Bottom-Line Framework**
5. **Step-by-step: Improving Your Prompts as a PM**
6. **The 201+301 Advanced Techniques Nobody Talks About**
7. **The Ultimate Prompt Template 2.0**
8. **The 3 Most Common Mistakes**

*It’s the wisdom we’ve collected shipping AI at places like OpenAI, Shopify, & Google.*

---

## 1\. Do You Really Need Prompt Engineering?

Before we go any further, do you really need prompt engineering?

It depends on *the state of your current prompt* and *where you are in productionizing it*.

Here’s a **simple playbook** to figure out where you are and where you need to go:

*Now that you know whether prompt engineering is worth your time, let's dive into how the best teams actually do it.*

---

## 2\. The Hidden Economics of Prompt Engineering

We want to emphasize to you how important this is by first saying: ***it’s not just abut revenue***.

A great prompt can 100x revenue you to a Cluely/Bolt state if you do it right. But prompt engineering also can reduce costs.

### The Real Cost Equation

![](https://substack-post-media.s3.amazonaws.com/public/images/90440199-24b1-4101-870c-936c3a9e72b7_3600x4500.png)

Total AI Cost = (Input Tokens \* Price Per Input Token) + (Output Tokens × Price per Output Token) × Number of Calls

Seems simple. But watch what happens with different prompt strategies:

**Detailed Approach (eg Bolt)**:

- Prompt: 2,500 tokens (detailed instructions)
- Output: 1500 tokens
- **Cost per call:** $0.03 *(at $0.003 per 1k input + $0.015 per 1k output for Claude Sonnet 4)*
- Daily volume: 100,000 calls
- **Daily cost: $3,000**

**Simpler Approach (eg Cluely)**:

- Prompt: 212 tokens (structured + few-shot)
- Output: 400 tokens (constrained format)
- **Cost per call:** $0.00706 *(at $0.005 per 1k input + $0.015 per 1k output for GPT-4o)*
- Daily volume: 100,000 calls
- **Daily cost: $706**

That's a 76% cost reduction.

Shorter, structured prompts also:

1. Have less variance in outputs
2. Come out faster with less latency

So there’s a lot to be said about prompt engineering on the cost side.

### Short vs Long: How to Decide

Shorter prompts and outputs have their benefits in terms of cost. But sometimes that 88% increase in cost is well worth it!

You have to weigh the performance vs the cost. A very common approach used by the best AI teams these days is the “hill climb up quality first” and then “down climb cost second”:

![](https://substack-post-media.s3.amazonaws.com/public/images/9fd53d3e-2bc7-4d59-86af-dbb1cc7623a3_3600x4500.png)

Along the way, it’s a delicate balancing act of model performance against evals, error analysis, and context engineering (via prompt engineering, RAG, and fine-tuning).

*We’ll walk you through, step-by-step, how to in section 4.*

---

## 3\. What the Research Says About Good Prompts

The cool thing about prompting is that, now that that we have actual research studies on what makes for a good prompt.

We don’t need to listen to random influencers. We can learn from **professional AI researchers**.

Here’s what the best research in July 2025 shows:

## Keep reading with a 7-day free trial

Subscribe to Product Growth to keep reading this post and get 7 days of free access to the full post archives.