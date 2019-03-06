def difference_quotients(x, f):
    """
    Counts difference quotients for given nodes and function values
    :param x: list of nodes x0,...,xn
    :param f: list of values: f(x0),...,f(xn)
    :return: list of difference quotients
    """
    n = len(f)

    dq = [f[i] for i in range(0, n)]

    for j in range(0, n):
        i = n - 1
        while i >= j:
            dq[i + 1] = (dq[i + 1] - dq[i]) / (x[i + 1] - x[i - j + 1])
            i -= 1
    return dq


def newton_polynomial_value(x, fx, t):
    """
    Counts value of nth degree polynomial in point t.
    It uses Horner's method.
    :param x: list of nodes x0,...xn
    :param fx: list of difference quotients f(x0), f(x0,x1), ..., f(x0,...,xn)
    :param t: point
    :return: value in point t
    """
    k = len(fx) - 2
    nt = fx[k+1]

    while k > 0:
        nt = fx[k] + (t-x[k]) * nt
        k -= 1
    return nt


def natural_form_coefficients(x, fx):
    """
    Counts coefficients of natural form.
    :param x: list of nodes x0,...,xn
    :param fx: list of difference quotients f(x0), f(x0,x1), ..., f(x0,...,xn)
    :return: list of coefficients
    """
    n = len(fx) - 1
    a = list()
    a[n] = fx[n]
    i = n - 1

    while i > 0:
        a[i] = fx[i]
        for k in range(i, n):
            a[k] -= x[i] * a[k+1]
        i -= 1
    return a
