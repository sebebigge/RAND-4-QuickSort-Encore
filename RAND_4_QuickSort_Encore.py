"""
@author: Sebastian Bigge
@date:   2026-11-02
"""

# Imports
import random
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm


####################################################################################
################################  IMPLEMENTATION  ##################################
####################################################################################

"""
Sorts a list A[p..r] in place using the quicksort algorithm and counts comparisons between pairs of elements

@param {list[int]} A:                   list to sort
@param {int} p:                         starting index of the subarray to be sorted
@param {int} r:                         ending index of the subarray to be sorted
@param {dict} counter:                  dictionary to count comparisons between pairs of elements
@return {dict[tuple[int,int],int]}:     dictionary with counts of comparisons between pairs
@return {dict[tuple[int,int],int]}:     updated dictionary with counts of comparisons between pairs
"""
def quicksort(A: list[int], p: int, r: int, counter: dict[tuple[int,int],int]
              ) -> dict[tuple[int,int],int]:
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
def partition(A: list[int], p: int, r: int, counter: dict[tuple[int,int],int]
              ) -> tuple[int, dict[tuple[int,int],int]]:
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
###################################  HELPERS  ######################################
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
Makes a dictionary to count theoretical expected comparisons between pairs of elements in the array

@param {int} size:                      size of the array to sort
@return {dict[tuple[int,int],float]}:   dictionary with expected counts of comparisons between pairs
"""
def make_expected_counter_dict(size: int) -> dict[tuple[int,int],float]:
    result = dict()
    for i in range(1, size+1):
        for j in range(i+1, size+1):
            result[(i,j)] = 2 / (j-i+1)
    return result


####################################################################################
####################################  PLOTS  #######################################
####################################################################################

# GenAI
"""
Plots the difference between expected and observed comparisons for each pair of elements

@param {dict[tuple[int,int],float]} diff:   dictionary with differences between expected and observed comparisons
@return {None}:                             generates a plot of the differences"""
def plot_diff(diff: dict[tuple[int,int], float]) -> None:
    # Group by distance j - i
    by_dist = {}
    for (i, j), v in diff.items():
        by_dist.setdefault(j - i, []).append(v)
    dists = sorted(by_dist)
    means = [np.mean(by_dist[d]) for d in dists]
    stds  = [np.std(by_dist[d])  for d in dists]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(dists, means, yerr=stds, fmt="o-", capsize=2)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("j − i")
    ax.set_ylabel("expected − observed")
    plt.tight_layout()
    plt.show()


# GenAI
"""
Plots the ratio of observed to expected comparisons for each pair of elements based on 
their distance (j - i)

@param {dict[tuple[int,int],float]} counter_avg:    dictionary with average observed comparisons
@param {dict[tuple[int,int],float]} counter_exp:    dictionary with expected comparisons
@param {int | None} runs:                           number of runs (used for noise band)
@return {None}:                                     generates a plot of the ratios
"""
def plot_ratio(counter_avg: dict[tuple[int,int], float], counter_exp: dict[tuple[int,int], float],
               runs: int | None = None, save_path: Path | None = None) -> None:
    # Group observed/expected by distance d = j - i
    by_dist = {}
    for (i, j), exp in counter_exp.items():
        by_dist.setdefault(j - i, []).append(counter_avg[(i, j)] / exp)
    dists = sorted(by_dist)
    means = np.array([np.mean(by_dist[d]) for d in dists])
    stds  = np.array([np.std(by_dist[d])  for d in dists])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(dists, means, yerr=stds, fmt="o-", capsize=2, label="mean ± std over pairs")
    # Optional: theoretical noise band for a single pair
    if runs is not None:
        d_arr = np.array(dists)
        p = 2 / (d_arr + 1)
        sigma = np.sqrt((1 - p) / (p * runs))
        ax.fill_between(d_arr, 1 - sigma, 1 + sigma, color="gray", alpha=0.2,
                        label="expected single-pair noise (±1σ)")
    ax.axhline(1, color="k", lw=0.8)
    ax.set_xlabel("j − i")
    ax.set_ylabel("observed / expected")
    ax.legend()
    plt.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, bbox_inches="tight")
    #plt.show()


# GenAI
"""
Plots observed vs expected comparisons for each pair of elements

@param {dict[tuple[int,int],float]} counter_avg:    dictionary with average observed comparisons
@param {dict[tuple[int,int],float]} counter_exp:    dictionary with expected comparisons
@return {None}:                                     generates a scatter plot of observed vs expected comparisons
"""
def plot_observed_vs_expected(counter_avg: dict[tuple[int,int], float], 
                              counter_exp: dict[tuple[int,int], float],
                              save_path: Path | None = None) -> None:
    x = [counter_exp[k] for k in counter_exp]
    y = [counter_avg[k] for k in counter_exp]
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, alpha=0.5)
    mn = min(min(x), min(y))
    mx = max(max(x), max(y))
    plt.plot([mn, mx], [mn, mx], 'r--', label='y = x')
    plt.xlabel("Expected probability")
    plt.ylabel("Observed probability")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")
    #plt.show()

# GenAI
"""
Plots a table of values for each pair of elements, with options for different modes

@param {dict[tuple[int,int],float]} counter_avg:    dictionary with average observed comparisons
@param {dict[tuple[int,int],float]} counter_exp:    dictionary with expected comparisons
@param {int} runs:                                  number of runs (used for z-score calculation)
@param {str} mode:                                  mode of the plot ("ratio", "diff", "z", "observed", 
                                                    "expected")
@param {bool | None} annotate:                      whether to annotate the cells with values (default: 
                                                    True for small tables)
@return {None}:                                     generates a heatmap table of the specified mode for 
                                                    each pair (i, j)
"""
def plot_table(counter_avg: dict[tuple[int,int], float], counter_exp: dict[tuple[int,int], float],
               runs: int, mode: str = "ratio",       # "ratio", "diff", "z", "observed", "expected"
               annotate: bool | None = None) -> None:
    size = max(j for _, j in counter_exp)
    M = np.full((size, size), np.nan)
    for (i, j), exp in counter_exp.items():
        obs = counter_avg[(i, j)]
        if mode == "ratio":
            v = obs / exp
        elif mode == "diff":
            v = exp - obs
        elif mode == "z":
            sd = np.sqrt(exp * (1 - exp) / runs)
            v = (obs - exp) / sd if sd > 0 else np.nan   # d = 1: p = 1, no variance
        elif mode == "observed":
            v = obs
        elif mode == "expected":
            v = exp
        else:
            raise ValueError(mode)
        M[i-1, j-1] = v
    # Colour scale: diverging and centred on the "perfect" value for comparison modes
    centre = {"ratio": 1.0, "diff": 0.0, "z": 0.0}.get(mode)
    if centre is not None:
        half = np.nanmax(np.abs(M - centre))
        vmin, vmax, cmap = centre - half, centre + half, "RdBu_r"
    else:
        vmin, vmax, cmap = 0, np.nanmax(M), "viridis"
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax)
    fig.colorbar(im, ax=ax, label=mode)
    # Write the numbers into the cells for small tables
    if annotate is None:
        annotate = size <= 15
    if annotate:
        for i in range(size):
            for j in range(size):
                if not np.isnan(M[i, j]):
                    ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=7)
    ticks = np.arange(size)
    step = 10
    ax.set_xticks(ticks[::step]); ax.set_xticklabels(ticks[::step])
    ax.set_yticks(ticks[::step]); ax.set_yticklabels(ticks[::step])
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")   # table-style: j across the top
    ax.set_xlabel("j"); ax.set_ylabel("i")
    plt.tight_layout()
    plt.show()


# GenAI
"""
Plots a split table of observed vs expected comparisons for each pair of elements

@param {dict[tuple[int,int],float]} counter_avg:    dictionary with average observed comparisons
@param {dict[tuple[int,int],float]} counter_exp:    dictionary with expected comparisons
@param {float} gamma:                               power normalization parameter for color scaling (default: 0.5)
@return {None}:                                     generates a heatmap table with observed values above the diagonal
                                                    and expected values below the diagonal
"""
def plot_table_split(counter_avg: dict[tuple[int,int], float], counter_exp: dict[tuple[int,int], float],
                     gamma: float = 0.5, save_path: Path | None = None) -> None:
    size = max(j for _, j in counter_exp)
    M = np.full((size, size), np.nan)
    for (i, j), exp in counter_exp.items():
        M[i-1, j-1] = counter_avg[(i, j)]   # observed: above the diagonal
        M[j-1, i-1] = exp                   # expected: below the diagonal
    # gamma < 1 stretches the low values so the long tail stays visible
    norm = PowerNorm(gamma=gamma, vmin=0, vmax=np.nanmax(M))
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(M, cmap="viridis", norm=norm)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("comparison probability", fontsize=12)
    cbar.ax.tick_params(labelsize=11)
    # Diagonal separator
    ax.plot([-0.5, size - 0.5], [-0.5, size - 0.5], color="white", lw=1)
    ticks = np.arange(size)
    step = max(1, size // 20)
    ax.set_xticks(ticks[::step]); ax.set_xticklabels(ticks[::step])
    ax.set_yticks(ticks[::step]); ax.set_yticklabels(ticks[::step])
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
    ax.set_xlabel("j (upper) / i (lower)", fontsize=12)
    ax.set_ylabel("i (upper) / j (lower)", fontsize=12)
    plt.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, bbox_inches="tight")
    #plt.show()


####################################################################################
####################################  TESTS  #######################################
####################################################################################

"""
Tests the quicksort function with a given array size and number of runs

@param {int} size:                      size of the array to sort
@param {int} runs:                      number of times to run the test
@return {dict[tuple[int,int],float]}:     dictionary with averages of comparisons between pairs
"""
def test_quicksort(size: int, runs: int) -> dict[tuple[int,int],float]:
    counter = make_counter_dict(size)
    for _ in range(runs):
        A = random.sample(range(1,size+1), size)
        counter = quicksort(A, 0, size-1, counter)
    counter_avg = {k: v / runs for k, v in counter.items()}
    return counter_avg


# GenAI: saving to path
"""
Tests the quicksort function and plots the results

@param {int} size:      size of the array to sort
@param {int} runs:      number of times to run the test
@return {None}:         generates plots
"""
def test_main(size: int, runs: int):
    counter_avg = test_quicksort(size, runs)
    counter_exp = make_expected_counter_dict(size)
    counter_difference = {k: v_exp - counter_avg[k] for k, v_exp in counter_exp.items()}
    output_dir = Path(f"Graphs/SIZE{size}_RUNS{runs}")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Graphs will be saved in: {output_dir}")
    plot_ratio(counter_avg, counter_exp, runs, output_dir / "ratio.png")
    plot_table_split(counter_avg, counter_exp, save_path=output_dir / "comparison_table.png")
    plot_observed_vs_expected(counter_avg, counter_exp,
                              save_path=output_dir / "observed_vs_expected.png")
    # not used but interesting:
    #plot_diff(counter_difference)
    #plot_table(counter_avg, counter_exp, runs, mode="diff")


if __name__ == "__main__":
    for size in [100, 1000, 10000]:
        for runs in [10, 100, 1000, 10000]:
            test_main(size, runs)