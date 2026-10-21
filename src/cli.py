REPLACABLE = [":",",",".","/"]

class CLI:
    def __init__(self):
        pass

    def input_time(self):
        while True:
            try:
                time = input("Uhrzeit eingeben in HH:MM: ")
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
                print(f"Deine Eingabe war {time} Uhr.\n")
                break     
        return time

if __name__ == "__main__":
    test = CLI().input_time()