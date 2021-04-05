### HTML

> 超文本标记语言，用来告知浏览器如何组织页面的标记语言。由一系列不同的标签元素组成的标记语言，由这些标签按照一定的规则嵌套而成的文件称为HTML文档（xxx.html）。它可以应用于文本片段，使文本在文档中具有不同的含义，通过标签将图片、音视频等内容嵌入到文档当中，还可以将文档结构化为不同的逻辑块。

#### HTML元素

元素的组成部分：

1. **开始标签**（Opening tag）：包含元素的名称，被左、右角括号所包围。表示元素从这里开始或者开始起作用 。

2. **结束标签**（Closing tag）：与开始标签相似，只是其在元素名之前包含了一个斜杠。这表示着元素的结尾。

3. **内容**（Content）：元素的内容，位于开始和结束标签之间。

4. **属性**（Attribute）：属性包含元素的额外信息，这些信息不会出现在实际的内容中。

   一个属性必须包含如下内容：

   1. 一个空格，在属性和元素名称之间。(如果已经有一个或多个属性，就与前一个属性之间有一个空格。)
   2. 属性名称，后面跟着一个等于号。
   3. 一个属性值，由一对引号“ ”引起来。**布尔属性没有属性值，它们的值只能与属性名一样**

5. **元素**（Element）：开始标签、结束标签与内容相结合，便是一个完整的元素。

#### HTML元素的类别

- 基本

  | Tag          | Description                                    |
  | :----------- | :--------------------------------------------- |
  | <!DOCTYPE>   | Defines the document type                      |
  | <html>       | Defines an HTML document                       |
  | <head>       | Contains metadata/information for the document |
  | <title>      | Defines a title for the document               |
  | <body>       | Defines the document's body                    |
  | <h1> to <h6> | Defines HTML headings                          |
  | <p>          | Defines a paragraph                            |
  | <br>         | Inserts a single line break                    |
  | <hr>         | Defines a thematic change in the content       |
  | <!--...-->   | Defines a comment                              |

- 格式化

- 表单和输入

  | Tag        | Description                                                |
  | :--------- | :--------------------------------------------------------- |
  | <from>     | Defines an HTML form for user input                        |
  | <input>    | Defines an input control                                   |
  | <textarea> | Defines a multiline input control (text area)              |
  | <button>   | Defines a clickable button                                 |
  | <select>   | Defines a drop-down list                                   |
  | <optgroup> | Defines a group of related options in a drop-down list     |
  | <option>   | Defines an option in a drop-down list                      |
  | <label>    | Defines a label for an <input> element                     |
  | <fieldset> | Groups related elements in a form                          |
  | <legend>   | Defines a caption for a <fieldset> element                 |
  | <datalist> | Specifies a list of pre-defined options for input controls |
  | <output>   | Defines the result of a calculation                        |

- 框架

  | Tag      | Description             |
  | :------- | :---------------------- |
  | <iframe> | Defines an inline frame |

- 图片

  | Tag          | Description                                                  |
  | :----------- | :----------------------------------------------------------- |
  | <img>        | Defines an image                                             |
  | <map>        | Defines a client-side image map                              |
  | <area>       | Defines an area inside an image map                          |
  | <canvas>     | Used to draw graphics, on the fly, via scripting (usually JavaScript) |
  | <figcaption> | Defines a caption for a <figure> element                     |
  | <figure>     | Specifies self-contained content                             |
  | <picture>    | Defines a container for multiple image resources             |
  | <svg>        | Defines a container for SVG graphics                         |

- 音视频

  | Tag      | Description                                                  |
  | :------- | :----------------------------------------------------------- |
  | <audio>  | Defines sound content                                        |
  | <source> | Defines multiple media resources for media elements (<video>, <audio> and <picture>) |
  | <track>  | Defines text tracks for media elements (<video> and <audio>) |
  | <video>  | Defines a video or movie                                     |

- 链接

  | Tag    | Description                                                  |
  | :----- | :----------------------------------------------------------- |
  | <a>    | Defines a hyperlink                                          |
  | <link> | Defines the relationship between a document and an external resource (most used to link to style sheets) |
  | <nav>  | Defines navigation links                                     |

- 列表

  | Tag  | Description                                                |
  | :--- | :--------------------------------------------------------- |
  | <ul> | Defines an unordered list                                  |
  | <ol> | Defines an ordered list                                    |
  | <li> | Defines a list item                                        |
  | <dl> | Defines a description list                                 |
  | <dt> | Defines a term/name in a description list                  |
  | <dd> | Defines a description of a term/name in a description list |

- 表格

  | Tag        | Description                                                  |
  | :--------- | :----------------------------------------------------------- |
  | <table>    | Defines a table                                              |
  | <caption>  | Defines a table caption                                      |
  | <th>       | Defines a header cell in a table                             |
  | <tr>       | Defines a row in a table                                     |
  | <td>       | Defines a cell in a table                                    |
  | <thead>    | Groups the header content in a table                         |
  | <tbody>    | Groups the body content in a table                           |
  | <tfoot>    | Groups the footer content in a table                         |
  | <col>      | Specifies column properties for each column within a <colgroup> element |
  | <colgroup> | Specifies a group of one or more columns in a table for formatting |

- 样式和语义化

  | Tag       | Description                                               |
  | :-------- | :-------------------------------------------------------- |
  | <style>   | Defines style information for a document                  |
  | <div>     | Defines a section in a document                           |
  | <span>    | Defines a section in a document                           |
  | <header>  | Defines a header for a document or section                |
  | <footer>  | Defines a footer for a document or section                |
  | <main>    | Specifies the main content of a document                  |
  | <section> | Defines a section in a document                           |
  | <article> | Defines an article                                        |
  | <aside>   | Defines content aside from the page content               |
  | <details> | Defines additional details that the user can view or hide |
  | <dialog>  | Defines a dialog box or window                            |
  | <summary> | Defines a visible heading for a <details> element         |
  | <data>    | Adds a machine-readable translation of a given content    |

- 元信息

  | Tag    | Description                                                  |
  | :----- | :----------------------------------------------------------- |
  | <head> | Defines information about the document                       |
  | <meta> | Defines metadata about an HTML document                      |
  | <base> | Specifies the base URL/target for all relative URLs in a document |

- 编程

  | Tag        | Description                                                  |
  | :--------- | :----------------------------------------------------------- |
  | <script>   | Defines a client-side script                                 |
  | <noscript> | Defines an alternate content for users that do not support client-side scripts |
  | <embed>    | Defines a container for an external (non-HTML) application   |
  | <object>   | Defines an embedded object                                   |
  | <param>    | Defines a parameter for an object                            |

#### HTML文档

单独的HTML元素是没有意义的。现在我们来学习这些特定元素是怎么被结合起来，从而形成一个完整的HTML页面的：

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>我的测试站点</title>
  </head>
  <body>
    <p>这是我的页面</p>
  </body>
</html>
```

分析如下:

1. `<!DOCTYPE html>`: 声明文档类型. 很久以前，早期的HTML(大约1991年2月)，文档类型声明类似于链接，规定了HTML页面必须遵从的良好规则，能自动检测错误和其他有用的东西。使用如下：

   ```html
   <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
   ```

   然而这种写法已经过时了，这些内容已成为历史。只需要知道`<!DOCTYPE html>`是最短有效的文档声明。

2. `<html></html>`: `<html>`元素。这个元素包裹了整个完整的页面，是一个根元素。

3. `<head></head>`: `<head>`元素. 这个元素是一个容器，它包含了所有你想包含在HTML页面中但不想在HTML页面中显示的内容。这些内容包括你想在搜索结果中出现的关键字和页面描述，CSS样式，字符集声明等等。以后的章节能学到更多关于<head>元素的内容。

4. `<meat charset="utf-8">`: 这个元素设置文档使用utf-8字符集编码，utf-8字符集包含了人类大部分的文字。基本上他能识别你放上去的所有文本内容。毫无疑问要使用它，并且它能在以后避免很多其他问题。

5. `<title></title>`: 设置页面标题，出现在浏览器标签上，当你标记/收藏页面时它可用来描述页面。

6. `<body></body>`: `<body>`元素。 包含了你访问页面时所有显示在页面上的内容，文本，图片，音频，游戏等等。