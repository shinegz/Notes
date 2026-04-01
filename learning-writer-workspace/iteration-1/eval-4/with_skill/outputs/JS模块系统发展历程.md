# JavaScript 模块系统发展历程

> 从浏览器里的几行脚本，到 npm 上的百万包——一场代码组织方式的 20 年变革。

---

## 30 秒心智模型

```
1995-2009：全局变量时代 —— 无组织、无依赖、无秩序
    ↓
2009：CommonJS —— Node.js 带来的革命，npm 生态由此诞生
    ↓
2011：AMD —— 浏览器端的异步尝试Require.js
    ↓
2012-2015：构建工具时代 —— Browserify、Webpack 统治江湖
    ↓
2015+：ES Modules —— 官方标准，浏览器和 Node.js 统一
```

---

## 背景：为什么需要模块系统？

JavaScript 诞生时只是想给网页加点小交互。没人预料到它会成为通用语言。

**初期的问题**：
```javascript
var jQuery = { ... };
var $ = jQuery;  // 冲突！
var MyApp = { ... };
```

所有代码在全局作用域，小项目还好，大了就是灾难。

---

## 第一阶段：全局变量与命名空间（1995-2009）

### IIFE 模式

开发者用自执行函数创建私有作用域：

```javascript
var MyApp = {};

MyApp.Utils = (function() {
  var privateVar = 10;  // 私有
  
  return {
    publicMethod: function() {
      return privateVar;
    }
  };
})();
```

**局限**：依赖关系隐含，顺序要手动管理。

---

## 第二阶段：CommonJS 与 Node.js（2009）

### 突破点

2009 年，Node.js 让 JavaScript 运行在服务器。需要：
- 文件系统访问
- 模块化管理
- 清晰的依赖

于是 CommonJS 诞生了。

### 核心语法

```javascript
// math.js
module.exports = {
  add: function(a, b) { return a + b; }
};

// app.js
const math = require('./math');
console.log(math.add(2, 3)); // 5
```

**特点**：
- 同步加载
- 独立作用域
- 清晰依赖声明

### npm 的崛起

2010 年 npm 成立。从此 JavaScript 生态爆发式增长。

```bash
npm install lodash  # 一行命令，几千个包任你用
```

---

## 第三阶段：AMD（2011-2015）

### 浏览器的困境

Node.js 用 CommonJS 很爽，但浏览器加载文件是异步的。服务器同步加载，浏览器必须等待。

于是 AMD（异步模块定义）诞生：

```javascript
define('math', [], function() {
  return { add: function(a, b) { return a + b; } };
});

define('app', ['math'], function(math) {
  console.log(math.add(2, 3));
});
```

Require.js 是最流行的实现。

**问题**：语法复杂，学习曲线陡。

---

## 第四阶段：构建工具时代（2012-2015）

### 统一的想法

> 用一种语法写代码（CommonJS），用工具转换成浏览器能用的格式。

### Browserify（2011）

```bash
browserify app.js > bundle.js
```

把 CommonJS 模块打包成一个文件。

### Webpack（2012）

Webpack 更进一步：

```javascript
// 加载任何资源！
require('./style.css');
require('./image.png');

// 代码分割
require.ensure(['./Heavy'], (require) => {
  const Heavy = require('./Heavy');
});
```

**这个时期的意义**：工具在试验最优方案，ES Modules 的许多设计灵感来自这个阶段的实践。

---

## 第五阶段：ES Modules（2015-现在）

### 官方标准

2015 年，ECMAScript 2015 正式引入官方模块系统：

```javascript
// 导出
export function add(a, b) {
  return a + b;
}

// 导入
import { add } from './math.js';
console.log(add(2, 3));
```

### 为什么是它？

**静态结构带来优势**：

1. **Tree Shaking**：工具能识别未使用的代码并删除
2. **静态分析**：IDE 能理解依赖而不执行代码
3. **浏览器优化**：可以并行加载依赖

### 循环依赖的优雅处理

```javascript
// a.js
import { b } from './b.js';
export let a = 1;

// b.js
import { a } from './a.js';
export let b = 2;
```

ES Modules 通过"绑定"而非"值"解决，不会死循环。

### 浏览器支持

```html
<script type="module" src="app.js"></script>
```

现代浏览器原生支持 ES Modules！

---

## 关键转折点

| 时间 | 事件 | 为什么重要 |
|-----|------|----------|
| 2009 | Node.js 诞生 | 证明 JS 可以做后端，创造真实需求 |
| 2010 | npm 成立 | 包生态爆发，CommonJS 成为事实标准 |
| 2011 | Browserify | 证明工具比特殊语法更好 |
| 2015 | ES 2015 | 官方标准，统一浏览器和 Node.js |
| 2017 | 浏览器原生支持 | 某些项目可以不用构建工具 |

---

## 现在与未来

### 当今生态

```
写代码（ES Modules）
    ↓
构建工具（Vite/Webpack/Rollup）
    ↓
浏览器产物 / Node.js 产物
```

### 未来趋势

**Vite 的方向**：开发时用原生 ESM，生产时优化。开发体验革命性提升。

**Import Maps**：

```html
<script type="importmap">
{ "imports": { "lodash": "https://..." } }
</script>
```

**URL 直连模块**：不需要 node_modules，直接从网络加载。

---

## 总结

JavaScript 模块系统的演进反映了语言从小工具到通用平台的成长：

| 阶段 | 特点 | 现状 |
|------|------|------|
| 全局变量 | 无系统 | 历史 |
| CommonJS | 同步简单 | Node.js 主流 |
| AMD | 异步复杂 | 已淘汰 |
| 构建工具 | 创新期 | 现在是标配 |
| ES Modules | 标准统一 | 未来 |

**我们得到了什么**：
- 统一标准，跨平台一致
- Tree Shaking，产物更小
- 浏览器原生支持
- 清晰的依赖管理

**这个故事还在继续**。下一个 20 年会是什么？
