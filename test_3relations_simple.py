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
    print(
        f"Time taken for {num_trials} trials: {end_time - start_time} seconds")

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



if __name__ == '__main__':

    # Define three new relations R3, R4, and R5
    R3 = Relation("R3", ["A", "B"], [(1, 7), (2, 8), (3, 9), (4, 10)])
    R4 = Relation("R4", ["B", "C"], [(7, 11), (8, 12), (9, 13), (10, 14)])
    R5 = Relation("R5", ["C", "D"], [(11, 15), (12, 16), (13, 17), (14, 18)])

    # Form the query Q containing the new relations
    Q = [R3, R4, R5]

    # Define the box_attributes and W as given in the example
    box_attributes = ["A", "B", "C", "D"]
    W = [1.5, 1, 1.5]  # Example fractional edge covering

    # Test the sampling algorithm with 1000 trials
    print("Testing the sampling algorithm with 1000 trials...")
    num_trials = 1000
    empirical_prob, sample_result = test_sampling_algorithm(Q, box_attributes,
                                                            W, num_trials)
    print(
        f"Empirical success sample probability after {num_trials} trials: {empirical_prob}")
    print("First 10 Samples in result:", sample_result[:10])
    print("\n")

    # Run sampling algorithm
    print("Run sampling algorithm until 1000 samples are obtained...")
    num_samples = 1000
    samples = run_sampling_algorithm(Q, box_attributes, W, num_samples)

    # Save samples to file
    save_samples_to_file(samples, "data/sampled_results.txt")
    print("Samples saved to data/sampled_results.txt")
    print("First 10 Samples in result:", samples[:10])



