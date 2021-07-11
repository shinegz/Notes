## 基本概念

### React Components

> 组件允许我们将 UI 拆分为独立可复用的代码片段

接收任意入参 props 作为输入，返回一个用于描述组件显示在屏幕上的内容的 React element。 

组件模型类似于函数：**props** => **element tree**

按照实现组件的方式，可将 component 分为两种类型：

+ `function`：无法使用 state、context、生命周期等 React 特性。
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

+ DOM：`type`属性值为一个`DOM tag`字符串，如‘div’、‘span’。
+ Component：`type`属性值为一个关联`function`或者`class`对象的变量。

生成 element 的方式：

+ `React.creatElement()`：返回一个element对象
+ `JSX`（最终也会被编译为`React.creatElement()`）
+ `React.createFactory()`：返回一个生成给定类型element的function



## Class



## Hook

> 允许我们在非 class 组件的情况下，可以使用 state 以及其他的 React 特性。

### 背景

在 Hook 出现前，如果我们想要使用诸如 state、context、生命周期等 React 特性时，只能在 class 组件中使用它们。但**使用 class 组件开发**，会带来**一些问题**：

+ 组件之间很难复用状态逻辑

  > 常用的状态逻辑复用方案过于复杂，React 没有为共享状态逻辑提供更好的原生途径。

+ 复杂组件变得难以理解

  > 复杂组件中状态逻辑和副作用众多，它们被包含在`componentDidMount` 和 `componentDidUpdate`等生命周期方法中，往往出现完全不相关的代码被放在同一个方法中，而相关联的代码被拆分到不同的方法中，导致逻辑不一致。

+ 难以理解的 class

  > class 的语法比较难理解，学习 class 语法的成本比较高

鉴于以上几个方面的问题，Hook 诞生了，它使得我们在非 class 组件中也能使用更多的 React 特性，拥抱 function 组件的开发方式。