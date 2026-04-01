# React 性能优化与现代模式

> 性能优化不是把代码写得更快，而是避免做不必要的事。React 提供的工具大部分是帮你"少干活"——少渲染、少计算、少传输。

## 阅读指南

```
前置阅读：01-react-overview.md、03-react-hooks-deep-dive.md
推荐阅读顺序：
01-react-overview.md → 02-concurrent-mode-fiber.md → 03-react-hooks-deep-dive.md → 本文
```

## 30 秒心智模型

**性能优化的本质：不做不必要的事。**

React 的性能问题只有三类：

| 问题 | 解决方案 | 工具 |
|------|---------|------|
| 组件渲染太频繁 | 阻断渲染 | `React.memo` |
| 计算成本高 | 缓存结果 | `useMemo` |
| 函数每次重建 | 缓存函数 | `useCallback` |
| 初始加载太慢 | 延迟加载 | `React.lazy` + `Suspense` |
| 列表太大 | 只渲染可见 | 虚拟列表 |

**核心心智模型：**

```
问题：组件重新渲染了，但 props/state 没变
    │
    ├── 如果是组件级别 ──→ React.memo（阻断）
    │
    ├── 如果是计算结果 ──→ useMemo（缓存）
    │
    └── 如果是函数引用 ──→ useCallback（稳定引用）
```

**一个例子看懂：**

```jsx
// 问题：父组件渲染，子组件跟着渲染
function Parent() {
  const [count, setCount] = useState(0);
  const user = { name: 'Alice' }; // 每次创建新对象
  
  return <Child user={user} />; // user 变了，Child 渲染
}

// 方案一：如果 Child 很重，用 React.memo
const Child = React.memo(function Child({ user }) { ... });

// 方案二：如果 user 不需要每次新建，用 useMemo
const user = useMemo(() => ({ name: 'Alice' }), []);
```

**记住：** 优化不是为了「更快」，而是为了「少做」。

## 目录

- [性能诊断](#性能诊断)
- [渲染优化](#渲染优化)
- [代码分割](#代码分割)
- [列表优化](#列表优化)
- [错误边界](#错误边界)
- [Portals](#portals)
- [Server Components](#server-components)
- [React Compiler](#react-compiler)
- [最佳实践](#最佳实践)
- [术语速查](#术语速查)

---

## 性能诊断

### React DevTools Profiler

Chrome 扩展 React DevTools 提供了 Profiler 面板。

使用步骤：
1. 安装 React DevTools
2. 打开 Profiler 面板
3. 点击录制按钮
4. 操作应用
5. 停止录制

Profiler 会显示：
- 哪些组件渲染了
- 渲染耗时
- 渲染原因（props 变化、state 变化、父组件渲染）

### 为什么组件渲染了

常见原因：

| 原因 | 解决方案 |
|-----|---------|
| 父组件渲染 | `React.memo` |
| props 是新对象/函数 | `useMemo`/`useCallback` |
| state 变化 | 确认是否必要 |
| context 变化 | 拆分 context |
| 强制更新 | 避免 `forceUpdate` |

### Chrome Performance 面板

分析运行时性能：

1. 打开 DevTools → Performance
2. 点击 Record
3. 操作应用
4. 停止录制

关注指标：
- **Scripting**：JS 执行时间
- **Rendering**：样式计算和布局
- **Painting**：绘制

如果 Scripting 时间长，可能是 React 渲染过重；如果 Rendering/Painting 长，可能是 DOM 操作或样式问题。

### 识别问题组件

用 `why-did-you-render` 库检测不必要的渲染：

```javascript
// setup.js
import whyDidYouRender from '@welldone-software/why-did-you-render';
whyDidYouRender(React, {
  trackAllPureComponents: true,
});

// 组件
function MyComponent(props) {
  return <div>{props.value}</div>;
}
MyComponent.whyDidYouRender = true;
```

控制台会显示组件渲染原因。

---

## 渲染优化

### React.memo

浅比较 props，避免不必要的渲染。

```jsx
const ExpensiveChild = React.memo(function Child({ data, onClick }) {
  // 只有 data 或 onClick 变化才渲染
  return <div onClick={onClick}>{data}</div>;
});

// 自定义比较函数
const Child = React.memo(
  function Child({ user }) {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => {
    // 返回 true 表示相等，不渲染
    return prevProps.user.id === nextProps.user.id;
  }
);
```

### useMemo 和 useCallback

```jsx
function Parent({ items, onItemClick }) {
  // 记忆计算结果
  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => a.name.localeCompare(b.name));
  }, [items]);
  
  // 记忆函数
  const handleClick = useCallback((id) => {
    onItemClick(id);
  }, [onItemClick]);
  
  return <List items={sortedItems} onItemClick={handleClick} />;
}
```

### 优化 Context

Context 值变化会导致所有消费者重新渲染。

```jsx
// 问题：value 每次都是新对象
function App() {
  const [user, setUser] = useState(null);
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <AppContent />
    </UserContext.Provider>
  );
}

// 方案一：拆分 Context
const UserContext = createContext();
const SetUserContext = createContext();

function App() {
  const [user, setUser] = useState(null);
  
  return (
    <SetUserContext.Provider value={setUser}>
      <UserContext.Provider value={user}>
        <AppContent />
      </UserContext.Provider>
    </SetUserContext.Provider>
  );
}

// 只需要 user 的组件不会因为 setUser 变化而渲染
function Profile() {
  const user = useContext(UserContext);
  return <div>{user?.name}</div>;
}

// 方案二：useMemo 记忆 value
function App() {
  const [user, setUser] = useState(null);
  const value = useMemo(() => ({ user, setUser }), [user]);
  
  return (
    <UserContext.Provider value={value}>
      <AppContent />
    </UserContext.Provider>
  );
}
```

### 状态下沉

把状态移到需要它的地方，减少影响范围。

```jsx
// 问题：整个 App 因为一个小状态重新渲染
function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  return (
    <>
      <Header />
      <Content />
      <Footer />
      {isModalOpen && <Modal />}
    </>
  );
}

// 优化：状态下沉到需要的地方
function App() {
  return (
    <>
      <Header />
      <Content />
      <Footer />
      <ModalTrigger />  {/* isModalOpen 在这里管理 */}
    </>
  );
}

function ModalTrigger() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  return (
    <>
      <button onClick={() => setIsModalOpen(true)}>Open</button>
      {isModalOpen && <Modal onClose={() => setIsModalOpen(false)} />}
    </>
  );
}
```

### 组件组合

用 `children` 避免传递 props 导致的渲染。

```jsx
// 问题：Page 重新渲染，ExpensiveChild 也跟着渲染
function Page({ user }) {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <ExpensiveChild user={user} />
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
    </div>
  );
}

// 优化：把 ExpensiveChild 提升出去
function App() {
  const [user, setUser] = useState({ name: 'Alice' });
  
  return (
    <Page user={user}>
      <ExpensiveChild user={user} />
    </Page>
  );
}

function Page({ user, children }) {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      {children}  {/* 不会因为 Page 渲染而重新渲染 */}
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
    </div>
  );
}
```

---

## 代码分割

### React.lazy 和 Suspense

动态导入组件，按需加载。

```jsx
import { lazy, Suspense } from 'react';

// 懒加载组件
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### 路由级分割

最常见的分割粒度是路由。

```jsx
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Dashboard = lazy(() => import('./pages/Dashboard'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoading />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

### 条件加载

某些功能只在特定条件下才加载。

```jsx
function App() {
  const [showChart, setShowChart] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Loading />}>
          <Chart />
        </Suspense>
      )}
    </div>
  );
}

const Chart = lazy(() => import('./Chart'));
```

### 预加载

在用户可能需要之前预加载。

```jsx
const Dashboard = lazy(() => import('./Dashboard'));

// 鼠标悬停时预加载
function App() {
  return (
    <Link
      to="/dashboard"
      onMouseEnter={() => import('./Dashboard')}
    >
      Dashboard
    </Link>
  );
}
```

### 命名导出

默认导出的模块适合 `React.lazy`，命名导出需要处理：

```javascript
// 导出命名导出的组件
export const NamedComponent = () => <div>Named</div>;

// 懒加载时需要重命名
const NamedComponent = lazy(() =>
  import('./NamedComponent').then(module => ({
    default: module.NamedComponent
  }))
);
```

---

## 列表优化

### 虚拟列表

大列表只渲染可见项。

```jsx
import { FixedSizeList } from 'react-window';

function LargeList({ items }) {
  return (
    <FixedSizeList
      height={400}
      width={300}
      itemCount={items.length}
      itemSize={50}
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </FixedSizeList>
  );
}
```

常用虚拟列表库：
- `react-window`：轻量，性能好
- `react-virtualized`：功能丰富，体积大
- `@tanstack/react-virtual`：现代化，支持变高

### Key 的正确使用

```jsx
// 错误：用索引作为 key
{items.map((item, index) => (
  <Item key={index} {...item} />
))}

// 正确：用唯一标识
{items.map(item => (
  <Item key={item.id} {...item} />
))}

// 错误：key 不稳定
{items.map(item => (
  <Item key={Math.random()} {...item} />
))}
```

用索引作为 key 的问题：
- 顺序变化时，React 无法正确追踪元素
- 可能导致状态错乱
- 性能下降（不必要的 DOM 操作）

### 列表组件优化

```jsx
// 列表项用 React.memo
const Item = React.memo(function Item({ data }) {
  return <div>{data.name}</div>;
});

function List({ items }) {
  return (
    <ul>
      {items.map(item => (
        <Item key={item.id} data={item} />
      ))}
    </ul>
  );
}
```

---

## 错误边界

错误边界捕获子组件的渲染错误，显示降级 UI。

### 创建错误边界

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    // 更新 state，下次渲染显示降级 UI
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // 记录错误
    console.error('Error caught by boundary:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}
```

### 使用错误边界

```jsx
function App() {
  return (
    <ErrorBoundary>
      <Header />
      <ErrorBoundary>  {/* 可嵌套 */}
        <Content />
      </ErrorBoundary>
      <Footer />
    </ErrorBoundary>
  );
}
```

### 错误边界的限制

错误边界**不能捕获**：
- 事件处理函数中的错误
- 异步代码（setTimeout、Promise）
- 服务端渲染
- 错误边界自身的错误

```jsx
// 这些错误不会被错误边界捕获
function Component() {
  const handleClick = () => {
    throw new Error('Event error');  // 不会被捕获
  };
  
  useEffect(() => {
    setTimeout(() => {
      throw new Error('Async error');  // 不会被捕获
    }, 1000);
  }, []);
  
  return <button onClick={handleClick}>Click</button>;
}

// 正确处理：用 try-catch
function Component() {
  const handleClick = () => {
    try {
      doSomething();
    } catch (e) {
      // 处理错误
    }
  };
}
```

---

## Portals

Portals 把子组件渲染到 DOM 树的其他位置。

### 基本用法

```jsx
import { createPortal } from 'react-dom';

function Modal({ children }) {
  return createPortal(
    <div className="modal-overlay">
      <div className="modal-content">
        {children}
      </div>
    </div>,
    document.getElementById('modal-root')
  );
}
```

### 为什么需要 Portals

1. **样式隔离**：模态框不受父元素的 `overflow: hidden`、`z-index` 影响
2. **语义正确**：模态框在 DOM 结构上独立，但逻辑上仍是组件树一部分
3. **事件冒泡**：事件仍然冒泡到 React 父组件

```jsx
function App() {
  const handleModalClick = () => {
    console.log('Modal clicked');
  };
  
  return (
    <div onClick={handleModalClick}>
      <Modal>
        <button>Click me</button>
        {/* 点击按钮，事件冒泡到 App，打印 "Modal clicked" */}
      </Modal>
    </div>
  );
}
```

### 常见用例

- 模态框
- 下拉菜单（防止被父容器裁剪）
- 工具提示
- 通知

---

## Server Components

React 18 引入 Server Components，在服务端渲染组件。

### 服务端组件 vs 客户端组件

| 特性 | 服务端组件 | 客户端组件 |
|-----|----------|----------|
| 渲染位置 | 服务端 | 客户端 |
| 可用 API | Node.js API | 浏览器 API |
| 状态/Hooks | 不可用 | 可用 |
| 交互性 | 无 | 有 |
| 包大小 | 不影响 JS bundle | 影响 bundle |

### 服务端组件示例

```jsx
// ServerComponent.js（服务端组件）
// 这个组件在服务端执行，不会发送到客户端
async function BlogPost({ slug }) {
  const post = await db.posts.findUnique({ where: { slug } });
  
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// 使用 'use client' 标记客户端组件
'use client';

function LikeButton({ postId }) {
  const [liked, setLiked] = useState(false);
  
  return (
    <button onClick={() => setLiked(!liked)}>
      {liked ? '❤️' : '🤍'}
    </button>
  );
}
```

### 组合使用

```jsx
// page.js（服务端组件）
import BlogPost from './BlogPost';
import LikeButton from './LikeButton';

export default function Page({ params }) {
  return (
    <div>
      <BlogPost slug={params.slug} />
      <LikeButton postId={params.slug} />
    </div>
  );
}
```

### 优势

1. **更小的 JS bundle**：服务端组件代码不发送到客户端
2. **直接访问后端资源**：数据库、文件系统
3. **自动代码分割**：客户端组件天然被分割
4. **更好的 SEO**：内容在 HTML 中

### 限制

- 服务端组件不能有状态（useState、useReducer）
- 不能有副作用（useEffect）
- 不能用浏览器 API（window、localStorage）
- 不能传函数给客户端组件作为 props

---

## React Compiler

React 19 引入官方编译器，自动优化组件。

### 自动 Memoization

编译器自动分析组件，决定哪里需要 memoization。

```jsx
// 编译前
function TodoList({ todos, onItemClick }) {
  const sortedTodos = [...todos].sort((a, b) => 
    a.priority - b.priority
  );
  
  return (
    <ul>
      {sortedTodos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onClick={() => onItemClick(todo.id)}
        />
      ))}
    </ul>
  );
}

// 编译后（概念性展示）
function TodoList({ todos, onItemClick }) {
  // 编译器自动 memoize
  const sortedTodos = useMemo(() => 
    [...todos].sort((a, b) => a.priority - b.priority),
    [todos]
  );
  
  // 编译器自动用 useCallback 包裹
  const createClickHandler = useCallback((id) => 
    () => onItemClick(id),
    [onItemClick]
  );
  
  return (
    <ul>
      {sortedTodos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onClick={createClickHandler(todo.id)}
        />
      ))}
    </ul>
  );
}
```

### 使用方式

```javascript
// babel.config.js
module.exports = {
  presets: [
    ['babel-preset-react-compiler'],
  ],
};
```

### 注意事项

- 编译器需要组件遵循 Rules of Hooks
- 需要正确声明依赖（useEffect 的依赖数组）
- 避免修改 props
- 避免在渲染中修改非局部变量

---

## 最佳实践

### 组件设计

```jsx
// 好：单一职责
function UserCard({ user }) {
  return (
    <div>
      <Avatar user={user} />
      <UserInfo user={user} />
    </div>
  );
}

// 避免：做太多事
function UserCard({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  
  // ...太多逻辑
}
```

### 状态设计

```jsx
// 好：最小状态
function Form() {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');
  // 其他值可从 value 派生
}

// 避免：冗余状态
function Form() {
  const [value, setValue] = useState('');
  const [isValid, setIsValid] = useState(true);  // 可派生
  const [error, setError] = useState('');        // 可派生
}

// 好：派生状态
function Form() {
  const [value, setValue] = useState('');
  const error = validate(value);  // 派生
  const isValid = !error;         // 派生
}
```

### 副作用处理

```jsx
// 好：依赖数组完整
useEffect(() => {
  const subscription = subscribe(userId);
  return () => subscription.unsubscribe();
}, [userId]);

// 避免：空依赖但用了外部变量
useEffect(() => {
  console.log(userId);  // userId 应该在依赖中
}, []);
```

### 列表渲染

```jsx
// 好：稳定的 key
{items.map(item => (
  <Item key={item.id} {...item} />
))}

// 避免：索引作为 key
{items.map((item, index) => (
  <Item key={index} {...item} />
))}
```

### 条件渲染

```jsx
// 好：提前返回
function Component({ user }) {
  if (!user) {
    return <LoginPrompt />;
  }
  
  return <Dashboard user={user} />;
}

// 避免：嵌套三元
function Component({ user, isLoading }) {
  return isLoading ? (
    <Loading />
  ) : user ? (
    <Dashboard user={user} />
  ) : (
    <LoginPrompt />
  );
}
```

### 避免过度优化

```jsx
// 过度：简单组件不需要 memo
const SimpleText = React.memo(function SimpleText({ text }) {
  return <span>{text}</span>;
});

// 过度：原生元素不需要 useCallback
const handleClick = useCallback(() => {}, []);
return <button onClick={handleClick}>Click</button>;

// 合理：复杂组件或频繁重渲染场景
const ExpensiveList = React.memo(function List({ items }) {
  // 复杂渲染逻辑
});
```

---

## 术语速查

| 术语 | 含义 |
|-----|------|
| **Re-render** | 组件函数重新执行 |
| **Memoization** | 缓存计算结果 |
| **React.memo** | 高阶组件，浅比较 props |
| **Code Splitting** | 代码分割，按需加载 |
| **Lazy Loading** | 懒加载，延迟加载 |
| **Suspense** | 等待异步内容的组件 |
| **Virtual List** | 虚拟列表，只渲染可见项 |
| **Error Boundary** | 错误边界，捕获渲染错误 |
| **Portal** | 传送门，渲染到其他 DOM 位置 |
| **Server Component** | 服务端组件 |
| **Client Component** | 客户端组件 |
| **Compiler** | React 编译器，自动优化 |

---

## 参考

- [React 性能优化官方文档](https://react.dev/learn/render-and-commit)
- [React.memo](https://react.dev/reference/react/memo)
- [React.lazy](https://react.dev/reference/react/lazy)
- [Server Components](https://react.dev/reference/rsc/server-components)
- [React Compiler](https://react.dev/learn/react-compiler)

---

**上一篇：** [React Hooks 深度解析](03-react-hooks-deep-dive.md)  
**下一篇：** [React 事件系统](05-react-event-system.md)
