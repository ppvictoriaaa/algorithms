import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def open_file():
    file_path = filedialog.askopenfilename()

    with open( file_path, 'r' ) as file:
        lines = file.readlines()

    if len( lines ) != 4:
        print( "Неправильний формат файлу. Повинно бути 4 рядки." )
        return

    try:
        n_entry.delete( 0, tk.END )
        a_entry.delete( 0, tk.END )
        b_entry.delete( 0, tk.END )
        x_entry.delete( 0, tk.END )

        n_entry.insert( 0, int( lines[0].strip() ) )
        a_entry.insert( 0, int( lines[1].strip() ) )
        b_entry.insert( 0, int( lines[2].strip() ) )
        x_entry.insert( 0, int( lines[3].strip() ) )
    except ValueError:
        print( "Неправильний формат даних у файлі." )

def func1(x):
    return math.sin(x) - 2 * math.cos(x)

def func_sin1(x):
    return math.sin(x)

def interpolation_nodes(a_entry, b_entry, n_entry):
    a = a_entry.get()
    b = b_entry.get()
    n = n_entry.get()

    a=float(a)
    b=float(b)
    n=int(n)
    h = (b - a) / n
    nodes = [a + h * i for i in range(1, n+1)]
    return nodes

def interpolate_function(nodes, func):
    x_values = nodes
    y_values = [func(x) for x in nodes]
    return x_values, y_values

def exact_function_values(x_values, func):
    return [func(x) for x in x_values]

def divided_differences(x_values, y_values):
    n = len(x_values)

    table = np.zeros((n, n))
    table[:, 0] = y_values

    for j in range(1, n):
        for i in range(n - j):
            table[i, j] = (table[i + 1, j - 1] - table[i, j - 1]) / (x_values[i + j] - x_values[i])

    return table[0]

def newton_polynomial(x_values, y_values):
    n = len(x_values)
    f_x = divided_differences(x_values, y_values)

    polynomial = str(f_x[0])
    for i in range(1, n):
        term = str(f_x[i])
        for j in range(i):
            term += f" * (x - {x_values[j]})"
        polynomial += " + " + term

    return polynomial

def newton_interpolation(x, x_values, y_values):
    n = len(x_values)
    f_x = divided_differences(x_values, y_values)

    result = f_x[0]
    for i in range(1, n):
        term = f_x[i]
        for j in range(i):
            term *= (x - x_values[j])
        result += term
    return result

def func2(x):
    return np.sin(x) - 2 * np.cos(x)

def func_sin2(x):
    return np.sin(x)

def graph_origin_and_interpolation(a_entry, b_entry, n_entry, x_entry, func1, func2):
    nodes = interpolation_nodes(a_entry, b_entry, n_entry)
    x_values, y_values = interpolate_function(nodes, func1)

    a = float(a_entry.get())
    b = float(b_entry.get())
    x = float(x_entry.get())
    x_range = np.linspace(a, b, 200)
    y_range_func = func2(x_range)
    y_range_interp = [newton_interpolation(x, x_values, y_values) for x in x_range]
    y_at_x = newton_interpolation(x, x_values, y_values)

    root = tk.Tk()
    root.title("Графіки")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    plt.subplots_adjust( hspace=0.5 )

    if func2==func_sin2:
        ax1.plot( x_range, y_range_func, label='sin(x)' )
        ax1.set_xlabel( 'x' )
        ax1.set_ylabel( 'f(x)' )
        ax1.set_title( 'Графік функції sin(x)' )
        ax1.grid( True )
        ax1.legend()
    else:
        ax1.plot(x_range, y_range_func, label='sin(x) - 2*cos(x)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('f(x)')
        ax1.set_title('Графік функції sin(x) - 2*cos(x)')
        ax1.grid(True)
        ax1.legend()

    ax2.plot(x_range, y_range_interp, label='Інтерполяція', color='red')
    ax2.scatter(x_values, y_values, color='blue', label='Вузли інтерполяції')
    ax2.scatter(x, y_at_x, color='green', label=f'f({x}) = {y_at_x}', marker='o', s=100)
    ax2.set_xlabel('x')
    ax2.set_ylabel('f(x)')
    ax2.set_title('Графік інтерполяції')
    ax2.grid(True)
    ax2.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    tk.mainloop()


def plot_error_graph(a_entry, b_entry, n_entry, func1, func2):
    a = float( a_entry.get() )
    b = float( b_entry.get() )
    n = int( n_entry.get() )

    nodes = np.linspace( a, b, n )
    x_values, y_values = interpolate_function( nodes, func1 )
    x_range = np.linspace( a, b, 200 )
    error = [abs( func2( x ) - newton_interpolation( x, x_values, y_values ) ) for x in x_range]

    error_fig = plt.figure( figsize=(8, 6) )
    plt.plot( x_range, error, label='Похибка', color='orange' )
    plt.xlabel( 'x' )
    plt.ylabel( 'Похибка' )
    if func2 == func_sin2:
        plt.title( 'Графік похибки sin x' )
    else:
        plt.title( 'Графік похибки' )
    plt.grid( True )
    plt.legend()

    error_window = tk.Toplevel()
    error_window.title( "Графік похибки" )

    canvas = FigureCanvasTkAgg( error_fig, master=error_window )
    canvas.draw()
    canvas.get_tk_widget().pack( side=tk.TOP, fill=tk.BOTH, expand=1 )

def plot_table(a_entry, b_entry, n_entry, func2):
    nodes = interpolation_nodes( a_entry, b_entry, n_entry )
    x_values, y_values = interpolate_function( nodes, func1 )

    a = float( a_entry.get() )
    b = float( b_entry.get() )
    x_range = np.linspace( a, b, 400 )
    y_range_func = func2( x_range )
    y_range_interp = [newton_interpolation( x, x_values, y_values ) for x in x_range]

    error = [abs( y1 - y2 ) for y1, y2 in zip( y_range_func, y_range_interp )]

    differences = []
    for node in nodes:
        new_nodes = nodes.copy()
        new_nodes.remove( node )
        new_x_values, new_y_values = interpolate_function( new_nodes, func1)
        new_y_range_interp = [newton_interpolation( x, new_x_values, new_y_values ) for x in x_range]
        difference = [abs( y1 - y2 ) for y1, y2 in zip( y_range_interp, new_y_range_interp )]
        differences.append( sum( difference ) / len( difference ) )

    k_values = [(1 - diff / err) if err != 0 else 0 for diff, err in zip( differences, error )]

    table_data = {
        'n': list( range( 1, len( nodes ) + 1 ) ),
        'Похибка': error,
        'Різниця': differences,
        'k': k_values
    }

    x = float( x_entry.get())
    x_new=x+1
    y_interp = newton_interpolation( x, x_values, y_values )
    y_interp_new = newton_interpolation(x_new, x_values, y_values)
    error_x = abs( func2( x ) - y_interp )
    difference_x = abs(y_interp-y_interp_new)
    k_x = error_x / difference_x

    table_data_x = {
        'X': [x],
        'Інтерпольоване значення': [y_interp],
        'Похибка': [error_x],
        'Різниця': [difference_x],
        'k': [k_x]
    }

    table_window = tk.Toplevel()
    table_window.title( "Таблиці похибок" )
    table_window.geometry( '800x400' )

    table_frame = tk.Frame( table_window )
    table_frame.pack( side=tk.TOP, pady=10 )
    table1 = ttk.Treeview( table_frame )
    table1['columns'] = ('n', 'Похибка', 'Різниця', 'k')
    table1.heading( '#0', text='', anchor='center' )
    table1.column( '#0', anchor='center', width=0, stretch=False )
    table1.heading( 'n', text='n' )
    table1.column( 'n', anchor='center', width=100 )
    table1.heading( 'Похибка', text='Похибка' )
    table1.column( 'Похибка', anchor='center', width=150 )
    table1.heading( 'Різниця', text='Різниця' )
    table1.column( 'Різниця', anchor='center', width=150 )
    table1.heading( 'k', text='k' )
    table1.column( 'k', anchor='center', width=150 )

    for i in range( len( nodes ) ):
        table1.insert( '', 'end', values=(
        table_data['n'][i], table_data['Похибка'][i], table_data['Різниця'][i], table_data['k'][i]) )

    table1.pack( expand=True, fill='both' )

    table_frame2 = tk.Frame( table_window )
    table_frame2.pack( side=tk.TOP, pady=10 )
    table2 = ttk.Treeview( table_frame2 )
    table2['columns'] = ('X', 'Інтерпольоване значення', 'Похибка', 'Різниця', 'k')
    table2.heading( '#0', text='', anchor='center' )
    table2.column( '#0', anchor='center', width=0, stretch=False )
    table2.heading( 'X', text='X' )
    table2.column( 'X', anchor='center', width=100 )
    table2.heading( 'Інтерпольоване значення', text='Інтерпольоване значення' )
    table2.column( 'Інтерпольоване значення', anchor='center', width=150 )
    table2.heading( 'Похибка', text='Похибка' )
    table2.column( 'Похибка', anchor='center', width=150 )
    table2.heading( 'Різниця', text='Різниця' )
    table2.column( 'Різниця', anchor='center', width=150 )
    table2.heading( 'k', text='k' )
    table2.column( 'k', anchor='center', width=150 )

    table2.insert( '', 'end', values=(
    table_data_x['X'][0], table_data_x['Інтерпольоване значення'][0], table_data_x['Похибка'][0],
    table_data_x['Різниця'][0], table_data_x['k'][0]) )

    table2.pack( expand=True, fill='both' )

    return table_window
root = tk.Tk()
root.title("Main Window")
root.geometry('1200x350')
root['bg'] = 'gray'

label_for_n = tk.Label(root, text="Введіть кількість інтерполяційних точок:", font=("Courier New", 18))
label_for_n.grid(row=1, column=0, sticky="ew")
n_entry = tk.Entry(root, font=("Courier New", 18))
n_entry.grid(row=1, column=1, sticky="ew")

label_for_a = tk.Label(root, text="Введіть межу від:", font=("Courier New", 18))
label_for_a.grid(row=2, column=0, sticky="ew")
a_entry = tk.Entry(root, font=("Courier New", 18))
a_entry.grid(row=2, column=1, sticky="ew")

label_for_b = tk.Label(root, text="Введіть межу до:", font=("Courier New", 18))
label_for_b.grid(row=3, column=0, sticky="ew")
b_entry = tk.Entry(root, font=("Courier New", 18))
b_entry.grid(row=3, column=1, sticky="ew")

label_for_x = tk.Label(root, text="Введіть значення x:", font=("Courier New", 18))
label_for_x.grid(row=4, column=0, sticky="ew")
x_entry = tk.Entry(root, font=("Courier New", 18))
x_entry.grid(row=4, column=1, sticky="ew")

btn_graph_origin_interpolation = tk.Button(root, text="Побудувати графік інтерполяції", font=("Courier New", 18),fg='white', bg='brown', command=lambda: graph_origin_and_interpolation(a_entry, b_entry, n_entry, x_entry, func1, func2))
btn_graph_origin_interpolation.grid(row=5, column=0, sticky="ew")

btn_graph_error = tk.Button(root, text="Побудувати графік похибки", font=("Courier New", 18),fg='white', bg='brown', command=lambda: plot_error_graph(a_entry, b_entry, n_entry, func1, func2))
btn_graph_error.grid(row=5, column=1, sticky="ew")

btn_graph_sin = tk.Button(root, text="Побудувати графік інтерполяції sin x", font=("Courier New", 18),fg='white', bg='brown', command=lambda: graph_origin_and_interpolation(a_entry, b_entry, n_entry, x_entry, func_sin1, func_sin2))
btn_graph_sin.grid(row=6, column=0, sticky="ew")

btn_graph_sin = tk.Button(root, text="Побудувати графік похибки інтерполяції sin x", font=("Courier New", 18),fg='white', bg='brown', command=lambda: plot_error_graph(a_entry, b_entry, n_entry, func_sin1, func_sin2))
btn_graph_sin.grid(row=6, column=1, sticky="ew")

btn_table = tk.Button(root, text="Таблиця похибок", font=("Courier New", 18), fg='white', bg='brown', command=lambda: plot_table(a_entry, b_entry, n_entry, func2))
btn_table.grid(row=7, column=0, columnspan=3, sticky='ew')

btn_file = tk.Button(root, text="Зчитати дані з файлу", font=("Courier New", 18), bg='white', command=open_file)
btn_file.grid(row=8, column=0, columnspan=3, sticky='ew')
root.mainloop()

