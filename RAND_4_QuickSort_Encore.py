"""
@author: Sebastian Bigge
@date:   2026-11-02
"""

# Imports
import random
import numpy as np


####################################################################################
################################  IMPLEMENTATION  ##################################
####################################################################################

"""
Sorts a randomly generated array of given size

@param {list[int]} A:                   list to sort
@param {int} p:                         starting index of the subarray to be sorted
@param {int} r:                         ending index of the subarray to be sorted
@param {dict} counter:                  dictionary to count comparisons between pairs of elements
@return {dict[tuple[int,int],int]}:     dictionary with counts of comparisons between pairs
@return {}
"""
def quicksort(A: list[int], p: int, r: int, counter: dict) -> dict[tuple[int,int],int]:
    if p < r:
        (q, counter) = partition(A, p, r, counter)
        quicksort(A, p, q - 1, counter)      # recursively sort left side
        quicksort(A, q + 1, r, counter)      # recursively sort right side
    return counter


"""
Partitions the subarray A[p..r] using Lomuto partitioning

@param {list[int]} A:       list to partition
@param {list[int]} p:       starting index of the subarray
@param {list[int]} r:       ending index of the subarray (pivot)
@param {dict} counter:      dictionary to count comparisons between pairs of elements
@return {tuple[int, dict[tuple[int,int],int]]}:  index of the pivot after partitioning and updated counter
"""
def partition(A: list[int], p: int, r: int, counter: dict) -> tuple[int, dict[tuple[int,int],int]]:
    x = A[r]
    i = p - 1
    for j in range(p,r):
        if A[j] > x:
            counter[(x, A[j])] += 1
        else:
            counter[(A[j], x)] += 1
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return (i+1, counter)


####################################################################################
####################################  TESTS  #######################################
####################################################################################

"""
Makes a dictionary to count comparisons between pairs of elements in the array

@param {int} size:                      size of the array to sort
@return {dict[tuple[int,int],int]}:     dictionary with counts of comparisons between pairs
"""
def make_counter_dict(size: int) -> dict[tuple[int,int],int]:
    result = dict()
    for i in range(1, size+1):
        for j in range(i+1, size+1):
            result[(i,j)] = 0
    return result


"""
Tests the quicksort function with a given array size and number of runs

@param {int} size:                      size of the array to sort
@param {int} runs:                      number of times to run the test
@return {dict[tuple[int,int],int]}:     dictionary with counts of comparisons between pairs
"""
def test_quicksort(size: int, runs: int) -> dict[tuple[int,int],int]:
    counter = make_counter_dict(size)
    for _ in range(runs):
        A = random.sample(range(1,size+1), size)
        counter = quicksort(A, 0, size-1, counter)
    counter_avg = {k: v / runs for k, v in counter.items()}
    return counter_avg

