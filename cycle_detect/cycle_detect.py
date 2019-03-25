# -*- coding: utf-8 -*-
"""
.. moduleauthor:: Francesco Witte <francesco.witte@hs-flensburg.de>

"""

import numpy as np
import pandas as pd

np.set_printoptions(threshold=np.nan)

class time_series:

    def __init__(self, path):
#    def __init__(self, path, binwidth=0.1):

        self.path = path
#        self.binwidth = binwidth
        self.series = pd.read_csv(path, names=['values'], header=None)
        self.series['norm'] = self.series['values'] - self.series['values'].min()
        self.series['norm'] /= self.series['norm'].max()
        self.cycles = pd.DataFrame()
        self.detect_cycles()

    def detect_cycles(self):
        """

        """
        # find minima and maxima
        min_idx, max_idx = detect_peaks_idx(self.series['norm'])
        t1 = soc_eq_find_b2(self.series['norm'], max_idx)
        t3 = soc_eq_find_a2(self.series['norm'], max_idx)
        # precalculation for cycles
        pre = search_precycle(self.series['norm'], max_idx, t1, t3)
        # remove rows with zeros only and remove duplicates
        pre_mod = pre[~np.all(pre == 0, axis=1)]
        pre_mod = np.unique(pre_mod, axis=0)
        # cycle detection
        cycle = cycling(pre_mod)
        cycle[:, 3] = calc_amplitude(self.series['norm'], cycle)
        self.cycles['t1'] = cycle[:, 0]
        self.cycles['t3'] = cycle[:, 1]
        self.cycles['minimum'] = cycle[:, 2]
        self.cycles['amplitude'] = cycle[:, 3]


    def cycle_to_csv(self):
        self.cycles.to_csv('results_' + self.path)


def calc_amplitude(series, pre):

    num = pre.shape[0]
    amp = np.zeros(num)

    for c in range(num):
        amp[c] = min(series[pre[c, 0]], series[pre[c, 1]]) - pre[c, 3]

    return amp


def cycling(rows):

    # remove rows
    for c in range(rows.shape[0]):
        indices = np.where((rows[c, 2] == rows[:, 2]) & (rows[c, 0] <= rows[:, 0]) & (rows[c, 1] >= rows[:, 1]))[0]
        indices = indices[indices != c]
        rows[indices] = 0

    # remove rows with zeros only
    rows = rows[~np.all(rows == 0, axis=1)]

    return rows


def search_precycle(series, indices, t_a, t_b):

    size = len(indices)
    pre_a = np.zeros((size, 4))
    pre_b = np.zeros((size, 4))

    for c in range(size):
        if t_a[c] < indices[c]:
            values = series[t_a[c]:indices[c] + 1].tolist()

            pre_a[c, 0] = t_a[c]
            pre_a[c, 1] = indices[c]
            pre_a[c, 2] = values.index(min(values)) + t_a[c]
            pre_a[c, 3] = min(values)

        if t_b[c] > indices[c]:
            values = series[indices[c]:t_b[c] + 1].tolist()

            pre_b[c, 0] = indices[c]
            pre_b[c, 1] = t_b[c]
            pre_b[c, 2] = values.index(min(values)) + indices[c]
            pre_b[c, 3] = min(values)

    return np.append(pre_a, pre_b, axis=0)


def soc_eq_find_b2(series, indices):

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


def soc_eq_find_a2(series, indices):

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


def detect_peaks_idx(series):
    """

    """
    # calculate difference between neibhoring values
    diff = np.diff(np.concatenate(([0], series, [0])))
    # calculate sign changes
    asign = np.sign(diff)
    sz = asign == 0
    while sz.any():
        asign[sz] = np.roll(asign, 1)[sz]
        sz = asign == 0
    signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)

    min_idx = []
    max_idx = []
    start = series[0]

    for index in np.where(signchange == 1)[0]:
        if start > 0:
            max_idx += [index - 1]
            start = diff[index]
        else:
            min_idx += [index - 1]
            start = diff[index]

    if min_idx[0] <= 0:
        min_idx = min_idx[1:]
    if max_idx[0] <= 0:
        max_idx = max_idx[1:]

    return min_idx, max_idx

#            if start > 0:

#        print(len(np.where(signchange == 1)[0]))
#        print(len(signchange))
#        print(signchange)
#        print(series)
#        diff = np.diff(series)

#        rising = np.where(diff > 0)
#        print(np.where(np.diff(rising) > 1))
#        falling = np.where(diff <= 0)
#        print(np.where(np.diff(falling) > 1))

#        diff[diff <= 0]
#
#        diff[]
#
#        i = 0
#        for val in diff:
#            if i > 0:
#                if val <= 0 and diff[i-1]:
#            i += 1
#
#
#        print(len(diff))
#        indices = np.where(diff <= 0)
##        values = diff[diff <= 0]
#        indices = np.where(diff <= 0)
#        indices2 = np.where(diff >= 0)
#
#        for val in diff:
#            if val < 0 and
#        print(values)
#        print(indices)
#        print(series[0:100])
#        print(series2[0:100])
#        print()
#        print(series[1:])
#        print(series2)
#        print(len(series))


#    def plot(self):

