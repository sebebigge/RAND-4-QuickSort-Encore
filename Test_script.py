def test_quicksort(size:int, runs:int) -> dict[tuple[int,int],float]:
    counter = make_counter_dict(size)
    for _ in range(runs):
        A = random.sample(range(1,size+1), size)
        counter = quicksort(A, 0, size-1, counter)
    return {k: v / runs for k, v in counter.items()}