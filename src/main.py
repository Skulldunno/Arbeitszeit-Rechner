# helloWorld("print")
from cli import CLI


class main:
    def __init__(self):
        self.cli = CLI()

    def start(self):
        self.cli.start_cli()

if __name__ == "__main__":
    App = main().start()