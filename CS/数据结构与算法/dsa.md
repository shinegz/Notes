<img src="D:\Notes\CS\数据结构与算法\数据结构与算法\刷题指南.jpg"  />

## 基础

### 数组

> 顺序（连续）存储结构的线性表，每个元素都有一个唯一的索引
>
> **数组的访问效率较高，而插入效率较低**

#### 添加数组元素的方法

+ unshift（首部添加）
+ push（尾部添加）
+ splice（任意位置）

#### 删除数组元素的方法

+ shift（首部删除）
+ pop（尾部删除）
+ splice（任意位置）



### 栈

> 后进先出（Last in First out）的线性表（限定了操作的线性表），且只能在栈尾进行添加删除操作

### 队列

> 先进先出（First in First out）的线性表（限定了操作的线性表），且只能在队尾添加，在队首删除

1. 栈向队列的转化
2. 双端队列：**双端队列就是允许在队列的两端进行插入和删除的队列**
3. 优先队列



### 链表

> 链式（离散）存储结构的线性表，链表中的每个节点（元素）由数据域（存储值）和指针域（指向下一个节点）组成
>
> **链表的插入/删除效率较高，而访问效率较低**

链表题目分类：

- 链表的处理：合并、删除等（删除操作画个记号，重点中的重点！）
- 链表的反转及其衍生题目
- 链表成环问题及其衍生题目



### 树与递归

#### 树的相关概念

- 树的层次计算规则：根结点所在的那一层记为第一层，其子结点所在的就是第二层，以此类推。
- 结点和树的“高度”计算规则：叶子结点高度记为1，每向上一层高度就加1，逐层向上累加至目标结点时，所得到的的值就是目标结点的高度。树中结点的最大高度，称为“树的高度”。
- “度”的概念：一个结点开叉出去多少个子树，被记为结点的“度”。
- “叶子结点”：叶子结点就是度为0的结点。

#### 二叉树

- 它可以没有根结点，作为一棵空树存在
- 如果它不是空树，那么**必须由根结点、左子树和右子树组成，且左右子树都是二叉树**。

##### 二叉树的遍历

按顺序规则划分：

+ 先序遍历：**根节点** -> 左子树 -> 右子树
+ 中序遍历：左子树 -> **根节点** -> 右子树
+ 后序遍历：左子树 -> 右子树 -> **根节点**
+ 层序遍历

按实现方式划分：

+ 递归遍历（前、中、后遍历）
+ 迭代遍历（层次遍历）



##### 二叉搜索树（BST）

> 1. 是一棵空树
> 2. 是一棵由根结点、左子树、右子树组成的树，同时左子树和右子树都是二叉搜索树，且**左子树**上所有结点的数据域都**小于等于**根结点的数据域，**右子树**上所有结点的数据域都**大于等于**根结点的数据域
>
> 满足以上两个条件之一的二叉树，就是二叉搜索树。

二叉搜索树的特性：中序遍历结果为有序数组

常见考点：

+ 查找数据域为某一特定值的结点

  ```javascript
  /**
   * @param {TreeNode} root
   * @param {number} val
   * @return {TreeNode}
   */
  var searchBST = function(root, val) {
      if (!root) {
          return null;
      }
  
      if (root.val === val) {
          return root;
      } else if (root.val > val) {
          return searchBST(root.left, val);
      } else {
          return searchBST(root.right, val);
      }
  };
  ```

+ 插入新结点

  ```javascript
  /**
   * @param {TreeNode} root
   * @param {number} val
   * @return {TreeNode}
   */
  var insertIntoBST = function(root, val) {
      // 递归边界
     if (!root) {
         return new TreeNode(val);
     }
  
     if (root.val > val) {
         root.left = insertIntoBST(root.left, val);
     } else {
         root.right = insertIntoBST(root.right, val);
     }
  
     return root;
  };
  ```

+ 删除指定结点

  ```javascript
  /**
   * @param {TreeNode} root
   * @param {number} key
   * @return {TreeNode}
   */
  var deleteNode = function(root, n) {
      if (!root) {
          return null;
      }
  
      if (root.val === n) {
          // 目标节点为叶子节点
          if (!root.left && !root.right) {
              root = null;
          } else if (root.left) {
              const maxLeft = findMax(root.left);
              root.val = maxLeft.val;
              root.left = deleteNode(root.left, maxLeft.val);
          } else {
              const minRight = findMin(root.right);
              root.val = minRight.val;
              root.right = deleteNode(root.right, minRight);
          }
      } else if (root.val > n) {
          root.left = deleteNode(root.left, n);
      } else {
          root.right = deleteNode(root.right, n);
      }
  
      return root;
  };
  
  function findMax (root) {
      while (root.right) {
          root = root.right;
      }
  
      return root;
  }
  
  function findMin (root) {
      while (root.left) {
          root = root.left
      }
  
      return root;
  }
  ```

+ 二叉搜索树的判定

  ```javascript
  /**
   * @param {TreeNode} root
   * @return {boolean}
   */
  var isValidBST = function(root) {
      
      function dfs (root, minValue, maxValue) {
          if (!root) {
              return true;
          }
  
          if (root.val <= minValue || root.val >= maxValue) return false;
  
          return dfs(root.left, minValue, root.val) && dfs(root.right, root.val, maxValue);
      }
  
      return dfs(root, -Infinity, +Infinity);
  };
  ```

  



##### 平衡二叉树（AVL Tree）

> **任意结点**的**左右子树高度差绝对值都不大于1**的二叉**搜索树**

常见考点：

+ 平衡二叉树的判定

  > 平衡二叉树中的任一节点的左右子树的高度差的绝对值不大于1。

  ```javascript
  /**
   * @param {TreeNode} root
   * @return {boolean}
   */
  var isBalanced = function(root) {
      let flag = true;
  
      function dfs (root) {
          if (!root) {
              return 0;
          }
  
          const left = dfs(root.left) + 1;
          const right = dfs(root.right) + 1;
  
          if (Math.abs(left - right) > 1) flag = false;
  
          return Math.max(left, right);
      }
  
      dfs(root);
  
      return flag;
  };
  ```

+ 平衡二叉树的构造（一般是将一颗二叉搜索树转换为平衡二叉树）

  > 思路：先对二叉搜索树进行中序遍历得到一个有序数组（利用了二叉搜索树的特性），再根据有序数组构造平衡二叉树。



##### 堆结构



#### 递归

> 当一个函数直接或间接的调用自身时，这个函数就称为递归函数。
>
> 递归函数的两要素：
>
> + 递归式（重复的内容）
> + 递归边界（停止继续调用自身的条件）

**适用场景：需要重复执行某个操作时**

递归与栈紧密相连：

​								进栈：函数调用自己

​								出栈：函数返回



### 哈希表

> 键值映射结构。
>
> **哈希表查找键值的时间复杂度为O(1)**

**适用场景：需要记录下一些对应关系**



### 双指针

> 双指针的本质是缩小问题的规模



## 思想

### 二分

### 滑动窗口

### 搜索

#### DFS（穷举法）

#### BFS

### 动态规划



## 提高

+ 贪心
+ 分治
+ 位运算
+ KMP&RK
+ 并查集
+ 前缀树
+ 线段树
+ 堆



## 解题模板

确定解题模板的思路

+ 什么时候用？（明确场景）
+ 为什么这样用？（提供依据）
+ 怎么用？（细化步骤）

### 递归与回溯问题解题模板

#### 什么时候用

看两个特征：

+ 题目中暗示了一个或多个解，并且要求我们详细地列举出每一个解的内容时，一定要想到递归回溯
+ 题目经分析后，可以转化为树形逻辑模型求解



#### 为什么这样用

递归与回溯的过程，本身就是穷举的过程。题目中要求我们列举每一个解的内容，解从哪来，解是基于穷举思想，对搜索树进行适当地剪枝后得来的



#### 怎么用（找“坑位”，画树形逻辑模型）

**一个模型——树形逻辑模型**；两个要点——递归式和递归边界。
树形逻辑模型的构建，**关键在于找“坑位”，一个坑位就对应树中的一层（坑位往往是哪些不会变的东西）**，每一层的处理逻辑往往是一样的，这个逻辑就是递归式的内容。至于递归边界，要么在题目中约束得非常清楚、要么默认为**“坑位”数量的边界**。 
用伪代码总结一下编码形式，大部分的题解都符合以下特征： 

```javascript
function xxx(入参) {
  前期的变量定义、缓存等准备工作 
  
  // 定义路径栈
  const path = []
  
  // 进入 dfs
  dfs(起点)
  
  // 定义 dfs 递归的过程就是去填坑的过程
  dfs(递归参数(坑位)) {
    if(到达了递归边界) {
      结合题意处理边界逻辑，往往和 path 内容有关
      return
    }
    
    // 注意这里也可能不是 for，视题意决定
    // 填坑
    for(遍历坑位的可选值) {
      path.push(当前选中值)
      处理坑位本身的相关逻辑
      path.pop()
    }
  }
}
```