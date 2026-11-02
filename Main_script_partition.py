def partition(A:list[int], p:int, r:int, counter:dict[tuple[int,int],int]) -> tuple[int, dict[tuple[int,int],int]]:
    x = A[r]; i = p - 1
    for j in range(p,r):
        if A[j] > x:
            counter[(x, A[j])] += 1
        else:
            counter[(A[j], x)] += 1
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return (i+1, counter)