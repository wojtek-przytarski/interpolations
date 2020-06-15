import parser

from math import e, sin

from flask import request, Flask, make_response

from app.exceptions import RequiredArgumentsMissing
from app.interpolation import get_interpolation_axes
from app.utils import check_if_request_has_required_params

app = Flask(__name__)


@app.route("/api/plots", methods=["GET"])
def plot_data():
    params = request.args
    try:
        check_if_request_has_required_params(params, ["f", "a", "b", "n"])
        function_str = params.get("f")
        formula = parser.expr(function_str).compile()

        a = float(params.get("a"))
        b = float(params.get("b"))
        n = int(params.get("n"))
        if a >= b:
            raise RequiredArgumentsMissing(
                "Please provide valid parameters: a should be lower than b."
            )

        data = get_interpolation_axes(lambda x: eval(formula), a, b, n)
        data['plotArgs'] = {
            'f': function_str,
            'a': a,
            'b': b,
            'n': n,
        }
    except SyntaxError:
        return make_error_response(f"Error in function provided: {params.get('f')}")
    except Exception as ex:
        return make_error_response(str(ex))
    return make_cors_response(data)


def make_error_response(error_message: str, status_code: int = 400):
    data = {'error': error_message}
    return make_cors_response(data, status_code)


def make_cors_response(data: dict, status_code: int = 200):
    response = make_response(data, status_code)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response
