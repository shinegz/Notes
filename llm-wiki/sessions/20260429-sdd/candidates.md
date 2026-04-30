# Collect session — SDD 规范驱动开发深度研究

- **Goal**: 深入研究 SDD 理论基础、框架生态与三大项目（Superpowers、Gstack、Compound Engineering）的源码实现
- **Default shelf**: `sdd`
- **Created**: 2026-04-29

## Candidate sources（待你确认）

### 理论/概述文章

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [ ] | blog | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | sdd | `articles/martin-fowler-sdd-3-tools.md` | Martin Fowler 对 SDD 及三大框架的权威解读 |
| [ ] | blog | https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai/ | sdd | `articles/github-blog-spec-driven-development.md` | GitHub 官方对 OpenSpec 及 SDD 工作流的介绍 |
| [ ] | blog | https://jeromevdl.medium.com/spec-driven-development-back-to-the-future-d71fde8d47cf | sdd | `articles/medium-spec-driven-back-to-future.md` | 从 API Design First 到 AI SDD 的历史演进 |
| [ ] | blog | https://zhuanlan.zhihu.com/p/2009360235362526486 | sdd | `articles/zhihu-sdd-framework-landscape.md` | 中文视角：五大框架对比与选型建议 |

### GitHub 项目文档

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [ ] | repo | https://github.com/obra/superpowers | sdd | `articles/obra-superpowers-readme.md` | Superpowers 官方 README：agentic skills 框架设计哲学 |
| [ ] | repo | https://github.com/garrytan/gstack | sdd | `articles/garrytan-gstack-readme.md` | Gstack 官方 README：23 个 opinionated tools 的 Claude Code 设置 |
| [ ] | repo | https://github.com/EveryInc/compound-engineering-plugin | sdd | `articles/everyinc-compound-engineering-readme.md` | Compound Engineering 官方 README：AI 工程复合增长平台 |

### 源码指针（refs）

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [ ] | repo-pointer | https://github.com/obra/superpowers | sdd | `refs/superpowers-repo.md` | 源码分析指针：核心 skills 目录与实现文件 |
| [ ] | repo-pointer | https://github.com/garrytan/gstack | sdd | `refs/gstack-repo.md` | 源码分析指针：tools 目录结构与 ARCHITECTURE.md |
| [ ] | repo-pointer | https://github.com/EveryInc/compound-engineering-plugin | sdd | `refs/compound-engineering-repo.md` | 源码分析指针：plugins 目录与 skill 系统实现 |

## 你的批复

用户全选（10 项），Agent 执行抓取。

## Fetched（确认后由 Agent 填写）

| raw路径 | 状态 |
|----------|------|
| `raw/sdd/articles/martin-fowler-sdd-3-tools.md` | ✅ 已抓取 |
| `raw/sdd/articles/github-blog-spec-driven-development.md` | ✅ 已抓取（URL 修正为完整路径） |
| `raw/sdd/articles/medium-spec-driven-back-to-future.md` | ❌ 网络超时（Medium 连接失败，tavily 需 API key） |
| `raw/sdd/articles/zhihu-sdd-framework-landscape.md` | ✅ 已抓取 |
| `raw/sdd/articles/obra-superpowers-readme.md` | ✅ 已抓取 |
| `raw/sdd/articles/garrytan-gstack-readme.md` | ✅ 已抓取 |
| `raw/sdd/articles/everyinc-compound-engineering-readme.md` | ✅ 已抓取 |
| `raw/sdd/refs/superpowers-repo.md` | ✅ 已创建 |
| `raw/sdd/refs/gstack-repo.md` | ✅ 已创建 |
| `raw/sdd/refs/compound-engineering-repo.md` | ✅ 已创建 |

**注**：Medium 文章因网络限制未能获取，可在后续补充或替换为其他来源。
