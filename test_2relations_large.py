import bisect
import time
from typing import Dict, List, Tuple, Set, Union
from Relation import Relation
from RangeTree import RangeTree
from Oracles import count_oracle, median_oracle, sub_join_induced_by_box
from Sample import join_relations, sample
from Split import agm_bound, replace, split
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

        # Print the current testing percentage as a progress bar
        progress = (_ + 1) / num_trials
        bar_length = 20
        progress_bar = '=' * int(progress * bar_length)
        percentage = progress * 100
        print(f"\r{progress_bar:<{bar_length}} {percentage:.0f}%", end='')

    end_time = time.time()
    print("\n")
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

            # Print the current testing percentage as a progress bar
            progress = (sample_count) / num_samples
            bar_length = 20
            progress_bar = '=' * int(progress * bar_length)
            percentage = progress * 100
            print(f"\r{progress_bar:<{bar_length}} {percentage:.0f}%", end='')

    end_time = time.time()
    print("\n")
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
def save_samples_to_file(samples: List[Dict[str, Union[List[str], Tuple[int]]]],
                         file_path: str):
    with open(file_path, 'w') as f:
        f.write("A\tB\tC\n")
        for sample in samples:
            tuple_ = sample["tuple"]
            f.write("\t".join(map(str, tuple_)) + "\n")


if __name__ == '__main__':

    # Generate random data for R1 and R2 by uncommenting the following code
    # num_tuples = 100
    # value_range = (0, 10)
    #
    # R1_data = generate_unique_random_data(num_tuples, value_range)
    # R2_data = generate_unique_random_data(num_tuples, value_range)
    #
    # save_to_file("data/R1_data.txt", R1_data)
    # save_to_file("data/R2_data.txt", R2_data)
    #
    # print("Unique random data saved to R1_data.txt and R2_data.txt")


    # Load data from file
    R1_data = read_from_file("data/R1_data.txt")
    R2_data = read_from_file("data/R2_data.txt")

    R1 = Relation("R1", ["A", "B"], R1_data)
    R2 = Relation("R2", ["B", "C"], R2_data)
    Q = [R1, R2]

    box_attributes = ["A", "B", "C"]
    W = [1.5, 1.5]




    # Example usage of count_oracle
    print("Example usage of count_oracle, Expected output: 100")
    print(count_oracle(R1, [(0, 10), (0, 10), (0, 10)], box_attributes))
    print("Example usage of count_oracle, Expected output: 100")
    print(count_oracle(R2, [(0, 10), (0, 10), (0, 10)], box_attributes))
    print("\n")

    # Example usage of median_oracle
    print("Example usage of median_oracle, Expected output: 5")
    print(median_oracle(Q, "B", [(0, 10), (0, 10), (0, 10)], box_attributes))
    print("\n")

    # Calculate sub join induced by box
    print("Example of calculating sub join introduced by B:")
    sub_join = sub_join_induced_by_box(Q, [(0, 10), (0, 10), (0, 10)], box_attributes)
    for name, sub_relation in sub_join.items():
        print(f"Sub-relation {name}: {sub_relation.tuples}")
    print("\n")

    # Calculate AGM_W(B)
    print("Example to calculate AGM_W(B), Expected output: 10000")
    print(f"AGM_W(B): {agm_bound(Q, [(0, 10), (0, 10), (0, 10)], box_attributes)}")
    print("\n")

    # Example usage of replace function
    print("Example usage of replace function, should replace the second box attribute with (5, 7)")
    new_box = replace([(0, 10), (0, 10), (0, 10)], 1, (5, 7))
    print(f"Original box: {[(0, 10), (0, 10), (0, 10)]}")
    print(f"New box after replace: {new_box}")
    print("\n")

    # Example usage of split function
    print("Example usage of split function")
    split_result = split(0, [(0, 10), (0, 10), (0, 10)], Q, box_attributes)
    print(f"Split result: {split_result}")
    print("\n")

    # Example usage of sample function
    print("Example usage of sample function:")
    sample_result = sample(W, Q, box_attributes)
    print(f"Sample result: {sample_result}")
    print("\n")

    # Calculate success probability
    print("Calculating success probability")
    theoretical_prob = calculate_success_probability(Q, box_attributes, W)
    print(f"Theoretical success probability: {theoretical_prob}")

    # Test the sampling algorithm with 1000 trials
    print(
        "Start testing the sampling algorithm with 1000 trials and calculate the empirical success probability...")
    num_trials = 1000
    empirical_prob, sample_result = test_sampling_algorithm(Q, box_attributes, W, num_trials)
    print(f"Empirical success probability after {num_trials} trials: {empirical_prob}")
    print("First 10 Samples in result:", sample_result[:10])
    print("\n")

    # Run sampling algorithm until 1000 samples are obtained
    print("Run sampling algorithm until 1000 samples are obtained...")
    num_samples = 1000
    samples = run_sampling_algorithm(Q, box_attributes, W, num_samples)

    # Save samples to file
    save_samples_to_file(samples, "data/sampled_results.txt")
    print("Samples saved to data/sampled_results.txt")
    print("First 10 Samples in result:", samples[:10])
