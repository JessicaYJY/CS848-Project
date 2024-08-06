import bisect
from typing import List, Tuple, Set
from Relation import Relation

class RangeTree:
    def __init__(self, points: List[Tuple[int]]):
        self.points = sorted(points)

    def range_count(self, box: List[Tuple[int, int]], box_attributes: List[str],
                    relation_attributes: List[str]) -> int:
        count = 0
        for point in self.points:
            if all(box[box_attributes.index(attr)][0] <= point[
                relation_attributes.index(attr)] <=
                   box[box_attributes.index(attr)][1] for attr in
                   relation_attributes):
                count += 1
        return count
