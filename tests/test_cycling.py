"""Tests for cycle detection package."""
import pandas as pd
from nose.tools import eq_, raises
from cydets.algorithm import detect_cycles
from pandas.util.testing import assert_frame_equal


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
        example_results = dict(zip(self.df.columns, [41, 85, 44]))
        for column, expected in example_results.items():
            cycles = detect_cycles(self.df[column])
            result = cycles.sum().sum()  # sum along column sums (kind of ID)
            eq_(result, expected, 'Test for example ' + column + ' failed.')


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
        # I just took the current results and assume they are correct
        expected = pd.DataFrame([
                [0, 1.0, 5.0, 3.0, 1.0, 4.0],
                [1, 5.0, 9.0, 7.0, 1.0, 4.0],
                ], columns=['index', 't_start', 't_end', 't_minimum', 'doc', 'duration'])
        assert_frame_equal(cycles, expected)
