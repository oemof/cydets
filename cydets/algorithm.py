"""Main cycle detection algorithm with auxiliary functions."""
import numpy as np
import pandas as pd


def detect_cycles(series, drop_zero_docs=True, integer_index=False):
    r"""
    Detect cycles in a time series with information on start, end and depths.

    - Normalize values of time series ts:

    .. math::

        ts_{z}\left(t \right) = ts\left(t \right) - min\left(t \right)

        ts_{norm}\left(t \right) = \frac{ts_{z}\left(t \right)}
        {max\left(ts_{z} \right)}

        ts \text{: time series}

        ts_{z} \text{: with zero point}

        ts_{norm} \text{: normalised}

    - find peaks (and valleys) of the series.
      (:func:`cycle_detection.find_peaks_valleys_idx`).
    - find possible starting and ending points for precycles
      (:func:`cycle_detection.soc_find_start`,
      :func:`cycle_detection.soc_find_end`).
    - identify precycles (:func:`cycle_detection.search_precycle`)
    - identify actual cycles by removing overlapping precycles (
      :func:`cycle_detection.cycling`).
    - calculate the depths of the actual cycles (
      :func:`cycle_detection.calc_doc`).

    Parameters
    ----------
    series : pandas.core.series.Series
        Input time series.

    drop_zero_docs : bool
        Drop cycles with doc = 0 at the end?

    integer_index : bool
        Use an integer index instead of the original input time series index?

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Dataframe containing the cycles start times, end times, local minima
        and depth of cycle (doc).

    Example
    -------
    >>> import pandas as pd
    >>> from cydets.algorithm import detect_cycles
    >>> series = pd.Series([0, 1, 0, 0.5, 0, 1, 0, 0.5, 0, 1, 0])
    >>> cycles = detect_cycles(series)
    >>> type(cycles)
    <class 'pandas.core.frame.DataFrame'>

    Note
    ----
    The DataFrame's collumns are :code:`t_start` (starttime),
    :code:`t_end` (endtime), :code:`t_minimum` (time of local minimum in cycle)
    and :code:`doc` (depths of cycle).
    """

    if len(series) < 4:
        msg = ('The number of elements in the input time series to form one '
               'cycle must be 4 at least.')
        raise ValueError(msg)
    # convert input data to a data frame
    series = series.to_frame(name='values')
    series['id'] = series.index
    series.index = pd.RangeIndex(len(series.index))

    # norm input data
    series['norm'] = series['values'] - series['values'].min()
    maximum = series['norm'].max()
    if maximum == 0:
        msg = 'Detected constant time series.'
        raise ValueError(msg)
    series['norm'] /= maximum

    # find minima and maxima
    min_idx, max_idx = find_peaks_valleys_idx(series['norm'])
    # find start and end times of cycles (potenial start/end at local maxima)
    t_start = soc_find_start(series['norm'], max_idx)
    t_end = soc_find_end(series['norm'], max_idx)

    # search for precycles
    precycles = search_precycle(series['norm'], max_idx, t_start, t_end)

    # cycle detection
    cycles = cycling(precycles)

    # calculate the amplitude of the cycles
    cycles[:, 3] = calc_doc(series['norm'], cycles)

    # write data to DataFrame
    df = pd.DataFrame()
    if integer_index is True:
        # use the integer index as time stamps
        df['t_start'] = cycles[:, 0]
        df['t_end'] = cycles[:, 1]
        df['t_minimum'] = cycles[:, 2]

    else:
        # use original index as time stamps
        df['t_start'] = series.iloc[cycles[:, 0]]['id'].values
        df['t_end'] = series.iloc[cycles[:, 1]]['id'].values
        df['t_minimum'] = series.iloc[cycles[:, 2]]['id'].values

    # write depth of cycle in DataFrame
    df['doc'] = cycles[:, 3]
    # calculate duration
    df['duration'] = df['t_end'] - df['t_start']

    # drop cycles where the amplitude (doc) is zero
    if drop_zero_docs is True:
        df = df.drop(df[df['doc'] == 0].index)

    # reset the index
    df = df.reset_index(drop=True)

    return df


def find_peaks_valleys_idx(series):
    """
    Find the indices of peaks and valleys.

    - Calculate the difference of neighboring values in the series.
    - Search for sign changes in the differences.
    - Remove sign changes for zeros (zero has an own sign in numpy).
    - Iterate over indices of the sign changes:

        - valley, if gradient before sign change is negative.
        - peak, if gradient before sign change is positive.

    - Remove peak/valley, if it is at the first value of the series.

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

    Note
    ----
    A peak is a point, where the value is higher than the value of the
    preceding timestep and not less than the succeeding value.
    A valley is a point, where the value is lower than the value of the
    preceding timestep and not more than the succeeding value.
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

    # no valley found
    if len(min_idx) == 0:
        msg = 'No valleys detected in time series.'
        raise ValueError(msg)

    # no peaks found
    if len(max_idx) == 0:
        msg = 'No peaks detected in time series.'
        raise ValueError(msg)

    # remove first sign change, if at first value of series
    if min_idx[0] <= 0:
        min_idx = min_idx[1:]
    if max_idx[0] <= 0:
        max_idx = max_idx[1:]

    return min_idx, max_idx


def soc_find_start(series, indices):
    """
    Find the starting times of the precycles.

    A possible starting point for a cycle is a peak that is higher than
    specific a succeeding peak.

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

    # number of peaks
    size = len(indices)

    # determine possible starting points for precycles:
    # searches the peaks from the end to the start for a peak at t1 that is
    # higher than the last peak at t2
    # if a peak is found or all preceding peaks have been searched
    # t2 is moved to its predecessor
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
    Find the ending times of the precycles.

    A possible ending point for a cycle is a peak that is higher than specific
    a preceding peak.

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

    # number of peaks
    size = len(indices)

    # determine possible ending points for precycles:
    # searches the peaks from start to end for a peak at t2 that is
    # higher than the first peak at t1
    # if a peak is found or all preceding peaks have been searched
    # t1 is moved to its successor
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
    Search for precycles.

    Precycles start at the calculated starting times and end at the next peak
    or start at a previous peak and end at the calculated ending times.

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
            # start time must be before time of corresponding peak
            # retrieve the values of the series between start time and
            # next peak
            values = series[t_start[c]:indices[c] + 1].tolist()

            # start time
            pre_a[c, 0] = t_start[c]
            # next peak
            pre_a[c, 1] = indices[c]
            # index/time of minimum value
            pre_a[c, 2] = values.index(min(values)) + t_start[c]
            # minimum value of the section
            pre_a[c, 3] = min(values)

        if t_end[c] > indices[c]:
            # end time must be after time of corresponding peak
            # retrieve the values of the series between previous peak and
            # end time
            values = series[indices[c]:t_end[c] + 1].tolist()

            # previous peak
            pre_b[c, 0] = indices[c]
            # end time
            pre_b[c, 1] = t_end[c]
            # index/time of minimum value
            pre_b[c, 2] = values.index(min(values)) + indices[c]
            # minimum value of the section
            pre_b[c, 3] = min(values)

    # concatenate the two arrays
    pre = np.append(pre_a, pre_b, axis=0)
    # remove rows with only zeros (=no precycle found)
    pre = pre[~np.all(pre == 0, axis=1)]

    if len(pre) == 0:
        msg = 'No cycles detected.'
        raise ValueError(msg)
    # remove duplicates
    pre = np.unique(pre, axis=0)
    return pre


def cycling(rows):
    """
    Detect cycles from given precycles by removing overlapping precycles.

    From all precycles with the same timestamp for the minimum value only the
    most narrow precycle is kept. The most narrow precycle is defined by the
    latest starting and the earliest ending time.

    Parameters
    ----------
    rows : numpy.ndarray
        Modified precycles.

    Returns
    -------
    rows : numpy.ndarray
        Array of cycles.
    """
    # remove overlaps in the precycles and flag the corresponding rows
    for c in range(rows.shape[0]):
        indices = np.where((rows[c, 2] == rows[:, 2]) &
                           (rows[c, 0] <= rows[:, 0]) &
                           (rows[c, 1] >= rows[:, 1]))[0]
        # choose indices to flag rows
        indices = indices[indices != c]
        rows[indices] = 0

    # remove the flagged rows (rows with zeros only)
    rows = rows[~np.all(rows == 0, axis=1)]

    return rows


def calc_doc(series, rows):
    r"""
    Calculate depths of cycle.

    The depths of the cycle is the minimum height between the minimum value
    of the cycle and the bordering peaks.

    .. math::

        doc\left(c \right)= min\left[soc\left(t_{start}\right),
        soc\left(t_{end}\right) \right] - c_{min}

    Parameters
    ----------
    series : pandas.core.series.Series
        Input series.

    rows : numpy.ndarray
        Array of cycles.

    Returns
    -------
    doc : numpy.ndarray
        Array of corresponding depth of the cylces.
    """
    num = rows.shape[0]
    doc = np.zeros(num)

    for c in range(num):
        doc[c] = min(series[rows[c, 0]], series[rows[c, 1]]) - rows[c, 3]

    return doc
