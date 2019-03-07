import math

from flask import Flask, render_template, request

from figure_creator import FigureCreator
from interpolation import get_interpolation_axes, get_original_axes

app = Flask(__name__)
figure_creator = FigureCreator()


@app.route('/', methods=['GET'])
def hello_world():
    f = lambda x: x**2 * math.sin(x)
    a = float(request.args.get('a', 0.0))
    b = float(request.args.get('b', 1.0))
    n = int(request.args.get('n', 5))
    return render_template('main.html', plots=get_plots(f, a, b, n))


def get_plots(f, a, b, n):
    x, fx = get_original_axes(f, a, b, n)
    x, npv = get_interpolation_axes(f, a, b, n)
    plots = {'interpolated': figure_creator.create_figure([(x, npv)]),
             'original': figure_creator.create_figure([(x, fx)]),
             'both': figure_creator.create_figure([(x, fx), (x, npv)])}
    return plots


if __name__ == '__main__':
    app.debug = True
    app.run()
