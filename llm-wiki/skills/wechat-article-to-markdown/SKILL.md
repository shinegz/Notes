---
name: wechat-article-to-markdown
description: Fetch WeChat Official Account (微信公众号) articles from mp.weixin.qq.com and convert to Markdown. 微信文章转 Markdown 工具。
author: jackwener
version: "1.0.0"
tags:
 - wechat
 - 微信
 - 微信文章
 - 公众号
 - mp.weixin.qq.com
 - markdown
 - article
 - converter
 - cli
---

> **llm-wiki**：本目录为上游 [`jackwener/wechat-article-to-markdown`](https://github.com/jackwener/wechat-article-to-markdown) 的 `SKILL.md` 副本，与 **`tools/source_registry.tsv`** 中 `wechat_article`（**`adapter_name`** / **`dependency_name`** = `wechat-article-to-markdown`，**`dependency_type=install_time`**）对齐。安装与用法见下。

# WeChat Article to Markdown

Fetch a WeChat Official Account article and convert it to a clean Markdown file.

## When to use

Use this skill when you need to save WeChat articles as Markdown for:
- Personal archive
- AI summarization input
- Knowledge base ingestion

## Prerequisites

- Python 3.8+

```bash
# Install
uv tool install wechat-article-to-markdown
# Or: pipx install wechat-article-to-markdown
```

## Usage

```bash
wechat-article-to-markdown "<WECHAT_ARTICLE_URL>"
```

Input URL format:
- `https://mp.weixin.qq.com/s/...`

Output files:
- `output/<article-title>/<article-title>.md`
- `output/<article-title>/images/*`

## Features

1. Anti-detection fetch with Camoufox
2. Metadata extraction (title, account name, publish time, source URL)
3. Image localization to local files
4. WeChat code-snippet extraction and fenced code block output
5. HTML to Markdown conversion via markdownify
6. Concurrent image downloading

## Limitations

- Some code snippets are image/SVG rendered and cannot be extracted as source code
- Public `mp.weixin.qq.com` URL is required
