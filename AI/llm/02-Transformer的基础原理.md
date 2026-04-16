# Transformer 的基础原理

> Attention 机制如何让机器学会"一目十行"。

## 30 秒心智模型

**核心问题：如何让模型高效处理长序列？**

RNN 的致命缺陷是"记性差"——序列太长时，开头的信息传到结尾早就变形了。

**Transformer 的解决方案：用注意力机制替代序列传递。**

所有词元可以"同时看到"整个序列，根据相关性动态分配权重。不再有一个词等另一个词的串行瓶颈。

---

## 目录

1. [Transformer 之前：RNN 的困境](#1-transformer-之前rnn-的困境)
2. [注意力机制：核心思想](#2-注意力机制核心思想)
3. [自注意力：Transformer 的心脏](#3-自注意力transformer-的心脏)
4. [多头注意力：多角度理解](#4-多头注意力多角度理解)
5. [完整架构：编码器与解码器](#5-完整架构编码器与解码器)
6. [为什么 Transformer 有效](#6-为什么-transformer-有效)

---

## 1. Transformer 之前：RNN 的困境

理解 Transformer 的价值，先要看清 RNN 的问题。

### 循环结构的本质

```
RNN 处理序列

输入: "The cat sat on the mat"

step 1: 处理 "The"  → h1
step 2: 处理 "cat" + h1 → h2   ← h1 的信息要"穿过" h2
step 3: 处理 "sat"  + h2 → h3   ← 信息继续传递，可能已经衰减
step 4: 处理 "on"   + h3 → h4
step 5: 处理 "the"  + h4 → h5
step 6: 处理 "mat"  + h5 → h6   ← 开头的信息还记得多少？
```

### RNN 的三个致命问题

**1. 顺序依赖，无法并行**

第 t 步必须等第 t-1 步算完。训练 1000 个词的句子，GPU 只能串行处理——算力被严重浪费。

**2. 长期依赖问题**

信息从序列开头传到结尾，要经过多次矩阵运算和激活函数。梯度在反向传播时容易消失或爆炸。

> 想象把一句话从中文翻译成英文。开头的主语决定结尾的动词形式——但模型可能早就忘了主语是什么。

**3. 参数量大但效率低**

隐藏状态是固定大小的向量，所有历史信息都被压缩到里面。

---

## 2. 注意力机制：核心思想

注意力（Attention）的灵感来自人类视觉：

> 扫视场景时，焦点不是均匀分布的。我们会重点关注与当前任务相关的区域。

### 查询-键-值框架

Attention 用三个向量来表达这个思想：

```
Query (Q) - "我在找什么"：当前位置的表示
Key (K)   - "我有什么"：每个位置的索引
Value (V) - "我的内容是什么"：每个位置的实际信息
```

### 计算流程

```
Q、K、V 计算过程

Q = X · Wq    K = X · Wk    V = X · Wv
     │            │            │
     ▼            ▼            ▼
  查询向量      键向量        值向量

注意力分数 = Q · Kᵀ / √dk
                │
                ▼
         Softmax → 注意力权重
                │
                ▼
    加权和 = Attention_Weight · V
```

数学表达式：

```
Attention(Q, K, V) = softmax(QKᵀ / √dk) · V
```

### 缩放因子的作用

dk 是 Key 向量的维度。除以 √dk 是为了防止点积过大导致 Softmax 梯度消失。

```
假设 dk = 64：
点积的方差 ≈ dk = 64
√64 = 8

不缩放时：Softmax 趋向 one-hot（梯度几乎为 0）
缩放后：  Softmax 分布更平滑
```

---

## 3. 自注意力：Transformer 的心脏

自注意力（Self-Attention）是 Transformer 的核心——让序列中的每个位置都能"关注"所有其他位置。

### 与普通 Attention 的区别

| | 普通 Attention | Self-Attention |
|---|---|---|
| Q 的来源 | 来自解码器 | 来自输入序列本身 |
| K、V 的来源 | 来自编码器 | 来自输入序列本身 |
| 用途 | 跨模态对齐 | 序列内部关系建模 |

### 自注意力的可视化

```
输入序列: "The animal didn't cross the street because it was too tired"

          "it" 应该关注什么？

The    animal  didn't  cross  the  street  because  it   was  too  tired
  │       │       │       │     │       │       │       │    │     │
  │       │       │       │     │       │       │       │    │     │
  └───┐───┴───────┴───────┴─────┴───────┴───────┴───────┼────┴─────┘
      │                                                      │
      └────────────── 它在计算和所有词的关系 ─────────────────┘

注意力可视化（简化）：

"it" ←→ "animal" 的权重最高（0.9）
"it" ←→ "tired"   的权重次高（0.6）
"it" ←→ "street"  的权重较低（0.1）

模型理解："it" 指的是 "animal"，而"animal" 是 tired 的主语
```

这是 RNN 极难做到的——自注意力用一个数学操作直接捕获了代词指代关系。

### 位置编码：注入序列顺序

Attention 本身是位置无关的——"猫咬人"和"人咬猫"在 Attention 看来是一样的。

Transformer 通过位置编码（Positional Encoding）解决这个问题：

```
PE(pos, 2i)   = sin(pos / 10000^(2i/dmodel))
PE(pos, 2i+1) = cos(pos / 10000^(2i/dmodel))

pos  = 位置 (0, 1, 2, ...)
i    = 维度索引
dmodel = 模型维度
```

用不同频率的正弦余弦函数，每个位置得到一个唯一的"地址标签"。

---

## 4. 多头注意力：多角度理解

单个 Attention 头只能学到一种关系模式。多头注意力（Multi-Head Attention）让模型同时关注不同类型的关系。

```
多头注意力结构

    输入 X
     │
     ├──► Wq₁ ──► Q₁ ──┐
     ├──► Wk₁ ──► K₁ ──┼──► Attention₁ ──┐
     └──► Wv₁ ──► V₁ ──┘                  │
                                          ├─► Concat ──► 输出
     ├──► Wq₂ ──► Q₂ ──┐                  │
     ├──► Wk₂ ──► K₂ ──┼──► Attention₂ ──┘
     └──► Wv₂ ──► V₂ ──┘

     ... (更多注意力头 ...)

     ├──► Wqₕ ──► Qₕ ──┐
     ├──► Wkₕ ──► Kₕ ──┼──► Attentionₕ
     └──► Wvₕ ──► Vₕ ──┘

h = 头的数量（BERT-base 用 12 个头）
每个头独立学习不同的注意力模式
```

### 不同头的典型关注点

```
"机器学习很有趣"

Head₁（句法）: "机器" ← "学习"（主谓关系）
Head₂（语义）: "学习" ← "有趣"（情感关系）
Head₃（共指）: "机器" ← "它"（指代关系）
Head₄（上下文）: 所有词均匀关注（全局信息聚合）
```

每个头像不同专业的"翻译员"，各有专长。

---

## 5. 完整架构：编码器与解码器

原论文《Attention Is All You Need》提出了完整的 Encoder-Decoder 结构：

```
Transformer 整体架构

                    编码器堆栈 (N=6)
    ┌─────────────────────────────────────────────────────┐
    │  Input Embedding + Positional Encoding              │
    │                    ↓                                 │
    │  Multi-Head Self-Attention                          │
    │                    ↓                                 │
    │  Add & Layer Norm                                   │
    │                    ↓                                 │
    │  Feed Forward Network                               │
    │                    ↓                                 │
    │  Add & Layer Norm                                   │
    └─────────────────────────────────────────────────────┘
                           │
                           ↓
                    编码器输出
                           │
                           ↓
                    解码器堆栈 (N=6)
    ┌─────────────────────────────────────────────────────┐
    │  Output Embedding + Positional Encoding             │
    │  (Shifted Right - 右移一位)                         │
    │                    ↓                                 │
    │  Masked Multi-Head Self-Attention                  │
    │  (遮蔽未来位置，确保自回归生成)                      │
    │                    ↓                                 │
    │  Cross-Attention (看向编码器输出)                    │
    │                    ↓                                 │
    │  Feed Forward Network                              │
    └─────────────────────────────────────────────────────┘
                           │
                           ↓
                    Linear + Softmax
                           │
                           ↓
                    下一个词预测
```

### 编码器和解码器的区别

| 组件 | 编码器 | 解码器 |
|------|--------|--------|
| Self-Attention | 完整的双向注意力 | **Masked**（看不到未来） |
| Cross-Attention | 无 | 有（看编码器输出） |
| 用途 | 理解输入 | 生成输出 |

### Masked Self-Attention 的必要性

解码器在生成第 t 个词时，不应该知道第 t+1、t+2... 个词是什么——否则就成"作弊"了。

```
训练时的掩码机制

目标序列: [SOS] 机 器 学 习 [EOS]

位置 0 (SOS): 只能看到 [SOS]          → 预测 "机"
位置 1 (机):  只能看到 [SOS, 机]       → 预测 "器"
位置 2 (器):  只能看到 [SOS, 机, 器]    → 预测 "学"
位置 3 (学):  只能看到 [SOS, 机, 器, 学] → 预测 "习"
位置 4 (习):  只能看到 [SOS, 机, 器, 学, 习] → 预测 [EOS]
位置 5 (EOS): 只能看到 [SOS, 机, 器, 学, 习, EOS] → 预测 结束

通过掩码矩阵实现：

       [SOS] 机  器  学  习 [EOS]
[SOS]   ✓     ✓   ✓   ✓   ✓    ✓
[机]    ✗     ✓   ✓   ✓   ✓    ✓
[器]    ✗     ✗   ✓   ✓   ✓    ✓
[学]    ✗     ✗   ✗   ✓   ✓    ✓
[习]    ✗     ✗   ✗   ✗   ✓    ✓
[EOS]   ✗     ✗   ✗   ✗   ✗    ✓

✓ = 可以attend    ✗ = 被遮蔽
```

---

## 6. 为什么 Transformer 有效

### 并行计算优势

```
RNN vs Transformer 序列处理

RNN（1000步序列）:
  ██████████ ██████████ ██████████ ...  (顺序执行，1000 步)

Transformer:
  ████████████████████████████████  (一步并行，1 步)

速度提升：对于长度为 N 的序列，Attention 计算复杂度 O(N²)，
但由于可以完全并行，实际速度比 RNN 快几十甚至上百倍。
```

### 全局感受野

RNN 的感受野随距离线性增长，而 Transformer 的每个位置都能直接 attending 到任意其他位置——O(1) 的信息访问距离。

### 可扩展性

Transformer 的架构非常适合Scale Up：

```
Transformer 规模演进

模型        年份   参数量      架构创新
Transformer 2017  65M        原始论文
BERT-base   2018  110M      编码器-only
GPT-2       2019  1.5B      解码器-only
GPT-3       2020  175B      In-context Learning
PaLM        2022  540B       Pathways 系统
GPT-4       2023  ~1T       (具体数字未公开)
```

参数越多，模型学到的表示越丰富，涌现能力越强。

### Layer Norm 和残差连接

每个子层都有残差连接和 Layer Norm，保证梯度稳定流动：

```
Add & Layer Norm 结构

      Input
        │
        ├──► 子层计算 ──────────────────┐
        │                               │
        │                               ▼
        └───── Add (残差) ──► LayerNorm ──► Output
                                  ↑
                                  │
                          mean = 0, std = 1
                          + 可学习的 γ, β
```

---

## 总结

```
Transformer 核心组件

┌──────────────────────────────────────────────────────┐
│                                                      │
│   输入Embedding + 位置编码                           │
│            ↓                                         │
│   ┌─────────────────────────────────────────────┐   │
│   │           Multi-Head Self-Attention          │   │
│   │                                             │   │
│   │   三个核心问题：                              │   │
│   │   - Q: 我在找什么？                          │   │
│   │   - K: 每个位置有什么特征？                   │   │
│   │   - V: 每个位置的实际内容？                   │   │
│   │                                             │   │
│   │   答案：QKᵀ 相关度 × V 的加权和              │   │
│   └─────────────────────────────────────────────┘   │
│            ↓                                         │
│         Add & Norm                                    │
│            ↓                                         │
│   ┌─────────────────────────────────────────────┐   │
│   │           Feed Forward Network              │   │
│   │                                             │   │
│   │   FFN(x) = ReLU(xW₁ + b₁)W₂ + b₂            │   │
│   └─────────────────────────────────────────────┘   │
│            ↓                                         │
│         Add & Norm                                   │
│            ↓                                         │
│         堆叠 N 层                                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Transformer 的核心洞察很简单：**用全局注意力替代序列传递，让信息流动不再受距离限制。** 这个看似简单的改变，开启了大模型时代的大门。

---

## 来源

- Vaswani et al. (2017). Attention Is All You Need. NeurIPS.
- Bahdanau et al. (2014). Neural Machine Translation by Jointly Learning to Align and Translate.
- Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.
