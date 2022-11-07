import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
import os


class Account:
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

        # WINDOW ICONS
        logo = Image.open('images\\logo.jpg')
        logo2 = ImageTk.PhotoImage(logo)
        root.iconphoto(True, logo2)
        root.title("Dnet Power Computer Center")

        # Navigating through windows
        select_account_page = Frame(root)
        login_account_admin_page = Frame(root)
        login_account_employee_page = Frame(root)
        create_account_page = Frame(root)

        for frame in (select_account_page, login_account_employee_page, login_account_admin_page, create_account_page):
            frame.grid(row=0, column=0, sticky='nsew')

        def show_frame(frame):
            frame.tkraise()

        # SHOW SELECT PAGE
        show_frame(select_account_page)

        # SELECT ACCOUNT BACKGROUND
        select_account_page['bg'] = '#BBD0FF'

        # EMPLOYEE IMG
        employee_img = Image.open('images\\team.png')
        employee_img_resize = employee_img.resize((100, 100))
        employee_photo = ImageTk.PhotoImage(employee_img_resize)
        employee_photo_place = Label(select_account_page, image=employee_photo, bg='#BBD0FF')
        employee_photo_place.image = employee_photo
        employee_photo_place.place(x=70, y=200)

        # EMPLOYEE BUTTON
        employee_Button = Button(select_account_page, text="Employee", font=("Comic Sans MS", 11, 'italic'),
                                 bg='black', fg='white', activebackground='white', width=20, border=0, cursor='hand2',
                                 justify=CENTER, command=lambda: show_frame(login_account_employee_page))
        employee_Button.place(x=30, y=350)

        # DIVIDE PAGE
        divide_page = Canvas(select_account_page, width=1.5, height=580, bg="#778899", highlightthickness=0)
        divide_page.place(x=250, y=10)

        # ADMIN IMG
        admin_img = Image.open('images\\admin.png')
        admin_img_resize = admin_img.resize((110, 110))
        admin_photo = ImageTk.PhotoImage(admin_img_resize)
        admin_photo_place = Label(select_account_page, image=admin_photo, bg='#BBD0FF')
        admin_photo_place.image = admin_photo
        admin_photo_place.place(x=325, y=200)

        # ADMIN BUTTON
        admin_Button = Button(select_account_page, text="Admin", font=("Comic Sans MS", 11, 'italic'),
                              bg='black', fg='white', activebackground='white', width=20, border=0, cursor='hand2',
                              justify=CENTER, command=lambda: show_frame(login_account_admin_page))
        admin_Button.place(x=285, y=350)

        # LOGIN EMPLOYEE BACKGROUND COLOR
        login_account_employee_page['bg'] = '#BBD0FF'
        back_img = Image.open('images\\back.png')
        back_img_resize = back_img.resize((30, 30))
        back_photo = ImageTk.PhotoImage(back_img_resize)
        back_photo_place = Button(login_account_employee_page, image=back_photo, bg='#BBD0FF',
                                  activebackground='#BBD0FF',
                                  cursor='hand2',
                                  border=0, command=lambda: show_frame(select_account_page))
        back_photo_place.image = back_photo
        back_photo_place.place(relx=0.02, rely=0.02, anchor='nw')
        # ad_back_previous.place(x=100, y=20)

        # LOGIN FORM
        login = LabelFrame(login_account_employee_page, bg="#BBD0FF", width='300', height=450)
        login.place(x=105, y=85)

        # LOGIN BLOCK
        wel = "Welcome to Dnet Power"
        top = Label(login_account_employee_page, text=wel, font=("Comic Sans MS", 15, 'italic'),
                    bg='#BBD0FF', fg='#040405')
        top.place(x=140, y=100)

        # SHOW EMPLOYEE PAGE
        def employee_page():
            root.destroy()
            filename = 'EmployeeHome.py'
            os.system(filename)

        def account_page():
            root.destroy()
            filename = 'account.py'
            os.system(filename)

        # DATABASE
        User_employee = StringVar()
        Password_employee = StringVar()

        def login_employee_database():
            try:
                conn = sqlite3.connect('./database/DnetPower.db')
                cursor = conn.cursor()
                find_pass = 'SELECT employee_password FROM Employee_Account'
                cursor.execute(find_pass)
                pass_result = cursor.fetchall()
                print(pass_result)
                new = [item for t in pass_result for item in t]
                print(f"Test {new}")
                # for decrypt
                key = b'qVnbM24duboqndhyHznH9hrd5IqLl5PjD8fspYKGI8Y='
                fernet = Fernet(key)
                for i in new:
                    decoded = fernet.decrypt(i)
                    decoded = str(decoded.decode("utf-8").strip())
                    # print(f"decoded {i} {decoded}")
                find_user = 'SELECT * FROM Employee_Account WHERE employee_username = ? '
                cursor.execute(find_user, [(u_employee_rec.get()),])
                result = cursor.fetchall()
                if result:
                    if decoded == p_employee_rec.get():
                        messagebox.showinfo("Login Status", 'Logged in Successfully.\n\nClick "OK" to continue.')
                        employee_page()
                    else:
                        messagebox.showerror("Login Status", "Password not match")
                else:
                    messagebox.showerror("Login Status", "Username doesn't exist\n\nPlease try again !")

            except Exception as ep:
               messagebox.showerror('', ep)

        # USER
        def enter(e):
            u_employee_rec.delete(0, 'end')

        def leave(e):
            name = u_employee_rec.get()
            if name == '':
                u_employee_rec.insert(0, 'Enter Username')

        user_employee = "Uername"
        u_employee_label = Label(login_account_employee_page, text=user_employee, font=("Comic Sans MS", 11,
                                                                                        'italic'), bg='#BBD0FF',
                                 fg='#040405')
        u_employee_label.place(x=160, y=180)

        u_employee_rec = Entry(login_account_employee_page, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                               font=("Comic Sans MS", 11, 'italic'), textvariable=User_employee)
        u_employee_rec.insert(0, 'Enter Username')
        u_employee_rec.bind('<FocusIn>', enter)
        u_employee_rec.bind('<FocusOut>', leave)
        u_employee_rec.place(x=135, y=210)

        # USER ICON
        u_employee_icon = Image.open('images\\user.png')
        u_employee_resize = u_employee_icon.resize((20, 20))
        user_employee_photo = ImageTk.PhotoImage(u_employee_resize)
        user_employee_icon = Label(login_account_employee_page, image=user_employee_photo, bg='#BBD0FF')
        user_employee_icon.image = user_employee_photo
        user_employee_icon.place(x=135, y=180)

        # PASSWORD
        def enter(e):
            p_employee_rec.delete(0, 'end')

        def leave(e):
            name = p_employee_rec.get()
            if name == '':
                p_employee_rec.insert(0, 'Enter Password')

        secret = "Password"
        p_employee_label = Label(login_account_employee_page, text=secret, font=("Comic Sans MS", 11, 'italic'),
                                 bg='#BBD0FF', fg='#040405')
        p_employee_label.place(x=165, y=260)

        p_employee_rec = Entry(login_account_employee_page, width=22, fg='#5a5a5a', relief=GROOVE, border=2,
                               bg='white', font=("Comic Sans MS", 11, 'italic'), textvariable=Password_employee)
        p_employee_rec.insert(0, 'Enter Password')
        p_employee_rec.bind('<FocusIn>', enter)
        p_employee_rec.bind('<FocusOut>', leave)
        p_employee_rec.place(x=135, y=290)

        # PASSWORD ICON
        password_employee_icon = Image.open('images\\padlock.png')
        password_employee_resize = password_employee_icon.resize((21, 20))
        password_employee_photo = ImageTk.PhotoImage(password_employee_resize)
        password_employee_place = Label(login_account_employee_page, image=password_employee_photo, bg='#BBD0FF')
        password_employee_place.image = password_employee_photo
        password_employee_place.place(x=135, y=260)

        # SHOW/HIDE PASSWORD
        def show_password():
            if p_employee_rec.cget('show') == "•":
                p_employee_rec.config(show="")

            else:
                p_employee_rec.config(show="•")

        show_pass = Checkbutton(login_account_employee_page, bg='#BBD0FF', activebackground='#BBD0FF',
                                command=show_password,
                                cursor='hand2')
        show_pass.select()
        show_pass.place(x=350, y=291)

        # LOGIN BUTTON
        login_employee_button = Button(login_account_employee_page, text="LOGIN", font=("Comic Sans MS", 11, 'italic'),
                                       bg='black', fg='white', activebackground='white', width=25, border=0,
                                       cursor='hand2',
                                       justify=CENTER, command=login_employee_database)
        login_employee_button.place(x=135, y=370)

        # FORGET PAGE WINDOW
        def employee_forget_password_page():
            window_ef = Toplevel(root)
            window_ef_width = 500
            window_ef_height = 500
            forget_page_screen_width = window_ef.winfo_screenwidth()
            forget_page_screen_height = window_ef.winfo_screenheight()
            p_x = int(forget_page_screen_width / 2) - (window_ef_width / 2)
            p_y = int(forget_page_screen_height / 2.5) - (window_ef_height / 2.5)
            window_ef.geometry("%dx%d+%d+%d" % (window_ef_width, window_ef_height, p_x, p_y))
            window_ef.title('Forgot Password')
            window_ef['bg'] = '#BBD0FF'
            window_ef.resizable(0, 0)
            window_ef.grab_set()

            # EMPLOYEE FORGET PASSWORD
            employee_forget_frame = LabelFrame(window_ef, bg="#BBD0FF", width='400', height=400)
            employee_forget_frame.place(x=55, y=55)

            employee_forget_word = Label(window_ef, text='Reset Password', font=("Comic Sans MS", 15, 'italic'),
                                bg='#BBD0FF', fg='#040405')
            employee_forget_word.place(x=180, y=65)

            def show_password5():
                if employee_forget_password_rec.cget('show') == "":
                    employee_forget_password_rec.config(show="•")
                    employee_forget_password_rec_2.config(show="•")

                else:
                    employee_forget_password_rec.config(show="")
                    employee_forget_password_rec_2.config(show="")

            show_pass5 = Checkbutton(window_ef, text='Show Password', font=("Comic Sans MS", 11, 'italic'),
                                     bg='#BBD0FF', activebackground='#BBD0FF',
                                     command=show_password5,
                                     cursor='hand2')
            show_pass5.select()
            show_pass5.place(x=150, y=320)

            # FORGET PASSWORD LINK WITH DATABASE

            employee_username_forget = StringVar()
            employee_password_forget = StringVar()
            employee_reenter_password = StringVar()

            # USERNAME & PASSWORD & REENTER PASSWORD
            # USERNAME ICON
            employee_fu_icon = Image.open('images\\user.png')
            employee_fu_resize = employee_fu_icon.resize((15, 15))
            employee_forget_user_photo = ImageTk.PhotoImage(employee_fu_resize)
            employee_forget_user_icon = Label(window_ef, image=employee_forget_user_photo, bg='#BBD0FF')
            employee_forget_user_icon.image = employee_forget_user_photo
            employee_forget_user_icon.place(x=150, y=130)

            # USERNAME
            employee_forget_page_user = Label(window_ef, text='Enter Username', bg='#BBD0FF', fg='#040405',
                                              font=("Comic Sans MS", 11, 'italic'))
            employee_forget_page_user.place(x=175, y=125)

            employee_forget_username_rec = Entry(window_ef, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                                 highlightthickness=2, textvariable=employee_username_forget,
                                                 font=("Comic Sans MS", 11, 'italic'))
            employee_forget_username_rec.place(x=150, y=155)

            # PASSWORD ICON
            employee_fp_icon = Image.open('images\\padlock.png')
            employee_fp_resize = employee_fp_icon.resize((17, 17))
            employee_fp_photo = ImageTk.PhotoImage(employee_fp_resize)
            employee_fp_place = Label(window_ef, image=employee_fp_photo, bg='#BBD0FF')
            employee_fp_place.image = employee_fp_photo
            employee_fp_place.place(x=150, y=193)

            # PASSWORD
            employee_forget_password = Label(window_ef, text='Enter New Password', bg='#BBD0FF', fg='#040405',
                                             font=("Comic Sans MS", 11, 'italic'))
            employee_forget_password.place(x=175, y=190)
            employee_forget_password_rec = Entry(window_ef, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                                 highlightthickness=2, textvariable=employee_password_forget,
                                                 show="", font=("Comic Sans MS", 11, 'italic'))
            employee_forget_password_rec.place(x=150, y=220)


            # REENTER PASSWORD ICON
            employee_fp_icon_2 = Image.open('images\\key.png')
            employee_fp_resize_2 = employee_fp_icon_2.resize((15, 15))
            employee_fp_photo_2 = ImageTk.PhotoImage(employee_fp_resize_2)
            employee_fp_place_2 = Label(window_ef, image=employee_fp_photo_2, bg='#BBD0FF')
            employee_fp_place_2.image = employee_fp_photo_2
            employee_fp_place_2.place(x=150, y=260)

            # REENTER PASSWORD
            employee_forget_password_2 = Label(window_ef, text='Reset Password', bg='#BBD0FF', fg='#040405',
                                               font=("Comic Sans MS", 11, 'italic'))
            employee_forget_password_2.place(x=185, y=255)
            employee_forget_password_rec_2 = Entry(window_ef, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                                   highlightthickness=2, textvariable=employee_reenter_password,
                                                   show="", font=("Comic Sans MS", 11, 'italic'))
            employee_forget_password_rec_2.place(x=150, y=285)

            def update_employee_password():
                check_counter_employee = 0
                message = ''

                if employee_forget_username_rec.get() == '':
                    message = 'Please enter username'

                else:
                    check_counter_employee += 1

                if employee_forget_password_rec.get() == '':
                    message = 'Please enter password'

                else:
                    if not any(fpa.isdigit() for fpa in employee_forget_password_rec.get()):
                        message = 'Require at least 1 numeral in password'

                    elif not any(fpa.islower() for fpa in employee_forget_password_rec.get()):
                        message = 'Require at least 1 lowercase character in password'

                    elif not any(fpa.isupper() for fpa in employee_forget_password_rec.get()):
                        message = 'Require at least 1 uppercase character in password'

                    else:
                        check_counter_employee += 1

                if employee_forget_password_rec_2.get() == '':
                    message = 'Please reenter password'

                else:
                    check_counter_employee += 1

                if check_counter_employee == 3:
                    try:
                        conn = sqlite3.connect('database/DnetPower.db')
                        cursor = conn.cursor()
                        found_user = 'SELECT * FROM Employee_Account WHERE employee_username = ?'
                        cursor.execute(found_user, [(employee_forget_username_rec.get())])

                        result = cursor.fetchall()

                        if result:
                            if employee_forget_password_rec.get() == employee_forget_password_rec_2.get():
                                key = b'qVnbM24duboqndhyHznH9hrd5IqLl5PjD8fspYKGI8Y='
                                fernet = Fernet(key)
                                hashed = fernet.encrypt(employee_forget_password_rec.get().encode())
                                print(hashed)
                                connect = sqlite3.connect('database/DnetPower.db')
                                curs = connect.cursor()
                                update = 'update Employee_Account set employee_password=? WHERE employee_username =? '
                                curs.execute(update, [hashed, employee_forget_username_rec.get(), ])
                                connect.commit()
                                connect.close()
                                messagebox.showinfo('Congrats', 'Password changed successfully')
                                window_ef.destroy()

                            else:
                                messagebox.showerror('Error!', "Passwords didn't match")

                        else:
                            messagebox.showerror("Update Password Status", "Username didn't exist.\n\nPlease try "
                                                                           "again !")

                    except Exception as ep:
                        messagebox.showerror('', ep)

                else:
                    messagebox.showerror('Sign Up Status', message)

            # SUBMIT BUTTON
            employee_forget_button = Button(window_ef, text='Reset', font=("Comic Sans MS", 11, 'italic'),
                                            bg='black', fg='white', activebackground='white', width=25, border=0, cursor='hand2',
                                            justify=CENTER, command=lambda: update_employee_password())
            employee_forget_button.place(x=140, y=370)

        # FORGET PASSWORD
        employee_forget_pass_button = Button(login_account_employee_page, text="Forget Password",
                                             font=("Comic Sans MS", 10, 'italic'),
                                             bg='#BBD0FF', fg='black', activebackground='#BBD0FF', width=25, border=0,
                                             cursor='hand2', justify=CENTER,
                                             command=lambda: employee_forget_password_page())
        employee_forget_pass_button.place(x=155, y=450)

        # ==================================================================== SEPARATE LINE

        # LOGIN ADMIN BACKGROUND COLOR
        login_account_admin_page['bg'] = '#BBD0FF'

        # BACK TO PREVIOUS PAGE BUTTON
        back_img = Image.open('images\\back.png')
        back_img_resize = back_img.resize((30, 30))
        back_photo = ImageTk.PhotoImage(back_img_resize)
        back_photo_place = Button(login_account_admin_page, image=back_photo, bg='#BBD0FF', activebackground='#BBD0FF',
                                  cursor='hand2',
                                  border=0, command=lambda: show_frame(select_account_page))
        back_photo_place.image = back_photo
        back_photo_place.place(relx=0.02, rely=0.02, anchor='nw')
        # ad_back_previous.place(x=100, y=20)

        # LOGIN FORM
        login = LabelFrame(login_account_admin_page, bg="#BBD0FF", width='300', height=450)
        login.place(x=105, y=85)

        # LOGIN BLOCK
        wel = "Welcome to Dnet Power"
        top = Label(login_account_admin_page, text=wel, font=("Comic Sans MS", 15, 'italic'),
                    bg='#BBD0FF', fg='#040405')
        top.place(x=140, y=100)

        # SHOW MANAGER PAGE
        def admin_page():
            root.destroy()
            filename = 'admin.py'
            os.system(filename)

        # DATABASE
        User = StringVar()
        Password = StringVar()

        def login_database():
            try:
                conn = sqlite3.connect('./database/DnetPower.db')
                cursor = conn.cursor()
                find_pass = 'SELECT admin_password FROM Admin_Account'
                cursor.execute(find_pass)
                pass_result = cursor.fetchall()
                print(pass_result)
                new = [item for t in pass_result for item in t]
                print(f"Test {new}")
                key = b'qVnbM24duboqndhyHznH9hrd5IqLl5PjD8fspYKGI8Y='
                fernet = Fernet(key)
                for i in new:
                    decoded2 = fernet.decrypt(i)
                    decoded2 = str(decoded2.decode("utf-8").strip())
                    # print(f"decoded {i} {decoded}")
                conn = sqlite3.connect('./database/DnetPower.db')
                cursor = conn.cursor()
                find_user = 'SELECT * FROM Admin_Account WHERE admin_username = ?'
                cursor.execute(find_user, [(u_rec.get()),])

                result = cursor.fetchall()

                if result:
                    if decoded2 == p_rec.get():
                        messagebox.showinfo("Login Status", 'Logged in Successfully.\n\nClick "OK" to continue.')
                        admin_page()
                    else:
                        messagebox.showerror("Login Status", 'Password not match.')
                else:
                    messagebox.showerror("Login Status", "Logged in Failed.\n\nUser doesn't exist !")

            except Exception as ep:
                messagebox.showerror('', ep)

        # USER
        def enter(e):
            u_rec.delete(0, 'end')

        def leave(e):
            name = u_rec.get()
            if name == '':
                u_rec.insert(0, 'Enter Username')

        user = "Uername"
        u_label = Label(login_account_admin_page, text=user, font=("Comic Sans MS", 11, 'italic'),
                        bg='#BBD0FF', fg='#040405')
        u_label.place(x=160, y=180)

        u_rec = Entry(login_account_admin_page, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                      font=("Comic Sans MS", 11, 'italic'), textvariable=User)
        u_rec.insert(0, 'Enter Username')
        u_rec.bind('<FocusIn>', enter)
        u_rec.bind('<FocusOut>', leave)
        u_rec.place(x=135, y=210)

        # USER ICON
        u_icon = Image.open('images\\user.png')
        u_resize = u_icon.resize((20, 20))
        user_photo = ImageTk.PhotoImage(u_resize)
        user_icon = Label(login_account_admin_page, image=user_photo, bg='#BBD0FF')
        user_icon.image = user_photo
        user_icon.place(x=135, y=180)

        # PASSWORD
        def enter(e):
            p_rec.delete(0, 'end')

        def leave(e):
            name = p_rec.get()
            if name == '':
                p_rec.insert(0, 'Enter Password')

        secret = "Password"
        p_label = Label(login_account_admin_page, text=secret, font=("Comic Sans MS", 11, 'italic'),
                        bg='#BBD0FF', fg='#040405')
        p_label.place(x=165, y=260)

        p_rec = Entry(login_account_admin_page, width=22, fg='#5a5a5a', relief=GROOVE, border=2, bg='white',
                      font=("Comic Sans MS", 11, 'italic'), textvariable=Password)
        p_rec.insert(0, 'Enter Password')
        p_rec.bind('<FocusIn>', enter)
        p_rec.bind('<FocusOut>', leave)
        p_rec.place(x=135, y=290)

        # PASSWORD ICON
        password_icon = Image.open('images\\padlock.png')
        password_resize = password_icon.resize((21, 20))
        password_photo = ImageTk.PhotoImage(password_resize)
        password_place = Label(login_account_admin_page, image=password_photo, bg='#BBD0FF')
        password_place.image = password_photo
        password_place.place(x=135, y=260)

        # SHOW/HIDE PASSWORD
        def show_password2():
            if p_rec.cget('show') == "•":
                p_rec.config(show="")

            else:
                p_rec.config(show="•")

        show_pass2 = Checkbutton(login_account_admin_page, bg='#BBD0FF', activebackground='#BBD0FF',
                                 command=show_password2,
                                 cursor='hand2')
        show_pass2.select()
        show_pass2.place(x=350, y=291)

        # LOGIN BUTTON
        login_button = Button(login_account_admin_page, text="LOGIN", font=("Comic Sans MS", 11, 'italic'),
                              bg='black', fg='white', activebackground='white', width=25, border=0, cursor='hand2',
                              justify=CENTER, command=login_database)
        login_button.place(x=135, y=370)

        # SEPARATE LINE
        alr_create_word = Label(login_account_admin_page, text="Do not have an account?",
                                font=("Comic Sans MS", 8, 'italic'), bg='#BBD0FF',
                                fg='#696969')
        alr_create_word.place(x=120, y=424)

        # CREATE ACCOUNT BUTTON
        create_button = Button(login_account_admin_page, text="Create New Account",
                               font=("Comic Sans MS", 10, 'italic'),
                               bg='#BBD0FF', fg='black', activebackground='#BBD0FF', width=18, border=0, cursor='hand2',
                               justify=CENTER, command=lambda: show_frame(create_account_page))
        create_button.place(x=250, y=420)

        # ================================================= SEPARATE LINE ==============================================

        # ADMIN FORGET PAGE WINDOW
        def forget_password_page():
            window = Toplevel(root)
            window_width = 500
            window_height = 500
            forget_page_screen_width = window.winfo_screenwidth()
            forget_page_screen_height = window.winfo_screenheight()
            p_x = int(forget_page_screen_width / 2) - (window_width / 2)
            p_y = int(forget_page_screen_height / 2.5) - (window_height / 2.5)
            window.geometry("%dx%d+%d+%d" % (window_width, window_height, p_x, p_y))
            window.title('Forgot Password')
            window['bg'] = '#BBD0FF'
            window.resizable(0, 0)
            window.grab_set()

            # FORGET PASSWORD
            forget_frame = LabelFrame(window, bg="#BBD0FF", width='400', height=400)
            forget_frame.place(x=55, y=55)

            forget_word = Label(window, text='Reset Password', font=("Comic Sans MS", 15, 'italic'),
                                bg='#BBD0FF', fg='#040405')
            forget_word.place(x=180, y=65)

            def show_password3():
                if forget_password_rec.cget('show') == "":
                    forget_password_rec.config(show="•")
                    forget_password_rec_2.config(show="•")

                else:
                    forget_password_rec.config(show="")
                    forget_password_rec_2.config(show="")

            show_pass3 = Checkbutton(window, text='Show Password', font=("Comic Sans MS", 11, 'italic'),
                                     bg='#BBD0FF', activebackground='#BBD0FF',
                                     command=show_password3,
                                     cursor='hand2')
            show_pass3.select()
            show_pass3.place(x=150, y=320)

            # FORGET PASSWORD LINK WITH DATABASE

            username_forget = StringVar()
            password_forget = StringVar()
            reenter_password = StringVar()

            # USERNAME & PASSWORD & REENTER PASSWORD
            # USERNAME ICON
            fu_icon = Image.open('images\\user.png')
            fu_resize = fu_icon.resize((15, 15))
            forget_user_photo = ImageTk.PhotoImage(fu_resize)
            forget_user_icon = Label(window, image=forget_user_photo, bg='#BBD0FF')
            forget_user_icon.image = forget_user_photo
            forget_user_icon.place(x=150, y=130)

            # USERNAME
            forget_page_user = Label(window, text='Enter Username', bg='#BBD0FF', fg='#040405',
                                     font=("Comic Sans MS", 11, 'italic'))
            forget_page_user.place(x=175, y=125)

            forget_username_rec = Entry(window, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                        highlightthickness=2, textvariable=username_forget,
                                        font=("Comic Sans MS", 11, 'italic'))
            forget_username_rec.place(x=150, y=155)

            # PASSWORD ICON
            fp_icon = Image.open('images\\padlock.png')
            fp_resize = fp_icon.resize((17, 17))
            fp_photo = ImageTk.PhotoImage(fp_resize)
            fp_place = Label(window, image=fp_photo, bg='#BBD0FF')
            fp_place.image = fp_photo
            fp_place.place(x=150, y=193)

            # PASSWORD
            forget_password = Label(window, text='Enter New Password', bg='#BBD0FF', fg='#040405',
                                    font=("Comic Sans MS", 11, 'italic'))
            forget_password.place(x=175, y=190)
            forget_password_rec = Entry(window, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                        highlightthickness=2, textvariable=password_forget,
                                        show="", font=("Comic Sans MS", 11, 'italic'))
            forget_password_rec.place(x=150, y=220)

            # REENTER PASSWORD ICON
            fp_icon_2 = Image.open('images\\key.png')
            fp_resize_2 = fp_icon_2.resize((15, 15))
            fp_photo_2 = ImageTk.PhotoImage(fp_resize_2)
            fp_place_2 = Label(window, image=fp_photo_2, bg='#BBD0FF')
            fp_place_2.image = fp_photo_2
            fp_place_2.place(x=150, y=260)

            # REENTER PASSWORD
            forget_password_2 = Label(window, text='Reset Password', bg='#BBD0FF', fg='#040405',
                                      font=("Comic Sans MS", 11, 'italic'))
            forget_password_2.place(x=175, y=255)
            forget_password_rec_2 = Entry(window, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                          highlightthickness=2, textvariable=reenter_password,
                                          show="", font=("Comic Sans MS", 11, 'italic'))
            forget_password_rec_2.place(x=150, y=285)

            def update_password():
                check_counter = 0
                msg = ''

                if forget_username_rec.get() == '':
                    msg = 'Please enter username'

                else:
                    check_counter += 1

                if forget_password_rec.get() == '':
                    msg = 'Please enter password'

                else:
                    if not any(fpa.isdigit() for fpa in forget_password_rec.get()):
                        msg = 'Require at least 1 numeral in password'

                    elif not any(fpa.islower() for fpa in forget_password_rec.get()):
                        msg = 'Require at least 1 lowercase character in password'

                    elif not any(fpa.isupper() for fpa in forget_password_rec.get()):
                        msg = 'Require at least 1 uppercase character in password'

                    else:
                        check_counter += 1

                if forget_password_rec_2.get() == '':
                    msg = 'Please reenter password'

                else:
                    check_counter += 1

                if check_counter == 3:
                    try:
                        conn = sqlite3.connect('database/DnetPower.db')
                        cursor = conn.cursor()
                        found_user = 'SELECT * FROM Admin_Account WHERE admin_username = ?'
                        cursor.execute(found_user, [(forget_username_rec.get())])

                        result = cursor.fetchall()

                        if result:
                            if forget_password_rec.get() == forget_password_rec_2.get():
                                key = b'qVnbM24duboqndhyHznH9hrd5IqLl5PjD8fspYKGI8Y='
                                fernet = Fernet(key)
                                hashed2 = fernet.encrypt(forget_password_rec.get().encode())
                                print(hashed2)
                                connect = sqlite3.connect('database/DnetPower.db')
                                curs = connect.cursor()
                                update = 'update Admin_account set admin_password=? WHERE admin_username=? '
                                curs.execute(update, [hashed2, forget_username_rec.get(), ])
                                connect.commit()
                                connect.close()
                                messagebox.showinfo('Congrats', 'Password changed successfully')
                                window.destroy()

                            else:
                                messagebox.showerror('Error!', "Passwords didn't match")

                        else:
                            messagebox.showerror("Update Password Status", "Username didn't exist.\n\nPlease try "
                                                                           "again !")

                    except Exception as ep:
                        messagebox.showerror('', ep)

                else:
                    messagebox.showerror('Sign Up Status', msg)

            # SUBMIT BUTTON
            forget_button = Button(window, text='Reset', font=("Comic Sans MS", 11, 'italic'),
                                   bg='black', fg='white', activebackground='white', width=25, border=0, cursor='hand2',
                                   justify=CENTER, command=lambda: update_password())
            forget_button.place(x=140, y=370)

        # FORGET PASSWORD
        forget_pass_button = Button(login_account_admin_page, text="Forget Password",
                                    font=("Comic Sans MS", 10, 'italic'),
                                    bg='#BBD0FF', fg='black', activebackground='#BBD0FF', width=25, border=0,
                                    cursor='hand2',
                                    justify=CENTER, command=lambda: forget_password_page())
        forget_pass_button.place(x=135, y=450)

        # ================================================= SEPARATE LINE ==============================================

        # CREATE ACCOUNT PAGE
        create_account_page['bg'] = '#BBD0FF'

        # CREATE ACCOUNT FRAME
        create_frame = LabelFrame(create_account_page, bg="#BBD0FF", width=300, height=550)
        create_frame.place(x=105, y=28)

        # CREATE ACCOUNT HEADING
        create_top = Label(create_account_page, text='Create Your Account', font=("Comic Sans MS", 15, 'italic'),
                           bg='#BBD0FF')
        create_top.place(x=160, y=38)

        # CONNECT DATABASE
        name = StringVar()
        username_input_c = StringVar()
        password_input_c = StringVar()
        contact_input_c = StringVar()
        email_input_c = StringVar()

        def create_acc_database():
            character = ['@', '.']
            counter = 0
            empty = ''

            try:
                con = sqlite3.connect('database/DnetPower.db')
                c = con.cursor()
                for row in c.execute("Select * from Employee_Account"):
                    usn = row[2]

            except Exception as ep:
                messagebox.showerror('', ep)

            if create_name_rec.get() == "":
                empty = "Please enter full name"

            else:
                if len(create_name_rec.get()) <= 2:
                    empty = 'Name is too short'

                elif len(create_name_rec.get()) >= 30:
                    empty = 'Name is too long'

                elif any(n.isdigit() for n in create_name_rec.get()):
                    empty = 'Name should not have numbers'

                else:
                    counter += 1

            if create_username_rec.get() == "":
                empty = "Please enter username"

            elif create_username_rec.get() == usn:
                empty = "Select another account"

            else:
                counter += 1

            if create_password_rec.get() == "":
                empty = "Please enter password"

            else:
                if not any(pa.isdigit() for pa in create_password_rec.get()):
                    empty = 'Require at least 1 numeral in password'

                elif not any(pa.islower() for pa in create_password_rec.get()):
                    empty = 'Require at least 1 lowercase character in password'

                elif not any(pa.isupper() for pa in create_password_rec.get()):
                    empty = 'Require at least 1 uppercase character in password'

                else:
                    print(create_password_rec.get())
                    counter += 1

            if create_contact_rec.get() == "":
                empty = "Please enter contact number"

            else:
                if len(create_contact_rec.get()) <= 9:
                    empty = 'Contact Number too short'

                elif len(create_contact_rec.get()) >= 13:
                    empty = 'Contact Number too long'

                elif not any(contact.isdigit() for contact in create_contact_rec.get()):
                    empty = 'Contact number must be in an integer'

                else:
                    counter += 1

            if create_email_rec.get() == "":
                empty = "Please enter email"

            else:
                # Validate Email
                try:
                    if not any(ch in character for ch in create_email_rec.get()):
                        empty = "Please enter correct format of email"

                    else:
                        counter += 1

                except Exception as ep:
                    messagebox.showerror('', ep)

            if counter == 5:
                try:
                    key = b'qVnbM24duboqndhyHznH9hrd5IqLl5PjD8fspYKGI8Y='
                    fernet = Fernet(key)
                    #test_str = "ABCDEFG"
                    hashed3 = fernet.encrypt(create_password_rec.get().encode())
                    # hashed3 = fernet.encrypt(test_str.encode())
                    print(hashed3)

                    connection = sqlite3.connect("./database/DnetPower.db")
                    cur = connection.cursor()
                    cur.execute(
                        "INSERT INTO Employee_Account(employee_name, employee_username, employee_password, employee_contact, "
                        "employee_email) VALUES(?,?,?,?,?)",
                        (name.get(), username_input_c.get(), hashed3, contact_input_c.get(),
                         email_input_c.get()))

                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Sign Up Status", 'Create account successfully\n\n Click "OK" to continue')
                    account_page()

                except Exception as ex:
                    messagebox.showerror('', ex)

            else:
                messagebox.showerror('Sign Up Status', empty)

        # NAME ICON
        n_icon = Image.open('images\\name.png')
        n_resize = n_icon.resize((17, 17))
        name_photo = ImageTk.PhotoImage(n_resize)
        name_icon = Label(create_account_page, image=name_photo, bg='#BBD0FF')
        name_icon.image = name_photo
        name_icon.place(x=120, y=93)

        # NAME
        create_name = Label(create_account_page, text='Enter name', bg='#BBD0FF', fg='#040405',
                            font=("Comic Sans MS", 11, 'italic'))
        create_name.place(x=145, y=90)
        create_name_rec = Entry(create_account_page, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                font=("Comic Sans MS", 11, 'italic'), highlightthickness=2, textvariable=name)
        create_name_rec.place(x=120, y=120)

        # USERNAME ICON
        u_icon = Image.open('images\\user.png')
        u_resize = u_icon.resize((15, 15))
        user_photo = ImageTk.PhotoImage(u_resize)
        user_icon = Label(create_account_page, image=user_photo, bg='#BBD0FF')
        user_icon.image = user_photo
        user_icon.place(x=120, y=155)

        # USERNAME
        create_user = Label(create_account_page, text='Enter username', bg='#BBD0FF', fg='#040405',
                            font=("Comic Sans MS", 11, 'italic'))
        create_user.grid(row=1, column=0, sticky='news', padx=145, pady=150)

        create_username_rec = Entry(create_account_page, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                    highlightthickness=2, font=("Comic Sans MS", 11, 'italic'),
                                    textvariable=username_input_c)
        create_username_rec.place(x=120, y=180)

        # PASSWORD ICON
        password_icon = Image.open('images\\padlock.png')
        password_resize = password_icon.resize((17, 16))
        password_photo = ImageTk.PhotoImage(password_resize)
        password_place = Label(create_account_page, image=password_photo, bg='#BBD0FF')
        password_place.image = password_photo
        password_place.place(x=120, y=215)

        # SHOW PASSWORD IN CREATE PAGE
        def show_password4():
            if create_password_rec.cget('show') == "":
                create_password_rec.config(show="•")

            else:
                create_password_rec.config(show="")

        # SHOW PASSWORD
        show_pass4 = Checkbutton(create_account_page, bg='#BBD0FF', activebackground='#BBD0FF', command=show_password4,
                                 cursor='hand2')
        show_pass4.select()
        show_pass4.place(x=340, y=240)

        # PASSWORD
        create_password = Label(create_account_page, text='Enter Password', bg='#BBD0FF', fg='#040405',
                                font=("Comic Sans MS", 11, 'italic'))
        create_password.place(x=145, y=210)
        create_password_rec = Entry(create_account_page, width=22, fg='#5a5a5a', relief=GROOVE, bg='white', show="",
                                    highlightthickness=2, font=("Comic Sans MS", 11, 'italic'),
                                    textvariable=password_input_c)
        create_password_rec.place(x=120, y=240)

        # CONTACT NUMBER ICON
        contact_icon = Image.open('images\\contact.png')
        contact_resize = contact_icon.resize((17, 16))
        contact_photo = ImageTk.PhotoImage(contact_resize)
        contact_place = Label(create_account_page, image=contact_photo, bg='#BBD0FF')
        contact_place.image = contact_photo
        contact_place.place(x=120, y=275)

        # CONTACT NUMBER
        create_contact = Label(create_account_page, text='Enter Contact Number', bg='#BBD0FF', fg='#040405',
                               font=("Comic Sans MS", 11, 'italic'))
        create_contact.place(x=145, y=270)
        create_contact_rec = Entry(create_account_page, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                   highlightthickness=2, font=("Comic Sans MS", 11, 'italic'),
                                   textvariable=contact_input_c)
        create_contact_rec.place(x=120, y=300)

        # EMAIL ICON
        email_icon = Image.open('images\\email.png')
        email_resize = email_icon.resize((17, 16))
        email_photo = ImageTk.PhotoImage(email_resize)
        email_place = Label(create_account_page, image=email_photo, bg='#BBD0FF')
        email_place.image = email_photo
        email_place.place(x=120, y=345)

        # EMAIL
        create_email = Label(create_account_page, text='Enter Email', bg='#BBD0FF', fg='#040405',
                             font=("Comic Sans MS", 11, 'italic'))
        create_email.place(x=145, y=340)
        create_email_rec = Entry(create_account_page, width=22, fg='#5a5a5a', relief=GROOVE, bg='white',
                                 highlightthickness=2, font=("Comic Sans MS", 11, 'italic'),
                                 textvariable=email_input_c)
        create_email_rec.place(x=120, y=370)

        # CREATE BUTTON
        create_button = Button(create_account_page, text='Create Account', font=("Comic Sans MS", 11, 'italic'),
                               bg='black', fg='white', activebackground='white', width=25, border=0, cursor='hand2',
                               justify=CENTER, command=create_acc_database)
        create_button.place(x=140, y=430)

        # SEPARATE LINE
        middle_line = Canvas(create_account_page, width=270, height=1.5, bg="#696969", highlightthickness=0)
        middle_line.place(x=120, y=490)
        alr_create_word = Label(create_account_page, text='Already have an account ?',
                                font=("Comic Sans MS", 11, 'italic'), bg='#BBD0FF',
                                fg='#696969')
        alr_create_word.place(x=160, y=475)

        # LOGIN BUTTON
        login_button = Button(create_account_page, text="LOGIN", font=("Comic Sans MS", 11, 'italic'),
                              bg='black', fg='white', activebackground='white', width=25, border=0, cursor='hand2',
                              justify=CENTER, command=lambda: show_frame(login_account_admin_page))
        login_button.place(x=140, y=510)

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
