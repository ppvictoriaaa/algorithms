import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

def open_file():
    file_path = filedialog.askopenfilename()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    if len(lines) != 3:
        print("Неправильний формат файлу. Повинно бути 3 рядки.")
        return

    try:
        input_a.delete(0, tk.END)
        input_b.delete(0, tk.END)
        input_e.delete(0, tk.END)

        input_a.insert(0, float(lines[0].rstrip()))
        input_b.insert(0, float(lines[1].rstrip()))
        input_e.insert(0, float(lines[2].rstrip()))
    except ValueError:
        print("Неправильний формат даних у файлі.")

root = tk.Tk()
root.title("Lab3")
root.geometry('1100x620')
root['bg'] = '#191970'
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)
root.grid_rowconfigure(5, weight=0)
root.grid_rowconfigure(6, weight=0)
root.grid_rowconfigure(7, weight=0)

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

variant_label = tk.Label(root, text="x^3 - 2x + 7 = 0", font=("Comic Sans MS", 20)).grid(row=1, column=1, columnspan=4)

def plot_function():
    fig = plt.figure(figsize=(5, 3), dpi=100)
    x = np.linspace(-5, 5, 500)
    y = x**3 - 2*x + 7
    plt.plot(x, y, color='#191970', label='y = x^3 - 2x + 7')
    plt.axhline(0, color='black', linestyle='-', linewidth=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Графік функції')
    plt.grid(True)
    plt.legend()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=2, column=1, columnspan=4)
plot_function()

input_ab_label = tk.Label(root, text="1)Для знаходження кореня рівняння введіть відрізок [a, b]:", font=("Comic Sans MS", 18), bg="#191970", fg="white").grid(row=3, column=1, columnspan=4)

input_a_label = tk.Label(root, text="a:", font=("Comic Sans MS", 18), bg="#191970", fg="white").grid(row=4, column=1)
input_a = tk.Entry(root, font=("Comic Sans MS", 18))
input_a.grid(row=4, column=2)

input_b_label = tk.Label(root, text="b:", font=("Comic Sans MS", 18), bg="#191970", fg="white").grid(row=4, column=3)
input_b = tk.Entry(root, font=("Comic Sans MS", 18))
input_b.grid(row=4, column=4)

input_ee_label = tk.Label(root, text="2)Введіть точність розрахунків:", font=("Comic Sans MS", 18), bg="#191970", fg="white").grid(row=5, column=1, columnspan=4)
input_e_label = tk.Label(root, text="e:", font=("Comic Sans MS", 18), bg="#191970", fg="white").grid(row=6, column=1)
input_e = tk.Entry(root, font=("Comic Sans MS", 18))
input_e.grid(row=6, column=2)

def func(x):
    y = x ** 3 - 2 * x + 7
    return y

x = sp.symbols('x')
f = x**3 - 2*x + 7

def calculate_roots():
    a = float(input_a.get())
    b = float(input_b.get())
    e = float(input_e.get())

    iterations = 0
    xn = a
    x_n1 = b
    f = x ** 3 - 2 * x + 7
    roots_xn = [a]
    roots_x_n1 = [b]

    while True:
        f_prime_x_n1 = f.diff(x).subs(x, x_n1).evalf()

        xn_plus_1 = xn - (func(xn) / (func(x_n1) - func(xn))) * (x_n1 - xn)
        x_n1_plus_1 = x_n1 - func(x_n1) / f_prime_x_n1

        roots_xn.append(xn_plus_1)
        roots_x_n1.append(x_n1_plus_1)

        if abs(x_n1_plus_1 - xn_plus_1) < e:
            break

        xn = xn_plus_1
        x_n1 = x_n1_plus_1

        iterations += 1
    res = (xn_plus_1 + x_n1_plus_1) / 2

    return roots_xn, roots_x_n1, iterations, res

def plot_function_ab():
    roots = calculate_roots()
    roots_xn = roots[0]
    roots_x_n1 = roots[1]

    a = float(input_a.get())
    b = float(input_b.get())

    if func(a) * func(b) < 0:
        graph = tk.Tk()
        graph.title('Lab3')
        graph.geometry('800x450')
        graph['bg'] = '#191970'

        graph.grid_rowconfigure( 1, weight=0 )
        graph.grid_rowconfigure( 2, weight=0 )
        graph.grid_rowconfigure( 3, weight=0 )

        graph.grid_columnconfigure( 1, weight=1 )
        graph.grid_columnconfigure( 2, weight=1 )


        fig = plt.figure(figsize=(5, 3), dpi=100)
        x = np.linspace(a, b, 500)
        y = func(x)
        plt.plot(x, y, color='#191970', label='y = x^3 - 2x + 7')
        plt.axhline(0, color='black', linestyle='-', linewidth=1)

        for i in range(len(roots_xn)):
            if a <= roots_xn[i] <= b:
                if i == len(roots_xn) - 1:
                    plt.plot(roots_xn[i], func(roots_xn[i]), 'ob', markersize=8)
                else:
                    plt.plot(roots_xn[i], func(roots_xn[i]), 'ok', markersize=8)

        for i in range(len(roots_x_n1)):
            if a <= roots_x_n1[i] <= b:
                if i == len(roots_x_n1) - 1:
                    plt.plot(roots_x_n1[i], func(roots_x_n1[i]), 'ob', markersize=8)
                else:
                    plt.plot(roots_x_n1[i], func(roots_x_n1[i]), 'ok', markersize=8)

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Графік функції')
        plt.grid(True)
        plt.legend()

        res = calculate_roots()[3]
        iter = calculate_roots()[2] + 1
        res_label = tk.Label(graph, text=f'Наближений корінь рівняння: {res}', font=("Comic Sans MS", 14), bg="#191970", fg="white")
        res_label.grid(row=2, column=1, sticky='w')
        iter_label = tk.Label(graph, text=f'Кількість пар наближення: {iter}', font=("Comic Sans MS", 14), bg="#191970", fg="white")
        iter_label.grid(row=3, column=1, sticky='w')

        canvas = FigureCanvasTkAgg(fig, master=graph)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=1)

        graph.mainloop()
    else:
        tk.messagebox.showinfo('Увага', 'Введіть значення для a і b такі, щоб функція мала різний знак на кінцях відрізку')
        input_a.delete(0, "end")
        input_b.delete(0, "end")
button_calculate = tk.Button(root, text="Розрахувати корінь рівняння", font=("Comic Sans MS", 18), bg="black", fg="white", command=plot_function_ab).grid(row=7, column=1, columnspan=4)

button_file = tk.Button(root, text = 'Вставити значення з файлу', font=("Comic Sans MS", 18), bg="black", fg="white", command=open_file).grid(row=8, column=1, columnspan=4)
root.mainloop()