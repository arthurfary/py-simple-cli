import sys
from functools import wraps

_commands = {}


class CliSyntaxError(Exception):
    """Raised when CLI arguments are in wrong order"""
    pass


def _parse_cli_args(argv):
    args = []
    kwargs = {}

    seen_kwarg = False

    for arg in argv:
        if '=' in arg:
            seen_kwarg = True
            key, value = arg.split('=', 1)
            kwargs[key] = value
        else:
            if seen_kwarg:
                raise CliSyntaxError(
                    "Positional arguments must come before keyword arguments. "
                    f"Found positional argument '{arg}' after keyword arguments."
                )
            args.append(arg)

    return args, kwargs


def command(func):
    """Decorator used to create cli commands.

    Usage:

        @command
        def mycommand(var1, var2=None):
            ...

        # will create a cli command called 'mycommand' that has
        # two vars as parameters

    """
    # appends func name to list of funcs
    _commands[func.__name__] = func

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        # this allows the function to be called directly in script
        if args or kwargs:
            return func(*args, **kwargs)

        # Get arguments after the command name
        argv = sys.argv[2:] if len(sys.argv) > 2 else []
        args, kwargs = _parse_cli_args(argv)
        return func(*args, **kwargs)

    return wrapper_func

# TODO: 1 - Make a main function replacer
# should be able to run the cli with no parameters
# and get something, like 'pytest' or ls


def run_cli():
    """Run the CLI with the registered commands"""
    if len(sys.argv) < 2:
        print("Available commands:", ", ".join(_commands.keys()))
        return

    command_name = sys.argv[1]
    if command_name not in _commands:
        print(f"Unknown command: {command_name}")
        print("Available commands:", ", ".join(_commands.keys()))
        return

    try:
        argv = sys.argv[2:]
        args, kwargs = _parse_cli_args(argv)
        _commands[command_name](*args, **kwargs)

    except CliSyntaxError as e:
        print(f"Error: {str(e)}")

    except TypeError as e:
        print("Missing required argument:", str(e).split("'")[1])
