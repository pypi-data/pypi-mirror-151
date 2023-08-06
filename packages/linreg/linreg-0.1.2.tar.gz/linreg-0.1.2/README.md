# linreg

Simple and flexible interface for basic linear regression.

## Motivation

I wanted to do very basic linear regression between two arrays of data.
It's a pain in the ass having to remember scikit-learn's interface for regression,
remember matplotlib's interface for plotting, and also having to do things like `np.array(x).reshape(1,-1)` 
so that it works with sklearn

I wanted to create an interface that is as simple as possible and also relatively flexible with your input
so that you don't have to open google every time you want to do some basic regression checking

## Usage

linreg supports basic lists, numpy arrays, and pandas series

<img src="https://raw.githubusercontent.com/purpleladydragons/linreg/main/img/plot.png" width=400>

```python
import linreg

x = [1,2,3]
y = [2,4,6]

linreg.linreg(x, y)
```

You can disable plotting with `plot=False`

If your data is a list of tuples, that works too
```python
import linreg

xy = [
    (1,2),
    (2,4),
    (3,6)
]
linreg.linreg(xy)
```

If your data is flipped, such that each column is a data point (instead of each row), then you can transpose it:
```python
import linreg

xy = [
    [1,2,3,4],
    [2,4,6,8]
]

linreg.linreg(xy, transpose=True)
```

If you forget to transpose in the above case, linreg will log a warning. 
It works by assuming that if you have more dimensions than data points, then you probably forgot to transpose.  
You can suppress these warnings with `warn=False`
