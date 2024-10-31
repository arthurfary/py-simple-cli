
from pysimplecli import functions


@functions.command
def greet(name, age):
    print("Hello ", name, age)


functions.run_cli()
