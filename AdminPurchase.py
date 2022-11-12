import tempfile
from tkinter import *
import os
import string
from tkinter import scrolledtext as tst
from PIL import ImageTk, Image
from time import strftime
from tkcalendar import DateEntry
from datetime import date
from tkinter import ttk
from tkinter import messagebox
import random
import googleEmail
from tkinter import filedialog
import re
import sqlite3


class StockItem:
    def __init__(self, name, price, quantity):
        self.product_name = name
        self.price = price
        self.qty = quantity


class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        if len(self.items) == 0:
            return True

class AdminPurchase:
    def __init__(self, purchase_page):
        self.purchase_page = purchase_page

        purchase_page.rowconfigure(0, weight=0)
        purchase_page.columnconfigure(0, weight=0)
        width = 1410
        height = 720
        screen_width = purchase_page.winfo_screenwidth()
        screen_height = purchase_page.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 3.5) - (height / 3.5)
        purchase_page.geometry("%dx%d+%d+%d" % (width, height, x, y))
        purchase_page.resizable(0, 0)

        purchase_page.title('Invoice')

        purchase_page['bg'] = '#BBD0FF'

        cash_name = StringVar()
        company_num = StringVar()
        bill_num = StringVar()
        bill_date = StringVar()

        def default_page():
            purchase_page.destroy()
            filename = 'AdminHome.py'
            os.system(filename)

        def inventory():
            purchase_page.destroy()
            filename = 'AdminInventory.py'
            os.system(filename)

        def supplier():
            purchase_page.destroy()
            filename = 'AdminSupplier.py'
            os.system(filename)

        def purchase():
            purchase_page.destroy()
            filename = 'AdminPurchase.py'
            os.system(filename)

        def bill_table():
            purchase_page.destroy()
            filename = 'PurchaseTable.py'
            os.system(filename)

        def forecast_product():
            purchase_page.destroy()
            filename = 'SalesForecast.py'
            os.system(filename)

        def logout():
            purchase_page.destroy()
            filename = 'account.py'
            os.system(filename)

        def control():

            menuFrame = Frame(purchase_page, width=300, height=750, bg='#D4E1F1', border=1)
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
            button(0, 200, 'I N V O I C E', purchase)
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
        header_line = Canvas(purchase_page, width=1420, height=1, bg="black", highlightthickness=0)
        header_line.place(x=0, y=60)

        # OPEN MENU BAR IMG
        menu_img = Image.open('images\\menu.png')
        menu_img_resize = menu_img.resize((25, 25))
        menu_photo = ImageTk.PhotoImage(menu_img_resize)
        menu_photo_place = Label(purchase_page, image=menu_photo, bg='#BBD0FF')
        menu_photo_place.image = menu_photo

        # OPEN MENU BAR BUTTON
        menuBtn = Button(purchase_page, image=menu_photo, bg='#BBD0FF', activebackground='#BBD0FF', width=40, height=40,
                         border=0, command=control)
        menuBtn.place(x=0, y=9)

        def time():
            string = strftime("%A, %H:%M:%S %p")
            timeLabel.config(text=string)
            timeLabel.after(1000, time)

        timeLabel = Label(purchase_page, text="", font=("Poppins SemiBold", 12, 'italic'), background='#BBD0FF')
        timeLabel.place(x=1205, y=20)
        time()

        payFrame = LabelFrame(purchase_page, text='Purchase Info', font=("Poppins SemiBold", 15, 'italic'),
                              bg='#BBD0FF', bd='1.5', width=450, height=630)
        payFrame.place(x=55, y=80)

        cashier_name = Label(purchase_page, text="Cashier Full Name", font=("Poppins SemiBold", 11, 'italic'),
                             background='#BBD0FF')
        cashier_name.place(x=65, y=110)

        cashier_entry = ttk.Entry(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=50,
                                  textvariable=cash_name)
        cashier_entry.place(x=65, y=135)

        company_contact = Label(purchase_page, text="Company Contact Number", font=("Poppins SemiBold", 11, 'italic'),
                                background='#BBD0FF')
        company_contact.place(x=65, y=160)

        company_entry = ttk.Entry(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=50,
                                  textvariable=company_num)
        comNum = str("0124324533")
        company_entry.insert(0, comNum)
        company_entry.place(x=65, y=185)

        conn = sqlite3.connect("./database/DnetPower.db")
        cur = conn.cursor()

        find_stock = "SELECT stock_name FROM stock"
        cur.execute(find_stock)
        result1 = cur.fetchall()
        stock = []
        for i in range(len(result1)):
            if (result1[i][0] not in stock):
                stock.append(result1[i][0])

        text_font = ("Poppins SemiBold", "11")

        def get_group(e):
            productGroup_combo.configure(state='readonly')
            productGroup_combo.set('')
            productBrand_combo.set('')
            conn2 = sqlite3.connect("./database/DnetPower.db")
            cur2 = conn2.cursor()
            find_cate = "SELECT stock_group FROM stock WHERE stock_name = ?"
            cur2.execute(find_cate, [productName_combo.get()])
            result2 = cur2.fetchall()
            group = []
            for j in range(len(result2)):
                if (result2[j][0] not in group):
                    group.append(result2[j][0])

            productGroup_combo.configure(values=group)
            productGroup_combo.bind("<<ComboboxSelected>>", get_brand)
            productBrand_combo.configure(state='disable')

        def get_brand(e):
            productBrand_combo.configure(state='readonly')
            productBrand_combo.set('')
            conn3 = sqlite3.connect("./database/DnetPower.db")
            cur3 = conn3.cursor()
            find_brand = "SELECT stock_brand FROM stock WHERE stock_name = ? and stock_group = ?"
            cur3.execute(find_brand, [productName_combo.get(), productGroup_combo.get()])
            result3 = cur3.fetchall()
            brand = []
            for k in range(len(result3)):
                brand.append(result3[k][0])

            productBrand_combo.configure(values=brand)
            productBrand_combo.bind("<<ComboboxSelected>>", show_quantity)
            productQty_entry.configure(state='disable')

        def show_quantity(e):
            global quantity_label

            productQty_entry.configure(state="normal")
            quantity_label = Label(purchase_page, font=("Poppins SemiBold", 11, 'italic'),
                                   background='#BBD0FF', width=15, anchor='w')
            quantity_label.place(x=65, y=410)

            product_name = productName_combo.get()
            conn4 = sqlite3.connect("./database/DnetPower.db")
            cur4 = conn4.cursor()
            find_qty = "SELECT stock_quantity FROM stock WHERE stock_name = ?"
            cur4.execute(find_qty, [product_name])
            result4 = cur4.fetchone()
            quantity_label.configure(text="In Stock : {}".format(result4[0]))
            quantity_label.configure(foreground='black')

        cart = Cart()

        def random_bill_number(stringLength):
            lettersAndDigits = string.ascii_letters.upper() + string.digits
            count = ''.join(random.choice(lettersAndDigits) for i in range(stringLength - 2))
            return ('DN' + count)

        def valid_phone(phone):
            if re.match(r"[789]\d{9}$", phone):
                return True
            return True

        def add_cart():
            Scrolledtext.configure(state='normal')
            count = Scrolledtext.get('1.0', END)
            if count.find('Total') == -1:
                product_name = productName_combo.get()
                if product_name != "":
                    product_quantity = productQty_entry.get()
                    find_mrp = "SELECT stock_price, stock_quantity FROM stock WHERE stock_name = ?"
                    cur.execute(find_mrp, [product_name])
                    results = cur.fetchall()
                    stocks = results[0][1]
                    mrp = results[0][0]
                    if product_quantity.isdigit() == True:
                        if (stocks - int(product_quantity)) >= 0:
                            sp = mrp * int(product_quantity)
                            item = StockItem(product_name, mrp, int(product_quantity))
                            cart.add_item(item)
                            Scrolledtext.configure(state="normal")
                            bill_text = "\n\t      {}\t\t\t    {}\t\t   {}\n".format(product_name, product_quantity, sp)
                            Scrolledtext.insert("insert", bill_text)
                            Scrolledtext.configure(state='disable')

                        else:
                            productQty_entry.configure(state='disable')
                            messagebox.showerror("Error", 'Out of stock. Please check the quantity',
                                                 parent=purchase_page)
                    else:
                        messagebox.showerror("Error", 'Invalid Quantity', parent=purchase_page)
                else:
                    messagebox.showerror("Error", "Choose a product", parent=purchase_page)
            else:
                Scrolledtext.delete('1.0', END)
                new_line = []
                li = count.split('\n')
                for z in range(len(li)):
                    if len(li[z]) != 0:
                        if li[z].find("Total") == -1:
                            new_line.append(li[z])

                        else:
                            break
                for w in range(len(new_line) - 1):
                    Scrolledtext.insert('insert', new_line[w])
                    Scrolledtext.insert('insert', '\n')

                product_name = productName_combo.get()
                if product_name != "":
                    product_quantity = productQty_entry.get()
                    find_mrp = "SELECT stock_price, stock_quantity, stock_id FROM stock WHERE stock_name = ?"
                    cur.execute(find_mrp, [product_name])
                    results = cur.fetchall()
                    stocks = results[0][1]
                    mrp = results[0][0]

                    if product_quantity.isdigit():
                        if (stocks - int(product_quantity)) >= 0:
                            sp = results[0][0] * int(product_quantity)
                            item = StockItem(product_name, mrp, int(product_quantity))
                            cart.add_item(item)
                            Scrolledtext.configure(state='normal')
                            bill_text = "{}\t\t\t\t{}\t\t\t   {}\n".format(product_name, product_quantity, sp)
                            Scrolledtext.insert('insert', bill_text)
                            Scrolledtext.configure(state="disabled")
                        else:
                            messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=purchase_page)
                    else:
                        messagebox.showerror("Oops!", "Invalid quantity.", parent=purchase_page)
                else:
                    messagebox.showerror("Oops!", "Choose a product.", parent=purchase_page)

        def remove_cart():
            if (cart.isEmpty() != False):
                Scrolledtext.configure(state="normal")
                count = Scrolledtext.get('1.0', END)
                if count.find('Total') == -1:
                    # Return -1 if sub is not found.
                    try:
                        cart.remove_item()
                    except IndexError:
                        messagebox.showwarning("Warning", "Cart is empty.", parent=purchase_page)

                    else:
                        Scrolledtext.configure(state="normal")
                        get_all_bill = (Scrolledtext.get('1.0', END).split("\n"))
                        all_string = get_all_bill[:len(get_all_bill) - 4]
                        Scrolledtext.delete('1.0', END)
                        for z in range(len(all_string)):
                            Scrolledtext.insert('insert', all_string[z])
                            Scrolledtext.insert('insert', '\n')

                        Scrolledtext.configure(state="disabled")
                else:
                    try:
                        cart.remove_item()

                    except IndexError:
                        messagebox.showwarning("Warning", "Cart is empty.", parent=purchase_page)

                    else:
                        Scrolledtext.delete('1.0', END)
                        new_line = []
                        line = count.split('\n')
                        for i in range(len(line)):
                            if len(line[i]) != 0:
                                if line[i].find('Total') == -1:
                                    new_line.append(line[i])

                                else:
                                    break

                        new_line.pop()
                        for w in range(len(new_line) - 1):
                            Scrolledtext.insert('insert', new_line[w])
                            Scrolledtext.insert('insert', '\n')
                        Scrolledtext.configure(state='disable')

            else:
                messagebox.showerror("Error", "Add a product.", parent=purchase_page)

        def total_bill():
            if cart.isEmpty():
                messagebox.showerror("Error", "Don't have a product.", parent=purchase_page)

            else:
                Scrolledtext.configure(state='normal')
                count = Scrolledtext.get('1.0', END)
                if count.find('Total') == -1:
                    Scrolledtext.configure(state='normal')
                    divided = "\n\n" + "\t" + ("——" * 20) + "\n"
                    Scrolledtext.insert('insert', divided)
                    total = "\t       Total:\t\t\t\t  RM  {}\n".format(cart.total())
                    Scrolledtext.insert('insert', total)
                    divided2 = "\t" + ("——" * 20) + "\n\n\tCashier : "
                    Scrolledtext.insert('insert', divided2)
                    Scrolledtext.configure(state="normal")
                    removeCart.configure(state='disable', background='grey')
                    addCart.configure(state='disable',background='grey')

        def generate_bill():
            state = 1
            if state == 1:
                count = Scrolledtext.get('1.0', END)

                if cash_name.get() == "":
                    messagebox.showerror("Error", "Please enter cashier name", parent=purchase_page)

                elif company_entry.get() == "":
                    messagebox.showerror("Error", "Please enter company number", parent=purchase_page)

                elif not valid_phone(company_entry.get()):
                    messagebox.showerror("Error", 'Please enter a valid number', parent=purchase_page)

                elif cart.isEmpty():
                    messagebox.showerror("Error", "Cart Empty", parent=purchase_page)

                else:
                    if count.find('Total') == -1:
                        total_bill()
                        generate_bill()

                    else:
                        cashNameText.insert(END, cash_name.get())

                        compContactText.insert(END, company_num.get())

                        bill_num.set(random_bill_number(6))

                        billNumbText.insert(END, bill_num.get())

                        bill_date.set(str(date.today()))

                        billDateText.insert(END, bill_date.get())

                        Scrolledtext.insert(END, cash_name.get())
                        row1 = "\n\n\tRECEIPT : "
                        Scrolledtext.insert('insert', row1)
                        Scrolledtext.insert(END, bill_num.get())
                        row2 = "\n\n\tDATE : "
                        Scrolledtext.insert('insert', row2)
                        Scrolledtext.insert(END, bill_date.get())
                        row3 = "\n\n\t" + ("——" * 20) + "\n\n\tHOTLINK NUMBER : "
                        Scrolledtext.insert("insert", row3)
                        Scrolledtext.insert(END, company_entry.get())

                        with sqlite3.connect("./database/DnetPower.db") as Db:
                            cur = Db.cursor()

                        insert = ("INSERT INTO Purchase (purchase_product_name, purchase_brand, purchase_quantity,"
                                  "purchase_time,purchase_billnm,purchase_cashier_name,purchase_status) VALUES(?,?,?,"
                                  "?,?,?,?)")
                        cur.execute(insert, [productName_combo.get(), productBrand_combo.get(), productQty_entry.get(),
                                             purchaseDate_entry.get(), bill_num.get(), cash_name.get(),
                                             purchaseStatus_combo.get()])
                        Db.commit()

                        product_name = productName_combo.get()
                        quantity = productQty_entry.get()
                        update_quantity = "UPDATE stock SET stock_quantity = stock_quantity - ? WHERE stock_name = ?"
                        cur.execute(update_quantity, [quantity, product_name])
                        Db.commit()

                        messagebox.showinfo("Success", "Generating Bill", parent=purchase_page)
                        cashier_entry.configure(state='disable', background='grey')
                        company_entry.configure(state='disable', background='grey')
                        removeCart.configure(state="disable", background='grey')
                        addCart.configure(state='disable', background='grey')
            else:
                return

        def clear_all():
            cashier_entry.configure(state='normal')
            company_entry.configure(state='normal')
            removeCart.configure(state="normal", background='white')
            addCart.configure(state='normal', background='white')
            cashier_entry.delete(0, END)
            productQty_entry.delete(0, END)
            cashNameText.configure(state='normal')
            compContactText.configure(state='normal')
            billNumbText.configure(state='normal')
            billDateText.configure(state='normal')
            Scrolledtext.configure(state='normal')
            productName_combo.configure(state='normal')
            productGroup_combo.configure(state='normal')
            productBrand_combo.configure(state='normal')
            productName_combo.delete(0, END)
            productGroup_combo.delete(0, END)
            productBrand_combo.delete(0, END)
            productQty_entry.delete(0, END)
            customerEmail_entry.delete(0, END)
            productGroup_combo.configure(state='disable')
            productBrand_combo.configure(state='disable')
            productQty_entry.configure(state='disable')
            cashNameText.delete(1.0, END)
            compContactText.delete(1.0, END)
            billNumbText.delete(1.0, END)
            billDateText.delete(1.0, END)
            Scrolledtext.delete(1.0, END)
            cart.remove_items()
            top = "\n\n\t\t\tDNET POWER COMPUTER CENTER \n" \
                  "\t\t\t         JALAN SIMPANG KUALA  \n\n\t\t\t       FAX NUMBER: +04 378398" \
                  "\n\n\t\t\tTHANK FOR CHOOSING OUR SHOPE\n" \
                  "\t\t\t         WELCOM ONCE AGAIN\n\n\n" + "\n\n\n\n\n " \
                                                             "\t————————————————————————————————————————————————" \
                  + "\n\t      PRODUCT\t\t    QUANTITY\t\tPRICE ( RM )\n" + " \t———————————————————————————————————————————————— \n"
            Scrolledtext.insert('insert', top)

        def clear_purchaseFrame():
            cashier_entry.delete(0, END)
            productName_combo.configure(state='normal')
            productGroup_combo.configure(state='normal')
            productBrand_combo.configure(state='normal')
            productName_combo.delete(0, END)
            productGroup_combo.delete(0, END)
            productBrand_combo.delete(0, END)
            productQty_entry.delete(0, END)
            customerEmail_entry.delete(0, END)
            productGroup_combo.configure(state='disable')
            productBrand_combo.configure(state='disable')
            productQty_entry.configure(state='disable')
            try:
                quantity_label.configure(foreground='#BBD0FF')

            except AttributeError:
                pass

        def send_email():
            character = ['@', '.']

            if customerEmail_entry.get() == "":
                messagebox.showerror("Fail", "Please enter customer email")

            elif not any(ch in character for ch in customerEmail_entry.get()):
                messagebox.showerror("Fail", "Please enter correct format of email")

            else:
                root = Toplevel()
                root.title('Gmail')
                root.geometry("400x400")
                root.configure(background='#BBD0FF')

                def sendEmail():
                    if root.filename == "":
                        send.configure(state='disable')
                        send.configure(background='grey')

                    else:
                        send.configure(state='normal')
                        _gEmailApi = googleEmail.googleEmailApi()
                        # msg = _gEmailApi.create_message("demofyp00@gmail.com", "demofyp00@gmail.com", "test", "Hello")
                        # print(rf"{root.filename}")
                        msg = _gEmailApi.create_message_with_attachment("demofyp00@gmail.com", customerEmail_entry.get(), "Invoice", "Hello",
                                                                        rf"{root.filename}")
                        _gEmailApi.send_message("demofyp00@gmail.com", msg)
                        root.destroy()
                        messagebox.showinfo("Success", "Invoice send successful.")

                notification = Label(root, text="Below will send the attachment to customer email.\n\n "
                                                "Kindly ensure email before send.\n\n"
                                                "Have a nice day :D ", font=("Poppins SemiBold", 11, 'italic'),
                                     background='#BBD0FF')
                notification.place(x=25, y=70)
                send = Button(root, text="Send Invoice", font=("Poppins SemiBold", 10, 'italic'),
                              bg='white', fg='black', activebackground='#BBD0FF', width=15, border=0, cursor='hand2',
                              justify=CENTER, command=sendEmail)
                send.place(x=120, y=200)
                root.filename = filedialog.askopenfilename(initialdir
                                                           ="/Desktop", title="Select File", filetypes=(("pdf files", "*.pdf"), (
                                                           "all.files","*,*")))

                if __name__ == "__main__":
                    #Email API
                    root.mainloop()

        productName = Label(purchase_page, text="Product Name", font=("Poppins SemiBold", 11, 'italic'),
                            background='#BBD0FF')
        productName.place(x=65, y=210)

        productName_combo = ttk.Combobox(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=48,
                                         state="readonly", values=stock)
        productName_combo.option_add("*TCombobox*Listbox.font", text_font)
        productName_combo.option_add("*TCombobox*Listbox.selectBackground", "lightblue")
        productName_combo.place(x=65, y=235)

        productName_combo.bind("<<ComboboxSelected>>", get_group)

        productGroup = Label(purchase_page, text="Product Categories", font=("Poppins SemiBold", 11, 'italic'),
                             background='#BBD0FF')
        productGroup.place(x=65, y=260)

        productGroup_combo = ttk.Combobox(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=48,
                                          state="disable")
        productGroup_combo.option_add("*TCombobox*Listbox.font", text_font)
        productGroup_combo.place(x=65, y=285)

        productBrand = Label(purchase_page, text="Product Brand", font=("Poppins SemiBold", 11, 'italic'),
                             background='#BBD0FF')
        productBrand.place(x=65, y=310)

        productBrand_combo = ttk.Combobox(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=48,
                                          state="disable")
        productBrand_combo.option_add("*TCombobox*Listbox.font", text_font)
        productBrand_combo.place(x=65, y=335)

        productQty = Label(purchase_page, text="Product Quantity", font=("Poppins SemiBold", 11, 'italic'),
                           background='#BBD0FF')
        productQty.place(x=65, y=360)

        productQty_entry = Entry(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=50)
        productQty_entry.place(x=65, y=385)

        purchaseDate = Label(purchase_page, text="Date", font=("Poppins SemiBold", 11, 'italic'),
                             background='#BBD0FF')
        purchaseDate.place(x=65, y=440)

        purchaseDate_entry = DateEntry(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=48,
                                       textvariable=bill_date)
        purchaseDate_entry.place(x=65, y=465)

        purchaseStatus = Label(purchase_page, text="Status", font=("Poppins SemiBold", 11, 'italic'),
                               background='#BBD0FF')
        purchaseStatus.place(x=65, y=490)

        purchaseStatus_combo = ttk.Combobox(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=48,
                                            state="readonly")
        purchaseStatus_combo['values'] = ('paid', 'pending')
        purchaseStatus_combo.option_add("*TCombobox*Listbox.font", text_font)
        purchaseStatus_combo.option_add("*TCombobox*Listbox.selectBackground", "lightblue")
        purchaseStatus_combo.set('pending')
        purchaseStatus_combo.place(x=65, y=515)

        customerEmail = Label(purchase_page, text="Customer Email", font=("Poppins SemiBold", 11, 'italic'),
                              background='#BBD0FF')
        customerEmail.place(x=65, y=540)

        customerEmail_entry = Entry(purchase_page, font=("Poppins SemiBold", 11, 'italic'), width=50)
        customerEmail_entry.place(x=65, y=565)

        Scrolledtext = tst.ScrolledText(purchase_page, width=110, height=41, borderwidth=1, bg='white'
                                        , font=("Poppins SemiBold", 9, 'italic'), state='normal')
        Scrolledtext.place(x=550, y=90)
        top = "\n\n\t\t\tDNET POWER COMPUTER CENTER \n" \
              "\t\t\t         JALAN SIMPANG KUALA  \n\n\t\t\t       FAX NUMBER: +04 378398" \
              "\n\n\t\t\tTHANK FOR CHOOSING OUR SHOPE\n" \
              "\t\t\t         WELCOM ONCE AGAIN\n\n\n" + "\n\n\n\n\n " \
                                                               "\t————————————————————————————————————————————————"\
              + "\n\t      PRODUCT\t\t    QUANTITY\t\tPRICE ( RM )\n" + " \t———————————————————————————————————————————————— \n"
        Scrolledtext.insert('insert', top)

        addCart = Button(purchase_page, text="Add to Cart ", font=("Poppins SemiBold", 10, 'italic'),
                         bg='white', fg='black', activebackground='#BBD0FF', width=10, border=0, cursor='hand2',
                         justify=CENTER, command=add_cart)
        addCart.place(x=65, y=630)

        removeCart = Button(purchase_page, text="Remove Cart ", font=("Poppins SemiBold", 10, 'italic'),
                            bg='white', fg='black', activebackground='#BBD0FF', width=10, border=0, cursor='hand2',
                            justify=CENTER, command=remove_cart)
        removeCart.place(x=175, y=630)

        clearEntry = Button(purchase_page, text="Clear Info ", font=("Poppins SemiBold", 10, 'italic'),
                            bg='white', fg='black', activebackground='#BBD0FF', width=10, border=0, cursor='hand2',
                            justify=CENTER, command=clear_purchaseFrame)
        clearEntry.place(x=285, y=630)

        sendEmail = Button(purchase_page, text="Email ", font=("Poppins SemiBold", 10, 'italic'),
                            bg='white', fg='black', activebackground='#BBD0FF', width=8, border=0, cursor='hand2',
                            justify=CENTER, command=send_email)
        sendEmail.place(x=390, y=630)

        totalCart = Button(purchase_page, text="Total ", font=("Poppins SemiBold", 10, 'italic'),
                           bg='white', fg='black', activebackground='#BBD0FF', width=10, border=0, cursor='hand2',
                           justify=CENTER, command=total_bill)
        totalCart.place(x=65, y=670)

        generateBill = Button(purchase_page, text="Generate", font=("Poppins SemiBold", 10, 'italic'),
                              bg='white', fg='black', activebackground='#BBD0FF', width=10, border=0, cursor='hand2',
                              justify=CENTER, command=generate_bill)
        generateBill.place(x=175, y=670)

        clearCart = Button(purchase_page, text="Clear ", font=("Poppins SemiBold", 10, 'italic'),
                           bg='white', fg='black', activebackground='#BBD0FF', width=10, border=0, cursor='hand2',
                           justify=CENTER, command=clear_all)
        clearCart.place(x=285, y=670)

        def print_pdf(text):
            # tempfile - create a temporary file in a safe manner
            # mktemp - create a temporary file or directory
            file = tempfile.mktemp('.txt')
            open(file, 'w').write(text)
            os.startfile(file, 'print')

        printBill = Button(purchase_page, text="Save", font=("Poppins SemiBold", 10, 'italic'),
                           bg='white', fg='black', activebackground='#BBD0FF', width=10, border=0, cursor='hand2',
                           justify=CENTER, command=lambda: print_pdf(Scrolledtext.get('1.0', END)))
        printBill.place(x=385, y=670)

        billNumb = Label(purchase_page, text="Bill Number", font=("Poppins SemiBold", 11, 'italic'),
                         background='white')
        billNumb.place(x=640, y=260)

        billNumbText = Text(purchase_page, font=("Poppins SemiBold", 11, 'italic'),
                            background='white', borderwidth=0, width=20, height=1)
        billNumbText.place(x=730, y=264)

        billDate = Label(purchase_page, text="Bill Date", font=("Poppins SemiBold", 11, 'italic'),
                         background='white')
        billDate.place(x=640, y=300)

        billDateText = Text(purchase_page, font=("Poppins SemiBold", 11, 'italic'),
                            background='white', borderwidth=0, width=20, height=1)
        billDateText.place(x=730, y=304)

        cashName = Label(purchase_page, text="Cashier Name", font=("Poppins SemiBold", 11, 'italic'),
                         background='white')
        cashName.place(x=950, y=260)

        cashNameText = Text(purchase_page, font=("Poppins SemiBold", 11, 'italic'),
                            background='white', borderwidth=0, width=20, height=1)
        cashNameText.place(x=1090, y=264)

        compContact = Label(purchase_page, text="Company Number", font=("Poppins SemiBold", 11, 'italic'),
                            background='white')
        compContact.place(x=950, y=300)

        compContactText = Text(purchase_page, font=("Poppins SemiBold", 11, 'italic'),
                               background='white', borderwidth=0, width=20, height=1)
        compContactText.place(x=1090, y=304)

        def leave():
            close = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=purchase_page)
            if close == True:
                purchase_page.destroy()

            else:
                pass

        purchase_page.protocol("WM_DELETE_WINDOW", leave)


def page():
    window = Tk()
    AdminPurchase(window)
    window.mainloop()


if __name__ == "__main__":
    page()
