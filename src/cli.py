class CLI:
    def __init__(self):
        pass

    def input(self):
        try:
            time = input("Uhrzeit eingeben in (HH:MM): ")
        except:
            print("Ungültige Uhrzeit eingegeben.\n")
        else:
            print(f"Deine Eingabe war {time}.\n Die Notierte Zeit ist {}")

if __name__ == "__main__":
    test = CLI().input()