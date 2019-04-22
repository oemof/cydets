"""Tests for cycle detection package."""
import pandas as pd
from nose.tools import eq_, raises
from cydets.algorithm import detect_cycles
from pandas.util.testing import assert_frame_equal
from datetime import datetime


class TestErrors():
    """"Check for different error messages when wrong arguments are passed."""

    def __init__(self):
        """Create dataframe with examples."""
        self.df = pd.DataFrame()
        self.df['nones'] = [None, None, None, None]
        self.df['no_peak'] = [0, 0, 0, 0]
        self.df['no_valley'] = [0, 1, 0, -1]

    @raises(ValueError)
    def test_ValueError_no_peak(self):
        """Invoke ValueErrors."""
        detect_cycles(self.df['no_peak'])

    @raises(ValueError)
    def test_ValueError_no_valley(self):
        """Invoke ValueErrors."""
        detect_cycles(self.df['no_valley'])

    @raises(TypeError)
    def test_TypeError(self):
        """Invoke TypeErrors."""
        detect_cycles(self.df['nones'])

    @raises(ValueError)
    def test_ValueError_length(self):
        """Invoke ValueErrors."""
        detect_cycles(pd.Series([0, 1, 0]))

    @raises(ValueError)
    def test_ValueError_no_cycle(self):
        """Invoke ValueErrors."""
        detect_cycles(pd.Series([0, 1, 2, 3, 2, 1, 0]))


class TestExamples():
    """"Check different examples for obtained results."""

    def __init__(self):
        """Create dataframe with examples."""
        self.df = pd.DataFrame()
        self.df['2xlong'] = [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0]
        self.df['2xlong1xshort'] = [0, 1, 0, 0.5, 0, 1, 0, 0.5, 0, 1, 0]
        self.df['mixed'] = [0, 2, 1, 0.5, 2, 2, 3, 1, 1, 2.5, 0]

    def test_examples(self):
        """Apply algorithm and check expected results."""
        example_results = dict(zip(self.df.columns, [40, 79, 41]))
        for column, expected in example_results.items():
            cycles = detect_cycles(self.df[column])
            result = cycles.sum().sum()  # sum along column sums (kind of ID)
            msg = ('Test for example ' + column + ' failed. Expected checksum '
                   + str(expected) + ', is ' + str(result) + '.' + str(cycles))
            eq_(result, expected, msg)


class TestTimeIndex():
    """Check if a timedate index is handled correctly."""

    def __init__(self):
        """Create the same dataframes as TestExamples with another index."""
        twoTimesLong = [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0]
        index = pd.date_range(start='01.01.2019', freq='1d',
                              periods=len(twoTimesLong))
        self.ds = pd.Series(twoTimesLong, index=index)

    def test_example(self):
        """Apply algorithm and check expected results."""
        cycles = detect_cycles(self.ds)
        # using an input series with DatetimeIndex returns the timestamps
        # for start, end and minimum as well as a timedelta as duration
        t0 = datetime.strptime('2019-01-02', '%Y-%m-%d')
        t1 = datetime.strptime('2019-01-06', '%Y-%m-%d')
        t2 = datetime.strptime('2019-01-10', '%Y-%m-%d')
        tmin1 = datetime.strptime('2019-01-04', '%Y-%m-%d')
        tmin2 =datetime.strptime('2019-01-08', '%Y-%m-%d')
        expected = pd.DataFrame(
                [[t0, t1, tmin1, 1.0, t1 - t0],
                 [t1, t2, tmin2, 1.0, t2 - t1]],
                columns=['t_start', 't_end', 't_minimum', 'doc', 'duration'])

        assert_frame_equal(cycles, expected)
