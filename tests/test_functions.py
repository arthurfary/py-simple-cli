from pysimplecli import functions

def test_command_direct(capfd):
    @functions.command
    def print_name(name: str) -> None:
        print(name)
    
    print_name('bob')
    capture = capfd.readouterr()
    assert capture.out == 'bob\n'

def test_command_with_sys_args(capfd, monkeypatch):
    @functions.command
    def print_name(name: str) -> None:
        print(name)
    
    # Simulate command line arguments
    monkeypatch.setattr('sys.argv', ['script_name', 'print_name', 'arthur'])
    functions.run_cli()
    capture = capfd.readouterr()
    assert capture.out == 'arthur\n'
