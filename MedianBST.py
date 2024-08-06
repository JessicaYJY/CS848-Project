import bisect
from typing import List, Tuple, Set
from Relation import Relation
from RangeTree import RangeTree


# class MedianBST:
#     def __init__(self):
#         self.elements = []
#
#     def insert(self, value: int):
#         bisect.insort(self.elements, value)
#
#     def find_median(self) -> int:
#         n = len(self.elements)
#         return self.elements[(n - 1) // 2]


class Node:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None
        self.size = 1  # size of the subtree rooted at this node


class MedianBST:
    def __init__(self):
        self.root = None

    def _insert(self, root: Node, value: int) -> Node:
        if not root:
            return Node(value)
        if value < root.value:
            root.left = self._insert(root.left, value)
        else:
            root.right = self._insert(root.right, value)
        root.size += 1
        return root

    def insert(self, value: int):
        self.root = self._insert(self.root, value)

    def _find_kth(self, root: Node, k: int) -> Node:
        left_size = root.left.size if root.left else 0
        if k == left_size + 1:
            return root
        elif k <= left_size:
            return self._find_kth(root.left, k)
        else:
            return self._find_kth(root.right, k - left_size - 1)

    def find_median(self) -> float:
        if not self.root:
            return None
        n = self.root.size
        if n % 2 == 1:
            return self._find_kth(self.root, n // 2 + 1).value
        else:
            left = self._find_kth(self.root, n // 2).value
            right = self._find_kth(self.root, n // 2 + 1).value
            return (left + right) / 2.0
