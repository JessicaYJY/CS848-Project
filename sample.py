import bisect
from typing import Dict, List, Tuple, Set, Union
from Relation import Relation
from RangeTree import RangeTree
from Oracles import count_oracle, sub_join_induced_by_box
from split import agm_bound, split
import random


def join_tuples(tuples: List[Tuple[int]], attributes: List[List[str]],
                box_attributes: List[str]) -> Tuple[int]:
    # Create a dictionary to store the joined result
    result_dict = {}

    for tuple_, attrs in zip(tuples, attributes):
        for value, attr in zip(tuple_, attrs):
            result_dict[attr] = value

    # Create the final joined tuple in the order of box_attributes
    result_tuple = tuple(result_dict[attr] for attr in box_attributes)
    return result_tuple


def join_relations(Q: List[Relation], box_attributes: List[str]) -> List[
    Tuple[int]]:
    join_results = []
    for tuple_1 in Q[0].tuples:
        for tuple_2 in Q[1].tuples:
            if tuple_1[Q[0].get_attribute_index("B")] == tuple_2[Q[1].get_attribute_index("B")]:
                joined_tuple = tuple_1[Q[0].get_attribute_index("A")], tuple_1[
                    Q[0].get_attribute_index("B")], tuple_2[Q[1].get_attribute_index("C")]
                join_results.append(joined_tuple)
    return join_results


def sample(W: List[float], Q: List[Relation], box_attributes: List[str]) -> \
Union[str, Dict[str, Union[List[str], Tuple[int]]]]:
    d = len(box_attributes)
    B = [(1, 100)] * d  # Assuming attribute space is [1, 100]^d for simplicity

    while agm_bound(Q, B, box_attributes) >= 2:
        C = split(1, B, Q, box_attributes)
        agm_B = agm_bound(Q, B, box_attributes)

        # Calculate probabilities
        prob = [agm_bound(Q, B_prime, box_attributes) / agm_B for B_prime in C]
        prob.append(1 - sum(prob))  # Probability for B_child = nil

        # Choose B_child with weighted probability
        B_child_index = random.choices(range(len(prob)), weights=prob, k=1)[0]
        if B_child_index == len(prob) - 1:
            return "failure"
        B = C[B_child_index]

    sub_join = sub_join_induced_by_box(Q, B, box_attributes)
    join_result = [tuple_ for relation in sub_join.values() for tuple_ in
                   relation.tuples]

    if not join_result:
        return "failure"

    # Toss a coin with heads probability 1 / agm_bound(Q, B, box_attributes)
    if random.random() < 1 / agm_bound(Q, B, box_attributes):
        # Collect attributes from the relations
        attributes = [relation.attributes for relation in sub_join.values()]
        # Join the tuples based on their common attributes
        joined_tuple = join_tuples(join_result, attributes, box_attributes)
        return {"attribute": box_attributes, "tuple": joined_tuple}

    return "failure"
