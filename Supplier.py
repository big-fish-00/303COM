from tkinter import *
import os
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class Supplier:
    def __init__(self, supplier_page):
        self.supplier_page = supplier_page

        supplier_page.rowconfigure(0, weight=0)
        supplier_page.columnconfigure(0, weight=0)
        width = 1410
        height = 720
        screen_width = supplier_page.winfo_screenwidth()
        screen_height = supplier_page.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 3.5) - (height / 3.5)
        supplier_page.geometry("%dx%d+%d+%d" % (width, height, x, y))

        supplier_page.title('Inventory')

        supplier_page['bg'] = '#BBD0FF'

        def default():
            supplier_page.destroy()
            filename = 'EmployeeHome.py'
            os.system(filename)

        def inventory():
            supplier_page.destroy()
            filename = 'inventory.py'
            os.system(filename)

        def supplier():
            supplier_page.destroy()
            filename = 'Supplier.py'
            os.system(filename)

        def purchase():
            supplier_page.destroy()
            filename = 'purchase.py'
            os.system(filename)

        def logout():
            supplier_page.destroy()
            filename = 'account.py'
            os.system(filename)

        def control():

            menuFrame = Frame(supplier_page, width=300, height=750, bg='#D4E1F1', border=1)
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

            button(0, 80, 'H O M E', default)
            button(0, 120, 'I N V E N T O R Y', inventory)
            button(0, 160, 'S U P P L I E R', supplier)
            button(0, 200, 'P U R C H A S E', purchase)
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
        header_line = Canvas(supplier_page, width=1420, height=1, bg="black", highlightthickness=0)
        header_line.place(x=0, y=60)

        # OPEN MENU BAR IMG
        menu_img = Image.open('images\\menu.png')
        menu_img_resize = menu_img.resize((25, 25))
        menu_photo = ImageTk.PhotoImage(menu_img_resize)
        menu_photo_place = Label(supplier_page, image=menu_photo, bg='#BBD0FF')
        menu_photo_place.image = menu_photo

        # OPEN MENU BAR BUTTON
        menuBtn = Button(supplier_page, image=menu_photo, bg='#BBD0FF', activebackground='#BBD0FF', width=40, height=40,
                         border=0, command=control)
        menuBtn.place(x=0, y=9)

        # CONNECT DATABASE
        def query_database():

            for datas in supplier_table.get_children():
                supplier_table.delete(datas)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("select rowid, * from Supplier")
            rows = cur.fetchall()

            global counter
            counter = 0

            for record in rows:
                if counter % 2 == 0:
                    supplier_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7]), tags=('evenrow',))
                else:
                    supplier_table.insert(parent='', index='end', iid=counter, text='',
                                      values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                              record[7]), tags=('oddrow',))
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

            c.execute("""CREATE TABLE if not exists Supplier (
            supplier_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name     TEXT,
            supplier_contact  TEXT,
            supplier_address  TEXT,
            supplier_state    TEXT,
            supplier_postcode INTEGER,
            stock_document    VARCHAR
            )""")

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # ADD DATA
        def add_stock():
            if id_entry.get() == "":
                messagebox.showerror("Failed", "ID can't be empty")
            else:
                conn = sqlite3.connect("./database/DnetPower.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO Supplier values(?,?,?,?,?,?,?)",
                            (id_entry.get(), name_entry.get(), contact_entry.get(),
                             address_entry.get(), state_entry.get(), postcode_entry.get(),
                             document_entry.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Supplier Info added into inventory")

            id_entry.delete(0, END)
            name_entry.delete(0, END)
            contact_entry.delete(0, END)
            address_entry.delete(0, END)
            state_entry.delete(0, END)
            postcode_entry.delete(0, END)
            document_entry.delete(0, END)

            supplier_table.delete(*supplier_table.get_children())
            query_database()

        # MOVE UP
        def move_up():
            rows = supplier_table.selection()
            for row in rows:
                supplier_table.move(row, supplier_table.parent(row), supplier_table.index(row) - 1)

        # MOVE DOWN
        def move_down():
            rows = supplier_table.selection()
            for row in reversed(rows):
                supplier_table.move(row, supplier_table.parent(row), supplier_table.index(row) + 1)

        # DELETE ONE DATA
        def delete_data():
            x = supplier_table.selection()[0]
            supplier_table.delete(x)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM Supplier where supplier_id=?",
                        [id_entry.get()])
            conn.commit()
            conn.close()

        # DELETE MANY DATA
        def delete_mny_data():
            response = messagebox.askyesno("Warning", "This will delete every select from what you choose "
                                                      "in the table\nAre You Sure?")

            if response == 1:
                x = supplier_table.selection()

                delete_list = []
                for data in x:
                    delete_list.append(supplier_table.item(data, 'values')[0])

                for data in x:
                    supplier_table.delete(data)
                    conn = sqlite3.connect("./database/DnetPower.db")
                    cur = conn.cursor()
                    cur.executemany("DELETE FROM Supplier where supplier_id=?", [(z,) for z in delete_list])
                    conn.commit()
                    conn.close()
                    clear_data()

        # DELETE ALL DATA
        def delete_all():
            # Add a little message box for fun
            response = messagebox.askyesno("Warning", "This will delete every supplier info from"
                                                      "the table\nAre You Sure?")

            # Add logic for message box
            if response == 1:
                for datas in supplier_table.get_children():
                    supplier_table.delete(datas)

                conn = sqlite3.connect("./database/DnetPower.db")
                cur = conn.cursor()
                cur.execute("DROP TABLE Supplier")
                conn.commit()
                conn.close()
                clear_data()
                create_table()

        # CLEAR DATA
        def clear_data():
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            contact_entry.delete(0, END)
            address_entry.delete(0, END)
            state_entry.delete(0, END)
            postcode_entry.delete(0, END)
            document_entry.delete(0, END)

        # SELECT DATA FROM TREEVIEW
        def slc_data(e):
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            contact_entry.delete(0, END)
            address_entry.delete(0, END)
            state_entry.delete(0, END)
            postcode_entry.delete(0, END)
            document_entry.delete(0, END)

            # GET NUMBER
            slc = supplier_table.focus()
            # GET DATA VALUE
            value = supplier_table.item(slc, "values")

            id_entry.insert(0, value[0])
            name_entry.insert(0, value[1])
            contact_entry.insert(0, value[2])
            address_entry.insert(0, value[3])
            state_entry.insert(0, value[4])
            postcode_entry.insert(0, value[5])
            document_entry.insert(0, value[6])

        # UPDATE
        def update_stock():
            get = supplier_table.focus()
            supplier_table.item(get, text="", values=(id_entry.get(), name_entry.get(), contact_entry.get(),
                                                      address_entry.get(), state_entry.get(), postcode_entry.get(),
                                                      document_entry.get()))

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute(
                "UPDATE Supplier set supplier_name=?, supplier_contact=?, supplier_address=?,"
                "supplier_state=?, supplier_postcode=?, supplier_document=? where supplier_id=?",
                (name_entry.get(), contact_entry.get(), address_entry.get(), state_entry.get(),
                 postcode_entry.get(), document_entry.get(), id_entry.get()))
            conn.commit()
            conn.close()

            id_entry.delete(0, END)
            name_entry.delete(0, END)
            contact_entry.delete(0, END)
            address_entry.delete(0, END)
            state_entry.delete(0, END)
            postcode_entry.delete(0, END)
            document_entry.delete(0, END)

        def search_data():
            get = searchName_entry.get()

            for datas in supplier_table.get_children():
                supplier_table.delete(datas)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("select rowid, * from Supplier WHERE supplier_name like ?", (get,))
            rows = cur.fetchall()

            global counter
            counter = 0

            for record in rows:
                if counter % 2 == 0:
                    supplier_table.insert(parent='', index='end', iid=counter, text='',
                                          values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                                  record[7]), tags=('evenrow',))
                else:
                    supplier_table.insert(parent='', index='end', iid=counter, text='',
                                          values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                                  record[7]), tags=('oddrow',))
                # increment counter
                counter += 1

            conn.commit()
            conn.close()

        def search_document():
            get = searchDocument_entry.get()

            for datas in supplier_table.get_children():
                supplier_table.delete(datas)

            conn = sqlite3.connect("./database/DnetPower.db")
            cur = conn.cursor()
            cur.execute("select rowid, * from Supplier WHERE supplier_document like ?", (get,))
            rows = cur.fetchall()

            global counter
            counter = 0

            for record in rows:
                if counter % 2 == 0:
                    supplier_table.insert(parent='', index='end', iid=counter, text='',
                                          values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                                  record[7]), tags=('evenrow',))
                else:
                    supplier_table.insert(parent='', index='end', iid=counter, text='',
                                          values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                                  record[7]), tags=('oddrow',))
                # increment counter
                counter += 1

            conn.commit()
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
        tree_frame = Frame(supplier_page)
        tree_frame.pack(pady=80)

        # Create a Treeview Scrollbar
        tree_scrollbar = Scrollbar(tree_frame)
        tree_scrollbar.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        supplier_table = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set, selectmode="extended")
        supplier_table.pack()

        # Configure the Scrollbar
        tree_scrollbar.config(command=supplier_table.yview)

        # Define Our Columns
        supplier_table['columns'] = ("ID", "Name", "Contact Number", "Address",
                                     "State", "Postcode", "Document NO")

        # Format Our Columns
        supplier_table.column("#0", width=0, stretch=NO)
        supplier_table.column("ID", anchor=CENTER, width=50)
        supplier_table.column("Name", anchor=CENTER, width=140)
        supplier_table.column("Contact Number", anchor=CENTER, width=150)
        supplier_table.column("Address", anchor=CENTER, width=140)
        supplier_table.column("State", anchor=CENTER, width=100)
        supplier_table.column("Postcode", anchor=CENTER, width=80)
        supplier_table.column("Document NO", anchor=CENTER, width=140)

        # Create Headings
        supplier_table.heading("#0", text="", anchor=W)
        supplier_table.heading("ID", text="ID", anchor=W)
        supplier_table.heading("Name", text="Name", anchor=W)
        supplier_table.heading("Contact Number", text="Contact Number", anchor=W)
        supplier_table.heading("Address", text="Address", anchor=W)
        supplier_table.heading("State", text="State", anchor=W)
        supplier_table.heading("Postcode", text="Postcode", anchor=W)
        supplier_table.heading("Document NO", text="Document NO", anchor=W)

        # Create Striped Row Tags
        supplier_table.tag_configure('oddrow', background="white")
        supplier_table.tag_configure('evenrow', background="lightblue")

        # Create label frame
        search_frame = LabelFrame(supplier_page, text="Search Supplier Name", font=("Comic Sans MS", 15, 'italic'),
                                  background='#BBD0FF')
        search_frame.pack(fill="x", padx=20)
        search_frame.place(x=20, y=360)

        searchName_entry = Entry(search_frame, font=("Arial", 10, 'italic'))
        searchName_entry.grid(row=0, column=0, padx=8, pady=10)

        searchName_button = Button(search_frame, text='Search Name', font=('Roboto', 10, 'italic'), command=search_data)
        searchName_button.grid(row=0, column=1, padx=10, pady=10)

        searchDocument_entry = Entry(search_frame, font=("Arial", 10, 'italic'))
        searchDocument_entry.grid(row=0, column=3, padx=8, pady=10)

        searchDocument_button = Button(search_frame, text='Search Document NO', font=('Roboto', 10, 'italic'), command=search_document)
        searchDocument_button.grid(row=0, column=4, padx=10, pady=10)

        # Add Record Entry Boxes
        info_frame = LabelFrame(supplier_page, text="Supplier Info", font=("Comic Sans MS", 15, 'italic'),
                                background='#BBD0FF')
        info_frame.pack(fill="x", padx=20, pady=(30, 0))

        id_label = Label(info_frame, text="ID", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        id_label.grid(row=0, column=0, padx=8, pady=10)
        id_entry = Entry(info_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        name_label = Label(info_frame, text="Name", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        name_label.grid(row=0, column=2, padx=8, pady=10)
        name_entry = Entry(info_frame)
        name_entry.grid(row=0, column=3, padx=10, pady=10)

        contact_label = Label(info_frame, text="Contact Number", font=("Comic Sans MS", 10, 'italic'),
                              background='#BBD0FF')
        contact_label.grid(row=0, column=4, padx=8, pady=10)
        contact_entry = Entry(info_frame)
        contact_entry.grid(row=0, column=5, padx=10, pady=10)

        address_label = Label(info_frame, text="Address", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        address_label.grid(row=0, column=6, padx=8, pady=10)
        address_entry = Entry(info_frame)
        address_entry.grid(row=0, column=7, padx=10, pady=10)

        state_label = Label(info_frame, text="State", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        state_label.grid(row=0, column=8, padx=8, pady=10)
        state_entry = Entry(info_frame)
        state_entry.grid(row=0, column=9, padx=10, pady=10)

        postcode_label = Label(info_frame, text="Postcode", font=("Comic Sans MS", 10, 'italic'), background='#BBD0FF')
        postcode_label.grid(row=0, column=10, padx=8, pady=10)
        postcode_entry = Entry(info_frame)
        postcode_entry.grid(row=0, column=11, padx=10, pady=10)

        document_label = Label(info_frame, text="Document NO", font=("Comic Sans MS", 10, 'italic'),
                               background='#BBD0FF')
        document_label.grid(row=1, column=0, padx=8, pady=10)
        document_entry = Entry(info_frame)
        document_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add Buttons
        button_frame = LabelFrame(supplier_page, text="Commands", font=("Comic Sans MS", 15, 'italic'),
                                  background='#BBD0FF')
        button_frame.pack(fill="x", padx=20, pady=(30, 0))

        update_button = Button(button_frame, text="Update Record", font=("Comic Sans MS", 10, 'italic'),
                               bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                               justify=CENTER, command=update_stock)
        update_button.grid(row=0, column=0, padx=30, pady=8)

        add_button = Button(button_frame, text="Add Record", font=("Comic Sans MS", 10, 'italic'),
                            bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                            justify=CENTER, command=add_stock)
        add_button.grid(row=0, column=1, padx=30, pady=8)

        remove_all_button = Button(button_frame, text="Remove All Records", font=("Comic Sans MS", 10, 'italic'),
                                   bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                                   justify=CENTER, command=delete_all)
        remove_all_button.grid(row=0, column=2, padx=30, pady=8)

        remove_one_button = Button(button_frame, text="Remove One Selected", font=("Comic Sans MS", 10, 'italic'),
                                   bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                                   justify=CENTER, command=delete_data)
        remove_one_button.grid(row=0, column=3, padx=30, pady=8)

        remove_many_button = Button(button_frame, text="Remove Many Selected", font=("Comic Sans MS", 10, 'italic'),
                                    bg='black', fg='white', activebackground='white', border=0, cursor='hand2',
                                    justify=CENTER, command=delete_mny_data)
        remove_many_button.grid(row=0, column=4, padx=30, pady=8)

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
        supplier_table.bind('<ButtonRelease-1>', slc_data)
        query_database()

        def leave():
            close = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=supplier_page)
            if close == True:
                supplier_page.destroy()

            else:
                pass

        supplier_page.protocol("WM_DELETE_WINDOW", leave)


def page():
    window = Tk()
    Supplier(window)
    window.mainloop()


if __name__ == "__main__":
    page()
