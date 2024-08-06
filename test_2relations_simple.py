import bisect
import time
from typing import Dict, List, Tuple, Set, Union
from Relation import Relation
from RangeTree import RangeTree
from Oracles import count_oracle, median_oracle, sub_join_induced_by_box
from sample import join_relations, sample
from split import agm_bound, replace, split
import random


def calculate_success_probability(Q: List[Relation], box_attributes: List[str],
                                  W: List[float]) -> float:
    # Calculate OUT as the actual join output size
    join_output = join_relations(Q, box_attributes)
    OUT = len(join_output)

    # Calculate AGM_W(Q)
    B = [(1, 100)] * len(box_attributes)  # Assuming attribute space is [1, 100]^d for simplicity
    AGM_W_Q = agm_bound(Q, B, box_attributes)

    return OUT / AGM_W_Q


def test_sampling_algorithm(Q: List[Relation], box_attributes: List[str],
                            W: List[float], num_trials: int) -> float:
    success_count = 0
    sample_results = []
    start_time = time.time()

    for _ in range(num_trials):
        # print(_)
        s = sample(W, Q, box_attributes)
        if s != "failure":
            success_count += 1
            sample_results.append(s)
    end_time = time.time()

    print(f"Time taken for {num_trials} trials: {end_time - start_time} seconds")

    return success_count / num_trials, sample_results


def run_sampling_algorithm(Q: List[Relation], box_attributes: List[str],
                            W: List[float], num_samples: int) -> List[Dict[str, Union[List[str], Tuple[int]]]]:
    samples = []
    sample_count = 0
    start_time = time.time()
    trail_count = 0


    while sample_count < num_samples:
        trail_count += 1
        result = sample(W, Q, box_attributes)
        if result != "failure":
            samples.append(result)
            sample_count += 1
            # print(sample_count)
    end_time = time.time()

    print(f"Time taken for {num_samples} samples: {end_time - start_time} seconds")
    print(f"Trail count for {num_samples} samples: {trail_count} trails")
    return samples


if __name__ == '__main__':

    # Example usage
    R1 = Relation("R1", ["A", "B"], [(1, 2), (3, 4), (5, 6)])
    R2 = Relation("R2", ["B", "C"], [(2, 3), (4, 5), (6, 7)])
    Q = [R1, R2]

    box_attributes = ["A", "B", "C"]
    W = [1, 1]  # Example fractional edge covering

    # Example usage of count_oracle, Expected output: 3
    print(count_oracle(R1, [(1, 5), (2, 6), (3, 7)], box_attributes))
    # Example usage of count_oracle, Expected output: 3
    print(count_oracle(R2, [(1, 5), (2, 6), (3, 7)], box_attributes))
    # Example usage of median_oracle,  Expected output: 4
    print(median_oracle(Q, "B", [(1, 5), (2, 6), (3, 7)], box_attributes))

    # Calculate Q(B) - the sub join introduced by B
    sub_join = sub_join_induced_by_box(Q, [(1, 5), (2, 6), (3, 7)], box_attributes)
    for name, sub_relation in sub_join.items():
        print(f"Sub-relation {name}: {sub_relation.tuples}")

    # Calculate AGM_W(B), Expected output: 9
    print(f"AGM_W(B): {agm_bound(Q, [(1, 5), (2, 6), (3, 7)], box_attributes)}")

    # Example usage of replace function
    # Should replace the second interval with (3, 4)
    # Expected output: [(1, 5), (3, 4), (3, 7)]
    new_box = replace([(1, 5), (2, 6), (3, 7)], 1, (3, 4))
    print(f"Original box: {[(1, 5), (2, 6), (3, 7)]}")
    print(f"New box after replace: {new_box}")

    # Example usage of split function
    # The split boxes should be at most 2d+1, where d is the number of attributes in Q
    # The boxes should be disjoint and have B as their union
    split_result = split(0, [(1, 5), (2, 6), (3, 7)], Q, box_attributes)
    print(f"Split result: {split_result}")
    # Split result:
    # [[(1, 2), (2, 6), (3, 7)],
    # [(3, 3), (2, 3), (3, 7)],
    # [(3, 3), (4, 4), (3, 4)],
    # [(3, 3), (4, 4), (5, 5)],
    # [(3, 3), (4, 4), (6, 7)],
    # [(3, 3), (5, 6), (3, 7)],
    # [(4, 5), (2, 6), (3, 7)]]

    # Example usage of sample function
    sample_result = sample(W, Q, box_attributes)
    print(f"Sample result: {sample_result}")

    # Calculate success probability for the simple example
    # Theoretical success probability: 0.3333333333333333
    theoretical_prob = calculate_success_probability(Q, box_attributes, W)
    print(f"Theoretical success probability: {theoretical_prob}")

    # Test the sampling algorithm with 1000 trials using the simple example
    # The empirical success probability should be close to the theoretical probability
    num_trials = 1000
    empirical_prob, sample_result = test_sampling_algorithm(Q, box_attributes, W, num_trials)
    print(f"Empirical success probability after {num_trials} trials: {empirical_prob}")
    print(sample_result[:10])  # Print the first 10 sample results

    # Run sampling algorithm
    num_samples = 1000
    samples = run_sampling_algorithm(Q, box_attributes, W, num_samples)

    # Save samples to file
    print(samples)
    # save_samples_to_file(samples, "sampled_results.txt")
