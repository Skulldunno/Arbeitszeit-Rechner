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
            print("4. Beenden")
            choice = input("Bitte wähle eine Option (1-4): ")
            if choice == "1":
                self.working_hours_input()
            elif choice == "2":
                self.breakfast_option()
            elif choice == "3":
                self.lunchtime_option()
            elif choice == "4":
                print("Programm wird beendet.")
                break
            else:
                print("Ungültige Eingabe. Bitte wähle eine Option von 1 bis 4.")
    
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