# helloWorld("print")
from cli import CLI
from gui import GUI


class main:
    def __init__(self):
        #self.cli = CLI()
        self.gui = GUI()

    def start(self):
        #self.cli.start_cli()
        self.gui.start()

if __name__ == "__main__":
    App = main().start()