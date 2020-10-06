## CSS

> 层叠样式表（**C**ascading **S**tyle **S**heet，简称：CSS），它是一门样式表语言，可以用它来选择性地为网页中的 HTML 元素添加样式。它描述的是HTML元素的布局和表现。

### “CSS 规则集”详解

![](D:\GitProjects\notes\前端\JS笔记图\css图\css-declaration.png)

整个结构称为 **规则集**（通常简称“规则”），各部分释义如下：

- 选择器（**Selector**）

  HTML 元素的名称位于规则集开始。它选择了一个或多个需要添加样式的元素（在这个例子中就是 `p` 元素）。要给不同元素添加样式只需要更改选择器就行了。

- 声明（**Declaration**）

  一个单独的规则，如 `color: red;` 用来指定添加样式元素的**属性**。

- 属性（**Properties**）

  改变 HTML 元素样式的途径。（本例中 `color` 就是 [``](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/p) 元素的属性。）CSS 中，由编写人员决定修改哪个属性以改变规则。

- 属性的值（Property value）

  在属性的右边，冒号后面即**属性的值**，它从指定属性的众多外观中选择一个值（我们除了 `red` 之外还有很多属性值可以用于 `color` ）。

注意其他重要的语法：

- 每个规则集（除了选择器的部分）都应该包含在成对的大括号里（`{}`）。
- 在每个声明里要用冒号（`:`）将属性与属性值分隔开。
- 在每个规则集里要用分号（`;`）将各个声明分隔开。



### 选择器

| Selector                                                     | Example             | Learn CSS tutorial                                           |
| :----------------------------------------------------------- | :------------------ | :----------------------------------------------------------- |
| [Type selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Type_selectors) | `h1 { }`            | [Type selectors](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Type_Class_and_ID_Selectors#Type_selectors) |
| [Universal selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Universal_selectors) | `* { }`             | [The universal selector](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Type_Class_and_ID_Selectors#The_universal_selector) |
| [Class selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Class_selectors) | `.box { }`          | [Class selectors](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Type_Class_and_ID_Selectors#Class_selectors) |
| [id selector](https://developer.mozilla.org/en-US/docs/Web/CSS/ID_selectors) | `#unique { }`       | [ID selectors](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Type_Class_and_ID_Selectors#ID_Selectors) |
| [Attribute selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) | `a[title] { }`      | [Attribute selectors](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Attribute_selectors) |
| [Pseudo-class selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-classes) | `p:first-child { }` | [Pseudo-classes](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Pseuso-classes_and_Pseudo-elements#What_is_a_pseudo-class) |
| [Pseudo-element selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements) | `p::first-line { }` | [Pseudo-elements](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Pseuso-classes_and_Pseudo-elements#What_is_a_pseudo-element) |
| [Descendant combinator](https://developer.mozilla.org/en-US/docs/Web/CSS/Descendant_combinator) | `article p`         | [Descendant combinator](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Combinators#Descendant_Selector) |
| [Child combinator](https://developer.mozilla.org/en-US/docs/Web/CSS/Child_combinator) | `article > p`       | [Child combinator](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Combinators#Child_combinator) |
| [Adjacent sibling combinator](https://developer.mozilla.org/en-US/docs/Web/CSS/Adjacent_sibling_combinator) | `h1 + p`            | [Adjacent sibling](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Combinators#Adjacent_sibling) |
| [General sibling combinator](https://developer.mozilla.org/en-US/docs/Web/CSS/General_sibling_combinator) | `h1 ~ p`            | [General sibling](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Combinators#General_sibling) |



### CSS属性值

CSS的属性值可以是单个值，也可以是值的组合。

CSS的属性值大概可以分为三大类：

+ 关键字类型：如red、float、relative、auto等。
+ 数值类型：如1.2、50%、16px、1.5em等。
  + 数字
  + 长度
    + 绝对长度：如px
    + 相对长度：em（在font-size中表示父元素的字体大小、其他属性中则为自身字体大小）、rem（根元素字体大小）、vw（视窗宽度的1%）、vh（视窗高度的1%）、vmin（视窗较小尺寸的1%）、vmax（视窗较大尺寸的1%）
  + 百分比：相对的是父元素
+ 函数类型：如rgb(255,12,0)、rgba(255,12,0.6)a表示透明度、hsl(360,60%,50%)三个值分别表示色调（0-360）饱和度亮度、hsla()、url()、linear-gradient()等。



### CSS盒子模型

> 完整的 CSS 盒模型应用于块级盒子，内联盒子只使用盒模型中定义的部分内容。模型定义了盒的每个部分 —— margin, border, padding, and content —— 合在一起就可以创建我们在页面上看到的内容。

 CSS中组成一个块级盒子需要:

- **Content box**: 这个区域是用来显示内容，大小可以通过设置 `width` 和 `height`.
- **Padding box**: 包围在内容区域外部的空白区域； 大小通过 `padding`相关属性设置。
- **Border box**: 边框盒包裹内容和内边距。大小通过 `border`相关属性设置。
- **Margin box**: 这是最外面的区域，是盒子和其他元素之间的空白区域。大小通过 `margin` 相关属性设置。

CSS的box模型有一个外部显示类型，来决定盒子是块级还是内联。

同样盒模型还有内部显示类型，它决定了盒子内部元素是如何布局的。默认情况下是按照 **正常文档流** 布局，也意味着它们和其他块元素以及内联元素一样。

但是，我们可以通过使用类似 `flex` 的 `display` 属性值来更改内部显示类型。 如果设置 `display: flex`，在一个元素上，外部显示类型是 `block`，但是内部显示类型修改为 `flex`。 该盒子的所有直接子元素都会成为flex元素，会根据 弹性盒子（Flexbox）规则进行布局。

### **css属性参考手册：** https://www.w3cschool.cn/cssref/ 

一般常用属性：

+ margin：margin-top（bottom、left、right）

+ padding : padding-top（bottom、left、right）

+ border ：简写语法 border ： style  color  width（同时为四个边设置三个属性）

​                 单个边框语法： border-方位-样式

​                 方位属性： -top、-left、-bottom、-right

​                 样式属性： -style、-color、-width

+ boder-radius: 语法： border-*-radius

​                         为 top-left、top-right、bottom-left、bottom-right

+ outline：轮廓线不影响页面布局，轮廓线显示在边框外边

​                语法： 简写语法outline ： style  color  width

​                             一般语法 outline-style、outline-color、outline-width

+ box-sizing：border-box表示元素高度与宽度包括内边距和边框

​                      border-content表示元素高度与宽度只是内容宽度

+ box-shadow：语法 box-shadow: *h-shadow v-shadow blur spread color* inset;  

+ visibility：控制元素的显示隐藏，在隐藏后空间位也保留。 



### Positioning scheme

> 它们之间的不同在于：1、定位的参照物不同。2、是否脱离正常文档流。

There are three schemes:

1. Normal: the object is positioned according to its place in the document. This means its place in the render tree is like its place in the DOM tree and laid out according to its **box type** and **dimensions**
2. Float: the object is first laid out like normal flow, then moved as far left or right as possible
3. Absolute: the object is put in the render tree in a different place than in the DOM tree



The positioning scheme is set by the "position" property and the "float" attribute.

- static and relative cause a normal flow
- absolute and fixed cause absolute positioning


In static positioning no position is defined and the default positioning is used. In the other schemes, the author specifies the position: top, bottom, left, right.



The way the box is laid out is determined by:

- Box type
- Box dimensions
- Positioning scheme
- External information such as image size and the size of the screen



### 前端布局中的一些知识

float属性只对还处于普通文档流中的元素起作用，例如若元素的position属性为absolute时，元素就脱离文档流了，此时该元素的float属性将会失效；而当position为relative时，float属性依然有效，这是因为relative没有使元素脱离文档流，并且left、top偏移是相对浮动后的位置偏移的，也就是其在文档流中的位置，这说明float的作用可以看做是将元素浮动到了文档流的面上（文档流可以形象的看做是一个大水池（window就是那最大的水池，里面的子元素也可以看做盒子，盒子又可以被看做是小的水池，里面的元素则是更小的水池，这样也就可以帮助理解元素浮动不会超过其父元素），没有浮动时各个元素盒子都是处于水池的底部，盒子的高和水池相同（这可以帮助理解浮动不会超过其上面的块兄弟元素），内联元素则比较特殊，它会被浮动元素所挤开，并且里面的文字会位于浮动元素的后面或四周）浮动后的元素都变成了inline-block元素，可以设置高宽，默认高宽由内容撑开。

### 定位

* 绝对定位 

开启绝对定位的元素，将会脱离普通文档流，处于更高的层级（普通文档流中的元素会占据其在普通文档流中的位置），**如果没有设置top、left、right、bottom属性值**，则默认为auto，而不是left：0；top：0；时的位置，**默认覆盖在其普通文档流中的位置的上方。**

如果所有的父元素都没有显式地定义position属性，那么所有的父元素默认情况下position属性都是static。结果，绝对定位元素会被包含在**初始块容器**中。这个初始块容器有着和浏览器视口一样的尺寸，并且<html>元素也被包含在这个容器里面。简单来说，绝对定位元素会被放在<html>元素的外面，并且根据浏览器视口（注意：不是浏览器窗口）来定位。

若其父元素中有position不为static的元素，则以该元素为参照元素进行定位。

top、left、bottom、right为参照元素盒子模型**padding盒子边框**与定位元素盒子模型的margin外边对应的距离。

* 相对定位

开启相对定位的元素，将会提升层级，不过其对普通文档流中的元素没有影响。偏移的参考点为其开启定位前的位置，top、left、right、bottom的值为元素原来位置与定位后的位置之间的对应距离。

+ 固定定位

其与绝对定位几乎完全相同，唯一不同的是其参照对象为浏览器窗口，这个从我们滚动浏览器窗口的滚动条就可以看出。

### Flex布局

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

- justify-content 属性定义了项目在主轴 上的对齐方式。  它可能取5个值，具体对齐方式与轴的方向有关。下面假设主轴为从左到右。 

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

