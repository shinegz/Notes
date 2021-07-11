## 基本概念

### React Component

> 组件模型：
>
> props => element tree

component 类型：

+ `function`
+ `class`

### React Element

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