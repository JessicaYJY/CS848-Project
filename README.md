# CS848-Project

## Description
This project focuses on the practical implementation of the theoretical advancements presented in the paper "On Join Sampling and the Hardness of Combinatorial Output-Sensitive Join Algorithms" by Deng et al on 2023. The paper can be found here: [On Join Sampling and the Hardness of Combinatorial Output-Sensitive Join Algorithms](https://www.cse.cuhk.edu.hk/~taoyf/paper/pods23-jsamp.pdf)

## Requirements
- Python 3.7 or higher

## File Descriptions
- `Relation.py`: This class represents a database relation with a set of attributes and tuples. It includes methods for retrieving attribute indices and extracting sub-relations based on specified ranges (boxes).
- `RangeTree.py`: This class was implemented to facilitate efficient range counting queries over the tuples. This tree structure supports the `range_count` function, which counts the number of points within a specified range.
- `MedianBST.py`: A Binary Search Tree (BST) was used to efficiently find the median value of an attribute within a box. This is crucial for the median oracle which helps in splitting the attribute space during the sampling process.
- `Oracles.py`: Contains oracle implementations for count oracle and median oracle.
- `split.py`: This algorithm splits the attribute space (box) into sub-boxes using the median oracle. It recursively partitions the box until the AGM bound is sufficiently small, ensuring efficient sampling.
- `sample.py`: The core sampling algorithm repeatedly splits the box and calculates the AGM bound until a sufficiently small box is identified. It then performs the join operation on the sub-relations and probabilistically selects a sample tuple.
- `test_2relations_simple.py`: Test script for simple cases involving two relations.
- `test_2relstions_large.py`: Test script for large cases involving two relations.
- `test_3relations_simple.py`: Test script for simple cases involving three relations.
- `test_3relations_large.py`: Test script for large cases involving three relations.

## Data
- For simple tests `test_2relations_simple.py` and `test_3relations_simple.py`, small synthetic datasets were defined directly within the code.
- For large tests `test_2relstions_large.py` and `test_3relations_large.py`, random data tuples were already generated and saved to text files in `data` folder. Then these files were read into the program for use in the experiments.
- You can generate the data again by comment out the `generate_unique_random_data` function in `test_2relstions_large.py` and `test_3relations_large.py`.

## Analysis
- The `test_sampling_algorithm` function was used to conduct a specified number of trials, recording the success rate and time taken.
- The `run_sampling_algorithm` function was used to obtain a specified number of successful samples, recording the number of trials needed and the time taken.
- The theoretical success probability was calculated using the `calculate_success_probability` function for 2 relations join, while the empirical success probability was determined from the results of the trials.
- The implementation made use of Python's (`time`) module to measure the execution time of the sampling algorithm.
- The `save_samples_to_file` function can save the generate samples to `data/sampled_results.txt`

## Running Experiments
1. Clone the repository:
   ```sh
   git clone https://github.com/JessicaYJY/CS848-Project.git
   cd CS848-Project
   ```
2. Basic Testing:
   ```python
   python test_2relations_simple.py
   ```
   
   The following tests are conducted in the above script:
   - Demonstrate Utility Functions: Example usage of `count_oracle`, `median_oracle`, Calculate Q(B), Calculate AGM_W(B), `replace`, `split`, `sample` functions.
   - Calculate Theoretical Success Probability: Calculates the theoretical success probability for a simple test case using the function `calculate_success_probability`.
   - Test Sampling Algorithm:
     - Tests the sampling algorithm with 1000 trials using the function `test_sampling_algorithm`.
     - Calculates the empirical success probability and compares it with the theoretical probability.
     - Outputs the first 10 sample results for inspection.
   - Run Sampling Algorithm:
     - Runs the sampling algorithm until 1000 samples are obtained using the function `run_sampling_algorithm`.
     - Recording the number of trials needed and the time taken.
     - Saves the samples to a file data/sampled_results.txt.
     - Outputs the first 10 sample results for inspection.

   ```python
   python test_3relations_simple.py
   ```
   The following tests are conducted in the above script:
   - Test Sampling Algorithm:
     - Tests the sampling algorithm with 1000 trials using the function `test_sampling_algorithm`.
     - Calculates the empirical success probability and compares it with the theoretical probability.
     - Outputs the first 10 sample results for inspection.
   - Run Sampling Algorithm:
     - Runs the sampling algorithm until 1000 samples are obtained using the function `run_sampling_algorithm`.
     - Recording the number of trials needed and the time taken.
     - Saves the samples to a file data/sampled_results.txt.
     - Outputs the first 10 sample results for inspection.

4. Large Dataset Testing:
   ```python
   python test_2relstions_large.py
   ```
   
   The following tests are conducted in the above script:
   - Demonstrate Utility Functions: Example usage of `count_oracle`, `median_oracle`, Calculate Q(B), Calculate AGM_W(B), `replace`, `split`, `sample` functions.
   - Calculate Theoretical Success Probability: Calculates the theoretical success probability for a simple test case using the function `calculate_success_probability`.
   - Test Sampling Algorithm:
     - Tests the sampling algorithm with 1000 trials using the function `test_sampling_algorithm`.
     - Calculates the empirical success probability and compares it with the theoretical probability.
     - Outputs the first 10 sample results for inspection.
   - Run Sampling Algorithm:
     - Runs the sampling algorithm until 1000 samples are obtained using the function `run_sampling_algorithm`.
     - Recording the number of trials needed and the time taken.
     - Saves the samples to a file data/sampled_results.txt.
     - Outputs the first 10 sample results for inspection.

   ```python
   python test_3relations_large.py
   ```
   
   The following tests are conducted in the above script:
   - Test Sampling Algorithm:
     - Tests the sampling algorithm with 1000 trials using the function `test_sampling_algorithm`.
     - Calculates the empirical success probability and compares it with the theoretical probability.
     - Outputs the first 10 sample results for inspection.
   - Run Sampling Algorithm:
     - Runs the sampling algorithm until 1000 samples are obtained using the function `run_sampling_algorithm`.
     - Recording the number of trials needed and the time taken.
     - Saves the samples to a file data/sampled_results.txt.
     - Outputs the first 10 sample results for inspection.

## Result
The results of the experiments will be printed to the console. For saved generate samples, check (`data/sampled_results.txt`).

