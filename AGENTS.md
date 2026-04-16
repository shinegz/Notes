# My existing Agents

## LLM Wiki（Karpathy 知识库）

- 约定见 **`.agents/skills/llm-wiki/SKILL.md`** 与 **`llm-wiki/CLAUDE.md`**
- **Collect**：**`llm-wiki/skills/collect/SKILL.md`** + **`llm-wiki/tools/source_registry.tsv`**（按 **`adapter_name`** 打开 **`llm-wiki/skills/<adapter_name>/`**）
- 写成稿（concepts / syntheses / overview）：**`llm-wiki/skills/wiki-writing/SKILL.md`** + **`llm-wiki/skills/humanizer-zh/SKILL.md`**
- **知识库根目录**：**`llm-wiki/`**（按门类分架的 `raw/<shelf>/`、`wiki/<shelf>/`；Collect 先清单后落盘；工具见 `llm-wiki/tools/`）
- 上游理念：[llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent)、[llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill)、[graphify](https://github.com/safishamsi/graphify)

在 `Notes` 根目录：

```bash
export WIKI_ROOT="$PWD/llm-wiki"
pip install -r llm-wiki/requirements.txt
bash llm-wiki/tools/check_all.sh "$WIKI_ROOT"
python3 llm-wiki/tools/build_graph.py --wiki-root "$WIKI_ROOT"
```

---

<!-- ProMem Start -->
# ProMem - 项目记忆系统

ProMem 为 AI Agent 提供项目知识的自动捕获、存储、检索和进化能力。

## 记忆目录

项目记忆存储在 `.promem/memory/` 下：

| 目录 | 用途 | 更新方式 |
|------|------|----------|
| decisions/ | 技术决策记录 | 自动（post-commit 检测到依赖/接口变更） |
| bugs/ | Bug 修复记录 | 自动（post-commit 检测到 fix/bugfix） |
| rules/ | 隐式规则 | 手动（对话中发现的约束） |
| entities/ | 配置实体 | 自动（post-commit 检测到配置文件变更） |
| summaries/ | 压缩摘要 | npx promem compact 生成 |
| suggestions/ | 进化建议 | npx promem evolve 生成 |

## 自动检索协议

### 检索时机

在以下场景应自动执行检索：

| 场景 | 关键词提取策略 | 推荐内容 |
|-----|--------------|----------|
| 讨论某个模块 | 模块名 + 相关文件名 | 该模块的约束和已知 Bug |
| 遇到错误/问题 | 错误类型 + 相关技术栈 | 相关历史 Bug 和修复方案 |
| 做技术决策 | 决策领域 + 可选方案 | 历史决策和规则 |
| 修改配置/接口 | 实体名 + 配置项名 | 相关实体信息 |
| 首次接触模块 | 模块名 | 模块摘要（summaries/） |

### 检索流程

1. **检查 ProMem 是否存在**
   ```bash
   ls .promem/memory/
   ```

2. **执行检索**
   ```bash
   npx promem search "关键词"
   ```

3. **注入上下文**
   - 将检索到的知识作为上下文注入当前对话
   - 在回答时引用相关历史知识
   - 如果发现冲突或过时信息，提示用户更新

### 重要性评分

```bash
# 计算所有记忆的重要性
npx promem score --score

# 按场景推荐记忆
npx promem score --suggest --context "当前任务描述"

# 检测知识缺口
npx promem score --gaps
```

## 自动沉淀协议

### 自动沉淀（通过 Git Hooks）

Git Hooks 会在 commit 后自动分析 diff，按规则沉淀：

| 检测模式 | 目标目录 | 触发条件 |
|---------|---------|---------|
| 依赖/接口变更 | decisions/ | 检测到 package.json、API 接口等变更 |
| Bug 修复 | bugs/ | commit message 包含 fix/bugfix/修复 |
| 配置文件变更 | entities/ | 检测到配置文件变更 |

### 手动沉淀（通过对话）

当 AI 检测到以下模式时，应手动将知识写入：

| 检测模式 | 目标目录 | 示例 |
|---------|---------|------|
| "我们决定..."/"选择 X 因为..." | decisions/ | 技术选型、架构决策 |
| "这个 bug 是因为..."/"踩了个坑..." | bugs/ | 问题根因和解法 |
| "必须要..."/"不能..."/"规则是..." | rules/ | 业务约束和规则 |
| "这个接口..."/"配置是..." | entities/ | 关键实体信息 |

### 沉淀流程

1. **识别知识类型** - 根据对话内容判断属于哪个目录
2. **提取关键信息** - 从对话中提取结构化信息
3. **生成文件名** - 格式：`YYYY-MM-DD-{slug}.md`
4. **写入记忆文件** - 使用对应模板写入
5. **确认沉淀结果** - 告知用户已沉淀的内容

## Git Hooks

ProMem 通过 Git Hooks 实现自动化：

- **post-commit**: 自动分析 commit diff，按规则沉淀到 decisions/bugs/entities/
- **pre-push**: 推送前自动检查记忆完整性
- **post-merge**: 合并后自动重建索引

安装 Git Hooks：
```bash
npx promem hooks
```

## Evolve 工作流

进化系统用于分析记忆中的重复模式，提炼出通用规则：

1. **检查进化建议**
   ```bash
   npx promem evolve --check
   ```

2. **审核建议** - 建议自动保存到 `memory/suggestions/`，状态为 `pending`

3. **应用建议**
   ```bash
   npx promem evolve --apply SUG-001
   ```

4. **查看历史**
   ```bash
   npx promem evolve --history
   ```

## 命令参考

| 命令 | 用途 |
|------|------|
| `npx promem search "关键词"` | 搜索记忆 |
| `npx promem capture` | 从 Commit 捕获 |
| `npx promem compact --category decisions` | 压缩指定类别记忆 |
| `npx promem compact --all` | 压缩所有记忆 |
| `npx promem evolve --check` | 检查进化建议 |
| `npx promem evolve --apply SUG-001` | 应用指定建议 |
| `npx promem score --score` | 计算重要性评分 |
| `npx promem hooks` | 安装 Git Hooks |
| `npx promem search --rebuild` | 重建搜索索引 |

## 记忆文件模板

### decisions/ - 技术决策

```markdown
# [决策]: {简短描述}

## 日期
{YYYY-MM-DD}

## 背景
{为什么需要做这个决策}

## 决策
{具体决定了什么}

## 原因
{为什么这样决定}

## 影响范围
{影响哪些模块/功能}
```

### bugs/ - 问题与解法

```markdown
# [Bug]: {简短描述}

## 日期
{YYYY-MM-DD}

## 症状
{表现出什么问题}

## 根因
{根本原因}

## 解法
{如何修复}

## 预防
{如何避免再次发生}
```

### rules/ - 业务规则

```markdown
# [规则]: {简短描述}

## 日期
{YYYY-MM-DD}

## 规则内容
{具体规则是什么}

## 原因
{为什么有这个规则}

## 适用范围
{在什么场景下适用}
```

### entities/ - 实体信息

```markdown
# [实体]: {实体名称}

## 类型
{接口/配置/模块/服务}

## 描述
{实体的用途和职责}

## 关键属性
{重要的配置项/字段/参数}

## 关联
{与其他实体的关系}
```

## 注意事项

1. **非侵入式** - 沉淀动作应该自然融入对话，不要频繁打断用户
2. **确认重要决策** - 对于重大决策，先确认再沉淀
3. **避免重复** - 沉淀前检索是否已有类似记录
4. **尊重用户意图** - 如果用户明确表示不需要记录，不要强制沉淀

<!-- ProMem End -->
