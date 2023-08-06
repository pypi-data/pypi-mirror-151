"""
A binning that has its edges aligned with the decade.
Choose how many bins you want within a decade and query the edges of the bins.
"""
import numpy as np


def lower_bin_edge(decade, bin, num_bins_per_decade=5):
    """
    Returns the lower edge of bin in decade.
    The binning has num_bins_per_decade.

    Parameters
    ----------
    decade : int
        E.g. decade=0 is 10^{0} = 1.0
    bin : int
        Index of bin within decade.
    num_bins_per_decade : int
        A decade has this many bins.

    Returns
    -------
    lower edge of bin : float
    """
    assert num_bins_per_decade > 0
    assert 0 <= bin < num_bins_per_decade
    return 10 ** (decade + np.linspace(0, 1, num_bins_per_decade + 1))[bin]


def make_decade_and_bin_combinations(
    start_decade, start_bin, stop_decade, stop_bin, num_bins_per_decade=5
):
    """
    Computes input-parameters to lower_bin_edge() in a given range.

    Parameters
    ----------
    start_decade : int
    start_bin : int
    stop_decade : int
    stop_bin : int
    num_bins_per_decade : int

    Returns
    -------
    A list of input-parameters to lower_bin_edge().
    """
    combos = []
    decade = start_decade
    assert 0 <= stop_bin < num_bins_per_decade
    assert 0 <= start_bin < num_bins_per_decade
    assert start_decade <= stop_decade

    bin = start_bin
    while decade != stop_decade or bin != stop_bin:
        combos.append((decade, bin, num_bins_per_decade))
        if bin + 1 < num_bins_per_decade:
            bin += 1
        else:
            bin = 0
            decade += 1
    return combos


def space(
    start_decade, start_bin, stop_decade, stop_bin, num_bins_per_decade=5
):
    """
    Power10.space:
    Compute the bin-edges starting from: (start_decade, start_bin)
    up to: (stop_decade, stop_bin).

    Parameters
    ----------
    start_decade : int
    start_bin : int
    stop_decade : int
    stop_bin : int
    num_bins_per_decade : int

    Returns
    -------
    Edges of bins : array of floats
    """
    combis = make_decade_and_bin_combinations(
        start_decade=start_decade,
        start_bin=start_bin,
        stop_decade=stop_decade,
        stop_bin=stop_bin,
        num_bins_per_decade=num_bins_per_decade,
    )
    out = np.nan * np.ones(len(combis))
    for i, combi in enumerate(combis):
        out[i] = lower_bin_edge(
            decade=combi[0], bin=combi[1], num_bins_per_decade=combi[2]
        )
    return out
