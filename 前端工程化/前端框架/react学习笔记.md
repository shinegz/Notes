## React 理念

构建**快速响应**的大型 Web 应用程序。

制约快速响应的因素：

+ CPU 瓶颈：大计算量的操作或者设备性能不足使页面掉帧，导致卡顿
+ IO 瓶颈：发送网络请求后，由于需要等待数据返回才能进一步操作导致不能快速响应

应对措施：

+ CPU 瓶颈：控制 JS 脚本在一个帧中的执行时间，即将一个长更新任务拆分到每一帧中，每个帧中执行一小段任务。将**同步的更新变为可中断的异步更新**，避免更新任务阻塞浏览器渲染UI。
+ IO 瓶颈：在等待的数据返回之前，先显示指定的页面，待收到数据后再更新页面。将页面的**同步更新变为可中断的异步更新**。



## 基本概念

### React Components

> 一种机制，允许我们将 UI 拆分为独立可复用的代码片段，并对每个片段进行独立构思。

它接收任意入参 props 作为输入，返回一个用于描述组件显示在屏幕上的内容的 React element。 

React 中组件模型类似于函数：**props** => **element tree**

React 提供了两种定义组件的方式：

+ `function`：无法使用 **state**、**context**、**生命周期**等 React 组件特性。
+ `class`

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

### JSX

> 一种用于描述组件显示内容的标记语言，最终会被编译为生成 React Element 的 React.creaetElement()





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

> 组件的整个生命周期在横向上可分为三个阶段：挂载，更新，卸载。
>
> 每个阶段可被纵向分为“Render”阶段和“Commit”阶段。
>
> 在组件生命周期的特殊时间点上会去调用特定的方法，这些方法被称为“生命周期方法”。

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
// 在effect中返回一个函数是可选的，func2会在组件卸载时执行，相当于componentWillUnmount
```

执行机制：

+ 默认情况下，当组件**每次渲染完成**之后，React 会先执行 func2 对前一个 effect 进行清理，然后再执行 func1 调用新的 effect。
+ 第二个状态数组参数用于告诉 React，只有当这些状态发生改变时才需要执行 effect；传入空数组[]，相当于就告诉 React 你的 effect 不依赖于 props 或 state 中的任何值，所以它永远都不需要重复执行，仅在组件挂载和卸载时执行。

与 Class 对比：

+ 无需将作用于**相同的副作用**的逻辑代码拆分到`componentDidMount` 和 `componentWillUnmount`
+ 无需将不相关的副作用的逻辑代码放到一个生命周期方法中
+ 不同于**生命周期方法**的**同步执行**，使用 `useEffect` 调度的 effect 是**异步执行**的，不会阻塞浏览器更新屏幕

优点：

+ 可以将具有相关逻辑的代码组织在一起
+ 实现关注点分离，将不相关的逻辑分离到不同的 effect 中



##### Context Hook

> 



#### 自定义 Hook



#### Hook 使用规则

Hook 就是 JavaScript 函数，调用它们需要遵循以下两个规则：

+ 只能在**函数最外层**调用 Hook。不要在块作用域中或者子函数中调用。
+ 只能在 **React 的函数组件**中调用 Hook。不能在其他 JavaScript 函数中调用（自定义 Hook 中例外）。



#### Hook 实现原理

https://react.iamkasong.com/hooks/create.html



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



## React 架构

React16 架构可以分为三层：

- Scheduler（调度器）—— 调度任务的优先级，高优任务优先进入**Reconciler**
- Reconciler（协调器）—— 负责找出变化的组件
- Renderer（渲染器）—— 负责将变化的组件渲染到页面上



### 实现原理

组件是如何渲染为 DOM

生命周期方法是如何被调用的，这些生命周期的时间点又是怎么确定的

setState方法的实现原理



### 工作原理

setState方法工作原理