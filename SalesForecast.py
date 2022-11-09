from tkinter import *
import os
import csv
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from prophet.plot import add_changepoints_to_plot



class SalesForecast:
    def __init__(self, sales_forecast_page):
        self.sales_forecast_page = sales_forecast_page

        sales_forecast_page.rowconfigure(0, weight=0)
        sales_forecast_page.columnconfigure(0, weight=0)
        width = 600
        height = 750
        screen_width = sales_forecast_page.winfo_screenwidth()
        screen_height = sales_forecast_page.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 3.5) - (height / 3.5)
        sales_forecast_page.geometry("%dx%d+%d+%d" % (width, height, x, y))

        sales_forecast_page.title('Forecast')

        sales_forecast_page['bg'] = '#BBD0FF'

        def default_page():
            sales_forecast_page.destroy()
            filename = 'AdminHome.py.py'
            os.system(filename)

        def inventory():
            sales_forecast_page.destroy()
            filename = 'AdminInventory.py'
            os.system(filename)

        def supplier():
            sales_forecast_page.destroy()
            filename = 'AdminSupplier.py'
            os.system(filename)

        def purchase():
            sales_forecast_page.destroy()
            filename = 'AdminPurchase.py'
            os.system(filename)

        def bill_table():
            sales_forecast_page.destroy()
            filename = 'PurchaseTable.py'
            os.system(filename)

        def forecast_product():
            sales_forecast_page.destroy()
            filename = 'SalesForecast.py'
            os.system(filename)

        def logout():
            sales_forecast_page.destroy()
            filename = 'account.py'
            os.system(filename)

        def control():

            menuFrame = Frame(sales_forecast_page, width=300, height=750, bg='#D4E1F1', border=1)
            menuFrame.place(x=0, y=0)

            def button(x, y, text, click):
                def when_enter(e):
                    widgetButton['background'] = '#D4E1F1'
                    widgetButton['foreground'] = 'black'

                def when_leave(e):
                    widgetButton['background'] = '#D4E1F1'
                    widgetButton['foreground'] = 'black'

                widgetButton = Button(menuFrame, text=text,
                                      width=44,
                                      height=2,
                                      bg='#D4E1F1',
                                      fg='black',
                                      border=0,
                                      activebackground='black',
                                      activeforeground='white',
                                      command=click)

                widgetButton.bind("<Enter>", when_enter)
                widgetButton.bind("<Leave>", when_leave)

                widgetButton.place(x=x, y=y)

            button(0, 80, 'H O M E', default_page)
            button(0, 120, 'I N V E N T O R Y', inventory)
            button(0, 160, 'S U P P L I E R', supplier)
            button(0, 200, 'P U R C H A S E', purchase)
            button(0, 240, 'P A Y M E N T', bill_table)
            button(0, 280, 'F O R E C A S T', forecast_product)
            button(0, 680, 'L O G O U T', logout)

            def close():
                menuFrame.destroy()

            # CLOSE MENU BAR IMG
            menu_close_img = Image.open('images\\close.png')
            menu_close_img_resize = menu_close_img.resize((25, 25))
            menu_close_photo = ImageTk.PhotoImage(menu_close_img_resize)
            menu_close_photo_place = Label(menuFrame, image=menu_close_photo, bg='#D4E1F1')
            menu_close_photo_place.image = menu_close_photo

            # CLOSE MENU BAR
            closeButton = Button(menuFrame, image=menu_close_photo, bg='#D4E1F1', activebackground='#D4E1F1',
                                 command=close, border=0)
            closeButton.place(x=260, y=10)

        # HOME PAGE MENU BAR
        header_line = Canvas(sales_forecast_page, width=1420, height=1, bg="black", highlightthickness=0)
        header_line.place(x=0, y=60)

        # OPEN MENU BAR IMG
        menu_img = Image.open('images\\menu.png')
        menu_img_resize = menu_img.resize((25, 25))
        menu_photo = ImageTk.PhotoImage(menu_img_resize)
        menu_photo_place = Label(sales_forecast_page, image=menu_photo, bg='#BBD0FF')
        menu_photo_place.image = menu_photo

        # OPEN MENU BAR BUTTON
        menuBtn = Button(sales_forecast_page, image=menu_photo, bg='#BBD0FF', activebackground='#BBD0FF', width=40,
                         height=40,
                         border=0, command=control)
        menuBtn.place(x=0, y=9)

        text_font = ("Poppins SemiBold", "11")

        conn = sqlite3.connect("./database/DnetPower.db")
        cur = conn.cursor()

        find_stock = "SELECT stock_name FROM stock"
        cur.execute(find_stock)
        result1 = cur.fetchall()
        stock = []
        for i in range(len(result1)):
            if (result1[i][0] not in stock):
                stock.append(result1[i][0])

        def printPDF():
            if productName_combo.get() == "":
                messagebox.showerror("Error", "Please select a product")
            else:
                conn = sqlite3.connect('./database/DnetPower.db')
                cursor = conn.cursor()
                some = "SELECT purchase_product_name, purchase_brand, purchase_quantity, purchase_time, purchase_billnm, purchase_cashier_name," \
                       "purchase_status FROM Purchase WHERE purchase_product_name = ?"
                cursor.execute(some, [productName_combo.get()])
                with open("purchase.csv", 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([i[0] for i in cursor.description])
                    csv_writer.writerows(cursor)
                conn.close()
                messagebox.showinfo('Success', "CSV File already generate.\n You can view the forecast")

        def forecast():
            sales_forecast_page.destroy()
            filename = 'TimeForecast.py'
            os.system(filename)


        foreLabel = Label(sales_forecast_page, text="Forecast",
                             font=("Poppins SemiBold", 13, 'italic'),
                             background='#BBD0FF')
        foreLabel.place(x=250, y=120)

        notification = Label(sales_forecast_page, text="Kindly reminder, select a product before generate csv file."
                                                       "\n System will be using the csv file to view forecast.",
                             font=("Poppins SemiBold", 11, 'italic'),
                             background='#BBD0FF')
        notification.place(x=120, y=180)

        productName = Label(sales_forecast_page, text="Product Name", font=("Poppins SemiBold", 11, 'italic'),
                            background='#BBD0FF')
        productName.place(x=65, y=260)

        productName_combo = ttk.Combobox(sales_forecast_page, font=("Poppins SemiBold", 11, 'italic'), width=48,
                                         state="readonly", values=stock)
        productName_combo.option_add("*TCombobox*Listbox.font", text_font)
        productName_combo.option_add("*TCombobox*Listbox.selectBackground", "lightblue")
        productName_combo.place(x=65, y=295)

        generateCSV = Button(sales_forecast_page, text="Generate CSV File", font=("Poppins SemiBold", 10, 'italic'),
                             bg='white', fg='black', activebackground='#BBD0FF', width=15, border=0, cursor='hand2',
                             justify=CENTER, command=printPDF)
        generateCSV.place(x=225, y=350)

        dateLine = Label(sales_forecast_page, text="View forecast for one year", font=("Poppins SemiBold", 11, 'italic'),
                         background='#BBD0FF')
        dateLine.place(x=195, y=410)

        forecast = Button(sales_forecast_page, text="View Forecast Result", font=("Poppins SemiBold", 10, 'italic'),
                          bg='white', fg='black', activebackground='#BBD0FF', width=18, border=0, cursor='hand2',
                          justify=CENTER, command=forecast)
        forecast.place(x=215, y=450)

        def leave():
            close = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=sales_forecast_page)
            if close == True:
                sales_forecast_page.destroy()

            else:
                pass

        sales_forecast_page.protocol("WM_DELETE_WINDOW", leave)


def page():
    window = Tk()
    SalesForecast(window)
    window.mainloop()


if __name__ == "__main__":
    page()
