# -*- coding: utf-8 -*-
"""
.. moduleauthor:: Francesco Witte <francesco.witte@hs-flensburg.de>

"""

import numpy as np
import pandas as pd

def detect_cycles(path):
    """
    Detect cycles: Read input data and search for cycles.

    Parameters
    ----------
    path : str
        Path to the input .csv-file.

    Returns
    -------
    cycles : pandas.core.frame.DataFrame
        Dataframe containing the cycles start times, end times, local minima
        and amplitude.

    Note
    ----
    The DataFrame's collumns are 't_start', 't_end', 't_minimum' and 'amplitude'.
    """

    # read input data from .csv file
    series = pd.read_csv(path, names=['values'], header=None)

    # norm input data
    series['norm'] = series['values'] - series['values'].min()
    series['norm'] /= series['norm'].max()

    # calculate cycles
    cycles = find_cycles(series['norm'])
    print(type(series['norm']))
    return cycles

def find_cycles(series_norm):
    """
    Search the normalised time series for cycles and detect start times, end times,
    local minimima and amplitudes with the corresponding functions.

    Parameters
    ----------
    series_norm : pandas.core.series.Series
        Normalised input time series.

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Dataframe containing the cycles start times, end times, local minima
        and amplitude.
    """
    # find minima and maxima
    min_idx, max_idx = find_peaks_idx(series_norm)
    # find start and end times
    t_start = soc_find_start(series_norm, max_idx)
    t_end = soc_find_end(series_norm, max_idx)

    # precalculation of the cycles
    precycles = search_precycle(series_norm, max_idx, t_start, t_end)

    # remove rows with zeros only and remove duplicates
    precycles_mod = precycles[~np.all(precycles == 0, axis=1)]
    precycles_mod = np.unique(precycles_mod, axis=0)

    # cycle detection
    cycles = cycling(precycles_mod)

    # calculate the amplitude of the cycles
    cycles[:, 3] = calc_amplitude(series_norm, cycles)

    # write data to DataFrame
    df = pd.DataFrame()
    df['t_start'] = cycles[:, 0]
    df['t_end'] = cycles[:, 1]
    df['t_minimum'] = cycles[:, 2]
    df['amplitude'] = cycles[:, 3]

    return df


def find_peaks_idx(series):
    """
    Find the indices of local minima and maxima:

    - Calculate the difference of neighboring values in the series.
    - Search for sign changes in the differences.
    - Remove sign changes for zeros (zero has an own sign in numpy).
    - Iterate over indices of the sign changes:

        - local minimum, if gradient before sign change is negative.
        - local maximum, if gradient before sign change is positive.

    - Remove first local minimum/maximum, if it is the first value of the series.

    Parameters
    ----------
    series : pandas.core.series.Series
        Input series to find local minima and maxima in.

    Returns
    -------
    min_idx : list
        List with the indices of local minima in the series.

    max_idx : list
        List with the indices of local maxima in the series.
    """
    # calculate difference between neighboring values
    diff = np.diff(np.concatenate(([0], series, [0])))
    # calculate sign changes
    asign = np.sign(diff)

    # remove sign changes for zero
    sz = asign == 0
    while sz.any():
        asign[sz] = np.roll(asign, 1)[sz]
        sz = asign == 0
    signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)

    min_idx = []
    max_idx = []
    start = series[0]

    # iterate over indices of sign changes
    for index in np.where(signchange == 1)[0]:
        if start > 0:
            max_idx += [index - 1]
            start = diff[index]
        else:
            min_idx += [index - 1]
            start = diff[index]

    # remove first sign change, if at first value of series
    if min_idx[0] <= 0:
        min_idx = min_idx[1:]
    if max_idx[0] <= 0:
        max_idx = max_idx[1:]

    return min_idx, max_idx


def soc_find_start(series, indices):
    """
    Find the starting times of the cycles.

    Parameters
    ----------
    series : pandas.core.series.Series
        Input series.

    indices : list
        The indices of local maxima in the time series.

    Returns
    -------
    t : list
        List  of start times.
    """
    t = []

    size = len(indices)

    for c in range(1, size)[::-1]:
        for d in range(c)[::-1]:
            if series[indices[d]] >= series[indices[c]]:
                t += [indices[d]]
                break
            elif d == 0:
                t += [0]
                break

    t += [indices[-1]]
    return t[::-1]


def soc_find_end(series, indices):
    """
    Find the ending times of the cycles.

    Parameters
    ----------
    series : pandas.core.series.Series
        Input series.

    indices : list
        The indices of local maxima in the time series.

    Returns
    -------
    t : list
        List  of end times.
    """
    t = []

    size = len(indices)

    for c in range(size):
        for d in range(c + 1, size):
            if series[indices[d]] >= series[indices[c]]:
                t += [indices[d]]
                break
            elif d == size - 1:
                t += [-1]
                break

    t += [-1]
    return t


def search_precycle(series, indices, t_start, t_end):
    """
    Precalculation of the cycles.

    Parameters
    ----------
    series : pandas.core.series.Series
        Input series.

    indices : list
        The indices of local maxima in the time series.

    t_start : list
        List of starting times.

    t_end : list
        List of ending times.

    Returns
    -------
    pre : numpy.ndarray
        List  of end times.
    """
    size = len(indices)
    pre_a = np.zeros((size, 4))
    pre_b = np.zeros((size, 4))

    for c in range(size):
        if t_start[c] < indices[c]:
            values = series[t_start[c]:indices[c] + 1].tolist()

            pre_a[c, 0] = t_start[c]
            pre_a[c, 1] = indices[c]
            pre_a[c, 2] = values.index(min(values)) + t_start[c]
            pre_a[c, 3] = min(values)

        if t_end[c] > indices[c]:
            values = series[indices[c]:t_end[c] + 1].tolist()

            pre_b[c, 0] = indices[c]
            pre_b[c, 1] = t_end[c]
            pre_b[c, 2] = values.index(min(values)) + indices[c]
            pre_b[c, 3] = min(values)

    # concatenate the two arrays
    pre = np.append(pre_a, pre_b, axis=0)
    return pre


def cycling(rows):
    """
    Cycle detection, delete from precycles if ...?

    Parameters
    ----------
    rows : numpy.ndarray
        Modified precycles.

    Returns
    -------
    rows : numpy.ndarray
        Array of cycles.
    """
    # remove rows
    for c in range(rows.shape[0]):
        indices = np.where((rows[c, 2] == rows[:, 2]) &
                           (rows[c, 0] <= rows[:, 0]) &
                           (rows[c, 1] >= rows[:, 1]))[0]
        indices = indices[indices != c]
        rows[indices] = 0

    # remove rows with zeros only
    rows = rows[~np.all(rows == 0, axis=1)]

    return rows


def calc_amplitude(series, pre):
    """
    Calculation of the cycles amplitude.

    Parameters
    ----------
    series : pandas.core.series.Series
        Input series.

    pre : numpy.ndarray
        Array of precycles.

    Returns
    -------
    amp : numpy.ndarray
        Array of corresponding amplitudes.
    """
    num = pre.shape[0]
    amp = np.zeros(num)

    for c in range(num):
        amp[c] = min(series[pre[c, 0]], series[pre[c, 1]]) - pre[c, 3]

    return amp
