# React Fiber 深度解析

> React 的旧引擎无法暂停。Fiber 教会了它如何呼吸。

---

## 30 秒心智模型

| React Fiber 概念 | 类比：厨房餐厅 |
|-----------------|--------------|
| Fiber 节点 | 任务分解卡 |
| Work Loop | 主厨的每日站会 |
| 时间切片 | 每盘菜做一半，去响应新客人 |
| 优先级 | VIP 客人优先上菜 |
| 双缓冲 | 备餐台和出餐台交替使用 |

---

## 目录

- [问题根源](#问题根源)
- [Fiber 核心原理](#fiber-核心原理)
- [两阶段工作模型](#两阶段工作模型)
- [时间切片](#时间切片)
- [优先级调度](#优先级调度)
- [实战应用](#实战应用)

---

## 问题根源

### 递归的代价

React 15 的 Stack Reconciler 用递归遍历组件树。一旦开始，必须跑完才能停。

想象厨房只有一个厨师：
- 1000 道菜的宴会
- 厨师必须做完一道再做下一道
- 客人中途加菜？对不起，等
- 用户界面卡死 300ms

这就是 React 15 遇到大组件树时的问题。

### 核心矛盾

JavaScript 是单线程。渲染和用户交互争抢同一资源。

```
旧方案：渲染 = 独占 CPU
新方案：渲染可以被"中断"，让交互先走
```

---

## Fiber 核心原理

### 从树到链表

Fiber 的关键洞察：**用数据结构代替调用栈来记录进度**。

```javascript
// 旧：递归（调用栈管理）
function reconcile(node) {
  process(node);
  node.children.forEach(child => reconcile(child));
}

// 新：循环（我们自己管理）
function workLoop() {
  while (workInProgress && !shouldYield()) {
    workInProgress = performUnitOfWork(workInProgress);
  }
}
```

### Fiber 节点结构

```javascript
{
  type: 'div',           // 组件类型
  child: fiberNode,      // 第一个子节点
  sibling: fiberNode,    // 下一个兄弟
  return: fiberNode,     // 父节点
  
  // 双缓冲
  alternate: oldFiber,    // 指向旧树对应节点
  
  // 优先级
  lanes: updateLane,      // 更新优先级
}
```

### 双缓冲机制

```
workInProgress 树（后台构建）←→ current 树（显示中）
        ↓                              ↑
    计算变更                      瞬间切换
```

这样做的好处：用户永远看到完整画面，没有中间状态闪烁。

---

## 两阶段工作模型

### Render Phase（可中断）

做计算，不碰 DOM：
- 调用组件函数
- Diff 对比
- 标记变更

### Commit Phase（不可中断）

应用 DOM 变更：
- 插入/删除节点
- 更新属性
- 执行 useEffect

> 想象装修房子：设计方案可以随时改，但一旦开始刷漆，就必须刷完。

---

## 时间切片

### 帧预算

浏览器 60 FPS = 每帧 16.7ms

```
┌──────────────────────────────────────┐
│ 0ms                            16.7ms │
├──────────────────────────────────────┤
│ React (~5ms)  │ 浏览器工作 │ 绘制   │
└──────────────────────────────────────┘
```

### shouldYield() 机制

```javascript
function shouldYield() {
  const deadline = getFrameDeadline();
  return getCurrentTime() >= deadline - 1;
}
```

每处理完一个 Fiber 节点，检查是否该让出主线程。

---

## 优先级调度

### Lane 位运算模型

```javascript
const SyncLane              = 0b0001;  // 用户点击
const TransitionLane        = 0b1000;  // 搜索输入
```

### 高优先级插队

```javascript
const [query, setQuery] = useState('');

<input onChange={e => {
  setQuery(e.target.value);              // 高优：立即响应
  startTransition(() => {
    setResults(search(e.target.value));   // 低优：可以打断
  });
}} />
```

---

## 实战应用

### 什么时候该关心 Fiber

| 场景 | 建议 |
|-----|------|
| 日常开发 | 了解概念，用好 useTransition |
| 大型列表 | 掌握 Key，用虚拟滚动 |
| 搜索/过滤 | 用 startTransition 标记低优更新 |
| 面试准备 | 掌握链表结构、双缓冲 |

### 常见误区

1. **Fiber ≠ 更快**：是更流畅，不是计算更快
2. **不是所有更新都中断**：只有 Render Phase 可以
3. **Time Slicing 有局限**：CPU 密集型计算无法切片

---

## 总结

1. **链表 + 循环** = 可中断的遍历
2. **两阶段** = 可撤销的计算 + 必须完成的 DOM 操作
3. **时间切片** = 让出主线程，保证交互
4. **Lane 优先级** = 智能调度，高优先行

Fiber 让 React 从"埋头干活"变成"会看脸色"——这才是现代 UI 框架该有的样子。
