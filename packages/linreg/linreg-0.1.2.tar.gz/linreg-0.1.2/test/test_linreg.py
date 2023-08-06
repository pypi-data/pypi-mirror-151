import sys
import numpy as np
import pandas as pd

sys.path.append('../src')
from src import linreg


def lr(*args, **kwargs):
    kwargs['plot'] = False
    return linreg.linreg(*args, **kwargs)


def test_x_and_y():
    x = [1, 2, 3]
    y = [2, 4, 6]

    assert lr(x, y) == 1


def test_combined_xy():
    xy = [
        (1, 2),
        (2, 4),
        (3, 6)
    ]
    assert lr(xy) == 1


def test_multivariate_combined():
    z = [
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9],
        [4, 8, 12]
    ]
    assert lr(z) == 1


def test_1d_input():
    x = [1, 2, 3, 4]
    y = [2, 4, 6, 8]

    assert lr(x, y) == 1


def test_numpy_array():
    x = np.array([1, 2, 3])
    y = np.array([2, 4, 6])
    assert lr(x, y) == 1

    xy = np.array([[1, 2],
                   [2, 4],
                   [3, 6]])

    assert lr(xy) == 1


def test_pandas_series():
    x = pd.Series([1, 2, 3])
    y = pd.Series([2, 4, 6])

    assert lr(x, y) == 1

    xy = pd.concat([x, y], axis=1)
    assert lr(xy) == 1


def test_transpose(capsys):
    z = [
        [1, 2, 3, 4],
        [2, 4, 6, 8]
    ]
    assert lr(z, transpose=True) == 1

    captured = capsys.readouterr()
    assert 'WARNING' not in captured.out


def test_warning(capsys):
    z = [
        [1, 2, 3, 4],
        [2, 4, 6, 8]
    ]
    lr(z)

    captured = capsys.readouterr()
    assert 'WARNING' in captured.out
