import sys
import os
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "crash_log.txt")


def _log(msg):
    """Write a checkpoint to crash_log.txt (next to the script). Even if
    the app dies in a way Python can't catch as a normal exception (e.g.
    a native Tcl/Tk failure), this file shows exactly how far it got —
    so a crash can never again give 'no error, no clue'."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass


try:
    open(LOG_PATH, "w", encoding="utf-8").close()  # fresh log each run
except Exception:
    pass

_log("[1] Script started, standard-library imports OK.")

try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import pandas as pd
    from PIL import Image, ImageTk
    import customtkinter as ctk
    _log("[2] Third-party imports OK (tkinter, PIL, pandas, customtkinter).")
except Exception:
    _log("[2] FAILED during imports:\n" + traceback.format_exc())
    traceback.print_exc()
    input(
        "\nThe app failed to start — a required package is likely missing "
        "or not installed for this Python.\n"
        "Try running:  pip install pillow pandas customtkinter openpyxl\n"
        f"Full details saved to:\n{LOG_PATH}\n"
        "Press Enter to close this window..."
    )
    sys.exit(1)


def asset(filename):
    return os.path.join(BASE_DIR, filename)


def load_photo(filename, size=None):
    """Load an image next to the script. Returns a PhotoImage, or None
    (with a visible error popup) if the file is missing or unreadable —
    instead of letting the whole app crash silently."""
    path = asset(filename)
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        _log(f"[image] MISSING: {path}")
        messagebox.showerror(
            'Missing file',
            f"Couldn't find:\n{path}\n\n"
            f"Make sure '{filename}' is in the same folder as DMX_working.py."
        )
        return None
    except Exception as e:
        _log(f"[image] FAILED to load {path}: {e}")
        messagebox.showerror('Image error', f"Couldn't load {filename}:\n{e}")
        return None


_log("[3] About to create the main window (Tk())...")
try:
    root = Tk()
    _log("[4] Main window created OK.")
except Exception:
    _log("[4] FAILED creating the main window:\n" + traceback.format_exc())
    traceback.print_exc()
    input(f"\nCouldn't create the app window. Full details saved to:\n{LOG_PATH}\nPress Enter to close...")
    sys.exit(1)

root.title('Dubai Municipality')
root.geometry('1000x600')
root.resizable(False, False)
root.attributes('-topmost', True)
icon_path = asset("scale.ico")
_log(f"[5] About to set window icon from: {icon_path}")
try:
    root.iconbitmap(icon_path)
    _log("[5] Icon loaded OK.")
except Exception as e:
    _log(f"[5] Icon failed to load (non-fatal, continuing): {e}")
    print(f"Warning: couldn't load icon at {icon_path} ({e}). Continuing without it.")


def logout():
    for widget in root.winfo_children():
        widget.destroy()
    login()


def login():
    root.configure(bg='white')
    labelziad = Label(root, text='Desigend and Created by Zeyad Mohamed', bg='white')
    labelziad.place(relx=0.75, rely=0.95)

    logo_photo = load_photo("unnamed.png", (300, 80))
    if logo_photo:
        logo_label = Label(root, image=logo_photo, bg='white')
        logo_label.place(relx=1.0, y=0, anchor='ne')  # Top-right corner
        logo_label.image = logo_photo

    global img
    img = load_photo("login.png")
    if img:
        Label(root, image=img, bg='white').place(x=60, y=120)

    frame = Frame(root, width=350, height=350, bg='white')
    frame.place(x=480, y=70)

    heading = Label(frame, text='sign in', fg='#57a1f8', bg='white', font=('Microsoft Yahwei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    def signin():
        username = user.get()
        user_password = password.get()
        if username == 'ziad' and user_password == 'dubai':
            main()
        else:
            messagebox.showerror('Error', 'Invalid Username or Password, Application terminated.')
            exit()

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username: ')

    def on_enter_password(e):
        password.delete(0, 'end')

    def on_leave_password(e):
        password.insert(0, 'Password: ')

    user = Entry(frame, width=25, fg='black', border=0, font=('Microsoft Yahwei UI Light', 11))
    user.place(x=30, y=130)
    user.insert(0, 'Username: ')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=157)

    password = Entry(frame, width=25, fg='black', border=0, font=('Microsoft Yahwei UI Light', 11))
    password.place(x=30, y=180)
    password.insert(0, 'Password: ')
    password.bind('<FocusIn>', on_enter_password)
    password.bind('<FocusOut>', on_leave_password)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=207)

    Button(frame, width=39, pady=7, text='Sign in', bg="#57a1f8", fg='white', border=0, command=signin).place(x=35,
                                                                                                              y=235)
    label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsfot YaHei UI Light', 9))
    label.place(x=75, y=290)
    sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8')
    sign_up.place(x=215, y=290)


def main():
    for widget in root.winfo_children():
        widget.destroy()
    logo_photo = load_photo("happy.png", (400, 300))
    if logo_photo:
        logo_label = Label(root, image=logo_photo, bg='white')
        logo_label.place(relx=0.01, y=325)  # Top-right corner
        logo_label.image = logo_photo

    global label1, label2
    root.config(bg='white')
    label1 = Label(root, text='Human Resource Department', fg='black', bg='white',
                   font=('Microsoft Yahwei UI Light', 17, 'bold'))
    label1.place(relx=0.34, rely=0.1)
    label2 = Label(root, text='Youth Development Program', fg='darkblue', bg='white',
                   font=('Microsoft Yahwei UI Light', 17, 'bold'))
    label2.place(relx=0.34, rely=0.2)

    logo_photo2 = load_photo("unnamed.png", (300, 80))
    if logo_photo2:
        logo_label2 = Label(root, image=logo_photo2, bg='white')
        logo_label2.place(relx=1.0, y=0, anchor='ne')  # Top-right corner
        logo_label2.image = logo_photo2

    labelziad = Label(root, text='Desigend and Created by Zeyad Mohamed', bg='white')
    labelziad.place(relx=0.75, rely=0.95)
    btns()


def back():
    for widget in root.winfo_children():
        widget.destroy()
    main()
    btns()


def open_units_page():
    for widget in root.winfo_children():
        widget.destroy()

    global label3, label4, label5, label6, label7, label18, label19, label19, label20, label21, label22, label23, label24, label25, label26, label27, btn9
    labelziad = Label(root, text='Desigend and Created by Zeyad Mohamed', bg='white')
    labelziad.place(relx=0.75, rely=0.95)
    logo_photo = load_photo("unnamed.png", (300, 80))
    if logo_photo:
        logo_label = Label(root, image=logo_photo, bg='white')
        logo_label.place(relx=1.0, y=0, anchor='ne')  # Top-right corner
        logo_label.image = logo_photo
    labe3 = Label(root, text='Organisational Units/Needs Gathering', bg='white', font=('bold 15'), padx=10, pady=10,
                  fg='#0A6DD3')
    labe3.pack()
    label4 = Label(root, text='Enviromental Sustainability Department', bg='white', font=('bold 15'), padx=11, pady=11,
                   fg='#0A6DD3')
    label4.pack()
    btn8 = ttk.Button(root, text="Back", command=back)
    btn8.place(relx=0.36, rely=0.93)
    clicked = StringVar()
    options = ['select',
               '2018',
               '2019',
               '2020',
               '2021',
               '2022',
               '2023',
               ]
    clicked.set(options[0])
    drop = ttk.OptionMenu(root, clicked, *options)
    drop.place(relx=0.59, rely=0.25)
    label5 = Label(root, text='Year', bg='white')
    label5.place(relx=0.61, rely=0.21)

    clicked1 = StringVar()
    options1 = ['select',
                'Behavioral',
                'Institutional',
                'Specialized',
                ]
    clicked1.set(options1[0])
    drop = ttk.OptionMenu(root, clicked1, *options1)
    drop.place(relx=0.48, rely=0.25)
    label6 = Label(root, text='Program Type:', bg='white')
    label6.place(relx=0.49, rely=0.21)

    clicked2 = StringVar()
    options2 = ['select',
                '1st Quarter',
                '2nd Quarter',
                '3rd Quarter',
                '4th Quarter',
                ]
    clicked2.set(options2[0])
    drop = ttk.OptionMenu(root, clicked2, *options2)
    drop.place(relx=0.40, rely=0.25)
    label7 = Label(root, text='Session Quarter:', bg='white')
    label7.place(relx=0.40, rely=0.21)

    entry = ttk.Entry(root, text='test')
    entry.place(relx=0.18, rely=0.26, width=210)
    label8 = Label(root, text='Program Name:', bg='white')
    label8.place(relx=0.25, rely=0.21)

    entry1 = ttk.Entry(root, text='Stategic goal')
    entry1.place(relx=0.18, rely=0.36, width=210)
    label9 = Label(root, text='Strategic goal:', bg='white')
    label9.place(relx=0.25, rely=0.31)

    clicked3 = StringVar()
    options3 = ['select',
                'Day',
                'Night',
                ]
    clicked3.set(options3[0])
    drop = ttk.OptionMenu(root, clicked3, *options3)
    drop.place(relx=0.40, rely=0.35)
    label10 = Label(root, text='Time:', bg='white')
    label10.place(relx=0.41, rely=0.31)

    import tkinter as tk

    entry2_var = tk.StringVar()
    entry3_var = tk.StringVar()
    entry4_var = tk.StringVar()
    entry5_var = tk.StringVar()
    entry6_var = tk.StringVar()
    entry7_var = tk.StringVar()
    entry8_var = tk.StringVar()
    entry9_var = tk.StringVar()
    entry10_var = tk.StringVar()

    def convert_days_to_hours(event):
        try:
            days = float(entry2_var.get())
            hours = int(round(days * 6))
            entry3_var.set(str(hours))
        except ValueError:
            entry3_var.set("")

    entry2 = ttk.Entry(root, textvariable=entry2_var)
    entry2.place(relx=0.48, rely=0.35, width=50)
    label11 = tk.Label(root, text='Days:', bg='white')
    label11.place(relx=0.48, rely=0.31)
    entry2.bind("<FocusOut>", convert_days_to_hours)

    entry3 = ttk.Entry(root, textvariable=entry3_var, state='readonly')
    entry3.place(relx=0.55, rely=0.35, width=50)
    label12 = Label(root, text='Days are auto-converted into hours!', fg='red', bg='white')
    label12.place(relx=0.61, rely=0.34)
    label13 = tk.Label(root, text='Hours:', bg='white')
    label13.place(relx=0.55, rely=0.31)

    entry4 = ttk.Entry(root, textvariable=entry4_var)
    entry4.place(relx=0.18, rely=0.46, width=210)
    label14 = Label(root, text='Professor employment number:', bg='white')
    label14.place(relx=0.20, rely=0.41)

    clicked4 = StringVar()
    options4 = ['select',
                'Locally',
                'Abroad', ]
    clicked4.set(options4[0])
    drop = ttk.OptionMenu(root, clicked4, *options4)
    drop.place(relx=0.08, rely=0.25)
    label15 = Label(root, text='Residency:', bg='white')
    label15.place(relx=0.08, rely=0.21)

    entry4 = ttk.Entry(root, textvariable=entry5_var)
    entry4.place(relx=0.08, rely=0.36, width=60)
    label16 = Label(root, text='Country:', bg='white')
    label16.place(relx=0.08, rely=0.31)

    label17 = tk.Label(root, text='Emirate:', bg='white')
    label17.place(relx=0.08, rely=0.41)
    clicked4 = StringVar()
    options4 = ['select',
                'Dubai',
                'Sharjah',
                'Abu Dhabi',
                'Al Ain',
                'Ajman',
                'Ras Al Khaima',
                'Fujairah', ]
    clicked4.set(options4[0])
    drop = ttk.OptionMenu(root, clicked4, *options4)
    drop.place(relx=0.08, rely=0.46)

    label18 = Label(root, text='Professor:', bg='white')
    label18.place(relx=0.40, rely=0.41)
    clicked4 = StringVar()
    options4 = ['select',
                'Local',
                'Foreign'
                ]
    clicked4.set(options4[0])
    drop = ttk.OptionMenu(root, clicked4, *options4)
    drop.place(relx=0.40, rely=0.46)

    label19 = Label(root, text='Program Language:', bg='white')
    label19.place(relx=0.08, rely=0.52)
    clicked4 = StringVar()
    options4 = ['select',
                'English',
                'Arabic',
                ]
    clicked4.set(options4[0])
    drop = ttk.OptionMenu(root, clicked4, *options4)
    drop.place(relx=0.08, rely=0.57)

    clicked5 = StringVar()
    options5 = ['select',
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                ]
    clicked5.set(options5[0])
    drop = ttk.OptionMenu(root, clicked5, *options5)
    drop.place(relx=0.40, rely=0.57)
    label20 = Label(root, text='مدخلات البرنامج', bg='white')
    label20.place(relx=0.40, rely=0.52)

    label21 = Label(root, text='Program purpose(1):', bg='white')
    label21.place(relx=0.07, rely=0.66)
    entry5 = ttk.Entry(root, textvariable=entry6_var)
    entry5.place(relx=0.18, rely=0.66, width=210)

    label22 = Label(root, text='Program purpose(2):', bg='white')
    label22.place(relx=0.07, rely=0.71)
    entry6 = ttk.Entry(root, textvariable=entry7_var)
    entry6.place(relx=0.18, rely=0.71, width=210)

    entry543 = ttk.Entry(root, textvariable=entry9_var)
    entry543.place(relx=0.18, rely=0.85, width=700)
    label12 = Label(root, text='Comments:', bg='white')
    label12.place(relx=0.08, rely=0.85)

    label23 = Label(root, text='Program purpose(3):', bg='white')
    label23.place(relx=0.07, rely=0.76)
    entry7 = ttk.Entry(root, textvariable=entry8_var)
    entry7.place(relx=0.18, rely=0.76, width=210)

    def save_to_excel():
        data = {
            'Days': [entry2_var.get()],
            'Hours': [entry3_var.get()],
            'Program Name': [entry.get()],
            'Strategic Goal': [entry1.get()],
            'Professor Employment Number': [entry4_var.get()],
            'Residency': [clicked4.get()],
            'Country': [entry5_var.get()],
            'Emirate': [clicked4.get()],
            'Professor': [clicked4.get()],
            'Program Language': [clicked4.get()],
            'مدخلات البرنامج': [clicked5.get()],
            'Program Purpose(1)': [entry6_var.get()],
            'Program Purpose(2)': [entry7_var.get()],
            'Program Purpose(3)': [entry8_var.get()]
        }

        df = pd.DataFrame(data)
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        file_path = os.path.join(desktop_path, 'program_data.xlsx')
        df.to_excel(file_path, index=False)
        print("Data saved to 'program_data.xlsx'")

    save_button = ttk.Button(root, text="Save to Excel", command=save_to_excel)
    save_button.place(relx=0.46, rely=0.93)

    Label_page = Label(root, text='1', bg='white')
    Label_page.place(relx=0.05, rely=0.95)

    def next():
        for widget in root.winfo_children():
            widget.destroy()
        Label_page = Label(root, text='2', bg='white')
        Label_page.place(relx=0.05, rely=0.95)
        labelziad = Label(root, text='Desigend and Created by Zeyad Mohamed', bg='white')
        labelziad.place(relx=0.75, rely=0.95)
        logo_photo = load_photo("unnamed.png", (300, 80))
        if logo_photo:
            logo_label = Label(root, image=logo_photo, bg='white')
            logo_label.place(relx=1.0, y=0, anchor='ne')  # Top-right corner
            logo_label.image = logo_photo
        button_back = ttk.Button(root, text='Back', command=back_again)
        button_back.place(relx=0.46, rely=0.93)

    button = ttk.Button(root, text='Next', command=next)
    button.place(relx=0.56, rely=0.93)

    def back_again():
        global label28, label29, label30, label31, label32, label33, label34, label35, label36, label37, label38, label39, label40, label41, label42, label43, label44
        for widget in root.winfo_children():
            widget.destroy()
        labelziad = Label(root, text='Desigend and Created by Zeyad Mohamed', bg='white')
        labelziad.place(relx=0.75, rely=0.95)
        logo_photo = load_photo("unnamed.png", (300, 80))
        if logo_photo:
            logo_label = Label(root, image=logo_photo, bg='white')
            logo_label.place(relx=1.0, y=0, anchor='ne')  # Top-right corner
            logo_label.image = logo_photo
        label24 = Label(root, text='Organisational Units/Needs Gathering', font=('bold 15'), padx=10, pady=10,
                        fg='#0A6DD3', bg='white')
        label24.pack()
        label24 = Label(root, text='Enviromental Sustainability Department', font=('bold 15'), padx=11, pady=11,
                        fg='#0A6DD3', bg='white')
        label24.pack()
        btn9 = ttk.Button(root, text="Back", command=back)
        btn9.place(relx=0.36, rely=0.93)
        clicked = StringVar()
        options = ['select',
                   '2018',
                   '2019',
                   '2020',
                   '2021',
                   '2022',
                   '2023',
                   ]
        clicked.set(options[0])
        drop = ttk.OptionMenu(root, clicked, *options)
        drop.place(relx=0.59, rely=0.25)
        label25 = Label(root, text='Year', bg='white')
        label25.place(relx=0.61, rely=0.21)

        clicked1 = StringVar()
        options1 = ['select',
                    'Behavioral',
                    'Institutional',
                    'Specialized',
                    ]
        clicked1.set(options1[0])
        drop = ttk.OptionMenu(root, clicked1, *options1)
        drop.place(relx=0.48, rely=0.25)
        label26 = Label(root, text='Program Type:', bg='white')
        label26.place(relx=0.49, rely=0.21)

        clicked2 = StringVar()
        options2 = ['select',
                    '1st Quarter',
                    '2nd Quarter',
                    '3rd Quarter',
                    '4th Quarter',
                    ]
        clicked2.set(options2[0])
        drop = ttk.OptionMenu(root, clicked2, *options2)
        drop.place(relx=0.40, rely=0.25)
        label27 = Label(root, text='Session Quarter:', bg='white')
        label27.place(relx=0.40, rely=0.21)

        entry = ttk.Entry(root, text='test')
        entry.place(relx=0.18, rely=0.26, width=210)
        label28 = Label(root, text='Program Name:', bg='white')
        label28.place(relx=0.25, rely=0.21)

        entry1 = ttk.Entry(root, text='Stategic goal')
        entry1.place(relx=0.18, rely=0.36, width=210)
        label29 = Label(root, text='Strategic goal:', bg='white')
        label29.place(relx=0.25, rely=0.31)

        clicked3 = StringVar()
        options3 = ['select',
                    'Day',
                    'Night',
                    ]
        clicked3.set(options3[0])
        drop = ttk.OptionMenu(root, clicked3, *options3)
        drop.place(relx=0.40, rely=0.35)
        label30 = Label(root, text='Time:', bg='white')
        label30.place(relx=0.41, rely=0.31)

        import tkinter as tk

        entry2_var = tk.StringVar()
        entry3_var = tk.StringVar()
        entry4_var = tk.StringVar()
        entry5_var = tk.StringVar()
        entry6_var = tk.StringVar()
        entry7_var = tk.StringVar()
        entry8_var = tk.StringVar()
        entry9_var = tk.StringVar()
        entry10_var = tk.StringVar()

        def convert_days_to_hours(event):
            try:
                days = float(entry2_var.get())
                hours = int(round(days * 6))
                entry3_var.set(str(hours))
            except ValueError:
                entry3_var.set("")

        entry2 = ttk.Entry(root, textvariable=entry2_var)
        entry2.place(relx=0.48, rely=0.35, width=50)
        label31 = Label(root, text='Days:', bg='white')
        label31.place(relx=0.48, rely=0.31)
        entry2.bind("<FocusOut>", convert_days_to_hours)

        entry3 = ttk.Entry(root, textvariable=entry3_var, state='readonly')
        entry3.place(relx=0.55, rely=0.35, width=50)
        label32 = Label(root, text='Days are auto-converted into hours!', fg='red', bg='white')
        label32.place(relx=0.61, rely=0.34)
        label33 = Label(root, text='Hours:', bg='white')
        label33.place(relx=0.55, rely=0.31)

        entry4 = ttk.Entry(root, textvariable=entry4_var)
        entry4.place(relx=0.18, rely=0.46, width=210)
        label34 = Label(root, text='Professor employment number:', bg='white')
        label34.place(relx=0.20, rely=0.41)

        clicked4 = StringVar()
        options4 = ['select',
                    'Locally',
                    'Abroad', ]
        clicked4.set(options4[0])
        drop = ttk.OptionMenu(root, clicked4, *options4)
        drop.place(relx=0.08, rely=0.25)
        label35 = Label(root, text='Residency:', bg='white')
        label35.place(relx=0.08, rely=0.21)

        entry4 = ttk.Entry(root, textvariable=entry5_var)
        entry4.place(relx=0.08, rely=0.36, width=60)
        label36 = Label(root, text='Country:', bg='white')
        label36.place(relx=0.08, rely=0.31)

        label37 = Label(root, text='Emirate:', bg='white')
        label37.place(relx=0.08, rely=0.41)
        clicked4 = StringVar()
        options4 = ['select',
                    'Dubai',
                    'Sharjah',
                    'Abu Dhabi',
                    'Al Ain',
                    'Ajman',
                    'Ras Al Khaima',
                    'Fujairah', ]
        clicked4.set(options4[0])
        drop = ttk.OptionMenu(root, clicked4, *options4)
        drop.place(relx=0.08, rely=0.46)

        label38 = Label(root, text='Professor:', bg='white')
        label38.place(relx=0.40, rely=0.41)
        clicked4 = StringVar()
        options4 = ['select',
                    'Local',
                    'Foreign'
                    ]
        clicked4.set(options4[0])
        drop = ttk.OptionMenu(root, clicked4, *options4)
        drop.place(relx=0.40, rely=0.46)

        label39 = Label(root, text='Program Language:', bg='white')
        label39.place(relx=0.08, rely=0.52)
        clicked4 = StringVar()
        options4 = ['select',
                    'English',
                    'Arabic',
                    ]
        clicked4.set(options4[0])
        drop = ttk.OptionMenu(root, clicked4, *options4)
        drop.place(relx=0.08, rely=0.57)

        clicked5 = StringVar()
        options5 = ['select',
                    '1',
                    '2',
                    '3',
                    '4',
                    '5',
                    '6',
                    '7',
                    ]
        clicked5.set(options5[0])
        drop = ttk.OptionMenu(root, clicked5, *options5)
        drop.place(relx=0.40, rely=0.57)
        label40 = Label(root, text='مدخلات البرنامج', bg='white')
        label40.place(relx=0.40, rely=0.52)

        label41 = Label(root, text='Program purpose(1):', bg='white')
        label41.place(relx=0.07, rely=0.66)
        entry5 = ttk.Entry(root, textvariable=entry6_var)
        entry5.place(relx=0.18, rely=0.66, width=210)

        label42 = Label(root, text='Program purpose(2):', bg='white')
        label42.place(relx=0.07, rely=0.71)
        entry6 = ttk.Entry(root, textvariable=entry7_var)
        entry6.place(relx=0.18, rely=0.71, width=210)

        entry543 = ttk.Entry(root, textvariable=entry9_var)
        entry543.place(relx=0.18, rely=0.85, width=700)
        label43 = Label(root, text='Comments:', bg='white')
        label43.place(relx=0.08, rely=0.85)

        label44 = Label(root, text='Program purpose(3):', bg='white')
        label44.place(relx=0.07, rely=0.76)
        entry7 = ttk.Entry(root, textvariable=entry8_var)
        entry7.place(relx=0.18, rely=0.76, width=210)

        def save_to_excel():
            data = {
                'Days': [entry2_var.get()],
                'Hours': [entry3_var.get()],
                'Program Name': [entry.get()],
                'Strategic Goal': [entry1.get()],
                'Professor Employment Number': [entry4_var.get()],
                'Residency': [clicked4.get()],
                'Country': [entry5_var.get()],
                'Emirate': [clicked4.get()],
                'Professor': [clicked4.get()],
                'Program Language': [clicked4.get()],
                'مدخلات البرنامج': [clicked5.get()],
                'Program Purpose(1)': [entry6_var.get()],
                'Program Purpose(2)': [entry7_var.get()],
                'Program Purpose(3)': [entry8_var.get()]
            }

            df = pd.DataFrame(data)
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            file_path = os.path.join(desktop_path, 'program_data.xlsx')
            df.to_excel(file_path, index=False)
            print("Data saved to 'program_data.xlsx'")

        save_button = ttk.Button(root, text="Save to Excel", command=save_to_excel)
        save_button.place(relx=0.46, rely=0.93)

        Label_page = Label(root, text='1', bg='white')
        Label_page.place(relx=0.05, rely=0.95)

        button = ttk.Button(root, text='Next', command=next)
        button.place(relx=0.56, rely=0.93)


# Opens the window for Talent Development Sector/Validation
def open1():
    top = Toplevel()
    top.title('Talent Development Sector/Validation')
    top.geometry('1000x600')


# opens the window for Training Programs Approved
def open2():
    top = Toplevel()
    top.title('Training Programs Approved')
    top.geometry('1000x600')


def open3():
    top = Toplevel()
    top.title('Behavioral Programs')
    top.geometry('1000x600')


def apply_style():
    style = ttk.Style()
    style.configure("first.TButton",  # Create a new style name
                    background="white",
                    foreground="black",
                    font=("Helvetica", 12),
                    padding=10,
                    bordercolor="black",
                    borderwidth=8,
                    focuscolor="black",
                    focusthickness=8)


apply_style()


def apply_style():
    style = ttk.Style()
    style.configure("second.TButton",  # Create a new style name
                    background="white",
                    foreground="black",
                    font=("Helvetica", 12),
                    padding=10,
                    bordercolor="black",
                    borderwidth=8,
                    focuscolor="black",
                    focusthickness=8)


apply_style()


def apply_style():
    style = ttk.Style()
    style.configure("third.TButton",  # Create a new style name
                    background="white",
                    foreground="black",
                    font=("Helvetica", 12),
                    padding=10,
                    bordercolor="black",
                    borderwidth=8,
                    focuscolor="black",
                    focusthickness=8)


apply_style()


def apply_style():
    style = ttk.Style()
    style.configure("fourth.TButton",  # Create a new style name
                    background="white",
                    foreground="black",
                    font=("Helvetica", 12),
                    padding=10,
                    bordercolor="black",
                    borderwidth=8,
                    focuscolor="black",
                    focusthickness=8)


apply_style()


def apply_style():
    style = ttk.Style()
    style.configure("fifth.TButton",  # Create a new style name
                    background="white",
                    foreground="Red",
                    font=("Helvetica", 12),
                    padding=10,
                    bordercolor="red",
                    borderwidth=8,
                    focuscolor="red",
                    focusthickness=8)


apply_style()


def btns():
    global btn1, btn2, btn3, btn4, btn5, btn6, btn7

    btn1 = ttk.Button(root, text="Organisational Units/Needs Gathering",
                      style='first.TButton', command=open_units_page, width=30)

    btn1.place(relx=0.2, rely=0.4, anchor='center')

    # Button for Talent Development Sector/Validation under me
    def unavailabke():
        messagebox.showerror('Error', 'Page unavailable for user')

    btn2 = ttk.Button(root, text="Talent Development Sector/Validation",
                      style='second.TButton', command=unavailabke, width=30)
    btn2.place(relx=0.8, rely=0.4, anchor='center')

    # Button for Training Programs Approved under me
    btn3 = ttk.Button(root, text="Training Programs Approved",
                      style='third.TButton', command=unavailabke, width=30)
    btn3.place(relx=0.2, rely=0.55, anchor='center')

    # Exit button under me
    btn4 = ttk.Button(root, text='Exit', style='fourth.TButton', command=exit)
    btn4.place(relx=0.5, rely=0.7, anchor='center')

    btn5 = ttk.Button(root, text="Behavioral Programs",
                      style='fourth.TButton', command=unavailabke, width=30)
    btn5.place(relx=0.8, rely=0.55, anchor='center')

    btn6 = ttk.Button(root, text='Switch Account?', style='fifth.TButton', command=logout)
    btn6.place(relx=0.5, rely=0.9, anchor='center')

    btn7 = ttk.Button(root, text='عربي', command=arabic)
    btn7.place(relx=0.05, rely=0.05, anchor='center')


def arabic():
    btn1.config(text='الوحدات التنظيمية/مسح الاحتياجات')
    btn2.config(text='قسم تطوير المواهب/صلاحية')
    btn3.config(text='البرامج التدريبية المعتمدة')
    btn4.config(text='خروج')
    btn5.config(text='البرامج السلوكية')
    btn6.config(text='تغيير الحساب؟')
    btn7.config(text='English')
    btn7.config(command=english)
    label1.config(text='ادارة الموار البشرية')
    label2.config(text='نظام تطوير المواهب')


def english():
    btn1.config(text='Organisational Units/Needs Gathering')
    btn2.config(text='Talent Development Sector/Validation')
    btn3.config(text='Training Programs Approved')
    btn4.config(text='Exit')
    btn5.config(text='Behavioral Programs')
    btn6.config(text='Switch Account?')
    btn7.config(text='عربي')
    btn7.config(command=arabic)
    label1.config(text='Human Resource Department')
    label2.config(text='Youth Development Program')


if __name__ == '__main__':
    try:
        _log("[6] Calling login()...")
        login()
        _log("[7] login() returned OK. Entering root.mainloop()...")
        root.mainloop()
        _log("[8] mainloop() exited normally (window was closed).")
    except Exception:
        # If anything crashes on startup, don't just let the window flash
        # shut with no explanation — log it, print it, and keep the
        # console open so it can actually be read.
        _log("[8] CRASHED:\n" + traceback.format_exc())
        traceback.print_exc()
        try:
            messagebox.showerror(
                'Startup Error',
                f'The app crashed.\n\nFull details were saved to:\n{LOG_PATH}'
            )
        except Exception:
            pass
        input(f'\nThe app hit an error. Full details saved to:\n{LOG_PATH}\nPress Enter to close this window...')