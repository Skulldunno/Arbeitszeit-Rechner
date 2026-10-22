import json

class Zeitnachweis:
    def __init__(self):
        self.daten = {}
        self.load_data()

    def save_data(self, data):
        with open("zeitnachweis.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        self.load_data()

    def load_data(self):
        with open("zeitnachweis.json", "r", encoding="utf-8") as file:
            self.daten = json.load(file)
