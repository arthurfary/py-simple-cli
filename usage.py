
from pysimplecli import functions

cli = functions.CLI()


@cli.command
def greet(name, punctuation="!"):
    """Greet someone by name."""
    print(f"Hello, {name}{punctuation}")


@cli.main
def default():
    print("This is the default command. Try 'help' for available commands.")


if __name__ == "__main__":
    cli.run()
