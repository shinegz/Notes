---
title: Shell 脚本编程学习笔记
date: 2026-03-09
tags:
  - Shell
  - Bash
  - Zsh
  - Linux
  - 脚本编程
aliases:
  - Shell 学习笔记
  - Bash 脚本入门
---

# Shell 脚本编程学习笔记

> [!abstract] 本文定位
> 面向日常使用命令行、但尚未系统掌握 Shell 脚本编程的开发者。从"能打命令"到"能写脚本自动化"，覆盖 Bash/Zsh 的核心语法、文本处理三剑客、信号处理、实战案例等。读完本文，你能：
> - 编写健壮的 Shell 脚本完成日常自动化任务
> - 熟练使用 grep/sed/awk 处理文本和日志
> - 理解管道、重定向、进程替换等核心机制
> - 知道 Bash 与 Zsh 的差异，合理选择

> [!tip] 阅读路径
> **想快速上手** → [[#30 秒心智模型]] → [[#脚本基础 — "写菜谱"]] → [[#变量 — "食材标签"]] → [[#流程控制 — "烹饪步骤"]] → [[#文本处理三剑客]] → [[#总结与一页速查]]
>
> **想搞懂原理** → [[#30 秒心智模型]] → [[#Shell 是什么]] → 逐章阅读 → [[#Bash vs Zsh — "中式 vs 西式厨房"]]

---

## 30 秒心智模型

> **Shell = 厨房**
>
> 你的操作系统就像一个食材丰富的厨房，Shell 是你和这个厨房交流的方式——你下达烹饪指令（命令），厨房（内核）执行操作。Shell 脚本就是把一系列指令写成菜谱，让厨房自动完成整道菜。

| 厨房 | Shell 概念 | 一句话解释 |
|------|-----------|----------|
| 👨‍🍳 你（厨师） | **用户** | 下达指令的人 |
| 📋 菜谱 | **Shell 脚本 (.sh)** | 一系列指令的集合，按步骤自动执行 |
| 🏷️ 食材标签 | **变量** | 给数据贴个名字，方便反复使用 |
| 🔀 烹饪流程图 | **流程控制 (if/for/while)** | 根据条件决定下一步做什么 |
| 🔪 切菜/剥皮/摆盘 | **grep/sed/awk** | 对文本数据进行搜索、编辑、统计 |
| 🚰 水管连接 | **管道 (`\|`)** | 把前一个命令的输出直接送入下一个命令 |
| 📤 装盘出菜 | **重定向 (`>` / `>>`)** | 把结果输出到文件而非屏幕 |
| 🔔 厨房计时器 | **信号 (Signal)** | 通知脚本外部发生了什么（如用户按了 Ctrl+C） |
| 🧰 厨房配置 | **配置文件 (.bashrc/.zshrc)** | 自定义你的厨房布局和默认设置 |

---

## 阅读指南

**本文语境：** 以 Bash 为主讲 Shell 脚本编程，涉及 Zsh 差异和 macOS/Linux 双平台。

**前置知识：** 能在终端中执行 `ls`、`cd`、`pwd` 等基本命令。

**术语表：**

| 术语 | 英文 | 本文中的落点 |
|------|------|-----------|
| Shebang | Shebang (`#!`) | 脚本第一行，告诉系统用哪个解释器执行 |
| 管道 | Pipe (`\|`) | 将前一命令的 stdout 接入后一命令的 stdin |
| 重定向 | Redirect (`>`, `>>`, `<`) | 改变命令输入/输出的方向 |
| 退出码 | Exit Code | 命令执行结果：0 = 成功，非 0 = 失败 |
| 环境变量 | Environment Variable | 系统级别的全局变量，影响程序行为 |
| 参数扩展 | Parameter Expansion | 用 `${}` 语法对变量进行操作的机制 |
| Glob | Globbing | 文件名通配符匹配（`*`、`?`、`[...]`） |

---

## Shell 是什么

### 不是什么 vs 是什么

| ❌ Shell 不是 | ✅ Shell 是 |
|--------------|------------|
| 操作系统本身 | 用户与操作系统内核之间的命令解释器 |
| 一种编程语言（通用意义上） | 一种面向命令行的脚本语言 |
| 图形界面 | 纯文本交互界面（CLI） |
| 只有 Bash 一种 | 一类程序的统称（Bash、Zsh、Fish、Dash 等） |

**正式定义：** Shell 是命令行解释器（Command-Line Interpreter），它读取用户输入的命令（或脚本文件中的命令），解析并传递给操作系统内核执行，最后将结果返回给用户。

### 常见 Shell 一览

| Shell | 发布年份 | 特点 | 默认于 |
|-------|---------|------|-------|
| **sh (Bourne Shell)** | 1979 | POSIX 标准基础 | 早期 Unix |
| **Bash** | 1989 | sh 超集，功能丰富，生态最广 | 大多数 Linux |
| **Zsh** | 1990 | Bash 超集，强大的自动补全和插件 | macOS (2019+) |
| **Fish** | 2005 | 开箱即用，语法独特 | — |
| **Dash** | 1997 | 极轻量，启动快 | Ubuntu (系统脚本) |

> **对你的启发**：日常交互推荐 Zsh + Oh My Zsh（体验好），编写脚本推荐用 Bash（兼容性最好）。脚本第一行用 `#!/usr/bin/env bash` 确保可移植。

---

## 脚本基础 — "写菜谱"

### 第一个脚本

```bash
#!/usr/bin/env bash
# hello.sh — 第一个脚本

echo "Hello, $(whoami)! 现在是 $(date '+%Y-%m-%d %H:%M')"
```

```bash
# 赋予执行权限
chmod +x hello.sh

# 执行
./hello.sh
# 输出: Hello, jiangchuan! 现在是 2026-03-09 14:30
```

### Shebang 的作用

脚本第一行 `#!/usr/bin/env bash` 叫 **Shebang**，告诉系统用哪个程序来解释执行这个文件。

| Shebang | 含义 |
|---------|------|
| `#!/bin/bash` | 用固定路径的 Bash |
| `#!/usr/bin/env bash` | 用 `$PATH` 中找到的 Bash（更可移植） |
| `#!/usr/bin/env python3` | 用 Python 3 |
| `#!/bin/sh` | 用系统默认 sh（可能是 Dash） |

### 脚本健壮性三件套

```bash
#!/usr/bin/env bash
set -euo pipefail
```

| 选项 | 作用 | 类比 |
|------|------|------|
| `set -e` | 任何命令失败立即退出 | 做菜发现食材坏了就停下，别硬做 |
| `set -u` | 引用未定义变量时报错 | 菜谱写了"盐"但厨房里没有，立刻提醒 |
| `set -o pipefail` | 管道中任何命令失败，整条管道失败 | 流水线上某一步出问题就报警 |

> **对你的启发**：所有正式脚本的第二行都应该写 `set -euo pipefail`。这三个选项能帮你在脚本早期发现 90% 的隐性 bug。

---

## 变量 — "食材标签"

### 基本语法

```bash
# 定义变量（= 两边不能有空格！）
name="Docker"
version=20
readonly PI=3.14159    # 只读变量

# 引用变量
echo "学习 ${name} 版本 ${version}"

# 删除变量
unset version
```

> [!warning] 空格陷阱
> `name = "Docker"` ❌ 这会被解析为执行名为 `name` 的命令，参数是 `=` 和 `"Docker"`。
> `name="Docker"` ✅ 赋值语句等号两侧**不能有空格**。

### 引号规则

| 符号 | 行为 | 示例 |
|------|------|------|
| `"双引号"` | 变量替换、命令替换，保留大部分特殊字符 | `"Hello $name"` → `Hello Docker` |
| `'单引号'` | 原样输出，不做任何替换 | `'Hello $name'` → `Hello $name` |
| `` `反引号` `` | 命令替换（旧写法，建议用 `$()` ） | `` echo `date` `` |
| `$()` | 命令替换（推荐） | `echo "今天是 $(date +%A)"` |

### 特殊变量

| 变量 | 含义 | 示例场景 |
|------|------|---------|
| `$0` | 脚本名称 | 打印使用帮助时显示脚本名 |
| `$1` ~ `$9` | 位置参数 | `./deploy.sh production` 中 `$1` = `production` |
| `$#` | 参数个数 | 检查用户是否传入了必要参数 |
| `$@` | 所有参数（保持独立） | 遍历所有传入的参数 |
| `$*` | 所有参数（合为一个字符串） | 少用，通常用 `$@` |
| `$?` | 上一条命令的退出码 | 判断上一步操作是否成功 |
| `$$` | 当前脚本的 PID | 创建唯一的临时文件名 |
| `$!` | 最近一个后台进程的 PID | 等待后台任务完成 |

### 参数扩展 — "食材加工"

> 参数扩展让你在 `${}` 内直接完成字符串操作，无需调用外部命令。

| 语法 | 功能 | 示例 |
|------|------|------|
| `${var:-default}` | 变量为空时用默认值 | `${PORT:-8080}` |
| `${var:=default}` | 变量为空时赋默认值并使用 | `${LOG_DIR:=/var/log}` |
| `${var:?error}` | 变量为空时报错退出 | `${API_KEY:?必须设置 API_KEY}` |
| `${#var}` | 字符串长度 | `${#name}` → `6` |
| `${var#pattern}` | 删除开头最短匹配 | `${path#*/}` |
| `${var##pattern}` | 删除开头最长匹配 | `${path##*/}` → 取文件名 |
| `${var%pattern}` | 删除结尾最短匹配 | `${file%.txt}` → 去扩展名 |
| `${var%%pattern}` | 删除结尾最长匹配 | `${path%%/*}` → 取第一段 |
| `${var/old/new}` | 替换第一个匹配 | `${str/foo/bar}` |
| `${var//old/new}` | 替换所有匹配 | `${str//foo/bar}` |
| `${var^^}` | 转大写 | `${name^^}` → `DOCKER` |
| `${var,,}` | 转小写 | `${NAME,,}` → `docker` |

> **对你的启发**：参数扩展比调用 `sed`/`awk` 处理简单字符串快得多，且不创建子进程。日常使用 `${var:-default}` 和 `${var##*/}` 最高频。

---

## 流程控制 — "烹饪步骤"

### 条件判断 (if)

```bash
#!/usr/bin/env bash
set -euo pipefail

file="/etc/hosts"

if [[ -f "$file" ]]; then
    echo "文件存在，行数：$(wc -l < "$file")"
elif [[ -d "$file" ]]; then
    echo "这是一个目录"
else
    echo "文件不存在"
fi
```

> [!question]- `[ ]` vs `[[ ]]`：用哪个？
> **`[ ]` (test)** — POSIX 标准，兼容所有 Shell，但语法限制多（变量必须加引号、不支持 `&&` / `||`）。
>
> **`[[ ]]`** — Bash/Zsh 扩展，推荐使用。支持模式匹配、正则、`&&` / `||`，变量不加引号也安全。
>
> ```bash
> # [ ] 的坑：变量为空时会语法错误
> [ $var = "hello" ]   # 如果 var 为空 → [ = "hello" ] → 语法错误！
> [ "$var" = "hello" ] # 必须加引号
>
> # [[ ]] 没这个问题
> [[ $var = "hello" ]] # 即使 var 为空也正常工作
> ```

### 常用测试表达式

| 文件测试 | 含义 |
|---------|------|
| `-f file` | 是普通文件 |
| `-d dir` | 是目录 |
| `-e path` | 路径存在 |
| `-r file` | 可读 |
| `-w file` | 可写 |
| `-x file` | 可执行 |
| `-s file` | 文件非空 |

| 字符串测试 | 含义 |
|-----------|------|
| `-z "$str"` | 字符串为空 |
| `-n "$str"` | 字符串非空 |
| `"$a" = "$b"` | 字符串相等 |
| `"$a" != "$b"` | 字符串不等 |

| 数字比较 | 含义 |
|---------|------|
| `-eq` | 等于 |
| `-ne` | 不等于 |
| `-lt` | 小于 |
| `-le` | 小于等于 |
| `-gt` | 大于 |
| `-ge` | 大于等于 |

### 循环

```bash
# for — 遍历列表
for lang in bash zsh fish dash; do
    echo "Shell: $lang"
done

# for — C 风格
for ((i = 0; i < 5; i++)); do
    echo "第 $i 次"
done

# while — 条件循环
count=0
while [[ $count -lt 5 ]]; do
    echo "计数: $count"
    ((count++))
done

# while read — 逐行读取文件（最常用模式）
while IFS= read -r line; do
    echo "行内容: $line"
done < /etc/hosts
```

### case 语句

```bash
case "$1" in
    start)
        echo "启动服务..."
        ;;
    stop)
        echo "停止服务..."
        ;;
    restart)
        echo "重启服务..."
        ;;
    *)
        echo "用法: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

> **对你的启发**：`while IFS= read -r line` 是读取文件最安全的方式——`IFS=` 保留前后空白、`-r` 防止反斜杠转义。写脚本处理文件时优先用这个模式。

---

## 函数 — "子菜谱"

```bash
#!/usr/bin/env bash
set -euo pipefail

log() {
    local level="$1"
    shift
    echo "[$(date '+%H:%M:%S')] [$level] $*"
}

check_dependency() {
    local cmd="$1"
    if ! command -v "$cmd" &>/dev/null; then
        log "ERROR" "缺少依赖: $cmd"
        return 1
    fi
    log "INFO" "$cmd 已安装: $(command -v "$cmd")"
    return 0
}

# 使用
log "INFO" "开始检查环境..."
check_dependency "docker" || exit 1
check_dependency "git" || exit 1
log "INFO" "环境检查通过"
```

| 要点 | 说明 |
|------|------|
| `local` | 声明局部变量，避免污染全局作用域 |
| `$1`, `$2` ... | 函数内也用位置参数接收参数 |
| `shift` | 弹出第一个参数，剩余参数前移 |
| `return N` | 函数返回退出码（0=成功） |
| `$()` 捕获输出 | `result=$(my_func)` 获取函数的 stdout 输出 |

> **对你的启发**：函数里务必用 `local` 声明变量。Bash 函数默认变量是全局的，这是最常见的 bug 来源之一。

---

## 管道与重定向 — "水管系统"

### 管道 (`|`)

> **类比**：管道就像厨房的流水线——洗菜的水槽连接切菜台，切菜台连接炒锅，每个环节只做一件事，上一步的输出直接流入下一步。

```bash
# 统计当前目录下 .sh 文件的数量
ls *.sh | wc -l

# 找出占用内存最多的前 5 个进程
ps aux | sort -k4 -rn | head -5

# 日志分析：找出访问量最大的前 10 个 IP
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

### 重定向

| 语法 | 作用 | 示例 |
|------|------|------|
| `>` | 标准输出写入文件（覆盖） | `echo "hello" > out.txt` |
| `>>` | 标准输出追加到文件 | `echo "world" >> out.txt` |
| `<` | 从文件读取标准输入 | `wc -l < data.txt` |
| `2>` | 标准错误写入文件 | `cmd 2> error.log` |
| `2>&1` | 标准错误合并到标准输出 | `cmd > all.log 2>&1` |
| `&>` | 标准输出 + 标准错误 写入文件 | `cmd &> all.log` |
| `/dev/null` | 丢弃输出（黑洞） | `cmd > /dev/null 2>&1` |

### 进程替换

```bash
# 比较两个命令的输出差异
diff <(ls dir1) <(ls dir2)

# 同时将输出写到文件和屏幕
echo "hello" | tee output.txt

# 将命令输出当作文件处理
while IFS= read -r line; do
    echo "进程: $line"
done < <(ps aux | grep nginx)
```

### Here Document

```bash
cat <<EOF
Dear ${USER},

这是一段多行文本。
变量会被替换。
当前时间: $(date)

EOF

# 不需要变量替换时，引用 EOF
cat <<'EOF'
这里的 $USER 和 $(date) 不会被替换。
原样输出。
EOF
```

> **对你的启发**：管道遵循 Unix 哲学——每个命令做好一件事，通过管道组合。遇到复杂文本处理时，先想"能不能用管道串几个简单命令"。

---

## 文本处理三剑客 — "切菜三件套"

### 定位速查

| 工具 | 厨房类比 | 核心能力 | 口诀 |
|------|---------|---------|------|
| **grep** | 🔍 照明灯 — 找到食材 | 文本搜索与过滤 | **找**行 |
| **sed** | 🔪 菜刀 — 切改食材 | 流式文本编辑 | **改**行 |
| **awk** | 📊 计量秤 — 统计分析 | 按列处理与统计 | **算**列 |

### grep — "找"

```bash
# 基础搜索
grep "error" app.log               # 搜索包含 "error" 的行
grep -i "error" app.log            # 忽略大小写
grep -n "error" app.log            # 显示行号
grep -c "error" app.log            # 统计匹配行数
grep -v "debug" app.log            # 排除包含 "debug" 的行
grep -r "TODO" ./src               # 递归搜索目录

# 正则表达式
grep -E "error|warning" app.log    # 扩展正则（多关键词）
grep -P "\d{4}-\d{2}-\d{2}" log   # Perl 正则（精确匹配日期）

# 上下文
grep -A 3 "Exception" app.log     # 显示匹配行及后 3 行
grep -B 2 "Exception" app.log     # 显示匹配行及前 2 行
grep -C 2 "Exception" app.log     # 显示匹配行及前后各 2 行
```

### sed — "改"

```bash
# 替换
sed 's/old/new/' file              # 替换每行第一个匹配
sed 's/old/new/g' file             # 全局替换
sed -i 's/old/new/g' file          # 直接修改文件（macOS 需 -i ''）

# 行操作
sed '3d' file                      # 删除第 3 行
sed '/pattern/d' file              # 删除匹配的行
sed '/^$/d' file                   # 删除空行
sed -n '10,20p' file               # 只打印第 10~20 行
sed '/start/,/end/d' file          # 删除两个模式之间的行

# 插入
sed '3i\新的第三行' file            # 在第 3 行前插入
sed '3a\追加的行' file              # 在第 3 行后追加

# 实战：批量修改配置
sed -i 's/PORT=3000/PORT=8080/g' .env
```

### awk — "算"

```bash
# 按列提取
awk '{print $1, $3}' data.txt      # 打印第 1 和第 3 列
awk -F ':' '{print $1}' /etc/passwd # 用 : 作分隔符，打印用户名

# 条件过滤
awk '$3 > 100 {print $1, $3}' data.txt  # 第 3 列大于 100 的行

# 统计
awk '{sum += $2} END {print "总计:", sum}' sales.txt
awk '{count[$1]++} END {for (k in count) print k, count[k]}' access.log

# 格式化输出
awk '{printf "%-20s %10.2f\n", $1, $3}' data.txt

# 内置变量
# NR = 当前行号, NF = 当前行的列数, FS = 字段分隔符
awk 'NR > 1 {print NR, $0}' data.txt   # 跳过表头
awk '{print NF}' data.txt               # 打印每行的列数
```

### 三剑客组合实战

```bash
# 场景 1：分析 Nginx 日志，找出 404 最多的 URL 前 10
grep " 404 " access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -10

# 场景 2：统计代码行数（排除空行和注释）
find ./src -name "*.js" | xargs grep -v '^\s*$' | grep -v '^\s*//' | wc -l

# 场景 3：批量重命名文件（.jpeg → .jpg）
for f in *.jpeg; do
    mv "$f" "${f%.jpeg}.jpg"
done

# 场景 4：从 CSV 中提取特定列并汇总
awk -F ',' 'NR > 1 {sum += $3} END {printf "平均值: %.2f\n", sum/(NR-1)}' data.csv
```

> **对你的启发**：掌握 `grep | awk | sort | uniq` 这套组合拳，能解决 80% 的日志分析和数据处理需求。遇到复杂需求再考虑 Python。

---

## 信号处理与 trap — "厨房报警器"

### 常见信号

| 信号 | 编号 | 触发方式 | 用途 |
|------|------|---------|------|
| `SIGINT` | 2 | Ctrl+C | 中断正在运行的脚本 |
| `SIGTERM` | 15 | `kill PID` | 优雅终止（默认 kill 信号） |
| `SIGHUP` | 1 | 终端关闭 | 终端断开时通知进程 |
| `SIGKILL` | 9 | `kill -9 PID` | 强制终止（不可被捕获） |
| `EXIT` | — | 脚本退出时 | 清理临时文件 |

### trap 实战

```bash
#!/usr/bin/env bash
set -euo pipefail

TMPDIR=$(mktemp -d)

cleanup() {
    echo "清理临时文件: $TMPDIR"
    rm -rf "$TMPDIR"
}

trap cleanup EXIT    # 脚本退出时（不论正常/异常）执行清理
trap 'echo "收到 Ctrl+C，正在优雅退出..."; exit 1' INT

echo "临时目录: $TMPDIR"
echo "按 Ctrl+C 测试信号处理..."

# 模拟长时间任务
for i in {1..100}; do
    echo "处理中... $i%"
    sleep 1
done
```

> **对你的启发**：任何创建临时文件/目录的脚本都应该用 `trap cleanup EXIT`。这是防止脚本异常退出后残留垃圾文件的最可靠方式。

---

## 实用模式与最佳实践

### 模式 1：安全的脚本模板

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

usage() {
    cat <<EOF
用法: $SCRIPT_NAME [选项] <参数>

选项:
  -h, --help    显示帮助
  -v, --verbose 详细输出
  -d, --dry-run 试运行（不实际执行）

示例:
  $SCRIPT_NAME -v deploy
  $SCRIPT_NAME --dry-run backup
EOF
}

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
die() { log "ERROR: $*" >&2; exit 1; }

VERBOSE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)    usage; exit 0 ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -d|--dry-run) DRY_RUN=true; shift ;;
        -*)           die "未知选项: $1" ;;
        *)            break ;;
    esac
done

[[ $# -ge 1 ]] || die "缺少必要参数。使用 -h 查看帮助。"

# 主逻辑从这里开始
log "开始执行: $1"
```

### 模式 2：带重试的命令执行

```bash
retry() {
    local max_attempts="${1:-3}"
    local delay="${2:-5}"
    shift 2
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if "$@"; then
            return 0
        fi
        log "WARN" "第 $attempt 次失败，${delay}s 后重试..."
        sleep "$delay"
        ((attempt++))
    done

    log "ERROR" "经过 $max_attempts 次尝试后仍然失败"
    return 1
}

# 使用：最多重试 3 次，间隔 5 秒
retry 3 5 curl -sSf https://api.example.com/health
```

### 模式 3：并行执行与等待

```bash
#!/usr/bin/env bash
set -euo pipefail

pids=()

for server in web-01 web-02 web-03 db-01; do
    echo "部署到 $server..."
    deploy_to "$server" &
    pids+=($!)
done

failed=0
for pid in "${pids[@]}"; do
    if ! wait "$pid"; then
        ((failed++))
    fi
done

if [[ $failed -gt 0 ]]; then
    echo "有 $failed 个部署失败"
    exit 1
fi
echo "全部部署成功"
```

---

## Bash vs Zsh — "中式 vs 西式厨房"

### 核心差异

| 特性 | Bash | Zsh |
|------|------|-----|
| 默认平台 | 大多数 Linux | macOS (2019+) |
| 自动补全 | 基础（需 bash-completion） | 强大（内置、可交互选择） |
| 拼写纠正 | 无 | 内置（`setopt CORRECT`） |
| 通配符 | 基础 glob | 扩展 glob + 递归（`**/*.js`） |
| 自动 cd | 不支持 | 支持（输入目录名即可进入） |
| 插件生态 | 有限 | 丰富（Oh My Zsh、Antigen 等） |
| 配置文件 | `.bashrc` + `.bash_profile` | `.zshrc` + `.zprofile` |
| 脚本兼容性 | POSIX 兼容性好 | 部分语法不兼容 Bash |

### Oh My Zsh 快速配置

```bash
# 安装 Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 常用插件（编辑 ~/.zshrc）
plugins=(
    git                  # Git 别名和补全
    docker               # Docker 命令补全
    zsh-autosuggestions  # 历史命令自动建议
    zsh-syntax-highlighting  # 命令语法高亮
    z                    # 智能目录跳转
)
```

> [!info]- 配置文件加载顺序
> **Bash：**
> - 登录 Shell → `.bash_profile` → `.bashrc`
> - 非登录 Shell → `.bashrc`
>
> **Zsh：**
> - 登录 Shell → `.zprofile` → `.zshrc`
> - 非登录 Shell → `.zshrc`
>
> macOS 终端默认启动的是登录 Shell，所以 `.bash_profile` / `.zprofile` 会被加载。Linux 终端模拟器通常启动非登录 Shell。

> **对你的启发**：交互体验选 Zsh，脚本编写选 Bash。在 `.zshrc` 里配 `zsh-autosuggestions` + `zsh-syntax-highlighting` 两个插件，就能大幅提升命令行效率。

---

## 总结与一页速查

> [!success] Shell 脚本带走的 8 条经验
>
> 1. **`set -euo pipefail` 是必写的第二行** — 让脚本遇错即停、变量未定义即报警
> 2. **变量必须双引号保护** — `"$var"` 而非 `$var`，防止空格和特殊字符引起问题
> 3. **用 `[[ ]]` 代替 `[ ]`** — 更安全、更强大，避免空变量引发语法错误
> 4. **函数里用 `local` 声明变量** — Bash 默认全局变量，不加 `local` 容易踩坑
> 5. **`trap cleanup EXIT` 清理临时资源** — 不论脚本如何退出都能执行清理
> 6. **`while IFS= read -r line` 读文件** — 最安全的逐行处理方式
> 7. **grep 找、sed 改、awk 算** — 三剑客各司其职，管道串联解决 80% 的文本处理需求
> 8. **交互用 Zsh，脚本写 Bash** — 各取所长

### 常用命令速查表

| 需求 | 命令 |
|------|------|
| 找文件 | `find . -name "*.log" -mtime -7` |
| 搜文本 | `grep -rn "TODO" ./src` |
| 替换文本 | `sed -i 's/old/new/g' file` |
| 按列提取 | `awk -F ',' '{print $2}' data.csv` |
| 排序去重 | `sort \| uniq -c \| sort -rn` |
| 统计行数 | `wc -l file` |
| 下载文件 | `curl -sSLO https://example.com/file` |
| 后台运行 | `nohup ./script.sh &` |
| 定时执行 | `crontab -e` → `0 2 * * * /path/to/script.sh` |
| 查看进程 | `ps aux \| grep process_name` |

---

## 参考资料

- [GNU Bash 官方手册](https://www.gnu.org/software/bash/manual/)
- [Advanced Bash-Scripting Guide (TLDP)](https://tldp.org/LDP/abs/html/abs-guide.html)
- [Shell Parameter Expansion](https://www.gnu.org/s/bash/manual/html_node/Shell-Parameter-Expansion.html)
- [Zsh 官方文档](https://zsh.sourceforge.io/Doc/)
- [Oh My Zsh](https://ohmyz.sh/)
- [健壮 Shell 脚本编写指南](https://liujiacai.net/blog/2024/04/05/robust-shell-scripting/)
- [ShellCheck — Shell 脚本静态分析工具](https://www.shellcheck.net/)
