from zeitrechner import WorkTimeCaluclator
import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self):
        self.calc = WorkTimeCaluclator()
        self.root = tk.Tk()
        self.root.title("Arbeitszeitrechner")
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="Rechner", command=lambda: self.show_frame("rechner"))
        self.menu.add_command(label="Options", command=lambda: self.show_frame("options"))
        self.menu.add_command(label="Übersicht", command=lambda: self.show_frame("übersicht"))
        self.frame1 = tk.Frame(master=self.root, bg="blue", height=10, width=10)
        self.frame2 = tk.Frame(master=self.root, bg="red", height=10, width=10)
        self.frame3 = tk.Frame(master=self.root, bg="black", height=10, width=10)
        self.frames = {
            "rechner": self.frame1, 
            "options": self.frame2, 
            "übersicht": self.frame3
            }
        self.currentframe = "rechner"

    def start(self):
        self.show_frame(self.currentframe)
        self.root.mainloop()

    def show_frame(self, frame_name):
        self.frames[self.currentframe].grid_forget()
        self.currentframe = frame_name
        self.frames[self.currentframe].grid(row=0, column=0)

if __name__ == "__main__":
    gui = GUI()
    gui.start()