from tkinter import *
import os
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class PurchaseTable:
    def __init__(self, purchase_table_page):
        self.purchase_table_page = purchase_table_page

        purchase_table_page.rowconfigure(0, weight=0)
        purchase_table_page.columnconfigure(0, weight=0)
        width = 1410
        height = 720
        screen_width = purchase_table_page.winfo_screenwidth()
        screen_height = purchase_table_page.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 3.5) - (height / 3.5)
        purchase_table_page.geometry("%dx%d+%d+%d" % (width, height, x, y))

        purchase_table_page.title('Inventory')

        purchase_table_page['bg'] = '#BBD0FF'

        def default_page():
            purchase_table_page.destroy()
            filename = 'EmployeeHome.py'
            os.system(filename)

        def inventory():
            purchase_table_page.destroy()
            filename = 'inventory.py'
            os.system(filename)

        def supplier():
            purchase_table_page.destroy()
            filename = 'Supplier.py'
            os.system(filename)

        def purchase():
            purchase_table_page.destroy()
            filename = 'purchase.py'
            os.system(filename)

        def table():
            purchase_table_page.destroy()
            filename = 'PurchaseTable.py'
            os.system(filename)

        def logout():
            purchase_table_page.destroy()
            filename = 'account.py'
            os.system(filename)


        def control():

            menuFrame = Frame(purchase_table_page, width=300, height=750, bg='#D4E1F1', border=1)
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
            button(0, 240, 'P U R C H A S E T A B L E', table)
            button(0, 400, 'L O G O U T', logout)

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
        header_line = Canvas(purchase_table_page, width=1420, height=1, bg="black", highlightthickness=0)
        header_line.place(x=0, y=60)

        # OPEN MENU BAR IMG
        menu_img = Image.open('images\\menu.png')
        menu_img_resize = menu_img.resize((25, 25))
        menu_photo = ImageTk.PhotoImage(menu_img_resize)
        menu_photo_place = Label(purchase_table_page, image=menu_photo, bg='#BBD0FF')
        menu_photo_place.image = menu_photo

        # OPEN MENU BAR BUTTON
        menuBtn = Button(purchase_table_page, image=menu_photo, bg='#BBD0FF', activebackground='#BBD0FF', width=40, height=40,
                         border=0, command=control)
        menuBtn.place(x=0, y=9)

        # CONNECT DATABASE
        def query_database():
            for datas in tree_table.get_children():
                tree_table.delete(datas)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("select rowid, * from Purchase")
            rows = cur.fetchall()

            global counter
            counter = 0

            for record in rows:
                if counter % 2 == 0:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8]),
                                      tags=('evenrow',))
                else:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8]),
                                      tags=('oddrow',))
                # increment counter
                counter += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # MOVE UP
        def move_up():
            rows = tree_table.selection()
            for row in rows:
                tree_table.move(row, tree_table.parent(row), tree_table.index(row) - 1)

        # MOVE DOWN
        def move_down():
            rows = tree_table.selection()
            for row in reversed(rows):
                tree_table.move(row, tree_table.parent(row), tree_table.index(row) + 1)

        # CLEAR DATA
        def clear_data():
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            brand_entry.delete(0, END)
            quantity_entry.delete(0, END)
            time_entry.delete(0, END)
            billnm_entry.delete(0, END)
            cashier_entry.delete(0, END)
            status_entry.configure(state='normal')
            status_entry.delete(0, END)

        # SELECT DATA FROM TREEVIEW
        def slc_data(e):
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            brand_entry.delete(0, END)
            quantity_entry.delete(0, END)
            time_entry.delete(0, END)
            billnm_entry.delete(0, END)
            cashier_entry.delete(0, END)
            status_entry.configure(state='normal')
            status_entry.delete(0, END)

            # GET NUMBER
            slc = tree_table.focus()
            # GET DATA VALUE
            value = tree_table.item(slc, "values")

            id_entry.insert(0, value[0])
            name_entry.insert(0, value[1])
            brand_entry.insert(0, value[2])
            quantity_entry.insert(0, value[3])
            time_entry.insert(0, value[4])
            billnm_entry.insert(0, value[5])
            cashier_entry.insert(0, value[6])
            status_entry.insert(0, value[7])

        # UPDATE
        def update_stock():
            get = tree_table.focus()
            tree_table.item(get, text="", values=(id_entry.get(), name_entry.get(), brand_entry.get(),
                                                  quantity_entry.get(), time_entry.get(), billnm_entry.get(),
                                                  cashier_entry.get(), status_entry.get()))

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute(
                "UPDATE Purchase set purchase_product_name=?, purchase_brand=?, purchase_quantity=?,"
                "purchase_time=?, purchase_billnm=?, purchase_cashier_name=?,"
                "purchase_status=? where purchase_id=?",
                (name_entry.get(), brand_entry.get(), quantity_entry.get(), time_entry.get(),
                 billnm_entry.get(), cashier_entry.get(), status_entry.get(), id_entry.get()))
            conn.commit()
            conn.close()

            id_entry.delete(0, END)
            name_entry.delete(0, END)
            brand_entry.delete(0, END)
            quantity_entry.delete(0, END)
            time_entry.delete(0, END)
            billnm_entry.delete(0, END)
            cashier_entry.delete(0, END)
            status_entry.configure(state='normal')
            status_entry.delete(0, END)

        def search_data():
            get = searchName.get()

            for datas in tree_table.get_children():
                tree_table.delete(datas)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("select rowid, * from Purchase WHERE purchase_product_name like ?", (get,))
            rows = cur.fetchall()

            global counter
            counter = 0

            for record in rows:
                if counter % 2 == 0:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8]),
                                      tags=('evenrow',))
                else:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8]),
                                      tags=('oddrow',))
                # increment counter
                counter += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")

        # Change Selected Color
        style.map('Treeview',
                  background=[('selected', "#347083")])

        # Create a Treeview Frame
        tree_frame = Frame(purchase_table_page)
        tree_frame.pack(pady=80)

        # Create a Treeview Scrollbar
        tree_scrollbar = Scrollbar(tree_frame)
        tree_scrollbar.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        tree_table = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set, selectmode="extended")
        tree_table.pack()

        # Configure the Scrollbar
        tree_scrollbar.config(command=tree_table.yview)

        # Define Our Columns
        tree_table['columns'] = ("ID", "Product Name", "Brand", "Quantity",
                                 "Time", "Bill Num", "Cashier Name", "Status")

        # Format Our Columns
        tree_table.column("#0", width=0, stretch=NO)
        tree_table.column("ID", anchor=W, width=50)
        tree_table.column("Product Name", anchor=W, width=140)
        tree_table.column("Brand", anchor=CENTER, width=100)
        tree_table.column("Quantity", anchor=CENTER, width=100)
        tree_table.column("Time", anchor=CENTER, width=100)
        tree_table.column("Bill Num", anchor=CENTER, width=140)
        tree_table.column("Cashier Name", anchor=CENTER, width=140)
        tree_table.column("Status", anchor=CENTER, width=100)

        # Create Headings
        tree_table.heading("#0", text="", anchor=W)
        tree_table.heading("ID", text="ID", anchor=W)
        tree_table.heading("Product Name", text="Name", anchor=W)
        tree_table.heading("Brand", text="Brand", anchor=CENTER)
        tree_table.heading("Quantity", text="Quantity", anchor=CENTER)
        tree_table.heading("Time", text="Time", anchor=CENTER)
        tree_table.heading("Bill Num", text="Bill Num", anchor=CENTER)
        tree_table.heading("Cashier Name", text="Cashier Name", anchor=CENTER)
        tree_table.heading("Status", text="Status", anchor=CENTER)

        # Create Striped Row Tags
        tree_table.tag_configure('oddrow', background="white")
        tree_table.tag_configure('evenrow', background="lightblue")

        # Create label frame
        search_frame = LabelFrame(purchase_table_page, text="Search Product Name", font=("Comic Sans MS", 15, 'italic'),
                                  background='#BBD0FF')
        search_frame.pack(fill="x", padx=20)
        search_frame.place(x=20, y=360)

        searchName = Entry(search_frame, font=("Arial", 10, 'italic'))
        searchName.grid(row=0, column=0, padx=8, pady=10)

        search_button = Button(search_frame, text='Search Name', font=('Roboto', 10, 'italic'), command=search_data)
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Add Record Entry Boxes
        info_frame = LabelFrame(purchase_table_page, text="Purchase History", font=("Comic Sans MS", 15, 'italic'),
                                background='#BBD0FF')
        info_frame.pack(fill="x", padx=20, pady=(20, 0))

        id_label = Label(info_frame, text="ID", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        id_label.grid(row=0, column=0, padx=8, pady=10)
        id_entry = Entry(info_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        name_label = Label(info_frame, text="Product Name", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        name_label.grid(row=0, column=2, padx=8, pady=10)
        name_entry = Entry(info_frame)
        name_entry.grid(row=0, column=3, padx=10, pady=10)

        brand_label = Label(info_frame, text="Brand", font=("Comic Sans MS", 10, 'italic'),
                              background='#BBD0FF')
        brand_label.grid(row=0, column=4, padx=8, pady=10)
        brand_entry = Entry(info_frame)
        brand_entry.grid(row=0, column=5, padx=10, pady=10)

        quantity_label = Label(info_frame, text="Quantity", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        quantity_label.grid(row=0, column=6, padx=8, pady=10)
        quantity_entry = Entry(info_frame)
        quantity_entry.grid(row=0, column=7, padx=10, pady=10)

        time_label = Label(info_frame, text="Time", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        time_label.grid(row=0, column=8, padx=8, pady=10)
        time_entry = Entry(info_frame)
        time_entry.grid(row=0, column=9, padx=10, pady=10)

        billnm_label = Label(info_frame, text="Bill Num", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        billnm_label.grid(row=0, column=10, padx=8, pady=10)
        billnm_entry = Entry(info_frame)
        billnm_entry.grid(row=0, column=11, padx=10, pady=10)

        cashier_label = Label(info_frame, text="Cashier Name", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        cashier_label.grid(row=1, column=0, padx=8, pady=10)
        cashier_entry = Entry(info_frame)
        cashier_entry.grid(row=1, column=1, padx=10, pady=10)

        status_label = Label(info_frame, text="Status", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        status_label.grid(row=1, column=2, padx=8, pady=10)
        status_entry = ttk.Combobox(info_frame, font=("Poppins SemiBold", 11, 'italic'), width=14, state="readonly")
        status_entry['values'] = ('paid', 'pending')
        status_entry.option_add("*TCombobox*Listbox.selectBackground", "lightblue")
        status_entry.grid(row=1, column=3, padx=10, pady=10)

        # Add Buttons
        button_frame = LabelFrame(purchase_table_page, text="Commands", font=("Comic Sans MS", 15, 'italic'),
                                  background='#BBD0FF')
        button_frame.pack(fill="x", padx=20, pady=(30, 0))

        update_button = Button(button_frame, text="Update Record", font=("Comic Sans MS", 10, 'italic'),
                               bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                               justify=CENTER, command=update_stock)
        update_button.grid(row=0, column=0, padx=30, pady=8)

        move_up_button = Button(button_frame, text="Move Up", font=("Comic Sans MS", 10, 'italic'),
                                bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                                justify=CENTER, command=move_up)
        move_up_button.grid(row=0, column=5, padx=30, pady=8)

        move_down_button = Button(button_frame, text="Move Down", font=("Comic Sans MS", 10, 'italic'),
                                  bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                                  justify=CENTER, command=move_down)
        move_down_button.grid(row=0, column=6, padx=30, pady=8)

        select_record_button = Button(button_frame, text="Clear All", font=("Comic Sans MS", 10, 'italic'),
                                      bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                                      justify=CENTER, command=clear_data)
        select_record_button.grid(row=0, column=7, padx=30, pady=8)

        reset_button = Button(button_frame, text="Reset", font=("Comic Sans MS", 10, 'italic'),
                              bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                              justify=CENTER, command=query_database)
        reset_button.grid(row=0, column=8, padx=30, pady=8)

        # BIND TREEVIEW
        tree_table.bind('<ButtonRelease-1>', slc_data)
        query_database()

        def leave():
            close = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=purchase_table_page)
            if close == True:
                purchase_table_page.destroy()

            else:
                pass

        purchase_table_page.protocol("WM_DELETE_WINDOW", leave)


def page():
    window = Tk()
    PurchaseTable(window)
    window.mainloop()


if __name__ == "__main__":
    page()
