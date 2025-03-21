
# cli.py (refactored)

import sys
from functools import wraps


class CLI:
    class CliSyntaxError(Exception):
        """Raised when CLI arguments are in wrong order."""
        pass

    def __init__(self):
        self.commands = {}

    @staticmethod
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
                    raise CLI.CliSyntaxError(
                        "Positional arguments must come before keyword arguments. "
                        f"Found positional argument '{arg}' after keyword arguments."
                    )
                args.append(arg)
        return args, kwargs

    def command(self, func):
        """Decorator to register a CLI command."""
        self.commands[func.__name__] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            # If called with parameters (direct call), use them
            if args or kwargs:
                return func(*args, **kwargs)
            # Otherwise parse sys.argv for command parameters
            argv = sys.argv[2:] if len(sys.argv) > 2 else []
            parsed_args, parsed_kwargs = self._parse_cli_args(argv)
            return func(*parsed_args, **parsed_kwargs)
        return wrapper

    def main(self, func):
        """Decorator to register the main command (used if no command is given)."""
        self.commands["main"] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def run(self):
        """Run the CLI by dispatching the correct command."""
        if len(sys.argv) == 1:
            command_name = "main"
        else:
            command_name = sys.argv[1]

        if command_name == "help":
            print("Available commands:", ", ".join(self.commands.keys()))
            return

        if command_name not in self.commands:
            print(f"Unknown command: {command_name}")
            print("Available commands:", ", ".join(self.commands.keys()))
            return

        try:
            argv = sys.argv[2:]
            args, kwargs = self._parse_cli_args(argv)
            self.commands[command_name](*args, **kwargs)
        except CLI.CliSyntaxError as e:
            print(f"Error: {e}")
        except TypeError as e:
            # This simplistic approach extracts the missing argument's name from the error message.
            missing_arg = str(e).split("'")[1] if "'" in str(e) else "unknown"
            print("Missing required argument:", missing_arg)


# Example usage:
cli = CLI()


@cli.command
def greet(name, punctuation="!"):
    """Greet someone by name."""
    print(f"Hello, {name}{punctuation}")


@cli.main
def default():
    print("This is the default command. Try 'help' for available commands.")


if __name__ == "__main__":
    cli.run()
