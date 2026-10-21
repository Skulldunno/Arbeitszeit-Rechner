REGULAR_ARRIVAL_TIME = "7:30"
REGULAR_LEAVE_TIME = "16:15"
REGULAR_FRIDAY_LEAVE_TIME =  "15:15"
REGULAR_BREAKFAST = ["09:00", "09:20"]
REGULAR_LUNCHTIME = ["12:30", "13:00"]
REGULAR_SMALL_BREAK_EARLY = ["11:00", "11:10"]
REGULAR_SMALL_BREAK_LATE = ["15:00", "15:10"]

class WorkTimeCaluclator:
    def __init__(self):
        self.breakfast = REGULAR_BREAKFAST
        self.lunchtime = REGULAR_LUNCHTIME
        self.small_break_early = REGULAR_SMALL_BREAK_EARLY
        self.small_break_late = REGULAR_SMALL_BREAK_LATE

    def get_break_duration(self, work_break):
        work_break_in_minute = []
        for time in work_break:
            work_break_in_minute.append(self.convert_to_minute(time))
        return work_break_in_minute[1] - work_break_in_minute[0]

    def calc_work_flextime(self, arrival_time, leave_time):
        arrival_flextime = self.convert_to_minute(REGULAR_ARRIVAL_TIME) - self.convert_to_minute((arrival_time))
        leave_flextime = self.convert_to_minute(REGULAR_LEAVE_TIME) - self.convert_to_minute(leave_time)
        return arrival_flextime - leave_flextime

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
        leftover_minutes = minutes - hours * 60
        time = [str(hours), str(leftover_minutes)]
        delimiter = ":"
        time = delimiter.join(time)
        if negativ:
            time = "-" + time
        return time

    def round_up_to_multiple_of_five(self, time):
        time = time.split(":")
        minutes = list(time[1])
        if int(minutes[-1]) == 0:
            pass
        elif int(minutes[-1]) < 5:
            minutes[-1] = "5"
        elif int(minutes[-1]) > 5:
            minutes[0] = str(int(minutes[0]) + 1)
            minutes[-1] = "0"
            print(type(minutes[0]))
            if int(minutes[0]) == 6:
                time[0] = str(int(time[0]) + 1)
                minutes[0] = "0"
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