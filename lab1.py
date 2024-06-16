import math
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

def read_values_from_file(entry_a, entry_b):
    file_path = filedialog.askopenfilename(title="Оберіть файл", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                a, b = map(int, lines)
                entry_a.delete(0, 'end')
                entry_b.delete(0, 'end')
                entry_a.insert(0, a)
                entry_b.insert(0, b)
        except (ValueError, FileNotFoundError):
            tk.messagebox.showinfo('Помилка', 'Не вдалося зчитати дані з файлу.')

def read_values_from_file_for_task3(entry_n):
    file_path = filedialog.askopenfilename(title="Оберіть файл", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                n = int(file.read().strip())
                entry_n.delete(0, 'end')
                entry_n.insert(0, n)
        except (ValueError, FileNotFoundError):
            tk.messagebox.showinfo('Помилка', 'Не вдалося зчитати дані з файлу.')

def validate_a_b(a, b):
    if a - b == 0 or a + b == 0 or a - b == 1 or a + b <= 0 or a - b <= 0:
        messagebox.showinfo('Увага', 'НЕ ВИЗНАЧЕНО\nОбласть визначення:\na - b != 0 \na + b != 0 \na - b != 1 \na + b >= 0 \n a - b >= 0')
        return False
    return True

root = tk.Tk()
root.title("Main Window")
root.geometry('550x250')
root['bg'] = 'gray'
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

button_style = ttk.Style()
button_style.configure('My.TButton', font=('Times New Roman', 20), foreground='black', background='white')

label_about_me = tk.Label(root, text='Інформація про студента', font=('Times New Roman', 25), bg='gray', fg='white', relief=tk.SUNKEN)
label_about_me.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

label_me = tk.Label(root, text='ПІБ: ', font=('Times New Roman', 20), bg='white', fg='black')
label_me.grid(row=2, column=0, padx=10, pady=10)

label_me1 = tk.Label(root, text='Група: ', font=('Times New Roman', 20), bg='white', fg='black')
label_me1.grid(row=3, column=0, padx=10, pady=10)

label_me2 = tk.Label(root, text='Пекур Вікторія Ігорівна', font=('Times New Roman', 20), bg='gray', fg='white')
label_me2.grid(row=2, column=1, columnspan=2)

label_me2 = tk.Label(root, text='ІО-24', font=('Times New Roman', 20), bg='gray', fg='white')
label_me2.grid(row=3, column=1, columnspan=2)

def open_window1(window_title):
    win1 = tk.Toplevel(root)
    win1.title(window_title)
    win1.grid_rowconfigure(0, weight=0)
    win1.grid_rowconfigure(1, weight=0)
    win1.grid_rowconfigure(2, weight=0)
    win1.grid_rowconfigure(3, weight=0)
    win1.grid_rowconfigure(4, weight=0)

    win1.grid_columnconfigure(0, weight=1)
    win1.grid_columnconfigure(1, weight=1)

    label_task1 = tk.Label(win1, text='Y1 = lg(a+b)/ln(a-b) + ln(a+b)/lg(a-b)', font=('Times New Roman', 16), bg='#a0a0a0')
    label_task1.grid(row=0, column=0, columnspan=2)

    label_for_a = tk.Label(win1, text="Введіть значення для а:", font=('Times New Roman', 16))
    label_for_a.grid(row=1, column=0)
    entry_for_a = tk.Entry(win1, font=('Times New Roman', 16))
    entry_for_a.grid(row=1, column=1)

    label_for_b = tk.Label(win1, text="Введіть значення для b:", font=('Times New Roman', 16))
    label_for_b.grid(row=2, column=0)
    entry_for_b = tk.Entry(win1, font=('Times New Roman', 16))
    entry_for_b.grid(row=2, column=1)

    def calculate():
        a = entry_for_a.get()
        b = entry_for_b.get()

        if not (str( a ).replace( ".", "", 1 ).replace( "-", "", 1 ).isdigit() and str( b ).replace( ".", "", 1 ).replace( "-", "", 1 ).isdigit()):
            messagebox.showinfo( 'Увага', 'Введіть числові значення для a та b.' )
            return False

        a = float(a)
        b = float(b)

        if not validate_a_b(a, b):
            return

        Y1 = math.log10(a + b) / math.log(a - b) + math.log(a + b) / math.log10(a - b)
        label_for_result = tk.Label(win1, text=f"Y1 = {round(Y1, 3)}", font=('Times New Roman', 16), bg='gray', fg='white')
        label_for_result.grid(row=5, column=0, columnspan=2)

    button_read_from_file = ttk.Button(win1, text='Зчитати значення з файлу',
                                       command=lambda: read_values_from_file(entry_for_a, entry_for_b),
                                       style='My.TButton')
    button_read_from_file.grid(row=4, column=0, columnspan=2)

    button_calculate = ttk.Button(win1, text='Розрахувати', command=calculate, style='My.TButton')
    button_calculate.grid(row=3, column=0, columnspan=2)

def open_window2(window_title):
    win2 = tk.Toplevel(root)
    win2.title(window_title)

    win2.grid_rowconfigure(0, weight=0)
    win2.grid_rowconfigure(1, weight=0)
    win2.grid_rowconfigure(2, weight=0)
    win2.grid_rowconfigure(3, weight=0)
    win2.grid_rowconfigure(4, weight=0)
    win2.grid_rowconfigure(5, weight=0)

    win2.grid_columnconfigure(0, weight=1)
    win2.grid_columnconfigure(1, weight=1)
    win2.grid_columnconfigure(2, weight=1)

    label_for_a = tk.Label(win2, text="Введіть значення для а:", font=('Times New Roman', 16))
    label_for_a.grid(row=0, column=0)
    entry_for_a = tk.Entry(win2, font=('Times New Roman', 16))
    entry_for_a.grid(row=0, column=1)

    label_for_b = tk.Label(win2, text="Введіть значення для b:", font=('Times New Roman', 16))
    label_for_b.grid(row=1, column=0)
    entry_for_b = tk.Entry(win2, font=('Times New Roman', 16))
    entry_for_b.grid(row=1, column=1)

    def continue_():
        a = entry_for_a.get()
        b = entry_for_b.get()

        if not (str( a ).replace( ".", "", 1 ).replace( "-", "", 1 ).isdigit() and str( b ).replace( ".", "", 1 ).replace( "-", "", 1 ).isdigit()):
            messagebox.showinfo( 'Увага', 'Введіть числові значення для a та b.' )
            return False

        a = float(a)
        b = float(b)

        if math.sqrt(a**2 + b**2) > 10:
            if abs( a ) <= abs( b ):
                messagebox.showinfo( 'Увага', 'НЕ ВИЗНАЧЕНО\nОбласть визначення: \n |a| > |b|' )
                entry_for_a.delete( 0, 'end' )
                entry_for_b.delete( 0, 'end' )

            else:
                label_task2_bigger_10 = tk.Label(win2, text='sqrt(a^2 + b^2) > 10\nОтже: y = sqrt((a^2 + b^2)/(a^2 - b^2))',
                                             font=('Times New Roman', 16), bg='#a0a0a0')
                label_task2_bigger_10.grid(row=2, column=0, columnspan=3)

            def calculate_():
                a = float(entry_for_a.get())
                b = float(entry_for_b.get())
                y = math.sqrt((a**2 + b**2) / (a**2 - b**2))
                label_result = tk.Label(win2, text=f'y = {round(y, 3)}', font=('Times New Roman', 20))
                label_result.grid(row=5, column=0, columnspan=3)

            button_calculate = ttk.Button(win2, text='Розрахувати', command=calculate_, style='My.TButton')
            button_calculate.grid(row=3, column=0, columnspan=3)

        elif math.sqrt(a**2 + b**2) <= 10:
            if abs( a ) < abs( b ):
                messagebox.showinfo( 'Увага', 'НЕ ВИЗНАЧЕНО\nОбласть визначення: \n |a| >= |b|' )
                entry_for_a.delete( 0, 'end' )
                entry_for_b.delete( 0, 'end' )
            else:
                label_task2_less_10 = tk.Label(win2, text='sqrt(a^2 + b^2) <= 10\nОтже: y = sqrt((a^2 - b^2)/(a^2 + b^2))',
                                           font=('Times New Roman', 16), bg='#a0a0a0')
                label_task2_less_10.grid(row=2, column=0, columnspan=3)

            def calculate_():
                a = float(entry_for_a.get())
                b = float(entry_for_b.get())
                y = math.sqrt((a**2 - b**2) / (a**2 + b**2))
                label_result = tk.Label(win2, text=f'y = {round(y, 3)}', font=('Times New Roman', 20))
                label_result.grid(row=5, column=0, columnspan=3)

            button_calculate = ttk.Button(win2, text='Розрахувати', command=calculate_, style='My.TButton')
            button_calculate.grid(row=3, column=0, columnspan=3)

    button_read_from_file = ttk.Button(win2, text='Зчитати значення з файлу',
                                       command=lambda: read_values_from_file(entry_for_a, entry_for_b),
                                       style='My.TButton')
    button_read_from_file.grid(row=4, column=0, columnspan=3)

    button_continue = ttk.Button(win2, text='Продовжити', command=continue_, style='My.TButton')
    button_continue.grid(row=0, rowspan=2, column=2)

def open_window3(window_title):
    win3 = tk.Toplevel(root)
    win3.title(window_title)
    win3.grid_rowconfigure(0, weight=0)
    win3.grid_rowconfigure(1, weight=0)
    win3.grid_rowconfigure(2, weight=0)
    win3.grid_rowconfigure(3, weight=0)

    win3.grid_columnconfigure(0, weight=1)
    win3.grid_columnconfigure(1, weight=1)

    label_task = tk.Label(win3, text='f = SUM[1 < i < n](i! - (i - 1)!)', font=('Times New Roman', 16), bg='#a0a0a0')
    label_task.grid(row=0, column=0, columnspan=2)

    label_for_n = tk.Label(win3, text="Введіть значення для n:", font=('Times New Roman', 16))
    label_for_n.grid(row=1, column=0)
    entry_for_n = tk.Entry(win3, font=('Times New Roman', 16))
    entry_for_n.grid(row=1, column=1)

    def calculate():
        n = entry_for_n.get()

        if not str(n).replace('-', '').isdigit():
            messagebox.showinfo('Помилка', 'Введіть ціле числове значення для n.')
            return

        n = int(n)

        if n < 1:
            messagebox.showinfo('Увага', 'НЕ ВИЗНАЧЕНО\nОбласть визначення:\n n >= 1')
            entry_for_n.delete(0, 'end')
            return

        f = 0
        for i in range(1, n + 1):
            f += math.factorial(i) - math.factorial(i - 1)
        label_for_result = tk.Label(win3, text=f"f = {f}", font=('Times New Roman', 16), bg='gray', fg='white')
        label_for_result.grid(row=5, column=0, columnspan=2)

    button_read_from_file = ttk.Button(win3, text='Зчитати значення з файлу',
                                       command=lambda: read_values_from_file_for_task3(entry_for_n),
                                       style='My.TButton')
    button_read_from_file.grid(row=4, column=0, columnspan=3)

    button_calculate = ttk.Button(win3, text='Розрахувати', command=calculate, style='My.TButton')
    button_calculate.grid(row=3, column=0, columnspan=2)

button1 = ttk.Button(root, text='Task 1', command=lambda: open_window1('Task 1'), style='My.TButton')
button1.grid(row=0, column=0)

button2 = ttk.Button(root, text='Task 2', command=lambda: open_window2('Task 2'), style='My.TButton')
button2.grid(row=0, column=1)

button3 = ttk.Button(root, text='Task 3', command=lambda: open_window3('Task 3'), style='My.TButton')
button3.grid(row=0, column=2)

root.mainloop()

