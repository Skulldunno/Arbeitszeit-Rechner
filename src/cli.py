from datetime import datetime, date
from zeitrechner import WorkTimeCaluclator
REPLACABLE = [":",",",".","/","-"]

class CLI:
    def __init__(self):
        self.calc = WorkTimeCaluclator()

    def start_cli(self):
        print("Willkommen zum Arbeitszeitrechner")
        self.main_menu()

    def main_menu(self):
        while True:
            print("Hauptmenü:")
            print("1. Arbeitszeit berechnen")
            print("2. Frühstückspause ändern")
            print("3. Mittagspause ändern")
            print("4. Gespeicherte Arbeitszeiten anzeigen")
            print("5. Beenden")
            choice = input("Bitte wähle eine Option (1-5): ")
            if choice == "1":
                self.working_hours_input()
            elif choice == "2":
                self.breakfast_option()
            elif choice == "3":
                self.lunchtime_option()
            elif choice == "4":
                self.show_saved_working_hours()
            elif choice == "5":
                print("Programm wird beendet.")
                break
            else:
                print("Ungültige Eingabe. Bitte wähle eine Option von 1 bis 4.")
    
    def show_saved_working_hours(self):
        if not self.calc.zeitnachweis.daten:
            print("Keine gespeicherten Arbeitszeiten vorhanden.")
            return
        print("Gespeicherte Arbeitszeiten:")
        for date, data in self.calc.zeitnachweis.daten.items():
            arrival_time = data.get("arrival_time", "N/A")
            leave_time = data.get("leave_time", "N/A")
            flextime = data.get("flextime", "N/A")
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            print(f"Datum: {date} {date_obj.strftime("%a")}, Ankunftszeit: {arrival_time}, Abreisezeit: {leave_time}, Gleitzeit: {flextime} Minuten")
        
        input("\nReturn drücken zum Fortfahren\n")
    
    def breakfast_option(self):
        while True:
            breakfast_option = input("Möchtest du die Frühstückspause ändern? (y/n): ")
            if breakfast_option.lower() == "y":
                breakfast_start = self.input_time(True)
                breakfast_end = self.input_time(False)
                self.calc.breakfast = [breakfast_start, breakfast_end]
                break
            elif breakfast_option.lower() == "n":
                break
            else:
                print("Ungültige Eingabe. Bitte gib 'y' oder 'n' ein.")

    def lunchtime_option(self):
        while True:
            lunchtime_option = input("Möchtest du die Mittagspause ändern? (y/n): ")
            if lunchtime_option.lower() == "y":
                lunchtime_start = self.input_time(True)
                lunchtime_end = self.input_time(False)
                self.calc.lunchtime = [lunchtime_start, lunchtime_end]
                break
            elif lunchtime_option.lower() == "n":
                break
            else:
                print("Ungültige Eingabe. Bitte gib 'y' oder 'n' ein.")

    def working_hours_input(self):
        arrival_time = self.input_time(True)
        if arrival_time == None:
            return None
        else:
            arrival_time = self.calc.round_up_to_multiple_of_five(arrival_time)
        leave_time = self.input_time(False)
        if leave_time == None:
            return None
        else:
            leave_time = self.calc.round_up_to_multiple_of_five(leave_time, False)
        flextime = self.calc.calc_work_flextime(arrival_time, leave_time)
        print(f"Deine Gleitzeit für Heute beträgt {flextime} Minuten.\n")
        print(f"Möchtest du die Arbeitszeit speichern? (y/n): ")
        if input().lower() == "y":
            date = self.date_input()
            self.save_working_hours(arrival_time, leave_time, flextime, date)
            print("Arbeitszeit erfolgreich gespeichert.")

    def date_input(self):
        while True:
            date_input = input("Bitte gib ein Datum ein (YYYY-MM-DD) oder today: ")
            if date_input.lower() == "today":
                return date.today()
            else:
                try:
                    valid_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                    print(valid_date)
                    return valid_date
                except ValueError:
                    print("Ungültiges Datum. Bitte gib das Datum im Format YYYY-MM-DD ein.")
        
    def save_working_hours(self, arrival_time, leave_time, flextime, date):
        data = {
            str(date): {
                "arrival_time": arrival_time,
                "leave_time": leave_time,
                "flextime": flextime
            }
        }
        self.calc.zeitnachweis.save_data(data)
        
    def input_time(self, arrive: False):
        while True:
            try:
                if arrive:
                    time = input("Ankunftszeit eingeben in HH:MM: ")
                else:
                    time = input("Abreisezeit eingeben in HH:MM: ")
                if time == "exit":
                    return print("BEENDEN")
                for symbol in REPLACABLE:
                    time = time.replace(symbol, ":")
                time = time.split(":")
                hour = int(time[0])
                minute = int(time[1])
                if hour > 23 or hour < 0:
                    raise Exception("Die Stunden Zahl ist nicht Real")
                if minute > 59 or minute < 0:
                    raise Exception("Die Minuten Zahl ist nicht Real")
                if len(str(hour)) == 1:
                    time[0] = "0" + time[0]
                if len(str(minute)) == 1:
                    time[1] = "0" + time[1]
                delimiter = ":"
                time = delimiter.join(time)
            except:
                print("Ungültige Uhrzeit eingegeben.\nAchten Sie darauf eine reale Uhrzeit.\nGültige Satzzeichen sind : , . /\n")
            else:
                print(f"Deine Eingabe war {time} Uhr.")
                break     
        return time

if __name__ == "__main__":
    print("Triple T")