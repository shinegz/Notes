### 正则表达式

正则表达式是对字符串操作的一种逻辑公式，就是用事先定义好的一些特定字符、及这些特定字符的组合，组成一个“规则字符串”，这个“规则字符串”用来表达对字符串的一种过滤逻辑。

> 用来处理字符串的规则
>
> + 只能处理字符串
> + 它是一个规则：可以验证字符串是否符合某个规则（test），也可以把字符串中符合规则的内容捕获到（exec/match..）

```javascript
let str = 'good'
// 学习正则就是用来制定规则
let reg = /\d+/
reg.test(str)  // =>false,验证字符串是否符合正则表达式所描述的的规则

str = '2020-04-01'
reg.exec(str)
```

**编写正则表达式**

创建方式有两种

````javascript
// 字面量方式(两个斜杠之间包起来的，都是用来描述规则的元字符)
let reg = /\d+/

// 构造函数模式创建  两个参数：元字符字符串，修饰符字符串
let reg2 = new RegExp('\\d+');
````

正则表达式由两部分组成

+ 元字符
+ 修饰符

```javascript
/*常用元字符*/
// 1.量词元字符：设置出现的次数
* 零到多次
+ 一到多次
？ 零次或者一次
{n} 出现n次
{n,} 出现n到多次
{n,m} 出现n到m次

// 2.特殊元字符：单个或者组合在一起代表特殊的含义
\ 转义字符(普通->特殊->普通)
. 除\n(换行符)以外的任意字符
^ 以哪一个元字符作为开始
$ 以哪一个元字符作为结束
\n 换行符
\b 代表单词边界
\d 0到9之间的一个数字
\D 非0到9之间的一个数字（大写和小写的意思是相反的）
\w 数字、字母、下划线中的任意一个字符
\s 一个空白符（包括空格、制表符、换页符等）
\t 一个制表符（一个TAB键；四个空格）
x|y x或者y中的一个字符
[xyz] x或者y或者z中的一个字符
[^xy] 除了x/y以外的任意字符
[a-z] 指定a-z这个范围中的任意字符
[^a-z] 除了a-z这个范围的任意字符
() 正则中的分组符号
(?:) 只匹配不捕获
(?=) 正向预查
(?!) 负向预查

// 3.普通元字符：代表本身含义的
/gaozhuang/ 此正则匹配的就是 'gaozhuang'
```

```javascript
/*正则表达式常用的修饰符*/
i =>ignoreCase 忽略单词大小写匹配
m =>multiline 可以进行多行匹配
g =>global 全局匹配

/*
/A/.test('aba')  =>false
/A/i.test('aba') =>true
*/
```

**元字符详解**

`^ $`

```javascript
let reg = /^\d/
reg.test('gz')     //false
reg.test('2020gz') //true 
reg.test('gz2020') //false

rge = /\d$/
reg.test('gz')     //false
reg.test('2020gz') //false 
reg.test('gz2020') //true
```

```javascript
// ^/$两个都不加：字符串中包含符合规则的内容即可
let reg1 = /\d+/
// ^/$两个都加: 字符串只能是和规则一致的内容
let reg2 = /^\d+$/

// 举个例子：验证手机号码（11位，第一个数字是1即可）
let reg = /^1\d{10}$/
```

`\`

```javascript
// .不是小数点，是除\n以外的任意字符
let reg = /^2.3$/
reg.test('2.3')  //true
reg.test('2@3') //true 
reg.test('23') //false

// 基于转义字符，让其只能代表小数点
reg = /^2\.3/
reg.test('2.3')  //true
reg.test('2@3') //false 
reg.test('23') //false

let str = '\\d'  //表示\d
reg = /^\d$/ 
reg.test(str) // false
reg = /^\\d$/
reg.test(str) //true
```

`x|y`

```javascript
let reg = /^18|29$/ 
reg.test('18')  //true
reg.test('29')  //true
reg.test('182')  //true
reg.test('829')  //true

// 直接x|y会存在很乱的优先级问题，一般我们写的时候都伴随着小括号进行分组，因为小括号改变处理的优先级
reg = /^(18|29)$/
reg.test('18')  //true
reg.test('29')  //true
reg.test('182')  //false
reg.test('829')  //false
```

`[]`

```javascript
//1.中括号中出现的字符一般都代表本身的含义
let reg = /^[@+]$/
reg.test('@')  //true
reg.test('+')  //true
reg.test('@+') //false

reg = /^[\d]$/    //字符串为0-9之间的任意一个数字
reg.test('9')  //true
reg.test('\')  //false
reg.test('d')  //false

reg = /^[\\d]$/  //字符串为一个斜杆或者字母d
reg.test('\\')  //true
reg.test('d')  //true
reg.test('3')  //false

//2.中括号中不存在多位数
reg = /^[18]$/
reg.test('1')  //true
reg.test('8')  //true
reg.test('18')  //false

reg = /^[10-29]$/  //表示1、0-2、9中的一个
```

**常用的正则表达式**

1.验证是否为有效数字

```javascript
/*
 *规则分析
 *1.可能出现 + -号，也可能不出现
 *2.一位0-9都可以，多位首位不能是0
 *3.小数部分可能有可能没有，一旦有后面必须有小数点和数字
 */
let reg = /^[+-]?(\d|([1-9]\d+))(\.\d+)?$/
```

2.验证密码

```javascript
// 数字、字母、下划线
// 6~16位

let val = userPassInp.val

let reg = /^\w{6,16}$/
let flag = reg.test(reg)
```

3.验证真实姓名

```javascript
/*
1.汉字  /^[\u4E00-\u9FA5]$/
2.名字长度 2~10位
3.可能有译名 ·汉字
*/
let reg = /^[\u4E00-\u9FA5]{2,10}(·[\u4E00-\u9FA5]{2,10}){0,2}$/
```

4.验证邮箱

```javascript
let reg = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/

// \w+((-\w+)|(\.\w+))*
// 1. 开头是数字、字母、下划线（1到多位）
// 2. 接着是 -数字、字母、下划线 或者 .数字、字母、下划线， 整体零到多次

// @[A-Za-z0-9]+
// 1.@后面紧跟着 数字、字母（一到多位）

// ((\.|-)[A-Za-z0-9]+)*
// 1.对@后面名字的补充
// 多域名  .com.cn

// \.[A-Za-z0-9]+
// 1.这个匹配的是邮箱最后的域名
```

5.身份证号码

```javascript
/*
1. 一共18位
2. 最后一位可能是X

身份证前6位： 省市县
中间8位： 年月日
最后四位：
	最后一位：X或者数字
	倒数第二位：偶数 女  奇数 男
	其余的是经过算法算出来的
*/
// 小括号分组的第二个作用：分组捕获，不仅可以把大正则匹配的信息捕获到，还可以单独捕获到每个小分组的内容
let reg = /^(\d{6})(\d{4})(\d{2})(\d{2})\d{2}(\d)(\d|X)$/
```

**正则两种创建方式的区别**

```javascript
// 如果我们想用变量的值作为正则的元字符，则不能使用字面量的方式创建正则，应该使用构造函数的方式,因为//中的所有内容都被当做元字符，即变量名会被当做元字符，而不会将其当做变量对待
let type = 'gz'
let reg = new RegExp('^'+type+'$')
```

**正则的捕获**

> 实现正则捕获的方法
>
> + 正则RegExp.prototype上的方法
>   + exec
>   + test
> + 字符串String.prototype上支持正则表达式处理的方法
>   + replace
>   + match
>   + splite
>   + ....

```javascript
// 实现正则捕获的前提是：当前正则要和字符串匹配，如果不匹配捕获的结果是null
let str = 'zhishdabk2020hska2021'
let reg = /\d+/
/*
基于exec实现正则的捕获
	1.捕获到的结果是null或者一个数组
	  第一项：本次捕获到的内容
	  其余项：对应小分组本次单独捕获的内容
	  index：当前捕获内容在字符串的起始索引
	  input：原始字符串
	2.每执行一次exec，只能捕获到第一个符合正则规则的，但是默认情况下，我们执行一百遍，获取的结果永远都是第一个匹配的，其余的捕获不到
	=> “正则捕获的懒惰性”：默认只能捕获第一个	
	 reg.lastIndex:当前正则下一次匹配的起始索引位置
		懒惰性捕获的原因：默认情况下lastIndex的值不会被修改，每一次都是从字符串开始位置查找，所以找到的永远只是第一个匹配到的
	解决办法，给正则表达式加全局修饰符，即：
	reg = /\d+/g
*/
console.log(reg.exec(str))
// ["2020", index: 9, input: "zhishdabk2020", groups: undefined]

练习：编写一个方法execAll，执行一次可以把所有匹配的结果捕获到（前提正则一定要设置全局修饰符g）
//  自己写的
(function () {
        function execAll(str){
            let arr = []
            let res = true
            let i = 0
            
            if(!this.global) return this.exec(str)
            
            while(res){
            	res = this.exec(str)
                //console.log(res)
                if(res){
                    arr[i++] = res[0]
                }
            }
            return arr
        }
     	RegExp.prototype.execAll = execAll
    })()

//  别人写的
(function () {
        function execAll(str){
            let arr = []
            let res = this.exec(str)
            
            if(!this.global) return this.exec(str)
            
            while(res){
            	arr.push(res[0])
                res = this.exec(str)
            }
            return arr
        }
     	RegExp.prototype.execAll = execAll
    })()
```

**正则的分组捕获**

```javascript
// 身份证号码
let str = '420983197901308112'
let reg = /^(\d{6})(\d{4})(\d{2})(\d{2})\d{2}(\d)(\d|X)$/
console.log(reg.exec(str))
console.log(str.match(reg))
// ["420983197901308112", "420983", "1979", "01", "30", "1", "2", index: 0, input: "420983197901308112", groups: undefined]
// 第一项：大正则匹配的结果
// 其余项：每一个小分组单独匹配捕获的结果
// 如果设置了分组（改变优先级），但是捕获的时候不需要单独捕获，可以基于？：来处理
```

```javascript
// 既要捕获到{数字}，也想单独的把数字也捕获到，例如：第一次找到{0}，还需要单独获取0
let str = '{0}年{1}月{2}日'
// 不设置g只能匹配一次，exec和match获取的结果一致（既有大正则匹配的信息，也有小分组匹配的信息）
let reg = /\{(\d+)\}/
console.log(reg.exec(str))
console.log(str.match(reg))
//["{0}","0"...]

let reg = /\{(\d+)\}/g
console.log(str.match(reg)) // ["{0}","{1}","{2}"]
// 多次匹配的情况下，match只能把大正则匹配的内容获取到，小分组匹配的信息无法获取
let aryBig = [],arySmall = [],res = reg.exec(str)
while(res){
    let [big,small] = res  // 数组的解构赋值
    aryBig.push(big)
    arySmall.push(small)
    res = reg.exec(str)
}
console.log(aryBig,arySmall)  //["{0}", "{0}", "{1}", "{2}"]  ["0", "0", "1", "2"]
```

```javascript
// 分组的第三个作用：“分组引用”
let str = "book"
let reg = /^[a-zA-Z]([a-zA-Z])\1[a-zA-Z]$/
// 分组引用就是通过“\数字”让其代表和对应分组出现一模一样的内容
console.log(reg.test('book')) // true
console.log(reg.test('deep')) // true
console.log(reg.test('some')) // false
```

**正则捕获的贪婪性**

```javascript
let str = '中国2020湖北'
// 正则捕获的贪婪性：默认情况下，正则捕获的时候，是按照当前正则所匹配的最长结果来获取的
let reg = /\d+/g
console.log(str.match(reg)) // ["2020"]

// 在量词元字符后面设置？：取消捕获时的贪婪性（按照正则匹配的最短结果来获取）
let reg = /\d+？/g
console.log(str.match(reg)) // ["2","0","2","0"]
```

问号在正则中的五大作用

+ 问号左边是非量词元字符：本身代表量词元字符，出现零到一次
+ 问号左边是量词元字符：取消捕获时的贪婪性
+ (?:)只匹配不捕获
+ (?=)正向预查
+ (?!)负向预查



**其它正则捕获的方法**

1.test也能捕获（本意是匹配）

```javascript
let str = "{0}年{1}月{2}日"
let reg = /\{(\d+)\}/g
console.log(reg.test(str))   // true
console.log(RegExp.$1)  // 0

console.log(reg.test(str))   // true
console.log(RegExp.$1)  // 1

console.log(reg.test(str))   // true
console.log(RegExp.$1)  // 2

console.log(reg.test(str))   // false
console.log(RegExp.$1)  // "2" 存储的是上次捕获的结果

// RegExp.$1~9：获取当前本次正则匹配后，第一个到第九个分组的信息
```

2.replace字符串中实现替换的方法（一般都是伴随正则一起使用的）

```javascript
let str = 'gz2020zknf2019kzznc2020gz'
// 把"gz"替换成"高壮"
// 1.不用正则，执行一次只能替换一个,且每次都是从字符串开始位置查找替换
str = str.replace("gz","高壮")
console.log(str)

// 2.使用正则会简单一点
str = str.replace(/gz/g,"高壮")  // 开启全局模式的正则，会从上次停止的位置接着找
```

案例：把时间字符串进行处理

```javascript
let time = '2020-04-05'
// 变为“2020年04月05日”
let reg = /^(\d{4})-(\d{1,2})-(\d{1,2})$/

// 这样可以实现
time = time.replace(reg,'$1年$2月$3日')
console.log(time)

// 还可以这样处理 [str].replace([reg],[function])
// 1.首先拿REG和TIME进行匹配捕获，能匹配到几次就会把传递的函数执行几次（而且是匹配一次就执行一次）
// 2.不仅把方法执行，而且REPLACE还给方法传递了实参信息（和exec捕获的内容一致的信息：大正则匹配的内容，小分组匹配的信息...）
// 3.在函数中我们返回的是啥，就把当前大正则匹配的内容替换成啥
time = time.replace(reg,(big,$1,$2,$3) => {
    // 这里的$1,$2,$3是我们自己设置的变量
    console.log(big,$1,$2,$3)
})
time = time.replace(reg,(...arg) => {
   let [,$1,$2,$3] = arg
   $2.length<2?$2='0'+$2:null
   $3.length<2?$3='0'+$3:null 
    return $1 + '年' + $2 + '月' + $3 + '日'
})
```

单词首字母大写

```javascript
let str = 'more hard, more happy!'
let reg = /\b([a-zA-Z])[a-zA-Z]*\b/g
// 函数被执行了六次，每一次都把正则匹配信息传递给函数
// 每一次ARG：['more','m'] ['hard','h']...
str = str.replace(reg,(...arg) => {
    let [content,$1] = arg
    $1 = $1.toUpperCase()
    content = content.substring(1)
    return $1 + content
})
console.log(str)  // "More Hard, More Happy!"
```

验证一个字符串中哪一个字母出现的次数最多，多少次？

```javascript
let str = 'gzshkdzhdkzjzkfhzkkdkhzsk'
/*去重*/
let obj = {}
[].forEach.call(str,char=>{
    if(typeof obj[char]!='undefined'){
        obj[char]++
        return
    }
    obj[char]=1
})
let max = 1,res=[]
for(let key in obj){
    let item = obj[key]
    max>item?null:max=item
}
for(let key in obj){
    let item = obj[key]
    if(item===max){
        res.push(key)
    }
}
console.log(`出现次数最多的字符是：${res},出现了${max}次`)

/*排序*/
let str = 'haskfdahkiubsdcgiucbfnfkss'
str = str.split('').sort((a,b)=>a.localeCompare(b)).join('') // "aabbccddfffghhiikkknssssuu"
let reg = /([a-zA-Z])\1+/g
let ary1 = str.match(reg) //["aa", "bb", "cc", "dd", "fff", "hh", "ii", "kkk", "ssss", "uu"]
ary1.sort((a,b)=>b.length-a.length)  // ["ssss", "fff", "kkk", "aa", "bb", "cc", "dd", "hh", "ii", "uu"]
let max = ary1[0].length,res=[ary1[0].substr(0,1)]
for(let i=1;i<ary1.length;i++){
    if(ary1[i].length<max){
        break
    }
    res.push(ary1[i].substr(0,1))
}
console.log(`出现次数最多的字符是：${res},出现了${max}次`)

/*按字符串长度依次递减找*/
let str = 'ahsfkjgushuidhwufsbssddhsjsshuskjhs',
    res=[],
    max=0,
    flag=false
str = str.split('').sort((a,b)=>a.localeCompare(b)).join('')
for(let i=str.length;i>0;i--){
   //  console.log('for循环中') 进去了
    let reg = new RegExp('([a-zA-Z])\\1{'+(i-1)+'}','g')
    str.replace(reg,(...arg)=>{
       let [content,$1] = arg
        console.log('replace循环中') // 没进去   原因：没有正确使用构造函数创建正则对象
    	max = content.length
    	res.push($1)
    	flag = true
    })
    if(flag) break
}
console.log(`出现次数最多的字符是：${res},出现了${max}次`)
```

时间字符串的格式化处理和URL字符串的处理和数字千分符的处理

```javascript
(function () {
    /*
     *@params: 模板字符串，其中{0}表示年，{1}表示月，{2}~{5}表示日、时、分、秒
     */
    function timeFormat( template = '{0}年{1}月{2}日 {3}时{4}分{5}秒') {
        // 获取字符串中的时间信息（时间字符串中应按照年月日，时分秒的顺序）
        let timeAry = this.match(/\d+/g)      
        return template.replace(/\{(\d+)\}/g,(...[,$1]) => {
            let time = timeAry[$1] || '00'  // 没有对应时间信息，则为00
            return time.length < 2 ? '0' + time : time
        })
    }
    
    /*
     *queryURLParams: 获取URL地址问号和后面的参数信息（可能包含hash值）
     */
    function queryURLParams() {
        let obj = {}
        this.replace(/([^?=&#])=([^?&=#])/g,(...[,$1,$2]) => obj[$1] = $2)
        this.replace(/#([^?=&#])/g,(...[,$1,$2]) => obj[$1] = $2)
        return obj
    }
    
    /*
     *  millimter: 实现
     */
    function millimter() {
        return this.replace(/\d{1,3}(?=(\d{3})+$)/g,(content) => content + ',')
    }
    
    ['timeFormat','queryURLParams','millimter'].forEach(item => {
        String.prototype[item] = eval(item)  // 将item当JavaScript脚本执行
    })
})()
```

