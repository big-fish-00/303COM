from tkinter import *
import os
from PIL import ImageTk, Image
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import sqlite3


class Inventory:
    def __init__(self, inventory_page):
        self.inventory_page = inventory_page

        inventory_page.rowconfigure(0, weight=0)
        inventory_page.columnconfigure(0, weight=0)
        width = 1410
        height = 720
        screen_width = inventory_page.winfo_screenwidth()
        screen_height = inventory_page.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 3.5) - (height / 3.5)
        inventory_page.geometry("%dx%d+%d+%d" % (width, height, x, y))
        inventory_page.resizable(0, 0)

        inventory_page.title('Inventory')

        inventory_page['bg'] = '#BBD0FF'

        def default_page():
            inventory_page.destroy()
            filename = 'EmployeeHome.py'
            os.system(filename)

        def inventory():
            inventory_page.destroy()
            filename = 'inventory.py'
            os.system(filename)

        def supplier():
            inventory_page.destroy()
            filename = 'Supplier.py'
            os.system(filename)

        def purchase():
            inventory_page.destroy()
            filename = 'purchase.py'
            os.system(filename)

        def logout():
            inventory_page.destroy()
            filename = 'account.py'
            os.system(filename)

        def control():

            menuFrame = Frame(inventory_page, width=300, height=750, bg='#D4E1F1', border=1)
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
        header_line = Canvas(inventory_page, width=1420, height=1, bg="black", highlightthickness=0)
        header_line.place(x=0, y=60)

        # OPEN MENU BAR IMG
        menu_img = Image.open('images\\menu.png')
        menu_img_resize = menu_img.resize((25, 25))
        menu_photo = ImageTk.PhotoImage(menu_img_resize)
        menu_photo_place = Label(inventory_page, image=menu_photo, bg='#BBD0FF')
        menu_photo_place.image = menu_photo

        # OPEN MENU BAR BUTTON
        menuBtn = Button(inventory_page, image=menu_photo, bg='#BBD0FF', activebackground='#BBD0FF', width=40, height=40,
                         border=0, command=control)
        menuBtn.place(x=0, y=9)

        # CONNECT DATABASE
        def query_database():
            searchName.delete(0, END)

            for datas in tree_table.get_children():
                tree_table.delete(datas)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("select rowid, * from stock")
            rows = cur.fetchall()

            global counter
            counter = 0

            for record in rows:
                if counter % 2 == 0:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8], record[9], record[10], record[11], record[12]),
                                      tags=('evenrow',))
                else:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8], record[9], record[10], record[11], record[12]),
                                      tags=('oddrow',))
                # increment counter
                counter += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # CREATE TABLE
        def create_table():
            conn = sqlite3.connect('./database/DnetPower.db')

            # Create a cursor instance
            c = conn.cursor()

            # Create Table
            c.execute("""CREATE TABLE if not exists stock (
              stock_id          INTEGER PRIMARY KEY AUTOINCREMENT,
              stock_name        TEXT,
              stock_description TEXT,
              stock_group       TEXT,
              stock_brand       TEXT,
              stock_price       INTEGER,
              stock_quantity    INTEGER,
              stock_date        DATETIME,
              stock_supplier    TEXT     REFERENCES Supplier (supplier_name),
              stock_document    INTEGER  REFERENCES Supplier (supplier_document),
              stock_discount    DECIMAL,
              stock_total       DOUBLE
              )""")

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # ADD DATA
        def add_stock():
            format = "%d/%m/%Y"

            if id_entry.get() == "":
                messagebox.showerror("Failed", "ID can't be empty")

            elif not any(num.isdigit() for num in id_entry.get()):
                messagebox.showerror("Failed", "ID must be a number")

            elif name_entry.get() == "":
                messagebox.showerror("Failed", "Stock Name can't be empty")

            elif descrip_entry.get() == "":
                messagebox.showerror("Failed", "Description can't be empty")

            elif group_entry.get() == "":
                messagebox.showerror("Failed", "Group can't be empty")

            elif brand_entry.get() == "":
                messagebox.showerror("Failed", "Brand can't be empty")

            elif price_entry.get() == "":
                messagebox.showerror("Failed", "Price can't be empty")

            elif not any(num.isdigit() for num in price_entry.get()):
                messagebox.showerror("Failed", "Invalid Price")

            elif qty_entry.get() == "":
                messagebox.showerror("Failed", "Quantity can't be empty")

            elif not any(num.isdigit() for num in qty_entry.get()):
                messagebox.showerror("Failed", "Invalid Quantity")

            elif date_entry.get() == "":
                messagebox.showerror("Failed", "Date can't be empty")

            elif date_entry.get() == (datetime.strptime(date_entry.get(), format)):
                messagebox.showerror("Failed", "Date format incorrect")

            elif supplier_entry.get() == "":
                messagebox.showerror("Failed", "Supplier can't be empty")

            elif document_entry.get() == "":
                messagebox.showerror("Failed", "Document NO can't be empty")

            elif discount_entry.get() == "":
                messagebox.showerror("Failed", "Discount can't be empty")

            elif total_entry.get() == "":
                messagebox.showerror("Failed", "Total price can't be empty")

            elif not any(num.isdigit() for num in total_entry.get()):
                messagebox.showerror("Failed", "Invalid Total Price")

            else:
                conn = sqlite3.connect("./database/DnetPower.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO stock values(?,?,?,?,?,?,?,?,?,?,?,?)",
                            (id_entry.get(), name_entry.get(), descrip_entry.get(),
                             group_entry.get(), brand_entry.get(), price_entry.get(),
                             qty_entry.get(), date_entry.get(), supplier_entry.get(),
                             document_entry.get(), discount_entry.get(), total_entry.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Stock added into inventory")

            id_entry.delete(0, END)
            name_entry.delete(0, END)
            descrip_entry.delete(0, END)
            group_entry.delete(0, END)
            brand_entry.delete(0, END)
            price_entry.delete(0, END)
            qty_entry.delete(0, END)
            date_entry.delete(0, END)
            supplier_entry.configure(state='normal')
            document_entry.configure(state='normal')
            supplier_entry.delete(0, END)
            document_entry.delete(0, END)
            discount_entry.delete(0, END)
            total_entry.delete(0, END)

            tree_table.delete(*tree_table.get_children())
            query_database()

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

        # DELETE ONE DATA
        def delete_data():
            x = tree_table.selection()[0]
            tree_table.delete(x)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM stock where stock_id=?",
                        [id_entry.get()])
            conn.commit()
            conn.close()

        # DELETE MANY DATA
        def delete_mny_data():
            response = messagebox.askyesno("Warning", "This will delete every select From The Table\nAre You Sure?")

            if response == 1:
                x = tree_table.selection()

                delete_list = []
                for data in x:
                    delete_list.append(tree_table.item(data, 'values')[0])

                for data in x:
                    tree_table.delete(data)
                    conn = sqlite3.connect("./database/DnetPower.db")
                    cur = conn.cursor()
                    cur.executemany("DELETE FROM stock where stock_id=?", [(z,) for z in delete_list])
                    conn.commit()
                    conn.close()
                    clear_data()

        # DELETE ALL DATA
        def delete_all():
            # Add a little message box for fun
            response = messagebox.askyesno("Warning", "This will delete everything from the table\nAre You Sure?")

            # Add logic for message box
            if response == 1:
                for datas in tree_table.get_children():
                    tree_table.delete(datas)

                conn = sqlite3.connect("./database/DnetPower.db")
                cur = conn.cursor()
                cur.execute("DROP TABLE stock")
                conn.commit()
                conn.close()
                clear_data()
                create_table()

        # CLEAR DATA
        def clear_data():
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            descrip_entry.delete(0, END)
            group_entry.delete(0, END)
            brand_entry.delete(0, END)
            price_entry.delete(0, END)
            qty_entry.delete(0, END)
            date_entry.delete(0, END)
            supplier_entry.configure(state='normal')
            document_entry.configure(state='normal')
            supplier_entry.delete(0, END)
            document_entry.delete(0, END)
            discount_entry.delete(0, END)
            total_entry.delete(0, END)

        # SELECT DATA FROM TREEVIEW
        def slc_data(e):
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            descrip_entry.delete(0, END)
            group_entry.delete(0, END)
            brand_entry.delete(0, END)
            price_entry.delete(0, END)
            qty_entry.delete(0, END)
            date_entry.delete(0, END)
            supplier_entry.configure(state='normal')
            document_entry.configure(state='normal')
            supplier_entry.delete(0, END)
            document_entry.delete(0, END)
            discount_entry.delete(0, END)
            total_entry.delete(0, END)

            # GET NUMBER
            slc = tree_table.focus()
            # GET DATA VALUE
            value = tree_table.item(slc, "values")

            id_entry.insert(0, value[0])
            name_entry.insert(0, value[1])
            descrip_entry.insert(0, value[2])
            group_entry.insert(0, value[3])
            brand_entry.insert(0, value[4])
            price_entry.insert(0, value[5])
            qty_entry.insert(0, value[6])
            date_entry.insert(0, value[7])
            supplier_entry.insert(0, value[8])
            document_entry.insert(0, value[9])
            discount_entry.insert(0, value[10])
            total_entry.insert(0, value[11])

        # UPDATE
        def update_stock():
            get = tree_table.focus()
            tree_table.item(get, text="", values=(id_entry.get(), name_entry.get(), descrip_entry.get(),
                                                  group_entry.get(), brand_entry.get(), price_entry.get(),
                                                  qty_entry.get(), date_entry.get(), supplier_entry.get(),
                                                  document_entry.get(), discount_entry.get(), total_entry.get()))

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute(
                "UPDATE stock set stock_name=?, stock_description=?, stock_group=?,"
                "stock_brand=?, stock_price=?, stock_quantity=?,"
                "stock_date=?, stock_supplier=?, stock_document=?, stock_discount=?, stock_total=? where stock_id=?",
                (name_entry.get(), descrip_entry.get(), group_entry.get(), brand_entry.get(),
                 price_entry.get(), qty_entry.get(), date_entry.get(), supplier_entry.get(), document_entry.get(),
                 discount_entry.get(), total_entry.get(), id_entry.get()))
            conn.commit()
            conn.close()

            id_entry.delete(0, END)
            name_entry.delete(0, END)
            descrip_entry.delete(0, END)
            group_entry.delete(0, END)
            brand_entry.delete(0, END)
            price_entry.delete(0, END)
            qty_entry.delete(0, END)
            date_entry.delete(0, END)
            supplier_entry.configure(state='normal')
            document_entry.configure(state='normal')
            supplier_entry.delete(0, END)
            document_entry.delete(0, END)
            discount_entry.delete(0, END)
            total_entry.delete(0, END)


        def search_data():
            get = searchName.get()

            for datas in tree_table.get_children():
                tree_table.delete(datas)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("select rowid, * from stock WHERE stock_name like ?", (get,))
            rows = cur.fetchall()

            global counter
            counter = 0

            for record in rows:
                if counter % 2 == 0:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8], record[9], record[10], record[11], record[12]),
                                      tags=('evenrow',))
                else:
                    tree_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7], record[8], record[9], record[10], record[11], record[12]),
                                      tags=('oddrow',))
                # increment counter
                counter += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        conn = sqlite3.connect("./database/DnetPower.db")

        cur = conn.cursor()
        find_supplier = "SELECT supplier_name from Supplier"
        cur.execute(find_supplier)
        result = cur.fetchall()
        suppliers = []
        for i in range(len(result)):
            if (result[i][0] not in suppliers):
                suppliers.append(result[i][0])
        # rows = [i[0] for i in cur.fetchall()]

        def select_document(e):
            document_entry.configure(state='readonly')
            conn2 = sqlite3.connect("./database/DnetPower.db")
            cur2 = conn2.cursor()
            find_doc = "SELECT supplier_document FROM Supplier WHERE supplier_name = ? ORDER BY supplier_document"
            cur2.execute(find_doc, [supplier_entry.get()])
            result2 = cur2.fetchall()
            group = []
            for j in range(len(result2)):
                if (result2[j][0] not in group):
                    group.append(result2[j][0])

            document_entry.configure(values=group)

        conn.commit()
        conn.close()

        opt = StringVar()
        opt2 = StringVar()

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
        tree_frame = Frame(inventory_page)
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
        tree_table['columns'] = ("ID", "Name", "Description", "Group",
                                 "Brand", "Price", "Quantity", "Date", "Supplier",
                                 "Document NO", "Discount", "Total Price")

        # Format Our Columns
        tree_table.column("#0", width=0, stretch=NO)
        tree_table.column("ID", anchor=W, width=50)
        tree_table.column("Name", anchor=W, width=140)
        tree_table.column("Description", anchor=CENTER, width=150)
        tree_table.column("Group", anchor=CENTER, width=140)
        tree_table.column("Brand", anchor=CENTER, width=140)
        tree_table.column("Price", anchor=CENTER, width=50)
        tree_table.column("Quantity", anchor=CENTER, width=140)
        tree_table.column("Date", anchor=CENTER, width=100)
        tree_table.column("Supplier", anchor=CENTER, width=140)
        tree_table.column("Document NO", anchor=CENTER, width=140)
        tree_table.column("Discount", anchor=CENTER, width=80)
        tree_table.column("Total Price", anchor=CENTER, width=80)

        # Create Headings
        tree_table.heading("#0", text="", anchor=W)
        tree_table.heading("ID", text="ID", anchor=W)
        tree_table.heading("Name", text="Name", anchor=W)
        tree_table.heading("Description", text="Description", anchor=CENTER)
        tree_table.heading("Group", text="Group", anchor=CENTER)
        tree_table.heading("Brand", text="Brand", anchor=CENTER)
        tree_table.heading("Price", text="Price", anchor=CENTER)
        tree_table.heading("Quantity", text="Quantity", anchor=CENTER)
        tree_table.heading("Date", text="Date", anchor=CENTER)
        tree_table.heading("Supplier", text="Supplier", anchor=CENTER)
        tree_table.heading("Document NO", text="Document NO", anchor=CENTER)
        tree_table.heading("Discount", text="Discount", anchor=CENTER)
        tree_table.heading("Total Price", text="Total Price", anchor=CENTER)

        # Create Striped Row Tags
        tree_table.tag_configure('oddrow', background="white")
        tree_table.tag_configure('evenrow', background="lightblue")

        # Create label frame
        search_frame = LabelFrame(inventory_page, text="Search Stock Name", font=("Poppins SemiBold", 15, 'italic'),
                                  background='#BBD0FF')
        search_frame.pack(fill="x", padx=20)
        search_frame.place(x=20, y=360)

        searchName = Entry(search_frame, font=("Arial", 10, 'italic'))
        searchName.grid(row=0, column=0, padx=8, pady=10)

        search_button = Button(search_frame, text='Search Name', font=('Roboto', 10, 'italic'), command=search_data)
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Add Record Entry Boxes
        info_frame = LabelFrame(inventory_page, text="Stock", font=("Poppins SemiBold", 15, 'italic'),
                                background='#BBD0FF')
        info_frame.pack(fill="x", padx=20, pady=(20, 0))

        id_label = Label(info_frame, text="ID", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        id_label.grid(row=0, column=0, padx=8, pady=10)
        id_entry = Entry(info_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        name_label = Label(info_frame, text="Name", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        name_label.grid(row=0, column=2, padx=8, pady=10)
        name_entry = Entry(info_frame)
        name_entry.grid(row=0, column=3, padx=10, pady=10)

        descrip_label = Label(info_frame, text="Description", font=("Poppins SemiBold", 10, 'italic'),
                              background='#BBD0FF')
        descrip_label.grid(row=0, column=4, padx=8, pady=10)
        descrip_entry = Entry(info_frame)
        descrip_entry.grid(row=0, column=5, padx=10, pady=10)

        group_label = Label(info_frame, text="Group", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        group_label.grid(row=0, column=6, padx=8, pady=10)
        group_entry = Entry(info_frame)
        group_entry.grid(row=0, column=7, padx=10, pady=10)

        brand_label = Label(info_frame, text="Brand", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        brand_label.grid(row=0, column=8, padx=8, pady=10)
        brand_entry = Entry(info_frame)
        brand_entry.grid(row=0, column=9, padx=10, pady=10)

        price_label = Label(info_frame, text="Price", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        price_label.grid(row=0, column=10, padx=8, pady=10)
        price_entry = Entry(info_frame)
        price_entry.grid(row=0, column=11, padx=10, pady=10)

        qty_label = Label(info_frame, text="Quantity", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        qty_label.grid(row=1, column=0, padx=8, pady=10)
        qty_entry = Entry(info_frame)
        qty_entry.grid(row=1, column=1, padx=10, pady=10)

        date_label = Label(info_frame, text="Date", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        date_label.grid(row=1, column=2, padx=8, pady=10)
        date_entry = Entry(info_frame)
        date_entry.grid(row=1, column=3, padx=10, pady=10)

        supplier_label = Label(info_frame, text="Supplier", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        supplier_label.grid(row=1, column=4, padx=8, pady=10)
        supplier_entry = ttk.Combobox(info_frame, textvariable=opt, state="readonly", background='white',
                                      values=suppliers)
        supplier_entry.bind("<<ComboboxSelected>>", select_document)
        supplier_entry.option_add("*TCombobox*Listbox.selectBackground", "lightblue")
        supplier_entry.grid(row=1, column=5, padx=10, pady=10)
        # supplier_entry.current(0)


        document_label = Label(info_frame, text="Document NO", font=("Poppins SemiBold", 10, 'italic'),
                               background='#BBD0FF')
        document_label.grid(row=1, column=6, padx=8, pady=10)
        document_entry = ttk.Combobox(info_frame, state="disable", textvariable=opt2, background='white')
        document_entry.grid(row=1, column=7, padx=10, pady=10)
        # document_entry.current(0)

        discount_label = Label(info_frame, text="Discount", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        discount_label.grid(row=1, column=8, padx=8, pady=10)
        discount_entry = Entry(info_frame)
        discount_entry.grid(row=1, column=9, padx=10, pady=10)

        total_label = Label(info_frame, text="Total Price", font=("Poppins SemiBold", 10, 'italic'), background='#BBD0FF')
        total_label.grid(row=1, column=10, padx=8, pady=10)
        total_entry = Entry(info_frame)
        total_entry.grid(row=1, column=11, padx=10, pady=10)

        # Add Buttons
        button_frame = LabelFrame(inventory_page, text="Commands", font=("Poppins SemiBold", 15, 'italic'),
                                  background='#BBD0FF')
        button_frame.pack(fill="x", padx=20, pady=(30, 0))

        update_button = Button(button_frame, text="Update Record", font=("Poppins SemiBold", 10, 'italic'),
                               border=0, cursor='hand2',
                               justify=CENTER, command=update_stock)
        update_button.grid(row=0, column=0, padx=30, pady=8)

        add_button = Button(button_frame, text="Add Record", font=("Poppins SemiBold", 10, 'italic'),
                            border=0, cursor='hand2',
                            justify=CENTER, command=add_stock)
        add_button.grid(row=0, column=1, padx=30, pady=8)

        remove_all_button = Button(button_frame, text="Remove All Records", font=("Poppins SemiBold", 10, 'italic'),
                                   border=0, cursor='hand2',
                                   justify=CENTER, command=delete_all)
        remove_all_button.grid(row=0, column=2, padx=30, pady=8)

        remove_one_button = Button(button_frame, text="Remove One Selected", font=("Poppins SemiBold", 10, 'italic'),
                                   border=0, cursor='hand2',
                                   justify=CENTER, command=delete_data)
        remove_one_button.grid(row=0, column=3, padx=30, pady=8)

        remove_many_button = Button(button_frame, text="Remove Many Selected", font=("Poppins SemiBold", 10, 'italic'),
                                    border=0, cursor='hand2',
                                    justify=CENTER, command=delete_mny_data)
        remove_many_button.grid(row=0, column=4, padx=30, pady=8)

        move_up_button = Button(button_frame, text="Move Up", font=("Poppins SemiBold", 10, 'italic'),
                                border=0, cursor='hand2',
                                justify=CENTER, command=move_up)
        move_up_button.grid(row=0, column=5, padx=30, pady=8)

        move_down_button = Button(button_frame, text="Move Down", font=("Poppins SemiBold", 10, 'italic'),
                                  border=0, cursor='hand2',
                                  justify=CENTER, command=move_down)
        move_down_button.grid(row=0, column=6, padx=30, pady=8)

        select_record_button = Button(button_frame, text="Clear All", font=("Poppins SemiBold", 10, 'italic'),
                                      border=0, cursor='hand2',
                                      justify=CENTER, command=clear_data)
        select_record_button.grid(row=0, column=7, padx=30, pady=8)

        reset_button = Button(button_frame, text="Reset", font=("Poppins SemiBold", 10, 'italic'),
                              border=0, cursor='hand2',
                              justify=CENTER, command=query_database)
        reset_button.grid(row=0, column=8, padx=30, pady=8)

        # BIND TREEVIEW
        tree_table.bind('<ButtonRelease-1>', slc_data)
        query_database()

        def leave():
            close = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=inventory_page)
            if close == True:
                inventory_page.destroy()

            else:
                pass

        inventory_page.protocol("WM_DELETE_WINDOW", leave)


def page():
    window = Tk()
    Inventory(window)
    window.mainloop()


if __name__ == "__main__":
    page()
