## 诞生背景

> 为了构建web，实现文档的共享，需要一个用于传递文档的协议。

## 使用场景

> HTTP 协议和 TCP/ IP 协议族内的其他众多的协议相同，用于客户端和服务器之间的通信。
>

## HTTP报文

> 用于 HTTP 协议交互的信息被称为 HTTP 报文。 请求端（ 客户端）的HTTP报文叫做请求报文，响应端（ 服务器端）的叫做响应报文。
>
> HTTP 报文本身是由多行（ 用 CR+ LF 作 换行符） 数据构成的字符串文本。
>

### 报文结构

> HTTP 报文大致可分为报文首部和报文主体两块。 两者由最初出现的空行（ CR+ LF） 来划分。通常，并不一定要有报文主体。
>

<img src=".\HTTP\request_message_structure.png" style="zoom:50%;" />

<img src=".\HTTP\response_message_structure.png" style="zoom:50%;" />

请求行：包含用于请求的方法，请求URI和HTTP版本。

状态行：包含表明响应结果的状态码，原因短语和HTTP版本。



### 报文主体与实体主体的差异

+ 报文

  是 HTTP 通信中的基本单位， 由 8 位组字节流（ octet sequence， 其中 octet 为 8 个 比特） 组成， 通过 HTTP 通信传输

+ 实体

  作为请求或响应的有效载荷数据（ 补充项）被传输，其内容由**实体首部**和**实体主体**组成。

HTTP 报文的**主体**用于**传输** 请求 或 响应 的 **实体主体**。 通常， 报文主体等于实体主体。只有当传输中进行编码操作时，实体主体的内容发生变化，才导致它和报文主体产生差异。



## 状态码

> HTTP 状态码负责表示客户端 HTTP 请求的返回结果、 标记服务器端的处理是否正常、 通知出现的错误等工作。

+ 2XX成功：2XX 的响应结果表明请求被正常处理了

  + 200（OK）：请求处理成功

  + 204（No Content）：请求处理成功，但没有资源可以返回
  + 206 （Partial Content）：该状态码表示客户端进行了范围请求， 而服务器成功执行了这部分的GET请求。 响应报文中包含由Content- Range指定范围的实体内容

+ 3XX重定向：表明浏览器需要执行某些特殊的处理以正确处理请求
  + 301（Moved Permanently）：永久性重定向
  + 302（Found）：临时性重定向
  + 303（See Other）：该状态码表示由于请求对应的资源存在着另一个URI，应使用GET方法定向获取请求的资源
  + 304（Not Modified）：该状态码表示客户端发送附带条件的请求（GET方法的请求报文中包含If-Match，If-Modified-Since，If-None-Match，If-Range，If-Unmodified-Since中任一首部）时，服务器端允许请求访问资源，但因请求未满足条件，直接返回304（服务器端资源未改变，可直接使用客户端未过期的缓存）

+ 4XX客户端错误：表明客户端是发生错误的原因所在
  + 400（Bad Request）：该状态码表示请求报文中存在语法错误
  + 401（Unauthorized）：表示发送的请求需要有通过HTTP认证（BASIC认证、DIGEST认证）的认证信息。返回含有401的响应必须包含一个适用于被请求资源的`WWW-Authenticate`首部用以质询用户信息
  + 403（Forbidden）：该状态码表明对请求资源的访问被服务器拒绝了
  + 404（Not Found）：该状态码表明服务器上无法找到请求的资源
+ 5XX服务器错误：表明服务器本身发生错误
  + 500（Internal Server Error）：该状态码表明服务器端在执行请求时发生了错误
  + 503（Service Unavailable）：该状态码表明服务器暂时处于超负载或正在进行停机维护，现在无法处理请求



## HTTP首部

> 首部内容为客户端和服务器分别处理请求和响应提供所需要的信息。
>

+ 通用首部字段

  > 请求报文和响应报文都会使用的首部

  | 首部字段名        | 说明                       |
  | ----------------- | -------------------------- |
  | Cache-Control     | 控制缓存的行为             |
  | Connection        | 逐跳首部、连接的管理       |
  | Date              | 创建报文的日期时间         |
  | Pragma            | 报文指令                   |
  | Trailer           | 报文末端的首部一览         |
  | Transfer-Encoding | 指定报文主体的传输编码方式 |
  | Upgrade           | 升级为其他协议             |
  | Via               | 代理服务器的相关信息       |
  | Warning           | 错误通知                   |

+ 请求首部字段

  > 只在请求报文中使用的首部

  | 首部字段名          | 说明                                          |
  | ------------------- | --------------------------------------------- |
  | Accept              | 用户代理可处理的媒体类型                      |
  | Accept-Charset      | 优先的字符集                                  |
  | Accept-Encoding     | 优先的内容编码                                |
  | Accept-Language     | 优先的语言（自然语言）                        |
  | Authorization       | Web认证信息                                   |
  | Expect              | 期待服务器的特定行为                          |
  | From                | 用户的电子邮箱地址                            |
  | Host                | 请求资源所在的服务器                          |
  | If-Match            | 比较实体标记（ETag）                          |
  | If-Modified-Since   | 比较资源的更新时间                            |
  | If-None-Match       | 比较实体标记（与If-Match相反）                |
  | If-Range            | 资源未更新时发送实体Byte的范围请求            |
  | If-Unmodified-Since | 比较资源的更新时间（与If-Modified-Since相反） |
  | Max-Forwards        | 最大传输逐级跳                                |
  | Proxy-Authorization | 代理服务器要求客户端的认证信息                |
  | Range               | 实体的字节范围请求                            |
  | Referer             | 对请求中URI的原始获取方                       |
  | TE                  | 传输编码的优先级                              |
  | User-Agent          | HTTP客户端程序的信息                          |

+ 响应首部字段

  > 只在响应报文中使用的首部

  | 首部字段名         | 说明                         |
  | ------------------ | ---------------------------- |
  | Accept-Ranges      | 是否接受字节范围请求         |
  | Age                | 推算资源创建经过时间         |
  | ETag               | 资源的匹配信息               |
  | Location           | 令客户端重定向至指定URI      |
  | Proxy-Authenticate | 代理服务器对客户端的认证信息 |
  | Retry-After        | 对再次发起请求的时机要求     |
  | Server             | HTTP服务器的安装信息         |
  | Vary               | 代理服务器缓存的管理信息     |
  | WWW-Authenticate   | 服务器对客户端的认证信息     |

+ 实体首部字段

  > 针对请求报文和响应报文的实体部分使用的首部

  | 首部字段名       | 说明                         |
  | ---------------- | ---------------------------- |
  | Allow            | 资源可支持的HTTP方法         |
  | Content-Encoding | 实体主体适用的编码方式       |
  | Content-Language | 实体主体的自然语言           |
  | Content-Length   | 实体主体的大小（单位：字节） |
  | Content-Location | 替代对应资源的URI            |
  | Content-MD5      | 实体主体的报文摘要           |
  | Content-Range    | 实体主体的位置范围           |
  | Content-Type     | 实体主体的媒体类型           |
  | Expires          | 实体主体过期的日期时间       |
  | Last-Modified    | 资源的最后修改日期时间       |

+ 为Cookie服务的首部字段

  | 首部字段名 | 说明                           | 首部类型     |
  | ---------- | ------------------------------ | ------------ |
  | Set-Cookie | 开始状态管理所使用的Cookie信息 | 响应首部字段 |
  | Cookie     | 服务器接收到的Cookie信息       | 请求首部字段 |

  Set-Cookie字段的属性

  | 属性         | 说明                                                         |
  | ------------ | ------------------------------------------------------------ |
  | NAME=VALUE   | 赋予Cookie的名称和其值（必需项）                             |
  | expires=DATE | Cookie的有效期（若不明确指定则默认为浏览器关闭前为止）       |
  | path=PATH    | 将服务器上的文件目录作为Cookie的适用对象（若不指定则默认为文档所在的文件目录） |
  | domain=域名  | 作为Cookie适用对象的域名（若不指定则默认为创建Cookie的服务器的域名） |
  | Secure       | 仅在HTTPS安全通信时才会发送Cookie                            |
  | HttpOnly     | 加以限制，使Cookie不能被JavaScript脚本访问                   |

![](.\HTTP\cookie_request.png)

HTTP 首部字段将定义成缓存代理和非缓存代理的行为，分成 2 种类型。

+ 端到端首部（End-to-End Header）

  分在此类别中的首部会转发给请求 / 响应对应的最终接收目标，且必须 保存在由缓存生成的响应中，另外规定它必须被转发。

+ 逐跳首部（Hop-by-hop Header）

  分在此类别中的首部只对单次转发有效，会因通过缓存或代理而不再转发。HTTP/ 1. 1和之后版本中，如果要使用 hop- by- hop 首部，需提供 Connection 首部字段。除这 8 个首部字段之外，其他所有字段都属于端到端首部。

  + Connection 
  + Keep- Alive 
  + Proxy- Authenticate 
  + Proxy- Authorization
  + Trailer
  + TE 
  + Transfer- Encoding 
  + Upgrade



## WebSocket

> WebSocket，即 Web 浏览器与 Web 服务器之间全双工通信标准。
>

### 出现的背景

> HTTP 协议做不到服务器主动向客户端推送信息。

### 简介

<img src=".\HTTP\http_vs_websocket.png" style="zoom: 67%;" />

一旦Web服务器与客户端之间建立起 WebSocket 协议的通信连接，之后所有的通信都依靠这个专用协议进行。通信过程中可互相发送 JSON、XML、 HTML 或图片等任意格式的数据。

WebSocket协议的主要特点：

+ 可以发送二进制数据。

+ 没有同源限制，客户端可以与任意服务器通信。

+ 推送功能

  支持由服务器向客户端推送数据的推送功能。这样，服务器可直接发送数据，而不必等待客户端的请求。

+ 减少通信量

  只要建立起WebSocket连接，就会一直保持连接状态，除非主动断开。

  和HTTP相比，每次连接时的总开销减少，而且由于WebSocket的首部信息很小，通信量也相应减少了。

  为了实现 WebSocket 通信， 在 HTTP 连接建立之后，需要完成一次“ 握手”（ Handshaking）的步骤。

  + 握手请求

    为了实现WebSocket通信，需要用到 HTTP 的Upgrade 首部字段，告知服务器通信协议发生改变， 以达到握手的目的

  + 握手响应

    对于之前的请求，返回状态码 101 Switching Protocols 的响应


成功握手确立 WebSocket 连接之后，通信时不再使用 HTTP 的数据帧，而 采用 WebSocket 独立的数据帧。

<img src=".\HTTP\WebSocket通信.png" style="zoom: 67%;" />



## AJAX

`Ajax`的全称是`Asynchronous JavaScript and XML`。在没有`Ajax`之前，前端想要向请求后端的数据，可以使用的方式有：

- `form` 表单请求 『缺点：页面会刷新』
- `img` 通过 img 标签，向服务器发送请求 『缺点：只能发送GET,页面没有刷新，只能请求图片』
- `script` 标签请求，传递回调函数给后台，后台把数据放入回调函数中，当作参数，执行。『缺点：只能发送`GET`请求』（这就是`jsonp`）
- ...

以上这些方式要么需要刷新页面，要么只能发送`get`请求。做不到既可以发送除`GET`以外的请求，并且不刷新页面的效果。而`Ajax`就是为了解决这么一个问题出现的，说白了`Ajax`就是让`JavaScript`可以发送`HTTP`请求和接收`HTTP`响应。



## HTTP/1.x 的缺陷

- **连接无法复用**：连接无法复用会导致每次请求都经历三次握手和慢启动。三次握手在高延迟的场景下影响较明显，慢启动则对大量小文件请求影响较大（没有达到最大窗口请求就被终止）。

  - HTTP/1.0 传输数据时，每次都需要重新建立连接，增加延迟。
  - HTTP/1.1 虽然加入 keep-alive 可以复用一部分连接，但域名分片等情况下仍然需要建立多个connection，耗费资源，给服务器带来性能压力。

- **Head-Of-Line Blocking（HOLB）**：导致带宽无法被充分利用，以及后续健康请求被阻塞。[HOLB](http://stackoverflow.com/questions/25221954/spdy-head-of-line-blocking)是指一列的第一个数据包（package）被阻塞而导致整列数据包受阻；当页面中需要请求很多资源的时候，HOLB（队头阻塞）会导致在达到最大请求数量时，剩余的资源需要等待其他资源请求完成后才能发起请求。

  - HTTP 1.0：下个请求必须在前一个请求返回后才能发出，`request-response`对按序发生。显然，如果某个请求长时间没有返回，那么接下来的请求就全部阻塞了。
  - HTTP 1.1：尝试使用 pipelining 来解决，即浏览器可以一次性发出多个请求（同个域名，同一条 TCP 链接）。但 pipelining 要求返回是按序的，那么前一个请求如果很耗时（比如处理大图片），那么后面的请求即使服务器已经处理完，仍会等待前面的请求处理完才开始按序返回。所以，pipelining 只部分解决了 HOLB。

  ![](D:\Notes\CS\计算机网络\HTTP\pipeline.webp)

- 无法实现多路复用：HTTP1.x是基于文本的协议，很难像HTTP2那样对请求/响应消息进行拆分，只能以消息为单位发送，而且由于没有“流”的概念，请求和响应消息在乱序发送后无法进行匹配，因此无法交错的发送请求或响应消息，“请求-响应”对只能按序发生。



## HTTP2.0

> 2015 年，HTTP/2 发布。HTTP/2 是现行 HTTP 协议（HTTP/1.x）的替代，但它不是重写，HTTP 方法/状态码/语义都与 HTTP/1.x 一样。HTTP/2 基于 SPDY3，专注于**性能**，最大的一个目标是在用户和网站间只用一个连接（connection）。

### 二进制传输

HTTP/2 采用二进制格式传输数据，而非 HTTP 1.x 的文本格式，二进制协议解析起来更高效。 HTTP / 1 的请求和响应报文，都是由起始行，首部和实体正文（可选）组成，各部分之间以文本换行符分隔。**HTTP/2 将请求和响应数据分割为更小的帧，并且它们采用二进制编码**。

几个重要的概念：

- 流：流是连接中的一个**虚拟信道**，可以承载双向的消息；每个流都有一个唯一的整数标识符（1、2…N）
- 消息：是指逻辑上的 HTTP 消息，比如请求、响应等，由一或多个帧组成
- 帧：HTTP 2.0 通信的**最小单位**，每个帧包含帧首部，至少也会标识出当前帧所属的流，承载着特定类型的数据，如 HTTP 首部、负荷，等等

<img src=".\HTTP\二进制帧.webp" style="zoom:50%;" />

规范中一共定义了10种不同的帧，每种帧都有如下公共字段：Type, Length, Flags, Stream Identifier和frame payload 。

流既可以被客户端/服务器端单方面的建立和使用，也可以被双方共享，或者被任意一边关闭。**`流`代表了一个完整的`请求-响应`数据交互过程**。

<img src=".\HTTP\HTTP2流.png" style="zoom:67%;" />

HTTP/2 中，同域名下所有通信都在单个连接上完成，该连接可以承载任意数量的双向数据流。每个数据流都以消息的形式发送，而消息又由一个或多个帧组成。多个帧之间可以乱序发送，根据帧首部的流标识可以重新组装。



### 多路复用（基于帧和流实现）

在 HTTP/2 中，有了二进制分帧之后，HTTP /2 不再依赖 TCP 链接去实现多流并行了，在 HTTP/2 中：

- 同域名下所有通信都在单个连接上完成。
- 单个连接可以承载任意数量的双向数据流。
- 数据流以消息（请求和响应）的形式发送，而消息又由一个或多个帧组成，多个帧之间可以乱序发送（**`request-response`对不用按序发生**），因为根据帧首部的流标识可以重新组装。

这一特性，使性能有了极大提升：

- 同个域名只需要占用一个 TCP 连接，使用一个连接并行发送多个请求和响应,消除了因多个 TCP 连接而带来的延时和内存消耗。
- **并行交错地发送多个请求，请求之间互不影响**。
- **并行交错地发送多个响应，响应之间互不干扰**。
- 在 HTTP/2 中，每个请求都可以带一个 31bit 的优先值，0 表示最高优先级， 数值越大优先级越低。有了这个优先值，客户端和服务器就可以在处理不同的流时采取不同的策略，以最优的方式发送流、消息和帧。

<img src=".\HTTP\多路复用.png" style="zoom:67%;" />

### 头部压缩

在 HTTP/1 中，我们使用文本的形式传输 header，在 header 携带 cookie 的情况下，可能每次都需要重复传输几百到几千的字节。

为了减少这块的资源消耗并提升性能， HTTP/2 对这些首部采取了压缩策略：

- HTTP/2 在客户端和服务器端使用“首部表”来跟踪和存储之前发送的键－值对，对于相同的数据，不再通过每次请求和响应发送；
- 首部表在 HTTP/2 的连接存续期内始终存在，由客户端和服务器共同渐进地更新;
- 每个新的首部键－值对要么被追加到当前表的末尾，要么替换表中之前的值

例如下图中的两个请求， 请求一发送了所有的头部字段，第二个请求则只需要发送差异数据，这样可以减少冗余数据，降低开销

<img src=".\HTTP\头部压缩.png" style="zoom:67%;" />

### 服务器端推送

Server Push 即服务端能通过 push 的方式将客户端需要的内容预先推送过去，也叫“cache push”。

可以想象以下情况，某些资源客户端是一定会请求的，这时就可以采取服务端 push 的技术，提前给客户端推送必要的资源，这样就可以相对减少一点延迟时间。当然在浏览器兼容的情况下你也可以使用 prefetch。
例如服务端可以主动把 JS 和 CSS 文件推送给客户端，而不需要客户端解析 HTML 时再发送这些请求。

<img src=".\HTTP\服务端推送.png" style="zoom:67%;" />

服务端可以主动推送，客户端也有权利选择是否接收。如果服务端推送的资源已经被浏览器缓存过，浏览器可以通过发送 RST_STREAM 帧来拒收。主动推送也遵守同源策略，换句话说，服务器不能随便将第三方资源推送给客户端，而必须是经过双方确认才行。



## HTTP1.0、HTTP1.1与HTTP2.0的比较

|            | 1.0                                                 | 1.1      | 2.0                                                          |
| ---------- | --------------------------------------------------- | -------- | ------------------------------------------------------------ |
| 长连接     | 需要使用`keep-alive` 参数来告知服务端建立一个长连接 | 默认支持 | 默认支持                                                     |
| HOST域     | ✘                                                   | ✔️        | ✔️                                                            |
| 多路复用   | ✘                                                   | -        | ✔️                                                            |
| 数据压缩   | ✘                                                   | ✘        | 使用`HAPCK`算法对header数据进行压缩，使数据体积变小，传输更快 |
| 服务器推送 | ✘                                                   | ✘        | ✔️                                                            |



## HTTPS



## TCP三次握手，四次挥手

https://zhuanlan.zhihu.com/p/53374516



## 浏览器同源政策

### 含义

> **同源策略**是一个浏览器采用的安全策略，它用于限制不同源的资源之间的交互

同源定义：

- 协议相同
- 域名相同
- 端口相同



### 目的

> 同源政策的目的，是为了保证用户信息的安全，防止恶意的网站窃取数据。



### 限制范围

如果非同源，共有三种行为（DOM、Web数据和网络）受到限制。

> （1） Cookie、LocalStorage 和 IndexDB 无法读取。
>
> （2） DOM 无法获得。
>
> （3） AJAX 请求不能发送。



### 规避方法

#### Cookie

Cookie 是服务器写入浏览器的一小段信息，**只有同源的网页才能共享**。但是，两个网页一级域名相同，只是二级域名不同，浏览器允许通过设置`document.domain`共享 Cookie。

举例来说，A网页是`http://w1.example.com/a.html`，B网页是`http://w2.example.com/b.html`，那么只要设置相同的`document.domain`，两个网页就可以共享Cookie。

> ```javascript
> document.domain = 'example.com';
> ```

现在，A网页通过脚本设置一个 Cookie。

> ```javascript
> document.cookie = "test1=hello";
> ```

B网页就可以读到这个 Cookie。

> ```javascript
> var allCookie = document.cookie;
> ```

注意，这种方法只适用于 Cookie 和 iframe 窗口

#### DOM、LocalStorage 和 IndexDB

HTML5为了解决这个问题，引入了一个全新的API：跨文档通信 API（Cross-document messaging）。

这个API为`window`对象新增了一个`window.postMessage`方法，允许跨窗口通信，不论这两个窗口是否同源。

举例来说，父窗口`http://aaa.com`向子窗口`http://bbb.com`发消息，调用`postMessage`方法就可以了。

> ```javascript
> var popup = window.open('http://bbb.com', 'title');
> popup.postMessage('Hello World!', 'http://bbb.com');
> ```

`postMessage`方法的第一个参数是具体的信息内容，第二个参数是接收消息的窗口的源（origin），即"协议 + 域名 + 端口"。也可以设为`*`，表示不限制域名，向所有窗口发送。

子窗口向父窗口发送消息的写法类似。

> ```javascript
> window.opener.postMessage('Nice to see you', 'http://aaa.com');
> ```

父窗口和子窗口都可以通过`message`事件，监听对方的消息。

> ```javascript
> window.addEventListener('message', function(e) {
>   console.log(e.data);
> },false);
> ```

`message`事件的事件对象`event`，提供以下三个属性。

> - `event.source`：发送消息的窗口
> - `event.origin`：消息发向的网址
> - `event.data`：消息内容

下面的例子是，子窗口通过`event.source`属性引用父窗口，然后发送消息。

> ```javascript
> window.addEventListener('message', receiveMessage);
> function receiveMessage(event) {
>   event.source.postMessage('Nice to see you!', '*');
> }
> ```

`event.origin`属性可以过滤不是发给本窗口的消息。

> ```javascript
> window.addEventListener('message', receiveMessage);
> function receiveMessage(event) {
>   if (event.origin !== 'http://aaa.com') return;
>   if (event.data === 'Hello World') {
>       event.source.postMessage('Hello', event.origin);
>   } else {
>     console.log(event.data);
>   }
> }
> ```



#### AJAX

同源政策规定，AJAX请求只能发给同源的网址，否则就报错。

除了架设服务器代理（浏览器请求同源服务器，再由后者请求外部服务），有三种方法规避这个限制。

> - JSONP
> - WebSocket
> - CORS

##### JSONP

> JSONP是资料格式JSON的一种“使用模式”，可以让网页从别的网域获取资料

JSONP是服务器与客户端跨源通信的常用方法。最大特点就是简单适用，老式浏览器全部支持，服务器改造非常小。

它的基本思想是，网页通过添加一个`<script>`元素，向服务器请求JSON数据，这种做法不受同源政策限制；服务器收到请求后，将数据放在一个指定名字的回调函数里传回来。

首先，网页动态插入`<script>`元素，由它向跨源网址发出请求。

> ```javascript
> function addScriptTag(src) {
>   var script = document.createElement('script');
>   script.setAttribute("type","text/javascript");
>   script.src = src;
>   document.body.appendChild(script);
> }
> 
> window.onload = function () {
>   addScriptTag('http://example.com/ip?callback=foo');
> }
> 
> function foo(data) {
>   console.log('Your public IP address is: ' + data.ip);
> };
> ```

上面代码通过动态添加`<script>`元素，向服务器`example.com`发出请求。注意，该请求的查询字符串有一个`callback`参数，用来指定回调函数的名字，这对于JSONP是必需的。

服务器收到这个请求以后，会将数据放在回调函数的参数位置返回。

> ```javascript
> foo({
>   "ip": "8.8.8.8"
> });
> ```

由于`<script>`元素请求的脚本，直接作为代码运行。这时，只要浏览器定义了`foo`函数，该函数就会立即调用。作为参数的JSON数据被视为JavaScript对象，而不是字符串，因此避免了使用`JSON.parse`的步骤。

##### websocket

WebSocket是一种通信协议，使用`ws://`（非加密）和`wss://`（加密）作为协议前缀。该协议不实行同源政策，只要服务器支持，就可以通过它进行跨源通信。

下面是一个例子，浏览器发出的WebSocket请求的头信息。

> ```http
> GET /chat HTTP/1.1
> Host: server.example.com
> Upgrade: websocket
> Connection: Upgrade
> Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
> Sec-WebSocket-Protocol: chat, superchat
> Sec-WebSocket-Version: 13
> Origin: http://example.com
> ```

上面代码中，有一个字段是`Origin`，表示该请求的请求源（origin），即发自哪个域名。

正是因为有了`Origin`这个字段，所以WebSocket才没有实行同源政策。因为服务器可以根据这个字段，判断是否许可本次通信。如果该域名在白名单内，服务器就会做出如下回应。

> ```http
> HTTP/1.1 101 Switching Protocols
> Upgrade: websocket
> Connection: Upgrade
> Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
> Sec-WebSocket-Protocol: chat
> ```

##### CORS

> **跨域资源共享**定义了浏览器和服务器如何实现跨源通信。CORS背后的基本思路就是**使用自定义的HTTP头部允许浏览器和服务器相互了解，以确实请求或响应应该成功还是失败**

CORS是跨源资源分享（Cross-Origin Resource Sharing）的缩写。它是W3C标准，是跨源AJAX请求的根本解决方法。相比JSONP只能发`GET`请求，CORS允许任何类型的请求。

###### 简介

CORS需要浏览器和服务器同时支持。目前，所有浏览器都支持该功能，IE浏览器不能低于IE10。

整个CORS通信过程，都是浏览器自动完成，不需要用户参与。对于开发者来说，CORS通信与同源的AJAX通信没有差别，代码完全一样。浏览器一旦发现AJAX请求跨源，就会自动添加一些附加的头信息，有时还会多出一次附加的请求，但用户不会有感觉。

因此，实现CORS通信的关键是服务器。只要服务器实现了CORS接口，就可以跨源通信。

###### 两种请求

浏览器将CORS请求分成两类：简单请求（simple request）和非简单请求（not-so-simple request）。

只要同时满足以下两大条件，就属于简单请求。

```markdown
（1) 请求方法是以下三种方法之一：
- HEAD
- GET
- POST

（2）HTTP的头信息不超出以下几种字段：
- Accept
- Accept-Language
- Content-Language
- Content-Type：只限于三个值`application/x-www-form-urlencoded`、`multipart/form-data`、`text/plain`
- DPR
- Downlink
- Save-Data
- Viewport-Width
- Width
```

凡是不同时满足上面两个条件，就属于非简单请求。

**简单请求**

对于**简单请求**，浏览器**直接发出CORS请求**。具体来说，就是在头信息之中，**增加一个`Origin`字段**。

下面是一个例子，浏览器发现这次跨源AJAX请求是简单请求，就自动在头信息之中，添加一个`Origin`字段。

> ```http
> GET /cors HTTP/1.1
> Origin: http://api.bob.com
> Host: api.alice.com
> Accept-Language: en-US
> Connection: keep-alive
> User-Agent: Mozilla/5.0...
> ```

上面的头信息中，`Origin`字段用来说明，本次请求来自哪个源（协议 + 域名 + 端口）。服务器根据这个值，决定是否同意这次请求。

如果`Origin`指定的源，不在许可范围内，服务器会返回一个正常的HTTP回应。浏览器发现，这个回应的头信息没有包含`Access-Control-Allow-Origin`字段（详见下文），就知道出错了，从而抛出一个错误，被`XMLHttpRequest`的`onerror`回调函数捕获。注意，这种错误无法通过状态码识别，因为HTTP回应的状态码有可能是200。

如果`Origin`指定的域名在许可范围内，服务器返回的响应，会多出几个头信息字段。

> ```http
> Access-Control-Allow-Origin: http://api.bob.com
> Access-Control-Allow-Credentials: true
> Access-Control-Expose-Headers: FooBar
> Content-Type: text/html; charset=utf-8
> ```

上面的头信息之中，有三个与CORS请求相关的字段，都以`Access-Control-`开头。

**非简单请求**

非简单请求的CORS请求，会在正式通信之前，增加一次HTTP查询请求，称为"预检"请求（preflight）。

浏览器先询问服务器，当前网页所在的域名是否在服务器的许可名单之中，以及可以使用哪些HTTP动词和头信息字段。只有得到肯定答复，浏览器才会发出正式的`XMLHttpRequest`请求，否则就报错。

下面是一段浏览器的JavaScript脚本。

> ```javascript
> var url = 'http://api.alice.com/cors';
> var xhr = new XMLHttpRequest();
> xhr.open('PUT', url, true);
> xhr.setRequestHeader('X-Custom-Header', 'value');
> xhr.send();
> ```

上面代码中，HTTP请求的方法是`PUT`，并且发送一个自定义头信息`X-Custom-Header`。

浏览器发现，这是一个非简单请求，就自动发出一个"预检"请求，要求服务器确认可以这样请求。下面是这个"预检"请求的HTTP头信息。

> ```http
> OPTIONS /cors HTTP/1.1
> Origin: http://api.bob.com
> Access-Control-Request-Method: PUT
> Access-Control-Request-Headers: X-Custom-Header
> Host: api.alice.com
> Accept-Language: en-US
> Connection: keep-alive
> User-Agent: Mozilla/5.0...
> ```

"预检"请求用的请求方法是`OPTIONS`，表示这个请求是用来询问的。头信息里面，关键字段是`Origin`，表示请求来自哪个源。

除了`Origin`字段，"预检"请求的头信息包括两个特殊字段。

**（1）Access-Control-Request-Method**

该字段是必须的，用来列出浏览器的CORS请求会用到哪些HTTP方法，上例是`PUT`。

**（2）Access-Control-Request-Headers**

该字段是一个逗号分隔的字符串，指定浏览器CORS请求会额外发送的头信息字段，上例是`X-Custom-Header`。

**预检请求的回应**

服务器收到"预检"请求以后，检查了`Origin`、`Access-Control-Request-Method`和`Access-Control-Request-Headers`字段以后，确认允许跨源请求，就可以做出回应。

> ```http
> HTTP/1.1 200 OK
> Date: Mon, 01 Dec 2008 01:15:39 GMT
> Server: Apache/2.0.61 (Unix)
> Access-Control-Allow-Origin: http://api.bob.com
> Access-Control-Allow-Methods: GET, POST, PUT
> Access-Control-Allow-Headers: X-Custom-Header
> Content-Type: text/html; charset=utf-8
> Content-Encoding: gzip
> Content-Length: 0
> Keep-Alive: timeout=2, max=100
> Connection: Keep-Alive
> Content-Type: text/plain
> ```

上面的HTTP回应中，关键的是`Access-Control-Allow-Origin`字段，表示`http://api.bob.com`可以请求数据。该字段也可以设为星号，表示同意任意跨源请求。

> ```http
> Access-Control-Allow-Origin: *
> ```

如果服务器否定了"预检"请求，会返回一个正常的HTTP回应，但是没有任何CORS相关的头信息字段。这时，浏览器就会认定，服务器不同意预检请求，因此触发一个错误，被`XMLHttpRequest`对象的`onerror`回调函数捕获。

**浏览器的正常请求和回应**

一旦服务器通过了"预检"请求，以后每次浏览器正常的CORS请求，就都跟简单请求一样，会有一个`Origin`头信息字段。服务器的回应，也都会有一个`Access-Control-Allow-Origin`头信息字段。

下面是"预检"请求之后，浏览器的正常CORS请求。

> ```http
> PUT /cors HTTP/1.1
> Origin: http://api.bob.com
> Host: api.alice.com
> X-Custom-Header: value
> Accept-Language: en-US
> Connection: keep-alive
> User-Agent: Mozilla/5.0...
> ```

上面头信息的`Origin`字段是浏览器自动添加的。

下面是服务器正常的回应。

> ```http
> Access-Control-Allow-Origin: http://api.bob.com
> Content-Type: text/html; charset=utf-8
> ```

上面头信息中，`Access-Control-Allow-Origin`字段是每次回应都必定包含的。