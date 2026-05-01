# 测试质量：Mock 策略、隔离与可维护性

本文档涵盖编写可靠、可维护且真正有用的测试的技巧。当测试计划涉及复杂 mock、测试数据问题或现有测试代码有质量问题时加载此参考。

> **通用测试原则**（黄金法则、AAA 模式、三元命名法、黑盒测试）见 `SKILL.md`，适用于所有测试类型。

---

## 目录

- [Mock 策略](#mock-策略)
- [Stub vs Spy vs Mock 选择指南](#stub-vs-spy-vs-mock-选择指南)
- [测试数据管理](#测试数据管理)
- [使用真实数据：Faker.js](#使用真实数据fakerjs)
- [测试隔离](#测试隔离)
- [测试组织与命名](#测试组织与命名)
- [测试可维护性](#测试可维护性)
- [测试坏味道与重构](#测试坏味道与重构)

---

## Mock 策略

Mock 是测试中最强大但也最被滥用的工具。正确的 mock 使测试聚焦和快速。错误的 mock 使测试毫无意义。

### 何时 Mock

- **外部服务**（API、数据库、文件系统、邮件）——你不控制它们，且它们在测试中慢/不可靠
- **非确定性来源**（时钟、随机、UUID）——你需要可复现的输出
- **昂贵操作**（重计算、文件 I/O）——仅当速度重要时
- **难以自然触发的错误条件**（网络超时、磁盘满、竞态条件）

### 何时不 Mock

- **被测对象本身。**这听起来明显但确实发生——mock 一个方法然后断言 mock 被调用。你什么都没测试。
- **简单协作者。**如果工具函数快、纯且稳定，直接用真实的。Mock 它增加复杂性而无价值。
- **框架内部。**不要 mock React 的 useState、Express 的 req/res（使用真实请求对象）、Python 内置类型。

### Mock 层级（从最优先到最不优先）

1. **Stub / Fake**：返回预配置数据的简单实现。易于理解。
   ```ts
   const getUser = () => ({ id: 1, name: 'Test User' })
   ```

2. **Spy on 真实实现**：让真实代码运行但也跟踪调用。当你想验证交互 AND 真实行为时有用。

3. **带行为验证的完整 Mock**：完全替换依赖并断言它被正确调用。当交互 IS 行为时使用（如"点击保存应该用表单数据调用 API"）。

4. **自动 Mock（框架生成）**：测试框架从模块类型签名创建 mock。方便但不透明——你看不到 mock 返回什么，可能导致测试因错误原因通过。

### Mock 范围

保持 mock 尽可能靠近测试。mock 范围越大，越模糊测试实际测试什么。

**优先：**
- 在测试函数内 mock——可见且作用域明确
- 在 `beforeEach` 中 mock——共享 setup、清晰生命周期

**避免：**
- 影响文件中所有测试的全局模块 mock——难以为特定情况覆盖
- 影响整个套件的测试 setup 文件中的 mock——不可见副作用

### 网络 Mock

对于测试发出 HTTP 请求的代码，优先在 network 层 mock 而非函数层 mock。

**网络层 Mock**（MSW、nock、WireMock、responses）：拦截实际 HTTP 请求。代码执行真实 fetch/axios/requests 路径。捕获 headers、序列化、URL 构造问题。

**函数层 Mock**（jest.mock('axios')）：完全替换 HTTP 客户端。更快、更简单，但错过代码如何调用客户端的 bug。

集成测试使用网络层 mock，隔离的单元测试才使用函数层 mock。

---

## Stub vs Spy vs Mock 选择指南

| 类型 | 定义 | 用途 | 示例 |
|------|------|------|------|
| **Stub** | 返回预配置数据的简单实现 | 隔离依赖、提供固定响应 | `const getUser = () => ({ id: 1 })` |
| **Spy** | 包装真实实现、记录调用 | 验证调用同时执行真实逻辑 | `jest.spyOn(api, 'fetch').mockImplementation(...)` |
| **Mock** | 完全替换、行为验证 | 验证交互模式 | `jest.fn().mockReturnValue(...)` |

### 决策原则

- 只需要返回值？→ **Stub**
- 需要验证调用但也要真实行为？→ **Spy**
- 验证交互模式是测试目标？→ **Mock**

### 示例对比

```ts
// Stub - 只提供数据
const userStub = {
  get: () => ({ id: 1, name: 'Test User' })
};

// Spy - 跟踪并执行真实逻辑
jest.spyOn(userService, 'fetchUser');

// Mock - 完全控制并验证
const mockApi = {
  fetchUser: jest.fn().mockResolvedValue({ id: 1 })
};

// 测试中验证
expect(mockApi.fetchUser).toHaveBeenCalledWith(1);
```

---

## 测试数据管理

好的测试数据足够真实以捕获真实 bug、足够最小以可读、足够隔离以不产生干扰。

### 方法

**内联数据** ——直接在测试中定义测试数据。适合数据本身就是测试场景的情况。

```ts
// 好：测试特定输入/输出的函数
test('formats price with currency symbol', () => {
  expect(formatPrice(100, 'USD')).toBe('$100.00');
});
```

**工厂函数** ——产生有合理默认值且可覆盖字段的测试对象的函数。复杂测试数据的首选模式。

```ts
// 好的工厂函数
function createUser(overrides = {}) {
  return {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    ...overrides
  };
}

// 使用
const admin = createUser({ role: 'admin' });
```

**Fixtures / Seed 文件** ——测试前加载的静态数据文件（JSON、SQL）。最适合只读参考数据。

```ts
// 适合：对已知数据集测试（如产品目录）
// 不适合：测试需要修改数据——fixtures 变成共享可变状态
```

**Builder** ——逐步构造复杂对象的链式 API。当对象构造有约束或依赖时有用。

```ts
// 适合：对象有复杂验证或相互依赖字段
const user = new UserBuilder()
  .withRole('admin')
  .withOrg(organization)
  .build();
```

### 使用真实数据：Faker.js

生产环境中的 bug 通常出现在特殊或意外的输入下。使用 "foo"、"test" 等假数据可能无法暴露真实问题。

**问题示例**：

```ts
// ❌ 假数据通过测试，但隐藏真实 bug
const addProduct = (name, price) => {
  const productNameRegexNoSpace = /^\S*$/; // 不允许空格
  if (!productNameRegexNoSpace.test(name)) return false;
  return true;
};

test('When adding new product, get successful confirmation', () => {
  const result = addProduct('Foo', 5); // 'Foo' 永远通过
  expect(result).toBe(true);
  // 正面假阴性：从未测试过带空格的长产品名
});
```

**解决方案**：使用 Faker 生成真实格式的随机数据。

```ts
import faker from 'faker';

it('When adding new valid product, get successful confirmation', () => {
  const result = addProduct(
    faker.commerce.productName(), // 如 'Sleek Cotton Computer'
    faker.random.number({ min: 1, max: 10000 })
  );
  // 随机输入可能触发未预料的路径，发现隐藏 bug
  expect(result).toBe(true);
});
```

**Faker 常用场景**：

```ts
// 用户数据
faker.name.findName()        // 'John Doe'
faker.internet.email()       // 'john.doe@example.com'
faker.phone.phoneNumber()    // '1-555-123-4567'

// 商业数据
faker.commerce.productName() // 'Awesome Steel Chair'
faker.finance.amount()       // '1234.56'
faker.address.city()         // 'San Francisco'

// 时间数据
faker.date.past()            // 过去的日期
faker.date.future()          // 未来的日期
faker.time.recent()          // 最近的时间戳
```

**可复现性**：使用 seeded randomness 保证测试可复现。

```ts
// 设置种子以复现结果
faker.seed(123);
const name1 = faker.name.findName(); // 每次运行结果相同
```

### 原则

**最小数据。**只包含测试相关的字段。测试"用户登录"不需要用户邮政地址。多余字段是噪音。

**真实数据。**使用真实格式和值。用户名"test"可能隐藏真实名称出现的 bug（unicode、空格、很长）。Faker 这样的库有帮助，但使用 seeded randomness 保证可复现。

**无共享可变数据。**如果测试 A 修改共享 fixture，测试 B 会间歇性失败。每个测试应创建或接收自己的数据。

**命名魔法值常量。**如果测试使用数字 42，那是期望年龄、项目计数还是只是随机数？命名它。

---

## 测试隔离

每个测试必须独立——应该能单独通过、首先运行、最后运行或并行运行。

### 耦合来源（及修复）

| 耦合来源 | 修复 |
|---------|------|
| 共享数据库记录 | 每个测试创建自己的数据，或使用事务回滚 |
| 全局变量 | 在 beforeEach/afterEach 中重置，或避免全局 |
| 单例服务 | 使用依赖注入，在测试间重置状态 |
| 文件系统副作用 | 使用临时目录，在 afterEach 中清理 |
| 时钟依赖 | 使用 fake timers，注入时钟 |
| 模块级副作用 | 延迟初始化，或 jest.isolateModules |
| 环境变量 | 在 beforeEach/afterEach 中保存和恢复 |
| 共享 mock | 在测试间重置 mock（jest.restoreAllMocks） |

### 并行安全

对于并行运行的测试（大多数框架默认）：
- 无共享文件、端口或数据库记录
- 无对执行顺序的依赖
- 每个测试运行使用唯一标识符（追加测试名或随机后缀到资源名）
- 注意控制台输出——并行测试交错输出

---

## 测试组织与命名

### 文件结构

遵循项目现有约定。常见模式：

**Co-located**：测试放在源文件旁边。
```
src/
├── utils/
│   ├── format.ts
│   └── format.test.ts
```

**独立测试目录**：测试在 `tests/` 或 `__tests__/` 目录中镜像源码树。
```
src/utils/format.ts
tests/utils/format.test.ts
```

**混合**：单元测试 co-located，集成/E2E 在独立目录。

无论项目使用哪种模式——遵循它。一致性比任何特定约定都重要。

### Describe/it 结构

按被测单元组织测试，然后按行为类别。

```
describe('ShoppingCart')
  describe('addItem')
    it('should add a new item to the cart')
    it('should increment quantity if item already exists')
    it('should throw if item is out of stock')
  describe('removeItem')
    it('should remove the item from the cart')
    it('should do nothing if item is not in cart')
  describe('getTotal')
    it('should sum all item prices × quantities')
    it('should return 0 for empty cart')
    it('should apply discount if coupon is valid')
```

> **测试命名规范**见 `SKILL.md` 中的「三元命名法」章节。

---

## 测试可维护性

测试是代码。它们需要和生产代码同样的关注——有时更多，因为维护不良的测试变得主动有害（慢、flaky、误导）。

### 保持测试 DRY——但要小心

在生产代码中，DRY 几乎总是好的。在测试中，可读性有时胜过 DRY。测试应该从上到下阅读就能理解，不需要跳到共享 helper。

**提取共享 setup** 当它确实在测试间相同时。但如果提取使测试更难理解，复制几行代替。

**Helper 函数**应该描述它们创建什么，而不是如何创建。`createAuthenticatedUser()` 比 `setupTestStep1()` 更好。

### 避免测试库锁定

编写不深度依赖一个断言库 API 的测试。核心逻辑（arrange、act、assert）应该清晰，无论你使用 Jest、Vitest、Mocha 还是 PyTest。

### 随代码更新测试

当功能改变时，先更新其测试（或至少同时）。过时的测试比没有测试更糟——它们通过但不验证当前行为，给人错误信心。

---

## 测试坏味道与重构

### 坏味道与补救

**慢测试**：Profile 找瓶颈。通常是不必要的 I/O、缺少 mock 或可以共享（如果是只读）的 setup。

**Flaky 测试**：系统性追踪 flaky 测试。对每一个：重现 flake、找到非确定性来源、修复它。常见来源：时序、共享状态、未控制的随机。

**脆弱测试**：每次重构都破坏但仍通过真实 bug。通常测试实现细节。重写以测试行为。

**晦涩测试**：阅读时无法理解测试什么。添加描述性名称、简化 setup、使用有意义的 helper 函数名。

**巨型测试**：一个测试文件有 50+ 测试用例和 500+ 行。按行为组拆分到独立文件。考虑是否某些测试属于不同层级（单元 vs 集成）。

**注释掉的测试**：要么修复要么删除。死测试不提供价值且增加困惑。

**从不失败的测试**：如果测试从未在生产中失败且从未捕获 bug，质疑它是否测试任何有意义的东西。它可能平凡地为真。

### 测试债务优先级

不是所有测试债务都相等。优先处理：

1. **Flaky 测试**——它们侵蚀对整个套件的信任。立即修复或隔离。
2. **慢测试**——它们拖慢每个人的工作流。Profile 并优化。
3. **关键路径缺少测试**——为代码添加测试，如果损坏会造成真实用户影响。
4. **脆弱测试**——每次重构都破坏的测试。重写以测试行为。
5. **死测试**——注释掉或禁用的测试。删除或修复。
6. **低价值测试**——从不失败且从未捕获 bug 的测试。考虑删除以减少维护。
