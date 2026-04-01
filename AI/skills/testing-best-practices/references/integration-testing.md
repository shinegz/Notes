# 集成测试指南

本文档提供集成测试的深入指导。当测试计划涉及模块间交互、API 端点或组件协作时，加载此参考。

> **通用测试原则**（黄金法则、AAA 模式、三元命名法、黑盒测试）见 `SKILL.md`，适用于所有测试类型。

---

## 目录

- [什么是集成测试](#什么是集成测试)
- [何时选择集成测试](#何时选择集成测试)
- [前端集成测试](#前端集成测试)
- [后端集成测试](#后端集成测试)
- [API / HTTP 集成测试](#api--http-集成测试)
- [数据库集成测试](#数据库集成测试)
- [中间件测试](#中间件测试)
- [契约测试](#契约测试)
- [测试异步工作流](#测试异步工作流)
- [静态分析工具](#静态分析工具)
- [良好集成测试的关键](#良好集成测试的关键)
- [常见陷阱](#常见陷阱)

---

## 什么是集成测试

集成测试验证两个或多个单元是否正确协作。它们比 E2E 快，覆盖面比单元测试广。**当有趣的行为发生在模块边界时使用集成测试。**

与单元测试相比，更少的东西被 mock——测试让真实代码交互，只在最外边界（网络、文件系统、第三方 API）进行 mock。

---

## 何时选择集成测试

| 场景 | 推荐 |
|------|------|
| 组件使用真实数据从 hook/store 正确渲染 | 集成测试 |
| API 端点在真实中间件链下返回正确响应 | 集成测试 |
| 表单验证显示错误并阻止提交 | 集成测试 |
| 服务正确转换并缓存 API 响应 | 集成测试 |
| 第三方集成 | 集成测试（mock 边界） |

**Testing Trophy（Kent C. Dodds 模型）**建议：大量集成测试、适量单元测试、少量 E2E 测试。集成测试提供最佳的信心/投入比。

---

## 前端集成测试

### 组件 + 真实状态管理

- 用真实的 store/context provider 渲染组件
- 像用户一样交互（点击、输入、提交）
- 断言渲染输出（而非 store 内部）

### 组件 + 真实路由

- 在 router provider 内渲染
- 触发导航（点击链接、提交表单）
- 断言结果路由和渲染内容

### 组件 + 真实 API 层（在 network 层 mock）

- 使用 MSW（Mock Service Worker）或类似工具拦截网络请求
- 渲染组件，让它通过真实代码路径获取数据
- 断言加载态 → 数据渲染 → 错误态
- 这测试完整数据流：组件 → hook → API 客户端 → network mock → 组件更新

### MSW (Mock Service Worker) 使用

Mock Service Worker 在网络层拦截请求，比直接 mock fetch/axios 更接近真实场景。

```ts
// handlers.ts - 定义 mock 响应
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/products', (req, res, ctx) => {
    return res(
      ctx.json([
        { id: 1, name: 'Product 1', price: 100 },
        { id: 2, name: 'Product 2', price: 200 }
      ])
    );
  }),

  rest.post('/api/orders', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({ id: 1, status: 'created' })
    );
  }),

  // 模拟错误场景
  rest.get('/api/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ message: 'Internal server error' })
    );
  })
];
```

```ts
// setup-tests.ts - 配置 MSW
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

```ts
// 组件测试
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { server } from './setup-tests';
import ProductList from './ProductList';

test('When products load successfully, should display product list', async () => {
  render(<ProductList />);

  // 等待加载状态消失
  await waitFor(() => {
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
  });

  // 验证产品显示
  expect(screen.getByText('Product 1')).toBeInTheDocument();
  expect(screen.getByText('$100')).toBeInTheDocument();
});

test('When API returns error, should display error message', async () => {
  // 覆盖特定端点的响应
  server.use(
    rest.get('/api/products', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );

  render(<ProductList />);

  await waitFor(() => {
    expect(screen.getByText('Failed to load products')).toBeInTheDocument();
  });
});
```

### 为什么选择网络层 Mock

| 方法 | 优点 | 缺点 |
|------|------|------|
| **MSW（网络层）** | 测试完整代码路径；捕获 headers、URL 问题 | 需要额外配置 |
| jest.mock('axios') | 简单直接 | 跳过真实 HTTP 客户端代码 |
| Sinon stub | 灵活 | 可能 mock 错误层 |

**集成测试优先使用网络层 mock**，只有隔离单元测试才使用函数层 mock。

---

## 后端集成测试

### 服务 + 真实数据库

- 使用测试数据库（SQLite 内存数据库、test container 或专用测试 DB）
- 测试前运行迁移，测试后清理
- 测试真实查询和事务，而非 mock 的 repository 返回值

### Controller + 真实中间件 + 真实服务（在 DB/external 层 mock）

- 使用测试 HTTP 客户端（supertest、httptest 等）发送真实 HTTP 请求
- 让完整中间件链执行（认证、验证、错误处理）
- 只 mock 外部依赖（DB、第三方 API）

---

## API / HTTP 集成测试

用真实 HTTP 请求但受控依赖测试 API 端点。

### 每个端点要验证什么

- 成功和每个错误情况的正确状态码
- 响应 body 结构和内容
- 响应 headers（content-type、caching、CORS）
- 认证和授权（有效 token、过期 token、错误角色）
- 输入验证（缺失字段、错误类型、过长、注入尝试）
- 分页（首页、末页、超出范围、页大小限制）
- 幂等操作的实际幂等性（PUT、DELETE）

### 测试设置模式

1. 启动应用（或其测试实例）
2. 用已知测试数据 seed 数据库
3. 使用测试 HTTP 客户端发送请求
4. 断言响应
5. 清理测试数据

---

## 数据库集成测试

### 隔离策略

| 策略 | 优点 | 缺点 |
|------|------|------|
| **事务回滚** | 快 | 不测试 commit 行为 |
| **截断** | 测试真实 commit | 慢 |
| **Test containers** | 最大隔离 | 启动慢 |

### 要测试什么

- CRUD 操作产生预期的数据库状态
- 约束被强制执行（unique、foreign key、not null）
- 并发操作被正确处理（乐观锁、竞态条件）
- 迁移在全新数据库上干净运行
- 查询在真实数据量下返回正确结果

---

## 中间件测试

中间件虽然小，但影响全部或大部分请求，必须单独测试。

### 隔离测试中间件

中间件可以作为纯函数测试——参数是 `{req, res}` JS 对象，无需启动完整服务器。

```ts
import httpMocks from 'node-mocks-http';
import authMiddleware from './auth-middleware';

test('When request has no auth header, should return 403', () => {
  // Arrange - 创建 mock 请求/响应对象
  const request = httpMocks.createRequest({
    method: 'GET',
    url: '/user/42',
    headers: { authorization: '' }
  });
  const response = httpMocks.createResponse();

  // Act
  authMiddleware(request, response, () => {});

  // Assert
  expect(response.statusCode).toBe(403);
});

test('When request has valid token, should call next', () => {
  const request = httpMocks.createRequest({
    headers: { authorization: 'Bearer valid-token' }
  });
  const response = httpMocks.createResponse();
  const nextFn = jest.fn();

  authMiddleware(request, response, nextFn);

  expect(nextFn).toHaveBeenCalled();
  expect(request.user).toBeDefined(); // 中间件应注入用户信息
});
```

### 测试要点

- **成功路径**：中间件调用 `next()` 并正确修改 `req`
- **失败路径**：返回正确的状态码和错误信息
- **边界情况**：无效 token、过期 token、权限不足
- **性能**：中间件在每个请求上执行，不应有阻塞操作

---

## 契约测试

在微服务架构中，服务间的 API 契约变更可能导致集成问题。契约测试确保服务提供方和消费方的接口一致。

### Consumer-Driven Contracts

不再由服务端定义测试计划，而是由客户端决定服务端的测试。消费者定义期望，提供者验证是否满足。

### 使用 PACT 框架

```ts
// 消费者端 - 定义契约
const { Verifier } = require('@pact-foundation/pact');

// 定义消费者对提供者的期望
provider.addInteraction({
  state: 'user 123 exists',
  uponReceiving: 'a request for user 123',
  withRequest: {
    method: 'GET',
    path: '/users/123'
  },
  willRespondWith: {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
    body: { id: 123, name: 'John Doe' }
  }
});
```

```ts
// 提供者端 - 验证契约
const { Verifier } = require('@pact-foundation/pact');

new Verifier({
  providerBaseUrl: 'http://localhost:8080',
  pactUrls: ['./pacts/consumer-provider.json']
}).verifyProvider().then(() => {
  console.log('契约验证通过');
});
```

### 工作流程

```
消费者测试 → 生成契约文件 → 上传到 Pact Broker
                                        ↓
提供者 CI ← 拉取契约 ← 验证是否满足契约
```

### 适用场景

| 场景 | 契约测试价值 |
|------|-------------|
| 微服务间 API | ⭐⭐⭐ 高 - 防止接口不兼容 |
| 多客户端后端 | ⭐⭐⭐ 高 - 客户端驱动契约 |
| 单体应用 | ⭐ 低 - 内部接口变更可控 |
| 第三方 API 集成 | ⚠️ 不适用 - 无法控制对方 |

---

## 静态分析工具

静态分析工具帮助客观提升代码质量并使其可维护。

### 推荐工具

**SonarQube** —— 综合代码质量平台：
- 代码复杂度分析
- 重复代码检测
- 代码异味检测
- 测试覆盖率趋势
- 安全漏洞扫描

**Code Climate** —— 轻量级云端分析：
- 可维护性评分
- 复杂方法识别
- 技术债务跟踪

### CI 集成

```yaml
# GitLab CI 示例
sonarqube-check:
  script:
    - sonar-scanner
  variables:
    SONAR_TOKEN: $SONAR_TOKEN
    SONAR_HOST_URL: $SONAR_HOST_URL
  only:
    - merge_requests
```

### 关注指标

| 指标 | 健康阈值 | 说明 |
|------|----------|------|
| 圈复杂度 | < 15 | 过高说明需要拆分 |
| 代码重复率 | < 3% | 重复代码应提取 |
| 技术债务 | < 5% | 偿还时间占比 |
| 认知复杂度 | < 25 | 可读性指标 |

---

## 测试异步工作流

异步操作（消息队列、事件驱动系统、定时任务）需要特殊关注。

### 策略

- 使用消息代理的测试替身（内存队列）
- 发布消息 → 断言 handler 正确处理
- 用可控时钟测试超时和重试行为
- 测试失败场景：handler 抛出、消息格式错误、队列不可用
- 验证幂等性：处理同一消息两次产生相同结果

### 前端异步（API 调用、定时器、动画）

- 对 debounce/throttle/setTimeout 使用 fake timers
- 在 network 层 mock（MSW、nock）而非直接 mock fetch
- 测试加载 → 成功 和 加载 → 错误 流程
- 验证取消（组件 unmount 时请求仍在进行）

---

## 良好集成测试的关键

### 控制边界

明确什么是真实的、什么是 mock 的。mock 边界推得越靠外，信心越大——但设置和清理也越多。

### 确定性测试数据

使用能产生已知数据的工厂或 seeder。永远不依赖其他测试的数据。

### 测试完整请求-响应周期

- **API**：发送真实 HTTP 请求 → 验证响应状态、headers、body
- **UI**：渲染 → 交互 → 验证可见结果

---

## 测试文件组织

集成测试遵循 Co-location 原则，与单元测试一致。详见 `SKILL.md` → 测试文件组织原则。

---

## ⚠️ 核心反模式警示

### 反模式 1：测试 Mock 对象而非真实代码

**这是集成测试中最严重的反模式**。集成测试的目的是验证「真实代码是否按预期协同工作」，而非「mock 的对象是否返回我们预设的值」。

**错误示例**：
```ts
// ❌ 反模式：测试的是 mock 的返回值，而非真实逻辑
jest.mock('../utils/helpers', () => ({
  formatData: jest.fn().mockReturnValue([{ id: 1 }]),
}));

test('When module A calls module B, should process data correctly', () => {
  const result = processWithModuleB();
  expect(result).toEqual([{ id: 1 }]); // 这个断言毫无意义
  // 因为 result 就是 mock 返回的值，根本没有测试真实逻辑
});
```

**正确做法**：
```ts
// ✅ 正确：测试真实模块间的协作，只在边界 mock
import { processWithModuleB } from '../moduleA';
import { fetchProducts } from '../api';

// 只在 API 边界 mock，让真实的数据处理逻辑执行
jest.mock('../api');
jest.mocked(fetchProducts).mockResolvedValue([{ id: 1, name: 'Test' }]);

test('When API returns products, should process and filter correctly', async () => {
  const result = await processWithModuleB();
  // 这个断言验证的是真实的 processWithModuleB 逻辑
  expect(result).toEqual([{ id: 1, processed: true }]);
});
```

**判断标准**：问自己「如果被测的真实代码有 bug，这个测试会失败吗？」如果答案是「不会，因为 mock 返回的是正确的值」，那就是反模式。

### 反模式 2：Mock 边界错位

集成测试的 mock 应该只发生在**系统边界**（网络、文件系统、第三方服务），而不是**模块边界**。

| 层级 | Mock 位置 | 是否合理 |
|------|----------|----------|
| 单元测试 | 函数/模块边界 | ✅ 合理 |
| 集成测试 | API/网络边界 | ✅ 合理 |
| 集成测试 | 模块边界（如 mock 另一个本地模块） | ❌ 失去集成意义 |

**错误示例**：
```ts
// ❌ 反模式：在模块边界 mock，失去了集成测试的意义
jest.mock('./calculator');
jest.mock('./formatter');

test('integration test', () => {
  // calculator 和 formatter 都被 mock 了
  // 这只是伪装成集成测试的单元测试
});
```

**正确做法**：
```ts
// ✅ 正确：让 calculator 和 formatter 真实执行，只在 API 边界 mock
jest.mock('./api');

test('When API returns data, should calculate and format correctly', async () => {
  jest.mocked(api.getData).mockResolvedValue({ value: 100 });
  const result = await processPipeline(); // 让 calculator 和 formatter 真实执行
  expect(result).toBe('Formatted: 100');
});
```

---

## 常见陷阱

### 集成测试中过度 mock

如果你 mock 单元接触的所有东西，那只是带额外步骤的单元测试。集成的目的是让真实代码交互。

**判断标准**：集成测试中，应该 mock 的东西是「你无法控制的」，而不是「你觉得麻烦 mock 掉更方便的」。

### 慢测试套件

如果集成套件太慢，开发者会停止运行它。并行化、高效使用 test containers、将测试移到最低适当层级。

### 不测试错误路径

Happy path 测试给人错误信心。测试关键失败场景（网络错误、auth 过期、server 500）。

### 测试顺序依赖

测试 B 只有在测试 A 运行后才通过。隔离测试数据，每个测试创建自己的数据。
