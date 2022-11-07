from tkinter import *
from PIL import ImageTk, Image, ImageDraw
from tkinter import messagebox
import random


class Manager:
    def __init__(self, root):
        self.root = root

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        width = 500
        height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2.5) - (height / 2.5)
        root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        root.resizable(0, 0)

        root['bg'] = '#BBD0FF'

        def exit():
            close = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=root)

            if close == True:
                root.destroy()
            else:
                pass

            # DESTROY WINDOW
        root.protocol("WM_DELETE_WINDOW", exit)


def page():
    root = Tk()
    Manager(root)
    root.mainloop()


if __name__ == "__main__":
    page()
