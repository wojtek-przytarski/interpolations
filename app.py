import math

from flask import Flask, render_template, request

from exceptions import RequiredArgumentsMissing
from figure_creator import FigureCreator
from interpolation import get_interpolation_axes, get_original_axes
from utils import check_if_request_has_required_params
app = Flask(__name__)
figure_creator = FigureCreator()


@app.route('/', methods=['GET'])
def home():
    try:
        check_if_request_has_required_params(request.args, ['f', 'a', 'b', 'n'])
        f = lambda x: eval(request.args.get('f'))
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        n = int(request.args.get('n'))
    except RequiredArgumentsMissing as ex:
        return render_template('main.html', error=str(ex))
    except SyntaxError as ex:
        return render_template('main.html', error='Error in function provided: {}'.format(request.args.get('f')))
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
