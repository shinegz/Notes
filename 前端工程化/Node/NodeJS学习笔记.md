## Node.Js

> 基于Google Chrome的V8 JavaScript引擎开发的JavaScript运行环境。

**node中的作用域**

在node中，JavaScript没有全局作用域，只有模块作用域，因为每个.js文件相当于一个模块，而node将每个模块的内容进行闭包处理（用函数包裹），相当于我们在模块中定义的变量都位于函数体内，因此每个模块被放进各个函数中，也就是在node环境中我们写的JavaScript代码都被封装在不同的函数里，没有位于任何函数体之外的JavaScript变量，所以也就没有全局作用域这个概念
而在浏览器的环境中，所有的JavaScript都被直接放在window这个区域内，没有被处理，当引入一个.js文件时，JavaScript代码被原封不动的放入window中，在.js文件中定义的任何函数之外的变量依然处于任何函数之外，这样所有的.js文件中定义在函数体之外的变量就共享同一个处于任何函数之外的区域，所以浏览器中有且仅有一个全局作用域

### 模块化

> 模块化出现的背景

由于代码量过大，在单一的文件中写代码，会使文件中的代码越来越长，维护起来难度巨大
为了编写可维护的代码，我们把很多函数分组，分别放到不同的文件里，这样，每个文件包含的代码就相对较少，每个文件包可以称之为一个模块

**模块化实现条件**

1、文件作用域
2、通讯规则（加载，导出）

**关于node中的模块导出原理**

在每个模块中，都有一个隐藏对象 

```javascript
                        module = { 
						  exports ：{

                             }
                         }
                         在使用 require 加载模块时，通过
                         return module.exports 将会导出这个对象
```

通过 module.exports.xxx = xxx;将要导出的内容挂载到 module.exports 对象上面便可导出。
又考虑到这样书写比较麻烦，又加入了 exports = module.exports 这一隐藏语句，所以可通过 exports.xxx = xxx 的方式将要导出内容挂载到导出对象上（exports 和 module.exports 指向同一个对象）
第二种方式会让我们以为导出的是 exports 对象，当我们只需要导出一个元素时，使用 exports = xxx,这种做法无法将想要导出的内容导出，原因在于 exports 和 module.exports 不再指向一个对象，而实际导出的是 module.exports 对象，故应该使用 module.exports = xxx 的方式导出一个对象。
综上所续，为了方便书写，且保证正确的写法最好是  module.exports = xxx (一个对象的情况)
                                            module.exports = {      
                                                 xxx ：xxx,
                                                 xxx : xxx
                                            }                   (多个对象的情况)

**关于node中的require**

require加载一个模块只是执行其中的代码，并返回了该模块的module.exports对象，该对象上挂载有该模块选择暴露给外部的变量（我们需要手动将变量挂载上去），文件与文件之间由于是模块作用域，所以不会有代码污染的问题
--模块完全是封闭的
--外部无法访问内部
--内部也无法访问外部



**关于模块加载所用的模块标识（根据模块标识寻找并加载文件）**

路径形式的模块：
         ./ 当前目录，不可忽略
         ../上一级目录，不可忽略
         xx:x/x/x.js 几乎不用
         /xxxx 几乎不用
         首位的 / 在这里表示的是当前文件模块所属磁盘根路径 (x:)
         .js 后缀名可以省略
非路径形式的模块标识:
1、核心模块：直接是模块名
2、第三方模块：模块标识为包名，由于既不是核心模块，也不是路径形式的模块
             先找到当前文件所处目录中的 node_modules 目录
             node_modules/xxx
             node_modules/xxx/package.josn 文件
             node_modules/xxx/package.josn 文件中的 main 属性
             main 属性中就记录了 xxx 的入口模块
             然后加载使用这个第三方包
             实际上最终加载的还是文件

             如果 package.josn 文件不存在或者 main 指定的入口模块不存在
             则 node 会自动找该目录下的 index.js
             也就是说 index.js 会作为一个默认备选项
    
             如果以上所有任何一个条件都不成立，则会进入上一级目录中的node_modules 目录查找
             如果上一级还没有，则会继续往上上一级查找，如果直到当前磁盘根目录还找不到，最后报错：can not find module xxx

注意： 我们一个项目有且只有一个 node_modules,放在项目根目录中，这样的话项目中所有的子目录都可以加载第三方包

## npm(node package manager) 

一个命令行工具，只要你安装了 node 就已经安装了 npm，方便我们下载JavaScript包，通过npm 命令便捷获取JavaScript包
常用命令：
        npm init
            npm init -y 可以跳过向导，快速生成
        npm install
            一次性把 dependencies 选项中的依赖项全部安装
            npm i
        npm install 包名
            只下载
            npm i 包名
        npm install --save 包名
            下载并保存依赖项（package.josn 文件中的 dependencies 选项）
            npm i -S 包名
        npm uninstall 包名
            只删除，如果有依赖项会依然保存
            npm un 包名
        npm uninstall --save 包名
            删除的同时也会把依赖信息也去除
            npm un -S 包名
        npm help
            查看使用帮助
        npm 命令 --help
            查看指定命令的使用帮助

## 关于 npm 被墙的问题

npm 存储包文件的服务器在国外，有时候会被墙，速度很慢，所以要解决这个问题
http://npm.taobao.org/ 淘宝的开发团队把npm 在国内做了一个备份
安装淘宝的 cnpm
在任意目录执行都可以
npm install --global cnpm (--global 表示安装到全局)
安装之后便可使用 cnpm ,只需将原先的 npm 换成 cnpm 即可，就会通过淘宝的服务器来下载相关包（npm 命令依然可用，只不过还是通过国外的服务器）
也可通过如下命令更改下载路径
npm config set registry https://registry.npm.taobao.org

# npm 全局包位置

**C:\Users\GZ\AppData\Roaming\npm**

## 关于 package.josn 的说明(***新建项目后第一步就是新建 package.josn 文件，并配置好里面的相关信息，这会帮助我们更加规范的编程***)

建议在每个项目的根目录下都有一个 package.josn 文件（可以不用手动创建，通过在项目根目录下输入 npm init 命令，便会引导创建 package.josn 中的内容）
在执行 npm install 下载包的时候，加上 --save 选项，这样就会自动在 package.josn 文件的 dependencies 选项中的依赖项全部安装
npm i
        npm install 包名
            只下载
            npm i 包名
        npm install --save 包名
            下载并保存依赖项（package.josn 文件中的 dependencies 选项）
 项添加包的信息
package.josn 文件中包含 dependencies 选项中的依赖项全部安装
npm i
        npm install 包名
            只下载
            npm i 包名
        npm install --save 包名
            下载并保存依赖项（package.josn 文件中的 dependencies 选项）
 的好处在于，哪怕不小心将项目下的 node_modules 文件误删了，只需要 npm install 命令，便可根据 dependencies 选项中的依赖项全部安装
npm i
        npm install 包名
            只下载
            npm i 包名
        npm install --save 包名
            下载并保存依赖项（package.josn 文件中的 dependencies 选项）
 将所依赖的包重新下载下来

## 关于package-lock.json

npm5 以前是不会有 package-lock.json 这个文件的
npm5 以后才加入了这个文件
当你安装包的时候，npm都会生成或者更新 package-lock.json 这个文件
    * 当你安装的时候，会自动创建或更新 package-lock.json 这个文件
        * package-lock.json 这个文件会保存 node_modules 中所有包的信息（版本、下载地址）
        *这样的话，当你误删掉 node_modules 中的文件，再重新 npm install 时，速度就会提升（直接按照 package-lock.json 中各包的地址去下载）
        * 从文件名来看，lock可以称之为锁
        * 这个lock是用来锁定版本的
        * 如果项目依赖了某个包的一个版本，当你重新npm install时，会默认下载包的最新版本，而如果我们的程序希望可以锁住一个版本，而不更新
        * 所以这个 package-lock.json 文件的另一个作用就是锁住版本号，防止自动升级新版

## 修改完代码保存后项目自动重启

可以通过第三方命名行工具： nodemon 实现
安装npm install --global nodemon 
使用nodemon xxx

## 回调函数

在JavaScript中，回调函数的意义在于它使得我们可以得到并操作异步代码执行过程中产生的数据。

## node中的其他成员

在每个模块中，除了require、exports等模块相关API之外，还有两个特殊的成员：

* __dirname 动态获取 可以用来获取当前文件模块所属目录的绝对路径
* __filename 动态获取 可以用来获取当前文件的绝对路径
* __dirname 和 __filename 是不受执行node命令所属路径影响的
  **在文件操作中**，使用相对路径是不可靠的，因为在node中**文件操作中的相对路径**被设计为相对执行node命令所处的路径（不是bug，人家这样设计是有使用场景的）。
  所以为了解决这个问题，很简单，只需要把相对路径变为绝对路径就可以了。
  在拼接路径的过程中，为了避免手动拼接带来的一些低级错误，所以推荐多使用： path.join() 来拼接。
  所以为了尽量避免刚才所描述的这个问题，在文件操作中使用的相对路径都统一转换为 动态的绝对路径。
  *补充：模块中的路径标识和这里的路径没关系（模块中的当前路径是当前文件所处的路径），不受影响（相对于文件模块）*

### 遇到的问题及解决办法

+  关于VScode中复制JavaScript项目文件夹后运行node指令提示找不到依赖包的情况

> 删除项目的 node_modules 文件夹，然后在项目当前目录执行 npm install 命令，重新下载 package.json 中的依赖项中的包，即可解决问题。

+ 路径问题

> 在不同的环境中对路径的处理会有所不同，常见的例如对 ./ 的处理就会不同**这个是我自己的主观臆断，之所以会让我觉得在不同环境下对 ./ 的处理不同，是因为我在不同的目录下执行了node命令，而对于node中的文件操作而言 ./ 表示的是当前node命令所处目录，自然会对 ./ 的解释不同**



### nvm命令

1. nvm arch ：显示node是运行在32位还是64位。
2. nvm install <version> [arch] ：安装node， version是特定版本也可以是最新稳定版本latest。可选参数arch指定安装32位还是64位版本，默认是系统位数。可以添加--insecure绕过远程服务器的SSL。
3. nvm list [available] ：显示已安装的列表。可选参数available，显示可安装的所有版本。list可简化为ls。
4. nvm on ：开启node.js版本管理。
5. nvm off ：关闭node.js版本管理。
6. nvm proxy [url] ：设置下载代理。不加可选参数url，显示当前代理。将url设置为none则移除代理。
7. nvm node_mirror [url] ：设置node镜像。默认是https://nodejs.org/dist/。如果不写url，则使用默认url。设置后可至安装目录settings.txt文件查看，也可直接在该文件操作。
8. nvm npm_mirror [url] ：设置npm镜像。https://github.com/npm/cli/archive/。如果不写url，则使用默认url。设置后可至安装目录settings.txt文件查看，也可直接在该文件操作。
9. nvm uninstall <version> ：卸载指定版本node。
10. nvm use [version] [arch] ：使用制定版本node。可指定32/64位。
11. nvm root [path] ：设置存储不同版本node的目录。如果未设置，默认使用当前目录。
12. nvm version ：显示nvm版本。version可简化为v。