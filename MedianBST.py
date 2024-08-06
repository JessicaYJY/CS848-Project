class TreeNode:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None
        self.count = 1  # Node count including itself

class MedianBST:
    def __init__(self):
        self.root = None

    def _insert(self, node: TreeNode, value: int) -> TreeNode:
        if not node:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        node.count += 1
        return node

    def insert(self, value: int):
        self.root = self._insert(self.root, value)

    def _find_kth(self, node: TreeNode, k: int) -> int:
        if not node:
            raise ValueError("k is out of the bounds of the tree size")

        left_count = node.left.count if node.left else 0
        if k == left_count + 1:
            return node.value
        elif k <= left_count:
            return self._find_kth(node.left, k)
        else:
            return self._find_kth(node.right, k - left_count - 1)

    def find_median(self) -> int:
        if not self.root:
            raise ValueError("Tree is empty")
        total_count = self.root.count
        # Median is the ⌈n/2⌉-th smallest value, which is (total_count // 2) + 1
        median_index = (total_count // 2) + 1
        return self._find_kth(self.root, median_index)
