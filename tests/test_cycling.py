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

    @raises(IndexError)
    def test_IndexError(self, columns=None):
        """Invoke IndexErrors."""
        detect_cycles(self.df['zeros'])

    @raises(TypeError)
    def test_TypeError(self, columns=None):
        """Invoke TypeErrors."""
        detect_cycles(self.df['nones'])


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
