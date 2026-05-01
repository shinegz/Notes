![git](http://www.ruanyifeng.com/blogimg/asset/2014/bg2014061202.jpg)

> 对于一个 git 仓库，只有一个工作区、一个暂存区、一个仓库
>
> 切换分支只是从仓库中取出该分支的文件到工作区，暂存区不会随着分支的切换而变化
>
> 仓库中的 HEAD 指向当前分支的最新版本

## 本地仓库上传到GitHub上的一般步骤

准备工作：安装好Git

1、首先要建立本地与GitHub的SSH的安全连接

​      具体步骤可参考 https://blog.csdn.net/Mrrrrr/article/details/102999742 

2、在GitHub上新建好仓库，注意：保持默认选项即可，仓库内不能有东西，否则上传时会出错。

3、在本地新建项目，并在项目根目录下初始化仓库

​     在项目根目录下右键打开**Git Bash Here**打开命令窗口

​      键入命令：

```bash
git init
```

​    为仓库指定GitHub用户名和email（这里可以不指定，不过当提交文件到仓库或者提交本地仓库到GitHub上时需要每次都输入用户名和邮箱）

```javascript
git config --global user.name "你的GitHub账号名"
git config --global user.email "你的注册账号"
```

 注意git config命令的–global参数，用了这个参数，表示你这台机器上所有的Git仓库都  会使用这个配置，当然也可以对某个仓库指定不同的用户名和Email地址。 

4、将项目文件提交到本地仓库

 ```bash
git add 文件 （提交单个文件）//git add . (提交全部文件)

git commit -m "提交信息"
 ```

5、与GitHub上的仓库建立连接

```bash
git remote add origin "仓库地址"    *origin 为远程主机名*
```

6、将本地的当前分支发送到origin主机上，若origin主机上没有对应分支，则在origin主机上新建分支

```bash
git push -u origin [branchname]    * -u 表示指定origin为默认远程主机，后面可直接使用 git push了
```

更多远程操作详解看： http://www.ruanyifeng.com/blog/2014/06/git_remote.html 

## 常用命令

### add

> 将工作区的文件添加到暂存区

### commit

> 提交记录保存的是当前目录下所有文件的快照，所有提交记录构成一颗提交树。条件允许的情况下，它会将当前版本与仓库中的上一个版本进行对比，并把所有的差异打包到一起作为一个提交记录。

```git
git commit
git commit
```

> c0为初始提交，c1是基于c0进行差异化后的提交，c2是基于c1进行差异化后的提交

<img src=".\git\git_commit.png" style="zoom:50%;" />

### branch

> 分支名指向某个提交记录。创建一个分支相当于：我想基于这个提交以及它所有的父提交进行新的工作。
>
> 语法：
>
> git branch <分支名>

```git
git branch newImage
git commit
```

<img src=".\Git\git_branch_commit_1.png" style="zoom:50%;" />

```git
git branch newImage
git checkout newImage
git commit
```

<img src=".\Git\git_branch_commit.png" style="zoom:50%;" />

### checkout

> 用于改变HEAD的指向

+ 参数为分支名

  > git checkout <分支名>
  >
  > HEAD指向分支名，即HEAD -> <分支名> -> <提交号>

+ 参数为提交号

  > git checkout <提交号>
  >
  > HEAD指向提交号，即HEAD -> <提交号>

+ 新建一个分支并切换到该分支：

  > git checkout -b <分支名>

### merge

> 将当前分支与指定分支进行合并

<img src=".\git\git_merge_1.png" style="zoom:50%;" />

```git
git merge bugFix
```

<img src=".\git\git_merge_2.png" style="zoom:50%;" />

### rebase

> 合并分支，将当前分支移动到指定分支下面

<img src=".\git\git_rebase_1.png" style="zoom:50%;" />

```git
git rebase main
```



<img src=".\git\git_rebase.png" alt="git_rebase" style="zoom:50%;" />

## 高级

### HEAD

> HEAD表示的是正在其基础上进行工作的提交记录，它始终指向当前分支上最近一次提交记录，通常情况下是指向分支名。每一个提交记录都有一个唯一的哈希值，可通过`checkout`命令改变HEAD指向，让其指向具体的提交记录，即分离HEAD
>
> **注意：一般不要分离HEAD，这会让Git的使用变得复杂**

#### 分离的HEAD

> 分离的 HEAD 就是让其指向了某个具体的提交记录而不是分支名。

```git
git checkout c1
// 分离前：HEAD -> main -> c1
// 分离后：HEAD -> c1
git checkout main
// HEAD -> mian -> c1
```

<img src=".\git\分离的HEAD.png" style="zoom:50%;" />

#### 哈希值

```git
git checkout <hash value>
```

#### 相对引用（^）

> 将HEAD后退一步

```git
git checkout main^
```

<img src=".\git\^.png" style="zoom:50%;" />

```git
git checkout main^2
// 默认后退到第一个父节点，^2表示选择后退到另一个父节点
```

<img src=".\git\选择回退.png" style="zoom:50%;" />

#### 相对引用（~）

> 将HEAD后退指定步数

```git
git checkout HEAD~4
```

<img src=".\git\~.png" style="zoom:50%;" />

### 强制修改分支位置

```git
git branch -f <分支名> <分支名|提交号>
```

### 撤销变更

#### git reset（改变提交记录历史）

> 将当前分支移动到指定提交记录处（**前提是HEAD没有分离**）
>
> 语法：
>
> git reset <提交号>

```git
git reset HEAD~1
// Git 把 main 分支移回到 `C1`；现在我们的本地代码库根本就不知道有 `C2` 这个提交了
// 在reset后， C2 所做的变更还在，但是处于未加入暂存区状态。
```

<img src=".\git\reset.png" style="zoom:50%;" />

#### git revert（添加一个新的提交记录用来消除指定提交记录的影响）

> 通过提交一个新的记录来“中和”掉指定提交记录
>
> 语法：
>
> git revert <提交号>

```git
git revert HEAD
// 新提交记录 `C2'` 引入了**更改** —— 这些更改刚好是用来撤销 `C2` 这个提交的。也就是说 `C2'` 的状态与 `C1`是相同的。
```

<img src=".\git\revert.png" style="zoom:50%;" />

## 移动提交树

### git cherry-pick（自由修改提交树）

> 将提交树中指定的提交记录**复制**到当前所在分支的最新提交记录的下面；**本质是移动到HEAD下面**
>
> 语法：
>
> git cherry-pick <提交号A> <提交号B>... 

<img src=".\git\git_cherry-pick_1.png" style="zoom:50%;" />

```git
git cherry-pick c2 c4
```

<img src=".\git\git_cherry-pick_2.png" style="zoom:50%;" />

### git rebase -i（交互式rebase）



## 标签

> 用于给特定的提交记录命名，它不会随着新的提交而移动，就像提交树上的一个锚点，标识了某个特定的位置。
>
> 语法：
>
> git tag <标签名> <提交号>

<img src=".\git\git_tag_1.png" style="zoom:50%;" />

```git
git tag v1 c1
```

<img src=".\git\git_tag_2.png" style="zoom:50%;" />

### git describe

> 用来**描述**离引用最近的锚点（也就是标签）
>
> 语法：
>
> git describe <ref>
>
> `<ref>` 可以是任何能被 Git 识别成提交记录的引用，如果你没有指定的话，Git 会以你目前所检出的位置（`HEAD`）

它输出的结果是这样的：

```git
<tag>_<numCommits>_g<hash>
```

`tag` 表示的是离 `ref` 最近的标签， `numCommits` 是表示这个 `ref` 与 `tag` 相差有多少个提交记录， `hash` 表示的是你所给定的 `ref` 所表示的提交记录哈希值的前几位。

当 `ref` 提交记录上有某个标签时，则只输出标签名称



## 远程

### 克隆

> git clone <版本库的网址>

该命令会在本地主机生成一个目录，与远程主机的版本库同名。如果要指定不同的目录名，可以将目录名作为`git clone`命令的第二个参数。

```git
git clone <版本库的网址> <本地目录名>
```

### 远程分支

> 远程分支反映了远程仓库（在上次与之通信时）的状态
>
> 远程分支命名规范
>
> `<remote name>/<branch name>`

在本地无法改变远程分支的状态，在远程分支上，Git变成了分离HEAD状态，即使添加新的提交记录，o/main不会更新。这是因为o/main只有在远程仓库中相应的分支更新了以后才会更新。

```git
git checkout o/main
git commit
```

<img src=".\git\远程分支.png" style="zoom:50%;" />

### 通信

#### 从远程仓库获取数据

> 通过git fetch命令可以从远程仓库获取数据
>
> 语法：
>
> git fetch origin <source>:<destination>

<img src=".\git\git_fetch_p1.png" style="zoom:50%;" />

```git
git fetch origin foo^:bar
// 将远程主机上的foo^提交记录下载到本地，并与bar分支合并
```

<img src=".\git\git_fetch_p2.png" style="zoom:50%;" />

如果 `git fetch` 没有参数，它会下载所有的提交记录到各个远程分支

<img src=".\git\git_fetch_1.png" style="zoom:50%;" />

```git
git fetch
```

<img src=".\git\git_fetch_2.png" style="zoom:50%;" />

`git fetch` 完成了仅有的但是很重要的两步:

- 从远程仓库下载本地仓库中缺失的提交记录
- 更新远程分支指针(如 `o/main`)

`git fetch` 实际上将本地仓库中的远程分支更新成了远程仓库相应分支最新的状态。

**git fetch 不会做的事**

`git fetch` 并不会改变你本地仓库的状态。它不会更新你的 `main` 分支，也不会修改你磁盘上的文件。



#### git pull

> 从远程仓库下载数据，更新远程分支，并与当前检出位置合并
>
> 语法：
>
> git pull origin <source>:<destination>

```git
git pull
// 当前分支自动与唯一一个追踪分支进行合并
// 相当于git fetch和git merge的缩写
git pull --rebase
// 相当于git fetch和git rebase的缩写
```

<img src=".\git\git_pull.png" style="zoom:50%;" />

#### 向远程仓库提交数据

> 将本地仓库的数据上传到远程仓库，**远程仓库中的分支和远程分支都会更新**
>
> 语法：
>
> git push origin <source>:<destination>

<img src=".\git\git_push_p1.png" style="zoom:50%;" />

```git
git push origin foo^:main
// Git 将 foo^ 解析为一个位置，上传所有未被包含到远程仓库里 main 分支中的提交记录。
```

<img src=".\git\git_push_p2.png" style="zoom:50%;" />

如果 `git push` 没有参数，它会上传当前分支的提交记录到远程主机上追踪分支

<img src=".\git\git_push_1.png" style="zoom:50%;" />

```git
git push
```

<img src=".\git\git_push_2.png" style="zoom:50%;" />

当**本地分支与远程仓库中的对应分支提交历史不同**时，提交会被拒绝

```git
git push
```

<img src=".\git\偏离的提交历史.png" style="zoom:50%;" />

这时需要让本地分支与远程仓库中的对应分支同步后再执行提交

```git
git fetch 
git rebase o/main
git push
```

<img src=".\git\偏离的提交历史1.png" style="zoom:50%;" />

### 远程跟踪

> 当你克隆时, Git 会为远程仓库中的每个分支在本地仓库中创建一个远程分支（比如 `o/main`）。然后再创建一个跟踪远程仓库中活动分支的本地分支，默认情况下这个本地分支会被命名为 `main`。

#### 设置远程跟踪

+ 第一种就是通过远程分支检出一个新的分支

```
git checkout -b totallyNotMain o/main
```

就可以创建一个名为 `totallyNotMain` 的分支，它跟踪远程分支 `o/main`。

+ 另一种设置远程追踪分支的方法就是使用：`git branch -u` 命令

```
git branch -u o/main foo
```

这样 `foo` 就会跟踪 `o/main` 了