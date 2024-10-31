
import sys
from functools import wraps

_commands = {}  # Store all registered commands

def command(func):
    _commands[func.__name__] = func  # Register the command
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        argv = sys.argv[1:]  # Get command line arguments
        if argv:  # If we have command line arguments
            return func(*argv)
        return func()  # If no arguments provided
    return wrapper_func

def run_cli():
    """Run the CLI with the registered commands"""
    if len(sys.argv) < 2:
        print("Available commands:", ", ".join(_commands.keys()))
        return
    
    command_name = sys.argv[1]
    if command_name in _commands:
        args = sys.argv[2:]  # Get arguments after the command name
        if args:
            try:
                _commands[command_name](*args)
            except TypeError as e:
                print("Missing required argument:", str(e).split("'")[1])
        else:
            _commands[command_name]()
    else:
        print(f"Unknown command: {command_name}")
        print("Available commands:", ", ".join(_commands.keys()))
