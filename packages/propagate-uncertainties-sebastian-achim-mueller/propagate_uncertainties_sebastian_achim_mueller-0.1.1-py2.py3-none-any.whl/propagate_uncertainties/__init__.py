import numpy as np


def auN(dfdx, x_au):
    """
    Absolute uncertainty of function f(x1, x2, ..., xN), assuming the
    N parameters x1 to xN are not correlated.

    Parameters
    ----------
    dfdx : array of floats, length N
        Derivatives of f w.r.t. x1 to xN.
    x_au : array of floats, length N
        Absolute uncertainties of x1 to xN.
    Returns
    -------
    Absolute uncertainty : float
    """
    dfdx = np.array(dfdx)
    x_au = np.array(x_au)
    assert len(dfdx) == len(x_au)
    S = 0.0
    for i in range(len(x_au)):
        S += (dfdx[i] * x_au[i]) ** 2.0
    return np.sqrt(S)


def au2(x_au, dfdx, y_au, dfdy):
    """
    Estimate the absolute uncertainty of function f(x,y), assuming the
    two parameters x and y are not correlated.

    Parameters
    ----------
    x_au : float
        Absolute uncertainty of x.
    y_au : float
        Absolute uncertainty of y.
    dfdx : float
        Derivative of f(x,y) w.r.t x, at (x,y).
    dfdy : float
        Derivative of f(x,y) w.r.t x, at (x,y).

    Returns
    -------
    Absolute uncertainty : float
    """
    return auN(dfdx=[dfdx, dfdy], x_au=[x_au, y_au])


def add(x, y):
    """
    Add x to y.

    Parameters
    ----------
    x : tubple(float, float)
        Value and absolute uncertainty of x
    y : tubple(float, float)
        Value and absolute uncertainty of y

    Returns
    -------
    x + y and absolute uncertainty : tuple(float, float)

    Derivative
    ----------
    f(x,y) = x + y
    df/dx = 1
    df/dy = 1
    """
    return x[0] + y[0], au2(x_au=x[1], dfdx=1.0, y_au=y[1], dfdy=1.0)


def multiply(x, y):
    """
    Multiply x by y.

    Parameters
    ----------
    x : tubple(float, float)
        Value and absolute uncertainty of x
    y : tubple(float, float)
        Value and absolute uncertainty of y

    Returns
    -------
    x * y and abs. uncertainty : tuple(float, float)

    Derivative
    ----------
    f(x,y) = x * y
    df/dx = y
    df/dy = x
    """
    return x[0] * y[0], au2(x_au=x[1], dfdx=y[0], y_au=y[1], dfdy=x[0])


def divide(x, y):
    """
    Divide x by y.

    Parameters
    ----------
    x : tubple(float, float)
        Value and absolute uncertainty of x
    y : tubple(float, float)
        Value and absolute uncertainty of y

    Returns
    -------
    x / y and abs. uncertainty : tuple(float, float)

    derivative
    ----------
    f(x,y) = x * y^{-1}
    df/dx = 1
    df/dy = -1x * y^{-2}
    """
    return (
        x[0] / y[0],
        au2(
            x_au=x[1],
            dfdx=1.0 / y[0],
            y_au=y[1],
            dfdy=(-1 * x[0] * y[0] ** (-2)),
        ),
    )


def prod(x):
    """
    Multilpy all elements in x

    Parameters
    ----------
    x : tuple(array of floats, array of floats)
        Values and absolute uncertainties of x

    Returns
    -------
    Product and abs. uncertainty : tuple(float, float)
    """
    x_au = np.array(x[1])
    x = np.array(x[0])
    assert len(x) == len(x_au)
    P = np.prod(x)
    dfdxs = []
    for i in range(len(x)):
        mask_i = np.ones(len(x), dtype=np.bool)
        mask_i[i] = False
        dfdxi = np.prod(x[mask_i])
        dfdxs.append(dfdxi)

    Pau = auN(dfdx=dfdxs, x_au=x_au)
    return P, Pau


def sum(x):
    """
    Add all elements in x

    Parameters
    ----------
    x : tuple(array of floats, array of floats)
        Values and absolute uncertainties of x

    Returns
    -------
    Sum and abs. uncertainty : tuple(float, float)
    """
    x_au = np.array(x[1])
    x = np.array(x[0])
    assert len(x) == len(x_au)
    S = np.sum(x)
    dfdxs = np.ones(len(x))
    S_au = auN(dfdx=dfdxs, x_au=x_au)
    return S, S_au


def integrate(f, x_bin_edges):
    """
    Integrate function f(x).

    Parameters
    ----------
    f : tuple(array of floats, array of floats)
        Values and absolute uncertainties of f(x)
    x_bin_edges : array of floats
        Edges of bins in x.

    Returns
    -------
    Integral and uncertainty : tuple(float, float)
    """
    f_au = np.array(f[1])
    f = np.array(f[0])
    num_bins = len(x_bin_edges) - 1
    assert len(f) == len(f_au)
    assert len(f) == num_bins

    a = np.zeros(num_bins)
    a_au = np.zeros(num_bins)
    for i in range(num_bins):
        step = x_bin_edges[i + 1] - x_bin_edges[i]
        assert step >= 0.0
        a[i], a_au[i] = multiply(x=(f[i], f_au[i]), y=(step, 0.0))
    return sum((a, a_au))
