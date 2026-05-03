---
title: "GitHub - NousResearch/hermes-agent: The agent that grows with you"
url: "https://github.com/NousResearch/hermes-agent"
requestedUrl: "https://github.com/nousresearch/hermes-agent"
coverImage: "https://opengraph.githubassets.com/9ce6283bb3e34f69354cfd070b6b96a318e57ba168a4683e2eb927d6dee40277/NousResearch/hermes-agent"
siteName: "GitHub"
summary: "The agent that grows with you. Contribute to NousResearch/hermes-agent development by creating an account on GitHub."
adapter: "generic"
capturedAt: "2026-05-03T13:04:29.484Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# GitHub - NousResearch/hermes-agent: The agent that grows with you

[![Hermes Agent](https://github.com/NousResearch/hermes-agent/raw/main/assets/banner.png)](https://github.com/NousResearch/hermes-agent/blob/main/assets/banner.png)

## Hermes Agent ☤

[![Documentation](https://camo.githubusercontent.com/76d7a880842f286c4d4e07baf2db1046197c6cfaa564365e912938445fc54a32/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f63732d6865726d65732d2d6167656e742e6e6f757372657365617263682e636f6d2d4646443730303f7374796c653d666f722d7468652d6261646765)](https://hermes-agent.nousresearch.com/docs/) [![Discord](https://camo.githubusercontent.com/8c0fca73564f21d7a6f235747eb4d739a2e4aaa348b8e074904127baeb944b9e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446973636f72642d3538363546323f7374796c653d666f722d7468652d6261646765266c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465)](https://discord.gg/NousResearch) [![License: MIT](https://camo.githubusercontent.com/153acf9dff19deb8abfc598c53bac50a4ceae0f5c83a552711060d3d78d2c057/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d677265656e3f7374796c653d666f722d7468652d6261646765)](https://github.com/NousResearch/hermes-agent/blob/main/LICENSE) [![Built by Nous Research](https://camo.githubusercontent.com/6195af06150f2173f79d16fa3462ccac43c7dbf78f06f3c7997dc4090d79b9ad/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4275696c7425323062792d4e6f757325323052657365617263682d626c756576696f6c65743f7374796c653d666f722d7468652d6261646765)](https://nousresearch.com/)

**The self-improving AI agent built by [Nous Research](https://nousresearch.com/).** It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — [Nous Portal](https://portal.nousresearch.com/), [OpenRouter](https://openrouter.ai/) (200+ models), [NVIDIA NIM](https://build.nvidia.com/) (Nemotron), [Xiaomi MiMo](https://platform.xiaomimimo.com/), [z.ai/GLM](https://z.ai/), [Kimi/Moonshot](https://platform.moonshot.ai/), [MiniMax](https://www.minimax.io/), [Hugging Face](https://huggingface.co/), OpenAI, or your own endpoint. Switch with `hermes model` — no code changes, no lock-in.

| **A real terminal interface** | Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output. |
| --- | --- |
| **Lives where you do** | Telegram, Discord, Slack, WhatsApp, Signal, and CLI — all from a single gateway process. Voice memo transcription, cross-platform conversation continuity. |
| **A closed learning loop** | Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. [Honcho](https://github.com/plastic-labs/honcho) dialectic user modeling. Compatible with the [agentskills.io](https://agentskills.io/) open standard. |
| **Scheduled automations** | Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended. |
| **Delegates and parallelizes** | Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns. |
| **Runs anywhere, not just your laptop** | Six terminal backends — local, Docker, SSH, Daytona, Singularity, and Modal. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster. |
| **Research-ready** | Batch trajectory generation, Atropos RL environments, trajectory compression for training the next generation of tool-calling models. |

---

## Quick Install

```
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Works on Linux, macOS, WSL2, and Android via Termux. The installer handles the platform-specific setup for you.

> **Android / Termux:** The tested manual path is documented in the [Termux guide](https://hermes-agent.nousresearch.com/docs/getting-started/termux). On Termux, Hermes installs a curated `.[termux]` extra because the full `.[all]` extra currently pulls Android-incompatible voice dependencies.
>
> **Windows:** Native Windows is not supported. Please install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run the command above.

After installation:

```
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

---

## Getting Started

```
hermes              # Interactive CLI — start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes config set   # Set individual config values
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configures everything at once)
hermes claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
hermes update       # Update to the latest version
hermes doctor       # Diagnose any issues
```

📖 **[Full documentation →](https://hermes-agent.nousresearch.com/docs/)**

## CLI vs Messaging Quick Reference

Hermes has two entry points: start the terminal UI with `hermes`, or run the gateway and talk to it from Telegram, Discord, Slack, WhatsApp, Signal, or Email. Once you're in a conversation, many slash commands are shared across both interfaces.

| Action | CLI | Messaging platforms |
| --- | --- | --- |
| Start chatting | `hermes` | Run `hermes gateway setup` + `hermes gateway start`, then send the bot a message |
| Start fresh conversation | `/new` or `/reset` | `/new` or `/reset` |
| Change model | `/model [provider:model]` | `/model [provider:model]` |
| Set a personality | `/personality [name]` | `/personality [name]` |
| Retry or undo the last turn | `/retry`, `/undo` | `/retry`, `/undo` |
| Compress context / check usage | `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]` |
| Browse skills | `/skills` or `/<skill-name>` | `/<skill-name>` |
| Interrupt current work | `Ctrl+C` or send a new message | `/stop` or send a new message |
| Platform-specific status | `/platforms` | `/status`, `/sethome` |

For the full command lists, see the [CLI guide](https://hermes-agent.nousresearch.com/docs/user-guide/cli) and the [Messaging Gateway guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging).

---

## Documentation

All documentation lives at **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**:

| Section | What's Covered |
| --- | --- |
| [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) | Install → setup → first conversation in 2 minutes |
| [CLI Usage](https://hermes-agent.nousresearch.com/docs/user-guide/cli) | Commands, keybindings, personalities, sessions |
| [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) | Config file, providers, models, all options |
| [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging) | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) | Command approval, DM pairing, container isolation |
| [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools) | 40+ tools, toolset system, terminal backends |
| [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | Procedural memory, Skills Hub, creating skills |
| [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | Persistent memory, user profiles, best practices |
| [MCP Integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) | Connect any MCP server for extended capabilities |
| [Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) | Scheduled tasks with platform delivery |
| [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) | Project context that shapes every conversation |
| [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | Project structure, agent loop, key classes |
| [Contributing](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) | Development setup, PR process, code style |
| [CLI Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) | All commands and flags |
| [Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) | Complete env var reference |

---

## Migrating from OpenClaw

If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.

**During first-time setup:** The setup wizard (`hermes setup`) automatically detects `~/.openclaw` and offers to migrate before configuration begins.

**Anytime after install:**

```
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

What gets imported:

- **SOUL.md** — persona file
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — user-created skills → `~/.hermes/skills/openclaw-imports/`
- **Command allowlist** — approval patterns
- **Messaging settings** — platform configs, allowed users, working directory
- **API keys** — allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS assets** — workspace audio files
- **Workspace instructions** — AGENTS.md (with `--workspace-target`)

See `hermes claw migrate --help` for all options, or use the `openclaw-migration` skill for an interactive agent-guided migration with dry-run previews.

---

## Contributing

We welcome contributions! See the [Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) for development setup, code style, and PR process.

Quick start for contributors — clone and go with `setup-hermes.sh`:

```
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
./setup-hermes.sh     # installs uv, creates venv, installs .[all], symlinks ~/.local/bin/hermes
./hermes              # auto-detects the venv, no need to \`source\` first
```

Manual path (equivalent to the above):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

> **RL Training (optional):** The RL/Atropos integration (`environments/`) ships via the `atroposlib` and `tinker` dependencies pulled in by `.[all,dev]` — no submodule setup required.

---

## Community

- 💬 [Discord](https://discord.gg/NousResearch)
- 📚 [Skills Hub](https://agentskills.io/)
- 🐛 [Issues](https://github.com/NousResearch/hermes-agent/issues)
- 🔌 [HermesClaw](https://github.com/AaronWong1999/hermesclaw) — Community WeChat bridge: Run Hermes Agent and OpenClaw on the same WeChat account.