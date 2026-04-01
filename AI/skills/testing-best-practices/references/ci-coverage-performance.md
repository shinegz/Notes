# 覆盖率、CI 集成、性能测试与测试重构

本文档涵盖测试的运维方面——如何衡量效果、集成到 CI/CD、处理性能问题以及改进现有测试套件。当测试计划涉及覆盖率分析、CI 流水线设置、性能测试或用户想改进现有测试套件时加载此参考。

> **通用测试原则**（黄金法则、AAA 模式、三元命名法、黑盒测试）见 `SKILL.md`，适用于所有测试类型。

---

## 目录

- [覆盖率分析](#覆盖率分析)
- [变异测试](#变异测试)
- [测试代码检查](#测试代码检查)
- [CI 集成](#ci-集成)
- [性能测试](#性能测试)
- [测试重构](#测试重构)

---

## 覆盖率分析

代码覆盖率衡量测试期间执行了哪些行/分支/函数。它是有用的信号但不是目标本身。

### 覆盖率作为诊断，不是目标

高覆盖率不代表测试好。你可以用不断言任何东西的测试达到 100% 行覆盖率。相反，70% 覆盖率加上强行为断言比 100% 覆盖率加弱断言更有价值。

**使用覆盖率找盲点**，而不是追求数字。最有用的覆盖率指标是分支覆盖率——它显示哪些决策路径未测试。

### 实用覆盖率指导

**在覆盖率报告中找什么：**
- 未覆盖的错误处理——catch 块、错误回调、回退路径
- 未覆盖的条件分支——else 子句、default case、提前返回
- 未测试的边界情况——代码处理但测试未执行的边界值
- 死代码——任何东西都到达不到的行（也许应该删除）

**覆盖率阈值**（作为指导，不是规则）：
- **关键业务逻辑**（支付、认证、数据验证）：目标 90%+ 分支覆盖率
- **API 端点 / 控制器**：80%+——覆盖所有响应路径
- **UI 组件**：70%+——覆盖渲染和关键交互，不追求快照覆盖率
- **工具函数**：90%+——这些容易彻底测试
- **生成代码、配置、类型定义**：从覆盖率中排除

**经验法则**：80% 是一个不错的起点。过低的覆盖率意味着信心不足，追求 100% 则投入产出比低。

> 参考：Martin Fowler 建议 "in the upper 80s or 90s"

### 配置覆盖率

大多数测试框架支持覆盖率配置：
- **Include/exclude 模式**：聚焦你的代码，不是 node_modules 或生成文件
- **按目录设置阈值**：对关键路径设更高阈值，UI 设更低
- **CI 中的覆盖率**：在 PR 中报告覆盖率但不单独阻止合并——一个减少覆盖率的有意义测试（通过删除坏测试）是净正面

### 有效改进覆盖率

当被要求改进覆盖率时，不要只是写触及未覆盖行的测试。相反：

1. 阅读未覆盖代码
2. 理解它代表什么行为
3. 问："如果这段代码坏了，有人会注意吗？会出什么问题？"
4. 写一个验证那个行为的测试——覆盖率增加是副作用

---

## 变异测试

传统覆盖率衡量测试**执行了**哪些代码，但不衡量测试是否**真正验证了**什么。

### 问题：高覆盖率 ≠ 好测试

```ts
// 100% 行覆盖率，0% 实际验证
function addNewOrder(newOrder) {
  logger.log(`Adding new order ${newOrder}`);
  DB.save(newOrder);
  Mailer.sendMail(newOrder.assignee, `A new order was placed`);
  return { approved: true };
}

it('Test addNewOrder', () => {
  addNewOrder({ assignee: 'john@example.com', price: 120 });
  // 没有任何断言！但覆盖率是 100%
});
```

### 变异测试原理

变异测试工具（如 [Stryker](https://stryker-mutator.io/)）通过以下方式验证测试质量：

1. **植入变异** ——有意修改代码，引入 bug
   ```ts
   // 原代码
   if (price > 0) { ... }
   // 变异后
   if (price >= 0) { ... }
   ```

2. **运行测试** ——如果测试全部通过，说明变异"存活"（测试未发现 bug）

3. **统计结果** ——被杀死的变异比例 = 测试真正有效性

### Stryker 使用示例

```bash
# 安装
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner

# 运行变异测试
npx stryker run
```

**Stryker 报告解读：**
- **Killed**：测试发现变异 ✅
- **Survived**：测试未发现变异 ⚠️（需要增强测试）
- **Timeout**：变异导致无限循环（也是一种 bug 发现）

### 何时使用变异测试

| 场景 | 价值 |
|------|------|
| 关键业务逻辑 | ⭐⭐⭐ 高价值 - 确保测试真正有效 |
| 安全相关代码 | ⭐⭐⭐ 高价值 - 验证安全测试覆盖 |
| 复杂算法 | ⭐⭐ 中价值 - 发现边界情况 |
| 简单 CRUD | ⭐ 低价值 - 投入产出比不高 |

---

## 测试代码检查

测试代码也需要质量检查。测试代码的 bug 会带来错误信心或遗漏真实问题。

### Test Linter 插件

**eslint-plugin-jest** —— Jest 测试最佳实践检查：

```ts
// 检测：测试没有断言
it('should return something', () => {
  // error: Test has no assertions
});

// 检测：测试被跳过
it.skip('todo', () => { ... }); // error: Skipped test encountered

// 检测：断言过于宽松
expect(result).toBeTruthy(); // warning: Use more specific assertion
```

**eslint-plugin-mocha** —— Mocha 测试最佳实践检查：

```ts
// 检测：全局测试（应在 describe 内）
it('standalone test', () => { ... }); // error: No global tests

// 检测：重复的测试标题
it('duplicate name', () => {});
it('duplicate name', () => {}); // error: No duplicate test titles
```

### 测试坏味道检测

```ts
// ❌ 被 linter 捕获的问题
describe('Too short', () => {
  const token = getDefaultToken(); // error: No setup in describe
  
  it('Some test', () => {}); // error: Test description too short
});

it.skip('Skipped', () => {}); // error: No skipped tests

it('Test name', () => {
  expect('value'); // error: No assertion
});
```

### 配置测试 Linter

```json
// .eslintrc.json
{
  "overrides": [
    {
      "files": ["**/*.test.ts", "**/*.spec.ts"],
      "plugins": ["jest"],
      "extends": ["plugin:jest/recommended"],
      "rules": {
        "jest/no-disabled-tests": "error",
        "jest/no-focused-tests": "error",
        "jest/no-identical-title": "error",
        "jest/prefer-to-have-length": "warn",
        "jest/valid-expect": "error"
      }
    }
  ]
}
```

---

## CI 集成

测试只有在一致运行时才有价值。CI 集成确保每次变更都运行测试，失败被早期捕获。

### 测试用例标签与分类

不同测试需要在不同场景执行：快速冒烟、完整集成、E2E 验证等。使用标签分类测试，按需执行子集。

**标签命名约定：**

| 标签 | 含义 | 执行时机 |
|------|------|----------|
| `#cold` | 无 I/O 的快速测试 | 开发时频繁执行 |
| `#sanity` | 基本功能验证 | 每次 commit |
| `#api` | API 端点测试 | PR 合并前 |
| `#integration` | 集成测试 | CI 流水线 |
| `#e2e` | 端到端测试 | 部署前 |
| `#slow` | 耗时测试 | 夜间构建 |

**使用方式：**

```ts
// 在测试名称或 describe 中使用标签
describe('Order service', function() {
  describe('Add new order #cold-test #sanity', function() {
    it('When no currency supplied, use default currency #sanity', function() {
      // 测试逻辑
    });
  });
});
```

**按标签执行：**

```bash
# Mocha - 只执行 sanity 测试
mocha --grep 'sanity'

# Jest - 使用 test.each 或自定义逻辑
jest --testNamePattern='sanity'

# 跳过慢测试
mocha --grep 'sanity|cold' --invert
```

**好处：**
- 开发者保存文件时只跑快速测试（秒级反馈）
- PR 提交时跑完整测试套件
- 避免因等待慢测试而跳过运行测试

### 测试流水线设计

**快速反馈循环：**
```
Commit → Lint + Type check (seconds)
       → Unit tests (seconds to low minutes)
       → Integration tests (minutes)
       → E2E tests (minutes to tens of minutes)
```

先运行快检查。快失败。不要让开发者等 20 分钟才发现类型错误。

**并行化：**
- 跨 worker 分割单元测试（大多数框架原生支持）
- 按 CI 容器跨文件分割 E2E 测试
- 对大型套件使用 test sharding
- 在运行间缓存依赖

### CI 特定测试关注点

**确定性环境**：锁定依赖版本。使用 lockfiles。指定确切 Node/Python/Go 版本。"在我机器上能用"不可接受。

**超时处理**：在测试级和作业级设置合理超时。挂起的测试应该失败，不是永远阻塞流水线。

**产物收集**：失败时，收集截图（E2E）、覆盖率报告、测试日志。这些对调试 CI 失败至关重要。

**数据库 setup**：使用 test containers 或 CI 提供的服务。永远不要从 CI 测试共享/staging 数据库。

**密钥管理**：测试配置不应包含真实 API 密钥。使用 mock 外部服务或具有最小权限的测试专用凭证。

### Pull Request 集成

- **在 PR 中报告测试结果**：显示哪些测试通过/失败、覆盖率差异
- **必需检查**：单元测试和 lint 应该在合并前必须通过
- **可选检查**：如果 E2E 测试 flaky，可以是建议性（不阻塞）的，但要努力让它们可靠
- **覆盖率评论**：显示覆盖率增量——PR 在增加还是减少覆盖率？新代码有覆盖吗？

---

## 性能测试

性能测试验证代码满足速度和资源要求。它是不同于功能测试的学科但共享工具和基础设施。

### 何时包含性能测试

- 用户提到延迟要求（"必须在 200ms 内响应"）
- 功能处理大数据集（排序、过滤、渲染长列表）
- 代码路径频繁运行（热循环、每请求中间件）
- 类似功能以前报告过性能问题
- 功能涉及渲染许多 UI 元素（虚拟滚动、大表）

### 性能测试类型

**微基准测试**：在隔离中为特定函数/操作计时。用于比较方法或检测回归。
- 运行多次迭代（1000+）并使用统计分析（中位数、P95、P99）
- 注意 JIT 预热、GC 暂停、CPU throttling
- 与基线比较，而非绝对数字

**负载测试**：对 API 模拟并发用户/请求。测量吞吐量、负载下延迟和断点。
- 工具：k6、Artillery、Locust、Gatling
- 定义场景：典型负载、峰值负载、持续负载
- 测量：响应时间（P50、P95、P99）、错误率、吞吐量（req/s）

**前端性能测试**：测量渲染时间、bundle 大小、交互响应性。
- Lighthouse CI 用于自动化审计
- 组件测试中的性能 marks/measures
- Bundle 大小跟踪（bundlesize、size-limit）

### CI 中的性能测试

- 在一致硬件上运行基准（CI runner 变化——使用专用或校准过的 runner）
- 与以前结果比较，而非绝对阈值（硬件变化）
- 对显著回归告警（>10% 降级）
- 存储结果随时间用于趋势分析

### 编写性能断言

对绝对时序断言要谨慎——它们依赖环境。优先：

- **相对断言**："新实现应该不比基线慢超过 10%"
- **复杂度断言**："处理 10x 更多项应该花不到 10x 更多时间（次线性）"
- **资源断言**："10k 项数据集的内存使用不应超过 100MB"

---

## 测试重构

改进现有测试套件与编写新测试同等重要。坏测试拖慢开发、制造错误信心、浪费 CI 资源。

### 何时重构测试

- **向有质量问题的文件添加新测试前**——先改进基础
- **测试因不相关变更频繁破坏时**——它们在测试实现
- **测试套件太慢时**——profile 并优化
- **开发者因不信任结果而跳过运行测试时**
- **功能重构期间**——更新测试以匹配新架构

### 常见重构模式

**提取测试 helper**：重复的 setup 代码 → 工厂函数、自定义 matcher 或测试工具。

**拆分大测试文件**：有 50+ 测试的文件 → 按行为组拆分到独立文件。每个文件应该独立可理解。

**用断言替换快照**：不断破坏的大型快照测试 → 对重要的属性进行针对性断言。

**升级 mock 策略**：如果测试 mock 太多（测试不到真实东西）或太少（因真实依赖而 flaky），调整 mock 边界。

**移除冗余测试**：如果单元测试和集成测试验证同一行为，集成测试通常更有价值。考虑移除单元测试。

**修复测试命名**：重命名模糊测试名以描述行为。这也迫使你思考测试实际验证什么。

**添加缺失测试**：覆盖率报告突出缺口。聚焦未测试的错误路径和边界条件，不是增加数字。

> **测试债务优先级**见 `test-quality.md` 中的「测试坏味道与重构」章节。

---

## 总结

测试运维的关键要素：
1. **覆盖率是诊断工具**——使用它找缺口，不是追数字
2. **CI 确保一致性**——自动化运行，快速反馈
3. **性能测试匹配需求**——验证关键路径满足要求
4. **测试债务有优先级**——先修复 flaky 和慢测试
5. **持续改进**——定期重构测试以保持可维护性
