from pysimplecli import functions
import pytest


def test_command_kwargs_and_args(monkeypatch, capfd):
    @functions.command
    def get_with_kw_arg(name, age):
        print(f"{name} {age}")

    monkeypatch.setattr(
        'sys.argv', ['script_name', 'get_with_kw_arg', 'arthur', 'age=30']
    )
    functions.run_cli()
    capture = capfd.readouterr()
    assert capture.out == 'arthur 30\n'

# Additional test cases would be good:


def test_command_mixed_args(monkeypatch, capfd):
    @functions.command
    def complex_greeting(name, age, city="Unknown", country="Unknown"):
        print(f"{name} ({age}) from {city}, {country}")

    # Test various combinations
    tests = [
        (
            ['script.py', 'complex_greeting', 'arthur', '30', 'city=london'],
            'arthur (30) from london, Unknown\n'
        ),
        (
            ['script.py', 'complex_greeting', 'name=bob', 'age=25', 'country=uk'],
            'bob (25) from Unknown, uk\n'
        ),
    ]

    for args, expected in tests:
        monkeypatch.setattr('sys.argv', args)
        functions.run_cli()
        capture = capfd.readouterr()
        assert capture.out == expected


def test_parse_cli_args():
    # These should work
    args, kwargs = functions._parse_cli_args(['bob', '25', 'city=london'])
    assert args == ['bob', '25']
    assert kwargs == {'city': 'london'}

    # This should raise CliSyntaxError
    with pytest.raises(functions.CliSyntaxError):
        functions._parse_cli_args(['name=bob', 'london'])
