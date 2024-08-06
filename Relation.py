import bisect
import random
from typing import List, Tuple, Set, Dict, Union


# Define the Relation
class Relation:
    def __init__(self, name: str, attributes: List[str],
                 tuples: List[Tuple[int]]):
        self.name = name
        self.attributes = attributes
        self.tuples = tuples

    def get_attribute_index(self, attr: str) -> int:
        return self.attributes.index(attr)

    def get_sub_relation(self, box: List[Tuple[int, int]],
                         box_attributes: List[str]) -> 'Relation':
        sub_tuples = [tuple_ for tuple_ in self.tuples if
                      check_tuple_in_box(self, tuple_, box, box_attributes)]
        return Relation(self.name, self.attributes, sub_tuples)

def check_tuple_in_box(relation: Relation, tuple_: Tuple[int], box: List[Tuple[int, int]], box_attributes: List[str]) -> bool:
    for attr in relation.attributes:
        attr_index_in_relation = relation.get_attribute_index(attr)
        attr_index_in_box = box_attributes.index(attr)
        if not (box[attr_index_in_box][0] <= tuple_[attr_index_in_relation] <= box[attr_index_in_box][1]):
            return False
    return True
