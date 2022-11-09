import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os


class Account:
    def __init__(self, root):
        self.root = root

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        width = 1410
        height = 720
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2.5) - (height / 2.5)
        root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        root.resizable(0, 0)

        # WINDOW ICONS
        logo = Image.open('images\\logo.jpg')
        logo2 = ImageTk.PhotoImage(logo)
        root.iconphoto(True, logo2)
        root.title("Dnet Power Computer Center")

        root['bg'] = '#BBD0FF'

        def stock():
            root.destroy()
            filename = "inventory.py"
            os.system(filename)

        def supplier():
            root.destroy()
            filename = "Supplier.py"
            os.system(filename)

        def bill():
            root.destroy()
            filename = "AdminPurchase.py"
            os.system(filename)

        def bill_table():
            root.destroy()
            filename = 'PurchaseTable.py'
            os.system(filename)

        def forecast_product():
            root.destroy()
            filename = 'SalesForecast.py'
            os.system(filename)


        def logout():
            root.destroy()
            filename = 'account.py'
            os.system(filename)

        welLabel = Label(root, font=("Poppins SemiBold", 20, 'italic'), text='Welcome to Dnet Power',
                         background='#BBD0FF')
        welLabel.place(x=530, y=10)


        # NAME ICON
        stock_icon = Image.open('images\\stock.png')
        stock_resize = stock_icon.resize((150, 160))
        stock_photo = ImageTk.PhotoImage(stock_resize)
        stock_photo_icon = Label(root, image=stock_photo, bg='#BBD0FF')
        stock_photo_icon.image = stock_photo
        stock_photo_icon.place(x=150, y=220)

        stockButton = Button(root, font=("Poppins SemiBold", 12, 'italic'), text='Inventory',  background='white',
                             width=15, height=1, relief='flat', borderwidth=0, overrelief="flat", cursor='hand2',
                             foreground='black', activebackground='grey', command=stock)
        stockButton.place(x=155, y=430)

        supplier_icon = Image.open('images\\supplier.png')
        supplier_resize = supplier_icon.resize((150, 160))
        supplier_photo = ImageTk.PhotoImage(supplier_resize)
        supplier_photo_icon = Label(root, image=supplier_photo, bg='#BBD0FF')
        supplier_photo_icon.image = supplier_photo
        supplier_photo_icon.place(x=400, y=220)

        supplButton = Button(root, font=("Poppins SemiBold", 12, 'italic'), text='Supplier',  background='white',
                             width=15, height=1, relief='flat', borderwidth=0, overrelief="flat", cursor='hand2',
                             foreground='black', activebackground='grey', command=supplier)
        supplButton.place(x=405, y=430)

        bill_icon = Image.open('images\\bill.png')
        bill_resize = bill_icon.resize((150, 150))
        bill_photo = ImageTk.PhotoImage(bill_resize)
        bill_photo_icon = Label(root, image=bill_photo, bg='#BBD0FF')
        bill_photo_icon.image = bill_photo
        bill_photo_icon.place(x=650, y=225)

        billButton = Button(root, font=("Poppins SemiBold", 12, 'italic'), text='Purchase', background='white',
                             width=15, height=1, relief='flat', borderwidth=0, overrelief="flat", cursor='hand2',
                             foreground='black', activebackground='grey', command=bill)
        billButton.place(x=655, y=430)

        billtable_icon = Image.open('images\\table.png')
        billtable_resize = billtable_icon.resize((150, 150))
        billtable_photo = ImageTk.PhotoImage(billtable_resize)
        billtable_photo_icon = Label(root, image=billtable_photo, bg='#BBD0FF')
        billtable_photo_icon.image = billtable_photo
        billtable_photo_icon.place(x=890, y=225)

        billTableButton = Button(root, font=("Poppins SemiBold", 12, 'italic'), text='Purchase Table', background='white',
                             width=15, height=1, relief='flat', borderwidth=0, overrelief="flat", cursor='hand2',
                             foreground='black', activebackground='grey', command=bill_table)
        billTableButton.place(x=900, y=430)

        graph_icon = Image.open('images\\graph.png')
        graph_resize = graph_icon.resize((150, 150))
        graph_photo = ImageTk.PhotoImage(graph_resize)
        graph_photo_icon = Label(root, image=graph_photo, bg='#BBD0FF')
        graph_photo_icon.image = graph_photo
        graph_photo_icon.place(x=1150, y=225)

        forecastButton = Button(root, font=("Poppins SemiBold", 12, 'italic'), text='Forecast',
                                 background='white',
                                 width=15, height=1, relief='flat', borderwidth=0, overrelief="flat", cursor='hand2',
                                 foreground='black', activebackground='grey', command=forecast_product)
        forecastButton.place(x=1150, y=430)

        logoutBtn = Button(root, font=("Poppins SemiBold", 12, 'italic'), text='Logout', background='white',
                             width=15, height=1, relief='flat', borderwidth=0, overrelief="flat", cursor='hand2',
                             foreground='black', activebackground='grey', command=logout)
        logoutBtn.place(x=1240, y=660)



        # CLOSE WINDOW
        def exit():
            close = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=root)

            if close == True:
                root.destroy()
            else:
                pass

            # DESTROY WINDOW

        root.protocol("WM_DELETE_WINDOW", exit)


def page():
    window = Tk()
    Account(window)
    window.mainloop()


if __name__ == '__main__':
    page()

