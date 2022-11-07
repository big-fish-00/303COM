from tkinter import *
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
import sys
import account
import os

root = Tk()
root.resizable(False, False)

# point the page in center
# set the height and width for the page
height = 450
width = 550
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))

# disable window to close
root.overrideredirect(True)
root.config(background='#BBD0FF')
# let page to stay
root.wm_attributes('-topmost', True)

# Welcome Page
greeting_word = Label(text='Dnet Power Computer Center', bg='#BBD0FF', font=("Comic Sans MS", 15, 'italic'), fg='black')
# greeting_word.pack(side="top")
greeting_word.place(x=140 , y=80)

# background images
img = Image.open("images\logo.jpg")
photo = ImageTk.PhotoImage(img)
Label(root, image=photo, bg="#BBD0FF").place(anchor='center', relx=0.5, rely=0.5)

# Loading word
wait_word = Label(root, text="Loading...", font=("Comic Sans MS", 11, 'italic'), fg='black', bg='#BBD0FF')
wait_word.place(x=200, y=360)

# Loading Progression Bar
wait = Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
wait.place(x=85, y=390)

# exit button
exit_button = Button(text='x', bg='#BBD0FF', command=lambda: exit(), font=("Comic Sans MS", 15, 'italic'), bd=0,
                     activebackground='#BBD0FF', fg='white')
exit_button.place(x=510, y=0)


def exit():
    sys.exit(root.destroy())


def top():
    root.withdraw()
    os.system("account.py")
    root.destroy()


z = 0


def load():
    global z
    if z <= 6:
        txt = 'Loading...  ' + (str(15 * z) + '%')
        wait_word.config(text=txt)
        wait_word.after(500, load)
        wait['value'] = 15 * z
        z += 1
    else:
        top()


load()
root.mainloop()
