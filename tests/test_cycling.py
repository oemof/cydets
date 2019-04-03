"""Tests for cycle detection package."""
import pandas as pd
from nose.tools import eq_, raises
from cycle_detection.algorithm import detect_cycles


class TestErrors():
    """"Check for different error messages when wrong arguments are passed."""

    def __init__(self):
        """Create dataframe with examples."""
        self.df = pd.DataFrame()
        self.df['zeros'] = [0, 0, 0]
        self.df['nones'] = [None, None, None]
        self.df['no_peak'] = [0, 0, 0, 0]
        self.df['no_valley'] = [0, 1, 0, -1]
        self.df['no_cycle'] = [0, 1, 2, 3, 2, 1, 0]

    @raises(ValueError)
    def test_ValueError_length(self):
        """Invoke ValueErrors."""
        detect_cycles(self.df['zeros'])

    @raises(ValueError)
    def test_ValueError_no_peak(self):
        """Invoke ValueErrors."""
        detect_cycles(self.df['no_peak'])

    @raises(ValueError)
    def test_ValueError_no_valley(self):
        """Invoke ValueErrors."""
        detect_cycles(self.df['no_valley'])

    @raises(ValueError)
    def test_ValueError_no_cycle(self):
        """Invoke ValueErrors."""
        detect_cycles(self.df['no_cycle'])

    @raises(TypeError)
    def test_TypeError(self):
        """Invoke TypeErrors."""
        detect_cycles(self.df['nones'])

    @raises(ValueError)


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
            eq_(result, expected, 'Test for example ' + column + ' failed.')
