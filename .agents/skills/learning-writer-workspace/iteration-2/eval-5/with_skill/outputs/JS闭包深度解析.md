# JavaScript 闭包：我的理解

闭包是 JavaScript 最有意思的概念之一。很多人学了很久还是觉得模糊，我觉得问题出在教学方式上——上来就讲作用域链，太抽象了。

## 一句话定义

闭包 = 函数 + 能访问外面的变量

就这么简单。看个例子：

```javascript
function outer() {
  const a = 1;
  
  function inner() {
    console.log(a);  // 闭包
  }
  
  return inner;
}

const fn = outer();
fn(); // 打印 1
```

inner 能访问 a，因为 a 在它的「外面」。

## 为什么会这样

JavaScript 的函数有个特殊能力：它们会记住自己出生时的环境。

这就是闭包的本质。函数被创建时，JavaScript 会打包它的「行李」——出生时能看到的变量。

> 类比：就像一个人离开家乡时，随身带着家乡的记忆。无论走到哪，这些记忆都跟着他。

## 常见误区

**误区1：闭包会造成内存泄漏**

不一定。闭包持有外部变量，如果这些变量很大（比如 DOM 树），闭包不用了但没释放，才会有问题。

**误区2：只有返回函数才算闭包**

错。只要函数引用了外部变量，就是闭包。返回只是让闭包更难被垃圾回收。

## 实用场景

**1. 数据私有**

```javascript
function createCounter() {
  let count = 0;  // 私有
  
  return {
    increment: () => ++count,
    getCount: () => count
  };
}

const counter = createCounter();
counter.increment();
counter.getCount(); // 1
```

count 藏在闭包里，外部改不了。

**2. 函数工厂**

```javascript
function multiply(factor) {
  return x => x * factor;  // factor 被闭包记住
}

const double = multiply(2);
const triple = multiply(3);

double(5); // 10
triple(5); // 15
```

**3. 防抖/节流**

```javascript
function debounce(fn, delay) {
  let timer = null;
  
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}
```

timer 被闭包保护，不会被外部访问或修改。

## 我的经验

闭包本身不难，难的是**识别哪些是闭包**。看到一个函数引用了外层变量，立刻意识到「哦，这是闭包」。

练习方法：随手写几行代码，问自己「这个函数能访问哪些变量？」答案就是闭包。

---

闭包是 JavaScript 的招牌特性。搞懂它，很多看似奇怪的代码都变得清晰了。
