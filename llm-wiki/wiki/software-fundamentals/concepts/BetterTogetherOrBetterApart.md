---
title: "Better Together or Better Apart"
type: concept
tags: [software-design, module-decomposition, coupling, cohesion]
sources:
  - software-fundamentals/sources/posd-2nd-edition
last_updated: "2026-05-02"
---

## 一句话理解

模块应该放在一起还是分开，取决于它们是否共享同一变化原因——共享则合，分离则解耦。

## 背景

软件设计中的经典问题是"什么时候把东西放在一起，什么时候分开"。没有简单规则，需要分析变化的原因和频率。

## 核心机制

### 合并的信号

- 两个模块因同一原因需要改变
- 两个模块共享共同的概念模型
- 一个模块的存在是为了支持另一个

### 分离的信号

- 模块有独立的变化原因
- 维护独立状态
- 接口可以完全独立定义

### 例子：文本编辑器

```python
# 合并：文本存储和文本格式都依赖于"文本内容"
class TextManager:
    def load(self): ...
    def format(self): ...

# 分离：文本存储和撤销历史有独立变化原因
class TextStore:
    def load(self): ...

class UndoManager:
    def undo(self): ...
```

## 关联概念

- [[software-fundamentals/concepts/Orthogonality|Orthogonality]] — 正交组件应分离，非正交组件应合并
- [[software-fundamentals/concepts/SoftwareArchitecture|Software Architecture]] — 模块分解是架构设计的核心决策
- [[software-fundamentals/concepts/GeneralPurposeModules|General-Purpose Modules are Deeper]] — 分解后的模块应追求通用目的

## 来源

- [[software-fundamentals/sources/posd-2nd-edition|A Philosophy of Software Design]] — Ch 9
