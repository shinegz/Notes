---
title: "Prompt Engineering From First Principles: The Mechanics They Don't Teach You part-1"
url: "https://dev.to/programmerraja/prompt-engineering-from-first-principles-the-mechanics-they-dont-teach-you-part-1-12nb"
requestedUrl: "https://dev.to/programmerraja/prompt-engineering-from-first-principles-the-mechanics-they-dont-teach-you-part-1-12nb"
author: "@Programmerraja"
coverImage: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fuvj2rgc5ew7ilhpk597t.png"
siteName: "DEV Community"
publishedAt: "2025-12-28T08:42:21Z"
summary: "This is my new series on Prompt Engineering and it's different from everything else out there.  Most... Tagged with promptengineering, llm, openai, gemin."
adapter: "generic"
capturedAt: "2026-05-07T02:34:26.827Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# Prompt Engineering From First Principles: The Mechanics They Don't Teach You part-1

This is my new series on Prompt Engineering and it's different from everything else out there.

Most blogs give you templates: "Try this prompt!" or "Use these 10 techniques!" That's not what we're doing here.

We're going deep: **How do LLMs actually process your prompts? What makes a prompt effective at the mechanical level? Where do LLMs fail and why?**

This series will give you the mental models to engineer prompts yourself, not just copy someone else's examples. Let's dive in.

We going to have 5 parts (so far I think but may be in future we add more )

- **The Foundation - How LLMs Really Work**
- **The Art & Science of Prompting**
- **Prompting techniques and optimization**
- **Prompt Evaluation and Scaling**
- **Tips, Tricks, and Experience**

Let's jump into Part 1.

## Do LLMs Think Like Humans?

Let me ask you something: **Do you think LLMs are intelligent like humans?** Do they have a "brain" that understands your questions and thinks through answers?

**If you answered yes, you're wrong.**

LLMs don't think. They don't understand. They're just **next-token predictors** —sophisticated autocomplete machines that guess what word (or rather, "token") should come next based on patterns they've seen before.

Now, you might be thinking: *"Wait, how can simple next-word prediction answer complex questions, write code, or have conversations?"*

That's a great question, and the answer involves some fascinating engineering. But we're not going to dive too deep into the theoretical computer science here—that would make this series endless. We're focusing on **what you need to know to write better prompts**, nothing more, nothing less.

![Preview](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fned9tmt8d4clwjb2jhrb.png)

If you really intrested in understanding How Machines Learn you can check out [here](https://dev.to/programmerraja/how-machines-learn-understanding-the-core-concepts-of-neural-networks-3a9j) where I have written a detail way

Let's start with the basics.

## How Does an LLM Process Your Prompt?

![Prompt Preview](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F14kn6apq5y0tgfaoaohm.png)

When you type a prompt and hit enter, here's the simplified workflow of what happens inside the model:

### Step 1: English Text → Tokens

Your text doesn't go directly into the model. First, it gets broken down into **tokens**.

A token is roughly a chunk of text—sometimes a whole word, sometimes part of a word, sometimes punctuation.

**Examples:**

- `"Hello world"` → `["Hello", " world"]` (2 tokens)
- `"apple"` → `["apple"]` (1 token)
- `"12345"` → `["123", "45"]` (2 tokens)

Why does this matter? Because:

1. Models have **token limits** (context windows), not word limits
2. The way text is tokenized affects how the model "sees" it
3. Some words the model handles better because they're single tokens, while others are split up

### Step 2: Tokens → Numbers (Embeddings)

The model can't work with text directly—it only understands numbers. Each token gets converted into a long list of numbers called an **embedding** (basically a mathematical representation of that token).

### Step 3: The Transformer Does Its Magic

Your tokens (now numbers) pass through the **Transformer architecture** layers of neural network computations. Here's where the attention mechanism kicks in, letting the model figure out which tokens relate to which.

Example: In the sentence *"The bank of the river was muddy"*, the model's attention mechanism connects `bank` with `river` and `muddy` to understand we're talking about a riverbank, not a financial institution.

Note: Currently we have some other emerging llm architectures like [**Diffusion Models**](https://www.ibm.com/think/topics/diffusion-models), [**State Space Models**](https://huggingface.co/blog/lbourdois/get-on-the-ssm-train), etc.. but for sake of simplicity i cover only **Transformer** based models.

### Step 4: Predict the Next Token (Probabilities)

At the end of all this processing, the model outputs a **probability distribution** over all possible next tokens in its vocabulary (which can be 50,000+ tokens).

It looks something like this:

```
Paris:       0.85  (85% probability)
the:         0.05  (5% probability)
beautiful:   0.03  (3% probability)
London:      0.02  (2% probability)
[thousands of other tokens with tiny probabilities...]
```

The model doesn't "know" Paris is the capital of France. It just calculates that based on the patterns it learned during training, `Paris` has the highest probability of being the next token after *"The capital of France is"*.

### Step 5: Select a Token & Repeat

The model picks a token based on these probabilities (we'll talk about *how* it picks in a moment), adds it to the sequence, and repeats the whole process to generate the next token, then the next, until it decides to stop.

**That's it. That's all an LLM does: predict the next token, over and over, based on probability.**

## But Wait... How Does This Answer My Questions?

Here's where it gets interesting. If LLMs are just probability machines playing "guess the next word," how do they:

- Answer questions correctly?
- Write code that actually works?
- Hold coherent conversations?
- Follow complex instructions?

The answer is **training** specifically, the two major phases that shape model behavior.

### Phase 1: Pre-Training (Learning Patterns from the Internet)

In this phase, the model reads **trillions of tokens** from:

- Websites (Wikipedia, forums, blogs)
- Books
- Code repositories (GitHub)
- Research papers
- Social media

**What it learns:** Statistical patterns. If it sees "The capital of France is Paris" thousands of times, it learns that `Paris` has a high probability of following "The capital of France is".

**What it doesn't learn:** How to answer questions like an assistant. A pre-trained "base model" has knowledge but no manners.

Ask a base model: *"What is the capital of France?"*

It might respond: *"What is the capital of Germany? What is the capital of Spain?"*

Why? Because it's just completing patterns it saw in training data probably quiz lists from forums. It has information, but no concept of "answering questions."

### Phase 2: Post-Training (Teaching It to Be an Assistant)

This is where base models become **ChatGPT**, **Claude**, or other chat assistants. Two key steps:

**1\. Supervised Fine-Tuning (SFT):**

- Humans write thousands of example conversations: questions and good answers
- The model learns: *"Oh, when I see a question, I should provide a helpful answer, not continue the question"*

**2\. Reinforcement Learning from Human Feedback (RLHF):**

- Humans rate different model responses as "good" or "bad"
- The model learns to optimize for helpful, harmless, and honest responses
- This is why models refuse harmful requests or add disclaimers

**The result:** A model that not only predicts the next token, but predicts tokens that *look like helpful assistant responses* because that pattern now has the highest probability in its training.

So when you ask *"What is the capital of France?"*, the model isn't "thinking" about geography. It's predicting that tokens forming a helpful answer have higher probability than tokens that continue the question—because that's what its training reinforced.

**It's all still just next-token prediction. The training just shaped *which* predictions have high probability.**

## Model Configuration: Controlling the Output

Remember that probability distribution we talked about? Here's where you get control. The model gives you probabilities, but **configuration parameters** decide how tokens are actually selected from those probabilities.

### Temperature: The Creativity Dial

**Temperature** controls how "random" the model's choices are.

**Example scenario:** The model predicts:

```
Paris:     85%
beautiful: 3%
London:    2%
```

**Low Temperature (e.g., 0.2):**

- The model becomes more "confident" and almost always picks the top choice
- `Paris` might effectively become 95%+ likely
- **Result:** Deterministic, focused, repetitive outputs
- **Use for:** Code generation, data extraction, factual answers

**High Temperature (e.g., 0.8):**

- The model flattens the probability curve
- `Paris` might drop to 60%, `beautiful` rises to 10%, `London` to 8%
- **Result:** More varied, creative, unpredictable outputs
- **Use for:** Creative writing, brainstorming, multiple perspectives

**Real example:**

Prompt: *"The sky is"*

**Temperature 0.2:** "blue" (almost always) **Temperature 0.8:** "blue" or "cloudy" or "vast" or "filled with stars" (varies)

### Top-P (Nucleus Sampling): Cutting Off the Nonsense

**Top-P** (also called nucleus sampling) sets a probability threshold.

If you set **Top-P = 0.9**, the model only considers tokens that together make up the top 90% of probability, ignoring everything else.

**Why this matters:**

Without Top-P, even with reasonable temperature, the model might occasionally pick a token with 0.001% probability—resulting in complete nonsense.

With Top-P = 0.9, those ultra-low-probability tokens are never even considered. The model stays coherent while still being creative.

**Practical combination:**

- **Temperature 0.7 + Top-P 0.9** = Creative but coherent
- **Temperature 0.2 + Top-P 1.0** = Deterministic and focused

### Top-K: Limiting Choices

**Top-K** simply limits the model to considering only the K most likely tokens.

**Example:** Top-K = 50 means the model only looks at the 50 highest-probability tokens and ignores the rest.

This is a simpler version of Top-P and less commonly used in modern systems.

## Putting It Together

Let's trace through a complete example:

**Your prompt:** *"Explain photosynthesis in simple terms"*

1. **Tokenization:** `["Explain", " photosynthesis", " in", " simple", " terms"]`
2. **Model processing:** Transformer calculates relationships between tokens
3. **Probability distribution for next token:**
```
Photosynthesis:  40%
It:             15%
The:            12%
In:              8%
[...]
```
1. **Configuration applied (Temperature 0.3, Top-P 0.9):**
- Low temperature sharpens: `Photosynthesis` → 65%
- Model picks `Photosynthesis`
1. **Repeat:** Now the sequence is *"Explain photosynthesis in simple terms Photosynthesis"*
	- Calculate probabilities for the next token
		- Pick based on configuration
		- Continue until complete answer is generated

**The model never "understood" photosynthesis. It predicted tokens that statistically form explanations based on patterns from its training data.**

## Now You Have the Mental Model

You now understand the fundamental truth: **LLMs are probability engines, not reasoning machines.** Every response is just a statistical prediction of the next token, shaped by training data and controlled by configuration parameters.

But here's where it gets powerful: **If you understand the mechanism, you can engineer the probabilities.**

Your prompt doesn't just ask a question it shapes the entire probability landscape the model uses to generate its response. Change a few words, reorder your instructions, add an example, and suddenly different tokens become more likely. Different tokens mean different outputs.

In the next part, we're going to explore **The Art & Science of Prompting** how to deliberately craft prompts that steer those probabilities in your favor.

**The foundation is set. Now let's learn to build on it.**

I’ve also set up a [GitHub](https://github.com/programmerraja/PromptEngineering) repository for this series, where I’ll be sharing the code and additional resources. Make sure to check it out and give it a star!

Feel free to share your thoughts, comments, and insights below. Let’s learn and grow together![Sonar](https://dev.to/sonar)Promoted

[![State of Code Developer Survey report](https://media2.dev.to/dynamic/image/width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fucarecdn.com%2F2f2ce9b0-68e0-48a1-bf3e-46c08831a9be%2F)](https://www.sonarsource.com/sem/the-state-of-code/developer-survey-report/?utm_medium=paid&utm_source=dev&utm_campaign=ss-state-of-code-developer-survey26&utm_content=report-devsurvey-banner-x-2&utm_term=ww-all-x&s_category=Paid&s_source=Paid+Social&s_origin=dev&bb=260505)

## State of Code Developer Survey report

Did you know 96% of developers don't fully trust that AI-generated code is functionally correct, yet only 48% always check it before committing? Check out Sonar's new report on the real-world impact of AI on development teams.