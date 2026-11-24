import json
from zeitnachweis import Zeitnachweis
REGULAR_ARRIVAL_TIME = "7:30"
REGULAR_LEAVE_TIME = "16:15"
REGULAR_FRIDAY_LEAVE_TIME =  "15:15"
REGULAR_BREAKFAST = ["09:00", "09:15"]
REGULAR_LUNCHTIME = ["12:30", "13:00"]

class WorkTimeCaluclator:
    def __init__(self):
        self.zeitnachweis = Zeitnachweis()
        self.breakfast = self.load_options("breakfast")
        self.lunchtime = self.load_options("lunchtime")
        self.regular_working_hours = self.calc_working_hours(REGULAR_ARRIVAL_TIME, REGULAR_LEAVE_TIME, self.calc_break_time(self.breakfast, self.lunchtime))

    def load_options(self, pause):
        try:
            with open("options.json", "r", encoding="utf-8") as file:
                daten = json.load(file)
                try:
                    daten = daten[pause]
                except KeyError:
                    return self.load_default_option(pause)
            return daten
        except FileNotFoundError:
            return self.load_default_option(pause)
    
    def load_default_option(self, pause):
        if pause == "breakfast":
            daten = REGULAR_BREAKFAST
        elif pause == "lunchtime":
            daten = REGULAR_LUNCHTIME
        elif pause == "all":
            daten = {
                "breakfast": ["09:00","09:20"],
                "lunchtime": ["12:30","13:00"]
            }
        else:
            Exception("Kein Gültiger Parameter")
        return daten

    def reset_to_default_options(self):
        self.breakfast = REGULAR_BREAKFAST
        self.lunchtime = REGULAR_LUNCHTIME
        self.save_options()
        
    def save_options(self):
        daten = {
            "breakfast": self.breakfast,
            "lunchtime": self.lunchtime
        }
        with open("options.json", "w", encoding="utf-8") as file:
            json.dump(daten, file, indent=4)

    def calc_break_time(self, breakfast, lunchtime):
        breakfast_duration = self.get_break_duration(breakfast)
        lunchtime_duration = self.get_break_duration(lunchtime)
        return breakfast_duration + lunchtime_duration
    
    def calc_working_hours(self, arrival_time, leave_time, work_break):
        arrival_time_in_minute = self.convert_to_minute(arrival_time)
        leave_time_in_minute = self.convert_to_minute(leave_time)
        working_hours = leave_time_in_minute - arrival_time_in_minute - work_break
        return working_hours

    def get_break_duration(self, work_break):
        work_break_in_minute = []
        for time in work_break:
            work_break_in_minute.append(self.convert_to_minute(time))
        return work_break_in_minute[1] - work_break_in_minute[0]

    def calc_work_flextime(self, arrival_time, leave_time):
        flextime = self.calc_working_hours(arrival_time, leave_time, self.calc_break_time(self.breakfast, self.lunchtime)) - self.regular_working_hours
        return flextime

    def convert_to_minute(self, time):
        time = time.split(":")
        for x in range(len(time)):
            time[x] = int(time[x])
        time[0] = time[0] * 60
        minutes = int(time[0] + time[1])
        return minutes

    def convert_to_time(self, minutes):
        negativ = False
        if minutes < 0:
            minutes = -minutes
            negativ = True
        hours = minutes // 60
        if len(str(hours)) == 1:
            str_hours = "0"+str(hours)
        leftover_minutes = minutes - hours * 60
        if len(str(leftover_minutes)) == 1:
            str_leftover_minutes = "0"+str(leftover_minutes)
        time = [str_hours, str_leftover_minutes]
        delimiter = ":"
        time = delimiter.join(time)
        if negativ:
            time = "-" + time
        return time

    def round_up_to_multiple_of_five(self, time, arrive = True):
        time = time.split(":")
        minutes = list(time[1])
        if arrive:
            if int(minutes[-1]) == 0:
                pass
            elif int(minutes[-1]) < 5:
                minutes[-1] = "5"
            elif int(minutes[-1]) > 5:
                minutes[0] = str(int(minutes[0]) + 1)
                minutes[-1] = "0"
                if int(minutes[0]) == 6:
                    time[0] = str(int(time[0]) + 1)
                    minutes[0] = "0"
        else:
            if int(minutes[-1]) == 0:
                pass
            elif int(minutes[-1]) < 5:
                minutes[-1] = "0"
            elif int(minutes[-1]) > 5:
                minutes[-1] = "5"
        delimiter = ""
        minutes = delimiter.join(minutes)
        delimiter = ":"
        time = [time[0],minutes]
        time = delimiter.join(time)
        print(f"Notiert wurde {time}")
        return time

if __name__ == "__main__":
    print(WorkTimeCaluclator().calc_work_flextime("7:20", "16:15"))
    print(WorkTimeCaluclator().convert_to_time(150))
    print(WorkTimeCaluclator().get_break_duration(REGULAR_BREAKFAST))
    print(WorkTimeCaluclator().calc_working_hours(REGULAR_ARRIVAL_TIME, REGULAR_LEAVE_TIME, WorkTimeCaluclator().calc_break_time(REGULAR_BREAKFAST, REGULAR_LUNCHTIME)))