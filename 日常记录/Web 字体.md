​		字体本质上是编码字符集和图形之间的映射关系，一种字体就是一种映射关系。

## 基本概念

字体指的是字型家族（font-family），也称字族，一个字族包含多个字型，字型之间以粗细、风格等来区分。
通用字型家族（generic font family）指的是一个大类的字体，也称字体族，至于最终会被解析成哪个字体，则是取决于浏览器和操作系统的设定。常见的字体族有如下几种：
● serif：衬线字体，笔画结尾有特殊的装饰线或衬线。 
● sans-serif：无衬线字体，即笔画结尾是平滑的字体。
● monospace：等宽字体，即字体中每个字宽度相同
● cursive：手写字体，这种字体有的有连笔，有的还有特殊的斜体效果，给人一种手写的感觉。
● fantasy：奇幻字体，具有特殊艺术效果的字体。
● system-ui：系统UI字体，从浏览器所处系统获取的默认用户界面字体。



## 字体来源

● 操作系统的本地字体库
● 通过 @font-face  加载的网络字体



## 字体生效规则

浏览器在决定将元素中的字符渲染为何种字形时，是逐字符进行的，并遵循如下规则：

1. 若 font-family 属性的计算值为 initial，则使用浏览器的默认字体，否则优先使用元素 font-family 属性指定的字体。font-family 属性可以指定单个字体名或字体族名，也可以指定一个由字体名或者字体族名组成的可选字体列表。字体名或字体族名之间由逗号分隔，优先级按照从左到右的顺序，由高到低。
2. 浏览器会按照优先级规则，选择列表中第一个当前计算机上有安装，或者是通过 @font-face 指定的可以直接下载的字体。
3. 若找到可用字体，则查找字体中是否包含当前要呈现字符的字形，若有，则将字符渲染为该字形；若无，则当前字体无效，继续寻找选择列表中下一个可用字体。
4. 若可选字体列表中指定的字体都无法应用成功，则使用浏览器的默认字体，默认字体由操作系统和浏览器共同决定（不同浏览器之间不统一，同一浏览器在不同操作系统下不一致）。

font-family 值确定规则
1. 如果 CSS 级联产生了一个值，则使用该值。
2. 否则，则使用父元素的计算值（ computed value）。 
3. 若属性值最终为 initial，则 font-family 的值为默认值，该值由操作系统和浏览器共同决定。 

![img](https://intranetproxy.alipay.com/skylark/lark/0/2022/jpeg/24056888/1661788334149-ffdfd468-5cb1-4053-a493-181f75e9f3e1.jpeg)



## 字体设置方案

需要考虑的因素：
● 操作系统：不同操作系统下，计算机的本地字体库中所保存的字体不同
● 浏览器：不同浏览器对字体相关的 css 属性解析不一致
● 国家/地区：在不同国家或地区，浏览器的字体相关的默认设置会不同
● 一致的视觉表现 or 个性化：对网站的文字呈现效果的期望
原则：
● 充分考虑兼容性
● 保证最终实际使用的字体在控制的范围内



### font-family

> 通过为 font-family 属性指定可选字体列表的方式，在列表中列出不同系统环境下优先使用的本地字体。

​		指定优先选用的字体，并在可选字体列表末尾添加通用的字体族名，这样使得浏览器既可以在特定系统环境下选用指定的字体，又可以在无法使用指定字体的情况下，使用一个相对接近的备选字体。

```css
font-family: <各系统下指定的优先字体名>..., <指定字体所属的字体族名>;
```

### @font-face

> 通过 @font-face 引入网络字体，不受本地字体库的限制。

```css
@font-face {
  font-family: <自定义字体或字体集的变量名>;
  src: url('url.eot');
  src: local(''),
       url('url.woff2') format('woff2'),
       url('url.woff') format('woff'),
       url('url.ttf');
}
```



### 最终方案

|                | **Mac**                          | **Window**           |
| -------------- | -------------------------------- | -------------------- |
| **字母、数字** | Helvetica Neue, Helvetica,Roboto | Tahoma, Arial,Roboto |
| **汉语**       | PingFang SC                      | Microsoft YaHei      |

```css
@font-face {
  font-family: Roboto;
  src: url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-thin.eot);
  src: local(''),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-thin.woff2) format("woff2"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-thin.woff) format("woff"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-thin.ttf);
  font-weight: 200;
  font-display: swap
}

@font-face {
  font-family: Roboto;
  src: url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-light.eot);
  src: local(''),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-light.woff2) format("woff2"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-light.woff) format("woff"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-light.ttf);
  font-weight: 300;
  font-display: swap
}

@font-face {
  font-family: Roboto;
  src: url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-regular.eot);
  src: local(''),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-regular.woff2) format("woff2"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-regular.woff) format("woff"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-regular.ttf);
  font-weight: 400;
  font-display: swap
}

@font-face {
  font-family: Roboto;
  src: url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-medium.eot);
  src: local(''),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-medium.woff2) format("woff2"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-medium.woff) format("woff"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-medium.ttf);
  font-weight: 500;
  font-display: swap
}

@font-face {
  font-family: Roboto;
  src: url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-bold.eot);
  src: local(''),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-bold.woff2) format("woff2"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-bold.woff) format("woff"),
       url(//i.alicdn.com/artascope-font/20160419204543/font/roboto-bold.ttf);
  font-weight: 700;
  font-display: swap
}

font-family: Roboto, Helvetica Neue, Helvetica,Tahoma, Arial, PingFang SC, Microsoft YaHei, sans-serif;
```

### 实践说明

​		为各 Solution 或 One Bp 入口祖先元素设置 font-family 值（这里不确定需不需要写入 @font-face，因为 ASC 已经引入了 Roboto 字体，在这里写入可能会显得多余）。

```css
font-family: Roboto, Helvetica Neue, Helvetica,Tahoma, Arial, PingFang SC, Microsoft YaHei, sans-serif;
```

​		根据 CSS 继承规则，后续子元素中无需再设置 font-family（除非需要使用上述 font-family 设置中没有的字体），仅设置字重便可使用相应地字体，如：
​		使用 Roboto-Bold 字体

```css
font-weight: 700;
```

​		使用 Roboto-Medium 字体
```css
font-weight: 500;
```

​		使用 Roboto-Regular 字体
```css
font-weight: 400;
```

​		使用 Roboto-Light 字体
```css
font-weight: 300;
```

​		使用 Roboto-Thin 字体
```css
font-weight: 200;
```

