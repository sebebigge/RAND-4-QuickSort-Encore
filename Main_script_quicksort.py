def quicksort(A:list[int], p:int, r:int, counter:dict[tuple[int,int],int]) -> dict[tuple[int,int],int]:
    if p < r:
        (q, counter) = partition(A, p, r, counter)
        quicksort(A, p, q - 1, counter)
        quicksort(A, q + 1, r, counter)
    return counter