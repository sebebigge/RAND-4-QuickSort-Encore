"""
@author: Sebastian Bigge
@date:   2026-11-01
"""

# Imports
import random
import numpy as np


####################################################################################
################################  IMPLEMENTATION  ##################################
####################################################################################

"""
Sorts the array A from index p to r in place using the Quicksort algorithm.

@param {list} A:    list to sort
@param {int} p:     starting index of the subarray to be sorted
@param {int} r:     ending index of the subarray to be sorted
@return {None}:     sorts the array A[p..r] in place
"""
def quicksort(A: list[int], p: int, r: int) -> None:
    if p < r:
        q = partition(A, p, r)
        quicksort(A, p, q - 1)      # recursively sort left side
        quicksort(A, q + 1, r)      # recursively sort right side


"""
Partitions the subarray A[p..r] using Lomuto partitioning

@param {list[int]} A:     list to partition
@param {list[int]} p:     starting index of the subarray
@param {list[int]} r:     ending index of the subarray (pivot)
@return {list[int]}:      index of the pivot after partitioning
"""
def partition(A: list[int], p: int, r: int) -> list[int]:
    x = A[r]
    i = p - 1
    for j in range(p,r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return i+1