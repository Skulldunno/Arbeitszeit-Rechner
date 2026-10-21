REGULAR_ARRIVAL_TIME = "7:30"
REGULAR_LEAVE_TIME = "16:15"
REGULAR_FRIDAY_LEAVE_TIME =  "15:15"

class WorkTimeCaluclator:
    def __init__(self):
        pass

    def calc_work_flextime(self, arrival_time, leave_time):
        arrival_flextime = self.convert_to_minute(REGULAR_ARRIVAL_TIME) - self.convert_to_minute(arrival_time)
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
    
if __name__ == "__main__":
    print(WorkTimeCaluclator().calc_work_flextime("7:20", "16:15"))
    print(WorkTimeCaluclator().convert_to_time(150))