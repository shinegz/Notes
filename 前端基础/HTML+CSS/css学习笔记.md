## CSS

> 层叠样式表（**C**ascading **S**tyle **S**heet，简称：CSS），它是一门样式表语言，可以用它来选择性地为网页中的 HTML 元素添加样式。它描述的是HTML元素的布局和表现。

### 语法

> css样式表由一系列的语句组成。

#### 语句

> css中有两种语句：at-rule和ruleset

##### at-rule

一个 **at-rule** 是一个CSS 语句，以at符号开头, '`@`' (`U+0040 COMMERCIAL AT`), 后跟一个标识符，并包括直到下一个分号的所有内容, '`;`' (`U+003B SEMICOLON`), 或下一个CSS块，以先到者为准。

下面是一些 @规则, 由它们的标示符指定, 每种规则都有不同的语法:

- [`@charset`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@charset), 定义样式表使用的字符集.
- [`@import`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@import), 告诉 CSS 引擎引入一个外部样式表.
- [`@namespace`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@namespace), 告诉 CSS 引擎必须考虑XML命名空间。
- 嵌套@规则, 是嵌套语句的子集,不仅可以作为样式表里的一个语句，也可以用在条件规则组里：
  - [`@media`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@media), 如果满足媒介查询的条件则条件规则组里的规则生效。
  - [`@page`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@page), 描述打印文档时布局的变化.
  - [`@font-face`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@font-face), 描述将下载的外部的字体。
  - [`@keyframes`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@keyframes), 描述 CSS 动画的中间步骤 .
  - [`@supports`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@supports), 如果满足给定条件则条件规则组里的规则生效。
  - [`@document`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@document), 如果文档样式表满足给定条件则条件规则组里的规则生效。 *(推延至 CSS Level 4 规范)*



##### ruleset

<img src=".\css图\css-ruleset-structure.png" style="zoom:50%;" />

整个结构称为 **规则集**（通常简称“规则”），由选择器和声明块构成，各部分释义如下：

- 选择器（**Selector**）

  HTML 元素的名称位于规则集开始。它选择了一个或多个需要添加样式的元素（在这个例子中就是 `p` 元素）。要给不同元素添加样式只需要更改选择器就行了。

- 声明块（**Declaration block**）

  由一对大括号`{}`及包含在内的0个或多个声明组成。

+ 声明（**Declaration**）

  一个单独的规则，如 `color: red;` 用来指定添加样式元素的**属性**。

+ 属性（**Properties**）

  改变 HTML 元素样式的途径。（本例中 `color` 就是 `p`元素的属性。）CSS 中，由编写人员决定修改哪个属性以改变规则。

+ 属性的值（**Property value**）

  在属性的右边，冒号后面即**属性的值**，它从指定属性的众多外观中选择一个值（我们除了 `red` 之外还有很多属性值可以用于 `color` ）。

注意其他重要的语法：

- 每个规则集（除了选择器的部分）都应该包含在成对的大括号里（`{}`），大括号及里面的一系列声明构成一个声明块。
- 在每个声明里要用冒号（`:`）将属性与属性值分隔开。
- 在每个规则集里要用分号（`;`）将各个声明分隔开。

### 选择器

> 在CSS中，模式匹配规则确定样式规则适用于文档树中的哪些元素。 这些模式称为选择器，从简单的元素名称模式到丰富的上下文模式。 如果模式中的所有条件对于某个元素都为真，则选择器匹配该元素。

**选择器使用原则**

+ 根据 id 选单个元素
+ class 和 class 的组合选成组元素
+ tag 选择器确定页面风格

**选择器类型**

+ 简单选择器

  > **元素上的单个条件**

  + 类型
  + 通用
  + 属性
  + 类
  + ID
  + 伪类
    + 树结构关系伪类
    + 链接与行为伪类
    + 逻辑伪类
    + 其他伪类

+ 复合选择器

  > 复合选择器是一系列没有被组合器分隔的简单的选择器，代表**单个元素上的一组同时条件**。

+ 复杂选择器

  > 复杂选择器是由组合器分隔的一个或多个复合选择器的序列。 它代表由其组合器描述的**特定关系**的**一组元素**上的**一组同时条件**。

  组合器

  + 后代组合器（空格）
  + 子代组合器（>）
  + 相邻兄弟组合器（+）
  + 后继兄弟组合器（~）

+ 选择器列表

  > 由逗号分隔的简单、复合、复杂选择器列表，逗号表示“或”的关系。

**选择器优先级**

> 当一个元素被多个规则命中，不同规则指定同一属性为不同值时，就需要考虑优先级的问题。

**常见选择器示例**

| Pattern                  | Meaning                                                      | Described in section                                         | First defined in CSS level |
| :----------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :------------------------: |
| *                        | any element                                                  | [Universal selector](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#universal-selector) |             2              |
| E                        | an element of type E                                         | [Type selector](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#type-selectors) |             1              |
| E[foo]                   | an E element with a "foo" attribute                          | [Attribute selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#attribute-selectors) |             2              |
| E[foo="bar"]             | an E element whose "foo" attribute value is exactly equal to "bar" | [Attribute selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#attribute-selectors) |             2              |
| E[foo~="bar"]            | an E element whose "foo" attribute value is a list of whitespace-separated values, one of which is exactly equal to "bar" | [Attribute selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#attribute-selectors) |             2              |
| E[foo^="bar"]            | an E element whose "foo" attribute value begins exactly with the string "bar" | [Attribute selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#attribute-selectors) |             3              |
| E[foo$="bar"]            | an E element whose "foo" attribute value ends exactly with the string "bar" | [Attribute selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#attribute-selectors) |             3              |
| E[foo*="bar"]            | an E element whose "foo" attribute value contains the substring "bar" | [Attribute selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#attribute-selectors) |             3              |
| E[foo\|="en"]            | an E element whose "foo" attribute has a hyphen-separated list of values beginning (from the left) with "en" | [Attribute selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#attribute-selectors) |             2              |
| E:root                   | an E element, root of the document                           | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:nth-child(n)           | an E element, the n-th child of its parent                   | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:nth-last-child(n)      | an E element, the n-th child of its parent, counting from the last one | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:nth-of-type(n)         | an E element, the n-th sibling of its type                   | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:nth-last-of-type(n)    | an E element, the n-th sibling of its type, counting from the last one | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:first-child            | an E element, first child of its parent                      | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             2              |
| E:last-child             | an E element, last child of its parent                       | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:first-of-type          | an E element, first sibling of its type                      | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:last-of-type           | an E element, last sibling of its type                       | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:only-child             | an E element, only child of its parent                       | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:only-of-type           | an E element, only sibling of its type                       | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:empty                  | an E element that has no children (including text nodes)     | [Structural pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#structural-pseudos) |             3              |
| E:link E:visited         | an E element being the source anchor of a hyperlink of which the target is not yet visited (:link) or already visited (:visited) | [The link pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#link) |             1              |
| E:active E:hover E:focus | an E element during certain user actions                     | [The user action pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#useraction-pseudos) |          1 and 2           |
| E:target                 | an E element being the target of the referring URI           | [The target pseudo-class](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#target-pseudo) |             3              |
| E:lang(fr)               | an element of type E in language "fr" (the document language specifies how language is determined) | [The :lang() pseudo-class](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#lang-pseudo) |             2              |
| E:enabled E:disabled     | a user interface element E which is enabled or disabled      | [The UI element states pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#UIstates) |             3              |
| E:checked                | a user interface element E which is checked (for instance a radio-button or checkbox) | [The UI element states pseudo-classes](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#UIstates) |             3              |
| E::first-line            | the first formatted line of an E element                     | [The ::first-line pseudo-element](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#first-line) |             1              |
| E::first-letter          | the first formatted letter of an E element                   | [The ::first-letter pseudo-element](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#first-letter) |             1              |
| E::before                | generated content before an E element                        | [The ::before pseudo-element](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#gen-content) |             2              |
| E::after                 | generated content after an E element                         | [The ::after pseudo-element](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#gen-content) |             2              |
| E.warning                | an E element whose class is "warning" (the document language specifies how class is determined). | [Class selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#class-html) |             1              |
| E#myid                   | an E element with ID equal to "myid".                        | [ID selectors](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#id-selectors) |             1              |
| E:not(s)                 | an E element that does not match simple selector s           | [Negation pseudo-class](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#negation) |             3              |
| E F                      | an F element descendant of an E element                      | [Descendant combinator](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#descendant-combinators) |             1              |
| E > F                    | an F element child of an E element                           | [Child combinator](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#child-combinators) |             2              |
| E + F                    | an F element immediately preceded by an E element            | [Adjacent sibling combinator](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#adjacent-sibling-combinators) |             2              |
| E ~ F                    | an F element preceded by an E element                        | [General sibling combinator](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/#general-sibling-combinators) |             3              |

### CSS值

#### 值的类型

+ CSS中的关键字

+ 数值
  + 整数
  + 实数
  + 百分比
  + 维度（带有单位的数）
+ 字符串
+ URL

+ color
+ image
+ 2D位置
+ 函数

#### 单位

+ 长度单位

  + 相对长度

    + 相对于字体

      rem、em、ex、cap、ch、ic、lh、rlh

    + 相对于视口

      vw、vh、vi、vb、vmax、vmin

  + 绝对长度

    mm、Q、in、pt、pc、px

+ 角度单位

  deg、grad、rad、turn

+ 时间单位

  s、ms

+ 频率单位

  Hz、kHz

+ 分辨率单位

  dpi、dpcm、dppx



### 属性赋值

> 浏览器在解析文档并构建文档树之后，它必须为树中的每个元素的每个样式属性分配一个适用于目标媒体类型的值。
>
> 属性的最终值是一个六步计算的结果：
>
> 1、首先，收集所有应用到元素上的声明值（declared values）。每个元素的每个属性可能有0个或多个声明	  值
>
> 2、根据级联规则对元素属性的所有声明值进行优先级排序，优先级最高的即为元素属性的级联值（cascaded value）。每个元素的每个属性最多只有一个级联值
>
> 3、如果元素属性产生了级联值，则该值为指定值（specified value）；如果没有级联值，则使用属性的默认   	  值（defaulted）作为指定值
>
> 4、将指定值解析为用于继承的值（computed value）
>
> 5、如果必要的话，将computed value转换为绝对值（used value使用值）
>
> 6、根据本地环境的限制进行转换（actual value）

+ specified values

  得出specified value的机制：

  + **如果级联产生了一个值，则使用该值**。此外，如果该值为‘inherit’，则：

    每个属性还可以具有“ inherit”的级联值，这意味着对于给定元素，该属性将元素父级的计算值作为指定值。 “inherit”值可用于强制值的继承，也可用于通常不继承的属性。如果在根元素上设置了“继承”值，则会为属性分配其初始值。

  + 否则，如果该属性是继承的，并且该元素不是root元素，则使用父元素的computed value。

  + 否则，（该属性既没有cascade value，也不是继承来的）使用属性的初始值（initial value）。每个属性的初始值在属性的定义中指定。

+ computed values

  在级联过程中，将指定值(specified values)解析为计算值； 例如，将URI设置为绝对，然后将“ em”和“ ex”单位计算为像素或绝对长度。

+ used values

  使用值（used value）是采用计算值（computed value）并将任何剩余依赖项解析为绝对值的结果。

+ actual values

  使用值（used value）原则上是用于渲染的值，但是user agent可能无法在给定环境中使用该值，这时需要根据具体环境进行转换。

#### 默认

当级联过程没有产生值时，则需要通过其他规则来确定指定值

+ 如果元素的属性为继承属性，则属性值默认为父元素属性的计算值（对于根元素，继承值为属性的初始值）
+ 如果元素的属性既不是继承的，也没有产生级联值，则属性值默认为初始值（initial value）

**显式默认**

可以通过给元素属性显式赋值的形式，请求元素属性采用默认值

如果一个属性的级联值为initial、inherit、unset关键字，则：

+ inherit

  强制元素继承父元素的计算值

+ initial

  强制元素属性值采用初始值

+ unset

  如果属性为继承属性，则按inherit处理；如果不是则按initial处理

#### 继承

“继承”是CSS中另一个重要概念。在W3C规范中，描述每个CSS属性时都会有一个选项是“Inherited”，如果值为“no”表示该属性是不可继承的。



### 层叠（cascade）

#### 样式层叠

> 样式表可能有三个不同的来源：author、user、user agent。
>
> 这三个来源的样式表在作用域上会重叠，并且会根据级联进行交互。
>
> CSS级联为每个样式规则分配权重。 当应用多个规则时，权重最大的规则优先。
>
> 默认情况下，**作者样式表中的规则比用户样式表中的规则具有更大的权重。 但是，对于“! important”规则，优先级相反。 与UA的默认样式表中的规则相比，所有用户和作者规则的权重都更大。**

+ cascading order

  要查找元素/属性组合的值，用户代理必须应用以下排序顺序

  + 1.查找适用于目标媒体类型的所有相关元素和属性的声明。 如果关联的选择器与所讨论的元素匹配，并且目标媒体与包含声明的所有@media规则以及到达样式表的路径上的所有链接上的媒体列表相匹配，则声明适用。
  + 2.根据**重要性**（normal or important）和**来源**（author、user、user agent）。按升序排列为：
    1. user agent declarations
    2. **user normal declarations**
    3. author normal declarations
    4. author important declarations
    5. **user important declarations**
  + 3.按**选择器的特异性对具有相同重要性和来源的规则进行排序**：更具体的选择器将覆盖更通用的选择器。 伪元素和伪类分别计为普通元素和类。
  + 4.最后，按指定的顺序排序：如果两个声明的**重要性，来源和特异性相同**，则以**后者为准**。导入的样式表中的声明被视为在样式表本身中的任何声明之前。

+ !important rules

  !important 声明的规则优先级高于普通声明，并且user中的‘!important’优先级高于author。

+ calculating a selector's specificity

  A selector's specificity is calculated as follows:

  - count 1 if the declaration is from is a 'style' attribute rather than a rule with a selector, 0 otherwise (= a) (In HTML, values of an element's "style" attribute are style sheet rules. These rules have no selectors, so a=1, b=0, c=0, and d=0.)
  - count the number of **ID** attributes in the selector (= b)
  - count the number of **other attributes and class and pseudo-classes** in the selector (= c)
  - count the number of **element names and pseudo-elements** in the selector (= d)

#### 元素层叠（stacking）

##### 层叠上下文（context）

​	平时我们从设备终端看到的HTML文档都是一个平面的，事实上HTML文档中的元素却是存在于三个维度中。

<img src=".\css图\document-model.png" style="zoom:50%;" />

​	该系统包括一个三维`z` 轴，其中的元素是层叠（Stacked）的。`z` 轴的方向指向查看者，`x` 轴指向屏幕的右边，`y` 轴指向屏幕的底部。

<img src=".\css图\stacking-context.png" style="zoom:50%;" />

​	事实上，每个HTML元素都属于一个层叠上下文。给定层叠上下文中的每个定位元素都具有一个整数的层叠层级，具有更大堆栈级别的元素盒子总是在具有较低堆栈级别的盒子的前面（上面）。

​	文档中的层叠上下文由满足以下任意一个条件的元素形成：

- 根元素 (`<html>`)
- `z-index` 值不为`auto` 的
- `position` 值为非`static` 
- 一个`z-index` 值不为`auto` 的 Flex 项目 (Flex item)，即：父元素`display: flex|inline-flex` 
- `opacity` 属性值小于`1` 的元素
- `transform` 属性值不为`none` 的元素
- `mix-blend-mode` 属性值不为`normal` 的元素
- `filter` 、`perspective` 、`clip-path` 、`mask` 、`motion-path` 值不为`none` 的元素
- `perspective` 值不为`none` 的元素
- `isolation` 属性被设置为`isolate` 的元素
- 在`will-change` 中指定了任意 CSS 属性，即便你没有直接指定这些属性的值

​	每个页面都有一个默认的层叠上下文，这个层叠上下文的根就是html元素。html元素中的一切都被置于这个默认的层叠上下文的一个层叠层上。

##### 层叠水平（level）

​	层叠水平（Stacking Level）决定了**同一个层叠上下文**中元素在**`z`轴**上的**显示顺序**。所有的元素都有层叠水平，包括层叠上下文元素（**层叠上下文元素可能是另一层叠上下文中的普通元素**）。普通元素的层叠水平优先由层叠上下文决定，因此，层叠水平的比较只有在当前层叠上下文元素中才有意义。

​	注意，层叠水平和css的`z-index`属性不是同一个概念，`z-index`可以影响层叠水平，但只限于定位元素以及Flex盒子的孩子元素。

##### 层叠顺序（order）

在HTML文档中，默认情况之下有一个自然层叠顺序（Natural Stacing Order），即元素在`z` 轴上的顺序。它是由许多因素决定的。比如下面这个列表，它显示了元素盒子放入层叠顺序上下文的顺序，从层叠的底部开始，共有七种层叠等级：

- 背景和边框：形成层叠上下文的元素的背景和边框。层叠上下文中的最低等级。
- 负`z-index` 值：层叠上下文内有着负`z-index` 值的子元素。
- 块级盒：文档流中非行内非定位子元素。
- 浮动盒：非定位浮动元素。
- 行内盒：文档流中行内级别非定位子元素。
- `z-index: 0` ：定位元素。这些元素形成了新的层叠上下文。
- 正`z-index` 值：定位元素。层叠上下文中的最高等级。

<img src=".\css图\stacking-order.png" style="zoom:50%;" />

### CSS盒子模型

> 完整的 CSS 盒模型应用于块级盒子，内联盒子只使用盒模型中定义的部分内容。模型定义了盒的每个部分 —— margin, border, padding, and content —— 合在一起就可以创建我们在页面上看到的内容。

 <img src=".\css图\box-model.png" style="zoom:80%;" />

CSS中组成一个块级盒子需要:

- **Content box**: 这个区域是用来显示内容，大小可以通过设置 `width` 和 `height`.
- **Padding box**: 包围在内容区域外部的空白区域； 大小通过 `padding`相关属性设置。
- **Border box**: 边框盒包裹内容和内边距。大小通过 `border`相关属性设置。
- **Margin box**: 这是最外面的区域，是盒子和其他元素之间的空白区域。大小通过 `margin` 相关属性设置。

**CSS的box模型有一个外部显示类型，来决定盒子是块级还是内联**。

**同样盒模型还有内部显示类型，它决定了盒子内部元素是如何布局的**。默认情况下是按照 **正常文档流** 布局，也意味着它们和其他块元素以及内联元素一样。

但是，我们可以通过使用类似 `flex` 的 `display` 属性值来更改内部显示类型。 如果设置 `display: flex`，在一个元素上，外部显示类型是 `block`，但是内部显示类型修改为 `flex`。 该盒子的所有直接子元素都会成为flex元素，会根据 弹性盒子（Flexbox）规则进行布局。



### 视觉格式化模型

> CSS视觉格式化模型是用来**处理文档并将它显示在视觉媒体上的机制**

视觉格式化模型会根据css盒子模型将文档中的元素转换为一个个盒子，每个盒子的布局由以下因素决定：

- **盒子的尺寸** ：精确指定、由约束条件指定或没有指定
- **盒子的类型** ：行内盒子（inline）、行内级盒子（inline-level）、原子行内级盒子（atomic inline-level）和块盒子（block）
- **定位方案** ：普通流定位、浮动定位或绝对定位
- **文档树中的其它元素** ：即当前盒子的子元素或兄弟元素
- **视窗尺寸与位置** 
- **所包含的图片的尺寸** 
- **其他的某些外部因素** 

#### 包含块

元素box的尺寸或位置有时需要根据某个矩形来计算，这个矩形被称为该元素的‘包含块’。（采用百分比来定义元素box的width、height、padding、margin，**绝对定位元素的offset属性**等）

**初始包含块**

> 以整个 `canvas` (渲染内容的区域) 的坐标原点(左上)为基准，以 `viewport` (显示渲染内容的区域)为大小的矩形。

**“包含块”的定义**

+ 对于根元素来说，其包含块是一个被称为‘**初始包含块**’的矩形，对于连续媒体，**它具备和视口一样的尺寸，并被固定在画布原点**；对于分页媒体，**它为页面区域**。

+ 对于其他元素

  + position属性值为relative或static

    则包含的块由作为**块容器**或**建立格式化上下文**的最近祖先框的‘**content edge**’（盒子模型的内容框）形成。

  + position属性值为fixed

    在连续媒体里，包含块为**视口**；在分页媒体里，包含块为页面区域。

  + position属性值为absolute

    + 有position属性值不为static的祖先元素

    ​       **祖先元素为inline元素：**

    ​		其他情况：包含块为祖先元素的‘**padding edge**’形成。

    + 没有position属性值不为static的祖先元素

      包含块为**初始包含块**

#### 盒子类型

> 盒子具有不同的类型，盒子的类型部分地影响其在视觉格式化模型中的行为。 “ display”属性指定了盒子的类型。

+ 块级元素（Block-level ）和块盒子（block box）

  + **块级元素**：被视觉格式化为block的源文档中的元素

    当元素的 `display`为 `block`、`list-item` 或 `table` 时，该元素将成为块级元素。

  + **块级盒子**：block-level box，由块级元素生成。一个块级元素至少会生成一个块级盒子，但也有可能生成多个（例如列表项元素）。参与**块格式化上下文**（block formatting context）（规定了块级盒子的渲染方式）的创建。**描述元素与其父元素和兄弟元素之间的行为**。

  + **块容器盒子**：block container box或block containing box，块容器盒子侧重于当前盒子作为“容器”的这一角色，它不参与当前块的布局和定位，它所描述的仅仅是当前盒子与其后代之间的关系。换句话说，**块容器盒子主要用于确定其子元素的定位、布局**等。

    **描述元素跟其后代之间的行为**

  + **块盒子**：block box，如果一个块级盒子同时也是一个块容器盒子，则称其为块盒子。
  + **匿名块盒子**

+ 行内级元素（Inline-level）和行内盒子（inline box）

  + **行内级元素**：源文档中不构成内容块的那些元素

    如果一个元素的 `display` 属性为 `inline`、`inline-block` 或 `inline-table`，则称该元素为行内级元素。

  + **行内级盒子**：inline-level box，行内级元素会生成行内级盒子，行内级盒子包括行内盒子和原子行内级盒子两种，区别在于该盒子是否参与行内格式化上下文（inline formatting context）的创建。
  + **行内盒子**：inline box，参与行内格式化上下文创建的行内级盒子称为行内盒子。
  + **匿名行内盒子**

+ 其他类型盒子

#### 格式化上下文

> CSS 格式化上下文 ，也被称作视觉格式化模型 ，**指页面中一个渲染区域，拥有一套渲染规则，用来控制盒子的布局**。
>
> **其主要作用是决定盒子模型的布局，其子元素将如何定位以及和其他元素的关系和相互作用**

+ 行内格式化上下文（IFC）

  > 行内元素从包含块顶端水平方向上逐一排列，水平方向上的`margin` 、`border` 、`padding` 生效。行内元素在垂直方向上可按照顶部、底部或基线对齐。

  - 行内元素按照`text-align` 进行水平居中
  - 行内元素撑开父元素高度，通过`vertical-align` 属性进行垂直居中

+ 块格式化上下文（BFC）

  > 是块盒子的布局过程发生的区域，也是浮动元素与其他元素交互的区域。BFC实际上就是页面中一块渲染区域，该区域与其他区域隔离开来。容器里面子元素不会影响到外部，外部的元素也不会影响到容器里的子元素。

  BFC 内部的盒子会从上至下一个接着一个顺序排列。BFC 内的垂直方向的盒子距离以`margin` 属性为准，上下`margin` 会叠加。每个元素的左侧最外层边界与包含块 BFC 的左边相接触(对于从左往右的格式化，否则相反)。即使存在浮动也是如此。BFC 的区域不会与浮动元素的盒子折叠。**BFC 的高度也会受到浮动元素的影响，浮动元素参与计算**。

  `html`元素不是唯一能够创建块格式上下文的元素。默认为块布局的任何元素也会为其后代元素创建块格式上下文。此外，还有一些CSS属性可以使元素创建一个BFC，即使默认情况下它不这样做。

  下面这些规则可以创建一个BFC：

  - 根元素或包含根元素的元素
  - 浮动元素（元素的`float` 不是`none` ）
  - 绝对定位元素（元素的`position` 为`absolute` 或`fixed` ）
  - 行内块元素（元素的`display` 为`inline-block` ）
  - 表格单元格（元素的`display` 为`table-cell` ，HTML表格单元格默认为该值）
  - 表格标题（元素的`display` 为`table-caption` ，HTML表格标题默认为该值）
  - 匿名表格单元格元素（元素的`display` 为`table` 、`table-row` 、`table-row-group` 、`table-header-group` 、`table-footer-group` （分别是HTML`table` 、`row` 、`tbody` 、`thead` 、`tfoot` 的默认属性）或`inline-table` ）
  - `overflow` 值不为`visible` 的块元素
  - `display` 值为`flow-root` 的元素
  - `contain` 值为`layout` 、`content` 或`strict` 的元素
  - 弹性元素（`display` 为`flex` 或`inline-flex` 元素的直接子元素）
  - 网格元素（`display` 为`grid` 或`inline-grid` 元素的直接子元素）
  - 多列容器（元素的`column-count` 或`column-width` 不为`auto` ，包括`column-count` 为`1` ）
  - `column-span` 为`all` 的元素始终会创建一个新的BFC，即使该元素没有包裹在一个多列容器中

  块格式化上下文包含创建它的元素内部的所有内容。其主要使用：

  - 创建独立的渲染环境
  - 防止因浮动导致的高度塌陷
  - 防止上下相邻的外边距折叠

+ FLex格式化上下文（FFC）

  > 当`display` 取值为`flex` 或`inline-flex` ，将会创建一个Flexbox容器。**该容器为其内容创建一个新的格式化上下文，即Flex格式化上下文。**

  不过要注意的是，Flexbox容器不是块容器（块级盒子），下列适用于块布局的属性并不适用于Flexbox布局：

  - 多列中的`column-*` 属性不适用于Flexbox容器
  - `float` 和`clear` 属性作用于Flex项目上将无效，也不会把让Flex项目脱离文档流
  - `vertical-algin` 属性作用于Flex项目上将无效
  - `::first-line` 和`::first-letter` 伪元素不适用于Flexbox容器，而且Flexbox容器不为他们的祖先提供第一个格式化的行或第一个字母

+ Grid格式化上下文（GFC）

  > 元素的`display` 值为`grid` 或`inline-grid` 时，将会创建一个Grid容器。**该容器为其内容创建一个新的格式化上下文，即Grid格式化上下文。**

  网格容器不是块容器，因此一些假定为块布局设计的属性并不适用于网格格式化上下文中。特别是：

  - `float` 和`clear` 运用于网格项目将不会生效。但是`float` 属性仍然影响网格完完全全器子元素上`display` 的计算值，因为这发生在确定网格项目之前
  - `vertical-align` 运用于网格项目也将不会生效
  - `::first-line` 和`::first-letter` 伪元素不适用于网格容器，而且网格容器不向它们社先提供第一个格式化行或第一个格式化字母

#### 定位方案

> 它们之间的不同在于：1、定位的参照物不同。2、是否脱离正常文档流。

There are three schemes:

1. Normal: the object is positioned according to its place in the document. This means its place in the render tree is like its place in the DOM tree and laid out according to its **box type** and **dimensions**
2. Float: the object is first laid out like normal flow, then moved as far left or right as possible
3. Absolute: the object is put in the render tree in a different place than in the DOM tree

The positioning scheme is set by the "position" property and the "float" attribute.

- static and relative cause a normal flow
- absolute and fixed cause absolute positioning

In static positioning no position is defined and the default positioning is used. In the other schemes, the author specifies the position: top, bottom, left, right.

##### 普通文档流（normal flow）

> **元素在web页面上的一种呈现方式**。按照元素在文档中的位置和顺序，从上往下依次排列，每个新的块级元素渲染为新行，行内元素则按照顺序被水平渲染直到当前行遇到边界，然后换到下一行垂直渲染。
>
> 普通文档流中的元素在屏幕上的位置只受三个因素影响：在文档中的位置、盒子类型、自身尺寸。

##### 浮动（float）

由float属性控制，此属性指定盒子是否应该向左，向右浮动或根本不浮动。 可以为任何元素设置它，**但仅作用于非绝对定位的元素**。

+ clear

> value: left、right、both、none

此属性指示元素框的上边应该在由源文档中它前面的元素产生的浮动盒子边框底部的下面。clear属性不考虑元素自身内部或其他块格式化上下文中的浮动

**left**

Requires that the top border edge of the box be below the bottom outer edge of any left-floating boxes that resulted from elements earlier in the source document.

**right**

Requires that the top border edge of the box be below the bottom outer edge of any right-floating boxes that resulted from elements earlier in the source document.

**both**

Requires that the top border edge of the box be below the bottom outer edge of any right-floating and left-floating boxes that resulted from elements earlier in the source document.

**none**

No constraint on the box's position with respect to floats.



##### 绝对定位（absolute positioning）

> 如果一个元素的‘position’属性的值为‘static’外任何值，那么这个元素被称为‘be positioned’，即被定位了。

+ **盒子偏移**

> 被定位的元素box，其left、top、right、bottom的大小表示的是
>
> + position为absolute或fixed
>
>   其**包含块**的边框与其**‘margin edge’**之间的距离。
>
> + position为relative
>
>   与其自身原来位置之间的距离。

开启绝对定位的元素，将会脱离普通文档流，处于更高的层级（普通文档流中的元素会占据其在普通文档流中的位置），**如果没有设置top、left、right、bottom属性值**，则默认为auto，而不是left：0；top：0；时的位置，**默认覆盖在其普通文档流中的位置的上方。**



#### overflow

> 此属性指定块容器元素的内容溢出元素盒子时是否被裁剪。

属性值：

+ **visible**

溢出的内容不会被裁减，内容会渲染到块盒子的外面。

This value indicates that content is not clipped, i.e., it may be rendered outside the block box.

+ **hidden**

溢出的内容会被裁减，并且不会提供滚动条来显示裁减区外的内容

This value indicates that the content is clipped and that no scrolling user interface should be provided to view the content outside the clipping region.

+ **scroll**

This value indicates that the content is clipped and that if the user agent uses a scrolling mechanism that is visible on the screen (such as a scroll bar or a panner), that mechanism should be displayed for a box whether or not any of its content is clipped. This avoids any problem with scrollbars appearing and disappearing in a dynamic environment. When this value is specified and the target medium is 'print', overflowing content may be printed. When used on [table boxes,](https://www.w3.org/TR/CSS22/tables.html#table-box) this value has the same meaning as 'visible'.

+ **auto**

The behavior of the 'auto' value is user agent-dependent, but should cause a scrolling mechanism to be provided for overflowing boxes. When used on [table boxes,](https://www.w3.org/TR/CSS22/tables.html#table-box) this value has the same meaning as 'visible'.



### 媒体类型

<img src=".\css图\mediatype.png" style="zoom: 50%;" />



### Flex布局

![](.\css图\flexbox.png)

#### Flex布局是什么

Flex布局：Flex是Flexible box的缩写，意为“弹性布局”，是W3C在2009年提出的一种新的网页布局方案，它可以根据屏幕的大小以及设备的类型来使网页元素更好的进行排列、对齐和分配空白空间。

任何一个容器都可以指定为 Flex 布局。 

块元素声明方式

````css
.box{
    display: flex
}
````

行内元素声明方式

````css
.box{
    display： inline-flex
}
````

注意：当设为Flex布局后，其子元素的float、clear和vertical-align属性将失效。

采用Flex布局的元素，称为Flex容器，它的所有子元素自动成为容器成员，称为Flex项目。

容器默认存在两根轴：水平的主轴（main axis）和垂直的交叉轴（cross axis）。主轴的开始位置（与边框的交叉点）叫做`main start`，结束位置叫做`main end`；交叉轴的开始位置叫做`cross start`，结束位置叫做`cross end`。

项目默认沿主轴排列。单个项目占据的主轴空间叫做`main size`，占据的交叉轴空间叫做`cross size`。

#### 容器属性

- flex-direction  属性决定主轴的方向（即项目的排列方向） ，它有四个值。

  - `row`（默认值）：主轴为水平方向，起点在左端。
  - `row-reverse`：主轴为水平方向，起点在右端。
  - `column`：主轴为垂直方向，起点在上沿。
  - `column-reverse`：主轴为垂直方向，起点在下沿。

- flex-wrap 属性定义，如果一条轴线排不下，如何换行。  它可能取三个值。 

  +  `nowrap`（默认）：不换行。 
  +  `wrap`：换行，第一行在上方。 
  +  `wrap-reverse`：换行，第一行在下方。 

- flex-flow 属性是`flex-direction`属性和`flex-wrap`属性的简写形式，默认值为`row nowrap`。 

- justify-content 属性定义了项目在主轴上的对齐方式。  它可能取5个值，具体对齐方式与轴的方向有关。下面假设主轴为从左到右。 

  - `flex-start`（默认值）：左对齐
  - `flex-end`：右对齐
  - `center`： 居中
  - `space-between`：两端对齐，项目之间的间隔都相等。
  - `space-around`：每个项目两侧的间隔相等。所以，项目之间的间隔比项目与边框的间隔大一倍。

- align-items 属性定义项目在交叉轴上如何对齐。  它可能取5个值。具体的对齐方式与交叉轴的方向有关，下面假设交叉轴从上到下。

  - `flex-start`：交叉轴的起点对齐。
  - `flex-end`：交叉轴的终点对齐。
  - `center`：交叉轴的中点对齐。
  - `baseline`: 项目的第一行文字的基线对齐。
  - `stretch`（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度。

- align-content 属性定义了多根轴线的对齐方式。如果项目只有一根轴线，该属性不起作用。  该属性可能取6个值。 

  - `flex-start`：与交叉轴的起点对齐。
  - `flex-end`：与交叉轴的终点对齐。
  - `center`：与交叉轴的中点对齐。
  - `space-between`：与交叉轴两端对齐，轴线之间的间隔平均分布。
  - `space-around`：每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍。
  - `stretch`（默认值）：轴线占满整个交叉轴。

#### 项目属性

 以下6个属性设置在项目上。 

- `order` 属性定义项目的排列顺序。数值越小，排列越靠前，默认为0。 

- `flex-grow`属性定义项目的放大比例，默认为`0`，即如果存在剩余空间，也不放大。

  如果所有项目的`flex-grow`属性都为1，则它们将等分剩余空间（如果有的话）。如果一个项目的`flex-grow`属性为2，其他项目都为1，则前者占据的剩余空间将比其他项多一倍。 

- `flex-shrink`属性定义了项目的缩小比例，默认为1，即如果空间不足，该项目将缩小。

  如果所有项目的`flex-shrink`属性都为1，当空间不足时，都将等比例缩小。如果一个项目的`flex-shrink`属性为0，其他项目都为1，则空间不足时，前者不缩小。

  负值对该属性无效。

- `flex-basis` 属性定义了在分配多余空间之前，项目占据的主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。它的默认值为`auto`，即项目的本来大小。 

- `flex` 属性是`flex-grow`, `flex-shrink` 和 `flex-basis`的简写，默认值为`0 1 auto`。后两个属性可选。 

  该属性有两个快捷值：`auto` (`1 1 auto`) 和 none (`0 0 auto`)。 

- `align-self` 属性允许单个项目有与其他项目不一样的对齐方式，可覆盖`align-items`属性。默认值为`auto`，表示继承父元素的`align-items`属性，如果没有父元素，则等同于`stretch`。 



### Grid 布局





### 变形动画





