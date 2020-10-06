# Vue
> 一个前端框架，根据其使用规范，可以极大地简化前端编程和代码量。

### vue的响应式设计

如何理解响应式

1、HTML5中的响应式（屏幕尺寸的变化导致样式的变化）
2、数据的响应式（数据的变化导致页面内容的变化）

+ 什么是数据绑定

数据绑定：将数据填充到标签中

+ Vue数据双向绑定理解

Vue实例化后,将数据对象data中的属性给添加到Vue实例对象上（两者的属性对象指向同一个内存单元）,
也就是添加到了Vue的响应式系统中了,所以改变data的属性也就改变了Vue实例对象的属性了,相应地,Vue的响应式系统便会响应变化

+ Vue实现数据绑定的形式

采用**Mustache**（{{}}）语法实现对标签内容的填充；
采用Vue指令实现HTML标签特性与数据的绑定

+ **计算属性**

计算属性是基于它们的**响应式依赖**进行缓存的

+ **计算属性与方法的区别**

1、计算属性是基于它们的依赖进行缓存的（如果依赖不变，缓存就不会更新；只有当依赖变化时，才会重新计算，否则将会一直使用缓存值）
2、方法不存在缓存

+ **侦听器**

数据一旦发生变化就执行侦听器所绑定的方法

**侦听器的应用场景**

数据变化时执行异步或开销较大的操作（所谓开销较大即比较耗时）



# Vue组件机制

一个 Vue 应用由一个通过 `new Vue` 创建的**根 Vue 实例**，以及可选的嵌套的、可复用的组件树组成。所有的Vue组件都是Vue实例。

所谓组件，好比一个定制的伪HTML标签，其显示效果由实例化时传入的参数对象的template属性值决定，该值是一个符合HTML语法的字符串。之所以说它是伪HTML标签，是因为它最终还是被编译为对应的真正的HTML标签。
其思想是将一些HTML标签封装成块，以便复用，使前端开发组件化。
对于这个标签，可以通过为属性设置属性值向组件中的模板传递值，以此改变显示效果，不过属性必须是组件初始化时通过 props 声明了的（一般都会在模板中用到），没注册过的即使不会报错，但也是没有任何作用的（这个是和HTML标签相一致的，只有它自身定义过的属性才会影响它的显示效果）

**组件注册**

+ 全局注册

 `Vue.component` 来创建组件：

```
Vue.component('my-component-name', {
  // ... 选项 ...
})
```

这些组件是**全局注册的**。也就是说，这些组件在根组件及各子组件中都可以使用。

+ 局部注册

通过一个普通的 JavaScript 对象来定义组件：

```javascript
var ComponentA = { /* ... */ }
var ComponentB = { /* ... */ }
var ComponentC = { /* ... */ }
```

然后在 `components` 选项中定义你想要使用的组件：

```javascript
new Vue({
  el: '#app',
  components: {
    'component-a': ComponentA,
    'component-b': ComponentB
  }
})
```

注意，局部注册的组件只能在注册过该组件的组件中使用。



**组件注册注意事项**

定义组件名的方式有两种：

+ 使用 kebab-case

```javascript
Vue.component('my-component-name', { /* ... */ })
```

当使用 kebab-case (短横线分隔命名) 定义一个组件时，你也必须在引用这个自定义元素时使用 kebab-case，例如 ``。

+ 使用 PascalCase

```javascript
Vue.component('MyComponentName', { /* ... */ })
```

当使用 PascalCase (首字母大写命名) 定义一个组件时，你在引用这个自定义元素时两种命名法都可以使用。也就是说 `` 和 `` 都是可接受的。注意，尽管如此，直接在 DOM (即非字符串的模板) 中使用时只有 kebab-case 是有效的。



**组件间信息传递**

* 父组件向子组件传值

  1.组件内部通过props接收传递过来的值。（设置可以接收值的属性）
  2.父组件通过属性将值传递给子组件。

  props属性名的命名规则：

​              1.在props中使用驼峰形式，模板中需要使用短横线的形式
​              2.字符串形式的模板中没有这个限制

（在JavaScript中是驼峰的，在HTML中的是短横线方式的）

​		每个prop都可以指定其值类型

​		prop既可以接受静态值，也可以通过`v-bind`动态赋值

​		当我们传入字面量值对prop进行静态赋值时，仍然需要用`v-bind`动态赋值，声明这是JavaScript表达式，否则Vue会将其当做字符串来处理。

​		每当父组件发生更新时，子组件中prop都会随之自动更新

**此外** 当一个非 prop 的 attribute 是指传向一个组件，但是该组件并没有相应 prop 定义的 attribute时。这些 attribute 会被添加到这个组件的根元素上。对于绝大多数 attribute 来说，从外部提供给组件的值会替换掉组件内部设置好的值。`class` 和 `style` attribute 会稍微智能一些，即两边的值会被合并起来。

​		如果你**不**希望组件的根元素继承 attribute，你可以在组件的选项中设置`inheritAttrs: false`。

`$attrs`决定这些 attribute 会被赋予哪个元素。在撰写基础组件的时候是常会用到的：（设置赋予给input元素）

```javascript
Vue.component('base-input', {
  inheritAttrs: false,
  props: ['label', 'value'],
  template: `
    <label>
      {{ label }}
      <input
        v-bind="$attrs"  
        v-bind:value="value"
        v-on:input="$emit('input', $event.target.value)"
      >
    </label>
  `
})
```

* 子组件向父组件传值

  1.子组件通过自定义事件向父组件传递消息   v-on:html事件名='$emit("自定义事件名")'
  2.父组件监听子组件的事件    v-on：自定义事件名='父组件方法'
  3.子组件通过自定义事件向父组件中传递信息  v-on:html事件名='$emit("自定义事件名"，"数据")'
  4.父组件监听子组件的事件   v-on：自定义事件名='父组件方法（$event）'

  Vue实例的$on方法用于自定义事件，$emit方法用于触发自定义事件，通过 v-on 指令可以监听子组件触发的自定义事件。

* 父子组件之间传值的原则

   对于父组件传递传递给子组件的值（即通过props接受的值）原则上不允许子组件控制其变动，而是通过自定义事件的方式向父组件传递消息，由父组件根据消息对数据进行改动。

   这里有两种常见的试图改变一个 prop 的情形：

   1. **这个 prop 用来传递一个初始值；这个子组件接下来希望将其作为一个本地的 prop 数据来使用。**在这种情况下，最好定义一个本地的 data 属性并将这个 prop 用作其初始值：

      ```javascript
      props: ['initialCounter'],
      data: function () {
        return {
          counter: this.initialCounter
        }
      }
      ```

   2. **这个 prop 以一种原始的值传入且需要进行转换。**在这种情况下，最好使用这个 prop 的值来定义一个计算属性：

      ```javascript
      props: ['size'],
      computed: {
        normalizedSize: function () {
          return this.size.trim().toLowerCase()
        }
      }
      ```

   **注意**在 JavaScript 中对象和数组是通过引用传入的，所以对于一个数组或对象类型的 prop 来说，在子组件中改变这个对象或数组本身**将会**影响到父组件的状态。

* 非父子组件间传值

     1. 单独的事件中心管理组件简单通信  var eventHub = new Vue（）
     2. 监听事件与销毁事件  eventHub.$on('add-todo',addTodo(val))
                                               eventHub.$off('add-todo')
     3. 触发事件  event.$emit('add-todo',val)

* 组件插槽基本用法

  1.插槽位置  在子组件模板中使用内置组件<slot></slot>
  2.插槽内容  在使用子组件时，往组件标签中插入内容，插入内容将传递到该组件模板中的<slot>位置
  3.具名插槽用法  <slot name=''></slot>
  4.作用域插槽  
  应用场景：父组件对子组件的内容进行加工处理



## Vue-router

路由（本质：对应关系）

* 后端路由
  概念：根据不同的用户URL请求，返回不同的内容
  本质：URL请求地址与服务器之间的对应关系

* 前端路由
  概念：根据不同的用户事件，显示不同的页面内容
  本质：用户事件与事件处理函数之间的对应关系
  前端路由主要做的事情就是监听事件并分发执行事件处理函数

**路由组件传参**

* 直接在路由组件模板中使用$route.params.

​      通过这种方式引用路由参数，使组件与路由高度耦合

* 通过props形式

​       1.布尔模式

​           在设计路由规则时，将路由的props设置为true，此时组件可以通过props接受路由参 数     

​       2.对象模式

​          路由的props属性值为一个对象，通过设置对象的属性值向对应组件传递值，组件依然是通过props接收，不过对象的属性值必须为静态值，即不能为变量。

​       3.函数模式

​          路由的props为一个函数，函数返回一个对象，这个对象的属性值可以是静态值、路由参数或者变量。



### 前后端交互

接口调用- fetch用法（相比于Ajax，其内置了promise）

````javascript
      fetch('url',{

      }).then(data => {
          return data.text()；//将数据处理成字符串
          return data.json(); //将json格式的数据处理为javascript对象
      }).then(ret => {
          //注意这里得到的才是最终的数据
      })
````



## Vue前端工程化

>  模块化规范
>
> 在ES6模块化规范诞生之前，JavaScript社区已经尝试提出了AMD、CMD、commonJS等模块化规范。
> 这些社区提出的模块化标准，存在一定的差异性与局限性，并不是浏览器与服务器通用的模块化标准。例如：

+ AMD和CMD适用于浏览器端的JavaScript模块化

+ commonJS适用于服务器端的JavaScript模块化

  因此，ES6语法规范中，在语义层面上定义了ES6模块化规范，是浏览器端和服务器端通用的模块化开发规范。                                                                                                                                                                                                 
  
  

## 疑问及解答

+ Vue实例化时，传入的对象中的参数`el`’的作用？
  `el`只在`new`创建实例时生效，用于选择一个页面上已存在的DOM元素作为Vue根组件的挂载目标， 如果 `render` 函数和 `template` 属性都不存在，挂载 DOM 元素的 HTML 会被提取出来用作模板 ，倘若`render`函数或`template`属性存在，则挂载元素将被Vue根据`render`和`template`生成的DOM所替换。

+ 库和框架的区别？

库以提供API为主；框架以提供功能性的服务为主，是一套完整的解决方案



### vue项目开发笔记

vscode语法查验规则在 **.prettierrc ** 文件中声明

eslint语法查验规则在 **.eslintrc.js ** 文件中的 rule 属性中声明