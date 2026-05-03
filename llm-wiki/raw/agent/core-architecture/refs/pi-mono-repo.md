---
title: "GitHub - badlogic/pi-mono: AI agent toolkit: coding agent CLI, unified LLM API, TUI & web UI libraries, Slack bot, vLLM pods"
url: "https://github.com/badlogic/pi-mono"
requestedUrl: "https://github.com/badlogic/pi-mono"
coverImage: "https://opengraph.githubassets.com/dfc0682a449a2bcbe41285c8b27808e908c54a5c59f393ccaabb7bb492e78e2b/badlogic/pi-mono"
siteName: "GitHub"
summary: "AI agent toolkit: coding agent CLI, unified LLM API, TUI & web UI libraries, Slack bot, vLLM pods - badlogic/pi-mono"
adapter: "generic"
capturedAt: "2026-05-03T13:04:13.146Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# GitHub - badlogic/pi-mono: AI agent toolkit: coding agent CLI, unified LLM API, TUI & web UI libraries, Slack bot, vLLM pods

[![pi logo](https://camo.githubusercontent.com/17747c1d541a223db8935e5a9112f17fb7c45b39c84d139e5cea9e133068bb2f/68747470733a2f2f70692e6465762f6c6f676f2e737667)](https://pi.dev/)[![Discord](https://camo.githubusercontent.com/953294acc08eb8150a8cafc213631144bebb20fea7bd4e407ef813d6c121dfd8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646973636f72642d636f6d6d756e6974792d3538363546323f7374796c653d666c61742d737175617265266c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465)](https://discord.com/invite/3cU7Bz4UPx) [![Build status](https://camo.githubusercontent.com/56abc7c4f932466ac09d8adafcac16f558e5ffd52989432b9d6d2d153de56374/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f6261646c6f6769632f70692d6d6f6e6f2f63692e796d6c3f7374796c653d666c61742d737175617265266272616e63683d6d61696e)](https://github.com/badlogic/pi-mono/actions/workflows/ci.yml)

[pi.dev](https://pi.dev/) domain graciously donated by

[![Exy mascot](https://github.com/badlogic/pi-mono/raw/main/packages/coding-agent/docs/images/exy.png)
exe.dev](https://exe.dev/)

> New issues and PRs from new contributors are auto-closed by default. Maintainers review auto-closed issues daily. See [CONTRIBUTING.md](https://github.com/badlogic/pi-mono/blob/main/CONTRIBUTING.md).

---

## Pi Monorepo

> **Looking for the pi coding agent?** See **[packages/coding-agent](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent)** for installation and usage.

Tools for building AI agents.

If you use pi or other coding agents for open source work, please share your sessions.

Public OSS session data helps improve coding agents with real-world tasks, tool use, failures, and fixes instead of toy benchmarks.

For the full explanation, see [this post on X](https://x.com/badlogicgames/status/2037811643774652911).

To publish sessions, use [`badlogic/pi-share-hf`](https://github.com/badlogic/pi-share-hf). Read its README.md for setup instructions. All you need is a Hugging Face account, the Hugging Face CLI, and `pi-share-hf`.

You can also watch [this video](https://x.com/badlogicgames/status/2041151967695634619), where I show how I publish my `pi-mono` sessions.

I regularly publish my own `pi-mono` work sessions here:

- [badlogicgames/pi-mono on Hugging Face](https://huggingface.co/datasets/badlogicgames/pi-mono)

## Packages

| Package | Description |
| --- | --- |
| **[@mariozechner/pi-ai](https://github.com/badlogic/pi-mono/blob/main/packages/ai)** | Unified multi-provider LLM API (OpenAI, Anthropic, Google, etc.) |
| **[@mariozechner/pi-agent-core](https://github.com/badlogic/pi-mono/blob/main/packages/agent)** | Agent runtime with tool calling and state management |
| **[@mariozechner/pi-coding-agent](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent)** | Interactive coding agent CLI |
| **[@mariozechner/pi-tui](https://github.com/badlogic/pi-mono/blob/main/packages/tui)** | Terminal UI library with differential rendering |
| **[@mariozechner/pi-web-ui](https://github.com/badlogic/pi-mono/blob/main/packages/web-ui)** | Web components for AI chat interfaces |

## Chat bot workflows

For Slack/chat automation, see [earendil-works/pi-chat](https://github.com/earendil-works/pi-chat).

## Contributing

See [CONTRIBUTING.md](https://github.com/badlogic/pi-mono/blob/main/CONTRIBUTING.md) for contribution guidelines and [AGENTS.md](https://github.com/badlogic/pi-mono/blob/main/AGENTS.md) for project-specific rules (for both humans and agents).

## Development

```
npm install          # Install all dependencies
npm run build        # Build all packages
npm run check        # Lint, format, and type check
./test.sh            # Run tests (skips LLM-dependent tests without API keys)
./pi-test.sh         # Run pi from sources (can be run from any directory)
```

> **Note:** `npm run check` requires `npm run build` to be run first. The web-ui package uses `tsc` which needs compiled `.d.ts` files from dependencies.

## License

MIT