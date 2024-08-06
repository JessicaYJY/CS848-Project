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
    join_output = join_relations(Q, box_attributes)
    OUT = len(join_output)

    B = [(0, 10)] * len(box_attributes)
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


def generate_unique_random_data(num_tuples: int, value_range: Tuple[int, int]) -> List[Tuple[int, int]]:
    unique_data = set()
    while len(unique_data) < num_tuples:
        new_tuple = (random.randint(value_range[0], value_range[1]), random.randint(value_range[0], value_range[1]))
        unique_data.add(new_tuple)
    return list(unique_data)


def save_to_file(filename: str, data: List[Tuple[int, int]]):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item[0]},{item[1]}\n")


def read_from_file(filename: str) -> List[Tuple[int, int]]:
    data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            data.append((int(parts[0]), int(parts[1])))
    return data




if __name__ == '__main__':
    # num_tuples = 100
    # value_range = (0, 10)
    #
    # R1_data = generate_unique_random_data(num_tuples, value_range)
    # R2_data = generate_unique_random_data(num_tuples, value_range)
    #
    # save_to_file("R1_data.txt", R1_data)
    # save_to_file("R2_data.txt", R2_data)
    #
    # print("Unique random data saved to R1_data.txt and R2_data.txt")

    R1_data = read_from_file("R1_data.txt")
    R2_data = read_from_file("R2_data.txt")

    R1 = Relation("R1", ["A", "B"], R1_data)
    R2 = Relation("R2", ["B", "C"], R2_data)
    Q = [R1, R2]

    box_attributes = ["A", "B", "C"]
    W = [1.5, 1.5]




    # Example usage of count_oracle
    print(count_oracle(R1, [(0, 10), (0, 10), (0, 10)], box_attributes))
    print(count_oracle(R2, [(0, 10), (0, 10), (0, 10)], box_attributes))

    # Example usage of median_oracle
    print(median_oracle(Q, "B", [(0, 10), (0, 10), (0, 10)], box_attributes))

    # Calculate sub join induced by box
    sub_join = sub_join_induced_by_box(Q, [(0, 10), (0, 10), (0, 10)], box_attributes)
    for name, sub_relation in sub_join.items():
        print(f"Sub-relation {name}: {sub_relation.tuples}")

    # Calculate AGM_W(B)
    print(f"AGM_W(B): {agm_bound(Q, [(0, 10), (0, 10), (0, 10)], box_attributes)}")

    # Example usage of replace function
    new_box = replace([(0, 10), (0, 10), (0, 10)], 1, (5, 7))
    print(f"Original box: {[(0, 10), (0, 10), (0, 10)]}")
    print(f"New box after replace: {new_box}")

    # Example usage of split function
    split_result = split(0, [(0, 10), (0, 10), (0, 10)], Q, box_attributes)
    print(f"Split result: {split_result}")

    # Example usage of sample function
    sample_result = sample(W, Q, box_attributes)
    print(f"Sample result: {sample_result}")

    # Calculate success probability
    theoretical_prob = calculate_success_probability(Q, box_attributes, W)
    print(f"Theoretical success probability: {theoretical_prob}")

    # Test the sampling algorithm with 1000 trials
    num_trials = 1000
    empirical_prob, sample_result = test_sampling_algorithm(Q, box_attributes, W, num_trials)
    print(f"Empirical success probability after {num_trials} trials: {empirical_prob}")
    print(sample_result[:10])

    # Run sampling algorithm until 1000 samples are obtained
    num_samples = 1000
    samples = run_sampling_algorithm(Q, box_attributes, W, num_samples)

    # Save samples to file
    print(samples)
    # save_samples_to_file(samples, "sampled_results.txt")
