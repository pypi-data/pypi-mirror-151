import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def linreg(x, y=None, plot=True, fit_intercept=True, transpose=False, warn=True):
    """

    :param x:
    :param y:
    :param plot: whether to display plot or not
    :param fit_intercept: whether to fit an intercept value or not
    :param transpose: if True and y=None, transposes x
    :param warn: if True, prints warnings when encountered
    :return:
    """
    x = np.array(x)
    if y is None:
        if transpose:
            x = np.transpose(x)

        rows, cols = x.shape
        if cols > rows and warn:
            if transpose:
                print(
                    'WARNING: You have more dimensions than data points after transposing. Did you mean to transpose?')
            else:
                print(
                    'WARNING: You have more dimensions than data points. Did you want to transpose? You can do so with transpose=True')

        y = x[:, -1]
        x = x[:, :-1]

    if x.ndim == 1:
        x = np.array(x).reshape(-1, 1)

    reg = LinearRegression(fit_intercept=fit_intercept).fit(x, y)
    if plot and x.shape[1] == 1:
        ypred = reg.coef_ * x + reg.intercept_

        fig, ax = plt.subplots()

        bbox_props = {
            'edgecolor': 'black',
            'facecolor': 'white'
        }

        intercept = str(round(reg.intercept_, 2))
        coef = str(round(reg.coef_[0], 2))
        eqtion = f"y={coef}x + {intercept}"
        r2 = f"R^2={round(reg.score(x,y), 4)}"
        textstr = f"{eqtion}\n{r2}"

        ax.text(0.5, 0.91, textstr, horizontalalignment='center', transform=plt.gcf().transFigure, bbox=bbox_props)

        ax.plot(x, ypred, color='red')
        ax.scatter(x=x, y=y)

        plt.show()

    return reg.score(x, y)
