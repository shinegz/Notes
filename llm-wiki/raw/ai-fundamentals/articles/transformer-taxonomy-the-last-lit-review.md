---
url: https://kipp.ly/transformer-taxonomy/
title: "Transformer Taxonomy (the last lit review)"
description: "This document is my running literature review for people trying to catch up on AI."
author: "kipply"
published: "2023-03-30T08:00:00+08:00"
coverImage: "https://substackcdn.com/image/fetch/$s_!q695!,f_auto,q_auto:best,fl_progressive:steep/https%3A%2F%2Fkipply.substack.com%2Ftwitter%2Fsubscribe-card.jpg%3Fv%3D-769841609%26version%3D9"
language: "en"
captured_at: "2026-04-19T06:45:28.879Z"
---

# Transformer Taxonomy (the last lit review)

This document is my running literature review for people trying to catch up on AI. It covers 22 models, 11 architectural changes, 7 post-pre-training techniques and 3 training techniques (and 5 things that are none of the above). Everything is very loosely in order of importance and somewhat uniqueness. All papers will link to the actual PDF and not the ArXiv page and the selection is mostly curated based on things I know about. Systems/performance and alignment are excluded for this one because they’re my favourite and I’d want to do it more justice. Alignment research is really important, I hope to do it justice some day! Also probably not all the papers in the model list are worth reading.

## 1\. Models

If a property is unspecified it’s either undisclosed or follows approximately the standard GPT recipe.

**GPT-3**

\[[paper](https://arxiv.org/pdf/2005.14165.pdf)\] — **175B params, 96 layers, 12288 embd dim, 96 heads — OpenAI May 2020**

This was a seminal paper for large language models, following the [GPT-2 paper](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) (2018) and the [scaling laws paper](https://arxiv.org/pdf/2001.08361.pdf). It was trained on a 300B token dataset consisting mostly of filtered Common Crawl, along with some books, webtext and Wikipedia. BPE tokenizer (same from GPT-2). 2048 context length. Alternates dense and sparse attention layers. Warms up to 0.6 × 10^−4 learning rate in the first 375M toks, cosine decayed to 10% after 260B toks. Batch size ramp from 32k toks to 3.2M toks over the first 12B tokens. 4x MLP projection ratio as done in the [2017 transformer paper](https://arxiv.org/pdf/1706.03762.pdf). 50k vocab size. Many of these characteristics (e.g. embd dim = 128 \* layers, 4x MLP projection ratio, and LR and batch size ramp) form a standard recipe that has been reused by later models.

> there’s a probably-typo in Table 2.1 that documents the hyperparameters, where GPT-3 13B is labelled as having an embedding dimension of 5140 which should probably be 5120

**GPT-4**

\[[technical report](https://arxiv.org/pdf/2303.08774.pdf)\] — **Released March 2023, finished pre-training August 2022**

Man, feels awkward to write a pathetic summary of something this big, but here goes: GPT-4 is a model available through OpenAI of unknown architecture (other than that it’s GPT-like, though they only technically specify transformer-like). The technical report contains mostly evals (which performed well of course), as well as the results of their continued scaling which are accurately extrapolated from smaller models. The report also documents safety mitigation and has a demo of their multi-modal capabilities of GPT-4 which seem trained in à la Flamingo. It also has the best Acknowledgements section of all time.

**Gopher**

\[[paper](https://arxiv.org/pdf/2112.11446.pdf)\] — *280B params, 260B non-embedding params, 80 layers, 16384 embd dim, 128 heads — DeepMind Dec 2021*

DeepMind’s first large language model release in 2021. It uses an RMSNorm instead of a LayerNorm, uses a relative positional encoding scheme from Transformer-XL instead of an absolute positional encoding, which is why there are so many embedding parameters. Tokenizes with SentencePiece, vocab size 32k. Trained on 300B tokens, with half being from MassiveText which was collected for Gopher, along with books, Common Crawl, Wikipedia, news and Github. Note that Gopher was actually trained end of 2020 and released a year later.

**AlphaCode**

\[[paper](https://arxiv.org/pdf/2203.07814.pdf)\] *— 41B, 8 encoder layers, 56 decoder layers, 6144 embd dim — DeepMind Feb 2022*

A model trained on 715GB(967B tokens) of code to do competitive programming. The only model on this list with an encoder-decoder architecture, it treated contest programming as a translation task (problem statement → solution) to gain bidirectionality. It uses 1536 tokens in the encoder and 768 tokens in the decoder. Uses multi-query attention, and generates thousands of samples at inference time and then selects a subset of solutions to submit.

**RETRO**

\[[paper](https://arxiv.org/pdf/2112.04426.pdf)\] — *7B parameters — DeepMind Feb 2022*

Retrieval is the general technique if giving a model a database to look up while doing inference. RETRO was the inaugural retrieval paper for transformers, using a 2T token database. It embeds the token-database in chunks using a pretrained BERT-style model and then performs chunked cross-attention to nearest neighbors in the database during training and inference

**GPT-3.5**

\[[docs](https://beta.openai.com/docs/model-index-for-researchers)\] — ***architecture unknown — OpenAI Mar 2022*** OpenAI delineates three models as GPT-3.5, specifically anything in the `davinci-002` or `davinci-003` family. `code-davinci-002` is the base model, `text-davinci-002` is a version with FeedME non-RL instruction tuning, and `text-davinci-003` is an InstructGPT with RLHF. There is an InstructGPT paper that trains an RLHF model and does not mention FeedME, and though `text-davinci-002` is an InstructGPT model it does not use RLHF. The `davinci` model on the OpenAI API is noted to be the 175B model in the 2020 paper, but it’s never confirmed whether `davinci-002` is the same size.

**Chinchilla**

\[[paper](https://arxiv.org/pdf/2203.15556.pdf)\] — *70B params, 80 layers, 8192 embd dim, 64 heads — DeepMind Mar 2022*

With the paper titled "Training Compute-Optimal Large Language Models”, new and improved scaling laws were introduced. Chinchilla is trained with 1.5T tokens (similar dataset as Gopher) and same amount of compute as Gopher, yet outperforms it. Results in scaling laws that have parameters and tokens linearly increase at a 20:1 token to parameter ratio. Learning rate adjusts with a cosine schedule. [Megatron Turing NLG](https://arxiv.org/pdf/2201.11990.pdf) and [Jurassic J-1 Jumbo](https://uploads-ssl.webflow.com/60fd4503684b466578c0d307/61138924626a6981ee09caf6_jurassic_tech_paper.pdf) are two other large models that aren’t documented here as they are not Chinchilla optimal and aren’t uniquely significant.

**Flamingo**

\[[paper](https://arxiv.org/pdf/2204.14198.pdf)\] *— 80B params — DeepMind Apr 2022*

Flamingo is a multi-modal (text and image) model. It only generates text, and image inputs are run through a vision encoder (435M params), and cross-attention is used to attend to those outputs. It also uses a resampler (194M params) after the vision encoder to produce a fixed (small) number of visual tokens no matter the number of input features. They build on frozen Chinchilla models, the 80B params come from the cross-attention layers added to the 70B Chinchilla model. [PaLI](https://arxiv.org/pdf/2209.06794.pdf) is a Google model that follows up on image/language multimodal.

**Gato**

\[[paper](https://arxiv.org/pdf/2205.06175.pdf)\] *— 1.18B params — May 2022*

Gato is a generalist agent, sort of a follow up to Flamingo with more modalities. It uses images and text, as well as button-press data formatted into tokens, as well as encodings of continuous data from robotics propioception, trying to use as little data as possible for additional tasks. The tasks include robotics stacking tests, image captioning, and Atari.

**Anthropic LM**

\[[paper](https://arxiv.org/pdf/2112.00861.pdf)\] *— 52B params, 64 layers, 8192 embd dim — Anthropic Dec 2021*

Trained on 400B tokens, though in a [later, post-Chinchilla paper](https://arxiv.org/pdf/2207.05221.pdf), Anthropic used a model with the same architecture trained for 850B tokens. And in yet another later paper on [moral self-correction](https://arxiv.org/pdf/2302.07459.pdf), a 175B with no other specified properties is used.

**PaLM**

\[[paper](https://arxiv.org/pdf/2204.02311.pdf)\] *— 540B params, 118 layers, 18432 embd dim, 48 heads — Google Apr 2022*

Current (as of Jan 2023) largest publicly known dense language model, unfortunately pre-Chinchilla. PaLM activates with SwiGLU, uses parallel attention, multi-query attention, rotary embeddings and uses the same matrices for input and output embeddings. No biases were used and a SentencePiece tokenizer with 256k tokens was used. PaLM was trained on 780B tokens, on a similar dataset as LaMDA and GLaM.

**GPT-NeoX**

\[[github](https://github.com/EleutherAI/gpt-neox)\]\[[paper](https://arxiv.org/pdf/2204.06745.pdf)\] — **20B params — Eleuther AI Feb 2022**

An Eleuther open-sourced model, trained on GPUs with [DeepSpeed](https://www.deepspeed.ai/) (microsoft) and [Nvidia Megatron](https://github.com/NVIDIA/Megatron-LM). It uses the same architectural modifications that GPT-J had and is trained on the entirety of Pile, 400B tokens.

**GPT-J**

\[[github](https://github.com/kingoflolz/mesh-transformer-jax/#gpt-j-6b)\] — *6.7B params — Eleuther AI Jul 2021*

Notable for being a fully open-sourced model, while matching the 6.7B performance from the GPT-3 paper. Trained on TPUs, and done with rotary embeddings, parallel attention. Only dense attention layers are used to reduce complexity. It was trained on [the Pile](https://pile.eleuther.ai/), an open dataset created by Eleuther AI which contains 22 smaller datasets including Common Crawl, OpenWebText, books and papers.

**GLaM**

\[[paper](https://arxiv.org/pdf/2112.06905.pdf)\] *— 1.2T parameters — Google Dec 2021*

Named “Generalist Language Model”, GLaM is a Mixture-of-Experts (MoE) model, where parameters are sparsely activated. It has 64 experts per layer, with each token activating 96.6B parameters. Each layer has a gating unit which selects one two of the 64 MLPs per each token

**LaMDA**

\[[paper](https://arxiv.org/pdf/2201.08239.pdf)\] — *137B params, 64 layers, 8192 embd dim, 128 heads — Google (demoed at I/O May 2021; paper posted Jan 2022)*

Dialog model made to follow [Meena](https://arxiv.org/pdf/2001.09977.pdf). A 2.81T dataset with a lot of dialog/forums (encoded with a 32k vocab size SentencePiece tokenizer) is specified. The base model is sometimes called LaMDA GLM or GLM-137B; LaMDA itself adds a lot of dialog finetuning on top.

> Though it’s explicit how many tokens the model was trained for. It does specify 1024 TPUv3 chips at 56.5% utilisation for 57.7 days, batch size 256k, probably bf16, and arithmetic says that would be about 900B of the 2.81T tokens.

**Switch**

\[[paper](https://arxiv.org/pdf/2101.03961.pdf)\] *— 1T parameters — Google Jun 2022*

An improvement on GLaM, SwitchTransformer only routes to one expert, reducing the amount of compute. It using a different routing mechanism, with the main update being that routing to a single expert works.

**BLOOM**

\[[paper](https://arxiv.org/pdf/2211.05100.pdf)\] — *176B params, 70 layers, 14336 embd dim, 112 heads — HuggingFace July 2022*

Current largest open-source model. Trained on a HuggingFace corpus called ROOTS, which is 498 HuggingFace datasets. The model was trained for 366B tokens. Positional encodings was done with ALiBi. 250k vocab size BPE tokenizer, to help accommodate for multilingual data.

**Galactica**

\[[paper](https://arxiv.org/pdf/2211.09085.pdf)\] *— 120B parameters — Meta Nov 2022*

Galactica is a science model pretrained mostly on papers, along with small amounts of code, other knowledge-based data and a bit of common crawl. It uses a `<work>` token to encode working memory, as well as special tokens for citations.

**LLaMa**

\[[paper](https://scontent-sjc3-1.xx.fbcdn.net/v/t39.8562-6/333078981_693988129081760_4712707815225756708_n.pdf?_nc_cat=108&ccb=1-7&_nc_sid=ad8a9d&_nc_ohc=ov6yTHfLfNQAX82vXIA&_nc_ht=scontent-sjc3-1.xx&oh=00_AfAg4KoJmp5lBEyThQ9XAh24xKRPZ-wVH1UWh4euhxSy8w&oe=63FFCFA2)\] *— 65B parameters — Meta Feb 2023*

Chinchilla replication. Fairly standard training mix of mostly Common Crawl.

**Jurassic J1-Grande v2**

\[[paper](https://arxiv.org/pdf/2204.14198.pdf) for v1\]\[[helm evals](https://crfm.stanford.edu/helm/latest)\] *— 17B parameters — AI21 Dec 2022*

No information other than the Helm results, which look really good for the size!

**OPT**

\[[paper](https://arxiv.org/pdf/2205.01068.pdf)\]\[[train logbook](https://github.com/facebookresearch/metaseq/blob/main/projects/OPT/chronicles/OPT175B_Logbook.pdf)\] — *175B params, same arch as GPT-3 — Meta May 2022*

Meta replication of GPT-3. Trains on the Pile and PushShift reddit, for only 180B tokens.

> The Meta papers aren’t at all connected projects. LLama, OPT and Galactica share only one author of 41.

**GLM-130B**

\[[paper](https://arxiv.org/pdf/2210.02414.pdf)\] — *130B params — Tsinghua University Oct 2022*

GLM is an open-sourced bilingual (Chinese and English) model. It uses rotary embeddings, DeepNorm, and activates the MLP with GeGLU. It notably inferenced in INT4 (where other models like BLOOM and OPT had quantized to INT8). It also includes prompts in pretraining Instead of the standard GPT architecture, it uses GLM for bidirectional attention.

## 2\. Architectural Changes

**Multi-Query Attention**

This [Noam Shazeer solo paper](https://arxiv.org/pdf/1911.02150.pdf), where the key and values are shared across heads, greatly reducing the amount of memory required at inference time, improving latency and throughput. It’s a perfectly concise barely 9 page paper complete with code and results so it feels silly to describe further. AlphaCode and PaLM both use multi-query.

**Sparse Attention**

\[[sparse transformer paper](https://arxiv.org/pdf/1904.10509.pdf)\] — Sparse attention is a mechanism where attention is not applied to all previous tokens. It describes two styles of the SparseTransformer, strided where it looks at the last N tokens, and then fixed where sections of tokens in the sequence are attended to. In the GPT-3 paper, the model is described to have alternating dense and “locally banded” sparse layers.

**Mixture-of-Experts**

There’s a lot more lore on MoE, and I already gave the one-liner in describing GLaM and Switch so here I’ll just give an good initial literature list!

- the [original MoE paper](https://arxiv.org/abs/1701.06538) from 2017 on LSTMs
- Deepmind Scaling Laws [paper](https://arxiv.org/pdf/2202.01169.pdf) for MoE
- Meta [paper](https://arxiv.org/pdf/2112.10684.pdf) that trains a 1.1T param MoE
- A [large](https://arxiv.org/pdf/2202.08906.pdf) [pool](https://arxiv.org/pdf/2202.09368.pdf) [of](https://arxiv.org/pdf/2205.10937.pdf) [Google](https://arxiv.org/pdf/2202.08906.pdf) [papers](https://openreview.net/pdf?id=23ZjUGpjcc)

**FlashAttention**

[FlashAttention](https://arxiv.org/pdf/2205.14135.pdf) is an architectural change to do attention with less memory access (most of costs in most cases). It tiles and incrementally performs the softmax reduction and avoids storing the whole intermediate attention matrix for the backwards pass. The paper cites 1.7x training speedup compared to megatron and up to over 4x on inference (with the multiplier increasing with longer context lengths). The same sort of approach achieving O(log\_n) memory was done earlier on TPUs in [this paper](https://arxiv.org/pdf/2112.05682.pdf).

**Encoder+Decoder** A la original [transformer paper](https://arxiv.org/pdf/1706.03762.pdf), the encoder decoder architecture was originally made for translation tasks. Where the classic GPT architecture are alternating attention and mlp blocks, the original transformer had an encoder block which was attention → mlp and a decoder block which was masked attention → encoder-decoder attention → mlp. This is still a reasonable architecture to many kinds of sequence-to-sequence tasks, such as AlphaCode or [T5](https://arxiv.org/pdf/1910.10683.pdf) (Google, 2019, 11B params).

**Parallel Attention**

[PaLM](https://arxiv.org/pdf/2204.02311.pdf) uses parallel attention (poorly named) where the model is trained with the attention and MLP layers run in parallel, taking the same vectors. This makes it so that you can do your attention and feed-forward matmuls together to increase arithmetic intensity for better performance (15% on PaLM). GPT-J also uses it.

**Activation Alternatives: GeGLU, SwiGLU, SoLU**

The [original transformer paper](https://arxiv.org/pdf/1706.03762.pdf) uses ReLU (Rectified Linear Unit) to activate the MLP block. It does the simple x if > x = 0 else 0 in between the two linear transformations (matmuls). Intuitively, this is a bit too no-brained. GeLU (Gaussian error) is similar to ReLU but smooths it out a bit. SoLU (Softmax) introduced by [this Anthropic paper](https://transformer-circuits.pub/2022/solu/index.html), is simply `x*softmax(x)` and is used to improve the interpretability of models. SwiGLU is the most sophisticated of the listed, and is a [Noam Shazeer solo paper](https://arxiv.org/pdf/2002.05202.pdf), as it came through “divine benevolence”. It builds upon gated linear units (meant to be more stable than ReLU) and does the swish operation before the GLU. Like GeLU, it softens out the ReLU and allows some values to be under zero.

**LayerNorm Alternatives: DeepNorm, RMSNorm**

LLMs norm twice per block (once for attention, once to feed-forward), which does some normalisation function to improve training. [DeepNorm](https://arxiv.org/pdf/2203.00555.pdf) and [RMSNorm](https://arxiv.org/pdf/1910.07467.pdf) are alternatives. RMSNorm (Root Mean Square) is simply the square root of the mean of the values. There’s also a batch norm that’s inefficient and seems silly to use.

**RoPE**

\[[paper](https://arxiv.org/pdf/2104.09864.pdf)\]\[[blog post](https://blog.eleuther.ai/rotary-embeddings/)\] — I don’t want to try to summarize this one because there’s a good tl;dr in the blog post.

**BPE vs SentencePiece Tokenizers** \[\[bpe\](https://huggingface.co/course/chapter6/5?fw=pt)\]\[[sentence piece](https://github.com/google/sentencepiece)\] — Byte Pair Encodings are the default for most language models, being used by the original GPT paper, GPT-3 and presumably (based on the API) GPT-3.5. An obvious reason to not use plain BPE (and instead use SentencePiece) is if your distribution doesn’t contain space separated words, as AlphaCode, GLM (Chinese) and PaLM (explicitly because multilingual) did.

**ALiBi**

[Attention with Linear Biases](https://arxiv.org/pdf/2108.12409.pdf) is a long context positional embedding scheme to support extrapolation to longer lengths, by biasing (linearly) the qk scores according to their distance. BLOOM uses ALiBi and Galactica tried it though didn’t go through with it.

## 3\. Post-Pre-Training Techniques

**RLHF with PPO**

In RLHF, a reward model is trained, where the labeler evaluates an array of model generations. Then the PPO ([proximal policy optimization](https://arxiv.org/pdf/1707.06347.pdf)) is used for the RL, where the policy generates an output evaluated by the reward model to improve on the policy.

Deepmind’s [Sparrow](https://arxiv.org/pdf/2209.14375.pdf), as well as Anthropic’s LMs are trained with RL(AI|H)F are have dialog interfaces. [WebGPT](https://arxiv.org/pdf/2112.09332.pdf) was was trained with RLHF, as was [GopherCite](https://storage.googleapis.com/deepmind-media/Teaching%20language%20models%20to%20support%20answers%20with%20verified%20quotes/Teaching%20language%20models%20to%20support%20answers%20with%20verified%20quotes.pdf) (which called RLHPreferences). I’d say the origination was [Christiano 2017](https://proceedings.neurips.cc/paper/2017/hash/d5e2c0adad503c91f91df240d0cd4e49-Abstract.html), preceding any LLM stuff, followed by 2020 [summarizing from human feedback](https://proceedings.neurips.cc/paper/2020/file/1f89885d556929e98d3ef9b86448f951-Paper.pdf), along with the PPO paper.

**Constitutional**

An extension of RLHF, [Constitutional](https://arxiv.org/pdf/2212.08073.pdf) is basically RLAIF, though actually called “CAI”. It has a supervised learning phase where a helpful-only AI is used to generate adversarial prompts. The assistant then iterates on its own response based on the provided constitution (a short set of values for the model to follow in the form of a string). Then finetuning is done on those responses. The second stage then is like RLHF with PPO, except substituting the AI feedback.

**Minerva**

Released in 2022 June from the Blueshift team, [Minerva](https://arxiv.org/pdf/2206.14858.pdf) is a finetuned model on math and science data, particularly well-executed. It’s a 62/540B finetuned model from PaLM, with datasets from ArXiV and some websites that were carefully preprocessed to preserve mathematical formatting.

**Codex**

Launched in July 2021 (and resulted in Github Copilot), [Codex](https://arxiv.org/pdf/2107.03374.pdf) is a finetune on 100B tokens of code (in this case, publicly available Github code). The paper also debuted HumanEval, human written code evals. This paper most notably demonstrates that code data is really important for code performance, as GPT-J was outperforming 3 at code. They also added some tokens for code, which improved the compression by 30%.

**Just Finetune on CoTed Outputs**

I forgot which paper did this but its like they finetuned their model on chain of thought outputs from the model, and it did better. Expected, but notable result.

**FeedME (SFT)**

Described in [Instruct GPT paper](https://arxiv.org/pdf/2203.02155.pdf) (though it is not necessarily the origination, which is closer [to this](https://arxiv.org/abs/1909.08593)). Supervised Fine-Tuning uses human-generated content which is then used to fine-tune the pre-trained model. The paper finds that SFT performs better than base pre-trained models but RLHF performs better than SFT.

**FLAN**

[Flan](https://arxiv.org/pdf/2109.01652.pdf) is an instruction-tuned model (finetuned on instruction-formatted nlp tasks) that results in improved zero-shot performance.

## 4\. Training Techniques

**Being** **Good at Setting Hyperparameters** There is obviously no one paper for this, but obviously getting the hyperparameters right is pretty important. Some baseline is available by reading papers, with the most notable probably being [Chinchilla](https://arxiv.org/pdf/2203.15556.pdf) or the [Scaling Laws paper](https://arxiv.org/pdf/2001.08361.pdf). There are also a bunch of good theory-based papers, though the one I am familiar with is actually this Jane Street [blog post on understanding batch size](https://blog.janestreet.com/does-batch-size-matter/).

**Pre-training with Human Feedback**

Pre-training tends to have a very unsupervised format, though [PHF](https://arxiv.org/pdf/2302.08582.pdf) (Feb 2023) applies a simple technique to label data at pretraining. It uses two conditioning tokens (good and bad) prepended to samples at training and then samples with them at inference. They tried various other objectives (notably, filtering out bad data) that all performed worse, evaluated on python styling, PII and toxicity.

**MuP**

[Maximal Update Parameterization](https://arxiv.org/pdf/2203.03466.pdf) is a method of parameterization that makes hyperparameters (the ones related to learning rates and optimisers) predictable (consistent) across model sizes. It not only saves the parameter sweep compute but should also be closer to optimal. The paper does a really good job getting into the theory of why this works.

## None of the Above

**Chain of Thought**

This is a technique where it makes the model think “step-by-step” and yielding better results. That name originated in [this paper](https://arxiv.org/pdf/2201.11903.pdf), which describes a specific application of the technique described in this February 2021 [paper](https://arxiv.org/pdf/2102.07350.pdf) which describes ways to do prompting that aren’t just few-shotting. The phrase now is sometimes used to describe techniques that aren’t just prompting.

**Tool Use**

A good canonical tool use paper is probably the Dec 2021 [WebGPT paper](https://arxiv.org/pdf/2112.09332.pdf) (though the earliest paper I can find is probably this [2017 Karpathy paper](https://proceedings.mlr.press/v70/shi17a.html)), in which capabilities are greatly enhanced by giving GPT-3 access to the web. It is finetuned with some RL and SL, though I put this not as a training or post-pretraining technique since the concept is not dependent on that. DeepMind also trained [RL tool use agents](https://arxiv.org/pdf/2202.08137.pdf), and Meta has [toolformer](https://arxiv.org/pdf/2302.04761.pdf) which does finetuning focused on API usage.

**Fill In the Middle**

This July 2022 [paper](https://arxiv.org/pdf/2207.14255.pdf) describes a simple data transformation which moves a substring from the middle of a text to the end, and asks the model to fill in the middle. This allows the model to gain a capability that is really useful for tasks like code completion without damage to performance on strictly left to right tasks.

**Sampling Techniques: Top-k, Top-p (nucleus), Beam Search**

The output of language models is fundamentally logits for every possible token, which are then softmaxed into becoming probabilities. The most naive way of turning your logits into tokens, is to take the most likely token. When there are temperature controls with language models, it’s dividing the logits by the temperature, which makes the model more/less confident in its top choice. Top-K sampling takes the top K tokens and samples from that distribution. Top-P sampling (it has a [paper](https://arxiv.org/pdf/1904.09751.pdf) but it’s probably useless), or nucleus sampling, uses the top P percentage (think CDFs) of tokens and samples from there.

**Tail Free Sampling**

[Tail Free Sampling](https://www.trentonbricken.com/Tail-Free-Sampling/) takes the derivative of top-P sampling, and is named as such to find the “tail”, as top-P sampling could fail in cases of being cut off at a point where many tokens have similar probabilities. The post linked details the theoretical reasons this should result in better sampling, but when it comes to improving creativity and range in the models there are no good benchmarks.

---

This feels particularly good to publish now since i feel like its ~the last time something like this could be helpful, given how close we are and the diminishing amount of published research.

*Edited by Claude <3*