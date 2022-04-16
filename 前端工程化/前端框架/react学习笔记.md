## React 理念

构建**快速响应**的大型 Web 应用程序。

制约快速响应的因素：

+ CPU 瓶颈：大计算量的操作或者设备性能不足使页面掉帧，导致卡顿
+ IO 瓶颈：发送网络请求后，由于需要等待数据返回才能进一步操作导致不能快速响应

应对措施：

+ CPU 瓶颈：控制 JS 脚本在一个帧中的执行时间，即将一个长更新任务拆分到每一帧中，每个帧中执行一小段任务（**时间切片**）。将**同步的更新变为可中断的异步更新**，避免更新任务阻塞浏览器渲染UI。
+ IO 瓶颈：在等待的数据返回之前，先显示指定的页面，待收到数据后再更新页面。将页面的**同步更新变为可中断的异步更新**。

### React 架构

`React16` 架构可以分为三层：

- Scheduler（调度器）—— 调度多种优先级的任务，高优任务优先进入**Reconciler**
- Reconciler（协调器）—— 负责找出变化的组件
- Renderer（渲染器）—— 负责将变化的组件渲染到页面上

相较于 `React15`，`React16` 中新增了 **Scheduler**



## 基本概念

### React Components

> 一种机制，允许我们将 UI 拆分为独立可复用的代码片段，并对每个片段进行独立构思。

它接收任意入参 props 作为输入，返回一个用于描述组件显示在屏幕上的内容的 React element。 

React 中组件模型类似于函数：**props** => **element tree**

React 提供了两种定义组件的方式：

+ `function`：无法使用(React 16前) **state**、**context**、**生命周期**等 React 组件特性。
+ `class`



### JSX

> 一种用于描述组件显示内容的标记语言，最终会被编译为生成 React Element 的 `React.creaetElement()`



### React Elements

> element 本质上是一个用于**描述** component 或 DOM 节点及其所需属性**的普通对象**，用来告诉React，你想要 component 或 DOM 节点在屏幕上显示为什么内容。

element 对象的特征：

+ 对象上没有方法，只有普通属性

+ 拥有特殊字段`$$typeof: Symbol.for('react.element')`，用于区别于其他对象
+ 用于描述 component 的 element 仍然是 element，就像描述 DOM 节点的 element 一样
+ element 之间可以相互嵌套和混合，构成 element tree
+ element 对象一经创建便不可变动

根据其描述的对象不同，可将 element 分为两大类：

+ DOM：`type` 属性值为一个 `DOM tag` 字符串，如‘div’、‘span’。
+ Component：`type` 属性值为一个关联 `function` 或者 `class` 对象的变量，变量名必须**首字母大写**。

生成 element 的方式：

+ `React.createElement()`：返回一个 element 对象
+ `JSX`（最终也会被编译为 `React.creaetElement()`）
+ `React.createFactory()`：返回一个生成给定类型 element 的 function



### Fiber节点

React 内部的一种数据结构，在组件 mount 时会根据组件返回的 React ELement 生成相应地 Fiber节点，最终映射到真实的 DOM 上。

```JavaScript
	  		React 声明式渲染系统
	  |-------------------------------|
JSX ——|——> React ELememt ————> Fiber——|——> DOM
	  |-------------------------------|
```





## 组件

组件是构建 React 应用的基本单元

### Class

> React 组件可以通过自定义 class 来实现，自定义的 class 需要继承组件基类 React.Component。

#### 实例属性

##### state

> this.state 包括组件自身所定义的数据，为一个普通 JavaScript 对象，对外不可见

+ setState：该方法会将对组件 state 的更改排入队列，然后**批量推迟**更新，React 将使用更新后的 state 重新渲染此组件及其子组件

  ```javascript
  setState(updater, [callback])
  ```

  参数一为带有形式参数的 `updater` 函数或对象类型：

  ```JavaScript
  (state, props) => stateChange || stateChange
  ```

  updater 函数中接收的 `state` 和 `props` 都保证为最新，stateChange 会与 `state` 进行浅合并。

  参数二为可选的回调函数，它将在 setState 完成合并并重新渲染组件后执行。

##### props

> this.props 包括被该组件调用者定义的 props，当组件的 props 发生变化时，就会触发组件更新

##### forceUpdate

> 当 render() 方法中依赖于 state、props 以外的数据时，需要调用 forceUpdate() 方法强制组件重新渲染。

#### render

> render() 方法是 class 组件中唯一必须实现的方法，返回的值决定了组件在屏幕上的显示内容。

该方法返回值可以是以下几种类型之一：

+ React 元素。通常通过 JSX 创建。
+ 数组或 fragments。使得 render 方法可以返回多个 React 元素。
+ Portals。可以渲染子节点到不同的 DOM 子树中。
+ 字符串或数值类型。它们在 DOM 中会被渲染为文本节点。
+ 布尔类型或 null、undefined。什么都不渲染。



#### 生命周期

<img src=".\react\微信截图_20200826143331.png" style="zoom:50%;" />

> 组件的整个生命周期在横向上可分为三个阶段：挂载（首次渲染），更新，卸载。
>
> 组件渲染的过程分为“Render”阶段和“Commit”阶段。
>
> 在组件生命周期的特殊时间点上会去调用特定的方法，这些方法被称为“生命周期方法”。
>
> ````
> React的架构遵循`schedule - render - commit`的运行流程，这个流程是 React 世界最底层的运行规律，而生命周期是为了介入 React 的运行流程而实现的更上层抽象。
> ````

##### 挂载

> 组件实例被创建并渲染到 DOM 中

组件挂载时，生命周期方法的调用顺序为：

+ **constructor()**
+ static getDerivedStateFromProps()
+ **render()**
+ **componentDidMount()**

##### 更新

> 组件首次渲染到 DOM 中后，当组件的 props 或 state 发生变化时（或调用 forceUpdate() ），就会触发组件更新

组件更新时，生命周期方法的调用顺序为：

+ static getDerivedStateFromProps()
+ shouldComponentUpdate()：**当该方法返回true时，才会继续更新，否则中断更新过程**
+ **render()**
+ getSnapshotBeforeUpdate()
+ **componentDidUpdate()**

##### 卸载

当组件从 DOM 中移除时会调用：

+ **componentWillUnmount()**

##### 错误处理

在生命周期的任何阶段，当有错误抛出时，会调用如下方法：

+ static getDerivedStateFromError()
+ componentDidCatch()



### Hook

> Hook 是一些可以让你在**函数组件**里“**钩入**”  React state 及生命周期等特性的**函数**，允许我们在编写非 class 组件的情况下，同样可以使用 state 以及其他的 React 特性。

#### 背景

在 Hook 出现前，如果我们想要使用诸如 `state`、`context`、生命周期等 React 特性时，只能在 class 组件中使用它们。但**使用 class 组件开发**，会带来**一些问题**：

+ 组件之间很难复用状态逻辑

  > 常用的状态逻辑复用方案过于复杂，React 没有为共享状态逻辑提供更好的原生途径。

+ 复杂组件变得难以理解

  > 复杂组件中状态逻辑和副作用众多，它们被包含在`componentDidMount` 和 `componentDidUpdate`等生命周期方法中，往往出现完全不相关的代码被放在同一个方法中，而相关联的代码被拆分到不同的方法中，导致逻辑不一致。

+ 难以理解的 class

  > class 的语法比较难理解，学习 class 语法的成本比较高

鉴于以上几个方面的问题，Hook 诞生了，它使得我们在非 class 组件中也能使用更多的 React 特性，拥抱 function 组件的开发方式。

#### 内置 Hook

##### State Hook

> 用于在函数组件中钩入 `state` 特性，与 class 组件中的 `this.state` 和 `this.setState` 相对应

`useState` 会返回一对值：**当前**状态和一个让你更新它的函数

`useState` 唯一的参数就是初始 `state`

语法：

```javascript
const [ stateName, setStateName ] = useState(stateIntialValue)
```

示例：

```javascript
function ExampleWithManyStates() {
  // 声明多个 state 变量！
  const [age, setAge] = useState(42);
  const [fruit, setFruit] = useState('banana');
  const [todos, setTodos] = useState([{ text: 'Learn Hooks' }]);
  // ...
}
```

注意：`useState` 只会在组件首次渲染时初始化状态值，后续组件更新会使用上一次的状态值。



##### Effect Hook

> 用于在函数组件中钩入操作副作用的能力，相当于`componentDidMount`，`componentDidUpdate` 和 `componentWillUnmount` 这三个生命周期函数的组合

语法：

```javascript
useEffect(func1 () {
    ...effect code
	return func2 () {
    ...clear effect code
	}     
}, [state1, state2...])
// func1会在组件每次渲染完成之后延迟执行，相当于componentDidMount和componentDidUpdate的组合
// 在effect中返回一个函数是可选的，func2会在组件卸载时执行（此外，每次渲染之后也会执行清除操作），相当于componentWillUnmount
```

执行机制：

+ 默认情况下，当组件**每次渲染完成**之后，React 会先执行 func2 对前一个 effect 进行清理，然后再执行 func1 调用新的 effect。
+ 第二个状态数组参数用于告诉 React，只有当这些状态发生改变时才需要执行 effect；传入空数组[]，相当于就告诉 React 你的 effect 不依赖于 props 或 state 中的任何值，所以它永远都不需要重复执行，仅在组件挂载和卸载时执行。

与 Class 对比：

+ 无需将作用于**相同的副作用**的逻辑代码拆分到`componentDidMount` 和 `componentWillUnmount`
+ 可以将不同用途的逻辑代码分离到不同的`effect`，无需将不相关的逻辑代码放到一个生命周期方法中
+ 不同于**生命周期方法**的**同步执行**，使用 `useEffect` 调度的 `effect` 是**异步执行**的，不会阻塞浏览器更新屏幕

优点：

+ 实现关注点分离，按照代码用途而非生命周期来分离代码，将不相关的逻辑分离到不同的 `effect` 中
+ 异步执行，性能更佳



##### Context Hook

> 



#### 自定义 Hook



#### Hook 使用规则

Hook 就是 JavaScript 函数，调用它们需要遵循以下两个规则：

+ 只能在**函数最外层**调用 Hook。不要在块作用域中或者子函数中调用。
+ 只能在 **React 的函数组件**中调用 Hook。不能在其他 JavaScript 函数中调用（自定义 Hook 中例外）。



### JSX

> 一种类似于 HTML 的语法，在 React 中被用来描述 React Element，执行时会被编译为 React.createElement(Element Type, props, ...children) 的调用

#### 元素类型

JSX 标签的第一部分指定了 React 元素的类型。JSX 元素可分为两类：

+ component：标签名以**大写字母**开头
+ DOM node：标签名以**小写字母**开头

标签名中可以使用点语法，但不能是一个表达式。

#### JSX 属性 Props

可以通过多种方式为 JSX 元素指定 props

+ 字符串字面量

+ JavaScript 表达式

  包裹在`{}`中的 JavaScript 表达式可以作为一个 prop 的值传递给 JSX 元素

+ 未赋值的 prop

  默认值为 true

+ 属性展开

  通过预展开算法`...`可以一次传递整个 pops 对象

#### JSX 中的子元素

包含在开始和结束标签之间的内容将作为特定属性 `props.children` 传递给外层组件。

有以下几种方式来传递子元素：

+ 字符串字面量

  此时 `props.children` 就只是该字符串

+ JSX 元素

  子元素可以由其他 JSX 元素组成

+ JavaScript 表达式

  JavaScript 表达式可以被包裹在`{}`中作为子元素

+ 函数

  函数同样可以作为子元素传递给自定义组件，只要确保在该组件渲染之前能够被转换成 React 理解的对象

JSX 中的子元素还可以是以上几种类型的组合。

**注意：**

`false`, `null`, `undefined`, and `true` 是合法的子元素。但它们并不会被渲染



## 原理

### <u>组件树渲染</u>

组件树最终渲染到 DOM 中的过程可以分为两个阶段：render阶段和commit阶段。

![](.\react\流程图\组件树渲染核心流程.png)

#### render阶段

> 创建各组件所对应的 Fiber 节点并构建 Fiber 树

##### 工作流程

```shell
render 入口（根据本次更新是同步还是异步调用不同方法`performSyncWorkOnRoot` 或 `performConcurrentWorkOnRoot`）
 	|
 	|
    v
进入循环，开始递归构建 Fiber 树（根据本次更新是同步还是异步调用不同方法`workLoopSync` 或 `workLoopConcurrent(可中断递归)`）
    |
    |
    v
执行循环体（`performUnitOfWork`)：performUnitOfWork的工作可以分为两部分：“递”和“归”
    |
    |
    V
“递”阶段（`beginWork`）：从 rootFiber 开始向下深度优先遍历，为遍历到的每个 Fiber 节点调用 beginWork 方法，该方法会根据传入的 Fiber 节点创建子 Fiber 节点，并将这两个 Fiber 节点连接起来，当遍历到叶子节点时就会进入“归”阶段 
    |
    |
    v
“归”阶段（`completeWork`）：当一个 Fiber 节点执行完 completeWork，如果其存在兄弟 Fiber 节点，会进入父级 Fiber 的“递”阶段
    |
    |
    v
构建完成：“递”和“归”阶段会交错执行直到“归”到 rootFiber
```



##### beginWork

![](.\react\流程图\beginWork工作流程.png)

##### completeWork

![](.\react\completeWork.png)





#### commit阶段

> 根据 render 阶段构建的 Fiber 树执行 DOM 操作（**同步执行**），更新 DOM 树

在 `rootFiber.firstEffect` 上保存了一条需要执行副作用的 Fiber 节点的单向链表 `effectList`，这些 Fiber 节点的 `updateQueue` 中保存了变化的 `props`。这些副作用对应的DOM操作、一些生命周期钩子（比如`componentDidXXX`）、`hook`（比如`useEffect`）在 commit 阶段执行。

##### 工作流程

commit 阶段的主要工作（即 Renderer 的工作流程）分为三部分：

```bash
commit 入口（fiberRootNode 作为传参调用`commitRoot(root)`）
 	|
 	|
    v
before mutation之前（变量赋值、状态重置）
    |
    |
    v
before mutation阶段（执行DOM操作前）
    |
    |
    v
mutation阶段（执行DOM操作）
    |
    |
    v
layout阶段（执行DOM操作后）
```

##### before mutation阶段



##### mutation阶段



##### layout阶段





### 更新流程

```sh
触发状态更新（根据场景调用不同方法）
 	|
 	|
    v
产生更新：创建Update对象并加入updateQueue，调度update：方法内部调用createUpdate、enqueueUpdate方法完成update的创建、入队。
    |
    |
    V
调度准备：在完成update的创建和入队后，接下来将进入`scheduleUpdateOnFiber`开始真正的更新任务调度流程。
    |
    |
    v
任务调度协调（`ensureRootIsScheduled`）：确保更新任务能够被正确的调度。
    |
    |
    v
render阶段（`performSyncWorkOnRoot` 或 `performConcurrentWorkOnRoot`）
    |
    |
    v
commit阶段（`commitRoot`）
```

![](.\react\流程图\产生更新任务流程.png)

#### 产生更新

在`React`中，有如下方法可以触发更新流程（排除`SSR`相关）：

- `ReactDOM.render` —— `HostRoot`
- `this.setState` —— `ClassComponent`
- `this.forceUpdate` —— `ClassComponent`
- `useState` —— `FunctionComponent`
- `useReducer` —— `FunctionComponent`

以`setState`为例，当调用`setstate`时，意味着组件对应的fiber节点产生了一个更新。在`setstate`内，会调用`enqueueSetState`。

```javascript
Component.prototype.setState = function(partialState, callback) {
  this.updater.enqueueSetState(this, partialState, callback, 'setState');
};
```

`enqueueSetState`的职责是创建update对象，将它入队fiber节点的update链表（`updateQueue`），然后发起调度。

```javascript
 enqueueSetState(inst, payload, callback) {
    // 获取当前触发更新的fiber节点。inst是组件实例
    const fiber = getInstance(inst);
    // eventTime是当前触发更新的时间戳
    const eventTime = requestEventTime();
    const suspenseConfig = requestCurrentSuspenseConfig();

    // 获取本次update的优先级
    const lane = requestUpdateLane(fiber, suspenseConfig);

    // 创建update对象
    const update = createUpdate(eventTime, lane, suspenseConfig);

    // payload就是setState的参数，回调函数或者是对象的形式。
    // 处理更新时参与计算新状态的过程
    update.payload = payload;

    // 将update放入fiber的updateQueue
    enqueueUpdate(fiber, update);

    // 开始进行调度
    scheduleUpdateOnFiber(fiber, lane, eventTime);
  }
```

##### 计算更新优先级

```javascript
const lane = requestUpdateLane(fiber, suspenseConfig);
```

事件触发时，合成事件机制调用scheduler中的`runWithPriority`函数，目的是以该交互事件对应的事件优先级去派发真正的事件流程。`runWithPriority`会将事件优先级转化为scheduler内部的优先级并记录下来。当调用`requestUpdateLane`计算lane的时候，会去获取scheduler中的优先级，以此作为lane计算的依据。



#### 调度准备

在完成update对象的创建和入队后，接下来会进入`scheduleUpdateOnFiber`，开始真正的任务调度流程。通过调用`scheduleUpdateOnFiber`，构建`workInProcess`树的任务会被调度执行，在这个过程中，fiber上的`updateQueue`会被处理。

在`scheduleUpdateOnFiber`中，它会区分update的lane，将同步更新和异步更新分流，让二者进入各自的流程。但在此之前，还需要做一些准备工作：

+ 检查是否是无限更新，例如在render函数中调用了`setState`。
+ 从产生更新的fiber节点开始，往上一直遍历到root，目的是将`fiber.lanes`一直向上收集，收集到父级节点的`childLanes`中，`childLanes`是识别这个fiber子树是否需要更新的关键。
+ 在root上标记更新，也就是将当前update的lane加入到`root.pendingLanes`中，每次渲染的优先级基准：`renderLanes`就是取自`root.pendingLanes`中最紧急的那一部分lanes。

```javascript
export function scheduleUpdateOnFiber(
  fiber: Fiber,
  lane: Lane,
  eventTime: number,
) {
  // 第一步，检查是否有无限更新
  checkForNestedUpdates();

  ...
  // 第二步，向上收集fiber.childLanes
  const root = markUpdateLaneFromFiberToRoot(fiber, lane);

  ...

  // 第三步，在root上标记更新，将update的lane放到root.pendingLanes
  markRootUpdated(root, lane, eventTime);

  ...

  // 根据Scheduler的优先级获取到对应的React优先级
  const priorityLevel = getCurrentPriorityLevel();

  if (lane === SyncLane) {
    // 本次更新是同步的，例如传统的同步渲染模式
    if (
      (executionContext & LegacyUnbatchedContext) !== NoContext &&
      (executionContext & (RenderContext | CommitContext)) === NoContext
    ) {
      // 如果是本次更新是同步的，并且当前还未渲染，意味着主线程空闲，并没有React的
      // 更新任务在执行，那么调用performSyncWorkOnRoot开始执行同步任务

      ...

      performSyncWorkOnRoot(root);
    } else {
      // 如果是本次更新是同步的，不过当前有React更新任务正在进行，
      // 而且因为无法打断，所以调用ensureRootIsScheduled
      // 目的是去复用已经在更新的任务，让这个已有的任务
      // 把这次更新顺便做了
      ensureRootIsScheduled(root, eventTime);
      if ( executionContext === NoContext ) {
        // Flush the synchronous work now, unless we're already working or inside
        // a batch. This is intentionally inside scheduleUpdateOnFiber instead of
        // scheduleCallbackForFiber to preserve the ability to schedule a callback
        // without immediately flushing it. We only do this for user-initiated
        // updates, to preserve historical behavior of legacy mode.
        resetRenderTimer();
        flushSyncCallbackQueue();
      }
    }
  } else {
    ...
    // Schedule other updates after in case the callback is sync.
    // 如果更新是异步的，调用ensureRootIsScheduled去进入异步调度
    ensureRootIsScheduled(root, eventTime);
    schedulePendingInteractions(root, lane);
  }

  ...
}
```

在经过了前面的准备工作后，`scheduleUpdateOnFiber`最终会调用`ensureRootIsScheduled`，决定更新任务如何被调度。



#### 任务调度

##### 任务本质

一个update的产生最终会使React在内存中根据`current fiber`树构建`workInProcess fiber`树，新的state的计算、diff操作以及一些生命周期函数的调用，都会在这个构建过程中进行。这个**整体的构建过程**被称为**render阶段**，这个**render阶段整体**就是一个完整的**React更新任务**（这个递归构建`workInProcess fiber`树的任务分为若干小任务，每个小任务负责一个fiber节点的处理。任务在执行过程中顺便收集了每个 fiber节点的副作用，将有副作用的节点通过 `firstEffect`、`lastEffect`、`nextEffect` 形成一条副作用单链表，在接下来的commit阶段就通过遍历副作用链完成 DOM 更新），更新任务可以看作一个**函数**，这个函数在concurrent模式下就是`performConcurrentWorkOnRoot`，**更新任务的调度**可以看成是这个**函数**被**Scheduler**按照**任务优先级**安排它**何时执行**。

> 注：Scheduler的调度和React的调度是两个完全不同的概念，React的调度是协调任务进入哪种Scheduler的调度模式，它的调度并不涉及任务的执行，而Scheduler是实打实地执行任务。

当一个任务被调度之后，scheduler就会生成一个任务对象（task），它的结构如下所示：

```javascript
var newTask = {
    id: taskIdCounter++,
    // 任务函数，也就是 performConcurrentWorkOnRoot
    callback,
    // 任务调度优先级
    priorityLevel,
    // 任务开始执行的时间点
    startTime,
    // 任务的过期时间
    expirationTime,
    // 在小顶堆任务队列中排序的依据
    sortIndex: -1,
};
```

每当生成了一个这样的任务，它就会被挂载到root节点的`callbackNode`属性上，以表示当前已经有任务被调度了，同时任务的优先级也会被存储到root的`callbackPriority`上，表示如果有新的任务进来，必须用它的任务优先级和已有任务的优先级（`root.callbackPriority`）比较，来决定是否有必要取消当前正在执行的任务。



##### 任务优先级

`状态更新`由`用户交互`产生，用户心里对`交互`执行顺序有个预期。`React`根据`人机交互研究的结果`中用户对`交互`的预期顺序为`交互`产生的`状态更新`赋予不同优先级。

任务本身是由更新产生的，因此任务优先级本质上是和update的优先级，即`updata.lane`有关（只是有关，不一定是由它而来）。得出的任务优先级属于`lanePriority`，它不是update的lane，而且与Scheduler内部的优先级是两个概念。

在调度准备时，`update.lane`会被加入到`root.pendingLanes`中，随后会取`root.pendingLanes`中最紧急的那部分lanes作为`renderLanes`。任务优先级的生成就发生在计算`renderLanes`的阶段，**任务优先级其实就是`renderLanes`对应的`lanePriority`**。

> `root.pendingLanes`，包含了当前fiber树中所有待处理的update的lane。

任务优先级有三类：

- 同步优先级：React传统的同步渲染模式产生的更新任务所持有的优先级
- 同步批量优先级：同步模式到concurrent模式过渡模式：blocking模式产生的更新任务所持有的优先级
- concurrent模式下的优先级：concurrent模式产生的更新持有的优先级

**任务优先级**决定着任务**在React中被如何处理**，而由任务优先级转化成的**任务调度优先级**（上面给出的Scheduler的task结构中的`priorityLevel`），决定着**Scheduler何时去处理这个任务**。



##### 任务调度协调

React对任务的调度本质上是以任务优先级为基准，去操作多个或单个任务。

+ 多个任务时，相对于新任务，会对现有任务进行**或复用**，**或取消**的操作。
+ 单个任务时，对任务进行**或同步**，**或异步**，**或批量同步**的调度决策。

这种行为可以看成是一种任务协调机制，这种协调通过`ensureRootIsScheduled`去实现。

在做出调度决策前，先获取了本次任务调度协调所需要的`renderLanes`和任务优先级。接下来是协调任务调度的过程：

+ 首先判断**是否有必要**发起一次新的任务调度，方法是通过比较新任务的优先级和旧任务的优先级
  + 相等，则说明无需再发起一次调度，直接复用旧任务即可，让旧任务在处理更新的时候把新任务一起做了。
  + 不相等，则说明新任务的优先级一定高于旧任务（这是因为获取任务优先级的时候，都只获取`root.pendingLanes`中最紧急的那部分lanes对应的优先级，低优先级的update持有的lane对应的优先级是无法被获取到的。），这种情况就是**高优先级任务插队**，需要把旧任务取消掉。
+ **需要调度一个新任务（不存在旧任务或存在旧任务但新任务优先级更高）**，根据任务的任务优先级决定以哪种模式调度任务：
  - 同步优先级：调用`scheduleSyncCallback`去同步执行任务。
  - 同步批量执行：调用`scheduleCallback`将任务以立即执行的优先级去加入调度。
  - 属于concurrent模式的优先级：调用`scheduleCallback`将任务以上面获取到的新任务优先级去加入调度。

三种任务优先级分别对应了三种调度模式：

- 同步优先级：传统的React同步渲染模式和过期任务的调度。通过React提供的`scheduleSyncCallback`函数将任务函数**`performSyncWorkOnRoot`**加入到React自己的同步队列（`syncQueue`）中，之后以`ImmediateSchedulerPriority`的优先级将循环执行`syncQueue`的函数加入到Scheduler中，目的是让任务在**下一次事件循环**中被执行掉。但是因为React的控制，这种模式下的时间片会在任务都执行完之后再去检查，表现为没有时间片。
- 同步批量执行：同步渲染模式到concurrent渲染模式的过渡模式blocking模式，会将任务函数**`performSyncWorkOnRoot`**以`ImmediateSchedulerPriority`的优先级加入到Scheduler中，也是让任务在**下一次事件循环**中被执行掉，也不会有时间片的表现。
- 属于concurrent模式的优先级：将任务函数**`performConcurrentWorkOnRoot`**以任务自己的优先级加入到Scheduler中，Scheduler内部的会通过这个优先级控制该任务在Scheduler内部任务队列中的排序，从而决定任务何时被执行，而且任务真正执行时会有时间片的表现。

```javascript
function ensureRootIsScheduled(root: FiberRoot, currentTime: number) {
  // 获取旧任务
  const existingCallbackNode = root.callbackNode;

  // 记录任务的过期时间，检查是否有过期任务，有则立即将它放到root.expiredLanes，
  // 便于接下来将这个任务以同步模式立即调度
  markStarvedLanesAsExpired(root, currentTime);

  // 获取renderLanes
  const nextLanes = getNextLanes(
    root,
    root === workInProgressRoot ? workInProgressRootRenderLanes : NoLanes,
  );

  // 获取renderLanes对应的任务优先级
  const newCallbackPriority = returnNextLanesPriority();

  if (nextLanes === NoLanes) {
    // 如果渲染优先级为空，则不需要调度
    if (existingCallbackNode !== null) {
      cancelCallback(existingCallbackNode);
      root.callbackNode = null;
      root.callbackPriority = NoLanePriority;
    }
    return;
  }

  // 如果存在旧任务，那么看一下能否复用
  if (existingCallbackNode !== null) {

    // 获取旧任务的优先级
    const existingCallbackPriority = root.callbackPriority;

    // 如果新旧任务的优先级相同，则无需调度
    if (existingCallbackPriority === newCallbackPriority) {
      return;
    }
    // 代码执行到这里说明新任务的优先级高于旧任务的优先级
    // 取消掉旧任务，实现高优先级任务插队
    cancelCallback(existingCallbackNode);
  }

  // 调度一个新任务
  let newCallbackNode;
  if (newCallbackPriority === SyncLanePriority) {

    // 若新任务的优先级为同步优先级，则同步调度，传统的同步渲染和过期任务会走这里
    newCallbackNode = scheduleSyncCallback(
      performSyncWorkOnRoot.bind(null, root),
    );
  } else if (newCallbackPriority === SyncBatchedLanePriority) {

    // 同步模式到concurrent模式的过渡模式：blocking模式会走这里
    newCallbackNode = scheduleCallback(
      ImmediateSchedulerPriority,
      performSyncWorkOnRoot.bind(null, root),
    );
  } else {
    // concurrent模式的渲染会走这里

    // 根据任务优先级获取Scheduler的调度优先级
    const schedulerPriorityLevel = lanePriorityToSchedulerPriority(
      newCallbackPriority,
    );

    // 计算出调度优先级之后，开始让Scheduler调度React的更新任务
    newCallbackNode = scheduleCallback(
      schedulerPriorityLevel,
      performConcurrentWorkOnRoot.bind(null, root),
    );
  }

  // 更新root上的任务优先级和任务，以便下次发起调度时候可以获取到
  root.callbackPriority = newCallbackPriority;
  root.callbackNode = newCallbackNode;
}
```

`ensureRootIsScheduled`实际上是在任务调度层面整合了高优先级任务的插队和任务饥饿问题的关键逻辑，这只是宏观层面的决策，决策背后的原因是React处理更新时对于不同优先级的update的取舍以及对`root.pendingLanes`的标记操作。



#### 处理更新

一旦有更新产生，update对象就会被放入`updateQueue`并挂载到fiber节点上。构建fiber树时，会带着`renderLanes`去处理`updateQueue`，在`beginWork`阶段，对于类组件会调用`processUpdateQueue`函数，逐个处理这个链表上的每个update对象，计算新的状态，一旦update持有的优先级不够，那么就会跳过这个update的处理，并把这个被跳过的update的lane放到`fiber.lanes`中，好在`completeWork`阶段收集起来。

##### 收集未被处理的lane

在`completeUnitOfWork`的时候，`fiber.lanes` 和 `childLanes`被一层一层收集到父级fiber的`childLanes`中，该过程发生在`completeUnitOfWork`函数中调用的`resetChildLanes`，它循环fiber节点的子树，将子节点及其兄弟节点中的lanes和`childLanes`收集到当前正在complete阶段的fiber节点上的`childLanes`。

假设第3层中的`<List/>`和`<Table/>`组件都分别有update因为优先级不够而被跳过，那么在它们父级的div fiber节点completeUnitOfWork的时候，会调用`resetChildLanes`
把它俩的lanes收集到div `fiber.childLanes`中，最终把所有的lanes收集到`root.pendingLanes`。

```maxima
                                    root（pendingLanes: 0b01110）
                                     |
  1                                  App
                                     |
                                     |
  2 compeleteUnitOfWork-----------> div （childLanes: 0b01110）
                                     /
                                    /
  3                              <List/> ---------> <Table/> --------> p
                            （lanes: 0b00010）   （lanes: 0b00100）
                         （childLanes: 0b01000）       /
                                 /                   /
                                /                   /
  4                            p                   ul
                                                  /
                                                 /
                                                li ------> li
```

在每一次往上循环的时候，都会调用resetChildLanes，目的是将fiber.childLanes层层收集。

```javascript
function completeUnitOfWork(unitOfWork: Fiber): void {
  // 已经结束beginWork阶段的fiber节点被称为completedWork
  let completedWork = unitOfWork;

  do {
    // 向上一直循环到root的过程
    ...

    // fiber节点的.flags上没有Incomplete，说明是正常完成了工作
    if ((completedWork.flags & Incomplete) === NoFlags) {

      ...
      // 调用resetChildLanes去收集lanes
      resetChildLanes(completedWork);

      ...

    } else {/*...*/}

    ...

  } while (completedWork !== null);

  ...

}
```

resetChildLanes中只收集当前正在complete的fiber节点的子节点和兄弟节点的lanes以及childLanes：

```javascript
function resetChildLanes(completedWork: Fiber) {

  ...

  let newChildLanes = NoLanes;

  if (enableProfilerTimer && (completedWork.mode & ProfileMode) !== NoMode) {
    // profile相关，无需关注
  } else {
    // 循环子节点和兄弟节点，收集lanes
    let child = completedWork.child;
    while (child !== null) {
      // 收集过程
      newChildLanes = mergeLanes(
        newChildLanes,
        mergeLanes(child.lanes, child.childLanes),
      );
      child = child.sibling;
    }
  }
  // 将收集到的lanes放到该fiber节点的childLanes中
  completedWork.childLanes = newChildLanes;
}
```

最后将这些收集到的childLanes放到root.pendingLanes的过程，是发生在本次更新的commit阶段中，因为render阶段的渲染优先级来自root.pendingLanes，不能随意地修改它。所以要在render阶段之后的commit阶段去修改。我们看一下commitRootImpl中这个过程的实现：

```javascript
function commitRootImpl(root, renderPriorityLevel) {

  // 将收集到的childLanes，连同root自己的lanes，一并赋值给remainingLanes
  let remainingLanes = mergeLanes(finishedWork.lanes, finishedWork.childLanes);
  // markRootFinished中会将remainingLanes赋值给remainingLanes
  markRootFinished(root, remainingLanes);

  ...

}
```

##### 重新发起调度

至此，我们将低优先级任务的lane重新收集到了`root.pendingLanes`中，这时只需要再发起一次调度就可以了，通过在commit阶段再次调用`ensureRootIsScheduled`去实现，这样就又会走一遍调度的流程，低优先级任务被执行。

```javascript
function commitRootImpl(root, renderPriorityLevel) {

  // 将收集到的childLanes，连同root自己的lanes，一并赋值给remainingLanes
  let remainingLanes = mergeLanes(finishedWork.lanes, finishedWork.childLanes);
  // markRootFinished中会将remainingLanes赋值给remainingLanes
  markRootFinished(root, remainingLanes);

  ...

  // 在每次所有更新完成的时候都会调用这个ensureRootIsScheduled
  // 以保证root上任何的pendingLanes都能被处理
  ensureRootIsScheduled(root, now());

}
```



### 状态计算

一旦用户的交互产生了更新，那么就会产生一个update对象去承载新的状态，多个update会连接在一起形成一个环状链表：`updateQueue`，挂载在fiber节点上，然后在该fiber节点的`beginWork`阶段会循环该`updateQueue`，依次处理其中的update，这是计算组件状态的大致过程。

每个触发更新的方法，React 都会为之创建一个相对应的 Update 对象，并把它加入`updateQueue`。

假设B节点产生了更新，那么B节点的`updateQueue`最终会是是如下的形态：

```coq
         A 
        /
       /
      B ----- updateQueue.shared.pending = update————
     /                                       ^       |
    /                                        |_______|
   C -----> D
 
```

`updateQueue.shared.pending`中存储着连接update的环状链表。

#### Update

##### 类型

触发更新的方法所隶属的组件一共有三种（`HostRoot` | `ClassComponent` | `FunctionComponent`）。由于不同类型的组件工作方式不同，所以存在两种不同结构的`Update`，其中：

+ `ClassComponent`与`HostRoot`共用一套`Update`结构
+ `FunctionComponent`单独使用一种`Update`结构

##### 结构

`ClassComponent`与`HostRoot`共用的`Update`结构

```typescript
type Update<State> = {
  // TODO: Temporary field. Will remove this by storing a map of
  // transition -> event time on the root.
  eventTime: number,
  lane: Lane,
  suspenseConfig: null | SuspenseConfig,

  tag: 0 | 1 | 2 | 3,
  payload: any,
  callback: (() => mixed) | null,

  next: Update<State> | null,
};
```

字段意义如下：

- `eventTime`：update的产生时间，通过`performance.now()`获取的毫秒数，若该update一直因为优先级不够而得不到执行，那么它会超时，此时React会立刻发起一次调度，将它处理掉。
- `lane`：update的优先级，即更新优先级，当前update对象能否被处理取决于它的优先级是否在本次的渲染优先级中。
- `suspenseConfig`：`Suspense`相关。
- `tag`：更新的类型，包括`UpdateState` | `ReplaceState` | `ForceUpdate` | `CaptureUpdate`。
- `payload`：更新挂载的数据，不同类型组件挂载的数据不同。
  - 类组件中：有两种可能，对象（{}），和函数`（(prevState, nextProps):newState => {}）`
  - 根组件中：是`React.element`，即`ReactDOM.render`的第一个参数
- `callback`：更新的回调函数。
- `next`：指向下一个update的指针。

`FunctionComponent`单独使用的`Update`结构

```typescript
type Update<S, A> = {
  // TODO: Temporary field. Will remove this by storing a map of
  // transition -> start time on the root.
  eventTime: number,
  lane: Lane,
  suspenseConfig: null | SuspenseConfig,
  action: A,
  eagerReducer: ((S, A) => S) | null,
  eagerState: S | null,
  next: Update<S, A>,
  priority?: ReactPriorityLevel,
};
```



##### 与Fiber的联系

类似`Fiber节点`组成`Fiber树`，`Fiber节点`上的多个`Update`会组成链表并被包含在`fiber.updateQueue`中。

`Fiber节点`最多同时存在两个`updateQueue`：

- `current fiber`保存的`updateQueue`即`current updateQueue`
- `workInProgress fiber`保存的`updateQueue`即`workInProgress updateQueue`

在`commit阶段`完成页面渲染后，`workInProgress Fiber树`变为`current Fiber树`，`workInProgress Fiber树`内`Fiber节点`的`updateQueue`就变成`current updateQueue`。



#### updateQueue

`updateQueue`有三种类型，其中一种针对`HostComponent`的类型，剩下两种类型和`Update`的两种类型对应。

`ClassComponent`与`HostRoot`使用的`UpdateQueue`结构（组件对应的Fiber节点上的`updateQueue`属性）如下：

```typescript
type SharedQueue<State> = {
  pending: Update<State> | null,
};

type UpdateQueue<State> = {
  baseState: State,
  firstBaseUpdate: Update<State> | null,
  lastBaseUpdate: Update<State> | null,
  shared: SharedQueue<State>,
  effects: Array<Update<State>> | null,
};
```

字段意义如下：

- `baseState`：前一次更新计算得出的状态，它是第一个被跳过的update之前的那些update计算得出的state。会以它为基础计算本次的state。
- `firstBaseUpdate`：前一次更新时`updateQueue`中第一个被跳过的update对象。
- `lastBaseUpdate`：前一次更新中，`updateQueue`中以第一个被跳过的update为起点一直到的最后一个update截取的队列中的最后一个update。
- `shared.pending`：存储着本次更新的update队列，是实际的`updateQueue`。shared的意思是current节点与`workInProgress`节点共享一条更新队列。
- `effects`：数组。保存`update.callback !== null`的`Update`。

`FunctionComponent`单独使用的`UpdateQueue`结构（注意：该`UpdateQueue` 指的是`useState/useReducer`对应Hook数据结构上的`queue`属性，而非组件对应的Fiber节点数据结构上的`updateQueue`属性）

```typescript
type UpdateQueue<S, A> = {
  pending: Update<S, A> | null,
  dispatch: (A => mixed) | null,
  lastRenderedReducer: ((S, A) => S) | null,
  lastRenderedState: S | null,
};
```



#### 处理机制

处理更新分为三个阶段：准备阶段、处理阶段、完成阶段。前两个阶段主要是处理`updateQueue`，最后一个阶段是将新计算的state赋值到fiber上。

##### 准备阶段

整理`updateQueue`。由于优先级的原因，会使得低优先级更新被跳过等待下次执行，这个过程中，又有可能产生新的update。所以当处理某次更新的时候，有可能会有两条update队列：**上次遗留的和本次新增的**。**上次遗留的**就是从`firstBaseUpdate` 到 `lastBaseUpdate` 之间的所有update；**本次新增的**就是新产生的那些的update。

准备阶段主要是将两条队列合并起来，并且合并之后的队列不再是环状的，目的方便从头到尾遍历处理。另外，由于以上的操作都是处理的`workInProgress`节点的`updateQueue`，所以还需要在current节点也操作一遍，保持同步，目的是在渲染被高优先级的任务打断后，再次以current节点为原型新建`workInProgress`节点时，不会丢失之前尚未处理的update。



##### 处理阶段

循环处理上一步整理好的更新队列。这里有两个重点：

- 本次更新update是否被处理取决于它的优先级（`update.lane`）和渲染优先级（`renderLanes`）。
- 本次更新的计算结果基于`baseState`。

###### 优先级不足

优先级不足的update会被跳过，除了跳过之外，还做了三件事：

1. 将被跳过的update放到`firstBaseUpdate` 和 `lastBaseUpdate`组成的链表中，（就是`baseUpdate`），等待下次处理低优先级更新的时候再处理。
2. 记录`baseState`，此时的`baseState`为该低优先级update之前所有已被处理的更新的结果，并且只在第一次跳过时记录，因为低优先级任务重做时，要从第一个被跳过的更新开始处理。
3. 将被跳过的update的优先级记录下来，更新过程即将结束后放到`workInProgress.lanes`中，这点是调度得以再次发起，进而重做低优先级任务的关键。

```sql
第一次更新的 baseState 是空字符串，更新队列如下，字母表示state，数字表示优先级。优先级是1 > 2的

 A1 - B1 - C2 - D1 - E2
 
 第一次的渲染优先级（renderLanes）为 1，Updates是本次会被处理的队列:
 Base state: ''
 Updates: [A1, B1, D1]      <- 第一个被跳过的update为C2，此时的baseUpdate队列为[C2, D1, E2]，
                             它之前所有被处理的update的结果是AB。此时记录下baseState = 'AB'
                             注意！再次跳过低优先级的update(E2)时，则不会记录baseState
                             
 Result state: 'ABD'--------------------------------------------------------------------------------------------------
 
 
 第二次的渲染优先级（renderLanes）为 2，Updates是本次会被处理的队列:
 Base state: 'AB'           <- 再次发起调度时，取出上次更新遗留的baseUpdate队列，基于baseState
                             计算结果。
                             
 Updates: [C2, D1, E2] Result state: 'ABCDE'
```

###### 优先级足够

如果某个update优先级足够，主要是两件事：

1. 判断若`baseUpdate`队列不为空（之前有被跳过的update），则将现在这个update加入`baseUpdate`队列。
2. 处理更新，计算新状态。

将优先级足够的update放入`baseUpdate`这一点可以和上边低优先级update入队`baseUpdate`结合起来看。这实际上意味着一旦有update被跳过，就以它为起点，将后边直到最后的update无论优先级如何都截取下来。



##### 完成阶段

主要是做一些赋值和优先级标记的工作。

- 赋值`updateQueue.baseState`。若此次render没有更新被跳过，那么赋值为新计算的state，否则赋值为第一个被跳过的更新之前的update。
- 赋值`updateQueue` 的 `firstBaseUpdate` 和 `lastBaseUpdate`，也就是如果本次有更新被跳过，则将被截取的队列赋值给`updateQueue`的`baseUpdate`链表。
- 更新`workInProgress`节点的lanes。更新策略为如果没有优先级被跳过，则意味着本次将update都处理完了，lanes清空。否则将低优先级update的优先级放入lanes，此处是再发起一次调度重做低优先级任务的关键。
- 更新`workInProgress`节点上的`memoizedState`。

源码实现：

`processUpdateQueue`函数的功能是处理更新队列，它之所以能够在保证更新按照优先级被处理的同时，不出差错，是因为它遵循一套固定的规则：优先级被跳过后，记住此时的状态和此优先级之后的更新队列，并将队列备份到current节点，这对于update对象按次序、完整地被处理至关重要，也保证了最终呈现的处理结果和用户的行为触发的交互的结果保持一致。

```javascript
function processUpdateQueue<State>(
 workInProgress: Fiber, props: any, instance: any, renderLanes: Lanes,): void {
 // 准备阶段----------------------------------------
 // 从workInProgress节点上取出updateQueue
 // 以下代码中的queue就是updateQueue
 const queue: UpdateQueue<State> = (workInProgress.updateQueue: any);
 // 取出queue上的baseUpdate队列（下面称遗留的队列），然后
 // 准备接入本次新产生的更新队列（下面称新队列）
 let firstBaseUpdate = queue.firstBaseUpdate;
 let lastBaseUpdate = queue.lastBaseUpdate;
 // 取出新队列
 let pendingQueue = queue.shared.pending;
 // 下面的操作，实际上就是将新队列连接到上次遗留的队列中。
 if (pendingQueue !== null) { queue.shared.pending = null;
 // 取到新队列
 const lastPendingUpdate = pendingQueue; const firstPendingUpdate = lastPendingUpdate.next;
 // 将遗留的队列最后一个元素指向null，实现断开环状链表
 // 然后在尾部接入新队列
 lastPendingUpdate.next = null;
 if (lastBaseUpdate === null) {
 firstBaseUpdate = firstPendingUpdate;
 } else {
 // 将遗留的队列中最后一个update的next指向新队列第一个update
 // 完成接入
 lastBaseUpdate.next = firstPendingUpdate; } // 修改遗留队列的尾部为新队列的尾部
 lastBaseUpdate = lastPendingUpdate;
 // 用同样的方式更新current上的firstBaseUpdate 和
 // lastBaseUpdate（baseUpdate队列）。
 // 这样做相当于将本次合并完成的队列作为baseUpdate队列备份到current节
 // 点上，因为如果本次的渲染被打断，那么下次再重新执行任务的时候，workInProgress节点复制
 // 自current节点，它上面的baseUpdate队列会保有这次的update，保证update不丢失。
 const current = workInProgress.alternate;
 if (current !== null) {
 // This is always non-null on a ClassComponent or HostRoot
   const currentQueue:UpdateQueue<State> = (current.updateQueue: any);
   const currentLastBaseUpdate = currentQueue.lastBaseUpdate;
   if (currentLastBaseUpdate !== lastBaseUpdate) {
     if (currentLastBaseUpdate === null) {
       currentQueue.firstBaseUpdate = firstPendingUpdate;
     } else {
       currentLastBaseUpdate.next = firstPendingUpdate;
     }
     currentQueue.lastBaseUpdate = lastPendingUpdate;
   }
 }
 }
 // 至此，新队列已经合并到遗留队列上，firstBaseUpdate作为
 // 这个新合并的队列，会被循环处理
 // 处理阶段-------------------------------------
 if (firstBaseUpdate !== null) { // 取到baseState
 let newState = queue.baseState;
 // 声明newLanes，它会作为本轮更新处理完成的
 // 优先级，最终标记到WIP节点上
 let newLanes = NoLanes;
 // 声明newBaseState，注意接下来它被赋值的时机，还有前置条件：
 // 1. 当有优先级被跳过，newBaseState赋值为newState，
 // 也就是queue.baseState
 // 2. 当都处理完成后没有优先级被跳过，newBaseState赋值为
 // 本轮新计算的state，最后更新到queue.baseState上
 let newBaseState = null;
 // 使用newFirstBaseUpdate 和 newLastBaseUpdate // 来表示本次更新产生的的baseUpdate队列，目的是截取现有队列中
 // 第一个被跳过的低优先级update到最后的所有update，最后会被更新到
 // updateQueue的firstBaseUpdate 和 lastBaseUpdate上
 // 作为下次渲染的遗留队列（baseUpdate）
 let newFirstBaseUpdate = null;
 let newLastBaseUpdate = null;
 // 从头开始循环
 let update = firstBaseUpdate;
 do {
   const updateLane = update.lane;
   const updateEventTime = update.eventTime;
   
   // isSubsetOfLanes函数的意义是，判断当前更新的优先级（updateLane）
   // 是否在渲染优先级（renderLanes）中如果不在，那么就说明优先级不足
   if (!isSubsetOfLanes(renderLanes, updateLane)) {
     const clone: Update<State> = {
     eventTime: updateEventTime,
     lane: updateLane,
     suspenseConfig: update.suspenseConfig,
     tag: update.tag,
     payload: update.payload,
     callback: update.callback,
     next: null,
   };
   
   // 优先级不足，将update添加到本次的baseUpdate队列中
   if (newLastBaseUpdate === null) {
      newFirstBaseUpdate = newLastBaseUpdate = clone;
      // newBaseState 更新为前一个 update 任务的结果，下一轮
      // 持有新优先级的渲染过程处理更新队列时，将会以它为基础进行计算。
      newBaseState = newState;
   } else {
     // 如果baseUpdate队列中已经有了update，那么将当前的update
     // 追加到队列尾部
     newLastBaseUpdate = newLastBaseUpdate.next = clone;
   }
   /* *
    * newLanes会在最后被赋值到workInProgress.lanes上，而它又最终
    * 会被收集到root.pendingLanes。
    *  再次更新时会从root上的pendingLanes中找出渲染优先级（renderLanes），
    * renderLanes含有本次跳过的优先级，再次进入processUpdateQueue时，
    * update的优先级符合要求，被更新掉，低优先级任务因此被重做
    * */
    newLanes = mergeLanes(newLanes, updateLane);
 } else {
 if (newLastBaseUpdate !== null) {
   // 进到这个判断说明现在处理的这个update在优先级不足的update之后，
   // 原因有二：
   // 第一，优先级足够；
   // 第二，newLastBaseUpdate不为null说明已经有优先级不足的update了
   // 然后将这个高优先级放入本次的baseUpdate，实现之前提到的从updateQueue中
   // 截取低优先级update到最后一个update
   const clone: Update<State> = {
      eventTime: updateEventTime,
      lane: NoLane,
       suspenseConfig: update.suspenseConfig,
       tag: update.tag,
       payload: update.payload,
       callback: update.callback,
       next: null,
 };
 newLastBaseUpdate = newLastBaseUpdate.next = clone;
 }
 markRenderEventTimeAndConfig(updateEventTime, update.suspenseConfig);
 
 // 处理更新，计算出新结果
 newState = getStateFromUpdate( workInProgress, queue, update, newState, props, instance, );
 const callback = update.callback;
 
 // 这里的callback是setState的第二个参数，属于副作用，
 // 会被放入queue的副作用队列里
 if (callback !== null) {
   workInProgress.effectTag |= Callback;
   const effects = queue.effects;
   if (effects === null) {
       queue.effects = [update];
   } else {
      effects.push(update);
   }
 }
 } // 移动指针实现遍历
 update = update.next;
 
 if (update === null) {
 // 已有的队列处理完了，检查一下有没有新进来的，有的话
 // 接在已有队列后边继续处理
 pendingQueue = queue.shared.pending;
 if (pendingQueue === null) {
   // 如果没有等待处理的update，那么跳出循环
   break;
 } else {
   // 如果此时又有了新的update进来，那么将它接入到之前合并好的队列中
   const lastPendingUpdate = pendingQueue;
   const firstPendingUpdate = ((lastPendingUpdate.next: any): Update<State>);
   lastPendingUpdate.next = null;
   update = firstPendingUpdate;
   queue.lastBaseUpdate = lastPendingUpdate;
   queue.shared.pending = null;
   }
}
} while (true);
 // 如果没有低优先级的更新，那么新的newBaseState就被赋值为
 // 刚刚计算出来的state
 if (newLastBaseUpdate === null) {
  newBaseState = newState;
 }
 // 完成阶段------------------------------------
 queue.baseState = ((newBaseState: any): State);
 queue.firstBaseUpdate = newFirstBaseUpdate;
 queue.lastBaseUpdate = newLastBaseUpdate; markSkippedUpdateLanes(newLanes);
 workInProgress.lanes = newLanes; workInProgress.memoizedState = newState;
 }
}
```



### <u>Hooks</u>

在 React 中，`Component` 之于 `UI`，好比原子之于世间万物。原子的类型与属性决定了事物的外观与表现，同样，`Component` 的属性和类型决定了 `UI` 的外观与表现。

`Hooks` 如同围绕着原子运行的电子，影响着 `Component` 的特性。

#### 数据结构

```typescript
export type Hook = {
  memoizedState: any,
  baseState: any,
  baseQueue: Update<any, any> | null,
  queue: UpdateQueue<any, any> | null,
  next: Hook | null,
};
```

不同类型`hook`的`memoizedState`保存不同类型数据，具体如下：

- `useState`：对于`const [state, updateState] = useState(initialState)`，`memoizedState`保存`state`的值
- `useReducer`：对于`const [state, dispatch] = useReducer(reducer, {});`，`memoizedState`保存`state`的值
- `useEffect`：`memoizedState`保存包含`useEffect回调函数`、`依赖项`等的链表数据结构`effect`。`effect`链表同时会保存在`fiber.updateQueue`中
- `useRef`：对于`useRef(1)`，`memoizedState`保存`{current: 1}`
- `useMemo`：对于`useMemo(callback, [depA])`，`memoizedState`保存`[callback(), depA]`
- `useCallback`：对于`useCallback(callback, [depA])`，`memoizedState`保存`[callback, depA]`。与`useMemo`的区别是，`useCallback`保存的是`callback`函数本身，而`useMemo`保存的是`callback`函数的执行结果

有些`hook`是没有`memoizedState`的，比如：

- `useContext`

#### 与Fiber的联系

类似`Fiber节点`组成`Fiber树`，`FunctionComponent Fiber节点`上的多个`Hook`会组成链表并被包含在`fiber.memoizedState`中。

`Fiber节点`最多同时存在两个`memoizedState`：

- `current fiber`保存的`memoizedState`即`current memoizedState`
- `workInProgress fiber`保存的`memoizedState`即`workInProgress memoizedState`

在`commit阶段`完成页面渲染后，`workInProgress Fiber树`变为`current Fiber树`，`workInProgress Fiber树`内`Fiber节点`的`memoizedState`就变成`current memoizedState`。

注意：

`hook`与`FunctionComponent fiber`都存在`memoizedState`属性。

- `fiber.memoizedState`：`FunctionComponent`对应`fiber`保存的`Hooks`链表。
- `hook.memoizedState`：`Hooks`链表中保存的单一`hook`对应的数据。



#### 工作流程

##### useState与useReducer





### Concurrent Mode

> Concurrent 模式是一组 React 的新功能，可帮助应用保持响应，并根据用户的设备性能和网速进行适当的调整，实现`多优先级`的`异步可中断`更新。

React 为了实现 Concurrent Mode，做了以下几部分的工作：

+ 底层架构 —— Fiber 架构

  > Fiber 架构的意义在于，它将单个`Fiber节点`作为`工作单元`，使以节点为粒度的“异步可中断的更新”成为可能。

+ 架构的驱动力 —— Scheduler

  > Scheduler 的功能是根据宿主环境性能，为每个`工作单元`（组件）分配一个`可运行时间`，实现“异步可中断的更新”。

+ 架构的运行策略 —— lane 模型

  > Fiber 架构配合 Scheduler 可以控制`更新`在`Fiber`架构中运行/中断/继续运行（异步可中断更新）。但要实现`多优先级`的异步可中断更新，还需要一个模型用于确定更新的优先级，并控制不同优先级的更新之间的关系和行为。



#### <u>Fiber 架构</u>

##### 产生背景

在 `React15` 及以前，`Reconciler` 采用递归的方式创建虚拟DOM，递归过程是不能中断的。如果组件树的层级很深，递归会占用线程很多时间，造成卡顿。

为了解决这个问题，`React16` 将**递归的无法中断的更新**重构为**异步的可中断更新(由Scheduler控制)**，由于曾经用于递归的**虚拟DOM**数据结构已经无法满足需要。于是，全新的`Fiber(React16虚拟DOM)`架构应运而生。

##### 实现原理

###### Fiber的含义

`Fiber`包含三层含义：

1. 作为架构来说，之前`React15`的`Reconciler`采用递归的方式执行，数据保存在递归调用栈中，所以被称为`stack Reconciler`。`React16`的`Reconciler`基于`Fiber节点`实现，被称为`Fiber Reconciler`。
2. 作为静态的数据结构来说，每个`Fiber节点`对应一个`React element`，保存了该组件的类型（函数组件/类组件/原生组件...）、对应的DOM节点等信息。
3. 作为动态的工作单元来说，每个`Fiber节点`保存了本次更新中该组件改变的状态、要执行的工作（需要被删除/被插入页面中/被更新...）。

###### Fiber的结构

```javascript
function FiberNode(
  tag: WorkTag,
  pendingProps: mixed,
  key: null | string,
  mode: TypeOfMode,
) {
  // 作为静态数据结构的属性
  this.tag = tag; // Fiber对应组件的类型 Function/Class/Host...
  this.key = key; // key属性
  this.elementType = null; // 大部分情况同type，某些情况不同，比如FunctionComponent使用React.memo包裹
  this.type = null; // 对于 FunctionComponent，指函数本身，对于ClassComponent，指class，对于HostComponent，指DOM节点tagName
  this.stateNode = null; // 实例对象，比如 class 组件 new 完后就挂载在这个属性上面，如果是RootFiber，那么它上面挂的是 FiberRootNode，如果是原生节点就是 dom 对象

  // 用于连接其他Fiber节点形成Fiber树
  this.return = null; // 指向父级Fiber节点
  this.child = null; // 指向子Fiber节点
  this.sibling = null; // 指向右边第一个兄弟Fiber节点
  this.index = 0;

  this.ref = null;

  // 作为动态的工作单元的属性
  this.pendingProps = pendingProps;
  this.memoizedProps = null;
  this.updateQueue = null;
  this.memoizedState = null;
  this.dependencies = null;

  this.mode = mode;
  
  // 保存本次更新会造成的DOM操作
  this.effectTag = NoEffect;
  this.nextEffect = null;

  this.firstEffect = null;
  this.lastEffect = null;

  // 调度优先级相关
  this.lanes = NoLanes;
  this.childLanes = NoLanes;

  // 指向该fiber在另一次更新时对应的fiber
  this.alternate = null;
}
```

##### 工作原理

> `React`使用“双缓存”来完成`Fiber树`的构建与替换——对应着`DOM树`的创建与更新。

在`React`中最多会同时存在两棵`Fiber树`。当前屏幕上显示内容对应的`Fiber树`称为`current Fiber树`，正在内存中构建的`Fiber树`称为`workInProgress Fiber树`。

`current Fiber树`中的`Fiber节点`被称为`current fiber`，`workInProgress Fiber树`中的`Fiber节点`被称为`workInProgress fiber`，他们通过`alternate`属性连接。

```javascript
currentFiber.alternate === workInProgressFiber;
workInProgressFiber.alternate === currentFiber;
```

`React`应用的根节点通过使`current`指针在不同`Fiber树`的`rootFiber`间切换来完成`current Fiber`树指向的切换。

即当`workInProgress Fiber树`构建完成交给`Renderer`渲染在页面上后，应用根节点的`current`指针指向`workInProgress Fiber树`，此时`workInProgress Fiber树`就变为`current Fiber树`。

每次状态更新都会产生新的`workInProgress Fiber树`，通过`current`与`workInProgress`的替换，完成`DOM`更新。

###### mount时

考虑如下例子：

```js
function App() {
  const [num, add] = useState(0);
  return (
    <p onClick={() => add(num + 1)}>{num}</p>
  )
}

ReactDOM.render(<App/>, document.getElementById('root'));
```

1. 首次执行`ReactDOM.render`会创建`fiberRootNode`（源码中叫`fiberRoot`）和`rootFiber`。其中`fiberRootNode`是整个应用的根节点，`rootFiber`是`<App/>`所在组件树的根节点。

之所以要区分`fiberRootNode`与`rootFiber`，是因为在应用中我们可以多次调用`ReactDOM.render`渲染不同的组件树，他们会拥有不同的`rootFiber`。但是整个应用的根节点只有一个，那就是`fiberRootNode`。

`fiberRootNode`的`current`会指向当前页面上已渲染内容对应`Fiber树`，即`current Fiber树`。

<img src=".\react\rootfiber.png" style="zoom:50%;" />

```js
fiberRootNode.current = rootFiber;
```

由于是首屏渲染，页面中还没有挂载任何`DOM`，所以`fiberRootNode.current`指向的`rootFiber`没有任何`子Fiber节点`（即`current Fiber树`为空）。

1. 接下来进入`render阶段`，根据组件返回的`JSX`在内存中依次创建`Fiber节点`并连接在一起构建`Fiber树`，被称为`workInProgress Fiber树`。（下图中右侧为内存中构建的树，左侧为页面显示的树）

在构建`workInProgress Fiber树`时会尝试复用`current Fiber树`中已有的`Fiber节点`内的属性，在`首屏渲染`时只有`rootFiber`存在对应的`current fiber`（即`rootFiber.alternate`）。

<img src=".\react\workInProgressFiber.png" style="zoom:50%;" />

1. 图中右侧已构建完的`workInProgress Fiber树`在`commit阶段`渲染到页面。

此时`DOM`更新为右侧树对应的样子。`fiberRootNode`的`current`指针指向`workInProgress Fiber树`使其变为`current Fiber树`。

<img src=".\react\wipTreeFinish.png" alt="workInProgressFiberFinish" style="zoom:50%;" />

###### update时

1. 接下来我们点击`p节点`触发状态改变，这会开启一次新的`render阶段`并构建一棵新的`workInProgress Fiber树`。

<img src=".\react\wipTreeUpdate.png" alt="wipTreeUpdate" style="zoom:50%;" />

和`mount`时一样，`workInProgress fiber`的创建可以复用`current Fiber树`对应的节点数据。

> 这个决定是否复用的过程就是`Diff`算法

1. `workInProgress Fiber树`在`render阶段`完成构建后进入`commit阶段`渲染到页面上。渲染完毕后，`workInProgress Fiber树`变为`current Fiber树`。

<img src=".\react\currentTreeUpdate.png" alt="currentTreeUpdate" style="zoom:50%;" />



#### Scheduler

Scheduler 包含两个功能：时间切片和优先级调度。

##### 时间切片

> 时间切片即更新过程碎片化，把一个耗时长的**大**任务**拆分**成很多执行时间短的**小**任务，一个小任务就是一个切片。

浏览器在一个 tick 中可以用于执行 JS 的时机：

```javascript
一个宏任务 -- 微任务队列中的全部微任务 -- requestAnimationFrame -- （浏览器重排/重绘） -- requestIdleCallback
```

`Scheduler `将需要被执行的更新任务注册为一个宏任务。

在`React`的`render`阶段，开启`Concurrent Mode`时，每次遍历前，都会通过`Scheduler`提供的`shouldYield`方法判断是否需要中断遍历，使浏览器有时间渲染：

```js
function workLoopConcurrent() {
  // Perform work until Scheduler asks us to yield
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}
```

是否中断的依据是每个任务的剩余可执行时间是否用完。在 `Scheduler`中，为任务分配的初始剩余时间为 5 ms，在应用运行过程中，会根据 fps 动态调整分配给任务的可执行时间。



##### 优先级调度

`Scheduler` 是独立于 `React` 的包，所以它的`优先级`是独立于 `React `的`优先级`的。

`Scheduler ` 对外暴露了一个方法 `unstable_runWithPriority`。这个方法接受一个`优先级`与一个`回调函数`，在`回调函数`内部调用获取`优先级`的方法都会取得第一个参数对应的`优先级`。

```javascript
function unstable_runWithPriority(priorityLevel, eventHandler) {
  switch (priorityLevel) {
    case ImmediatePriority:
    case UserBlockingPriority:
    case NormalPriority:
    case LowPriority:
    case IdlePriority:
      break;
    default:
      priorityLevel = NormalPriority;
  }

  var previousPriorityLevel = currentPriorityLevel;
  currentPriorityLevel = priorityLevel;

  try {
    return eventHandler();
  } finally {
    currentPriorityLevel = previousPriorityLevel;
  }
}
```



##### 优先级的意义

`Scheduler` 对外暴露最重要的方法便是`unstable_scheduleCallback` 。**该方法用于以某个`优先级`注册一个任务。**

不同的`优先级`意味着不同时长的**任务过期时间**，进而影响任务在任务队列中的先后顺序:

```js
var timeout;
switch (priorityLevel) {
  case ImmediatePriority:
    timeout = IMMEDIATE_PRIORITY_TIMEOUT;
    break;
  case UserBlockingPriority:
    timeout = USER_BLOCKING_PRIORITY_TIMEOUT;
    break;
  case IdlePriority:
    timeout = IDLE_PRIORITY_TIMEOUT;
    break;
  case LowPriority:
    timeout = LOW_PRIORITY_TIMEOUT;
    break;
  case NormalPriority:
  default:
    timeout = NORMAL_PRIORITY_TIMEOUT;
    break;
}

var expirationTime = startTime + timeout;
```

其中：

```js
// Times out immediately
var IMMEDIATE_PRIORITY_TIMEOUT = -1;
// Eventually times out
var USER_BLOCKING_PRIORITY_TIMEOUT = 250;
var NORMAL_PRIORITY_TIMEOUT = 5000;
var LOW_PRIORITY_TIMEOUT = 10000;
// Never times out
var IDLE_PRIORITY_TIMEOUT = maxSigned31BitInt;
```



##### 不同优先级任务的排序

`优先级`意味着任务的**过期时间**，不同`优先级`的任务，对应不同的过期时间。

同时，由因为任务可以被延迟，所以可以将这些任务按是否被延迟分为：

+ 已就绪任务：未被延迟
+ 未就绪任务：被延迟

```js
  if (typeof options === 'object' && options !== null) {
    var delay = options.delay;
    if (typeof delay === 'number' && delay > 0) {
      // 任务被延迟
      startTime = currentTime + delay;
    } else {
      startTime = currentTime;
    }
  } else {
    startTime = currentTime;
  }
```

所以，`Scheduler` 存在两个任务队列：

+ timerQueue：一个以**开始时间**为排序标准的**最小**优先队列，保存未就绪任务。
+ taskQueue：一个以**过期时间**为排序标准的**最小**优先队列，保存就绪任务。

每当有新的**未就绪**的任务被注册，就将其加入 `timerQueue`。

```javascript
if (startTime > currentTime) {
    // This is a delayed task.
    newTask.sortIndex = startTime;
    push(timerQueue, newTask);
} else {
  ...
}
```

`timerQueue` 中最早**开始**的任务位于队列首部，当 `timerQueue` 中有任务就绪，即 `startTime <= currentTime`，就将其取出并加入 `taskQueue` 。

```javascript
function advanceTimers(currentTime) {
  // Check for tasks that are no longer delayed and add them to the queue.
  let timer = peek(timerQueue);
  while (timer !== null) {
    if (timer.callback === null) {
      // Timer was cancelled.
      pop(timerQueue);
    } else if (timer.startTime <= currentTime) {
      // Timer fired. Transfer to the task queue.
      pop(timerQueue);
      timer.sortIndex = timer.expirationTime;
      push(taskQueue, timer);
      if (enableProfiling) {
        markTaskStart(timer, currentTime);
        timer.isQueued = true;
      }
    } else {
      // Remaining timers are pending.
      return;
    }
    timer = peek(timerQueue);
  }
}
```

`taskQueue` 中最早**过期**的任务位于任务队列首部，会被优先取出并执行。



#### 优先级

UI产生交互的根本原因是各种事件，这也就意味着事件与更新有着直接关系。不同事件产生的更新，它们的优先级是有差异的，所以更新优先级的根源在于事件的优先级。一个更新的产生可直接导致React生成一个更新任务，最终这个任务被Scheduler调度。

所以在React中，人为地将事件划分了等级，最终目的是决定调度任务的轻重缓急，因此，React有一套从事件到调度的优先级机制。

- 事件优先级：按照用户事件的交互紧急程度，划分的优先级
- 更新优先级：事件导致React产生的更新对象（update）的优先级（`update.lane`）
- 任务优先级：产生更新对象之后，React去执行一个更新任务，这个任务所持有的优先级
- 调度优先级：Scheduler依据React更新任务生成一个调度任务，这个调度任务所持有的优先级

前三者属于React的优先级机制，第四个属于Scheduler的优先级机制，Scheduler内部有自己的优先级机制，虽然与React有所区别，但等级的划分基本一致。

##### 事件优先级

React按照事件的紧急程度，把它们划分成三个等级：

+ 离散事件（`DiscreteEvent`）：click、`keydown`、`focusin`等，这些事件的触发不是连续的，优先级为0。
+ 用户阻塞事件（`UserBlockongEvent`）：drag、scroll、`mouseover`等，特点是连续触发，阻塞渲染，优先级为1。
+ 连续事件（`ContinuousEvent`）：`canplay`、error、audio标签的`timeupdate`和`canplay`，优先级最高，为2。

###### 派发事件优先级

事件优先级是在**注册阶段**被确定的，在向root上注册事件时，会根据事件的类别，创建不同优先级的事件监听（listener），最终将它绑定到root上去。

`createEventListenerWrapperWithPriority`函数会首先根据**事件的名称**去找对应的**事件优先级**，然后依据优先级返回不同的**事件监听函数**。

```javascript
export function createEventListenerWrapperWithPriority(
  targetContainer: EventTarget,
  domEventName: DOMEventName,
  eventSystemFlags: EventSystemFlags,
  priority?: EventPriority,
): Function {
  const eventPriority =
    priority === undefined
      ? getEventPriorityForPluginSystem(domEventName)
      : priority;
  let listenerWrapper;
  switch (eventPriority) {
    case DiscreteEvent:
      listenerWrapper = dispatchDiscreteEvent;
      break;
    case UserBlockingEvent:
      listenerWrapper = dispatchUserBlockingUpdate;
      break;
    case ContinuousEvent:
    default:
      listenerWrapper = dispatchEvent;
      break;
  }
  return listenerWrapper.bind(
    null,
    domEventName,
    eventSystemFlags,
    targetContainer,
  );
}
```

最终绑定到root上的事件监听函数其实是**`dispatchDiscreteEvent`**、**`dispatchUserBlockingUpdate`**、**`dispatchEvent`**这三个中的一个。它们做的事情都是一样的，以**各自的事件优先级**去**执行真正的事件处理函数**。

以某种优先级去执行事件处理函数其实要借助Scheduler中提供的`runWithPriority`函数来实现：

```javascript
function dispatchUserBlockingUpdate(
  domEventName,
  eventSystemFlags,
  container,
  nativeEvent,
) {

  ...
  
  runWithPriority(
    UserBlockingPriority,
    dispatchEvent.bind(
      null,
      domEventName,
      eventSystemFlags,
      container,
      nativeEvent,
    ),
  );
      
  ...
}
```

这么做可以将事件优先级记录到Scheduler中，相当于告诉Scheduler：你帮我记录一下当前事件派发的优先级，等React那边创建更新对象（即update）计算更新优先级时直接从你这拿就好了。

```javascript
function unstable_runWithPriority(priorityLevel, eventHandler) {
  switch (priorityLevel) {
    case ImmediatePriority:
    case UserBlockingPriority:
    case NormalPriority:
    case LowPriority:
    case IdlePriority:
      break;
    default:
      priorityLevel = NormalPriority;
  }

  var previousPriorityLevel = currentPriorityLevel;
  // 记录优先级到Scheduler内部的变量里
  currentPriorityLevel = priorityLevel;

  try {
    return eventHandler();
  } finally {
    currentPriorityLevel = previousPriorityLevel;
  }
}
```



##### 更新优先级

以`setState`为例，事件处理函数的执行会导致`setState`执行，生成一个update对象，这时候会调用`requestUpdateLane`计算update的优先级，即`update.lane`。它首先找出Scheduler中记录的优先级：`schedulerPriority`，然后计算更新优先级：lane，具体的计算过程在`findUpdateLane`函数中。

```javascript
export function requestUpdateLane(
  fiber: Fiber,
  suspenseConfig: SuspenseConfig | null,
): Lane {

  ...
  // 获取记录下的事件优先级
  const schedulerPriority = getCurrentPriorityLevel();

  let lane;
  if (
    (executionContext & DiscreteEventContext) !== NoContext &&
    schedulerPriority === UserBlockingSchedulerPriority
  ) {
    // 如果事件优先级是用户阻塞级别，则直接用InputDiscreteLanePriority去计算更新优先级
    lane = findUpdateLane(InputDiscreteLanePriority, currentEventWipLanes);
  } else {
    // 依据事件的优先级去计算schedulerLanePriority
    const schedulerLanePriority = schedulerPriorityToLanePriority(
      schedulerPriority,
    );
    ...
    // 根据事件优先级计算得来的schedulerLanePriority，去计算更新优先级
    lane = findUpdateLane(schedulerLanePriority, currentEventWipLanes);
  }
  return lane;
}
```

`getCurrentPriorityLevel`负责读取记录在Scheduler中的优先级：

```javascript
function unstable_getCurrentPriorityLevel() {
  return currentPriorityLevel;
}
```

update对象创建完成后意味着需要对页面进行更新，会调用`scheduleUpdateOnFiber`进入调度，而真正开始调度之前会计算本次产生的更新任务的任务优先级，目的是与已有任务的任务优先级去做比较，便于做出多任务的调度决策。



##### 任务优先级

一个update会被一个React的更新任务执行掉，任务优先级被用来区分多个更新任务的紧急程度，它由更新优先级计算而来。

任务优先级在即将调度的时候去计算，代码在`ensureRootIsScheduled`函数中：

```javascript
function ensureRootIsScheduled(root: FiberRoot, currentTime: number) {

  ...

  // 获取nextLanes，顺便计算任务优先级
  const nextLanes = getNextLanes(
    root,
    root === workInProgressRoot ? workInProgressRootRenderLanes : NoLanes,
  );

  // 获取上面计算得出的任务优先级
  const newCallbackPriority = returnNextLanesPriority();

  ...

}
```

通过调用`getNextLanes`去计算在本次更新中应该处理的这批lanes（`nextLanes`），`getNextLanes`会调用`getHighestPriorityLanes`去计算任务优先级。

任务优先级计算的原理是这样：更新优先级（update的lane），它会被并入`root.pendingLanes`，`root.pendingLanes`经过`getNextLanes`处理后，挑出那些应该处理的lanes，传入`getHighestPriorityLanes`，根据`nextLanes`找出这些lanes的优先级作为任务优先级。

```javascript
function getHighestPriorityLanes(lanes: Lanes | Lane): Lanes {
  ...
  // 都是这种比较赋值的过程，这里只保留两个以做简要说明
  const inputDiscreteLanes = InputDiscreteLanes & lanes;
  if (inputDiscreteLanes !== NoLanes) {
    return_highestLanePriority = InputDiscreteLanePriority;
    return inputDiscreteLanes;
  }
  if ((lanes & InputContinuousHydrationLane) !== NoLanes) {
    return_highestLanePriority = InputContinuousHydrationLanePriority;
    return InputContinuousHydrationLane;
  }
  ...
  return lanes;
}
```

`return_highestLanePriority`就是任务优先级，它有如下这些值，值越大，优先级越高。

```javascript
export const SyncLanePriority: LanePriority = 17;
export const SyncBatchedLanePriority: LanePriority = 16;

const InputDiscreteHydrationLanePriority: LanePriority = 15;
export const InputDiscreteLanePriority: LanePriority = 14;

const InputContinuousHydrationLanePriority: LanePriority = 13;
export const InputContinuousLanePriority: LanePriority = 12;

const DefaultHydrationLanePriority: LanePriority = 11;
export const DefaultLanePriority: LanePriority = 10;

const TransitionShortHydrationLanePriority: LanePriority = 9;
export const TransitionShortLanePriority: LanePriority = 8;

const TransitionLongHydrationLanePriority: LanePriority = 7;
export const TransitionLongLanePriority: LanePriority = 6;

const RetryLanePriority: LanePriority = 5;

const SelectiveHydrationLanePriority: LanePriority = 4;

const IdleHydrationLanePriority: LanePriority = 3;
const IdleLanePriority: LanePriority = 2;

const OffscreenLanePriority: LanePriority = 1;

export const NoLanePriority: LanePriority = 0;
```

如果已经存在一个更新任务，`ensureRootIsScheduled`会在获取到新任务的任务优先级之后，去和旧任务的任务优先级去比较，从而做出是否需要重新发起调度的决定，若需要发起调度，那么会去计算调度优先级。



##### 调度优先级

一旦任务被调度，那么它就会进入Scheduler，在Scheduler中，这个任务会被包装一下，生成一个属于Scheduler自己的task，这个task持有的优先级就是调度优先级。

调度优先级由**任务优先级**计算得出，在`ensureRootIsScheduled`真正让Scheduler发起更新任务调度的时候，会去计算调度优先级。

```javascript
function ensureRootIsScheduled(root: FiberRoot, currentTime: number) {

    ...

    // 根据任务优先级获取Scheduler的调度优先级
    const schedulerPriorityLevel = lanePriorityToSchedulerPriority(
      newCallbackPriority,
    );

    // 计算出调度优先级之后，开始让Scheduler调度React的更新任务
    newCallbackNode = scheduleCallback(
      schedulerPriorityLevel,
      performConcurrentWorkOnRoot.bind(null, root),
    );

    ...
}
```

`lanePriorityToSchedulerPriority`计算调度优先级的过程是根据任务优先级找出对应的调度优先级。

```javascript
export function lanePriorityToSchedulerPriority(
  lanePriority: LanePriority,
): ReactPriorityLevel {
  switch (lanePriority) {
    case SyncLanePriority:
    case SyncBatchedLanePriority:
      return ImmediateSchedulerPriority;
    case InputDiscreteHydrationLanePriority:
    case InputDiscreteLanePriority:
    case InputContinuousHydrationLanePriority:
    case InputContinuousLanePriority:
      return UserBlockingSchedulerPriority;
    case DefaultHydrationLanePriority:
    case DefaultLanePriority:
    case TransitionShortHydrationLanePriority:
    case TransitionShortLanePriority:
    case TransitionLongHydrationLanePriority:
    case TransitionLongLanePriority:
    case SelectiveHydrationLanePriority:
    case RetryLanePriority:
      return NormalSchedulerPriority;
    case IdleHydrationLanePriority:
    case IdleLanePriority:
    case OffscreenLanePriority:
      return IdleSchedulerPriority;
    case NoLanePriority:
      return NoSchedulerPriority;
    default:
      invariant(
        false,
        'Invalid update priority: %s. This is a bug in React.',
        lanePriority,
      );
  }
}
```

**事件优先级、更新优先级、任务优先级、调度优先级**，它们之间是递进的关系。事件优先级由事件本身决定，更新优先级由事件计算得出，然后放到`root.pendingLanes`，任务优先级来自`root.pendingLanes`中最紧急的那些lanes对应的优先级，调度优先级根据任务优先级获取。



#### lane模型





