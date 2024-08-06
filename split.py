import bisect
from typing import List, Tuple, Set
from Relation import Relation
from RangeTree import RangeTree
from Oracles import count_oracle, median_oracle


def agm_bound(Q: List[Relation], box: List[Tuple[int, int]],
              box_attributes: List[str]) -> float:
    agm_w_b = 1.0
    for relation in Q:
        re_b = count_oracle(relation, box, box_attributes)
        agm_w_b *= re_b
    return agm_w_b


def replace(box: List[Tuple[int, int]], i: int, interval: Tuple[int, int]) -> \
List[Tuple[int, int]]:
    new_box = box.copy()
    new_box[i] = interval
    return new_box


def split(i: int, B: List[Tuple[int, int]], Q: List[Relation],
          box_attributes: List[str]) -> List[List[Tuple[int, int]]]:
    C = []
    x_i, y_i = B[i]
    B_agm = agm_bound(Q, B, box_attributes)

    # def condition(z: int) -> bool:
    #     B_left = replace(B, i, (x_i, z - 1))
    #     return agm_bound(Q, B_left, box_attributes) <= 0.5 * B_agm
    #
    # # Binary search to find the largest z
    # z = x_i
    # low, high = x_i, y_i
    # while low <= high:
    #     mid = (low + high) // 2
    #     if condition(mid):
    #         z = mid
    #         low = mid + 1
    #     else:
    #         high = mid - 1

    while True:
        z = median_oracle(Q, box_attributes[i], B, box_attributes)
        B_left = replace(B, i, (x_i, z - 1))
        if agm_bound(Q, B_left, box_attributes) <= 0.5 * B_agm:
            break
        else:
            y_i = z - 1

    # Create B_left, B_mid, B_right
    if z - 1 >= x_i:
        B_left = replace(B, i, (x_i, z - 1))
        C.append(B_left)

    B_mid = replace(B, i, (z, z))
    if i == len(B) - 1:
        C.append(B_mid)
    else:
        C.extend(split(i + 1, B_mid, Q, box_attributes))

    if z + 1 <= y_i:
        B_right = replace(B, i, (z + 1, y_i))
        C.append(B_right)

    return C
