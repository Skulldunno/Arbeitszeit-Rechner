from zeitrechner import WorkTimeCaluclator
import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self):
        self.calc = WorkTimeCaluclator()
        self.root = tk.Tk()
        self.root.title("Arbeitszeitrechner")
        
    def start(self):
        self.title_label = tk.Label(self.root, text="Arbeitszeitrechner")
        self.title_label.pack()
        self.label1 = tk.Label(self.root, text="Uhr bis")
        self.label2 = tk.Label(self.root, text="Uhr")
        self.begin_entry = tk.Entry(self.root)
        self.begin_entry.insert(tk.END, "Ankunftsszeit")
        self.end_entry = tk.Entry(self.root)
        self.end_entry.insert(tk.END, "Endzeit")
        self.begin_entry.pack(side="left", padx=1)
        self.label1.pack(side="left")
        self.end_entry.pack(side="left", padx=1)
        self.label2.pack(side="left")
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.start()