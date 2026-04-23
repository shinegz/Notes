# [决策]: docs: add wiki visual enhancement design spec

## 日期
2026-04-16

## 背景
从 commit 上下文推断

## 决策
docs: add wiki visual enhancement design spec

## 影响范围
- .../iteration-1/benchmark.json
- .../iteration-1/benchmark.md
- .../iteration-1/eval-0/eval_metadata.json
- .../iteration-1/eval-0/with_skill/grading.json
- ...267\261\345\272\246\350\247\243\346\236\220.md"
- .../iteration-1/eval-0/with_skill/timing.json
- .../iteration-1/eval-0/without_skill/grading.json
- .../iteration-1/eval-0/without_skill/timing.json
- .../iteration-1/eval-1/eval_metadata.json
- .../iteration-1/eval-1/with_skill/grading.json
- ...240\270\345\277\203\346\246\202\345\277\265.md"
- .../iteration-1/eval-1/with_skill/timing.json
- .../iteration-1/eval-1/without_skill/grading.json
- ...205\261\350\257\206\346\234\272\345\210\266.md"
- .../iteration-1/eval-1/without_skill/timing.json
- .../iteration-1/eval-2/eval_metadata.json
- ...205\245\351\227\250\346\214\207\345\215\227.md"
- .../iteration-1/eval-2/with_skill/timing.json
- .../outputs/TCP\346\217\241\346\211\213.md"
- .../iteration-1/eval-2/without_skill/timing.json
- .../iteration-1/eval-3/eval_metadata.json
- ...257\271\346\257\224\345\210\206\346\236\220.md"
- .../iteration-1/eval-3/with_skill/timing.json
- ...215\256\345\272\223\347\264\242\345\274\225.md"
- .../iteration-1/eval-3/without_skill/timing.json
- .../iteration-1/eval-4/eval_metadata.json
- ...217\221\345\261\225\345\216\206\347\250\213.md"
- .../iteration-1/eval-4/with_skill/timing.json
- .../JS\346\250\241\345\235\227\345\214\226.md"
- .../iteration-1/eval-4/without_skill/timing.json
- .../iteration-2/benchmark.json
- .../iteration-2/benchmark.md
- .../iteration-2/eval-0/with_skill/grading.json
- ...267\261\345\272\246\350\247\243\346\236\220.md"
- .../iteration-2/eval-0/with_skill/timing.json
- .../iteration-2/eval-5/with_skill/grading.json
- ...267\261\345\272\246\350\247\243\346\236\220.md"
- .../iteration-2/eval-5/with_skill/timing.json
- .agents/skills/llm-wiki/SKILL.md
- .github/workflows/llm-wiki-check.yml
- .gitignore
- .promem/promem.log
- AGENTS.md
- ...256\244\347\237\245\346\214\207\345\215\227.md"
- ...274\200\345\217\221\346\212\200\346\234\257.md"
- ...255\246\344\271\240\346\214\207\345\215\227.md"
- ...267\261\345\272\246\350\247\243\346\236\220.md"
- ...265\204\346\226\231\346\261\207\346\200\273.md"
- .../specs/2026-04-16-wiki-visual-design.md
- ...230\205\350\257\273\346\214\207\345\215\227.md"
- ...217\221\345\261\225\345\216\206\347\250\213.md"
- ...237\272\347\241\200\345\216\237\347\220\206.md"
- ...256\255\347\273\203\346\265\201\347\250\213.md"
- ...256\255\347\273\203\346\265\201\347\250\213.md"
- ...276\256\350\260\203\345\256\236\350\267\265.md"
- .../__pycache__/memory_utils.cpython-312.pyc
- ...255\246\344\271\240\346\241\206\346\236\266.md"
- ...264\257\347\247\257\346\250\241\345\274\217.md"
- ...276\204\344\270\216\346\200\273\350\247\210.md"
- ...234\272\345\210\266\350\256\276\350\256\241.md"
- ...234\215\345\212\241\350\256\276\350\256\241.md"
- ...220\206\344\270\216\350\256\272\350\257\201.md"
- ...264\250\351\207\217\346\224\271\350\277\233.md"
- ...244\226\351\203\250\347\273\274\345\220\210.md"
- llm-wiki/AGENTS.md
- llm-wiki/CLAUDE.md
- llm-wiki/LICENSE
- llm-wiki/README.md
- llm-wiki/graph/.gitkeep
- llm-wiki/graph/graph.html
- llm-wiki/graph/graph.json
- llm-wiki/purpose.md
- llm-wiki/raw/README.md
- llm-wiki/raw/agent/harness-engineering/README.md
- .../agent/harness-engineering/articles/.gitkeep
- .../anthropic-building-c-compiler-captured.html
- .../articles/anthropic-building-c-compiler.md
- ...ive-harnesses-long-running-agents-captured.html
- ...opic-effective-harnesses-long-running-agents.md
- ...r-skill-issue-harness-engineering-captured.html
- .../humanlayer-skill-issue-harness-engineering.md
- ...ance-emerging-harness-engineering-captured.html
- .../ignorance-emerging-harness-engineering.md
- ...1f4be3ad0cde990aea7ef5742a6550493d6-1799x10.jpg
- ...1b3e8e87a990f6df4c4def2b9e52815e977-2400x12.png
- ...859f5453e9481278681aa6409856d61153c-2400x12.png
- .../imgs/img-001-LangSmith-for-Startups-4.png
- .../articles/imgs/img-001-card.png
- ...-substack-post-media-s3-amazonaws-com-publi.jpg
- .../articles/imgs/img-001-og.png
- .../articles/imgs/img-001-thumbnail-jpeg.jpg
- .../articles/imgs/img-002-agent-harness-jpeg.jpg
- .../articles/imgs/img-002-gpt-6.png
- .../imgs/img-002-harness-bounded-contexts.png
- .../articles/imgs/img-002-image.gif
- .../articles/imgs/img-002-image.png
- .../img-003-harness-change-lifecycle-examples.png
- .../articles/imgs/img-003-harness-components.png
- .../articles/imgs/img-003-image-1.png
- .../articles/imgs/img-004-harness-engineering.png
- .../articles/imgs/img-004-harness-types.png
- .../articles/imgs/img-004-image-2.png
- .../articles/imgs/img-005-backwards.png
- .../articles/imgs/img-005-harness-templates.png
- .../articles/imgs/img-006-context-firewall.png
- .../articles/imgs/img-007-terminal-bench.png
- .../articles/imgs/img-008-too-many-tools.png
- .../articles/imgs/img-009-sub-agents.png
- .../articles/imgs/img-010-long-context.jpg
- .../articles/imgs/img-011-limit-case.png
- .../articles/imgs/img-012-compaction.png
- .../articles/imgs/img-013-sub-agent-telephone.png
- ...chain-anatomy-of-an-agent-harness-captured.html
- .../langchain-anatomy-of-an-agent-harness.md
- ...martin-fowler-harness-engineering-captured.html
- .../articles/martin-fowler-harness-engineering.md
- ...i-adoption-journey-step-5-harness-captured.html
- ...mitchellh-ai-adoption-journey-step-5-harness.md
- .../articles/openai-harness-engineering-zh.md
- ...parallel-what-is-an-agent-harness-captured.html
- .../articles/parallel-what-is-an-agent-harness.md
- .../philschmid-agent-harness-2026-captured.html
- .../articles/philschmid-agent-harness-2026.md
- .../raw/agent/harness-engineering/notes/.gitkeep
- .../raw/agent/harness-engineering/papers/.gitkeep
- .../raw/agent/harness-engineering/pdfs/.gitkeep
- .../raw/agent/harness-engineering/refs/.gitkeep
- .../agent/harness-engineering/transcripts/.gitkeep
- .../harness-engineering/wechat/images/img_001.png
- .../harness-engineering/wechat/images/img_002.png
- .../harness-engineering/wechat/images/img_003.png
- .../harness-engineering/wechat/images/img_004.png
- .../harness-engineering/wechat/images/img_005.png
- .../harness-engineering/wechat/images/img_006.png
- .../harness-engineering/wechat/images/img_007.png
- .../harness-engineering/wechat/images/img_008.png
- .../harness-engineering/wechat/images/img_009.png
- ...350\247\243\346\236\220-Harness-Engineering.md"
- llm-wiki/requirements.txt
- .../20260414-harness-engineering/_ae_body.txt
- .../20260414-harness-engineering/_cc_body.txt
- .../20260414-harness-engineering/_mf_body.txt
- .../_openai_zh_webfetch.md
- .../20260414-harness-engineering/candidates.md
- .../sessions/20260414-wechat-article/candidates.md
- llm-wiki/sessions/README.md
- llm-wiki/sessions/_template/candidates.md
- llm-wiki/skills/README.md
- llm-wiki/skills/baoyu-url-to-markdown/SKILL.md
- .../references/config/first-time-setup.md
- .../skills/baoyu-url-to-markdown/scripts/cdp.ts
- .../baoyu-url-to-markdown/scripts/constants.ts
- .../scripts/defuddle-converter.ts
- .../scripts/html-to-markdown.ts
- .../scripts/legacy-converter.ts
- .../skills/baoyu-url-to-markdown/scripts/main.ts
- .../scripts/markdown-conversion-shared.ts
- .../scripts/media-localizer.ts
- .../scripts/package-lock.json
- .../baoyu-url-to-markdown/scripts/package.json
- .../skills/baoyu-url-to-markdown/scripts/paths.ts
- .../scripts/vendor/baoyu-chrome-cdp/package.json
- .../vendor/baoyu-chrome-cdp/src/index.test.ts
- .../scripts/vendor/baoyu-chrome-cdp/src/index.ts
- llm-wiki/skills/collect/SKILL.md
- llm-wiki/skills/humanizer-zh/LICENSE
- llm-wiki/skills/humanizer-zh/README.md
- llm-wiki/skills/humanizer-zh/SKILL.md
- .../skills/wechat-article-to-markdown/SKILL.md
- llm-wiki/skills/wiki-writing/SKILL.md
- llm-wiki/skills/youtube-transcript/SKILL.md
- .../youtube-transcript/scripts/get_transcript.py
- llm-wiki/taxonomy.md
- llm-wiki/tools/README.md
- .../source_registry_cli.cpython-312.pyc
- llm-wiki/tools/build_graph.py
- llm-wiki/tools/check_all.sh
- llm-wiki/tools/lint_wiki.py
- llm-wiki/tools/source_record_contract.tsv
- llm-wiki/tools/source_registry.tsv
- llm-wiki/tools/source_registry_cli.py
- llm-wiki/tools/validate_source_registry.py
- .../concepts/HarnessEngineering.md
- .../agent/harness-engineering/entities/.gitkeep
- llm-wiki/wiki/agent/harness-engineering/index.md
- .../sources/anthropic-building-c-compiler.md
- ...opic-effective-harnesses-long-running-agents.md
- .../humanlayer-skill-issue-harness-engineering.md
- .../ignorance-emerging-harness-engineering.md
- .../langchain-anatomy-of-an-agent-harness.md
- .../sources/martin-fowler-harness-engineering.md
- ...mitchellh-ai-adoption-journey-step-5-harness.md
- .../sources/openai-harness-engineering-zh.md
- .../sources/parallel-what-is-an-agent-harness.md
- .../sources/philschmid-agent-harness-2026.md
- ...350\247\243\346\236\220-Harness-Engineering.md"
- .../agent/harness-engineering/syntheses/.gitkeep
- .../syntheses/harness-engineering-deep-dive.md
- llm-wiki/wiki/agent/index.md
- llm-wiki/wiki/index.md
- llm-wiki/wiki/log.md
- llm-wiki/wiki/overview.md
## 依赖变更
- `from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, DataCollatorForLanguageModeling`
- `from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training`
- `from datasets import load_dataset`
- `import torch`
- `from peft import PeftModel`
- `from peft import PeftModel`
- `import torch`
- `import {`
- `import { resolveUrlToMarkdownChromeProfileDir } from './paths.js';`
- `import { NETWORK_IDLE_TIMEOUT_MS } from './constants.js';`

## 新增的函数/类
- `步骤1 (正确) → 步骤2 (错误) → 步骤3 (基于错误结果) → ... → 结果完全错误`
- `pillar1`
- `p1_q`
- `p1_t`
- `i1`
- `harness`
- `noClasses()`
- `ma`
- `sa1`
- `sa2`

## 删除的函数/类
- `A`
- `P`
- `MCP`
- `LLM`
- `FC`
- `Skill`
- `q1`
- `q2`
- `q3`
- `q4`

## 相关注释
> **`llm-wiki/`**（与仓库根相对路径；也可单独拷贝本目录对外开源）
> **按任务追加**：Collect → `llm-wiki/skills/collect/SKILL.md` + `llm-wiki/tools/source_registry.tsv`；写成稿 → `llm-wiki/skills/wiki-writing/SKILL.md` + `llm-wiki/skills/humanizer-zh/SKILL.md`
> ## 与用户约定的流程
> # Deterministic checks for llm-wiki/ (no API keys).
> # Upstream clones used only for design reference


## 相关链接
- Commit: 4c27e7f53e9a1fa3446518d66ff4aa9ebead67b6
