# JavaScript

> Javascript是一门单线程语言，所谓单线程，是指在JS引擎中负责解释和执行JavaScript代码的线程只有一个。
> Event Loop是Javascript的执行机制。

### JavaScript的定义

+ node中的JavaScript

EcmaScript、核心模块（http、fs等）、第三方模块、用户自定义模块

+ 浏览器中的JavaScript

EcmaScript、DOM、BOM、第三方库、用户自定义对象

## 数据类型

数据类型实际指的就是值（字面量）的类型，在JavaScript中，有8种数据类型，分别是

7种基本类型：

String、Number、Boolean、Undefined、Null、BigInt、Symbol

和引用类型Object

其中Object包括简单对象{}、function (){}、[]、/^$/等不同类型的对象。

基本类型的值存储在栈内存中，引用类型的值存储在堆内存中。

+ 基本类型的值

  除 Object 以外的所有类型都是不可变的（值本身无法被改变）。例如，与 C 语言不同，JavaScript 中字符串是不可变的（译注：如，JavaScript 中对字符串的操作一定返回了一个新字符串，原始字符串并没有被改变）。我们称这些类型的值为“原始值”。

### JS中的数据类型检测

- typeof [val]: 用于检测数据类型的运算符

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

- instanceof ： 用来检测当前实例是否隶属于某个类

- constructor ： 基于构造函数检测数据类型

- Object.prototype.toString.call() : 检测数据类型最好的方法

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


### null与undefined

null与undefined是JavaScript的两个基本数据类型，都表示没有。

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

> 在JS中，有六种声明变量的方式 var、let、const、function、import、Class、Symbol

`let`和`const`命令是ES6新增的命令，用来声明变量，它的用法类似于var。

1.作用域

​	被`let`和`const`命令声明的变量，只在let命令所在的代码块内生效，代码块外无法访问；

​	每次进入一个作用域时，会创建一个变量的 *环境*。当`let`声明出现在循环体里时拥有完全不同的行为。 不仅是在循环里引入了一个新的变量环境，而是针对 *每次迭代*都会创建这样一个新作用域。

2.变量提升

​	与`var`不同，`let`和`const`声明的变量，虽然会被提升，但不会被初始化（var声明的变量被提升并初始化为undefined），即变量不能在声明之前使用，一旦使用就会报错。

3.暂时性死区

​	被`let`和`const`命令声明的变量，它们不能在被声明之前读或写。 **虽然这些变量始终“存在”于它们的作用域里，但在直到声明它的代码之前的区域都属于 *暂时性死区***。

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



## 变量

> 用来保存值的标识符。

在JavaScript中，变量是松散类型的，即可以用来保存任意类型的值（变量与类型之间不存在固定关系）。

变量可能包含两种数据类型的值：基本类型的值和引用类型的值。

基本类型的值直接存储在变量所关联的栈内存中（变量本身也存储在栈内存中）；引用类型的值由于保存在堆内存中，所以变量所关联的栈内存中存储的是值在堆内存中的地址。

### 执行环境（context）

>执行环境：定义了 变量有权访问的其他数据。**每个执行环境都有一个与之相关联的变量对象**，环境中定义的所有变量都保存在这个对象中。

- 全局执行环境

  全局执行环境中的数据能够被在任何地方的变量访问，根据ECMAScript实现所在的宿主环境不同，表示执行环境的对象也不一样，在浏览器中，window对象就是全局执行环境。

- 局部执行环境

  函数内部对外是封闭，只有函数内部的变量才有权访问其中定义的其他数据，一个函数对象就是一个局部执行环境（简单来说，局部执行环境就是非全局执行环境）。

### 作用域

从字面上的意思来看就是起作用的范围、区域；在计算机程序中，是指标识符能够作用到的代码块；作用域的分布结构是从全局作用域向内逐层嵌套。

+ 作用域类型

  + 全局作用域

    任何函数作用域和块级作用域之外的范围

  + 函数作用域

    函数代码块的范围

  + 块级作用域

    一个代码块（{}）的范围，由let关键字声明的变量具有块级作用域

+ 静态作用域和动态作用域

> javascript中的作用域是静态作用域。静态作用域是指在标识符定义的时候，其作用域就已经确定了，即表现为静态的；动态作用域是指当调用标识符时，其作用域才随之确定，即表现为动态的。

+ 作用域链

> 当代码在一个环境中执行时，会创建变量对象的一个作用域链。作用域链的用途，是**保证对执行环境有权访问的所有变量和函数的有序访问**。当**前执行的代码所在环境的变量对象**始终是**作用域链**的**始端**，作用域链中的下一个变量对象来自前一个变量对象的父执行环境，依次类推，一直到全局执行环境的变量对象；**全局执行环境的变量对象**始终是**作用域链**中的**最后**一个对象。

## 关于强类型和弱类型；动态类型检查和静态类型检查；编译型和解释型

> 动态类型检查是指在运行期间才去做数据类型检查的语言，也就是说，动态类型的语言是在第一次赋值给变量时，才确定变量类型；静态类型检查则是在编译阶段确定变量类型。
>
> 弱类型语言是指类型检查不严格，容忍隐式类型转换；强类型则是不容忍隐式类型转换，如果发现类型错误就会中断程序的执行。
>
> 编译型是指在代码在执行之前先将它编译成机器码，再由机器执行；解释型则是指代码在执行前不需要提前编译，而是在执行时再进行解释执行；编译型和解释型是**实现语言**的特性。
>
> **区分静态和动态的关键在于：在什么时候进行类型检查（而不是是否有变量类型声明），在运行时则为动态，在编译阶段则为静态**
>
> **区分强弱类型的关键在于：是否容忍隐式类型转换**



## JS中的对象

> 在计算机科学中，对象是指内存中可以被标识符所引用的一块区域

在JavaScript中，万物皆对象，一个对象就是一个无序属性的集合，一个属性包含一个名和一个值。一个属性的值可以是函数，这种情况下属性也被称为*方法*。每个对象由构造函数（通过构造函数定义一类对象的属性和方法）生成，也叫作这个构造函数的实例，每个构造函数都有一个隐藏属性`prototype`指向一个原型对象，由该构造函数生成的对象都继承于这个原型对象（即继承原型对象的所有属性和方法），原型对象中有一个隐藏属性`constructor`指向构造函数（实例对象也继承了这一属性，但不属于它自身的属性），具有相同构造函数的对象（继承同一个原型对象）被称为同一类对象。

+ 对象的创建

  除了JavaScript原生对象和宿主对象外，用户还可以自定义对象，JavaScript中创建对象有三种方式，一种为字面量方式，一种为`new`关键字加构造函数的方式，对象也可以用 `Object.create()`方法创建。该方法非常有用，因为它允许你为创建的对象选择一个原型对象，而不用定义构造函数。

  ​		**对于基本类型的值，它本身不是对应基本类型的实例（对象），之所以可以对其进行对象操作，如读取其默认属性，这是因为JavaScript引擎为了方便操作基本类型的数据，当处于读取模式时，会在后台创建对应基本类型的对象，在读取操作结束后自动销毁对象；但不能添加新属性，因为写模式不会创建对应类型的对象**，引用类型的值为引用类型的一个实例，可以进行对象的各种操作。

+ 对象的属性

  + 属性名

    一个对象的属性名可以是任何有效的 JavaScript 字符串，或者可以被转换为字符串的任何类型，包括空字符串。

    **然而，一个属性的名称如果不是一个有效的 JavaScript 标识符（例如，一个由空格或连字符，或者以数字开头的属性名），就只能通过方括号标记访问。**

    注意：方括号中的所有键都将转换为字符串类型。

  + ECMAScript定义的对象中有两种属性：数据属性和访问器属性。

    + 数据属性是键值对， 并且每个数据属性拥有下列特性: 

    **数据属性的特性(Attributes of a data property)**

    | 特性             | 数据类型           | 描述                                                         | 默认值    |
    | :--------------- | :----------------- | :----------------------------------------------------------- | :-------- |
    | [[Value]]        | 任何Javascript类型 | 包含这个属性的数据值。                                       | undefined |
    | [[Writable]]     | Boolean            | 如果该值为 `false，`则该属性的 [[Value]] 特性 不能被改变。   | false     |
    | [[Enumerable]]   | Boolean            | 如果该值为 `true，`则该属性可以用 [for...in](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in) 循环来枚举。 | false     |
    | [[Configurable]] | Boolean            | 如果该值为 `false，`则该属性不能被删除，并且 除了 [[Value]] 和 [[Writable]] 以外的特性都不能被改变。 | false     |

    + 访问器属性有一个或两个访问器函数 (get 和 set) 来存取数值。

    | 特性             | 类型                   | 描述                                                         | 默认值    |
    | :--------------- | :--------------------- | :----------------------------------------------------------- | :-------- |
    | [[Get]]          | 函数对象或者 undefined | 该函数使用一个空的参数列表，能够在有权访问的情况下读取属性值。另见 `get。` | undefined |
    | [[Set]]          | 函数对象或者 undefined | 该函数有一个参数，用来写入属性值，另见 `set。`               | undefined |
    | [[Enumerable]]   | Boolean                | 如果该值为 `true，则该属性可以用` [for...in](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in) 循环来枚举。 | false     |
    | [[Configurable]] | Boolean                | 如果该值为 `false，则该属性不能被删除，并且不能被转变成一个数据属性。` | false     |

    以上这些特性只有 JavaScript 引擎才用到，因此不能直接访问它们。所以特性被放在两对方括号中，而不是一对。

    注：当配置对象属性时，并不一定是该对象的自身属性，有可能是继承来的属性。

    ​		set 和 get 函数中的this对象为赋值时的this对象，不一定为定义该属性的对象。

  + 删除属性
  
    可以用 [delete](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/delete) 操作符删除一个**不是继承而来**和Configurable不为false的属性，如果删除成功，返回true，反之为false。
  
    注：通过 `var`, `const` 或 `let` 关键字声明的变量无法用 `delete` 操作符来删除

**使用new关键字和构造函数创建对象的过程**

1、在内存中开辟空间，用于存储新对象

2、把`this`与该存储空间相关联，使其指向该存储空间

3、在开辟的空间内存储对象的属性和方法的值

4、把`this`返回

```javascript
let obj = new Test()
//1. let obj = {}
//2. obj.__proto__ = Test.prototype
//3. Test.call(obj)
```

### 内置对象

+ parseInt(string, radix)

  解析一个字符串并返回指定基数的十进制整数， `radix` 是2-36之间的整数，表示被解析字符串的基数。

  注：如果 `parseInt `遇到的字符不是指定 `radix `参数中的数字，它将忽略该字符以及所有后续字符，并返回到该点为止已解析的整数值。 `parseInt` 将数字截断为整数值。 允许前导和尾随空格。

+ parseFloat(string)

  给定值被解析成浮点数。如果给定值不能被转换成数值，则会返回 `NaN`。

+ isNaN()

  如果给定值为 `NaN`（not a number）则返回值为`true`；否则为`false`。

  **`Number.isNaN()`** 方法确定传递的值是否为 `NaN`，并且检查其类型是否为 `Number`。

  注：和全局函数 `isNaN()`相比，`Number.isNaN()` 不会自行将参数转换成数字，只有在参数值为 `NaN` 的数字时，才会返回 `true`。

### 基于原型链实现的Object Oriented

面向对象编程是一种编程方法，正如它的名字所表达的意思，面向对象编程将代码组织到对象的定义当中，或者说类的定义当中，将具有相关行为的数据分组在一起，其中，数据是对象的属性，行为（或者函数）是对象的方法。面向对象的精髓在于消息的传递和处理。

对象可以通过调用另一个对象的方法并向方法中传递数据来进行**信息的传递**,对象的方法在接收到信息过后便可以对**信息进行处理**。一个类可以从另一个类继承它所有的特征，这个被继承的类就称为继承它的类的父类，这种类的继承机制可以有效的减少代码的重复量。

在JavaScript中，没有类的机制，而是通过构造函数定义对象，同时，它的继承机制是基于原型链实现的，每个对象都有一个隐藏属性`__proto__`指向原型对象（与生成该对象的构造函数中的隐藏属性`prototype`指向的对象是同一个），并继承原型对象的所有特征，原型对象也可能继承于另一个对象，这就形成了一条原型链，每条原型链的最顶端是Object构造函数的原型对象。



## JavaScript执行机制

#### 浏览器环境下的JavaScript执行机制

主线程从"任务队列"中读取事件，这个过程是循环不断的，所以整个的这种运行机制又称为Event Loop（事件循环）。

![](.\TS\event_loop.png)

+ **事件循环（Event Loop）**

  事件循环是一个在 JavaScript 引擎等待任务，执行任务和进入休眠状态等待更多任务这几个状态之间转换的无限循环。事件循环模型有效的避免了阻塞的发生。

   JS引擎在进入事件循环时，首先会将宏任务队列中的第一个宏任务（即整体代码）放到执行栈中执行（全局执行环境进栈），在执行过程中如果遇到同步任务会立即执行，遇到异步任务（分为宏任务和微任务）则会先将其挂起（异步任务派生出对应事件和事件处理程序），继续执行执行栈中的其他任务。当一个异步事件发生时，JS引擎需要执行该事件的处理程序，如果此时引擎繁忙，会根据事件类型将事件放入宏任务事件队列或微任务事件队列。当执行栈中的所有任务都执行完毕， 主线程处于闲置状态时，主线程会依次执行当前微任务事件队列中事件所对应的处理程序，执行完后再去查找宏任务事件队列是否有任务，如果有，那么主线程会从中取出排在第一位的事件，并把这个事件对应的回调（事件处理程序）放入执行栈中，然后执行其中的同步任务...，如此反复，这样就形成了一个无限的循环。这就是这个过程被称为“事件循环（Event Loop）”的原因。

  **事件循环简化算法：**

  1. 从 **宏任务** 队列（例如 “script”）中出队（dequeue）并执行最早的任务。
  2. 执行所有微任务：
     - 当微任务队列非空时：
       - 出队（dequeue）并执行最早的微任务。
  3. 执行渲染，如果有。
  4. 如果宏任务队列为空，则休眠直到出现宏任务。
  5. 转到步骤 1。

+ **执行（环境）栈**

  当我们执行函数的时候，js会生成一个与这个函数对应的执行环境（context），又叫执行上下文。这个执行环境中存在着这个函数的私有作用域，上层作用域的指向，函数的参数，这个作用域中定义的变量以及这个作用域的this对象。 而当一系列函数被嵌套依次调用的时候，对应的函数的执行环境会被依次压入一个栈中，在函数执行完后再将该执行环境弹出栈。这个栈被称为执行（环境）栈。

+ **宏任务（macrotask）和微任务（microtask）**

  + 宏任务

    宏任务包含：script(整体代码)、setTimeout、setInterval、I/O、UI交互事件、postMessage、MessageChannel、setImmediate(Node.js 环境)

  + 微任务

    在宏任务执行期间如果遇到微任务，并不会立刻执行它们，而是依次将它们放到一个队列（称为微任务队列microtask queue）中，在当前宏任务执行完后，再将微任务队列中的微任务依次全部执行完。

    常见微任务有：Promise.then\catch\finally、MutaionObserver、process.nextTick(Node.js 环境)

+ **注意**

  + 在不同环境下，JavaScript的执行机制是不同，主要体现在事件队列的分类和各事件队列的执行顺序上。
  + 引擎执行任务时永远不会进行渲染（render）。如果任务执行需要很长一段时间也没关系。仅在任务完成后才会绘制对 DOM 的更改。
  + 如果一项任务执行花费的时间过长，浏览器将无法执行其他任务，无法处理用户事件，因此，在一定时间后浏览器会在整个页面抛出一个如“页面未响应”之类的警报，建议你终止这个任务。这种情况常发生在有大量复杂的计算或导致死循环的程序错误时。



## 异步

所谓"异步"，简单说就是一个任务不是连续完成的，可以理解成该任务被人为分成两段，先执行第一段，然后转而执行其他任务，等做好了准备，再回过头执行第二段。

比如，有一个任务是读取文件进行处理，任务的第一段是向操作系统发出请求，要求读取文件。然后，程序执行其他任务，等到操作系统返回文件，再接着执行任务的第二段（处理文件）。这种不连续的执行，就叫做异步。

相应地，连续的执行就叫做同步。由于是连续执行，不能插入其他任务，所以操作系统从硬盘读取文件的这段时间，程序只能干等着。

ES6 诞生以前，异步编程的方法，大概有下面四种。

- 回调函数
- 事件监听
- 发布/订阅
- Promise 对象

### 同步和异步、单线程和多线程、串行和并行

> 同步就是一个任务是连续完成的，中途不能插入其他任务；异步表示一个任务不是连续完成的，而被分成了几个阶段，在执行完一个阶段后可以转而执行其他的任务，在后来的某个时间点再来执行下一个阶段。**区分同步异步的关键是看一个任务是否连续执行完**。
>
> 线程是能独立运行的基本单位，是进程（操作系统进行资源分配的最小单位）中的运作单位。单线程就是在同一个时间点，只能干一件事，多线程表示可以同时干多件事。**区分单线程多线程的关键是看是否能同时执行多个任务**。
>
> 串行和并行这个概念是数据传输的两种方式，串行传输表示数据是一位接一位的传送；并行传输则是一次传输多位数据。

### 回调函数

> JavaScript 语言对异步编程的实现，就是回调函数。所谓回调函数，就是把任务的第二段单独写在一个函数里面，等到重新执行这个任务的时候，就直接调用这个函数。回调函数的英语名字`callback`，直译过来就是"重新调用"。

读取文件进行处理，是这样写的。

```javascript
fs.readFile('/etc/passwd', 'utf-8', function (err, data) {
  if (err) throw err;
  console.log(data);
});
```

上面代码中，`readFile`函数的第三个参数，就是回调函数，也就是任务的第二段。等到操作系统返回了`/etc/passwd`这个文件以后，回调函数才会执行。

一个有趣的问题是，为什么 Node 约定，回调函数的第一个参数，必须是错误对象`err`（如果没有错误，该参数就是`null`）？

原因是执行分成两段，第一段执行完以后，任务所在的上下文环境就已经结束了。在这以后抛出的错误，原来的上下文环境已经无法捕捉，只能当作参数，传入第二段。



### Promise

* **出现的背景**

> 在JavaScript中，由于其是单线程的，为了保证JS代码的执行效率，采用了异步编程技术，但这也带来了一个问题：对于异步代码的执行顺序就带来了不确定性。
> 为了保证代码执行顺序按照我们的意愿去执行，可以使用异步代码A中嵌套异步代码B，异步代码B中嵌套异步代码C，以此类推的方式进行编程来控制异步代码的执行顺序。但这又带来了另一个问题：这样的代码可读性太差，且难以维护。

* **解决方案**

为了解决这个问题，在EcmaScript 6 中新增了一个API Promise

> Promise是一个构造函数，它可以通过它本身的机制和方法来控制异步操作的执行顺序，使异步编程更加规范和优雅
> 利用promise可以将异步操作以同步操作的流程表达出来，避免了层层嵌套的回调函数
> Promise是一个用来传递未来即将发生的事件（通常为异步操作）的状态的一个对象
> 所谓Promise，简单说就是一个容器，里面保存着某个未来才会结束的事件(通常是一个异步操作）的状态结果。从语法上说，Promise是一个对象，从它可以获取异步操作的消息。
> Promise接受一个executor，向这个executor传入了两个函数参数resolve、reject，当在回调函数中调用resolve（value）或reject（error）时，Promise的状态就会由pending（待定）对应变为fulfilled（满足的）或rejected（Promise的三种状态，Promise状态由pending变化之后，其状态就会凝固，不会再发生变化了，这时称作resolved（坚定地）），若状态变为fulfilled，那么将会执行该Promise对象then方法的第一个callback参数，并且前面的value（往往是异步代码的执行结果）还会作为参数传给callback；若为rejected，同理则执行then的第二个callback参数，或者执行catch的第一个callback参数。**这样就可以控制异步操作的流程（当执行executor中的异步操作时，调用resolve()，接下来便会执行then的第一个callback参数，这就实现了控制异步操作的先后执行顺序）**
> **这就是Promise的作用了，简单来讲，就是能把原来的回调写法分离出来，在异步操作执行完后，用链式调用的方式执行回调函数。**
> Promise也有一些缺点。首先，无法取消Promise，一旦新建它就会立即执行，无法中途取消。其次，如果不设置回调函数，Promise内部抛出的错误，不会反应到外部。第三，当处于pending状态时，无法得知目前进展到哪一个阶段（刚刚开始还是即将完成）。

* **使用场景**

  出现异步回调嵌套需求时，就需要使用Promise 

* **意义**

  既保留了`JavaScript`的异步执行高效的优势，又解决了回调地狱的问题。



### ES6异步编程解决方案之 async、await 关键字

`async`、`await`关键字是为了简化使用`Promise`异步编程。

* `async`用于定义异步函数

进一步说，`async`函数完全可以看作多个异步操作，包装成的一个 Promise 对象，而`await`命令就是内部`then`命令的语法糖。

`async`函数返回一个 Promise 对象。

`async`函数内部`return`语句返回的值，会成为`then`方法回调函数的参数。`async`函数内部抛出错误，会导致返回的 Promise 对象变为`reject`状态。抛出的错误对象会被`catch`方法回调函数接收到。

**注意：**`async`函数返回的 Promise 对象，**必须等到内部所有`await`命令后面的 Promise 对象执行完，才会发生状态改变**，除非遇到`return`语句或者抛出错误（任何一个`await`语句后面的 Promise 对象变为`reject`状态，那么整个`async`函数都会中断执行。）。也就是说，只有`async`函数内部的异步操作执行完，才会执行`then`方法指定的回调函数。

**所以async的使用要注意错误处理，可将await命令放入 try{}catch当中**

* `await` 操作符用于等待一个`Promise` 对象。它只能在异步函数 `async function` 中使用。如果不是则会报错。（`await`其实是`Promise`的`then`方法的语法糖，await表达式的返回值相当于then方法接收的第一个参数，await后面剩余的代码被放到then回调函数体内）

语法：

```javascript
[return_value] = await expression;    
```

expression为 一个 `Promise` 对象或者任何要等待的值。

如果等待的不是 `Promise `对象，则返回该值本身。（如果该值不是一个 `Promise`，`await` 会把该值转换为已正常处理的`Promise`，然后等待其处理结果。和返回值本身是一样的效果）

**执行逻辑：**

await 表达式会暂停当前 `async function`的执行，等待 Promise 处理完成。若 Promise 正常处理(fulfilled)，其回调的resolve函数参数作为 await 表达式的值，继续执行 `async function`。若 Promise 处理异常(rejected)，await 表达式会把 Promise 的异常原因抛出。另外，如果 await 操作符后的表达式的值不是一个 Promise，则返回该值本身。

**注意：**多个`await`命令后面的异步操作，如果不存在继发关系，最好让它们同时触发。写法如下。

```javascript
let [foo, bar] = await Promise.all([getFoo(), getBar()]);
```



## Module

历史上，JavaScript 一直没有模块（module）体系，无法将一个大程序拆分成互相依赖的小文件，再用简单的方法拼装起来。其他语言都有这项功能，比如 Ruby 的`require`、Python 的`import`，甚至就连 CSS 都有`@import`，但是 JavaScript 任何这方面的支持都没有，这对开发大型的、复杂的项目形成了巨大障碍。

在 ES6 之前，社区制定了一些模块加载方案，最主要的有 CommonJS 和 AMD 两种，前者用于服务器，后者用于浏览器。ES6 在语言标准的层面上，实现了模块功能，而且实现得相当简单，完全可以取代 CommonJS 和 AMD 规范，成为浏览器和服务器通用的模块解决方案。

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

    因为 CommonJS 加载的是一个对象（即`module.exports`属性），该对象只有在脚本运行完才会生成 。 而 ES6 模块不是对象，它的对外接口只是一种静态定义，在代码静态解析阶段就会生成。 

  - CommonJS 模块的`require()`是同步加载模块，ES6 模块的`import`命令是异步加载，有一个独立的模块依赖的解析阶段。
  

## this

`this`是 JavaScript 语言的一个关键字。

它是函数**运行时**，在函数体内部自动生成的一个对象，一般在函数体内部使用。

> ```javascript
> function test() {
> 　this.x = 1;
> }
> ```

上面代码中，函数`test`运行时，内部会自动有一个`this`对象可以使用。

那么，`this`的值是什么呢？

函数的不同使用场合，`this`有不同的值。总的来说，`this`就是函数运行时所在的环境对象。下面分四种情况，详细讨论`this`的用法。

+ 情况一：纯粹的函数调用

这是函数的最通常用法，属于全局性调用，因此`this`就代表全局对象。请看下面这段代码，它的运行结果是1。

> ```javascript
> var x = 1;
> function test() {
>    console.log(this.x);
> }
> test();  // 1
> ```

+ 情况二：作为对象方法的调用

函数还可以作为某个对象的方法调用，这时`this`就指这个上级对象。

> ```javascript
> function test() {
>   console.log(this.x);
> }
> 
> var obj = {};
> obj.x = 1;
> obj.m = test;
> 
> obj.m(); // 1
> ```

+ 情况三 作为构造函数调用

所谓构造函数，就是通过这个函数，可以生成一个新对象。这时，`this`就指这个新对象。

> ```javascript
> function test() {
> 　this.x = 1;
> }
> 
> var obj = new test();
> obj.x // 1
> ```

运行结果为1。为了表明这时this不是全局对象，我们对代码做一些改变：

> ```javascript
> var x = 2;
> function test() {
>   this.x = 1;
> }
> 
> var obj = new test();
> x  // 2
> ```

运行结果为2，表明全局变量`x`的值根本没变。

+ 情况四 apply 调用

`apply()`是函数的一个方法，作用是改变函数的调用对象。它的第一个参数就表示改变后的调用这个函数的对象。因此，这时`this`指的就是这第一个参数。

> ```javascript
> var x = 0;
> function test() {
> 　console.log(this.x);
> }
> 
> var obj = {};
> obj.x = 1;
> obj.m = test;
> obj.m.apply() // 0
> ```

`apply()`的参数为空时，默认调用全局对象。因此，这时的运行结果为`0`，证明`this`指的是全局对象。

如果把最后一行代码修改为

> ```javascript
> obj.m.apply(obj); //1
> ```

运行结果就变成了`1`，证明了这时`this`代表的是对象`obj`。

总结一下，`this`是动态变化的，是在运行时才能确定的。



## 闭包

> 在JavaScript中，函数总是可以访问创建它的上下文环境，这就叫做闭包。

JavaScript权威指南解释：**函数的执行依赖于变量作用域，这个作用域是函数定义时决定的，而不是函数调用时决定的。**

简单讲，**闭包就是有权访问另一个函数作用域中的变量的函数。它定义在函数内部，当外部函数调用结束之后，其变量对象本应该被销毁，但闭包的存在使得我们仍然可以访问外部函数的变量对象。**

但这也会造成比较大的性能开销，因此，在闭包使用完成后应该将其销毁。对闭包不再引用就会自动将其销毁。

（注：在JavaScript中，如果一个对象不再被引用，那么这个对象就会被垃圾回收机制回收）

> 注：函数对象可以通过作用域链相互关联起来，函数体内部使用到的变量都可以保存在外部函数作用域内，这种特性叫闭包； **函数执行时所依赖的作用域链的确定，和在哪运行没有关系，只和在哪儿定义有关系；**

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

JavaScript高级程序设计解释：当在函数内部定义了其它函数时，就创建了闭包；闭包有权访问其外面函数内部的所有变量。

**通常，函数的作用域及其所有的变量都会在函数执行结束后被销毁。但是，当这个函数内部还有函数时，也就是创建了闭包后，使得它不会被销毁，会一直保存到闭包不存在为止。**

闭包可以理解为函数运行时的一个特性，即函数运行所依赖的变量作用域是在函数定义时就已经确定，而不是在运行时确定。闭包不是一种语法，它的形成和作用域链有关系。

闭包的形成和JavaScript的函数作用域以及静态作用域链有关，当在函数A内部定义函数B时，在函数B中访问变量时，会先在函数B的作用域内查找变量，如果没有，则在函数A的作用域中查找该变量的值，而函数作用域对外是封闭的，并且函数访问变量所依赖的作用域链是在函数定义时就确定的。这样，函数B在运行时所调用的变量的值也就确定了，因为这些变量保存在函数作用域内，对外封闭，所以我们称函数B为闭包。

**闭包的用处**

闭包可以用在许多地方。它的最大用处有两个，一个是可以读取函数内部的变量，另一个就是让这些变量的值始终保持在内存中。



### 函数

>函数就是一个方法或者一个功能体，函数就是把实现某个功能的代码放到一起进行封装，以后需要这个功能时，只需要执行函数即可。
>
>这种思想即是"封装"，封装的目的是减小重复代码，提供代码复用率（低耦合高内聚）
>
>此外：当函数和`new`搭配使用时，可以用来创建对象，用来创建对象的函数又称为构造函数，JS中的对象都是通过构造函数生成的。

+ 编写pure function的准则

  函数的功能是提供input到output的映射，除此之外，不应该再有其他对外部程序状态的影响（如函数在执行过后，改变了函数外的变量的值）；**对于相同的输入，永远输出相同的结果**；函数内部的任何计算都不应该影响到外部作用域的变量；函数计算所需要的外部值只能通过形参获取，并且不能改变向形参传递值的实参的值。

  一个pure function的输出仅仅取决于它的输入。

+ 函数种类

  + 高阶函数

    以函数作为参数或返回值的函数称为高阶函数

  + first class functions

    在计算机科学当中，将能够作为函数的参数和返回值，以及赋值给变量的一类值称为First Class；

    可以作为函数的参数，但不能从函数返回，也不能赋给变量的一类值称为Second Class；

    不能作为函数参数和返回值，也不能赋给变量的一类值称为Third Class。

    将满足First Class定义条件的函数称为First Class Functions（即函数可以作为函数的参数和返回值以及赋值给变量），在JavaScript中，所有函数都属于这一类型。

  + lambda

    作为函数参数和返回值的函数称为lambda，即匿名函数。

+ 创建函数

  + 形参：入口

  + 返回值：出口

    函数体内创建的变量从函数体外无法获取，如果想要获取内部的信息，需要通过return返回值机制，将相关信息返回。

    注意：**return result返回的是result变量存储的值，而不是变量本身（倘若是变量本身，则就可以改变函数体内创建的变量，这与函数作用域的机制相违背），且运行完return语句后，将结束函数的执行**

    没有return语句或者return为空，函数默认返回值为undefined

+ 传递参数

  在JavaScript中所有参数的传递是按值传递。

  对于基本类型的变量：传递的变量的值（值的拷贝）

  对于引用类型的变量：传递的也是变量的值，只不过该值是引用类型值在堆内存中的地址

+ 执行函数

  + 实参：传入函数的东西

    执行函数时，没有接收到值的形参默认为undefined

+ arguments

  函数内置的实参集合，用来存储所有函数执行时传入函数的实参

  不论是否传递形参，arguments都存在

  不论是否传递实参，arguments也都存在

  ```javascript
  function sum () {
  	let total = null
  	for(let i = 0; i < arguments.lenth; i++){
  		let item = arguments[i]
  		if(isNaN(item)){
              continue
          }
  		total += item
      }
  	return total
  }
  ```

+ 函数底层运行机制

  ![](D:\GitProjects\notes\前端\JS笔记图\JS中的函数运行机制（简化版）.png)



# DOM

> DOM is short for Document Object Model. It is the object presentation of the HTML document and the interface of HTML elements to the outside world like JavaScript.
> The root of the tree is the "[Document](http://www.w3.org/TR/1998/REC-DOM-Level-1-19981001/level-one-core.html#i-Document)" object.

### JS中获取DOM元素的几种方式

- document.getElementById() 指定在文档中，基于元素的ID或者这个元素对象
- [context].getElementsByTagName() 在指定上下文中，通过标签名获取一组元素集合
- [context].getElementsByClassName() 在指定上下文中，通过样式类名获取一组元素集合（不兼容IE6~8）
- document.getElementsByName() 在整个文档中，通过标签的name属性值获取一组元素集合（在IE中只有表单元素的name才能识别，所以一般只应用于表单处理）
- document.head/document.body/document.documentElement 获取页面中的HEAD/BODY/HTML三个元素
- [context].querySelector([selector])在指定上下文中，通过选择器获取到指定的元素对象
- [context].querySelectorAll([selector]) 在指定上下文中，通过选择器获取到指定的元素集合

> 以上方法可以帮我们获取到页面中的任意的元素，但只能通过在某个范围设置筛选条件的形式，这就限制了我们获取元素的途径，不够灵活，因此，还可以根据各节点之间的层级关系来获取节点对象，DOM中各个节点对象都具有描述节点间层级关系的属性，通过它们可以获取节点对象。

### JS中的节点和描述节点之间的关系属性

> 节点：Node（页面中的所有东西都是节点）
>
> 节点都是单个对象，有些时候需要一种数据结构来容纳多个节点，DOM提供了两种数据结构，用来容纳节点集合。
>
> 节点集合（可容纳各种类型的节点）：NodeList（getElementsByName/querySelectorAll获取的都是节点集合）
>
> 元素节点集合（只能包含元素类型的节点）：
>
> HTMLCollection（getElementsByTagName/getElementsByClassName等获取的都是元素节点的集合）

- 元素节点（元素标签）
  + nodeType：1
  + nodeName：大写的标签名
  + nodeValue：null
- 文本节点
  + nodeType：3
  + nodeName：‘#text’
  + nodeValue：文本内容
- 注释节点
  + nodeType：8
  + nodeName：‘#comment’
  + nodeValue：注释内容
- 文档节点（代表整个文档树，是文档树的根节点）
  + nodeType：9
  + nodeName：‘#document’
  + nodeValue：null
- 文档类型（DocumentType）节点和顶层元素节点HTML为文档（Document）根节点的两个子节点

描述这些节点之间的关系的属性

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

### JS中动态增删改元素

常用方法

`document.createElement`创建元素对象

`document.createTextNode`创建文本对象

`appendChild`把元素添加到容器的末尾

> 容器.appendChild([节点对象])

`insertBefore`把元素添加到指定容器中指定元素的前面

> 容器.insertBefore([新增元素],[指定元素])  // 指定元素要是容器的子元素

`cloneNode(true/false)` 克隆元素或节点，true表示深克隆，里面的节点也克隆，false表示浅克隆，不包含里面的节点

`removeChild`删除元素

> 容器.removeChild(元素)

给元素设置自定义属性的方法（标签属性）

`[element].setAttribute`

`[element].getAttribute`

`[element].removeAttribute`

给元素对象设置自定义属性

[element].xxx = xxx

### 获取元素样式和操作样式

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
```

```javascript
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
```

```javascript
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

# BOM

