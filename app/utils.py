from app.exceptions import RequiredArgumentsMissing


def check_if_request_has_required_params(request_args, required_params):
    missing_args = [param for param in required_params if not request_args.get(param)]
    if missing_args:
        raise RequiredArgumentsMissing('Following arguments missing: {}'.format(', '.join(missing_args)))
