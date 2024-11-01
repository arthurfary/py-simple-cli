
from pysimplecli import functions


@functions.command
def greet(name, age=10):
    print("Hello", name, age)


functions.run_cli()
