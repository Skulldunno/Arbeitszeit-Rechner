from calendar import monthrange
from zeitrechner import WorkTimeCaluclator
import tkinter as tk
from tkinter import ttk
import ctypes
from datetime import datetime

class GUI:
    def __init__(self):
        self.calc = WorkTimeCaluclator()
        self.root = tk.Tk()
        self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set()
              if not isinstance(event.widget, tk.Entry)
              else None)
        self.root.title("Arbeitszeitrechner")
        self.root.resizable(False, False)
        make_corners_square(self.root)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="Rechner", command=lambda: self.show_frame("calc"))
        self.menu.add_command(label="Options", command=lambda: self.show_frame("options"))
        self.menu.add_command(label="Übersicht", command=lambda: self.show_frame("overview"))
        self.menu.add_command(label="   ", command=lambda: self.show_frame("secret"))
        self.frame1 = CalcFrame(master=self.root, worktime_calculator=self.calc)
        self.frame2 = OptionFrame(master=self.root, calc=self.calc)
        self.frame3 = OverviewFrame(master=self.root)
        self.frame4 = SecretFrame(master=self.root)
        self.frames = {
            "calc": self.frame1, 
            "options": self.frame2, 
            "overview": self.frame3,
            "secret": self.frame4
            }
        self.currentframe = "calc"

    def start(self):
        self.show_frame(self.currentframe)
        self.root.mainloop()

    def show_frame(self, frame_name):
        self.frames[self.currentframe].grid_forget()
        self.currentframe = frame_name
        self.frames[self.currentframe].reset()
        self.frames[self.currentframe].grid(row=0, column=0, padx=5, pady=5)

        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        self.root.geometry(f"{width}x{height}")

class CalcFrame(tk.Frame):
    def __init__(self, master, worktime_calculator, **options):
        super().__init__(master,**options)
        self.calc = worktime_calculator
        self.master = master

        # Date Input
        self.date = tk.Label(master=self, text="Datum (jahr.monat.tag):").grid(row=0, column=0, stick="e")
        self.date_entry = DateEntry(master=self)
        self.date_entry.grid(row=0, column=1, stick="we")

        # Beginn Input
        self.begin = tk.Label(master=self, text="Anfang (HH:MM):").grid(row=1, column=0, stick="e")
        self.begin_entry = TimeEntry(master=self)
        self.begin_entry.grid(row=1, column=1, stick="we")

        # Beginn Input
        self.end = tk.Label(master=self, text="Ende (HH:MM):").grid(row=2, column=0, stick="e")
        self.end_entry = TimeEntry(master=self)
        self.end_entry.grid(row=2, column=1, stick="we")

        # Output Label
        self.output = tk.Text(master=self, height=3, width=40, wrap="word")
        self.output.insert("1.0","Lorem ipsum")
        self.output.config(state="disabled")
        self.output.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Button to start Calculation
        self.calc_button = tk.Button(master=self, text="Ausrechnen", command=self.calculate_working_hours).grid(row=4, column=0, sticky="w")

        # Button to save results
        self.save_button = tk.Button(master=self, text="Save", command=None).grid(row=4, column=1, sticky="e")

    def calculate_working_hours(self):
        begin = self.begin_entry.get().strip()
        end = self.end_entry.get().strip()
        date = self.date_entry.get().strip()
        if begin == "" or end == "" or date =="":
            self.empty_input_error()
            return
        try:
            begin = self.calc.round_up_to_multiple_of_five(begin)
            end = self.calc.round_up_to_multiple_of_five(end, False)
        except IndexError:
            self.empty_input_error()
            return
        if self.calc.convert_to_minute(begin) > self.calc.convert_to_minute(end):
            self.chronologic_input_error()
            return
        self.set_output_text(str(self.calc.calc_work_flextime(begin, end)), date, datetime.strptime(date, "%Y.%m.%d").strftime("%A"))

    def set_output_text(self, flextime:str, date:str, weekday):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(fg="black")
        self.output.insert("1.0", f"Deine Gleitzeit für den {date} {weekday} ist: {flextime} Minuten")
        self.output.config(state="disabled")

    def empty_input_error(self):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(fg="red")
        self.output.insert("1.0","Ein oder mehrere Felder sind unvollständig!")
        self.output.config(state="disabled")

    def chronologic_input_error(self):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(fg="red")
        self.output.insert("1.0","Die Abreisezeit kann nicht vor der Ankunftszeit sein!")
        self.output.config(state="disabled")

    def reset(self, *args):
        pass

class TimeEntry(tk.Entry):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        v_cmd = self.register(self.check_input_format)
        self.configure(validate="key", validatecommand=(v_cmd, "%P"))

        self.placeholder_active = False
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.show_placeholder)

    def show_placeholder(self, event=None, text="Leere Eingabe"):
        self.placeholder = text
        if self.get() == "":
            self.configure(validate="none", foreground="red")
            self.insert(0, self.placeholder)
            self.configure(validate="key")
            self.placeholder_active = True

    def remove_placeholder(self, event=None):
        if self.placeholder_active:
            self.configure(validate="none", foreground="black")
            self.delete(0, tk.END)
            self.configure(validate="key")
            self.placeholder_active = False

    def check_input_format(self, input):
        allowed_characters = "0123456789:"
        special_characters = ":"

        if input =="":  #allow emptying entry
            return True

        if not all(char in allowed_characters for char in input):   #allow new string when all characters are allowed
            return False

        if input[0] in special_characters:  #first character of the new string can not be a special character
            return False
         
        special_chars_in_input = [char for char in input if char in special_characters] #note every special character in the new string

        if len(special_chars_in_input) > 1: # do not allow the new string if there is more than 1 special character
            return False
        elif len(special_chars_in_input) == 1: # if there is exactly one special character
            split_char = special_chars_in_input[0]

            time = input.split(split_char) #split the new string at the special character
            hours = time[0]
            minutes = time[1]

            if len(hours) > 2 or len(minutes) > 2: #if either hour or minutes string is too long do not allow the new string
                return False

            if int(hours) > 23: # hours can not be above 23 decline the new string
                return False

            if len(minutes) > 0: #if there is a minute written
                if int(minutes) > 59: # minutes can not be above 59 decline the new string
                    return False
            
        elif len(input) > 0: # if there is text in the input of the new string
            if int(input) > 23: #check if the hours are not above 23; hours are the first thing to be input
                return False
            if len(input) > 2: #if hours are longer than 2 characters decline the new string
                return False

        return True #when all checks are passed allow the new string

    def insert_unvalidated(self, text:str):
        self.configure(validate="none")
        self.insert(0, text)
        self.configure(validate="key")

class DateEntry(tk.Entry):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        v_cmd = self.register(self.check_input_format)
        self.configure(validate="key", validatecommand=(v_cmd, "%P"))

    def check_input_format(self, input):
        allowed_characters = "0123456789."
        special_characters = "."

        if input =="":  #allow emptying entry
            return True
        
        if not all(char in allowed_characters for char in input):   #only allowed characters can be entered
            return False

        if input[0] in special_characters:  #first character can not be a special character
            return False

        special_chars_in_input = {index:char for index, char in enumerate(input) if char in special_characters} #note every special character in the new string and its position in the new string

        if len(special_chars_in_input) > 2: #if there are more than 2 special character decline the new string
            return False

        elif len(special_chars_in_input) == 1:  #if there is one special character split the new string at the special character
            split_char = list(special_chars_in_input.values())[0]

            date = input.split(split_char, 1)
            year = date[0]
            month = date[1]

            if len(year) > 4 or len(month) > 2: #if the year is over 4 characters long or the month over 2 characters long decline the new string
                return False

            if len(month) > 0:  #if there is an input for month
                if int(month) > 12 or int(month) < 1:   #check whether or not the month is a real month
                    return False

        elif len(special_chars_in_input) == 2:  #if there are two special character first check whether or not they are next to each other
            position_of_chars = list(special_chars_in_input.keys())
            if position_of_chars[0] +1 == position_of_chars[1]:
                return False

            split_char = list(special_chars_in_input.values())[0] #split the new string into first into two
            date = input.split(split_char, 1)
            year = date[0]
            rest = date[1]
            split_char = list(special_chars_in_input.values())[1] #split the rest into two more
            rest = rest.split(split_char, 1)
            month = rest[0]
            day = rest[1]

            if len(year) > 4 or len(month) > 2 or len(day) > 2: #if the year is over 4 characters long or the month over 2 characters long or the day over 2 characters long decline the new string
                return False

            if len(month) > 0:  #if there is an input for month
                if int(month) > 12 or int(month) < 1:   #check whether or not the month is a real month
                    return False

            if len(day) > 0:
                if int(day) > monthrange(int(year), int(month))[1] or int(day) < 1:
                    return False

        elif len(input) > 4:
            return False
            
        return True #when all checks are passed allow the new string
    
class OptionFrame(tk.Frame):
    def __init__(self, master, calc ,**options):
        super().__init__(master,**options)
        self.calc = calc

        # 1.row
        self.begin_label = tk.Label(master=self, text="Pausenbeginn").grid(row=0, column=1, sticky="ew")
        self.end_label = tk.Label(master=self, text="Pausenende").grid(row=0, column=2, sticky="ew")

        # 2.row
        self.breakfast_label = tk.Label(master=self, text="Frühstück", anchor="e").grid(row=1, column=0, sticky="ew")
        self.breakfast_begin_entry = TimeEntry(master=self)
        self.breakfast_begin_entry.grid(row=1, column=1, sticky="ew")
        self.breakfast_end_entry = TimeEntry(master=self)
        self.breakfast_end_entry.grid(row=1, column=2, sticky="ew")

        # 3.row
        self.lunch_label = tk.Label(master=self, text="Mittag", anchor="e").grid(row=2, column=0, sticky="ew")
        self.lunch_begin_entry = TimeEntry(master=self)
        self.lunch_begin_entry.grid(row=2, column=1, sticky="ew")
        self.lunch_end_entry = TimeEntry(master=self)
        self.lunch_end_entry.grid(row=2, column=2, sticky="ew")

        # Button to reset options
        self.reset_button = tk.Button(master=self, text="Reset Default All", command=None).grid(row=3, column=0, sticky="w", pady=5, columnspan=2)
        # Button to save options
        self.save_button = tk.Button(master=self, text="Save", command=self.save_options).grid(row=3, column=2, sticky="e", pady=5)

    def reset(self):
        times = [
            self.calc.breakfast[0],
            self.calc.breakfast[1],
            self.calc.lunchtime[0],
            self.calc.lunchtime[1]
            ]
        i = 0
        for widget in self.winfo_children():
            if isinstance(widget, TimeEntry):
                widget.remove_placeholder()
                widget.delete(0, tk.END)
                widget.insert(0, times[i])
                i+=1

    def save_options(self):
        entries = []
        even = True
        for widget in self.winfo_children():
            if isinstance(widget, TimeEntry):
                entries.append(widget)
        for widget in entries:
            if widget.get().strip() == "":
                self.empty_input_error(widget)
                return
            self.check_for_empty_input_error(widget, even)
            if even:
                even = False
            else:
                even = True
        
        for start, end in zip(entries, entries[1:]):
            try:
                start_time = self.calc.convert_to_minute(start.get())
            except ValueError:
                self.empty_input_error(start, text=start.get())
                continue
            try:
                end_time = self.calc.convert_to_minute(end.get())
            except ValueError:
                self.empty_input_error(end, text=end.get())
                continue
            if start_time > end_time:
                self.chronologic_input_error(start)
            
    def check_for_empty_input_error(self, entry, even):
        try:
            output = self.calc.round_up_to_multiple_of_five(entry.get().strip(), even)
            entry.delete(0, tk.END)
            entry.insert_unvalidated(output)
        except IndexError:
            self.empty_input_error(entry, text=entry.get())

    def chronologic_input_error(self, entry):
        entry.delete(0, tk.END)  
        entry.show_placeholder(text="Unmögliche Pause")

    def empty_input_error(self, entry, text):
        entry.delete(0, tk.END)
        entry.show_placeholder(text=text)
    
class OverviewFrame(tk.Frame):
    def __init__(self, master ,**options):
        super().__init__(master,**options)

        # Widgets to change week 
        self.week_frame = tk.Frame(master=self)
        self.week_before_button = tk.Button(master=self.week_frame, text="<-", anchor="e", command=None).grid(row=0, column=0, sticky="e")
        self.week_label = tk.Label(master=self.week_frame, text=f"Kalenderwoche: Placeholder", relief="raised").grid(row=0, column=1, sticky="nsew")
        self.week_after_button = tk.Button(master=self.week_frame, text="->", anchor="w", command=None).grid(row=0, column=2, sticky="w")
        self.week_frame.grid(row=0, column=0, columnspan=5)
        # Widgets to change year
        self.year_frame = tk.Frame(master=self)
        self.year_before_button = tk.Button(master=self.year_frame, text="<-", anchor="e", command=None).grid(row=0, column=0, sticky="e")
        self.year_label = tk.Label(master=self.year_frame, text=f"Jahr: Placeholder", relief="raised").grid(row=0, column=1, sticky="nsew")
        self.year_after_button = tk.Button(master=self.year_frame, text="->", anchor="w", command=None).grid(row=0, column=2, sticky="w")
        self.year_frame.grid(row=0, column=5, columnspan= 2)
        
        categories = ["Beginn", "Frühstück", "Mittag", "Ende", "Gleitzeit", "Kumulativ", "Datum"]
        self.categories_label = {
            category: tk.Label(master=self, text=category, bd=1, relief="solid").grid(row=1, column=index, sticky="nsew") for index, category in enumerate(categories) 
        }
        days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        for index, day in enumerate(days):
            self.day_row = {
                f"{day}_begin" : tk.Label(master=self, text=f"HH:MM", bd=1, relief="solid").grid(row=index +2, column=0, sticky="nsew"),
                f"{day}_breakfast" : tk.Label(master=self, text=f"HH:MM\n-\nHH:MM", bd=1, relief="solid").grid(row=index +2, column=1, sticky="nsew"), 
                f"{day}_lunch" : tk.Label(master=self, text=f"HH:MM\n-\nHH:MM", bd=1, relief="solid").grid(row=index +2, column=2, sticky="nsew"), 
                f"{day}_end" : tk.Label(master=self, text=f"HH:MM", bd=1, relief="solid").grid(row=index +2, column=3, sticky="nsew"), 
                f"{day}_flextime" : tk.Label(master=self, text=f"0", bd=1, relief="solid").grid(row=index +2, column=4, sticky="nsew"), 
                f"{day}_accumulated" : tk.Label(master=self, text=f"0", bd=1, relief="solid").grid(row=index +2, column=5, sticky="nsew"), 
                day : tk.Label(master=self, text=day, bd=1, relief="solid").grid(row=index +2, column=6, sticky="nsew")
            }
    def reset(self, *args):
        pass

class SecretFrame(tk.Frame):
    def __init__(self, master ,**options):
        super().__init__(master,**options)

        self.canvas = tk.Canvas(master=self, bg="blue", height=300, width=300 )
        self.canvas.grid(column=0, row=0)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        
    def start_drawing(self, event):
        self.canvas.old_x = event.x
        self.canvas.old_y = event.y

    def draw(self, event):
        self.canvas.create_line(
            self.canvas.old_x,
            self.canvas.old_y,
            event.x,
            event.y,
            width=3,
            fill="black",
            capstyle=tk.ROUND,
            smooth=True
        )

        self.canvas.old_x = event.x
        self.canvas.old_y = event.y

    def reset(self):
        self.canvas.delete("all")
        
# erstellt von mister GPT um die ecken eckig zu machen
def make_corners_square(root):
    # Aktualisiert ausstehende Tkinter-Aufgaben, damit unter anderem
    # die Fenstergeometrie und die Fenster-ID bereitstehen.
    root.update_idletasks()

    # HWND = Handle to a Window
    # Eine HWND ist eine eindeutige Kennung, über die Windows
    # ein bestimmtes Fenster identifiziert.
    #
    # winfo_id() liefert die Fenster-ID des Tkinter-Fensters.
    # GetParent() ermittelt das übergeordnete Fenster-Handle.
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

    # DWMWA = Desktop Window Manager Window Attribute
    # Die Zahl 33 bezeichnet die Windows-Eigenschaft,
    # mit der die Form der Fensterecken festgelegt werden kann.
    DWMWA_WINDOW_CORNER_PREFERENCE = 33

    # DWMWCP = Desktop Window Manager Window Corner Preference
    # DONOTROUND = Die Ecken sollen nicht abgerundet werden.
    # Der Wert 1 steht für eckige Fensterecken.
    DWMWCP_DONOTROUND = 1

    # Erstellt einen C-kompatiblen Integer.
    # ctypes ermöglicht damit die Übergabe des Wertes
    # an eine Windows-Funktion.
    preference = ctypes.c_int(DWMWCP_DONOTROUND)

    # DWM = Desktop Window Manager
    # DwmSetWindowAttribute() übermittelt eine Einstellung
    # an Windows, die das Aussehen des Fensters beeinflusst.
    #
    # Parameter:
    # 1. hwnd: Fenster, dessen Darstellung geändert werden soll
    # 2. 33: Eigenschaft für die Fensterecken
    # 3. byref(preference): Adresse des gewünschten Wertes
    # 4. sizeof(preference): Größe des übergebenen Wertes in Bytes
    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        hwnd,
        DWMWA_WINDOW_CORNER_PREFERENCE,
        ctypes.byref(preference),
        ctypes.sizeof(preference)
    )
if __name__ == "__main__":
    gui = GUI()
    gui.start()