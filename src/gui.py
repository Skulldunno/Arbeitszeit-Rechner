#from zeitrechner import WorkTimeCaluclator
import tkinter as tk
from tkinter import ttk
import ctypes

class GUI:
    def __init__(self):
        #self.calc = WorkTimeCaluclator()
        self.root = tk.Tk()
        self.root.title("Arbeitszeitrechner")
        self.root.resizable(False, False)
        make_corners_square(self.root)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="Rechner", command=lambda: self.show_frame("rechner"))
        self.menu.add_command(label="Options", command=lambda: self.show_frame("options"))
        self.menu.add_command(label="Übersicht", command=lambda: self.show_frame("übersicht"))
        self.frame1 = CalcFrame(master=self.root)
        self.frame2 = OptionFrame(master=self.root)
        self.frame3 = OverviewFrame(master=self.root, bg="black")
        self.frames = {
            "rechner": self.frame1, 
            "options": self.frame2, 
            "übersicht": self.frame3
            }
        self.currentframe = "options"

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
    def __init__(self, master ,**options):
        super().__init__(master,**options)

        # Date Input
        self.date = tk.Label(master=self, text="Datum (YYYY.MM.DD):")
        self.date.grid(row=0, column=0, stick="e")
        self.date_entry = tk.Entry(master=self)
        self.date_entry.grid(row=0, column=1, stick="we")

        # Beginn Input
        self.begin = tk.Label(master=self, text="Anfang (HH:MM):")
        self.begin.grid(row=1, column=0, stick="e")
        self.begin_entry = tk.Entry(master=self)
        self.begin_entry.grid(row=1, column=1, stick="we")

        # Beginn Input
        self.end = tk.Label(master=self, text="Ende (HH:MM):")
        self.end.grid(row=2, column=0, stick="e")
        self.end_entry = tk.Entry(master=self)
        self.end_entry.grid(row=2, column=1, stick="we")

        # Output Label
        self.output = tk.Text(master=self, height=3, width=40, wrap="word")
        self.output.grid(row=3, column=0, columnspan=2, pady=10)
        self.output.insert("1.0","Lorem ipsum")
        self.output.config(state="disabled")

        # Button to start Calculation
        self.calc_button = tk.Button(master=self, text="Ausrechnen", command=None)
        self.calc_button.grid(row=4, column=0, sticky="w")

        # Button to save results
        self.save_button = tk.Button(master=self, text="Save", command=None)
        self.save_button.grid(row=4, column=1, sticky="e")

class OptionFrame(tk.Frame):
    def __init__(self, master ,**options):
        super().__init__(master,**options)

        # 1.row
        self.begin_label = tk.Label(master=self, text="Pausenbeginn")
        self.begin_label.grid(row=0, column=1, sticky="ew")
        self.end_label = tk.Label(master=self, text="Pausenende")
        self.end_label.grid(row=0, column=2, sticky="ew")

        # 2.row
        self.breakfast_label = tk.Label(master=self, text="Frühstück", anchor="e")
        self.breakfast_label.grid(row=1, column=0, sticky="ew")
        self.breakfast_begin_entry = tk.Entry(master=self)
        self.breakfast_begin_entry.grid(row=1, column=1, sticky="ew")
        self.breakfast_end_entry = tk.Entry(master=self)
        self.breakfast_end_entry.grid(row=1, column=2, sticky="ew")

        # 3.row
        self.lunch_label = tk.Label(master=self, text="Mittag", anchor="e")
        self.lunch_label.grid(row=2, column=0, sticky="ew")
        self.lunch_begin_entry = tk.Entry(master=self)
        self.lunch_begin_entry.grid(row=2, column=1, sticky="ew")
        self.lunch_end_entry = tk.Entry(master=self)
        self.lunch_end_entry.grid(row=2, column=2, sticky="ew")

        # Button to reset options
        self.reset_button = tk.Button(master=self, text="Reset Default All", command=None)
        self.reset_button.grid(row=3, column=0, sticky="w", pady=5, columnspan=2)
        # Button to save options
        self.save_button = tk.Button(master=self, text="Save", command=None)
        self.save_button.grid(row=3, column=2, sticky="e", pady=5)

class OverviewFrame(tk.Frame):
    def __init__(self, master ,**options):
        super().__init__(master,**options)

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