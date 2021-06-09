# JavaScript

> Javascript是一门单线程语言，所谓单线程，是指在JS引擎中负责解释和执行JavaScript代码的线程只有一个。
> Event Loop是Javascript的执行机制。

## JavaScript的定义

+ node中的JavaScript

EcmaScript、核心模块（http、fs等）、第三方模块、用户自定义模块

+ 浏览器中的JavaScript

EcmaScript、DOM、BOM、第三方库、用户自定义对象

## 数据类型

> 在JavaScript中，用户无法自定义数据类型。
>
> 数据类型指的是一组值和一组对这些值的操作的集合。

数据类型实际指的就是值（字面量）的类型，在JavaScript中，有8种数据类型，分别是

7种基本类型：

String、Number、Boolean、Undefined、Null、BigInt、Symbol（用于创建独一无二的属性）

和引用类型Object

其中Object包括简单对象{}、function (){}、[]、/^$/等不同类型的对象。

基本类型的值存储在栈内存中（**其关联的变量所指向的栈内存中存储的是该值本身**），引用类型的值存储在堆内存中（**其关联的变量所指向的栈内存中存储的是其在堆内存中的地址**）。

<img src=".\TS\值在内存中的存储形式.png" style="zoom:50%;" />

+ 基本类型的值

  除 Object 以外的所有类型都是不可变的（值本身无法被改变）。例如，与 C 语言不同，JavaScript 中字符串是不可变的（译注：如，JavaScript 中对字符串的操作一定返回了一个新字符串，原始字符串并没有被改变）。我们称这些类型的值为“原始值”。

### JS中的数据类型检测

- **typeof** [val]: 用于检测数据类型的运算符

  | 类型                                                         | 结果                                                         |
  | :----------------------------------------------------------- | :----------------------------------------------------------- |
  | [Undefined](https://developer.mozilla.org/zh-CN/docs/Glossary/undefined) | `"undefined"`                                                |
  | [Null](https://developer.mozilla.org/zh-CN/docs/Glossary/Null) | `"object"` (见[下文](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/typeof#null)) |
  | [Boolean](https://developer.mozilla.org/zh-CN/docs/Glossary/Boolean) | `"boolean"`                                                  |
  | [Number](https://developer.mozilla.org/zh-CN/docs/Glossary/Number) | `"number"`                                                   |
  | [BigInt](https://developer.mozilla.org/zh-CN/docs/Glossary/BigInt)(ECMAScript 2020 新增) | `"bigint"`                                                   |
  | [String](https://developer.mozilla.org/zh-CN/docs/Glossary/字符串) | `"string"`                                                   |
  | [Symbol](https://developer.mozilla.org/zh-CN/docs/Glossary/Symbol) (ECMAScript 2015 新增) | `"symbol"`                                                   |
  | 宿主对象（由 JS 环境提供）                                   | *取决于具体实现*                                             |
  | [Function](https://developer.mozilla.org/zh-CN/docs/Glossary/Function) 对象 (按照 ECMA-262 规范实现 [[Call]]) | `"function"`                                                 |
  | 其他任何对象                                                 | `"object"`                                                   |

  **缺陷：无法区分对象类型的数据**

- object **instanceof** constructor ： 用来检测constructor.prototype是否存在于object的**原型链**上

  该方法只能用来判断对象类型的数据，对应**原始类型的值无法判断**，且无法检测出`iframes`，并且所有的对象类型instanceof Object都为true。

- constructor ： 基于构造函数检测数据类型

- Object.prototype.toString.call() : 检测数据类型最好的方法**（适用于检测基本数据类型和内置构造函数的实例类型，对于自定义构造函数的实例都为[object Object]）**

  > JavaScript中内置构造函数生成的对象都有私有的[[class]]属性，该属性可以用Object.prototype.toString获取，在JavaScript中，没有任何方法可以更改私有的Class属性

```javascript
let getType = (value) => {
    // 值为null的情况
    if (value === null) return 'Null';
    // 值为引用类型的情况
    if (typeof value === 'object')  return value.constructor.name; // 弊端是value.constructor.name可配置
    // 值为基本类型和函数时
    return (typeof value).slice(0, 1).toUpperCase() + (typeof value).slice(1);
}
```

### JS中的各类型值运算时的默认转换规则

JS中做`+`运算时，若运算值有string类型值时，则运算值默认转换为字符串并进行拼接，其中简单对象转换为[object Object]，其他类型的值转换的字符串引号内为其字面量

true做数学运算时，自动转换为1；false在做数学运算时，自动转换为0

null在做数学运算时，自动转换为0

undefined在做数学运算时，自动转换为NaN，任何数学运算中出现了NaN，运算结果为NaN

数字字符串在数学运算时，自动转换为对应number类型的值；其他字符串在做数学运算时，表达式的运算结果都为NaN

'1'*'2'  //2

’5‘-1  //4

'a'-5  // NaN

true + 1 + typeof undefined  // '2undefined'

[1,3]-5 //NaN
[1,3]+5  //"1,35"

0、NaN、null、undefined、'' 在运用Boolean()转换为Boolean类型的值时是false，其他为true

### 装箱和拆箱

- 装箱转换：把基本类型转换为对应的包装类型
- 拆箱操作：把引用类型转换为基本类型

既然原始类型不能扩展属性和方法，那么我们是如何使用原始类型调用方法的呢？

每当我们操作一个基础类型时，后台就会自动创建一个包装类型的对象，从而让我们能够调用一些方法和属性，例如下面的代码：

```JavaScript
var name = "ConardLi";
var name2 = name.substring(2);
```

实际上发生了以下几个过程：

- 创建一个`String`的包装类型实例
- 在实例上调用`substring`方法
- 销毁实例

也就是说，我们使用基本类型调用方法，就会自动进行装箱和拆箱操作，相同的，我们使用`Number`和`Boolean`类型时，也会发生这个过程。

从引用类型到基本类型的转换，也就是拆箱的过程中，会遵循`ECMAScript规范`规定的`toPrimitive`原则，一般会调用引用类型的`valueOf`和`toString`方法，你也可以直接重写`toPeimitive`方法。一般转换成不同类型的值遵循的原则不同，例如：

- 引用类型转换为`Number`类型，先调用`valueOf`，再调用`toString`
- 引用类型转换为`String`类型，先调用`toString`，再调用`valueOf`

若`valueOf`和`toString`都不存在，或者没有返回基本类型，则抛出`TypeError`异常。


### null与undefined

null与undefined是JavaScript的两个基本数据类型Null、Undefined的值，都表示没有。

null表示变量没有值，不指向任何地方，不与任何值相关联，它的出现是往往是人为设定给某个变量的。

undefined表示变量没有值，表明一个变量应该与某个值相关联，但没有赋值，它的出现往往不是有意为之，是意料之外的。

值 `null` 是一个字面量，不像 `undefined`，它不是全局对象的一个属性。`null` 是表示缺少的标识，指示变量未指向任何对象，而`undefined`表示变量应该有关联的值，但却没有。把 `null` 作为尚未创建的对象，也许更好理解。在 API 中，`null` 常在返回类型应是一个对象，但没有关联的值的地方使用。

```js
// foo 不存在，它从来没有被定义过或者是初始化过：
foo;
"ReferenceError: foo is not defined"

// foo 现在已经是知存在的，但是它没有类型或者是值：
var foo = null; 
foo;
null
```

+ 6种`falsy`值
  + undefined
  + null
  + NaN
  + 0
  + ''(empty string)
  + false
+ `null` 与 `undefined` 的不同点：

当检测 `null` 或 `undefined` 时，注意[相等（==）与全等（===）两个操作符的区别) ，前者会执行类型转换：

```js
typeof null        // "object" (因为一些以前的原因而不是'null')
typeof undefined   // "undefined"
null === undefined // false
null  == undefined // true
null === null // true
null == null // true
!null //true
isNaN(1 + null) // false
isNaN(1 + undefined) // true
```



## 变量

> 用来保存值的标识符。

在JavaScript中，变量是无类型的（untyped），变量可以被赋予任何类型的值，同样一个变量也可以重新赋予不同类型的值。

变量可能包含两种数据类型的值：基本类型的值和引用类型的值。

基本类型的值直接存储在变量所关联的栈内存中（变量本身也存储在栈内存中）；引用类型的值由于保存在堆内存中，所以变量所关联的栈内存中存储的是值在堆内存中的地址。

### 执行上下文（execution context）

>执行上下文：一段JavaScript代码（全局代码或函数）执行时所需的所有信息。

JavaScript中有三种执行上下文：

- 全局执行上下文

  不在任何函数中的js代码执行时所需的所有信息。一个JavaScript程序只能有一个全局执行上下文。

- 函数执行上下文

  函数执行时所需的所有信息。函数每次被调用时，都会创建一个新的函数执行上下文。
  
- eval执行上下文

  eval函数执行时所需的所有信息。

#### 执行上下文的组成

执行上下文在 ES3 中，包含三个部分。

+ scope：作用域，也常常被叫做作用域链。
+ variable object：变量对象，用于存储变量的对象。
+ this value：this 值。

在 ES5 中，改进了命名方式，把执行上下文最初的三个部分改为下面这个样子。

+ lexical environment：词法环境，当获取变量时使用。
+ variable environment：变量环境，当声明变量时使用。
+ this value：this 值。

在 ES2018 中，执行上下文又变成了这个样子，this 值被归入 lexical environment，但是增加了不少内容。

+ lexical environment：词法环境，当获取变量或者 this 值时使用。
+ variable environment：变量环境，当声明变量时使用。
+ code evaluation state：用于恢复代码执行位置。
+ Function：执行的任务是函数时使用，表示正在被执行的函数。
+ ScriptOrModule：执行的任务是脚本或者模块时使用，表示正在被执行的代码。
+ Realm：使用的基础库和内置对象实例。
+ Generator：仅生成器上下文有这个属性，表示当前生成器。

### 作用域

从字面上的意思来看就是起作用的区域；在计算机程序中，变量的作用域是指其**有定义**（可被访问）的区域；作用域的分布结构是从全局作用域向内逐层嵌套。

+ 作用域类型

  + 全局作用域

    任何函数作用域和块级作用域之外的区域，在全局作用域中定义的变量或函数在程序的任何地方都可以被访问。

  + 函数作用域

    函数代码块的区域，函数作用域中定义的变量只在函数内部可访问，对外不可见。

  + 块级作用域

    一个代码块（{}）的区域，由let、const关键字声明的变量具有块级作用域。

+ 静态（词法）作用域和动态作用域

> javascript中的作用域是静态作用域。静态作用域是指在标识符定义的时候，其作用域就已经确定了，即表现为静态的；动态作用域是指当调用标识符时，其作用域才随之确定，即表现为动态的。

+ 作用域链

> JavaScript中每段代码（全局代码或函数）的执行都会有一个执行上下文（提供了代码执行过程中所需的全部信息），每个执行上下文中都有一个作用域链（ES6中称为词法环境），**用于代码执行过程中标识符的解析**（标识符的解析是通过沿着作用域链逐级搜索标识符名称完成的，搜索过程始终从作用域链的最前端开始，然后逐级往后，直到找到标识符。若没有找到便会发生Reference错误）。

**作用域链**本质上是一个**对象列表或者链表**，是**执行上下文的组成部分**，它决定了**执行上下文所关联的代码**对有权访问的所有变量和函数的**访问顺序**。

**作用域链的组成：**

每个执行上下文中都有一个关联的变量对象，在这个**上下文中**（上下文所关联的一段代码中）定义的所有变量和函数都存在于这个对象。作用域链的最前端始终是当前执行上下文所对应的变量对象，下一个变量对象来自包含执行上下文，依次类推直至全局执行上下文。

**函数执行上下文中的作用域链的形成：**

在一个函数被定义的时候，会将它**定义时刻的作用域链**（scope chain）链接到这个函数对象的**[[scope]]**属性。（**函数在执行时所能访问到的外部环境中的变量或函数是在函数定义时就确定的，而不是在执行时确定的**）
在一个函数对象被调用的时候，会创建一个活动对象(activation object)，用来存储它的局部变量，然后将这个活动对象做为此时的作用域链(scope chain)最前端，并将这个函数对象的[[scope]]加入到作用域链（scope chain）中。

（函数在执行函数体中的代码时，存储局部变量的活动对象已经被添加到作用域链中，所以在var声明的变量以及函数声明前，就能够访问这些变量和函数）



## 运算符

+ 相等运算符

  ==：相等（如果左右两边数据值类型不同，默认先转换为相同的类型，然后比较；如果为引用类型的值，则比较是否为同一个对象）

  ===：绝对相等（如果类型不一样，肯定不相等，不会默认转换数据类型；如果类型相同，基本数据类型的如果值是相同的，则相等，引用数据类型的如果引用同一个对象，则相等）

+ 逻辑运算符

  逻辑运算符如下表所示 (其中*expr*可能是任何一种类型, 不一定是布尔值):

  | 运算符              | 语法                 | 说明                                                         |
  | :------------------ | :------------------- | :----------------------------------------------------------- |
  | 逻辑与，AND（`&&`） | *expr1* && *expr2*   | 若 expr**1** 可转换为 `true`，则返回 expr**2**；否则，返回 expr**1**。 |
  | 逻辑或，OR（`||`）  | *expr1* \|\| *expr2* | 若 expr**1** 可转换为 `true`，则返回 expr**1**；否则，返回 expr**2**。 |
  | 逻辑非，NOT（`!`）  | !*expr*              | 若 `expr` 可转换为 `true`，则返回 `false`；否则，返回 `true`。 |

  由于逻辑表达式的运算顺序是从左到右，也可以用以下规则进行"短路"计算：

  - (some falsy expression) && (*expr)* 短路计算的结果为假。
  - (some truthy expression) || *(expr)* 短路计算的结果为真。

  短路意味着上述表达式中的expr部分**不会被执行**，因此expr的任何副作用都不会生效（举个例子，如果expr是一次函数调用，这次调用就不会发生）。造成这种现象的原因是，整个表达式的值在第一个操作数被计算后已经确定了。

+ 算数运算符

  幂运算符返回第一个操作数做底数，第二个操作数做指数的乘方。即，`var1` `var2`，其中 `var1` 和 `var2` 是其两个操作数。幂运算符是右结合的。`a ** b ** c` 等同于 `a ** (b ** c)`。

  注：底数前不能紧跟一元运算符（`+/-/~/!/delete/void/typeof`）

+ 一元运算符

  + void

    **`void` 运算符** 对给定的表达式进行求值，然后返回 undefined。

    注：主要防止一个期望值为undefined的表达式产生副作用。
  
+ 运算符优先级

  下面的表将所有运算符按照优先级的不同从高（21）到低（0）排列。

| 优先级 | 运算类型                    | 关联性        | 运算符           |
| :----- | :-------------------------- | :------------ | :--------------- |
| 21     | `圆括号`                    | n/a（不相关） | `( … )`          |
| 20     | `成员访问`                  | 从左到右      | `… . …`          |
|        | `需计算的成员访问`          | 从左到右      | `… [ … ]`        |
|        | `new` (带参数列表)          | n/a           | `new … ( … )`    |
|        | 函数调用                    | 从左到右      | `… ( … )`        |
|        | 可选链（Optional chaining） | 从左到右      | `?.`             |
| 19     | new (无参数列表)            | 从右到左      | `new …`          |
| 18     | 后置递增(运算符在后)        | n/a           | `… ++`           |
|        | 后置递减(运算符在后)        |               | `… --`           |
| 17     | 逻辑非                      | 从右到左      | `! …`            |
|        | 按位非                      |               | `~ …`            |
|        | 一元加法                    |               | `+ …`            |
|        | 一元减法                    |               | `- …`            |
|        | 前置递增                    |               | `++ …`           |
|        | 前置递减                    |               | `-- …`           |
|        | typeof                      |               | typeof …         |
|        | void                        |               | `void …`         |
|        | delete                      |               | `delete …`       |
|        | await                       |               | `await …`        |
| 16     | 幂                          | 从右到左      | `… ** …`         |
| 15     | 乘法                        | 从左到右      | `… * …`          |
|        | 除法                        |               | `… / …`          |
|        | 取模                        |               | `… % …`          |
| 14     | 加法                        | 从左到右      | `… + …`          |
|        | 减法                        |               | `… - …`          |
| 13     | 按位左移                    | 从左到右      | `… << …`         |
|        | 按位右移                    |               | `… >> …`         |
|        | 无符号右移                  |               | `… >>> …`        |
| 12     | 小于                        | 从左到右      | `… < …`          |
|        | 小于等于                    |               | `… <= …`         |
|        | 大于                        |               | `… > …`          |
|        | 大于等于                    |               | `… >= …`         |
|        | in                          |               | `… in …`         |
|        | instanceof                  |               | `… instanceof …` |
| 11     | 等号                        | 从左到右      | `… == …`         |
|        | 非等号                      |               | `… != …`         |
|        | 全等号                      |               | `… === …`        |
|        | 非全等号                    |               | `… !== …`        |
| 10     | 按位与                      | 从左到右      | `… & …`          |
| 9      | 按位异或                    | 从左到右      | `… ^ …`          |
| 8      | 按位或                      | 从左到右      | `… | …`          |
| 7      | 逻辑与                      | 从左到右      | `… && …`         |
| 6      | 逻辑或                      | 从左到右      | `… || …`         |
| 5      | 空值合并                    | 从左到右      | `… ?? …`         |
| 4      | 条件运算符                  | 从右到左      | `… ? … : …`      |
| 3      | 赋值                        | 从右到左      | `… = …`          |
|        |                             |               | `… += …`         |
|        |                             |               | `… -= …`         |
|        |                             |               | `… **= …`        |
|        |                             |               | `… *= …`         |
|        |                             |               | `… /= …`         |
|        |                             |               | `… %= …`         |
|        |                             |               | `… <<= …`        |
|        |                             |               | `… >>= …`        |
|        |                             |               | `… >>>= …`       |
|        |                             |               | `… &= …`         |
|        |                             |               | `… ^= …`         |
|        |                             |               | `…|=`…`          |
|        |                             |               | `… &&= …`        |
|        |                             |               | `…||=…`          |
|        |                             |               | `… ??= …`        |
| 2      | yield                       | 从右到左      | `yield …`        |
|        | yield*                      |               | `yield* …`       |
| 1      | 展开运算符                  | n/a           | `...` …          |
| 0      | 逗号                        | 从左到右      | `… , …`          |

## 语句

### 声明

#### let和const命令

> 在JS中，有六种声明变量的方式 var、let、const、function、import、class

`let`和`const`命令是ES6新增的命令，用来声明变量，它的用法类似于var。

1.作用域

​	被`let`和`const`命令声明的变量，只在let命令所在的代码块内生效，代码块外无法访问；

​	每次进入一个作用域时，会创建一个变量的 *环境*。当`let`声明出现在循环体里时拥有完全不同的行为。不仅是在循环里引入了一个新的变量环境，而是针对 *每次迭代*都会创建这样一个新作用域。

2.变量提升

​	与`var`不同，`let`和`const`声明的变量，虽然会被提升，但不会被初始化（var声明的变量被提升并初始化为undefined），即变量不能在声明之前使用，一旦使用就会报错。

3.暂时性死区

​	被`let`、`const`和`class`命令声明的变量，它们不能在被声明之前读或写。 **虽然这些变量始终“存在”于它们的作用域里，但在直到声明它的代码之前的区域都属于 *暂时性死区***。

4.重复声明

​	在同一个块级作用域中，被`let`和`const`声明的变量不可重复声明。

在ES6之前，JavaScript只有全局作用域和函数作用域，`let`命令实际上增加了块级作用域。块级作用域的应用场景：

​	1.在函数作用域内声明变量

​    2.在for循环中声明循环变量

`const`声明一个只读的常量。一旦声明，常量的值就不能改变。 

`const`实际上保证的，并不是变量的值不得改动，而是变量指向的那个栈内存地址所保存的数据不得改动。对于简单类型的数据（数值、字符串、布尔值），值就保存在变量指向的那个栈内存地址，因此等同于常量。但对于复合类型的数据（主要是对象和数组），变量指向的栈内存地址，保存的只是一个指向实际数据的指针，`const`只能保证这个指针是固定的（即总是指向另一个固定的地址），至于它指向的数据结构是不是可变的，就完全不能控制了。

### 判断

- if  else
- expression ？ A  ： B
- switch  case ；其中switch与case的比较是`===`

### 控制流、迭代

重复执行某些操作

循环体中的两个关键字：

continue：结束当前这轮循环（continue后面的代码不再执行），继续执行下一轮循环

break：强制结束整个循环（break后面的代码也不再执行）

- for 循环

- for in 循环 （主要为遍历{}而设计）

  obj中有多少个属性**（自身以及从原型对象那里继承的除Symbol以外的可枚举属性）**就循环多少次

  for(let key in obj){

  // 每次循环key变量存储的是当前对象的属性名

  // 获取属性值的方法  obj[key]

  // for in 在循环时优先循环数字属性名的属性（数字按照从小到大的顺序）

  }

- for of 循环（ES6新增）

  一个数据结构只要部署了`Symbol.iterator`属性，就被视为具有 iterator 接口，就可以用`for...of`循环遍历它的成员**(对象自身属性，不包含原型对象上的属性)**。也就是说，`for...of`循环内部调用的是数据结构的`Symbol.iterator`方法。

  `for...of`循环可以使用的范围包括数组、Set 和 Map 结构、某些类似数组的对象（比如`arguments`对象、DOM NodeList 对象）、后文的 Generator 对象，以及字符串。

- while循环

- do while循环



## 对象

> 在计算机科学中，对象是指内存中可以被标识符所引用的一块区域。
>
> JavaScript标准对基于对象的定义：**语言和宿主的基础设施由对象来提供，并且 JavaScript 程序即是一系列互相通讯的对象集合**。（表达了对象对JavaScript的重要性）

​		除了JavaScript原生对象和宿主对象外，用户还可以自定义对象，JavaScript中创建对象有三种方式：

​	一种为字面量方式。

​	一种为`new`关键字加构造函数的方式，这种方式创建对象会经历四个步骤：

​	（1）创建一个新对象

​	（2）将`this`指向新对象

​	（3）执行构造函数中的代码（为这个对象添加属性）

​	（4）返回新对象

​	对象也可以用 `Object.create()`方法创建。该方法非常有用，因为它允许你为创建的对象选择一个原型对象，而不用定义构造函数。

​		**对于基本类型的值，它本身不是基本类型在对象中所对应的类的实例（对象），之所以可以对其进行对象操作，如读取其默认属性，这是因为JavaScript引擎为了方便操作基本类型的数据，当处于读取模式时，会在后台把基本类型值转换为对应的对象，这个过程称为包装（从对象到基本类型值的转换过程称为拆包），该对象称作包装对象（包装对象模糊了基本类型与对象的关系），在读取操作结束后自动销毁对象；但不能添加新属性，因为写模式不会创建对应类型的对象**，引用类型的值为引用类型的一个实例，可以进行对象的各种操作。

### 对象模型

在JavaScript中，万物皆对象（基本类型的值的情况比较特殊），一个对象就是一个无序属性的集合（散列表），一个属性包含一个名和一个值。属性名可以是字符串或者 Symbol 类型，一个属性的值可以是函数，这种情况下属性也被称为*方法*。

+ 对象的基本特征

  + 对象具有唯一标识性：每个对象都是唯一的（通过内存地址来体现）。
  + 对象具有状态：对象具有状态，同一对象可能处于不同状态之下。
  + 对象具有行为：即对象的状态，可能因为它的行为而发生变迁。

  在JavaScript中，状态和行为都用属性来抽象。

  **JavaScript 中对象独有的特色是：对象具有高度的动态性，这是因为 JavaScript 赋予了使用者在运行时为对象添改状态和行为的能力（对象的原型在运行时可改变）**。

+ 对象的属性

  + 属性名（**字符串或Symbol值**）

    一个对象的属性名可以是任何有效的 JavaScript 字符串，或者可以被转换为字符串的任何类型，包括空字符串。

    **然而，一个属性的名称如果不是一个有效的 JavaScript 标识符（例如，一个由空格或连字符，或者以数字开头的属性名），就只能通过方括号标记访问。**

    注意：**方括号中的所有键都将转换为字符串类型**。

  + ECMAScript定义的对象中有两种属性：数据属性和访问器属性。

    + 数据属性是键值对， 并且每个数据属性拥有下列特性: 

    **数据属性的特性(Attributes of a data property)**

    | 特性             | 数据类型               | 描述                                                         | 默认值    |
    | :--------------- | :--------------------- | :----------------------------------------------------------- | :-------- |
    | [[Value]]        | **任何Javascript类型** | 包含这个属性的数据值。                                       | undefined |
    | [[Writable]]     | Boolean                | 如果该值为 `false，`则该属性的 [[Value]] 特性 不能被改变。   | false     |
    | [[Enumerable]]   | Boolean                | 如果该值为 `true，`则该属性可以用 [for...in](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in) 循环来枚举。 | false     |
    | [[Configurable]] | Boolean                | 如果该值为 `false，`则该属性不能被删除，并且 除了 [[Value]] 和 [[Writable]] 以外的特性都不能被改变。 | false     |

    + 访问器属性有一个或两个访问器函数 (get 和 set) 来存取数值。

    | 特性             | 类型                   | 描述                                                         | 默认值    |
    | :--------------- | :--------------------- | :----------------------------------------------------------- | :-------- |
    | [[Get]]          | 函数对象或者 undefined | 该函数使用一个空的参数列表，能够在有权访问的情况下读取属性值。另见 `get。` | undefined |
    | [[Set]]          | 函数对象或者 undefined | 该函数有一个参数，用来写入属性值，另见 `set。`               | undefined |
    | [[Enumerable]]   | Boolean                | 如果该值为 `true，则该属性可以用` [for...in](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in) 循环来枚举。 | false     |
    | [[Configurable]] | Boolean                | 如果该值为 `false，则该属性不能被删除，并且不能被转变成一个数据属性。` | false     |

    以上这些特性只有 JavaScript 引擎才用到，因此不能直接访问它们。所以特性被放在两对方括号中，而不是一对。

    > 定义属性及属性描述符的方法：Object.defineProperty([obj], [descriptor])
  >
    > 读取属性的特性的方法：Object.prototype.getOwnPropertyDescriptor([obj], [prop])

    注：当配置对象属性时，并不一定是该对象的自身属性，有可能是继承来的属性。
  
    ​		set 和 get 函数中的this对象为赋值时的this对象，不一定为定义该属性的对象。
  
  + 删除属性
  
    可以用 [delete](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/delete) 操作符删除一个**不是继承而来**和Configurable不为false的属性，如果删除成功，返回true，反之为false。
  
    注：通过 `var`, `const` 或 `let` 关键字声明的变量无法用 `delete` 操作符来删除

### 对象的分类

+ 宿主对象（host Objects）: 由JavaScript宿主环境提供的对象。
+ 内置对象（Built-in Objects）：由JavaScript语言提供的对象。
  + 固有对象（Intrinsic Objects）：由标准规定，随着JavaScript运行时创建而自动创建的对象实例。
  + 原生对象（Native Objects）：可以由用户通过Array、Date等内置构造器或者特殊语法创建的对象。
  + 普通对象（Ordinary Objects）：由{}语法、Object构造器或者class关键字定义类创建的对象，它能够被原型继承。

#### 内置对象-固有对象

> 由标准规定，随着JavaScript运行时创建而自动创建的对象实例。
>
> 固有对象在任何JavaScript代码执行前就已经被创建出来了，它们通常扮演着类似基础库的角色。

#### 内置对象-原生对象

> 能够通过语言本身的构造器创建的对象称为原生对象

![](.\TS\内置对象-元生对象.png)

### 对象属性

+ 对象的原型（prototype）属性指向另一个对象，本对象的属性继承自它的原型对象
+ 对象的类（class）属性是一个标识对象类型的字符串（内置构造函数生成的对象才具有该属性）
+ 对象的扩展标记（extensiable flag）指明了（在ECMAScript5中）是否可以向该对象添加新属性

### 基于原型的Object Oriented

> 面向对象编程是一种更接近人类思维模式的编程风格，正如它的名字所表达的意思，面向对象编程将代码组织到**对象的定义**当中，通过定义一组属性和一组对属性操作的方法，实现状态和行为的关联，其中，状态是对象的属性，行为是对象的方法（函数）。
>
> 面向对象的精髓在于消息的传递和处理。对象可以通过调用另一个对象的方法并向方法中传递数据来进行**信息的传递**，对象的方法在接收到信息过后便可以对**信息进行处理**。

+ 基于原型的类型的定义(描述一类对象所具有的属性和方法)

  在JavaScript中，没有类的机制，而是通过**原型**定义对象。每个对象由构造函数生成，也叫作这个构造函数的实例，每个构造函数都有一个隐藏属性`prototype`指向一个原型对象，由该构造函数生成的对象都继承于这个原型对象（即拥有原型对象的所有属性和方法），原型对象中有一个隐藏属性`constructor`指向构造函数（实例对象也继承了这一属性，但不属于它自身的属性），具有相同构造函数的对象（继承同一个原型对象）被称为同一个类的实例。

  **JavaScript中，创建自定义类型采用的是构造函数+原型的组合模式，构造函数模式用于定义实例属性，而原型模式用于定义方法和共享的属性。**

+ 基于原型链的继承机制

  在JavaScript中，没有类的机制，它的继承机制是基于原型链实现的，每个对象都有一个隐藏属性`__proto__`指向原型对象（与生成该对象的构造函数中的隐藏属性`prototype`指向的对象是同一个），并继承原型对象的所有属性和方法，原型对象又继承于另一个对象，这就形成了一条原型链，每条原型链的最顶端是Object构造函数的原型对象。



## 数组（有下划线的表示改变原数组）

> 值的有序集合，每个值称为一个元素，每个元素在数组中都有一个位置，以数字表示，称为索引。
>
> 数组是对象，所有的索引都是属性名，但只有在0~2^32-2之间的整数属性名才是索引。可以为数组创建任意名字的属性，但如果使用的属性时数组的索引，数组将会根据需要更新它们的`length`属性值。
>
> + **length**（该属性使其区别于常规的JavaScript对象）
>
>   数组的length属性值不一定等于数组元素的个数
>
>   + 针对非稀疏数组，该属性就是数组元素的个数
>   + 针对稀疏数组（不连续索引的数组），length比所有元素的索引要大

### 创建数组对象

+ 字面量：[]

+ 构造函数：new Array([arrayLength])、new Array(arrayValue...)

+ 静态方法：

  + **Array.from([likeArrayObject], ?mapfn, ?thisArg)**

    用于将类数组结构转换为数组实例

  + **Arrray.of()**

    用于将一组参数转换为数组实例

### 检测数组

**Array.isArray(arrObj)**

> 该方法可解决 `arrayObj instanceof Array`在arrayObj和Array来自不同框架时不适用的问题

### 迭代器方法

+ **keys()**：返回数组索引的迭代器
+ **values()**：返回数组元素的迭代器
+ **entries()**：返回索引/值对的迭代器

### 复制和填充方法

+ **<u>copyWithin(target,?start,?end)</u>**：浅复制数组的一部分到同一数组中的另一个位置，并返回它，不会改变原数组的长度。

  将从`start`索引开始到`end`索引结束（不包括`end`索引）的数组元素复制到`target`索引处

+ **<u>fill(value,?start,?end)</u>**：方法用一个固定值填充一个数组中从起始索引到终止索引内的全部元素。不包括终止索引

  + `value`

    用来填充数组元素的值。

  + `start` 可选

    起始索引，默认值为0。

  + `end` 可选

    终止索引，默认值为 `this.length`。

### 转换方法

+ **toLocaleString([locales[,options]])**：返回一个字符串表示数组中的元素。数组中的元素将使用各自的 `toLocaleString` 方法转成字符串，这些字符串将使用一个特定语言环境的字符串（例如一个逗号 ","）隔开。
+ **toString()**：返回一个字符串，表示指定的数组及其元素
+ **valueOf()**：返回数组本身
+ **join()**：将数组中的每个值的等效字符串拼接成一个以指定符号分隔的字符串

### 栈方法

+ **<u>push</u>(element1, ..., elementN)**：将一个或多个元素添加到数组的末尾，并返回该数组的新长度
+ **<u>pop()</u>**：从数组中删除最后一个元素，并返回该元素的值。此方法更改数组的长度

### 队列方法

+ **<u>shift()</u>**：从数组中删除**第一个**元素，并返回该元素的值。此方法更改数组的长度
+ **push()**

### 排序方法

+ **<u>reverse()</u>**：将数组中元素的位置颠倒，并返回该数组。数组的第一个元素会变成最后一个，数组的最后一个元素变成第一个。该方法会改变原数组

+ **<u>sort([compareFunction])</u>**

  + 没有compareFunction的情况

    如果没有指明 `compareFunction` ，那么元素会按照转换为的字符串的诸个字符的Unicode位点进行排序

  + 有compareFunction的情况

    - 如果 `compareFunction(a, b)` 小于 0 ，那么 a 会被排列到 b 之前（索引小的表示在前）；
- 如果 `compareFunction(a, b)` 等于 0 ， a 和 b 的相对位置不变。备注： ECMAScript 标准并不保证这一行为，而且也不是所有浏览器都会遵守（例如 Mozilla 在 2003 年之前的版本）；
    - 如果 `compareFunction(a, b)` 大于 0 ， b 会被排列到 a 之前（索引大的表示在后）。

    **a-b为升序排列，b-a为降序排列**

### 操作方法

+ **concat(value1[, value2[, ...[, valueN]]])**：用于合并两个或多个数组。此方法不会更改现有数组，而是返回一个新数组
+ **slice([begin[, end]])**：返回一个新的数组对象，这一对象是一个由 `begin` 和 `end` 决定的原数组的**浅拷贝**（包括 `begin`，不包括`end`）。原始数组不会被改变
+ **<u>splice(start[, deleteCount[, item1[, item2[, ...]]]])</u>**：通过删除或替换现有元素或者原地添加新的元素来修改数组,并以**数组形式返回被修改的内容**。此方法会改变原数组

### 搜索和位置方法

+ **indexOf(searchElement[, fromIndex])**：返回在数组中可以找到一个给定元素的第一个索引，如果不存在，则返回-1
+ **lastIndexOf(searchElement[, fromIndex])**：返回指定元素（也即有效的 JavaScript 值或变量）在数组中的最后一个的索引，如果不存在则返回 -1。从数组的后面向前查找，从 `fromIndex` 处开始
+ **includes(valueToFind[, fromIndex])**：用来判断一个数组是否包含一个指定的值，根据情况，如果包含则返回 true，否则返回false
+ **find((element, index, array) => {}, thisArg)**：返回数组中满足提供的测试函数的第一个元素的值。否则返回 `undefined`
+ **findIndex((element, index, array) => {}, thisArg)**：返回数组中满足提供的测试函数的第一个元素的**索引**。若没有找到对应元素则返回-1

### 迭代方法

每个方法接收两个参数：

以每一项为参数运行的函数，函数接收三个参数：数组元素、元素索引、数组本身。

可选的作为函数调用上下文的对象，即`this`的值。

+ **every()**：对数组每一项都运行传入函数，如果对每一项函数都返回true，则这个方法返回true
+ **filter()**：对数组每一项都运行传入函数，函数返回true的项会组成数组之后返回
+ **forEach()**：对数组每一项都运行传入函数，没有返回值
+ **map()**：对数组每一项都运行传入函数，返回由每次函数调用的结果构成的数组
+ **some()**：对数组每一项都运行传入函数，如果有一项函数返回true，则这个方法返回true

**以上方法都不改变调用它们的数组**

### 归并方法

+ **reduce(callback(accumulator, currentValue[, index[, array]])[, initialValue])**：对数组中的每个元素执行一个提供的**reducer**函数(升序执行)，将其结果汇总为单个返回值。

  回调函数第一次执行时，`accumulator` 和`currentValue`的取值有两种情况：如果调用`reduce()`时提供了`initialValue`，`accumulator`取值为`initialValue`，`currentValue`取数组中的第一个值；如果没有提供 `initialValue`，那么`accumulator`取数组中的第一个值，`currentValue`取数组中的第二个值。

+ **reduceRight(callback(accumulator, currentValue[, index[, array]])[, initialValue])**：对数组中的每个元素执行一个提供的**reducer**函数(从右到左执行)，将其结果汇总为单个返回值。



## 字符串

### 字符

> JavaScript字符串由16位码元组成。对多数字符来说，每16位码元对应一个字符，字符串对象的`length`属性值即为16位码元的个数。

### 创建字符串对象

`new String('str')`

### 字符相关方法

+ **charCodeAt(index)**：返回 `0` 到 `65535` 之间的整数，表示给定索引处的 UTF-16 代码单元

+ **String.fromCharCode(num1[, ...[, numN]])**：返回由指定的 UTF-16 代码单元序列创建的字符串

+ **charAt(index)**：从一个字符串中返回指定位置的字符

+ **codePointAt(pos)**：返回 一个 Unicode 编码点值的非负整数

+ **String.fromCodePoint(num1[, ...[, numN]])**：**返回使用指定的代码点序列创建的字符串**

+ **normalize([form])**：按照指定的一种 Unicode 正规形式将当前字符串正规化

  `form` 可选

  四种 Unicode 正规形式（Unicode Normalization Form）`"NFC"`、`"NFD"`、`"NFKC"`，或 `"NFKD"` 其中的一个, 默认值为 `"NFC"`。

  这四个值的含义分别如下：

  - `"NFC"`

    Canonical Decomposition, followed by Canonical Composition.

  - `"NFD"`

    Canonical Decomposition.

  - `"NFKC"`

    Compatibility Decomposition, followed by Canonical Composition.

  - `"NFKD"`

    Compatibility Decomposition.

### 操作方法

+ **concat(str2, [, ...strN])**：将一个或多个字符串与原字符串连接合并，形成一个新的字符串并返回
+ **slice(beginIndex[, endIndex])**：提取某个字符串的一部分，并返回一个新的字符串
+ **substring(indexStart[, indexEnd])**：返回一个字符串在开始索引到结束索引之间的一个子集, 或从开始索引直到字符串的末尾的一个子集



### 位置方法

+ **indexOf(searchValue [, fromIndex])**：返回调用它的 `String` 对象中第一次出现的指定值的索引，从 `fromIndex` 处进行搜索。如果未找到该值，则返回 -1
+ **lastIndexOf(searchValue [, fromIndex])**：返回调用`String` 对象的指定值最后一次出现的索引，在一个字符串中的指定位置 `fromIndex`处从后向前搜索。如果没找到这个特定值则返回-1



### 包含方法

+ **startsWith(searchString[, position])**：用来判断当前字符串是否以另外一个给定的子字符串开头，并根据判断结果返回 `true` 或 `false`

+ **endsWith(searchString[, length])**：用来判断当前字符串是否是以另外一个给定的子字符串“结尾”的，根据判断结果返回 `true` 或 `false`

  `searchString`

  要搜索的子字符串。

  `length` 可选

  作为 `str` 的长度。默认值为 `str.length`。

+ **includes(searchString[, position])**：判断一个字符串是否包含在另一个字符串中，根据情况返回 true 或 false

  `searchString`

  要在此字符串中搜索的字符串。

  `position` 可选

  从当前字符串的哪个索引位置开始搜寻子字符串，默认值为 `0`。

### 大小写转换方法

+ **toLowerCase()**：将调用该方法的字符串值转为小写形式，并返回
+ **toLocalLowerCase([locale, locale, ...])**：根据任何指定区域语言环境设置的大小写映射，返回调用字符串被转换为小写的格式
+ **toUpperCase()**：将调用该方法的字符串值转为大写形式，并返回
+ **toLocalUpperCase([locale, locale, ...])**：根据任何指定区域语言环境设置的大小写映射，返回调用字符串被转换为大写的格式



### 模式匹配方法

+ **match(regexp)**：检索返回一个字符串匹配正则表达式的结果

  **返回值**

  - 如果使用g标志，则将返回与完整正则表达式匹配的所有结果，但不会返回捕获组。
  - 如果未使用g标志，则仅返回第一个完整匹配及其相关的捕获组（`Array`）。 在这种情况下，返回的项目将具有如下所述的其他属性。
    - `groups`: 一个捕获组数组 或 `undefined`（如果没有定义命名捕获组）
    - `index`: 匹配的结果的开始位置
    - `input`: 搜索的字符串

+ **search(regexp)**：返回正则表达式在字符串中首次匹配项的索引;否则，返回 `-1`

+ **replace(regexp|substr, newSubStr|function)**：返回一个由替换值（`replacement`）替换部分或所有的模式（`pattern`）匹配项后的新字符串。模式可以是一个字符串或者一个正则表达式，替换值可以是一个字符串或者一个每次匹配都要调用的回调函数。**如果`pattern`是字符串，则仅替换第一个匹配项。**

  **参数**

  - `regexp `(pattern)

    一个`RegExp`对象或者其字面量。该正则所匹配的内容会被第二个参数的返回值替换掉。

  - `substr `(pattern)

    一个将被 `newSubStr` 替换的 `字符串`。其被视为一整个字符串，而不是一个正则表达式。仅第一个匹配项会被替换。

  - `newSubStr` (replacement)

    用于替换掉第一个参数在原字符串中的匹配部分的`字符串`。该字符串中可以内插一些特殊的变量名。参考下面的**使用字符串作为参数**。

  - `function` (replacement)

    一个用来创建新子字符串的函数，该函数的返回值将替换掉第一个参数匹配到的结果。参考下面的**指定一个函数作为参数**。

  **使用字符串作为参数**

  替换字符串可以插入下面的特殊变量名：

  | 变量名      | 代表的值                                                     |
  | ----------- | ------------------------------------------------------------ |
  | `$$`        | 插入一个 "$"。                                               |
  | `$&`        | 插入匹配的子串。                                             |
  | `$``        | 插入当前匹配的子串左边的内容。                               |
  | `$'`        | 插入当前匹配的子串右边的内容。                               |
  | `$*n*`      | 假如第一个参数是 `RegExp`对象，并且 n 是个小于100的非负整数，那么插入第 n 个括号匹配的字符串。提示：索引是从1开始。如果不存在第 n个分组，那么将会把匹配到到内容替换为字面量。比如不存在第3个分组，就会用“$3”替换匹配到的内容。 |
  | `*$<Name>*` | 这里*`Name`* 是一个分组名称。如果在正则表达式中并不存在分组（或者没有匹配），这个变量将被处理为空字符串。只有在支持命名分组捕获的浏览器中才能使用。 |

  **指定一个函数作为参数**

  函数的返回值作为替换字符串。 (注意：上面提到的特殊替换参数在这里不能被使用。) 另外要注意的是，如果第一个参数是正则表达式，并且其为全局匹配模式，那么这个方法将被多次调用，每次匹配都会被调用。

  下面是该函数的参数：

  | 变量名            | 代表的值                                                     |
  | ----------------- | ------------------------------------------------------------ |
  | `match`           | 匹配的子串。（对应于上述的$&。）                             |
  | `p1,p2, ...`      | 假如replace()方法的第一个参数是一个`RegExp`对象，则代表第n个括号匹配的字符串。（对应于上述的$1，$2等。）例如，如果是用 `/(\a+)(\b+)/` 这个来匹配，`p1` 就是匹配的 `\a+`，`p2` 就是匹配的 `\b+`。 |
  | `offset`          | 匹配到的子字符串在原字符串中的偏移量。（比如，如果原字符串是 `'abcd'`，匹配到的子字符串是 `'bc'`，那么这个参数将会是 1） |
  | `string`          | 被匹配的原字符串。                                           |
  | NamedCaptureGroup | 命名捕获组匹配的对象                                         |

+ **split([separator[, limit]])**：使用指定的分隔符（可以是一个字符串或正则表达式）将一个`String`对象分割成子字符串数组，以一个指定的分割字串来决定每个拆分的位置



### 其他方法

+ **padStart(argetLength [, padString])**：会用一个字符串填充当前字符串（如果需要的话则重复填充），返回填充后达到指定长度的字符串。从当前字符串的末尾（右侧）开始填充

  `targetLength`

  当前字符串需要填充到的目标长度。如果这个数值小于当前字符串的长度，则返回当前字符串本身

  `padString` 可选

  填充字符串。如果字符串太长，使填充后的字符串长度超过了目标长度，则只保留最左侧的部分，其他部分会被截断。此参数的缺省值为 " "（U+0020）

+ **padEnd(argetLength [, padString])**：会用一个字符串填充当前字符串（如果需要的话则重复填充），返回填充后达到指定长度的字符串。从当前字符串的开始（左侧）开始填充

+ **repeat(count)**：构造并返回一个新字符串，该字符串包含被连接在一起的指定数量的字符串的副本

+ **trim()**：从一个字符串的两端删除空白字符

+ **trimLeft()**：从一个字符串的首端移除空白字符

+ **trimRight()**：从一个字符串的末端移除空白字符

+ **localCompare()**



## 正则表达式





## Set和Map

### Set

> ES6 提供了新的数据结构 `Set`。它类似于数组，但是成员的值都是唯一的，没有重复的值。
>
> `Set`本身是一个构造函数，用来生成 `Set` 数据结构。
>
> `Set` 结构没有键名，只有键值（或者说键名和键值是同一个值）

#### 初始化

`Set`函数可以接受一个数组（或者具有 iterable 接口的其他数据结构）作为参数，用来初始化。

```javascript
// 例一
const set = new Set([1, 2, 3, 4, 4]);
[...set]
// [1, 2, 3, 4]

// 例二
const items = new Set([1, 2, 3, 4, 5, 5, 5, 5]);
items.size // 5

// 例三
const set = new Set(document.querySelectorAll('div'));
set.size // 56

// 类似于
const set = new Set();
document
 .querySelectorAll('div')
 .forEach(div => set.add(div));
set.size // 56
```

#### 值

向 Set 加入值的时候，不会发生类型转换，所以`5`和`"5"`是两个不同的值。Set 内部判断两个值是否不同，使用的算法叫做“Same-value-zero equality”，**它类似于精确相等运算符（`===`），主要的区别是向 Set 加入值时认为`NaN`等于自身，而精确相等运算符认为`NaN`不等于自身。**

**另外，两个对象总是不相等的。**



#### Set 实例的属性和方法

Set 结构的实例有以下属性。

- `Set.prototype.constructor`：构造函数，默认就是`Set`函数。
- `Set.prototype.size`：返回`Set`实例的成员总数。

Set 实例的方法分为两大类：操作方法（用于操作数据）和遍历方法（用于遍历成员）。

四个操作方法。

- `Set.prototype.add(value)`：添加某个值，返回 Set 结构本身。
- `Set.prototype.delete(value)`：删除某个值，返回一个布尔值，表示删除是否成功。
- `Set.prototype.has(value)`：返回一个布尔值，表示该值是否为`Set`的成员。
- `Set.prototype.clear()`：清除所有成员，没有返回值。

四个遍历方法，可以用于遍历成员。

- `Set.prototype.keys()`：返回键名的遍历器
- `Set.prototype.values()`：返回键值的遍历器
- `Set.prototype.entries()`：返回键值对的遍历器
- `Set.prototype.forEach()`：使用回调函数遍历每个成员

Set结构的默认遍历器接口（`Symbol.iterator`属性），就是`values`方法。

```javascript
let set = new Set(['red', 'green', 'blue']);

for (let item of set.keys()) {
  console.log(item);
}
// red
// green
// blue

for (let item of set.values()) {
  console.log(item);
}
// red
// green
// blue

for (let item of set.entries()) {
  console.log(item);
}
// ["red", "red"]
// ["green", "green"]
// ["blue", "blue"]

let set = new Set([1, 4, 9]);
set.forEach((value, key) => console.log(key + ' : ' + value))
// 1 : 1
// 4 : 4
// 9 : 9
```

### WeakSet

> WeakSet 结构与 Set 类似，也是不重复的值的集合

#### 实例属性和方法

属性

+ `Set.prototype.constructor`：构造函数，默认就是`Map`函数。

WeakSet 结构有以下三个方法。

- `WeakSet.prototype.add(value)`：向 WeakSet 实例添加一个新成员。
- `WeakSet.prototype.delete(value)`：清除 WeakSet 实例的指定成员。
- `WeakSet.prototype.has(value)`：返回一个布尔值，表示某个值是否在 WeakSet 实例之中。

#### 与Set的区别

+ WeakSet 的成员只能是对象，而不能是其他类型的值

```javascript
const ws = new WeakSet();
ws.add(1)
// TypeError: Invalid value used in weak set
ws.add(Symbol())
// TypeError: invalid value used in weak set
```

+ **WeakSet 中的对象都是弱引用，即垃圾回收机制不考虑 WeakSet 对该对象的引用**，也就是说，如果其他对象都不再引用该对象，那么垃圾回收机制会自动回收该对象所占用的内存，不考虑该对象还存在于 WeakSet 之中



### Map

#### 出现的背景

JavaScript 的对象（Object），本质上是键值对的集合（Hash 结构），但是传统上只能用字符串当作键。这给它的使用带来了很大的限制。

```javascript
const data = {};
const element = document.getElementById('myDiv');

data[element] = 'metadata';
data['[object HTMLDivElement]'] // "metadata"
```

上面代码原意是将一个 DOM 节点作为对象`data`的键，但是由于对象只接受字符串作为键名，所以`element`被自动转为字符串`[object HTMLDivElement]`。

为了解决这个问题，ES6 提供了 Map 数据结构。它类似于对象，也是键值对的集合，但是“键”的范围不限于字符串，各种类型的值（包括对象）都可以当作键。也就是说，Object 结构提供了“字符串—值”的对应，Map 结构提供了“值—值”的对应，是一种更完善的 Hash 结构实现。

#### 初始化

`Map`构造函数接受数组作为参数，任何具有 Iterator 接口、且每个成员都是一个双元素的数组的数据结构都可以当作`Map`构造函数的参数。

```javascript
const set = new Set([
  ['foo', 1],
  ['bar', 2]
]);
const m1 = new Map(set);
m1.get('foo') // 1

const m2 = new Map([['baz', 3]]);
const m3 = new Map(m2);
m3.get('baz') // 3
```

#### 键

如果 Map 的键是一个简单类型的值（数字、字符串、布尔值），则只要两个值严格相等，Map 将其视为一个键，比如`0`和`-0`就是一个键，布尔值`true`和字符串`true`则是两个不同的键。另外，`undefined`和`null`也是两个不同的键。虽然`NaN`不严格相等于自身，但 Map 将其视为同一个键。

**如果Map的键是引用类型的值时，只有对同一个对象的引用，Map 结构才将其视为同一个键。**

```javascript
let map = new Map();

map.set(-0, 123);
map.get(+0) // 123

map.set(true, 1);
map.set('true', 2);
map.get(true) // 1

map.set(undefined, 3);
map.set(null, 4);
map.get(undefined) // 3

map.set(NaN, 123);
map.get(NaN) // 123

map.set(['a'], 555);
map.get(['a']) // undefined
```

#### Map实例的属性和方法

Map 结构的实例有以下属性。

- `Set.prototype.constructor`：构造函数，默认就是`Map`函数。
- `Set.prototype.size`：返回`Map`实例的成员总数。

Map 实例的方法分为两大类：操作方法（用于操作数据）和遍历方法（用于遍历成员）。

五个操作方法。

+ `Map.prototype.set(key, value)`：`set`方法设置键名`key`对应的键值为`value`，然后返回整个 Map 结构。如果`key`已经有值，则键值会被更新，否则就新生成该键。
+ `Map.prototype.get(key)`：`get`方法读取`key`对应的键值，如果找不到`key`，返回`undefined`。
+ `Map.prototype.has(key)`：`has`方法返回一个布尔值，表示某个键是否在当前 Map 对象之中。
+ `Map.prototype.delete(key)`：`delete`方法删除某个键，返回`true`。如果删除失败，返回`false`。
+ `Map.prototype.clear()`：`clear`方法清除所有成员，没有返回值。

Map 结构原生提供三个遍历器生成函数和一个遍历方法。

- `Map.prototype.keys()`：返回键名的遍历器。
- `Map.prototype.values()`：返回键值的遍历器。
- `Map.prototype.entries()`：返回所有成员的遍历器。
- `Map.prototype.forEach()`：遍历 Map 的所有成员。

Map 结构的默认遍历器接口（`Symbol.iterator`属性），就是`entries`方法。

```javascript
// Map 的遍历顺序就是插入顺序。
const map = new Map([
  ['F', 'no'],
  ['T',  'yes'],
]);

for (let key of map.keys()) {
  console.log(key);
}
// "F"
// "T"

for (let value of map.values()) {
  console.log(value);
}
// "no"
// "yes"

for (let item of map.entries()) {
  console.log(item[0], item[1]);
}
// "F" "no"
// "T" "yes"

// 或者
for (let [key, value] of map.entries()) {
  console.log(key, value);
}
// "F" "no"
// "T" "yes"

// 等同于使用map.entries()
for (let [key, value] of map) {
  console.log(key, value);
}
// "F" "no"
// "T" "yes"
```

### WeakMap

> `WeakMap`结构与`Map`结构类似，也是用于生成键值对的集合

#### 实例属性和方法

实例属性

+ `Set.prototype.constructor`：构造函数，默认就是`WeakMap`函数。

实例方法

+ `Map.prototype.set(key, value)`：`set`方法设置键名`key`对应的键值为`value`，然后返回整个 Map 结构。如果`key`已经有值，则键值会被更新，否则就新生成该键。
+ `Map.prototype.get(key)`：`get`方法读取`key`对应的键值，如果找不到`key`，返回`undefined`。
+ `Map.prototype.has(key)`：`has`方法返回一个布尔值，表示某个键是否在当前 Map 对象之中。
+ `Map.prototype.delete(key)`：`delete`方法删除某个键，返回`true`。如果删除失败，返回`false`。

#### 与Map的区别

+ `WeakMap`只接受对象作为键名（`null`除外），不接受其他类型的值作为键名。

```javascript
const map = new WeakMap();
map.set(1, 2)
// TypeError: 1 is not an object!
map.set(Symbol(), 2)
// TypeError: Invalid value used as weak map key
map.set(null, 2)
// TypeError: Invalid value used as weak map key
```

+ `WeakMap`的键名所指向的对象，不计入垃圾回收机制

它的键名所引用的对象都是弱引用，即垃圾回收机制不将该引用考虑在内。因此，只要键名所引用的对象的其他引用都被清除，垃圾回收机制就会释放该对象所占用的内存。也就是说，一旦不再需要，WeakMap 里面的键名对象和所对应的键值对会自动消失，不用手动删除引用。

```javascript
const wm = new WeakMap();

const element = document.getElementById('example');

wm.set(element, 'some information');
wm.get(element) // "some information"
```

WeakMap 里面对`element`的引用就是弱引用，不会被计入垃圾回收机制。也就是说，上面的 DOM 节点对象的引用计数是`1`，而不是`2`。这时，一旦消除对该节点的引用，它占用的内存就会被垃圾回收机制释放。Weakmap 保存的这个键值对，也会自动消失。

**注意，WeakMap 弱引用的只是键名，而不是键值。键值依然是正常引用。**



## 函数

>函数是一段能够实现某个功能的JavaScript代码，只需定义一次，以后需要这个功能时，只需要执行函数即可。
>
>这种思想即是"封装"，封装的目的是减小重复代码，提供代码复用率（低耦合高内聚）

+ 函数种类

  + 普通函数：function关键字定义的函数
  + 箭头函数：用 => 运算符定义的函数
  + 方法：在class中定义的函数
  + 生成器函数：用function*定义的函数
  
  + 类：用class定义
  + 异步函数：被async关键字修饰的函数
  
+ 创建函数

  + 函数声明语句（声明提前）：函数声明语句并非真正的语句，它可以出现在全局代码或者内嵌在其他函数中，但不能块级作用域中

  + 函数表达式：可以出现在任何地方

  + 箭头函数：() => {}

  + Function构造函数

    函数体内创建的变量从函数体外无法获取，如果想要获取内部的信息，需要通过return返回值机制，将相关信息返回。

    注意：**return result返回的是result变量存储的值，而不是变量本身（倘若是变量本身，则就可以改变函数体内创建的变量，这与函数作用域的机制相违背），且运行完return语句后，将结束函数的执行**

    没有return语句或者return为空，函数默认返回值为undefined

+ 函数名

  函数是对象，函数名是指向函数的指针，ES6中所有的函数对象都会暴露一个只读的name属性，这个属性保存的是一个字符串化的函数名，若函数没有名称，则为空字符串（若为Function构造函数创建，则为"anonymous"）。如果函数是一个get、set或者使用bind()实例化，那么标识符前面会加上一个前缀“get [funName]”、"set [funName]"、"bound [funName]"

+ 传递参数

  在JavaScript中所有参数的传递是按值传递。

  对于基本类型的变量：传递的变量的值（值的拷贝）

  对于引用类型的变量：传递的也是变量的值，只不过该值是引用类型值在堆内存中的地址

+ 函数内部

  + arguments

    函数内部的一个类数组对象，包含调用函数时传入的所有参数

    该对象还有一个`callee`属性，是一个指向`arguments`对象所在函数的指针

  + this

  + caller

    函数对象的一个属性，该属性引用的是调用当前函数的函数，在全局作用域中调用函数则为`null`

  + new.target

    用于检测函数是否使用`new`关键字调用。若函数是正常调用，则`new.target`的值是undefined；如果是`new`关键字调用，则new.target为被调用的构造函数

+ 函数相关概念

  + 高阶函数

    以函数作为参数或返回值的函数称为高阶函数

  + first class functions

    在计算机科学当中，将能够作为函数的参数和返回值，以及赋值给变量的一类值称为First Class；

    可以作为函数的参数，但不能从函数返回，也不能赋给变量的一类值称为Second Class；

    不能作为函数参数和返回值，也不能赋给变量的一类值称为Third Class。

    将满足First Class定义条件的函数称为First Class Functions（即函数可以作为函数的参数和返回值以及赋值给变量），在JavaScript中，所有函数都属于这一类型。

+ 编写pure function的准则

  函数的功能是提供input到output的映射，除此之外，不应该再有其他对外部程序状态的影响（如函数在执行过后，改变了函数外的变量的值）；**对于相同的输入，永远输出相同的结果**；函数内部的任何计算都不应该影响到外部作用域的变量；函数计算所需要的外部值只能通过形参获取，并且不能改变向形参传递值的实参的值。

  一个pure function的输出仅仅取决于它的输入。

### this

`this`是 JavaScript 语言的一个关键字，为**执行上下文中的重要组成部分，指向本次调用的上下文对象**。

它是函数执行时，自动生成的一个对象，一般在函数体内部使用。

> ```javascript
> function test() {
> 　this.x = 1;
> }
> ```

上面代码中，函数`test`运行时，会创建一个与之相应的执行上下文，`this`的值也就随之确定。

也就是说在不同的执行上下文中，`this`的取值会有所不同。

那么，`this`的值是什么呢？

+ 全局执行上下文

  `this`值为全局对象（在浏览器中为window）

+ 函数执行上下文

  + 被一个引用对象调用

    `this`为该引用对象

  + 其他情况

    `this`值为全局对象或undefined（严格模式下）

**特殊情况：**

+ 箭头函数

  `this`为**定义**箭头函数的上下文对象

+ 在构造函数中

  `this`为实例对象

**apply、call、bind**

+ Function.prototype.apply()：调用有指定**`this`**值和参数的函数的结果。

  func.apply(thisArg, [argsArray])

+ Function.prototype.call()：使用调用者提供的 **`this` **值和参数调用该函数的结果。

  function.call(thisArg, arg1, arg2, ...)

  **call方法的性能要比apply好，原因在于apply的内部需要遍历[argsArray]，取出里面的参数到arguments中**

+ Function.prototype.bind()：返回一个原函数的拷贝，并拥有指定的 **`this`** 值和初始参数。

  function.bind(thisArg, arg1, arg2, ...)

### 闭包

> 在JavaScript中，所有函数都是闭包。

JavaScript权威指南解释：**函数的执行依赖于变量作用域，这个作用域是函数定义时决定的，而不是函数调用时决定的。**

因为JavaScript是基于词法作用域的语言，每一段JavaScript代码（全局代码或函数）都有一个与之关联的作用域链，该作用域链（一个对象列表或者链表，定义了“作用域”中的变量）是在静态分析阶段就已经确定，它与函数在哪定义有关，而与在哪执行无关，通过作用域链，函数内部可以访问外部函数作用域中定义的变量。

简单讲，**闭包就是绑定了作用域链的函数。它将外部函数作用域中的变量隐藏在作用域链中，因此看起来函数将变量“包裹”了起来。**

但这也会造成比较大的性能开销，因此，在闭包使用完成后应该将其销毁。对闭包不再引用就会自动将其销毁。

（注：在JavaScript中，如果一个对象不再被引用，那么这个对象就会被垃圾回收机制回收）

如下代码：

```JavaScript
var a=0;
function fn(){
	var a=1;
	function fm(){
		console.log(a);
	}
	return fm;
}
var f1=fn();
f1();//相当于fm函数运行；此时输出的是1；而不是0；虽然是在window中运行的；但是在fn中定义的；所以a找到的是fm上一级作用域fn的a；而不是window中的a；
```

**闭包的用处**

闭包可以用在许多地方。它的最大用处有两个，一个是可以读取函数内部的变量，另一个就是让这些变量的值始终保持在内存中。



## 异步

所谓"异步"，简单说就是一个任务不是连续完成的，可以理解成该任务被人为分成两段，先执行第一段，然后转而执行其他任务，等做好了准备，再回过头执行第二段。

比如，有一个任务是读取文件进行处理，任务的第一段是向操作系统发出请求，要求读取文件。然后，程序执行其他任务，等到操作系统返回文件，再接着执行任务的第二段（处理文件）。这种不连续的执行，就叫做异步。

相应地，连续的执行就叫做同步。由于是连续执行，不能插入其他任务，所以操作系统从硬盘读取文件的这段时间，程序只能干等着。

### 同步和异步、单线程和多线程

> 同步就是一个任务是连续完成的，中途不能插入其他任务；异步表示一个任务不是连续完成的，而被分成了几个阶段，在执行完一个阶段后可以转而执行其他的任务，在后来的某个时间点再来执行下一个阶段。**区分同步异步的关键是看一个任务是否连续执行完**。
>
> 线程是能独立运行的基本单位，是进程（操作系统进行资源分配的最小单位）中的运作单位。单线程就是在同一个时间点，只能干一件事，多线程表示可以同时干多件事。**区分单线程多线程的关键是看是否能同时执行多个任务**。
>

### 回调函数（解决了异步操作返回值获取的问题）

> JavaScript 语言对异步编程的实现，就是回调函数。所谓回调函数，就是把任务的第二段单独写在一个函数里面，等到重新执行这个任务的时候，就直接调用这个函数。回调函数的英语名字`callback`，直译过来就是"回头调用"。

读取文件进行处理，是这样写的。

```javascript
fs.readFile('/etc/passwd', 'utf-8', function (err, data) {
  if (err) throw err;
  console.log(data);
});
```

从系统本地存储中读取文件这个操作为异步操作（JavaScript运行时不需要等待读取操作完成，在发起读取操作后转而执行其他任务，直到**读取操作完成事件**发生，再将对应的**事件处理程序**推到自己的**任务队列**上去**等待执行**），该异步操作会返回读取到的文件数据，如何获取异步返回值成为需要解决的问题，广泛接受的一个策略便是给异步操作提供一个回调，该回调会在事件处理程序中被调用，即获取了文件数据后将其作为参数传递给回调函数。**因为闭包的存在，回调在事件处理程序执行时依然是可用的**。

### Promise（解决了异步逻辑的组织问题）

* **出现的背景**

> 在JavaScript中，由于其是单线程的，为了保证JS代码的执行效率，采用了异步编程技术，但这也带来了一个问题：对于异步代码的执行顺序就带来了不确定性。
> 为了保证代码执行顺序按照我们的意愿去执行，可以使用异步代码A中嵌套异步代码B，异步代码B中嵌套异步代码C，以此类推的方式进行编程来控制异步代码的执行顺序。但这又带来了另一个问题：这样的代码可读性太差，且难以维护。

* **概念**

  > Promise是一个构造函数对象，它可以通过它本身的机制和方法来控制异步操作的执行顺序，支持**优雅地定义和组织异步逻辑**。
  >
  > Promise是对尚不存在结果的一个替身。期约通常被用来封装一个异步操作，通过控制其自身的状态和内部的状态变化处理机制实现对异步操作的管理。
  >
  > Promise 是 JavaScript 语言提供的一种标准化的异步管理方式。

  + **期约状态机**

    Promise是一个有状态的对象（期约的状态是私有的，无法通过外部JavaScript代码检测和修改），可能处于下列三种状态之一：

    + 待定（pending）
    + 兑现（fulfilled，有时候也称为“解决”，resolved）
    + 拒绝（rejected）

    待定是期约的最初始状态，在待定状态下，期约可以落定为代表成功的兑现状态，或者代表失败的拒绝状态。

    期约**状态的改变是不可逆的**，且只有从待定转换为兑现或拒绝，期约的状态就不再改变。

  + **控制期约状态**

    执行器函数（执行函数是同步执行的）的职责：

    + 初始化期约的异步行为
    + 控制状态的最终切换

    控制期约状态的转换是通过执行器函数的两个函数参数实现的。这两个函数通常命名为resolve()和reject()，调用resolve()会把状态切换为兑现，调用reject()会把状态切换为拒绝

+ **期约的用途**

  + 利用自身的状态来表示一个异步操作的状态
  + 获取执行器中异步操作生成的值

  Promise接受一个executor，向这个executor传入了两个函数参数resolve、reject，当在executor中调用resolve(value)或reject(reason)时，Promise的状态就会由pending（待定）变为fulfilled（兑现）或rejected（拒绝），若状态变为fulfilled，那么将会执行该Promise对象then方法的第一个callback参数，并且前面的value（往往是异步返回值）还会作为参数传给callback；若为rejected，同理则执行then的第二个callback参数，或者执行catch的第一个callback参数。这样就可以控制异步操作的流程（当在executor中的异步操作中调用resolve()时，接下来便会执行then的第一个callback参数，这就实现了控制异步操作的先后执行顺序）
  **这就是Promise的作用了，简单来讲，就是能把原来的回调嵌套写法分离出来，用链式调用的方式执行回调函数（串行化异步任务）。**

+ **缺点**

  + 无法取消Promise，一旦新建它就会立即执行，无法中途取消。
  + Promise内部抛出的错误，只能通过拒绝处理程序捕获，不会反应到外部（在执行器中可以通过`try{}catch`捕获）。
  + 当处于pending状态时，无法得知目前进展到哪一个阶段（刚刚开始还是即将完成）。

+ **使用场景**

  出现异步回调嵌套需求时，就需要使用Promise 。

+ **意义**

  既保留了`JavaScript`的异步执行高效的优势，又解决了回调地狱的问题。



### 异步函数（用同步代码的形式完成异步功能）

> 异步函数，也称为“async/await”，是ES6期约模式在ECMAScript函数中的应用。
>
> 这个特性从行为和语法上都增强了JavaScript，让以同步方式写的代码能够异步执行。

+ 出现的背景

  > 通过Promise可以实现异步任务的串行化，解决了依赖回调的的难题，但又出现了另一个问题，任何需要访问Promise所产生值的代码都要放到Promise对应的处理程序中，这在一定程度上也不方便。

  `async`、`await`关键字是为了简化使用`Promise`异步编程。

+ `async`用于定义异步函数

  `async`关键字用来声明异步函数，该关键字可以用在函数声明、函数表达式、箭头函数和方法上。

  `async`函数仍然具有普通函数的正常行为，不过，异步函数始终返回一个 Promise对象（普通值会被包装成解决的Promise）。

  + `async`函数返回的Promise对象的状态，只有当内部所有`await`命令后面的 Promise 对象执行完才会发生变化，除非遇到以下情况：
    
    + 遇到`return`语句，返回的Promise对象变为`resolved`状态，返回值会被`then`方法回调函数接收
    
    + 抛出错误，返回的Promise对象变为`reject`状态，抛出的错误对象会被`catch`方法回调函数接收到，**`async`函数中断执行**
    
    + `await`命令后的Promise对象变为`reject`状态，拒绝原因会被`catch`方法回调函数接收到，**`async`函数中断执行**
    
      注意：不在`await`命令后的Promise对象变为`reject`状态，拒绝原因不会被异步函数捕获，**async函数不会中断执行**

  **注意：为避免`async`函数意外中断执行，应考虑将`await`命令放入`try{}catch`块中，或对命令后的Promise对象调用catch方法**

+ `await` （只能在async函数中使用）

  `await`操作符用于等待一个`Promise` 对象的结果，普通值会被包装成已经解决的Promise。

  JavaScript运行时在碰到`await`关键字，会暂停异步函数的执行，并记录在哪里暂停，等到**await右边的值可用（Promise对象有了解决值）**了，JavaScript运行时会向任务队列中推送一个任务，这个任务会恢复异步函数的执行。

**注意：**多个`await`命令后面的异步操作，如果不存在继发关系，最好让它们同时触发。写法如下。

```javascript
let [foo, bar] = await Promise.all([getFoo(), getBar()]);
```



## 模块

> 模块模式的思想：把逻辑分块，各自封装，相互独立，每个块自行决定对外暴露什么，同时自行决定引入执行哪些外部代码。
>
> 模块化系统设计基本要素：1、模块的定义 2、定义模块中如何引入其他模块的内容 3、定义如何导出模块中的内容

历史上，JavaScript 一直没有模块（module）体系，无法将一个大程序拆分成相互独立的小文件，再用简单的方法拼装起来。其他语言都有这项功能，比如 Ruby 的`require`、Python 的`import`，甚至就连 CSS 都有`@import`，但是 JavaScript 任何这方面的支持都没有，这对开发大型的、复杂的项目形成了巨大障碍。

在 ES6 之前，社区制定了一些模块加载方案，最主要的有 CommonJS 和 AMD（异步模块定义） 两种（UMD为二者的杂糅），前者用于服务器，后者用于浏览器。ES6 在语言标准的层面上，实现了模块功能，而且实现得相当简单，完全可以取代 CommonJS 和 AMD 规范，成为浏览器和服务器通用的模块解决方案。

> ES6 模块的设计思想是尽量的静态化，使得编译时就能确定模块的依赖关系，以及输入和输出的变量。CommonJS 和 AMD 模块，都只能在运行时确定这些东西。比如，CommonJS 模块就是对象，输入时必须查找对象属性。

```javascript
// CommonJS模块
let { stat, exists, readFile } = require('fs');

// 等同于
let _fs = require('fs');
let stat = _fs.stat;
let exists = _fs.exists;
let readfile = _fs.readfile;
```

上面代码的实质是整体加载`fs`模块（即加载`fs`的所有方法），生成一个对象（`_fs`）(此对象是模块的内置对象module.exports,模块内通过往该对象上挂载属性实现模块变量导出)，然后再从这个对象上面读取 3 个方法。这种加载称为“运行时加载”，因为只有运行时才能得到这个对象，导致完全没办法在编译时做“静态优化”。

ES6 模块不是对象，而是通过`export`命令显式指定输出的代码，再通过`import`命令输入。

```javascript
// ES6模块
import { stat, exists, readFile } from 'fs';
```

上面代码的实质是从`fs`模块加载 3 个方法，其他方法不加载。这种加载称为“编译时加载”或者静态加载，即 ES6 可以在编译时就完成模块加载。

* export命令

模块功能主要由两个命令构成：`export`和`import`。`export`命令用于规定模块的对外接口，`import`命令用于输入其他模块提供的功能。

一个模块就是一个独立的文件。该文件内部的所有变量，外部无法获取。如果你希望外部能够读取模块内部的某个变量，就必须使用`export`关键字输出该变量。

需要特别注意的是，`export`命令规定的是对外的接口，必须与模块内部的变量建立一一对应关系。

```javascript
// 报错
export 1;

// 报错
var m = 1;
export m;
```

上面两种写法都会报错，因为没有提供对外的接口。第一种写法直接输出 1，第二种写法通过变量`m`，还是直接输出 1。`1`只是一个值，不是接口。正确的写法是下面这样。

```javascript
// 写法一
export var m = 1;   

// 写法二
var m = 1;
export {m};

// 写法三
var n = 1;
export {n as m};
```

上面三种写法都是正确的，规定了对外的接口`m`。其他脚本可以通过这个接口，取到值`1`。它们的实质是，在接口名与模块内部变量之间，建立了一一对应的关系。

另外，`export`语句输出的接口，与其对应的值是动态绑定关系，即通过该接口，可以取到模块内部实时的值。**即模块内部变量和export导出的接口指向同一个内存地址，这一点与 CommonJS 规范完全不同。CommonJS 模块输出的是值的缓存，即内部变量的值，而不是拿到值的接口，故不存在动态更新**

* import命令

  通过import命令可以拿到模块通过export导出的接口。

  **注意：导入的接口是只读的接口，不可更改接口的指向，否则会报错。如果导出的接口指向的是{}，操作其属性不会报错，但不应该这样做**

import、export命令是在**静态解析阶段执行**的，所以它是一个模块之中最早执行的。

* export default命令

  用export命令导出的接口变量，在用import命令导入时必须要用相同名称的变量接受，

  原因在于一个模块可以有多个export命令，导出多个接口，这样在导入时就需要指明要导入的接口，因而需要用相同的名称来进行匹配（这里的思想和结构赋值是一样的）

  ```javascript
  import {A，B，C}
  
  import { A } from 'module';
  ```

`export default`命令用于指定模块的默认输出。显然，一个模块只能有一个默认输出，因此`export default`命令只能使用一次。所以，import命令后面才不用加大括号，因为只可能唯一对应`export default`命令。

下面比较一下默认输出和正常输出。

```javascript
// 第一组
export default function crc32() { // 输出
  // ...
}

import crc32 from 'crc32'; // 输入

// 第二组
export function crc32() { // 输出
  // ...
};

import {crc32} from 'crc32'; // 输入
```

+ export 与 import 的复合写法

```javascript
export { foo, bar } from 'my_module';

// 可以简单理解为
import { foo, bar } from 'my_module';
export { foo, bar };
```

 写成一行以后，`foo`和`bar`实际上并没有被导入当前模块，只是相当于对外转发了这两个接口，导致当前模块不能直接使用`foo`和`bar`。 

 模块的接口改名和整体输出，也可以采用这种写法 。

```javascript
// 接口改名
export { foo as myFoo } from 'my_module';

// 整体输出
export * from 'my_module';
```

默认接口的写法如下。

```javascript
export { default } from 'foo';
```

具名接口改为默认接口的写法如下。

```javascript
export { es6 as default } from './someModule';

// 等同于
import { es6 } from './someModule';
export default es6;
```

同样地，默认接口也可以改名为具名接口。

```javascript
export { default as es6 } from './someModule';
```

```javascript
export * as ns from "mod";

// 等同于
import * as ns from "mod";
export {ns};
```

+ import()

因为`import`命令会被JavaScript引擎静态分析，先于模块内的其他语句执行，所有 `import`和`export`命令只能在模块的顶层，不能在代码块之中 。

这样的设计使得条件加载不可能实现。因此， [ES2020提案](https://github.com/tc39/proposal-dynamic-import) 引入`import()`函数，支持动态加载模块。 

`import()`返回一个 Promise 对象。下面是一个例子。

```javascript
const main = document.querySelector('main');

import(`./section-modules/${someVariable}.js`)
  .then(module => {
    module.loadPageInto(main);
  })
  .catch(err => {
    main.textContent = err.message;
  });
```

 `import()`函数可以用在任何地方，不仅仅是模块，非模块的脚本也可以使用。它是运行时执行，也就是说，什么时候运行到这一句，就会加载指定的模块。  另外，`import()`函数与所加载的模块没有静态连接关系，这点也是与`import`语句不相同。  `import()`类似于 Node 的`require`方法，区别主要是前者是异步加载，后者是同步加载。 

+ ES6 模块与 CommonJS 模块的差异

  - CommonJS 模块输出的是一个值的拷贝，ES6 模块输出的是值的引用。

  - CommonJS 模块是运行时加载，ES6 模块是编译时输出接口。

    因为 CommonJS 模块对外输出的是一个对象（即`module.exports`），该对象只有在脚本运行完才会生成 。 而 ES6 模块的对外接口只是一种静态定义，在代码静态解析阶段就会生成。 

  - CommonJS 模块的`require()`是同步加载模块（服务器端的模块文件存储在本地磁盘，加载较快），ES6 模块的`import`命令是异步加载，有一个独立的模块依赖的解析阶段。

## 错误类型

Error

TypeError

SyntaxError

ReferenceError

RangeError

InternalError

EvalError

URIError

AggregateError



## JavaScript执行机制

### 浏览器环境下的JavaScript执行机制

主线程判断"任务队列"中是否非空，是则取出任务执行，否则等待新的任务。这个过程是循环不断的，所以整个的这种运行机制又称为Event Loop（事件循环）（这些任务通常都是某个事件的处理程序，当事件发生时被加入到任务队列，因此叫做事件循环）。

![](.\TS\event_loop.png)

+ **事件循环（Event Loop）**

  事件循环是一个在 JavaScript 引擎**等待任务**，**执行任务**和**进入休眠状态等待更多任务**这几个**状态**之间**转换**的**无限循环**。事件循环模型有效的避免了阻塞的发生。

   JS引擎在进入事件循环时，首先会将宏任务队列中的第一个宏任务（即整体代码）放到执行栈中执行（全局执行环境进栈），在执行过程中如果遇到同步任务会立即执行，遇到异步任务（分为宏任务和微任务）则会先将其挂起（异步任务会有相应的触发规则），继续执行执行栈中的其他任务。当一个异步任务被触发时，JS引擎需要执行该任务，如果此时引擎繁忙（无法立刻执行），会根据任务类型将任务放入**宏任务队列**或**微任务队列**。当执行栈中的所有任务都执行完毕， 主线程处于闲置状态时，主线程会依次执行当前微任务队列中的任务，所有微任务执行完后再去查找宏任务队列是否有任务，如果有，那么主线程会从中取出当前最早的宏任务，并进入执行栈执行，然后执行其中的同步任务...，如此反复，这样就形成了一个无限的循环。这就是这个过程被称为“事件循环（Event Loop）”的原因。

  **事件循环简化算法：**

  <img src=".\TS\event-loop.jpg" style="zoom: 25%;" />

  1. 从 **宏任务** 队列（例如 “script”）中出队（dequeue）并执行最早的任务。
  2. 执行宏任务中所有微任务：
     - 当微任务队列非空时：
       - 出队（dequeue）并执行最早的微任务。
  3. 执行渲染，如果有。
  4. 如果宏任务队列为空，则休眠直到出现宏任务。
  5. 转到步骤 1。

+ **执行（环境）栈**

  当我们执行函数的时候，js会生成一个与这个函数对应的执行环境（context），又叫执行上下文。这个执行环境中存在着这个函数的私有作用域，上层作用域的指向，函数的参数，这个作用域中定义的变量以及这个作用域的this对象。 而当一系列函数被嵌套依次调用的时候，对应的函数的执行环境会被依次压入一个栈中，在函数执行完后再将该执行环境弹出栈。这个栈被称为执行（环境）栈。

+ **宏任务（macrotask）和微任务（microtask）**

  + 宏任务

    > 由宿主环境发起的任务

  + 微任务

    > 由JavaScript引擎发起的任务

+ **异步执行顺序确定步骤**

  + 首先我们分析有多少个宏任务；
  + 在每个宏任务中，分析有多少个微任务；
  + 根据调用次序，确定宏任务中的微任务执行次序；
  + 根据宏任务的触发规则和调用次序，确定宏任务的执行次序；
  + 确定整个顺序。



## 垃圾回收机制

https://juejin.cn/post/6844904016325902344



# DOM

> DOM（Document Object Model）是W3C标准，一种平台和语言无关的接口标准。它提供了一套规范，程序和脚本可以按照这套规范动态地访问和更新结构化文档的内容，结构和样式。
>
> W3C Document Object Model分为三部分：
>
> - Core DOM - standard model for all document types
> - XML DOM - standard model for XML documents
> - HTML DOM - standard model for HTML documents

HTML DOM

> HTML DOM是HTML的标准**对象**模型和**编程接口**。它定义了：
>
> + HTML元素作为**对象**
> + 所有HTML元素的**属性**
> + 访问所有HTML元素的**方法**
> + 所有HTML元素的**事件**
>
> 也就是说HTML DOM是如何获取、改变、增加和删除HTML元素的标准。

DOM 编程接口

> HTML DOM可以用JavaScript实现（也可以用其他编程语言）。在DOM中，所有的HTML元素被定义为**对象**，编程接口就是每个对象的**方法**和**属性**。
>
> **属性**即是一个你能够获取和设置的值（如改变一个HTML元素的内容）。
>
> **方法**即是一个你可以做的行为（如添加和删除一个HTML元素）。

DOM Document

> HTML DOM document object是网页中所有其他对象的所有者。
>
> document object表示网页，它是获取HTML页面中任何元素的入口。



##  HTML DOM 

> 在web页面的加载完成后，浏览器会根据 DOM 模型（用来描述结构化文档），将结构化文档（比如 HTML 和 XML）解析成一系列的节点对象（文档中各部分都唯一对应一个节点对象），再由这些节点对象组成一个树状结构（DOM Tree）。所有的**节点**和最终的**树状结构**，都有规范的**对外接口**（节点对象的方法和属性）。

![](.\TS\pic_htmltree.gif)

### DOM Nodes

> 根据W3C HTML DOM标准，HTML文档中的任何内容都是一个node。
>
> 通过HTML DOM，节点树中的所有节点都可以使用JavaScript来获取，新的节点可以被创建、所有节点可以被修改或删除。

- The entire document is a document node
- Every HTML element is an element node
- The text inside HTML elements are text nodes
- Every HTML attribute is an attribute node (deprecated)
- All comments are comment nodes

### Node relationship

节点树中的节点之间具有层次关系。

The terms parent, child, and sibling are used to describe the relationships.

- In a node tree, the top node is called the root (or root node)
- Every node has exactly one parent, except the root (which has no parent)
- A node can have a number of children
- Siblings (brothers or sisters) are nodes with the same parent

描述这些节点之间的关系的属性。

- childNodes：获取所有的子节点
- children：获取所有的元素子节点（子元素标签）
- parentNode：获取父亲节点
- parentElement：获取父亲元素节点
- firstChild：获取第一个子节点
- lastChild：获取最后一个子节点
- firstElementChild/lastElementChild：获取第一个和最后一个元素子节点（不兼容IE6~8）
- previousSibling：获取上一个哥哥节点
- nextSibling：获取下一个弟弟节点
- previousElementSibling/nextElementSibling
- ....

### 几个重要的Node attribute

+ nodeName

  nodeName属性指定一个节点的名字

  - nodeName is read-only
  - nodeName of an element node is the same as the tag name
  - nodeName of an attribute node is the attribute name
  - nodeName of a text node is always #text
  - nodeName of the document node is always #document

+ nodeValue

  nodeValue属性指定一个节点的值

  - nodeValue for element nodes is `null`
  - nodeValue for text nodes is the text itself
  - nodeValue for attribute nodes is the attribute value

+ nodeType

  只读属性，返回一个节点的类型

  | Node                        | Type | Example                                         |
  | :-------------------------- | :--- | ----------------------------------------------- |
  | ELEMENT_NODE                | 1    | <h1 class="heading">W3Schools</h1>              |
  | ATTRIBUTE_NODE              | 2    | class = "heading" (deprecated)                  |
  | TEXT_NODE                   | 3    | W3Schools                                       |
  | PROCESSING_INSTRUCTION_NODE | 7    | <?a 1?>                                         |
  | COMMENT_NODE                | 8    | <!-- This is a comment -->                      |
  | DOCUMENT_NODE               | 9    | The HTML document itself (the parent of <html>) |
  | DOCUMENT_TYPE_NODE          | 10   | <!Doctype html>                                 |
  | DOCUMENT_FRAGMENT_NODE      | 11   |                                                 |

##  获取DOM元素（nodes）

- document.getElementById() 指定在文档中，基于元素的ID。
- [context].getElementsByTagName() 在指定上下文中，通过标签名获取一组元素集合。
- [context].getElementsByClassName() 在指定上下文中，通过样式类名获取一组元素集合（不兼容IE6~8）。
- document.getElementsByName() 在整个文档中，通过标签的name属性值获取一组元素集合（在IE中只有表单元素的name才能识别，所以一般只应用于表单处理）。
- document.head/document.body/document.documentElement 获取页面中的HEAD/BODY/HTML三个元素。
- [context].querySelector([selector])在指定上下文中，通过选择器获取到指定的元素对象
- [context].querySelectorAll([selector]) 在指定上下文中，通过选择器获取到指定的元素集合

> 以上方法可以帮我们获取到页面中的任意的元素，但只能通过在某个范围设置筛选条件的形式，这就限制了我们获取元素的途径，不够灵活，因此，还可以根据各节点之间的层级关系来获取节点对象，DOM中各个节点对象都具有描述节点间层级关系的属性，通过它们可以获取节点对象。

## 增删改DOM元素（nodes）

常用方法

`document.createElement`创建元素对象

`document.createTextNode`创建文本对象

`appendChild`把元素添加到容器的末尾

> [container].appendChild([节点对象])

`insertBefore`把元素添加到指定容器中指定元素的前面

> [container].insertBefore([新增元素],[指定元素])  // 指定元素要是容器的子元素

`cloneNode(true/false)` 克隆元素或节点，true表示深克隆，里面的节点也克隆，false表示浅克隆，不包含里面的节点

`removeChild`删除元素

> [container].removeChild(元素)

给元素设置自定义属性的方法（标签属性）

`[element].setAttribute`

`[element].getAttribute`

`[element].removeAttribute`

给元素对象设置自定义属性

[element].xxx = xxx

## 存放DOM节点的数据结构对象

> 节点：Node（页面中的所有东西都是节点）
>
> 节点都是单个对象，有些时候需要一种数据结构来容纳多个节点，DOM提供了两种数据结构，用来容纳节点集合。
>
> **节点集合**（可容纳各种类型的节点）：NodeList（getElementsByName/querySelectorAll获取的都是节点集合）
>
> **元素节点集合**（只能包含元素类型的节点）：
>
> HTMLCollection（getElementsByTagName/getElementsByClassName等获取的都是元素节点的集合）

## DOM CSS

```javascript
// 修改元素样式
[ELEMENT].style.xxx = xxx // 设置和修改元素的行内样式
[ELEMENT].className = xxx // 设置样式类
```

+ JS盒子模型属性

> 基于一些属性和方法，让我们能够获取对应元素的样式信息，例如：clientWidth、offsetWidth等
>
> + client
>   + width/height（可视区域内容宽高+PADDING）（没有单位）
>   + top/left
> + offset
>   + width/height（client+border）
>   + top/left
>   + parent
> + scroll
>   + width/height（内容的真实宽高）
>   + top/left
>
> 方法：window.getComputedStyle([ELEMENT],[伪类])/[ELEMENT].currentStyle

```javascript
let document.getElementById('box')
// 获取盒子可视化区域的宽高（CONTENT+PADDING）
//1、内容溢出与否对它没有影响
//2、获取的结果是没有单位的（其余的盒模型也是）
//3、获取的结果是整数，它会自己进行四舍五入（其余的盒模型也是）
box.clientWidth
box.clientHeight
//获取当前页面一屏幕（可视化）区域的宽高
let winWidth = document.body.clientWidth
let winHeight = document.body.clientHeight

// 获取盒子左边框和上边框的大小
box.clientLeft
box.clientTop

let box = document.getElementById('box')

// 在CLIENT的基础上加上BORDER（CONTENT+PADDING+BORDER） === 盒子本身的宽高
box.offsetWidth
box.offsetHeight

//在没有内容溢出的情况下，获取的结果和CLIENT是一样的
//在有内容溢出的情况下，获取的结果约等于真实内容的宽高
//1、不同浏览器获取的结果不同
//2、设置overflow属性值对最后的结果也会有影响
box.scrollWidth
box.scrollHeight

//获取页面真实高度
document.documentElement.scrollWidth
document.documentElement.scrollHeight

let box = document.getElementById('box')
//竖向滚动条卷去的高度
box.scrollTop
//横向滚动条卷去的宽度
box.scrollLeft
//边界值
//min=0，max= 整个的高度scrollHeight - 可视高度clientHeight

// 13个盒子模型属性，只有scrollTop、scrollLeft这两个是“可读写”属性，其余的都是“只读”属性

// offsetParent：获取它的父参照物（不一定是父元素）
// 父参照物与它的父元素没有必然联系；同一个平面中，最外层元素是所有后代元素的父参照物，而基于position：relative/absolute/fixed可以让元素脱离文档流（一个新的平面，其中relative不影响普通文档流布局），从而改变元素的父参照物
document.body.offsetParent // null

// offsetTop：距离其父参照物的上偏移
// offsetLeft：距离其父参照物的左偏移（当前元素的外边框到父参照物的里边框）

```

+ getComputedStyle

> 获取当前元素所有经过浏览器计算过的样式
>
> + 只要元素在页面中呈现出来，那么所有的样式都是经过浏览器计算的
> + 即使没有设置过样式，还有浏览器给元素的原生样式
>
> 在IE6~8浏览器中不兼容，用currentStyle来获取

```javascript
// 第一个参数是操作的元素，第二个参数是元素的伪类 ：after/：before
// 获取的结果是CSSStyleDeclaration这个类的实例（对象），包含了当前元素的所有样式信息
let styObj = window.getComputedStyle([element],null)
styleObj['属性名']
styleObj.属性名
```



## DOM Event和Event Listener

> HTML DOM Event允许JavaScript在HTML文档中的元素上注册不同的事件处理程序。
>
> 事件可以表示任何从基本的用户交互、到发生在渲染模型自动通知的任何事情

+ HTML Event Attribute

  ```html
  <button onclick="displayDate()">Try it</button>
  ```

+ HTML DOM

  ```html
  <script>document.getElementById("myBtn").onclick = displayDate;</script>
  ```

+ Event Listener

  ```javascript
  element.addEventListener(event, function, useCapture);
  element.removeEventListener(event, function);
  ```

  通过addEventListener方法可以为一个元素的同一个事件添加多个处理函数，不会发生覆盖。

  第一个参数是事件的类型（如`click`或`mousedown`或其他事件类型[HTML DOM Event](https://www.w3schools.com/jsref/dom_obj_event.asp)）

  第二个参数是事件处理函数（当事件发生时调用）。

  第三个为可选参数，是一个布尔值，默认为false，在冒泡阶段触发元素的事件监听器（the inner most element's event is handled first and then the outer）；若为true，则在捕获阶段触发元素的事件监听器（the outer most element's event is handled first and then the inner）。（事件的传播分为两个阶段：捕获（由外向内，从最外层元素向内直到事件目标元素）和冒泡（由内向外，从事件目标元素向外传播））。



# BOM

> Browser Object Model允许JavaScript与浏览器‘对话’。
>
> 浏览器对象模型（BOM）没有官方标准。
>
> 由于现代浏览器已经（几乎）实现了与JavaScript交互性相同的方法和属性，因此通常将其称为BOM的方法和属性。

## Window

> window对象被所有浏览器对象支持，它表示浏览器的窗口。
>
> 所有全局的JavaScript对象、函数和变量自动成为window对象的成员，全局变量是window对象的属性，全局函数是window对象的方法，document object也是window对象的属性。

### window.screen

> window.screen对象包含关于用户屏幕的相关信息。

属性:

- `screen.width`
- `screen.height`
- `screen.availWidth`
- `screen.availHeight`
- `screen.colorDepth`
- `screen.pixelDepth`

### window.location

> window.location对象可用于获取当前页面地址（URL）并将浏览器重定向到新页面。

- `window.location.href` returns the href (URL) of the current page
- `window.location.hostname` returns the domain name of the web host
- `window.location.pathname` returns the path and filename of the current page
- `window.location.protocol` returns the web protocol used (http: or https:)
- `window.location.assign()` loads a new document

### window.history

> window.history对象包含浏览器的历史记录。

### window.navigator

> window.navigator对象包含有关访问者浏览器的信息。

### popup boxes

> 三种盒子：alert box、confirm box、prompt box

+ window.alert
+ window.confirm
+ window.prompt

### Timing events

- window.setTimeout(*function*, *milliseconds*)
  Executes a function, after waiting a specified number of milliseconds.

- window.clearTimeout(*timeoutVariable*)

  ```javascript
  myVar = setTimeout(function, milliseconds);
  clearTimeout(myVar);
  ```

- window.setInterval(*function*, *milliseconds*)
  Same as setTimeout(), but repeats the execution of the function continuously.

- window.clearInterval(*timerVariable*)

  ```javascript
  myVar = setInterval(function, milliseconds);
  clearInterval(myVar);
  ```

### Cookies

> 用来在网页中存储用户信息。

Cookies是存储在您计算机上的小型文本文件中的数据。

Web服务器将网页发送到浏览器后，连接将关闭，并且服务器会忘记有关用户的所有信息。

Cookies被发明来解决“如何记住有关用户的信息”的问题：

+ 当用户访问网页时，他/她的名字可以存储在cookie中。
+ 下次用户访问页面时，Cookie会“记住”他/她的名字。



**关于强类型和弱类型；动态类型检查和静态类型检查；编译型和解释型**

> 动态类型检查是指在运行期间才去做数据类型检查的语言，也就是说，动态类型的语言是在第一次赋值给变量时，才确定变量类型；静态类型检查则是在编译阶段确定变量类型。
>
> 弱类型语言是指类型检查不严格，容忍隐式类型转换；强类型则是不容忍隐式类型转换，如果发现类型错误就会中断程序的执行。
>
> 编译型是指在代码在执行之前先将它编译成机器码，再由机器执行；解释型则是指代码在执行前不需要提前编译，而是在执行时再进行解释执行；编译型和解释型是**实现语言**的特性。
>
> **区分静态和动态的关键在于：在什么时候进行类型检查（而不是是否有变量类型声明），在运行时则为动态，在编译阶段则为静态**
>
> **区分强弱类型的关键在于：是否容忍隐式类型转换**

