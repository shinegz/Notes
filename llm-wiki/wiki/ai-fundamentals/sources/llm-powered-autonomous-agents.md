---
title: "LLM Powered Autonomous Agents"
type: source
tags: [agent, llm, planning, memory, tool-use, react, reflection]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/articles/llm-powered-autonomous-agents.md
---

# LLM Powered Autonomous Agents

**Lilian Weng**  
*OpenAI*

## Abstract

Building agents with LLM as its core controller is a powerful paradigm. LLM-powered autonomous agents consist of three key components: Planning (subgoal decomposition, reflection), Memory (short-term via context, long-term via vector stores), and Tool Use (external APIs). The article surveys major techniques including Chain of Thought, Tree of Thoughts, ReAct, Reflexion, and real-world proof-of-concepts like AutoGPT and GPT-Engineer.

## Key Contributions

- **Agent system taxonomy**: Three-component framework (Planning + Memory + Tool Use)
- **Task decomposition techniques**: CoT, ToT, LLM+P with external classical planners
- **Self-reflection mechanisms**: ReAct (reasoning + acting), Reflexion (dynamic memory), Chain of Hindsight
- **Tool-augmented LLMs**: MRKL, TALM, Toolformer, HuggingGPT, API-Bank benchmark
- **Real-world case studies**: ChemCrow (scientific discovery), Generative Agents (social simulation)

## Component One: Planning

| Technique | Description |
|-----------|-------------|
| **Chain of Thought (CoT)** | Instruct model to "think step by step" to decompose complex tasks |
| **Tree of Thoughts (ToT)** | Explore multiple reasoning possibilities at each step (BFS/DFS search) |
| **LLM+P** | Use external classical planner (PDDL) for long-horizon planning |
| **ReAct** | Integrate reasoning (Thought) and acting (Action/Observation) in a loop |
| **Reflexion** | Dynamic memory + self-reflection with heuristic-based trajectory evaluation |
| **Chain of Hindsight (CoH)** | Present sequence of past outputs with feedback for incremental improvement |
| **Algorithm Distillation (AD)** | Distill RL learning histories into in-context RL algorithm |

## Component Two: Memory

- **Sensory memory** → Embedding representations for raw inputs
- **Short-term memory** → In-context learning (restricted by finite context window)
- **Long-term memory** → External vector store with fast retrieval (MIPS/ANN)

Common ANN algorithms for fast retrieval: LSH, ANNOY, HNSW, FAISS, ScaNN.

## Component Three: Tool Use

- **MRKL**: Neuro-symbolic architecture routing to expert modules
- **TALM / Toolformer**: Fine-tune LM to learn external tool APIs
- **HuggingGPT**: Use ChatGPT as task planner for HuggingFace models
- **API-Bank**: Benchmark with 3 levels — call API, retrieve API, plan beyond retrieve+call

## Case Studies

| Project | Domain | Key Mechanism |
|---------|--------|---------------|
| ChemCrow | Organic synthesis / drug discovery | ReAct + 13 expert chemistry tools |
| Generative Agents | Social simulation (The Sims-like) | Memory stream + retrieval + reflection + planning |
| AutoGPT | General autonomous agent | JSON-formatted thought/action loop |
| GPT-Engineer | Code generation | Task clarification → code writing pipeline |

## Challenges

1. **Finite context length** limits historical information and tool call context
2. **Long-term planning and task decomposition** remain challenging for unexpected errors
3. **Reliability of natural language interface** — formatting errors and instruction refusal

## Connections

- [[react-chain-of-thought|ReAct paper]] — Original ReAct reasoning+acting framework
- [[toolformer]] — Language models teaching themselves to use tools
- [[attention-is-all-you-need|Transformer]] — Foundation architecture for LLM agents
- [[gpt3-language-models-few-shot|GPT-3]] — Base model for many agent systems
