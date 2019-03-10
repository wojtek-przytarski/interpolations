from math import e, sin, cos, sqrt, pow, tan, pi, exp

from flask import Flask, render_template, request

from exceptions import RequiredArgumentsMissing
from figure_creator import FigureCreator
from interpolation import get_interpolation_axes, get_original_axes
from utils import check_if_request_has_required_params

app = Flask(__name__)
figure_creator = FigureCreator()


@app.route('/', methods=['GET'])
def home():
    params = request.args
    try:
        check_if_request_has_required_params(params, ['f', 'a', 'b', 'n'])
        f = lambda x: eval(params.get('f'))
        a = float(params.get('a'))
        b = float(params.get('b'))
        n = int(params.get('n'))
        if a >= b:
            raise RequiredArgumentsMissing('Please provide valid parameters: a should be lower than b.')
        plots = get_plots(f, a, b, n)
    except RequiredArgumentsMissing as ex:
        return render_template('main.html', error=str(ex), params=params)
    except SyntaxError as ex:
        return render_template('main.html', error='Error in function provided: {}'.format(params.get('f')),
                               params=params)
    except Exception as ex:
        return render_template('main.html', error='Error: {}'.format(str(ex)), params=params)
    return render_template('main.html', plots=plots, params=params)


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
