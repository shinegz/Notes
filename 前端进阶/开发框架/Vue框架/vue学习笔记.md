# Vue

## 模板语法

### 插值

### 指令

#### v-bind



#### v-on



#### v-model

#### v-text

#### v-html

#### 条件渲染

##### `v-show`

> 根据表达式的真假值，切换元素的 `display` CSS property，元素始终会被渲染并保留在DOM中。
>
> 当表达式的值为`false`时，元素的`display`值为`none`。
>
> 当条件变化时该指令触发过渡效果。

##### `v-if/v-else/v-else-if`

> `v-if` 指令用于条件性地渲染一块内容。这块内容只会在指令的表达式返回 truthy 值的时候被渲染。
>
> `v-else-if`，充当 `v-if` 的“else-if 块”。
>
> `v-else` 元素必须紧跟在带 `v-if` 或者 `v-else-if` 的元素的后面，否则它将不会被识别。

##### `v-if` vs `v-show`

`v-if` 是“真正”的条件渲染，因为它会确保在切换过程中，条件块内的事件监听器和子组件适当地被销毁和重建。

`v-if` 也是**惰性的**：如果在初始渲染时条件为假，则什么也不做——直到条件第一次变为真时，才会开始渲染条件块。

|        | 特点                                                         | 适用场景           |
| ------ | ------------------------------------------------------------ | ------------------ |
| v-if   | **切换开销高**，需要更改DOM结构；初始渲染时条件为假时不会渲染元素 | 运行时条件很少改变 |
| v-show | 切换开销低，只是更改元素的CSS属性样式；初始化时不管条件真假，都会渲染元素，**初始渲染开销高** | 频繁切换元素的显示 |



#### v-for

#### v-slot

#### v-pre

#### v-cloak

#### v-once



### 特殊指令

#### key

`key` 的特殊 attribute 主要用在 Vue 的虚拟 DOM 算法，在新旧 nodes 对比时辨识 VNodes。

当 Vue 正在更新使用 `v-for` 渲染的元素列表时：

+ 不使用key

  Vue默认使用“就地更新”的策略。如果**数据项的顺序被改变**，Vue 将不会**移动 DOM 元素来匹配数据项的顺序**，而是**就地更新每个元素，并且确保它们在每个索引位置正确渲染**。

+ 使用key

  Vue会基于 key 的变化**重新排列元素顺序**，并且**会移除/销毁 key 不存在的元素**。

#### ref

`ref` 被用来给**元素**或**子组件**注册引用信息。引用信息将会注册在**父组件的 `$refs` 对象**上。如果在普通的 DOM 元素上使用，引用指向的就是 DOM 元素；如果用在子组件上，引用就指向组件实例：

```html
<!-- vm.$refs.p 会是 DOM 节点 -->
<p ref="p">hello</p>

<!-- vm.$refs.child 会是子组件实例 -->
<child-component ref="child"></child-component>

<!-- 当动态绑定时，我们可以将ref定义为回调函数，显式地传递元素或组件实例 -->
<child-component :ref="(el) => child = el"></child-component>
```

#### is



## 组件

### 组件名

在字符串模板或单个文件组件中定义组件时，定义组件名的方式有两种：

#### 使用 kebab-case

```js
app.component('my-component-name', {
  /* ... */
})
```

当使用 kebab-case (短横线分隔命名) 定义一个组件时，你也必须在引用这个自定义元素时使用 kebab-case，例如 `<my-component-name>`。

#### 使用 PascalCase

```js
app.component('MyComponentName', {
  /* ... */
})
```

当使用 PascalCase (首字母大写命名) 定义一个组件时，你在引用这个自定义元素时两种命名法都可以使用。也就是说 `<my-component-name>` 和 `<MyComponentName>` 都是可接受的。注意，尽管如此，直接在 DOM (即非字符串的模板) 中使用时只有 kebab-case 是有效的。



### 选项

> 一个`{}`，对象上的属性和对应的属性值在初始化组件对象时会被用到

#### data

> 用于声明需要被**加入到组件实例的响应式系统的数据**。
>
> Type：Function
>
> 返回组件实例的 data 对象的函数。
>
> 实例创建之后，可以通过 `vm.$data` 访问原始数据对象。组件实例也代理了 data 对象上所有的 property，因此访问 `vm.a` 等价于访问 `vm.$data.a`。



#### props

> 用于接收来自父组件的数据。props会被添加到组件实例上，在模板中可以使用，但在任何时候组件内部都不应该改变属性的值。
>
> Type：Array<string> | Object
>
> props 可以是简单的数组，或者使用对象作为替代，对象允许配置高阶选项，如类型检测、自定义验证和设置默认值。



#### methods

> 用于为组件实例添加方法。在模板中可以使用。
>
> Type：{ [key: string]: Function }



#### computed

> 用于为组件实例添加访问器属性，**访问器属性会被加入到组件实例的响应式系统中，成为响应式 property**。
>
> Type：{ [key: string]: Function | { get: Function, set: Function } }
>
> 对象上的`key`的值：
>
> + 函数：函数将用作实例对象属性`vm.key`的getter函数
> + 对象
>   + 有get属性：属性值用作实例对象属性`vm.key`的getter函数
>   + 有set属性：属性值用作实例对象属性`vm.key`的setter函数

**应用场景**

> 当在**模板渲染**中，**某个值**是**依赖**了**其它的响应式对象**甚至是计算属性**计算而来**

**注意，如果某个依赖 (比如非响应式 property) 在该实例范畴之外，则计算属性是不会被更新的。**

**比较**

+ VS方法

  **计算属性是基于它们的响应式依赖进行缓存的**。只在相关响应式依赖发生改变时它们才会重新求值，这就意味着只要**计算属性的相关响应式依赖没有改变**，多次**访问计算属性**会**立即返回之前的计算结果**，而不必再次执行函数。

  方法在每次重新渲染时都会再次执行函数。

+ VS侦听属性

  侦听属性也是用来响应数据变化的，但与计算属性不同的是，它被设计用来根据响应式数据的变化去执行一段复杂的任务，而计算属性被设计用来根据响应式数据的变化去更新自身的值。



#### watch

> 用于观察和响应 **Vue 实例上的响应式数据**变动。
>
> Type：{ [key: string]: string | Function | Object | Array }

**应用场景**

> 当需要**观测**某个值的**变化**去完成一段**复杂的业务逻辑（如异步或开销较大的操作）**



### 组件实例

#### 实例属性

#### 实例方法



### <u>生命周期</u>

> 每个Vue实例在被创建到被销毁，中间会经历一系列的过程，例如设置数据监听、编译模板、挂载实例到DOM、在数据变化时更新DOM等。**同时在这个过程中也会运行一些叫做生命周期钩子的函数，给予用户机会在一些特定的场景下添加他们自己的代码。**

<img src=".\vue\lifecycle.png" style="zoom: 33%;" />

#### beforeCreate & created



#### beforeMount & mounted

#### beforeUpdate & updated

#### beforeDestroy & destroyed

#### activated & deactivated



### 通信

#### 父子

##### Prop

> 用于接收父组件传递的数据

+ `Prop`类型

  + 字符串数组

    ```js
    props: ['title', 'likes', 'isPublished', 'commentIds', 'author']
    ```

  + 对象（可以为每个`prop`指定值的类型）

+ 传递静态或动态的`Prop`值

  + 传递静态值

    ```html
    <blog-post title="My journey with Vue"></blog-post>
    ```

  + 传递动态值

    ```html
    <!-- 动态赋予一个变量的值 -->
    <blog-post :title="post.title"></blog-post>
    
    <!-- 动态赋予一个复杂表达式的值 -->
    <blog-post :title="post.title + ' by ' + post.author.name"></blog-post>
    ```

+ 单向数据流

  > 所有的 prop 都使得其父子 prop 之间形成了一个**单向下行绑定**：父级 prop 的更新会向下流动到子组件中，但是反过来则不行。这样会防止从子组件意外变更父级组件的状态，从而导致你的应用的数据流向难以理解。

  **单向数据流的必要性**：

  + 每次父级组件发生变更时，子组件中所有的 prop 都将会刷新为最新的值

    子组件内部对prop的改动会因为父级组件的变更而被覆盖掉

  + 对于一个值为引用类型的prop，因为父组件传递的是值的引用，所以在子组件内部改变该prop的值将影响到父组件的状态

+ `Prop`验证

##### <u>自定义事件</u>

> 用于向父组件传递信息

+ 事件名

  与组件和 prop 一样，事件名提供了自动的大小写转换。如果用驼峰命名的子组件中触发一个事件，你将可以在父组件中添加一个 kebab-case (短横线分隔命名) 的监听器。

  ```js
  this.$emit('myEvent')
  ```

  ```html
  <my-component @my-event="doSomething"></my-component>
  ```



#### 跨层级

##### 使用场景

有一些深度嵌套的组件，而深层的子组件只需要父组件的部分内容。在这种情况下，如果仍然将 prop 沿着组件链逐级传递下去，可能会很麻烦。

##### Provide / Inject

对于这种情况，我们可以使用一对 `provide` 和 `inject`。无论组件层次结构有多深，父组件都可以作为其所有子组件的依赖提供者。

父组件有一个 `provide` 选项来提供数据，子组件有一个 `inject` 选项来开始使用这些数据。

<img src=".\vue\provide_inject.png" style="zoom:50%;" />

语法：

- **provide：**`Object | () => Object`
- **inject：**`Array<string> | { [key: string]: string | Symbol | Object }`

`provide` 选项应该是一个对象或返回一个对象的函数。该对象包含可注入其子孙的 property。在该对象中你可以使用 ES2015 Symbols 作为 key，但是只在原生支持 `Symbol` 和 `Reflect.ownKeys` 的环境下可工作。

`inject` 选项应该是：

- 一个字符串数组，或
- 一个对象，对象的 key 是本地的绑定名，value 是：
  - 在可用注入内容中搜索用的 key (字符串或 Symbol)，或
  - 一个对象，该对象的：
    - `from` property 是在可用的注入内容中搜索用的 key (字符串或 Symbol)
    - `default` property 是降级情况下使用的 value



### 插槽

> 用于分发传递给组件的内容。
>
> 这些内容可以是简单的字符串，或者是任何模板代码，也可以是其他组件。

+ 插槽

  `<slot>` 元素作为承载分发内容的出口，当组件渲染的时候，`<slot></slot>` 将会被替换为传递给组件的内容。

  如果组件的模板中没有`<slot>` 元素，则该组件起始标签和结束标签之间的任何内容都会被抛弃。

  ```html
  <!-- todo-button 组件模板 -->
  <button class="btn-primary">
    Create a new item
  </button>
  ```

  ```html
  <todo-button>
    <!-- 以下文本不会渲染 -->
    Add todo
  </todo-button>
  ```

+ 渲染作用域

  > 父级模板里的所有内容都是在父级作用域中编译的；子模板里的所有内容都是在子作用域中编译的。

  当你想在一个插槽中使用数据时，例如：

  ```html
  <todo-button>
    Delete a {{ item.name }}
  </todo-button>
  ```

  该插槽可以访问与模板其余部分相同的实例 property (即相同的“作用域”)。插槽**不能**访问 `<todo-button>` 的作用域。例如，尝试访问 `action` 将不起作用：

  ```html
  <todo-button action="delete">
    Clicking here will {{ action }} an item
    <!-- `action` 未被定义，因为它的内容是传递*到* <todo-button>，而不是*在* <todo-button>里定义的。  -->
  </todo-button>
  ```

+ 具名插槽

  带有“名字”的插槽。即指定了`name`attribute的`<slot>`，用于承载指定的分发内容的出口，一个不带 `name` 的 `<slot>` 出口会带有隐含的名字“default”。

  在向具名插槽提供内容的时候，在 `<template>` 元素上使用 `v-slot` 指令，并以 `v-slot` 的参数的形式提供其名称：

  ```html
  <base-layout>
    <template v-slot:header>
      <h1>Here might be a page title</h1>
    </template>
  
    <template v-slot:default>
      <p>A paragraph for the main content.</p>
      <p>And another one.</p>
    </template>
  
    <template v-slot:footer>
      <p>Here's some contact info</p>
    </template>
  </base-layout>
  ```

   `<template>` 元素中的所有内容都将会被传入相应的插槽。

+ 作用域插槽

  > 用于向父级作用域传递数据的插槽。

  作用域插槽可以使得**插槽内容**能够**访问**到**子组件内部作用域**的**数据**

  语法：

  绑定在 `<slot` > 元素上的 attribute 被称为**插槽 prop**	

  ```html
  <ul>
    <li v-for="( item, index ) in items">
      <slot :item="item" :index="index" :another-attribute="anotherAttribute"></slot>
    </li>
  </ul>
  ```

  现在在父级作用域中，我们可以使用带值的 `v-slot` 来定义包含所有插槽 prop 的对象名：

  ```html
  <todo-list>
    <template v-slot:default="slotProps">
      <i class="fas fa-check"></i>
      <span class="green">{{ slotProps.item }}</span>
    </template>
  </todo-list>
  ```

  在这个例子中，将包含所有插槽 prop 的对象命名为 `slotProps`，也可以是其他任何名字。



## 原理

### 数据驱动

#### 虚拟DOM

> Virtual DOM 就是用一个原生的 JS 对象去描述一个 DOM 节点。

##### 产生背景

它产生的前提是浏览器中的 DOM 是很“昂贵"的，因为 DOM 标准设计的非常复杂，真正的 DOM 元素是非常庞大的。当我们频繁的去做 DOM 更新，会产生一定的性能问题。而 Virtual DOM 就是用一个原生的 JS 对象去描述一个 DOM 节点，所以它比创建一个 DOM 的代价要小很多。



### 组件化

### 响应式原理

### 编译

#### 指令的本质

### 