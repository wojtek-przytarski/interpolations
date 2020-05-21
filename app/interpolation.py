def difference_quotients(x, f):
    """
    Counts difference quotients for given nodes and function values
    :param x: list of nodes x0,...,xn
    :param f: list of values: f(x0),...,f(xn)
    :return: list of difference quotients
    """
    n = len(f)

    dq = [f[i] for i in range(n)]

    for j in range(1, n):
        for i in range(n-1, j, -1):
            dq[i] = (dq[i] - dq[i-1]) / (x[i] - x[i-j])
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
    nt = fx[len(x)-1]

    for k in range(len(x)-1, 0, -1):
        nt = fx[k] + (t-x[k]) * nt
    return nt


def natural_form_coefficients(x, fx):
    """
    Counts coefficients of natural form.
    :param x: list of nodes x0,...,xn
    :param fx: list of difference quotients f(x0), f(x0,x1), ..., f(x0,...,xn)
    :return: list of coefficients
    """
    n = len(fx)
    a = list()
    a[n] = fx[n]

    for i in range(n-1, 0, -1):
        a[i] = fx[i]
        for k in range(i-1, n):
            a[k] -= x[i] * a[k]
    return a


def get_original_axes(f, a, b, n, accuracy=40):
    points_number = n * accuracy
    distance = (b-a) / points_number
    x_axis = [a + i * distance for i in range(points_number)]
    y_axis = [f(x_axis[i]) for i in range(points_number)]
    return x_axis, y_axis


def get_original_points(f, a, b, n, accuracy=40):
    points_number = n * accuracy
    distance = (b-a) / points_number
    data = []
    for i in range(points_number):
        x = a + i * distance
        data.append({
            'x': x,
            'y': f(x)
        })
    return data


def get_interpolation_axes(f, a, b, n, accuracy=40):
    h = (b - a) / n
    x = [a + i * h for i in range(n)]
    fx = [f(x[i]) for i in range(n)]

    dq = difference_quotients(x, fx)

    points_number = n * accuracy
    distance = (b - a) / points_number
    x_axis = [a + i * distance for i in range(points_number)]

    npv = [newton_polynomial_value(x, dq, x_axis[i]) for i in range(len(x_axis))]
    return x_axis, npv


def get_interpolation_points(f, a, b, n, accuracy=40):
    h = (b - a) / n
    x = [a + i * h for i in range(n)]
    fx = [f(x[i]) for i in range(n)]

    dq = difference_quotients(x, fx)

    points_number = n * accuracy
    distance = (b - a) / points_number
    data = []
    for i in range(points_number):
        xi = a + i * distance
        data.append({
            'x': xi,
            'y': newton_polynomial_value(x, dq, xi)
        })
    return data
