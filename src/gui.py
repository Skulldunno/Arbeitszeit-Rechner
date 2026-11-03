from zeitrechner import WorkTimeCaluclator
import tkinter as tk
from tkinter import ttk
import ctypes

class GUI:
    def __init__(self):
        self.calc = WorkTimeCaluclator()
        self.root = tk.Tk()
        self.root.title("Arbeitszeitrechner")
        self.root.resizable(False, False)
        make_corners_square(self.root)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="Rechner", command=lambda: self.show_frame("calc"))
        self.menu.add_command(label="Options", command=lambda: self.show_frame("options"))
        self.menu.add_command(label="Übersicht", command=lambda: self.show_frame("overview"))
        self.frame1 = CalcFrame(master=self.root, worktime_calculator=self.calc)
        self.frame2 = OptionFrame(master=self.root)
        self.frame3 = OverviewFrame(master=self.root)
        self.frames = {
            "calc": self.frame1, 
            "options": self.frame2, 
            "overview": self.frame3
            }
        self.currentframe = "calc"

    def start(self):
        self.show_frame(self.currentframe)
        self.root.mainloop()

    def show_frame(self, frame_name):
        self.frames[self.currentframe].grid_forget()
        self.currentframe = frame_name
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
        self.date = tk.Label(master=self, text="Datum (YYYY.MM.DD):").grid(row=0, column=0, stick="e")
        self.date_entry = tk.Entry(master=self).grid(row=0, column=1, stick="we")

        # Beginn Input
        self.begin = tk.Label(master=self, text="Anfang (HH:MM):").grid(row=1, column=0, stick="e")
        self.begin_entry = tk.Entry(master=self)
        self.begin_entry.grid(row=1, column=1, stick="we")

        # Beginn Input
        self.end = tk.Label(master=self, text="Ende (HH:MM):").grid(row=2, column=0, stick="e")
        self.end_entry = tk.Entry(master=self)
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
        if not begin == "" or not end == "":
            self.set_output_text(str(self.calc.calc_work_flextime(begin, end)))
        self.empty_input_error()

    def set_output_text(self, text:str):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(fg="black")
        self.output.insert("1.0", text)
        self.output.config(state="disabled")

    def empty_input_error(self):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(fg="red")
        self.output.insert("1.0","Ein oder mehrere Felder wurden nicht ausgefüllt!")
        self.output.config(state="disabled")

    def check_input_format(self, input):
        pass

class OptionFrame(tk.Frame):
    def __init__(self, master ,**options):
        super().__init__(master,**options)

        # 1.row
        self.begin_label = tk.Label(master=self, text="Pausenbeginn").grid(row=0, column=1, sticky="ew")
        self.end_label = tk.Label(master=self, text="Pausenende").grid(row=0, column=2, sticky="ew")

        # 2.row
        self.breakfast_label = tk.Label(master=self, text="Frühstück", anchor="e").grid(row=1, column=0, sticky="ew")
        self.breakfast_begin_entry = tk.Entry(master=self).grid(row=1, column=1, sticky="ew")
        self.breakfast_end_entry = tk.Entry(master=self).grid(row=1, column=2, sticky="ew")

        # 3.row
        self.lunch_label = tk.Label(master=self, text="Mittag", anchor="e").grid(row=2, column=0, sticky="ew")
        self.lunch_begin_entry = tk.Entry(master=self).grid(row=2, column=1, sticky="ew")
        self.lunch_end_entry = tk.Entry(master=self).grid(row=2, column=2, sticky="ew")

        # Button to reset options
        self.reset_button = tk.Button(master=self, text="Reset Default All", command=None).grid(row=3, column=0, sticky="w", pady=5, columnspan=2)
        # Button to save options
        self.save_button = tk.Button(master=self, text="Save", command=None).grid(row=3, column=2, sticky="e", pady=5)

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