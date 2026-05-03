---
title: "GitHub - anomalyco/opencode: The open source coding agent."
url: "https://github.com/anomalyco/opencode"
requestedUrl: "https://github.com/anomalyco/opencode"
coverImage: "https://repository-images.githubusercontent.com/975734319/2c2c3389-c647-405c-a499-f80e4d521277"
siteName: "GitHub"
summary: "The open source coding agent. Contribute to anomalyco/opencode development by creating an account on GitHub."
adapter: "generic"
capturedAt: "2026-05-03T13:04:37.092Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# GitHub - anomalyco/opencode: The open source coding agent.

[![OpenCode logo](https://github.com/anomalyco/opencode/raw/dev/packages/console/app/src/asset/logo-ornate-light.svg)](https://opencode.ai/)The open source AI coding agent.

[![Discord](https://camo.githubusercontent.com/83daa53aa89771d7c1b411e9d8aab90692f07934a8c2aea6a6794687082e2f68/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f313339313833323432363034383635313333343f7374796c653d666c61742d737175617265266c6162656c3d646973636f7264)](https://opencode.ai/discord) [![npm](https://camo.githubusercontent.com/4e57d77e1805497a6befb9cc1743a8069756f26377e832d09f1ba2ca49f9370c/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f762f6f70656e636f64652d61693f7374796c653d666c61742d737175617265)](https://www.npmjs.com/package/opencode-ai) [![Build status](https://camo.githubusercontent.com/dfb623969ed19b150f1ccf242b1b4c4b4629515c1aa0603fb795ff3e407c1b2d/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f616e6f6d616c79636f2f6f70656e636f64652f7075626c6973682e796d6c3f7374796c653d666c61742d737175617265266272616e63683d646576)](https://github.com/anomalyco/opencode/actions/workflows/publish.yml)

[English](https://github.com/anomalyco/opencode/blob/dev/README.md) | [简体中文](https://github.com/anomalyco/opencode/blob/dev/README.zh.md) | [繁體中文](https://github.com/anomalyco/opencode/blob/dev/README.zht.md) | [한국어](https://github.com/anomalyco/opencode/blob/dev/README.ko.md) | [Deutsch](https://github.com/anomalyco/opencode/blob/dev/README.de.md) | [Español](https://github.com/anomalyco/opencode/blob/dev/README.es.md) | [Français](https://github.com/anomalyco/opencode/blob/dev/README.fr.md) | [Italiano](https://github.com/anomalyco/opencode/blob/dev/README.it.md) | [Dansk](https://github.com/anomalyco/opencode/blob/dev/README.da.md) | [日本語](https://github.com/anomalyco/opencode/blob/dev/README.ja.md) | [Polski](https://github.com/anomalyco/opencode/blob/dev/README.pl.md) | [Русский](https://github.com/anomalyco/opencode/blob/dev/README.ru.md) | [Bosanski](https://github.com/anomalyco/opencode/blob/dev/README.bs.md) | [العربية](https://github.com/anomalyco/opencode/blob/dev/README.ar.md) | [Norsk](https://github.com/anomalyco/opencode/blob/dev/README.no.md) | [Português (Brasil)](https://github.com/anomalyco/opencode/blob/dev/README.br.md) | [ไทย](https://github.com/anomalyco/opencode/blob/dev/README.th.md) | [Türkçe](https://github.com/anomalyco/opencode/blob/dev/README.tr.md) | [Українська](https://github.com/anomalyco/opencode/blob/dev/README.uk.md) | [বাংলা](https://github.com/anomalyco/opencode/blob/dev/README.bn.md) | [Ελληνικά](https://github.com/anomalyco/opencode/blob/dev/README.gr.md) | [Tiếng Việt](https://github.com/anomalyco/opencode/blob/dev/README.vi.md)

[![OpenCode Terminal UI](https://github.com/anomalyco/opencode/raw/dev/packages/web/src/assets/lander/screenshot.png)](https://opencode.ai/)

---

### Installation

```
# YOLO
curl -fsSL https://opencode.ai/install | bash

# Package managers
npm i -g opencode-ai@latest        # or bun/pnpm/yarn
scoop install opencode             # Windows
choco install opencode             # Windows
brew install anomalyco/tap/opencode # macOS and Linux (recommended, always up to date)
brew install opencode              # macOS and Linux (official brew formula, updated less)
sudo pacman -S opencode            # Arch Linux (Stable)
paru -S opencode-bin               # Arch Linux (Latest from AUR)
mise use -g opencode               # Any OS
nix run nixpkgs#opencode           # or github:anomalyco/opencode for latest dev branch
```

> [!tip] Tip
> Remove versions older than 0.1.x before installing.

### Desktop App (BETA)

OpenCode is also available as a desktop application. Download directly from the [releases page](https://github.com/anomalyco/opencode/releases) or [opencode.ai/download](https://opencode.ai/download).

| Platform | Download |
| --- | --- |
| macOS (Apple Silicon) | `opencode-desktop-darwin-aarch64.dmg` |
| macOS (Intel) | `opencode-desktop-darwin-x64.dmg` |
| Windows | `opencode-desktop-windows-x64.exe` |
| Linux | `.deb`, `.rpm`, or AppImage |

```
# macOS (Homebrew)
brew install --cask opencode-desktop
# Windows (Scoop)
scoop bucket add extras; scoop install extras/opencode-desktop
```

#### Installation Directory

The install script respects the following priority order for the installation path:

1. `$OPENCODE_INSTALL_DIR` - Custom installation directory
2. `$XDG_BIN_DIR` - XDG Base Directory Specification compliant path
3. `$HOME/bin` - Standard user binary directory (if it exists or can be created)
4. `$HOME/.opencode/bin` - Default fallback
```
# Examples
OPENCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://opencode.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://opencode.ai/install | bash
```

### Agents

OpenCode includes two built-in agents you can switch between with the `Tab` key.

- **build** - Default, full-access agent for development work
- **plan** - Read-only agent for analysis and code exploration
	- Denies file edits by default
		- Asks permission before running bash commands
		- Ideal for exploring unfamiliar codebases or planning changes

Also included is a **general** subagent for complex searches and multistep tasks. This is used internally and can be invoked using `@general` in messages.

Learn more about [agents](https://opencode.ai/docs/agents).

### Documentation

For more info on how to configure OpenCode, [**head over to our docs**](https://opencode.ai/docs).

### Contributing

If you're interested in contributing to OpenCode, please read our [contributing docs](https://github.com/anomalyco/opencode/blob/dev/CONTRIBUTING.md) before submitting a pull request.

### Building on OpenCode

If you are working on a project that's related to OpenCode and is using "opencode" as part of its name, for example "opencode-dashboard" or "opencode-mobile", please add a note to your README to clarify that it is not built by the OpenCode team and is not affiliated with us in any way.

### FAQ

#### How is this different from Claude Code?

It's very similar to Claude Code in terms of capability. Here are the key differences:

- 100% open source
- Not coupled to any provider. Although we recommend the models we provide through [OpenCode Zen](https://opencode.ai/zen), OpenCode can be used with Claude, OpenAI, Google, or even local models. As models evolve, the gaps between them will close and pricing will drop, so being provider-agnostic is important.
- Built-in opt-in LSP support
- A focus on TUI. OpenCode is built by neovim users and the creators of [terminal.shop](https://terminal.shop/); we are going to push the limits of what's possible in the terminal.
- A client/server architecture. This, for example, can allow OpenCode to run on your computer while you drive it remotely from a mobile app, meaning that the TUI frontend is just one of the possible clients.

---

**Join our community** [Discord](https://discord.gg/opencode) | [X.com](https://x.com/opencode)