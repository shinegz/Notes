# 单元测试策略与最佳实践

本文档提供单元测试的深入指导。当测试计划包含单元测试时加载此参考。

---

## 目录

- [核心哲学](#核心哲学)
- [业务叙事式命名规则](#业务叙事式命名规则)
- [文件头 JSDoc 规范](#文件头-jsdoc-规范)
- [什么构成好的单元](#什么构成好的单元)
- [测试纯函数](#测试纯函数)
- [测试组件 (UI)](#测试组件-ui)
- [测试状态管理](#测试状态管理)
- [测试 API/服务层](#测试-api服务层)
- [边界值分析](#边界值分析)
- [错误断言最佳实践](#错误断言最佳实践)
- [快照测试策略](#快照测试策略)
- [基于属性的测试](#基于属性的测试)
- [何时选择单元测试](#何时选择单元测试)
- [常见反模式](#常见反模式)
- [BDD 风格断言最佳实践](#bdd-风格断言最佳实践)
- [其他测试习惯](#其他测试习惯)

---

## 核心哲学

单元测试验证最小有意义行为单元的隔离性。关键词是"行为"——不是"函数"或"方法"。单元由它为消费者做什么来定义，而不是由其实现结构定义。

**好的单元测试回答这个问题**："如果我改变实现但保持相同行为，这个测试还能通过吗？"如果答案是否定的，说明测试过度耦合实现细节。

**单元测试也是活的规格。** 未来的开发者或 Agent 阅读测试文件时，必须能够重构功能的业务规则而无需阅读源码。测试名称、`describe` 块名称和文件级 JSDoc 头共同构成人类可读 + Agent 可读的规格。

> **通用测试原则**（黄金法则、AAA 模式、三元命名法、黑盒测试）见 `SKILL.md` 中的「通用测试原则」章节，适用于所有测试类型。

---

## 业务叙事式命名规则

测试名称即规格。它们必须传达：
1. **属于哪个功能上下文**（`describe` 中的 `[Feature]` 前缀）
2. **验证什么业务规则**（不是调用哪个函数）
3. **期望什么结果**（Given/When/Then 或等效形式）

### 反模式 vs 正确模式

| 反模式（实现导向） | 正确做法（业务叙事） |
|---|---|
| `it('returns correct object')` | `it('首次进入创建页：活动名称自动生成，前缀为 Sponsored_Max-product_campaign_')` |
| `it('works correctly')` | `it('默认为长期活动：结束日期为 3020-12-30（无过期哨兵值）')` |
| `describe('extractBiddingData')` | `describe('[AM Campaign] 从 OnePage 卡片数据中提取出价信息')` |
| `it('handles TROI type')` | `it('TROI 出价类型：maxBid 设为 -1（不限制消耗，无上限）')` |
| `it('V2 adds rapid boost')` | `it('V2 参数：添加 _rapid_boost_switch 字段用于快速提升资格')` |

### describe 块模式

```ts
/**
 * 业务规则：[一句话描述规则]
 */
describe('[功能名] [组件或行为组]', () => {
  it('[给定上下文] [操作或条件] [期望结果]', () => {
    // Arrange: 设置最小测试数据
    // Act: 调用单元
    // Assert: 验证业务结果（魔法值加注释）
    expect(result.endDate).toBe('3020-12-30') // 哨兵值：长期活动/无过期
    expect(result.autoCreative).toBe(1) // 1 = 启用；业务默认值
  })
});
```

### 魔法值行内注释

测试期望使用魔法值时，必须添加行内注释说明其业务含义：

```ts
// ❌ 不好:
expect(result.maxBid).toBe(-1)

// ✅ 好:
expect(result.maxBid).toBe(-1) // -1 = 无出价上限（不限制消耗），用于 TROI/BCB 类型
```

---

## 文件头 JSDoc 规范

每个单元测试文件必须以 JSDoc 文件头开头，同时记录：功能归属、迭代信息、需求单号、业务规则。

### 标准模板

```ts
/**
 * @feature   功能名称（中文，与产品需求一致）
 * @module    被测文件的相对路径（从 src/ 开头）
 * @iteration 迭代名称（与 O2 迭代标题一致）
 * @ticket    需求单号（Aone / JIRA 等）
 * @since     首次交付日期（YYYY-MM-DD）
 * @purpose   本文件的测试目的一句话总结
 *
 * 本文件覆盖的业务规则：
 *   - 规则 1：具体描述，包含魔法值的业务含义
 *   - 规则 2：...
 *
 * 不看源码如何还原功能：
 *   自上而下阅读 describe() 和 it() 名称，即得完整功能规格。
 */
```

### 字段填写规则

| 字段 | 是否必填 | 说明 |
|------|--------|------|
| `@feature` | 必填 | 与产品需求文档中功能名称一致 |
| `@module` | 必填 | 被测源文件路径，便于 Agent 定位 |
| `@iteration` | 必填 | O2 / 迭代管理工具中的迭代标题 |
| `@ticket` | 必填 | 需求单号；查不到填 `N/A` |
| `@since` | 必填 | 首次建立此测试文件的日期 |
| `@purpose` | 必填 | 一句话，说清"这个模块在业务上做什么" |
| 业务规则列表 | 必填 | 测试文件覆盖的每条规则，一条一行 |

---

## 什么构成好的单元

**测试契约，而不是实现。** 对于一个排序列表的函数，测试输出已排序——不要测试它内部使用快速排序。

**每个测试一个逻辑断言。** 这不意味着字面上一个 `expect()` 调用——而是每个测试验证一个连贯的行为。在一个测试中同时断言函数返回值和类型是可以的。断言不相关的行为则不行。

**快速。** 单元测试超过 50ms 就有异味。不要网络调用、文件系统、数据库。如果需要这些，那是集成测试。

**确定性。** 相同输入 → 相同结果，每次都一样。不依赖系统时钟、随机值或全局状态，除非显式控制。

---

## 测试纯函数

纯函数最容易测试——给定输入，验证输出。

### 策略

1. **黄金路径**开始——典型有效输入产生预期输出
2. **错误输入**——null、undefined、empty、错误类型会怎样？
3. **边界值**——零、负数、最大整数、空字符串、单字符
4. **等价类**——如果函数处理范围（1-10, 11-20），从每个范围测试一个值加边界

> 边界值详细清单见下文「边界值分析」章节。

---

## 测试组件 (UI)

组件测试验证组件正确渲染并按预期响应用户交互。

### 测试什么

- 给定有效 props 时无崩溃渲染
- 不同 prop 组合的正确输出
- 用户事件（click、input、submit）触发正确的回调或状态变化
- 条件渲染——基于 state 或 props 显示/隐藏元素
- 可访问性——正确的角色、标签、aria 属性

### 不测试什么

- 内部状态实现——测试用户看到的，不是 useState 的值
- CSS 样式细节——除非它们代表行为（可见性、禁用状态）
- 第三方库内部——不要测试日期选择器库是否工作
- 子组件的实现细节——从消费者角度测试

### UI 与功能分离

测试组件逻辑时，UI 细节是噪音。通过提取数据，降低与图形实现的耦合。

```ts
// ✅ 推荐：分离 UI 细节，只测试数据
test('When users-list shows only VIP, should display only VIP members', () => {
  // Arrange
  const allUsers = [
    { id: 1, name: 'Yoni Goldberg', vip: false },
    { id: 2, name: 'John Doe', vip: true }
  ];

  // Act
  const { getAllByTestId } = render(<UsersList users={allUsers} showOnlyVIP={true} />);

  // Assert - 从 UI 提取数据，然后比较数据
  const allRenderedUsers = getAllByTestId('user').map(el => el.textContent);
  const allRealVIPUsers = allUsers.filter(u => u.vip).map(u => u.name);

  expect(allRenderedUsers).toEqual(allRealVIPUsers);
  // 比较数据与数据，没有 UI 细节
});

// ❌ 反模式：混杂 UI 细节和数据
test('shows only VIP members', () => {
  const { getAllByTestId } = render(<UsersList users={allUsers} showOnlyVIP={true} />);

  expect(getAllByTestId('user')).toEqual('[<li data-test-id="user">John Doe</li>]');
  // 耦合了具体 HTML 结构
});
```

### 元素查询最佳实践

使用不易受图形变更影响的属性查询元素。

**优先级顺序：**

1. **语义属性**（首选）：角色、标签文本、占位符文本
2. **test-id**（次选）：专用测试属性
3. **CSS 类/ID**（避免）：易受样式变更影响

```ts
// ✅ 首选：通过语义属性查询
const submitBtn = getByRole('button', { name: /提交/i });
const emailInput = getByLabelText(/邮箱/i);

// ✅ 次选：使用专用 test-id
const userElement = getByTestId('user-name');

// ❌ 避免：依赖 CSS 类
const element = container.querySelector('.d-flex-column'); // 设计变更会破坏测试
```

**创建 test-id：**

```tsx
// 组件代码
<span data-test-id="errorsLabel">{value}</span>

// 测试代码
expect(getByTestId('errorsLabel').textContent).toBe("0");
```

### 真实渲染 vs Shallow Render

只要大小合适，像用户那样从外部完全渲染组件。

```ts
// ✅ 推荐：真实渲染的组件测试
test('When clicked to show filters, filters are displayed', () => {
  const wrapper = mount(<Calendar showFilters={false} />);

  wrapper.find('button').simulate('click');

  expect(wrapper.text().includes('Choose Filter')).toBe(true);
  // 用户视角：通过文本找到元素
});

// ❌ 反模式：shallow render 测试伪组件
test('shows filters when clicked', () => {
  const wrapper = shallow(<Calendar showFilters={false} />);

  wrapper.find('FiltersPanel').instance().showFilters();
  // 白盒测试：绕过 UI，直接调用内部方法

  expect(wrapper.find('Filter').props()).toEqual({ title: 'Choose Filter' });
  // 测试实现细节，而非行为
});
```

**何时用 Shallow Render：**
- 子组件明显拖慢测试（如动画）
- 子组件难以配置
- 明确测试的是父组件逻辑，而非集成

### 用户中心测试方法

以用户找到它们的方式查询元素——通过角色、标签文本、占位符文本、显示文本。避免通过 test-id 查询，除非没有语义替代方案。避免通过 CSS 类或内部数据属性查询。

### 测试交互流程

1. 用初始 props 渲染组件
2. 验证初始状态正确渲染
3. 模拟用户操作（click、type 等）
4. 断言可见结果或调用的回调

---

## 测试状态管理

无论使用 Redux、Zustand、MobX、Vuex 还是任何其他状态管理器，测试方法是一致的。

### 隔离测试 store/slice

- 用已知状态初始化
- 分发 action 或调用 mutation
- 断言新状态符合预期

### 关注点

- **状态转换**——action X 是否产生状态 Y？
- **派生状态 / selectors**——给定状态 X，selector 是否返回 Y？
- **异步 effects**——异步 action 是否产生预期的状态变化序列？
- **reducer 边界情况**——未知 action 类型、格式错误的 payload

### 不要测试

- 框架本身——信任 Zustand/Redux dispatch 工作
- store 和组件之间的连接——那是集成关注点

---

## 测试 API/服务层

服务层函数协调传输层和业务逻辑之间的逻辑。

### 策略

- Mock HTTP 客户端或数据库客户端——服务测试不需要命中真实服务器
- 测试每个代码路径：成功、客户端错误（4xx）、服务器错误（5xx）、超时、网络故障
- 验证服务正确转换数据（API 响应 → 领域模型）
- 验证正确参数传递给依赖（正确的 URL、正确的 query params、正确的 headers）

### 常见测试场景

- 成功请求 → 正确数据返回并可能缓存
- 401 响应 → 触发 auth 刷新或重定向
- 404 响应 → 适当的错误/回退
- 网络超时 → 重试或错误暴露
- 格式错误的响应 → 优雅降级，不是崩溃

---

## 边界值分析

一种系统化的技术，用于发现边界情况。对于任何有有效范围的输入，测试：

| 点 | 为什么 |
|---|--------|
| 最小有效值 | 刚好有效 |
| 刚低于最小值 | 第一个无效值 |
| 最大有效值 | 刚好有效 |
| 刚高于最大值 | 第一个无效值 |
| 典型值 | 黄金路径健全性检查 |

### 示例——分页（每页 1-100 条）

测试：0（无效）、1（最小）、50（典型）、100（最大）、101（无效）、-1（负数）、null（缺失）

这种技术单独就能捕获惊人比例的真实世界 bug，因为差一错误和边界处理不当极其常见。

### 边界值类型清单

**数值输入**：0、-1、MAX_SAFE_INTEGER、NaN、Infinity、浮点精度（0.1 + 0.2）

**字符串输入**：空字符串、单字符、超长字符串、unicode、emoji、特殊字符、仅空白、含 HTML/SQL 注入模式

**数组/集合输入**：空、单元素、重复、已排序、逆序、超大（性能）、嵌套结构

**对象输入**：空对象、缺少可选字段、多余字段、null prototype、循环引用

**日期/时间输入**：epoch、闰年、DST 转换、时区边界、远未来、远过去、无效日期

---

## 错误断言最佳实践

当测试需要验证代码抛出错误时，使用声明式断言而非 try-catch。

### 推荐方式：使用 toThrow 断言

```ts
// ✅ 推荐：声明式断言，清晰易读
it('When no product name is provided, should throw InvalidInput error', () => {
  expect(() => addNewProduct({ name: '' }))
    .toThrow(AppError);

  expect(() => addNewProduct({ name: '' }))
    .toThrow(expect.objectContaining({ code: 'InvalidInput' }));
});

// ✅ Jest 风格
it('When price is negative, should throw with error message', () => {
  expect(() => calculatePrice(-100))
    .toThrow('Price cannot be negative');
});
```

### 避免的方式：try-catch 反模式

```ts
// ❌ 不推荐：冗长且失败信息不明确
it('throws error when name is missing', async () => {
  let errorWeExpect = null;
  try {
    await addNewProduct({ name: '' });
  } catch (error) {
    errorWeExpect = error;
  }
  expect(errorWeExpect).not.toBeNull();
  // 失败时只会显示 "received null"，无法定位问题
});
```

### 断言错误属性

```ts
// ✅ 断言错误类型和属性
it('When authentication fails, should throw AuthError with status 401', () => {
  expect(() => authenticate(invalidToken))
    .toThrow(AuthError);

  try {
    authenticate(invalidToken);
  } catch (error) {
    expect(error.statusCode).toBe(401);
    expect(error.message).toContain('Invalid token');
  }
});
```

---

## 快照测试策略

快照测试是一把双刃剑。正确使用时很有价值，滥用时会产生巨大维护负担。

### 原则：使用短的内联快照

```ts
// ✅ 推荐：短小、内联、聚焦关键输出
it('When user profile is rendered, should show user name and role', () => {
  const { getByTestId } = render(<UserProfile user={mockUser} />);

  expect(getByTestId('user-name').textContent).toMatchInlineSnapshot(`"John Doe"`);
});

// ✅ 推荐：对小型稳定输出使用快照
it('When config is generated, should match expected structure', () => {
  const config = generateConfig({ env: 'production' });
  expect(config).toMatchInlineSnapshot(`
Object {
  "apiUrl": "https://api.example.com",
  "timeout": 5000,
}
`);
});
```

### 反模式：大型外部快照

```ts
// ❌ 不推荐：大型外部快照，耦合 2000+ 行不可见内容
it('TestJavaScript.com is rendered correctly', () => {
  const receivedPage = renderer.create(<DisplayPage />).toJSON();
  expect(receivedPage).toMatchSnapshot(); // 生成 2000+ 行外部文件
  // 任何空格、注释变更都会导致测试失败
  // 失败时无法判断是否符合预期
});
```

### 何时使用快照

| 场景 | 推荐 | 原因 |
|------|------|------|
| 小型配置对象 | ✅ 内联快照 | 稳定、易审查 |
| UI 组件渲染 | ⚠️ 谨慎使用 | 脆弱，优先用针对性断言 |
| 大型 API 响应 | ❌ 避免 | 用 schema 验证或字段断言 |
| 多人协作项目 | ⚠️ 需 code review | 快照变更必须审查 |

### 快照最佳实践

1. **内联优于外部** - 快照内容在测试文件中可见
2. **小优于大** - 聚焦关键输出，不是整个对象树
3. **审查快照变更** - 每次快照更新必须人工确认
4. **快照不是文档** - 不要依赖快照理解代码行为

---

## 基于属性的测试

基于属性的测试（Property-based Testing）通过自动生成大量输入组合来发现边界情况下的 bug。

### 为什么需要

传统测试只覆盖有限的输入样本。一个接收 5 个参数的函数可能有数千种输入组合，其中某些组合可能触发未预料的 bug。基于属性的测试自动生成并验证大量组合。

### 使用 fast-check 库

```ts
import fc from 'fast-check';

describe('Product service', () => {
  describe('Adding new product', () => {
    // 自动运行 100 次，每次使用不同的随机属性
    it('When adding product with valid properties, always returns approved status', () => {
      fc.assert(
        fc.property(
          fc.integer({ min: 1 }),
          fc.string({ minLength: 1 }),
          fc.boolean(),
          (id, name, isActive) => {
            const result = addNewProduct({ id, name, isActive });
            expect(result.status).toEqual('approved');
          }
        )
      );
    });
  });
});
```

### 适用场景

| 场景 | 效果 |
|------|------|
| 纯函数、工具函数 | ⭐⭐⭐ 高价值 - 容易发现边界 bug |
| 数据转换函数 | ⭐⭐⭐ 高价值 - 覆盖各种输入格式 |
| 校验逻辑 | ⭐⭐ 中价值 - 发现未预料的输入组合 |
| 复杂业务逻辑 | ⭐ 中价值 - 需要约束输入范围 |

### 定义属性约束

```ts
// 约束输入范围以匹配业务规则
it('When price is within valid range, calculates discount correctly', () => {
  fc.assert(
    fc.property(
      fc.float({ min: 0.01, max: 1000000 }), // 价格范围
      fc.constantFrom('basic', 'premium', 'enterprise'), // 有限的会员等级
      (price, tier) => {
        const discount = calculateDiscount(price, tier);
        // 属性验证：折扣应在合理范围内
        expect(discount).toBeGreaterThanOrEqual(0);
        expect(discount).toBeLessThanOrEqual(price);
      }
    )
  );
});
```

### 与传统测试配合

基于属性的测试**不替代**传统单元测试，而是补充：
- 传统测试：验证已知场景和边界
- 基于属性的测试：发现未预料的输入组合问题

---

## 何时选择单元测试

### 单元测试适合的场景

1. **纯函数和工具函数** - 输入输出明确，无副作用
2. **校验逻辑** - 复杂的表单验证规则
3. **数据转换** - 格式化、解析、映射
4. **算法实现** - 排序、搜索、计算
5. **边界条件** - 需要测试大量边界值组合

### 单元测试不适合的场景

1. **跨模块交互** - 应使用集成测试
2. **用户真实操作流** - 应使用 E2E 测试
3. **需要真实数据** - mock 会导致测试与实际脱节
4. **UI 渲染** - 应使用组件测试或 E2E

### 决策原则

当选择测试层级时：
- **优先集成测试** - 能验证真实交互
- **单元测试用于** - 纯逻辑、边界条件、工具函数
- **E2E 测试用于** - 关键用户旅程

---

## 常见反模式

### 测试实现，不是行为

断言特定的内部方法被调用，而不是断言可见结果。这使测试脆弱——任何重构都会破坏它们。

**问题**：测试与实现细节耦合，重构时测试必须跟着改。

**解决**：测试用户可见的行为，而不是内部如何实现。

### 快照过度使用

大型快照（完整组件树、完整 API 响应）因外观原因频繁破坏，训练开发者盲目更新它们。使用针对性断言代替。快照最适合小型、稳定的输出（序列化配置、小型 SVG）。

### Setup/Teardown 做太多

如果 `beforeEach` 有 30 行，测试可能有太多共享状态。考虑使用 builder 函数或 factory helper 代替。

### 测试中的条件逻辑

测试不应包含 `if/else` 或 `try/catch` 进行流程控制。每个测试是一条线性路径。如果需要不同路径，写不同的测试。

### 忽略测试失败消息

编写能产生有用失败消息的断言。`expect(result).toEqual(expected)` 给你差异。具有良好描述的自定义 matcher 更有帮助。

### 不测试悲伤路径

如果函数可以抛出，测试它抛出正确的错误和正确的消息。不要只测试它在有效输入上不抛出。

---

## BDD 风格断言最佳实践

使用声明式断言让读者无脑 get 到重点，而不是用条件逻辑包裹。

### 使用人类语言形式的断言

```ts
// ✅ 推荐：声明式断言，清晰易读
it('When asking for admins, ensure only ordered admins in results', () => {
  const allAdmins = getUsers({ adminOnly: true });

  expect(allAdmins)
    .to.include.ordered.members(['admin1', 'admin2'])
    .but.not.include.members(['user1']);
});

// ❌ 反模式：冗长复杂的断言逻辑
it('should return only admins', () => {
  const allAdmins = getUsers({ adminOnly: true });

  let admin1Found = false, admin2Found = false;
  allAdmins.forEach(user => {
    if (user === 'user1') {
      assert.notEqual(user, 'user1', 'A user was found');
    }
    if (user === 'admin1') admin1Found = true;
    if (user === 'admin2') admin2Found = true;
  });

  if (!admin1Found || !admin2Found) {
    throw new Error('Not all admins returned');
  }
});
```

### 扩展自定义 Matcher

当内置断言不满足需求时，扩展自定义 matcher 以提高可读性。

```ts
// Jest 自定义 matcher
expect.extend({
  toBeValidEmail(received) {
    const pass = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(received);
    return {
      pass,
      message: () => `expected ${received} ${pass ? 'not ' : ''}to be a valid email`
    };
  }
});

// 使用
expect('user@example.com').toBeValidEmail();
```

---

## 其他测试习惯

以下是一些经时间验证的测试最佳实践，虽然与 Node.js 无直接关联，但能显著提升测试效果。

### TDD 原则

测试驱动开发（Test-Driven Development）对许多团队非常有价值，但不必强迫使用。

| 阶段 | 说明 | 示例 |
|------|------|------|
| **Red** | 先写一个失败的测试 | `it('When price is negative, should throw error', ...)` |
| **Green** | 写最少的代码让测试通过 | 添加 `if (price < 0) throw ...` |
| **Refactor** | 在测试保护下重构代码 | 提取 `validatePrice()`、`applyTax()` |

### 更多最佳实践

| 实践 | 说明 |
|------|------|
| 每个测试只检查一件事 | 聚焦单一行为，失败时易于定位 |
| 修复 bug 前先写测试 | 确保不会再次出现 |
| 让每个测试至少失败一次 | 验证测试真的能捕获问题 |
| 快速编写简单代码 | 先满足测试，再逐步优化 |
| 避免环境依赖 | 不依赖特定路径、操作系统、时区 |
| 测试失败时立即可读 | 好的测试名称和断言消息 |

---

## 总结

单元测试的核心价值：
1. **快速反馈** - 毫秒级验证逻辑正确性
2. **活文档** - 测试名称即功能规格
3. **安全重构** - 改实现不改行为时测试仍通过
4. **边界覆盖** - 系统化测试边界条件

记住：**好的单元测试让人不看源码也能还原功能规格**。
