# React Fiber 深度解析

> React 15 的渲染引擎有个致命问题：一旦开始渲染，中途不能停。Fiber 的出现，就是为了解决这个问题。

---

## 30 秒心智模型

先记住这个比喻：**Fiber 把 React 从「单线程厨师」变成了「会看脸色的大厨」**。

| 旧方案 | 新方案 |
|--------|--------|
| 一次做完全部菜 | 每做一道菜，看一眼客人 |
| 客人中途加单？等 | 立刻响应VIP客人 |
| 300ms 厨房锁死 | 用户输入秒响应 |

---

## 问题出在哪

Stack Reconciler 用了递归。递归的特点是：一旦开始，必须跑完。

```javascript
// 这段代码跑起来就不能停
function reconcile(node) {
  process(node);
  node.children.forEach(child => reconcile(child));
}
```

想象这个场景：你点了一道大餐，厨师必须从头做到尾，中途不能接新订单。这就是 React 15 在大组件树下的状态——页面卡死，用户输入没反应。

**核心矛盾：** JavaScript 单线程，渲染和交互抢同一资源。

---

## Fiber 的解决思路

关键洞察：**用数据结构代替调用栈来保存进度**。

```javascript
// 不再依赖调用栈
function workLoop() {
  while (workInProgress && !shouldYield()) {
    workInProgress = performUnitOfWork(workInProgress);
  }
}
```

每个 Fiber 节点记住自己的 child、sibling、return。像一张任务卡，处理到哪一步都记着。

### 双缓冲

```
workInProgress（后台构建）←→ current（屏幕上）
```

后台算好了，一次性切换。没有中间状态，用户看不到闪烁。

---

## 两阶段：可中断的秘密

Render Phase 做的事：调用函数、Diff、更新标记。**只算，不碰 DOM**。

所以可以随时停——反正 DOM 没改，丢了重新算也没损失。

Commit Phase 做的事：**必须一口气做完**。插入节点、更新属性、执行 useEffect。这些不能停，停了就白屏。

> 打个比方：设计方案可以随时改，墙漆一旦开始刷就必须刷完。

---

## 时间切片

浏览器 60 FPS，一帧只有 16.7ms。React 用 5ms 左右，剩下的留给浏览器。

```javascript
function shouldYield() {
  return getCurrentTime() >= deadline - 1;
}
```

每处理完一个节点检查一次：该让出主线程了吗？

---

## 优先级调度

Lane 模型用位运算表示优先级：

```javascript
SyncLane = 0b0001;      // 用户点击，最急
TransitionLane = 0b1000; // 搜索输入，可以等
```

```javascript
<input onChange={e => {
  setQuery(e.target.value);              // 高优，秒响应
  startTransition(() => {
    setResults(search(e.target.value)); // 低优，让路
  });
}} />
```

打字的时候，输入框必须立刻更新。搜索结果可以慢一点。高优先级直接打断低优先级任务。

---

## 什么时候该关心 Fiber

| 场景 | 建议 |
|-----|------|
| 写业务代码 | 会用 useTransition 就行 |
| 优化大列表 | 掌握 key，用虚拟滚动 |
| 面试 | 链表结构、双缓冲是常考点 |
| 读源码 | Lane 模型、调度器是硬骨头 |

---

## 常见误解

**1. Fiber 让渲染更快？**
不全是。它让体感更流畅——用户不觉得卡，但总计算时间可能更长。

**2. 所有更新都会被中断？**
只有 Render Phase 可以。同步更新（普通 setState）不会被中断。

**3. Time Slicing 什么都能切片？**
CPU 密集型计算（单个任务超过 5ms）无法切片，这时候该用 Web Worker。

---

## 我的看法

Fiber 是 React 最有深度的架构决策。它不只是性能优化，而是范式转变——从「埋头干活」到「会看脸色」。

这种思想影响了很多后来的框架。Vue 的响应式、Svelte 的编译时优化，都在解决这个问题。只是 Fiber 走得最远。
