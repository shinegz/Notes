# TypeScript

> TypeScript 是添加了`静态类型系统`的 JavaScript，适用于`任何规模`的项目。



## 简介

### 设计理念

在完整保留 JavaScript 运行时行为的基础上，通过引入静态类型系统来提高代码的可维护性，减少可能出现的 bug。



### 特性

**类型系统**

+ 静态类型

  TypeScript 在运行前需要先编译为 JavaScript，在编译阶段就会进行类型检查。

+ 弱类型

  和 JavaScript 一样，TypeScript 允许隐式类型转换



**适用于任何规模**





**与标准同步发展**

当 ECMAScript 中新增的语法进入到 Stage 3 阶段后，TypeScript 就会实现它。



### 发展历程

- 2012-10：微软发布了 TypeScript 第一个版本（0.8），此前已经在微软内部开发了两年。
- 2014-04：TypeScript 发布了 1.0 版本。
- 2014-10：Angular 发布了 2.0 版本，它是一个基于 TypeScript 开发的前端框架。
- 2015-01：ts-loader 发布，webpack 可以编译 TypeScript 文件了。
- 2015-04：微软发布了 Visual Studio Code，它内置了对 TypeScript 语言的支持，它自身也是用 TypeScript 开发的。
- 2016-05：`@types/react` 发布，TypeScript 可以开发 React 应用了。
- 2016-05：`@types/node` 发布，TypeScript 可以开发 Node.js 应用了。
- 2016-09：TypeScript 发布了 2.0 版本。
- 2018-06：TypeScript 发布了 3.0 版本。
- 2019-02：TypeScript 宣布由官方团队来维护 typescript-eslint，以支持在 TypeScript 文件中运行 ESLint 检查。
- 2020-05：Deno 发布了 1.0 版本，它是一个 JavaScript 和 TypeScript 运行时。
- 2020-08：TypeScript 发布了 4.0 版本。
- 2020-09：Vue 发布了 3.0 版本，官方支持 TypeScript。



## 类型

### 基础类型

TypeScript 支持 JavaScript 中所有的数据类型，此外还提供了更多实用的数据类型。

**布尔值**

布尔数据类型中的值只有两个：true 和 false。

```typescript
let isDone: boolean = false;
```



**数字**

和 JavaScript 一样，TypeScript 里的所有数字都是浮点数。这些浮点数的类型为 number。除了支持十进制和十六进制字面量，TypeScript还支持 ECMAScript 2015 中引入的二进制和八进制字面量。

```ts
let decLiteral: number = 6;
let hexLiteral: number = 0xf00d;
let binaryLiteral: number = 0b1010;
let octalLiteral: number = 0o744;
```



**字符串**

和 JavaScript 一样，可以使用双引号（ `"`）或单引号（`'`）表示字符串。

```ts
let name: string = "bob";
name = "smith";
```

通过使用*模版字符串*，可以定义多行文本和内嵌表达式。 这种字符串是被反引号包围（ ` `` `），并且以`${ expr }`这种形式嵌入表达式

```ts
let sentence: string = `Hello, my name is ${ name }.

I'll be ${ age + 1 } years old next month.`;
```



**Null 和 Undefined**

在 TypeScript 中，可以使用 `null` 和 `undefined` 来定义这两个原始数据类型：

```ts
let u: undefined = undefined;
let n: null = null;
```

与 `void` 的区别是，`undefined` 和 `null` 是所有类型的子类型。但当指定了`--strictNullChecks`标记时，`null`和`undefined`只能赋值给`void`和它们各自。



**Symbol**

`symbol` 类型表示的是哪些唯一值的类型。



**Object**

`object`表示非原始类型，也就是除`number`，`string`，`boolean`，`symbol`，`null`或`undefined`之外的类型。

```ts
declare function create(o: object | null): void;

create({ prop: 0 }); // OK
create(null); // OK

create(42); // Error
create("string"); // Error
create(false); // Error
create(undefined); // Error
```



**Void**

JavaScript 没有空值（Void）的概念，在 TypeScript 中，可以用 `void` 表示没有任何返回值的函数：

```ts
function alertName(): void {
    alert('My name is Tom');
}
```

声明一个 `void` 类型的变量没有什么用，因为你只能将它赋值为 `undefined` 和 `null`（只在 --strictNullChecks 未指定时）：

```ts
let unusable: void = undefined;
```



**Never**

`never`类型表示的是那些永不存在的值的类型。

`never`类型是任何类型的子类型，也可以赋值给任何类型；然而，*没有*类型是`never`的子类型或可以赋值给`never`类型（除了`never`本身之外）。 即使 `any`也不可以赋值给`never`。

下面是一些返回`never`类型的函数：

```ts
// 返回never的函数必须存在无法达到的终点
function error(message: string): never {
    throw new Error(message);
}

// 推断的返回值类型为never
function fail() {
    return error("Something failed");
}

// 返回never的函数必须存在无法达到的终点
function infiniteLoop(): never {
    while (true) {
    }
}
```



**枚举**

`enum`类型是对 JavaScript 标准数据类型的一个补充。枚举（Enum）类型用于取值被限定在一定范围内的场景，使用枚举类型可以为一组数值赋予友好的名字。

枚举成员会被赋值为从 `0` 开始递增的数字，同时也会对枚举值到枚举名进行反向映射：

```ts
enum Days {Sun, Mon, Tue, Wed, Thu, Fri, Sat};

console.log(Days["Sun"] === 0); // true
console.log(Days["Mon"] === 1); // true
console.log(Days["Tue"] === 2); // true
console.log(Days["Sat"] === 6); // true

console.log(Days[0] === "Sun"); // true
console.log(Days[1] === "Mon"); // true
console.log(Days[2] === "Tue"); // true
console.log(Days[6] === "Sat"); // true
```

我们也可以给枚举项手动赋值：

```ts
enum Days {Sun = 7, Mon = 1, Tue, Wed, Thu, Fri, Sat};

console.log(Days["Sun"] === 7); // true
console.log(Days["Mon"] === 1); // true
console.log(Days["Tue"] === 2); // true
console.log(Days["Sat"] === 6); // true
```

未手动赋值的枚举项会接着上一个枚举项递增。



**Any**

任意值（Any）用来表示允许赋值为任意类型。

在任意值上访问任何属性和调用任何方法都是允许的，并且对任意值的任何操作，返回的内容的类型都是任意类型。

**变量如果在声明的时候，未指定其类型，那么它会被识别为任意值类型**



**数组**

TypeScript 像 JavaScript 一样可以操作数组元素。 有两种方式可以定义数组。 第一种，可以在元素类型后面接上 `[]`，表示由此类型元素组成的一个数组：

```ts
let list: number[] = [1, 2, 3];
```

第二种方式是使用数组泛型，`Array<元素类型>`：

```ts
let list: Array<number> = [1, 2, 3];
```



**元组 Tuple**

数组合并了相同类型的对象，而元组（Tuple）合并了不同类型的对象。元组类型允许表示一个已知元素数量和类型的数组，各元素的类型不必相同。

```ts
// Declare a tuple type
let x: [string, number];
// Initialize it
x = ['hello', 10]; // OK
// Initialize it incorrectly
x = [10, 'hello']; // Error
```

当访问一个已知索引的元素，会得到正确的类型：

```ts
console.log(x[0].substr(1)); // OK
console.log(x[1].substr(1)); // Error, 'number' does not have 'substr'
```

当访问一个越界的元素，会使用联合类型替代：

```ts
x[3] = 'world'; // OK, 字符串可以赋值给(string | number)类型

console.log(x[5].toString()); // OK, 'string' 和 'number' 都有 toString

x[6] = true; // Error, 布尔不是(string | number)类型
```



### 联合类型

联合类型表示取值可以为多种类型中的一种。

```ts
let myFavoriteNumber: string | number;
myFavoriteNumber = true;

// index.ts(2,1): error TS2322: Type 'boolean' is not assignable to type 'string | number'.
//   Type 'boolean' is not assignable to type 'number'.
```

联合类型使用 `|` 分隔每个类型。

当 TypeScript 不确定一个联合类型的变量到底是哪个类型的时候，我们**只能访问此联合类型的所有类型里共有的属性或方法**：

```ts
function getLength(something: string | number): number {
    return something.length;
}

// index.ts(2,22): error TS2339: Property 'length' does not exist on type 'string | number'.
//   Property 'length' does not exist on type 'number'.
```

联合类型的变量在被赋值的时候，会根据类型推论的规则推断出一个类型：

```ts
let myFavoriteNumber: string | number;
myFavoriteNumber = 'seven';
console.log(myFavoriteNumber.length); // 5
myFavoriteNumber = 7;
console.log(myFavoriteNumber.length); // 编译时报错

// index.ts(5,30): error TS2339: Property 'length' does not exist on type 'number'.
```



### 类型推论

TypeScript 里，在没有明确指出类型的地方，会根据类型推断规则确定出最合适的类型。

#### 最佳通用类型

当需要从几个表达式中推断类型的时候，会使用这些表达式的类型来推断出一个合适的通用类型。

计算通用类型算法会考虑所有候选类型，并给出一个兼容所有候选类型的类型，如果没有找到，则类型推断的结果为联合类型。

#### 上下文类型

当表达式的类型与所处的位置相关时，就会根据上下文来推断出类型，这种表达式被称为上下文类型表达式。

注：

+ 当上下文类型表达式包含了明确的类型信息，上下文的类型就会被忽略。
+ 上下文的类型也会作为最佳通用类型的候选类型。



### 泛型

泛型是强类型程序设计语言的一种风格或范式。它指的是我们在程序定义时，不预先确定具体的类型，在程序执行时再指定类型。

泛型使得程序能够适用于多种数据类型，为程序提供了更好地灵活性。

```ts
function identity<T>(arg: T): T {
    return arg;
}
```

我们给 identity 添加了类型（泛型）变量`T`（用于表示类型而不是值的变量）。 `T` 帮助我们捕获用户传入的类型（比如：`number`），之后我们就可以使用这个类型。 之后我们再次使用了 `T` 当做返回值类型。现在我们可以知道参数类型与返回值类型是相同的了。

我们把这个版本的`identity`函数叫做泛型函数，因为它可以适用于多个类型。

#### 泛型接口

使用接口的方式来定义一个函数需要符合的形状：

```ts
interface SearchFunc {
  (source: string, subString: string): boolean;
}

let mySearch: SearchFunc;
mySearch = function(source: string, subString: string) {
    return source.search(subString) !== -1;
}
```

使用含有泛型的接口来定义函数的形状：

```ts
interface CreateArrayFunc<T> {
    (length: number, value: T): Array<T>;
}

let createArray: CreateArrayFunc<any>;
createArray = function<T>(length: number, value: T): Array<T> {
    let result: T[] = [];
    for (let i = 0; i < length; i++) {
        result[i] = value;
    }
    return result;
}

createArray(3, 'x'); // ['x', 'x', 'x']
```



#### 泛型类

与泛型接口类似，泛型也可以用于类的类型定义中：

```ts
class GenericNumber<T> {
    zeroValue: T;
    add: (x: T, y: T) => T;
}

let myGenericNumber = new GenericNumber<number>();
myGenericNumber.zeroValue = 0;
myGenericNumber.add = function(x, y) { return x + y; };
```

注：泛型类指的是实例部分的类型，所以类的静态属性不能使用这个泛型类型。



#### 泛型约束

泛型约束指的是借助接口来限制传入的类型。

创建一个包含 `.length`属性的接口，使用这个接口和`extends`关键字来实现约束：

```ts
interface Lengthwise {
    length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
    console.log(arg.length);  // Now we know it has a .length property, so no more error
    return arg;
}
```

现在这个泛型函数被定义了约束，因此它不再是适用于任意类型：

```ts
loggingIdentity(3);  // Error, number doesn't have a .length property
```

我们需要传入符合约束类型的值，必须包含必须的属性：

```ts
loggingIdentity({length: 10, value: 3});
```



## 函数

### 函数定义

在 JavaScript 中，有两种常见的定义函数的方式——函数声明（Function Declaration）和函数表达式（Function Expression），在 TypeScript 中对应如下：

```js
// 函数声明（Function Declaration）
function sum(x: number, y: number): number {
    return x + y;
}

// 函数表达式（Function Expression）
let mySum: (x: number, y: number) => number = function (x: number, y: number): number {
    return x + y;
};
```



### 函数参数

在 TypeScript 中，传递给一个函数的参数个数必须与函数期望的参数个数一致。

#### 可选参数

JavaScript 里，每个参数都是可选的，可传可不传。 没传参的时候，它的值就是undefined。 在 TypeScript 中，我们可以在参数名旁使用 `?`实现可选参数的功能。不过需要注意的是，可选参数必须跟在必须参数后面。

```typescript
function buildName(firstName: string, lastName?: string) {
    if (lastName)
        return firstName + " " + lastName;
    else
        return firstName;
}
```



#### 参数默认值

在 TypeScript 里，我们也可以为参数提供一个默认值当用户没有传递这个参数或传递的值是`undefined`时。 它们叫做有默认初始化值的参数。

注意：

+ 在所有必须参数后面的带默认初始化的参数都是可选的，与可选参数一样，在调用函数的时候可以省略。

+ 与普通可选参数不同的是，带默认值的参数不需要放在必须参数的后面。 如果带默认值的参数出现在必须参数前面，用户必须明确的传入 `undefined`值来获得默认值。

```typescript
function buildName(firstName: string, lastName = "Smith") {
    return firstName + " " + lastName;
}
```



#### 剩余参数

必要参数，默认参数和可选参数有个共同点：它们表示某一个参数。当需要操作多个参数或不知道会有多少参数传递进来时，便需要使用剩余参数。

在 TypeScript 里，可以通过如下方式将所有参数收集到一个变量里：

```typescript
function buildName(firstName: string, ...restOfName: string[]) {
  return firstName + " " + restOfName.join(" ");
}
```

剩余参数会被当做个数不限的可选参数。 可以一个都没有，同样也可以有任意个。 编译器创建参数数组，名字是你在省略号（ `...`）后面给定的名字，你可以在函数体内使用这个数组。



### 重载

> 函数的重载指的是，同一个函数在同一声明域内进行了多次函数类型定义，但参数表各不相同。

当调用重载的函数时，编译器会查找重载列表，找到那个能够匹配传入参数的重载定义，然后根据该定义进行类型检查。

应用场景：当一个函数接收不同类型或数量的参数时，需要做出不同的处理。

比如，我们需要实现一个函数 `reverse`，输入数字 `123` 的时候，输出反转的数字 `321`，输入字符串 `'hello'` 的时候，输出反转的字符串 `'olleh'`。

利用联合类型，我们可以这么实现：

```ts
function reverse(x: number | string): number | string | void {
    if (typeof x === 'number') {
        return Number(x.toString().split('').reverse().join(''));
    } else if (typeof x === 'string') {
        return x.split('').reverse().join('');
    }
}
```

**然而这样有一个缺点，就是不能够精确的表达，输入为数字的时候，输出也应该为数字，输入为字符串的时候，输出也应该为字符串。**

这时，我们可以使用重载定义多个 `reverse` 的函数类型：

```ts
function reverse(x: number): number;
function reverse(x: string): string;
function reverse(x: number | string): number | string | void {
    if (typeof x === 'number') {
        return Number(x.toString().split('').reverse().join(''));
    } else if (typeof x === 'string') {
        return x.split('').reverse().join('');
    }
}
```

上例中，我们重复定义了多次函数 `reverse`，前几次都是函数定义，最后一次是函数实现。



## 类

传统的 JavaScript 使用函数和基于原型的继承来实现面向对象。从 ES6 开始，JavaScript 能够使用基于类的面向对象。TypeScript 除了实现了所有 ES6 中的类的功能以外，还添加了一些新的用法。

类的成员可以分为两部分：实例部分和静态部分。

### 实例部分

类的实例成员指的是存在于类的实例上的属性，仅当类被实例化的时候才会被初始化，通过实例化对象或在实例成员中通过 `this.` 的方式访问。

#### 访问限定属性

+ public

  在 TypeScript 中，类的成员都默认为 `public`，访问不受限定。

+ private

  经`private`关键字修饰的成员在声明它的类的外部不可访问。

+ protected

  经`protected`关键字修饰的成员在声明它的类的外部不可访问，但在其派生类中可访问。

+ readonly

  经`readonly`关键字修饰的成员为只读的。 只读属性必须在声明时或构造函数里被初始化。

注：

> TypeScript使用的是结构性类型系统。 当我们比较两种不同的类型时，并不在乎它们从何处而来，如果所有成员的类型都是兼容的，我们就认为它们的类型是兼容的。
>
> 然而，当我们比较带有 `private`或 `protected`成员的类型的时候，情况就不同了。 如果其中一个类型里包含一个 `private`成员，那么只有当另外一个类型中也存在这样一个 `private`成员， 并且它们都是来自同一处声明时，我们才认为这两个类型是兼容的。 对于 `protected`成员也使用这个规则。

#### 参数属性

通过给构造函数参数前面添加一个访问限定符来声明并初始化的属性。

```typescript
class Example {
    // readOnly、public、private、protected
    constructor(readonly name: string) {
    }
}
```

#### 访问器属性

TypeScript 支持通过 getters/setters 来截取对对象成员的访问。

```typescript
let passcode = "secret passcode";

class Employee {
    private _fullName: string;

    get fullName(): string {
        return this._fullName;
    }

    set fullName(newName: string) {
        if (passcode && passcode == "secret passcode") {
            this._fullName = newName;
        }
        else {
            console.log("Error: Unauthorized update of employee!");
        }
    }
}

let employee = new Employee();
employee.fullName = "Bob Smith";
if (employee.fullName) {
    alert(employee.fullName);
}
```



### 静态部分

类的静态部分指的是存在于**类本身上面**而不是类的实例上的部分。

#### 构造函数

通过 `new` 生成新实例的时候，会自动调用构造函数。

```typescript
class Animal {
    public name;
    constructor(name) {
        this.name = name;
    }
    sayHi() {
        return `My name is ${this.name}`;
    }
}

let a = new Animal('Jack');
console.log(a.sayHi()); // My name is Jack
```

注：当构造函数被标记成 protected 时，意味着这个类不能在包含它的类外被实例化，但是能被继承（protected 成员在派生类中可以访问，但在类外不可访问）。

#### 静态属性

使用 static 定义的属性为静态属性，它们通过类来直接访问，而不是实例化对象。



### 继承

在 TypeScript 中，允许使用继承来扩展现有的类。使用 `extends` 关键字实现继承，子类中使用 `super` 关键字来调用父类的构造函数和方法。

```typescript
class Animal {
    public name;
    constructor(name) {
        this.name = name;
    }
    sayHi() {
        return `My name is ${this.name}`;
    }
}

class Cat extends Animal {
  constructor(name) {
    super(name); // 调用父类的 constructor(name)
    console.log(this.name);
  }
  sayHi() {
    return 'Meow, ' + super.sayHi(); // 调用父类的 sayHi()
  }
}

let c = new Cat('Tom'); // Tom
console.log(c.sayHi()); // Meow, My name is Tom
```

在这里，Cat 是一个派生类，它通过 `extends` 关键字派生自 Animal 基类。派生类通常被称作子类，基类通常被称为超类。

注意：在派生类的构造函数里访问 `this` 的属性之前，我们*一定*要调用 `super()`，它会执行基类的构造函数，否则会报错。



### 抽象类

抽象类作为其它派生类的基类使用。不同于接口，抽象类可以包含成员的实现细节。 `abstract` 用于定义抽象类和其中的抽象方法。

抽象类不允许被实例化，并且抽象类中的抽象方法必须被子类实现

```typescript
abstract class Animal {
  public name;
  public constructor(name) {
    this.name = name;
  }
  public abstract sayHi();  // 抽象方法
}

class Cat extends Animal {
  public eat() {
    console.log(`${this.name} is eating.`);
  }
}

let a = new Animal('Jack');

// index.ts(9,11): error TS2511: Cannot create an instance of the abstract class 'Animal'.

let cat = new Cat('Tom');

// index.ts(9,7): error TS2515: Non-abstract class 'Cat' does not implement inherited abstract member 'sayHi' from class 'Animal'.
```





## 接口

> TypeScript 的核心原则之一是对值所具有的`结构（外形）`进行类型检查。接口的作用就是为这些类型命名和定义契约（值的结构检查规则）。

在面向对象语言中，接口（Interfaces）是一个很重要的概念，它是对行为的抽象，而具体如何行动需要由类（classes）去实现（implement）。

TypeScript 中的接口是一个非常灵活的概念，除了可用于对类的一部分行为进行抽象以外，也常用于对对象的形状（Shape）进行描述。

### 对象接口

用于描述对象的外形。

**可选属性**

> 接口里非必需的属性。有些属性在一些条件下存在，一些条件下不存在，这样的属性便可用可选属性来定义。

语法：

```typescript
interface SquareConfig {
  color?: string;
  width?: number;
}
```



**只读属性**

> 只能在对象刚刚创建时修改其值的属性。

语法：

```typescript
interface Point {
    readonly x: number;
    readonly y: number;
}
```



**任意属性**

> 任意属性使一个接口可以拥有任意的属性。

语法：

```typescript
interface Person {
    [propName: string]: string;
}
```

一旦定义了任意属性，那么确定属性和可选属性的类型都必须是它的类型的子集。



### 函数接口

接口能够描述 JavaScript 中对象拥有的各种各样的外形。 除了描述带有属性的普通对象外，接口也可以描述函数类型。

为了使用接口表示函数类型，我们需要给接口定义一个调用签名。 它就像是一个只有参数列表和返回值类型的函数定义。参数列表里的每个参数都需要名字和类型。

```ts
interface SearchFunc {
  (source: string, subString: string): boolean;
}
```

这样定义后，我们可以像使用其它接口一样使用这个函数类型的接口。对于函数类型的类型检查来说，函数的参数名不需要与接口里定义的名字相匹配，但要求对应位置上的参数类型是兼容的。



### 类接口

类接口可以用来明确的强制一个类去符合某种契约。接口描述了**类的实例部分**，而不是实例和静态两部分，也就是说，当一个类实现了一个接口时，只对其实例部分进行类型检查。

```typescript
interface ClockInterface {    
    currentTime: Date;    
    setTime(d: Date); 
}

class Clock implements ClockInterface {
    currentTime: Date;    
    setTime(d: Date) {        
        this.currentTime = d;   
    }    
    constructor(h: number, m: number) { } 
}
```



### 继承接口

和类一样，接口也可以相互继承。这使得我们可以从一个接口里复制成员到另一个接口里，从而可以灵活地将接口分割到可重用的模块里。

```typescript
interface Shape {
    color: string;
}

interface PenStroke {
    penWidth: number;
}

interface Square extends Shape, PenStroke {
    sideLength: number;
}

let square = <Square>{};
square.color = "blue";
square.sideLength = 10;
square.penWidth = 5.0;
```



### 接口继承类

当接口继承了一个类类型时，它会继承类的成员但不包括其实现。 就好像接口声明了所有类中存在的成员，但并没有提供具体实现一样。 接口同样会继承到类的 private 和 protected 成员。 这意味着当你创建了一个接口继承了一个拥有私有或受保护的成员的类时，这个接口类型只能被这个类或其子类所实现（implement）。

```typescript
class Control {
    private state: any;
}

interface SelectableControl extends Control {
    select(): void;
}

class Button extends Control implements SelectableControl {
    select() { }
}

// 错误：“Image”类型缺少“state”属性。
class Image implements SelectableControl {
    select() { }
}
```

在上面的例子里，`SelectableControl`包含了`Control`的所有成员，包括私有成员`state`。 因为 `state`是私有成员，所以只能够是`Control`的子类们才能实现`SelectableControl`接口。 因为只有 `Control`的子类才能够拥有一个声明于`Control`的私有成员`state`，这对私有成员的兼容性是必需的。



## 模块与命名空间

### 模块

> TypeScript 与 ECMAScript 2015一样，任何包含顶级`import`或者`export`的文件都被当成一个模块。相反地，如果一个文件不带有顶级的`import`或者`export`声明，那么它的内容被视为全局可见的（因此对模块也是可见的）。

模块在其自身作用域中执行，而非全局作用域；这意味着定义在一个模块里的变量，函数，类等等一切在模块外是不可见的，除非明确的使用 export 形式之一导出；相反，如果想使用其他模块导出的变量，函数，类等的时候，必须使用 import 形式之一导入它们。

#### 导出

**导出声明**

任何声明（比如变量，函数，类，类型别名或接口）都能够通过添加`export` 关键字来导出。

```typescript
export interface StringValidator {
    isAcceptable(s: string): boolean;
}

export const numberRegexp = /^[0-9]+$/;

export class ZipCodeValidator implements StringValidator {
    isAcceptable(s: string) {
        return s.length === 5 && numberRegexp.test(s);
    }
}
```



**导出语句**

当需要对导出的部分重命名时，就要用到导出语句。

```typescript
class ZipCodeValidator implements StringValidator {
    isAcceptable(s: string) {
        return s.length === 5 && numberRegexp.test(s);
    }
}
export { ZipCodeValidator };
export { ZipCodeValidator as mainValidator };
```



**重新导出**

重新导出功能并不会在当前模块导入那个模块或定义一个新的局部变量。

```typescript
// 导出原先的验证器但做了重命名
export {ZipCodeValidator as RegExpBasedZipCodeValidator} from "./ZipCodeValidator";
```

或者一个模块可以包裹多个模块，并把他们导出的内容联合在一起通过语法：`export * from "module"`。

```ts
export * from "./StringValidator"; // exports interface StringValidator
export * from "./LettersOnlyValidator"; // exports class LettersOnlyValidator
export * from "./ZipCodeValidator";  // exports class ZipCodeValidator
```



**默认导出**

> 每个模块都可以也只能有一个 default 导出。

对于默认导出的内容，需要使用一种特殊的导入形式来导入。

JQuery.d.ts

```ts
declare let $: JQuery;
export default $;
```

App.ts

```ts
import $ from "JQuery";

$("button.continue").html( "Next Step..." );
```





#### 导入

**导入指定内容**

```ts
import { ZipCodeValidator as ZCV } from "./ZipCodeValidator";

let myValidator = new ZipCodeValidator();
```

**整个模块导入到一个变量**

```typescript
import * as validator from "./ZipCodeValidator";
let myValidator = new validator.ZipCodeValidator();
```

**导入模块**

一些模块会设置一些全局状态供其他模块使用，这些模块可能没有任何的导出或用户根本就不关注它的导出。

```typescript
import "./my-module.js";
```



### 命名空间

一种组织代码的方式。通过命名空间可以将代码组织在一个与外部隔离的空间里。本质上，命名空间是**位于全局命名空间下**的一个普通的带有名字的 JavaScript **对象**。

使用命名空间的目的是为了提供**逻辑分组**和**避免命名冲突**。

#### 多文件中的命名空间

我们可以把命名空间分割到多个文件，尽管在不同文件中，但它们仍然是同一个命名空间。如果文件之间存在依赖关系，可以使用引用标签来告诉编译器文件之间的关联。

Validation.ts

```ts
namespace Validation {
    export interface StringValidator {
        isAcceptable(s: string): boolean;
    }
}
```

LettersOnlyValidator.ts

```ts
/// <reference path="Validation.ts" />
namespace Validation {
    const lettersRegexp = /^[A-Za-z]+$/;
    export class LettersOnlyValidator implements StringValidator {
        isAcceptable(s: string) {
            return lettersRegexp.test(s);
        }
    }
}
```

ZipCodeValidator.ts

```ts
/// <reference path="Validation.ts" />
namespace Validation {
    const numberRegexp = /^[0-9]+$/;
    export class ZipCodeValidator implements StringValidator {
        isAcceptable(s: string) {
            return s.length === 5 && numberRegexp.test(s);
        }
    }
}
```

Test.ts

```ts
/// <reference path="Validation.ts" />
/// <reference path="LettersOnlyValidator.ts" />
/// <reference path="ZipCodeValidator.ts" />

// Some samples to try
let strings = ["Hello", "98052", "101"];

// Validators to use
let validators: { [s: string]: Validation.StringValidator; } = {};
validators["ZIP code"] = new Validation.ZipCodeValidator();
validators["Letters only"] = new Validation.LettersOnlyValidator();

// Show whether each string passed each validator
for (let s of strings) {
    for (let name in validators) {
        console.log(`"${ s }" - ${ validators[name].isAcceptable(s) ? "matches" : "does not match" } ${ name }`);
    }
}
```



#### 别名

当我们需要经常用到命名空间中的某个成员时，为了简化操作，可以使用起别名语法给该成员起一个短的名字。

```typescript
namespace Shapes {
    export namespace Polygons {
        export class Triangle { }
        export class Square { }
    }
}

import polygons = Shapes.Polygons;
let sq = new polygons.Square(); // Same as "new Shapes.Polygons.Square()"
```



### 异同

相同之处：

+ 都是 TypeScript 用来组织代码的方法。
+ 都可以包含代码和声明。
+ 自身内容对外部不可见，除非明确使用 export 形式导出。

不同之处：

+ 命名空间是位于全局命名空间下的一个普通的带有名字的 JavaScript 对象；模块是一个包含顶级 import 或 export 的文件。
+ 由于命名空间是全局命名空间下的一个 JavaScript 对象，这使得它可以在多文件中同时使用。而模块只能是单个文件。
+ 模块可以声明它依赖关系，而命名空间不行。

注意：不应该对模块使用命名空间，使用命名空间是为了提供逻辑分组和避免命名冲突，而模块文件本身已经是一个逻辑分组，并且它的名字是由导入这个模块的代码指定，所以不同的模块在相同的作用域内不会使用相同的名字。



## 声明文件

