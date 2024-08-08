import bisect
import time
from typing import Dict, List, Tuple, Set, Union
from Relation import Relation
from RangeTree import RangeTree
from Oracles import count_oracle, median_oracle, sub_join_induced_by_box
from Sample import join_relations, sample
from Split import agm_bound, replace, split
import random



def test_sampling_algorithm(Q: List[Relation], box_attributes: List[str],
                            W: List[float], num_trials: int) -> float:
    success_count = 0
    sample_results = []
    start_time = time.time()

    for _ in range(num_trials):
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


def save_samples_to_file(samples: List[Dict[str, Union[List[str], Tuple[int]]]],
                         file_path: str):
    with open(file_path, 'w') as f:
        f.write("A\tB\tC\tD\n")
        for sample in samples:
            tuple_ = sample["tuple"]
            f.write("\t".join(map(str, tuple_)) + "\n")


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

    # Generate random data for R3, R4 and R5 by uncommenting the following code
    # num_tuples = 100
    # value_range = (0, 10)

    # R3_data = generate_unique_random_data(num_tuples, value_range)
    # R4_data = generate_unique_random_data(num_tuples, value_range)
    # R5_data = generate_unique_random_data(num_tuples, value_range)
    #
    # save_to_file("data/R3_data.txt", R3_data)
    # save_to_file("data/R4_data.txt", R4_data)
    # save_to_file("data/R5_data.txt", R5_data)
    #
    # print("Unique random data saved to R1_data.txt and R2_data.txt")


    # Load data from file
    R3_data = read_from_file("data/R3_data.txt")
    R4_data = read_from_file("data/R4_data.txt")
    R5_data = read_from_file("data/R5_data.txt")

    R3 = Relation("R3", ["A", "B"], R3_data)
    R4 = Relation("R4", ["B", "C"], R4_data)
    R5 = Relation("R5", ["C", "D"], R5_data)
    Q = [R3, R4, R5]

    box_attributes = ["A", "B", "C", "D"]
    W = [1.5, 1, 1.5]

    # Test the sampling algorithm with 1000 trials
    print("Testing the sampling algorithm with 1000 trials...")
    num_trials = 1000
    empirical_prob, sample_result = test_sampling_algorithm(Q, box_attributes,
                                                            W, num_trials)
    print(
        f"Empirical success sample probability after {num_trials} trials: {empirical_prob}")
    print("First 10 Samples in result:", sample_result[:10])
    print("\n")


    # Run sampling algorithm until 1000 samples are obtained
    # print running time

    print("Run sampling algorithm until 1000 samples are obtained...")
    num_samples = 1000
    samples = run_sampling_algorithm(Q, box_attributes, W, num_samples)

    # Save samples to file
    save_samples_to_file(samples, "data/sampled_results.txt")
    print("Samples saved to data/sampled_results.txt")
    print("First 10 Samples in result:", samples[:10])



