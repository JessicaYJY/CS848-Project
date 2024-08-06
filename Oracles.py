import bisect
from typing import List, Tuple, Set, Dict
from Relation import Relation
from RangeTree import RangeTree
from MedianBST import MedianBST

def check_tuple_in_box(relation: Relation, tuple_: Tuple[int], box: List[Tuple[int, int]], box_attributes: List[str]) -> bool:
    for attr in relation.attributes:
        attr_index_in_relation = relation.get_attribute_index(attr)
        attr_index_in_box = box_attributes.index(attr)
        if not (box[attr_index_in_box][0] <= tuple_[attr_index_in_relation] <= box[attr_index_in_box][1]):
            return False
    return True

def count_oracle(relation: Relation, box: List[Tuple[int, int]], box_attributes: List[str]) -> int:
    points = [tuple_ for tuple_ in relation.tuples if check_tuple_in_box(relation, tuple_, box, box_attributes)]
    range_tree = RangeTree(points)
    return range_tree.range_count(box, box_attributes, relation.attributes)

def get_active_domain(Q: List[Relation], X: str, box: List[Tuple[int, int]], box_attributes: List[str]) -> Set[int]:
    active_domain = set()
    for relation in Q:
        if X in relation.attributes:
            attr_index = relation.get_attribute_index(X)
            for tuple_ in relation.tuples:
                if check_tuple_in_box(relation, tuple_, box, box_attributes):
                    active_domain.add(tuple_[attr_index])
    return active_domain

def median_oracle(Q: List[Relation], X: str, box: List[Tuple[int, int]], box_attributes: List[str]) -> int:
    active_domain = get_active_domain(Q, X, box, box_attributes)
    median_bst = MedianBST()
    for value in active_domain:
        median_bst.insert(value)
    return median_bst.find_median()

def sub_join(Q: List[Relation], box: List[Tuple[int, int]], box_attributes: List[str]) -> Dict[str, List[Tuple[int]]]:
    sub_join_result = {}
    for relation in Q:
        sub_relation = [tuple_ for tuple_ in relation.tuples if check_tuple_in_box(relation, tuple_, box, box_attributes)]
        sub_join_result[relation.name] = sub_relation
    return sub_join_result

def sub_join_induced_by_box(Q: List[Relation], box: List[Tuple[int, int]], box_attributes: List[str]) -> Dict[str, Relation]:
    sub_join = {}
    for relation in Q:
        sub_relation = relation.get_sub_relation(box, box_attributes)
        sub_join[relation.name] = sub_relation
    return sub_join


if __name__ == '__main__':

    # Example usage
    R1 = Relation("R1", ["A", "B"], [(1, 2), (3, 4), (5, 6)])
    R2 = Relation("R2", ["B", "C"], [(2, 3), (4, 5), (6, 7)])
    Q = [R1, R2]

    box = [(1, 5), (2, 6), (3, 7)]
    box_attributes = ["A", "B", "C"]

    print(count_oracle(R1, box, box_attributes))  # Example usage of count_oracle
    print(count_oracle(R2, box, box_attributes))  # Example usage of count_oracle

    print(median_oracle(Q, "A", box, box_attributes))  # Example usage of median_oracle
    print(median_oracle(Q, "B", box, box_attributes))  # Example usage of median_oracle
    print(median_oracle(Q, "C", box, box_attributes))  # Example usage of median_oracle

    print(sub_join(Q, box, box_attributes))  # Example usage of sub_join
    # Calculate Q(B)
    sub_join = sub_join_induced_by_box(Q, box, box_attributes)
    print(sub_join)
    for name, sub_relation in sub_join.items():
        print(f"Sub-relation {name}: {sub_relation.tuples}")
