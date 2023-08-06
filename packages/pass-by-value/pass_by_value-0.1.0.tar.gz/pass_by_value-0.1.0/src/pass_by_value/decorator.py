from copy import deepcopy
from warnings import warn


def pass_by_value(func):
    def wrapper(*args, **kwargs):
        new_args = []
        new_kwargs = {}

        for arg in args:
            new_args.append(_copy_argument(arg))
        for key, value in kwargs.items():
            new_kwargs[key] = _copy_argument(value)
        return func(*new_args, **new_kwargs)

    return wrapper


def _copy_argument(argument):
    try:
        return deepcopy(argument)
    except Exception:
        warn(
            f"Argument {argument} of type "
            "{type(argument)} can't be copied, "
            "passing by object-reference"
        )
        return argument
