import parser

from math import e, sin
from flask import render_template, request, Flask, make_response

from app.exceptions import RequiredArgumentsMissing
from app.figure_creator import FigureCreator
from app.interpolation import get_interpolation_axes, get_original_axes
from app.utils import check_if_request_has_required_params

app = Flask(__name__)
figure_creator = FigureCreator()


@app.route("/", methods=["GET"])
def home():
    params = request.args
    try:
        check_if_request_has_required_params(params, ["f", "a", "b", "n"])
        formula = parser.expr(params.get("f")).compile()

        a = float(params.get("a"))
        b = float(params.get("b"))
        n = int(params.get("n"))
        if a >= b:
            raise RequiredArgumentsMissing(
                "Please provide valid parameters: a should be lower than b."
            )
        plots = get_plots(lambda x: eval(formula), a, b, n)
    except RequiredArgumentsMissing as ex:
        return render_template("main.html", error=str(ex), params=params)
    except SyntaxError as ex:
        return render_template(
            "main.html",
            error="Error in function provided: {}".format(params.get("f")),
            params=params,
        )
    except Exception as ex:
        return render_template(
            "main.html", error="Error: {}".format(str(ex)), params=params
        )
    return render_template("main.html", plots=plots, params=params)


@app.route("/api/plots", methods=["GET"])
def plot_points():
    params = request.args
    try:
        check_if_request_has_required_params(params, ["f", "a", "b", "n"])
        formula = parser.expr(params.get("f")).compile()

        a = float(params.get("a"))
        b = float(params.get("b"))
        n = int(params.get("n"))
        if a >= b:
            raise RequiredArgumentsMissing(
                "Please provide valid parameters: a should be lower than b."
            )

        x, fx = get_original_axes(lambda x: eval(formula), a, b, n)
        x, npv = get_interpolation_axes(lambda x: eval(formula), a, b, n)

        data = {
            'x': x,
            'npv': npv,
            'fx': fx,
        }
    except SyntaxError:
        data = {'error': f"Error in function provided: {params.get('f')}"}
        return make_response(data, 400)
    except Exception as ex:
        data = {'error': str(ex)}
        return make_response(data, 400)
    return make_response(data)


def get_plots(f, a, b, n):
    x, fx = get_original_axes(f, a, b, n)
    x, npv = get_interpolation_axes(f, a, b, n)
    plots = {
        "interpolated": figure_creator.create_figure([(x, npv, 'Interpolated')]),
        "original": figure_creator.create_figure([(x, fx, 'Original')]),
        "both": figure_creator.create_figure([(x, fx, 'Original'), (x, npv, 'Interpolated')]),
    }
    return plots
