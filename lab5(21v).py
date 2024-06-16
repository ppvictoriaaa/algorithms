import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    with open( file_path, 'r' ) as file:
        lines = file.readlines()

    if len( lines ) != 3:
        print( "Неправильний формат файлу. Повинно бути 3 рядки." )
        return
    try:
        data = [list( map( float, line.split() ) ) for line in lines]

        # Заповнити відповідні елементи інтерфейсу
        entry_x1_1.delete( 0, tk.END )
        entry_x2_1.delete( 0, tk.END )
        entry_x3_1.delete( 0, tk.END )
        entry_res_1.delete( 0, tk.END )
        entry_x1_2.delete( 0, tk.END )
        entry_x2_2.delete( 0, tk.END )
        entry_x3_2.delete( 0, tk.END )
        entry_res_2.delete( 0, tk.END )
        entry_x1_3.delete( 0, tk.END )
        entry_x2_3.delete( 0, tk.END )
        entry_x3_3.delete( 0, tk.END )
        entry_res_3.delete( 0, tk.END )

        entry_x1_1.insert( 0, data[0][0] )
        entry_x2_1.insert( 0, data[0][1] )
        entry_x3_1.insert( 0, data[0][2] )
        entry_res_1.insert( 0, data[0][3] )
        entry_x1_2.insert( 0, data[1][0] )
        entry_x2_2.insert( 0, data[1][1] )
        entry_x3_2.insert( 0, data[1][2] )
        entry_res_2.insert( 0, data[1][3] )
        entry_x1_3.insert( 0, data[2][0] )
        entry_x2_3.insert( 0, data[2][1] )
        entry_x3_3.insert( 0, data[2][2] )
        entry_res_3.insert( 0, data[2][3] )
    except ValueError:
        print( "Неправильний формат даних у файлі." )


def make_matrix_diag(A):
    D = np.diag(np.diag(A))
    R = A - D
    return D, R

def check_norms_jacobi():
    A = [[float( entry_x1_1.get() ), float( entry_x2_1.get() ), float( entry_x3_1.get() )],
         [float( entry_x1_2.get() ), float( entry_x2_2.get() ), float( entry_x3_2.get() )],
         [float( entry_x1_3.get() ), float( entry_x2_3.get() ), float( entry_x3_3.get() )]]
    D, R = make_matrix_diag(A)
    D_inv = np.linalg.inv( D )
    T = np.dot( D_inv, R )
    # Перевірка збіжності за спектральним радіусом
    eigenvalues = np.linalg.eigvals( T )
    spectral_radius = max( abs( eigenvalues ) )
    if spectral_radius < 1:
        return True
    else:
        return False

def jacobi_iteration(e=0.0000000000000001, max_iterations=10000):
    A = [[float( entry_x1_1.get() ), float( entry_x2_1.get() ), float( entry_x3_1.get() )],
         [float( entry_x1_2.get() ), float( entry_x2_2.get() ), float( entry_x3_2.get() )],
         [float( entry_x1_3.get() ), float( entry_x2_3.get() ), float( entry_x3_3.get() )]]
    b = [float( entry_res_1.get() ), float( entry_res_2.get() ), float( entry_res_3.get() )]

    if check_norms_jacobi() == True:
        n = len( b )
        x = np.zeros( n )
        D, R = make_matrix_diag( A )
        D_inv = np.linalg.inv( D )

        max_iterations_count = 0
        for _ in range( max_iterations ):
            x_new = np.dot( D_inv, b - np.dot( R, x ) )
            max_iterations_count += 1
            if np.linalg.norm( x_new - x ) < e:
                print( f"Кількість ітерацій: {max_iterations_count}" )
                return x_new
            x = x_new
        raise ValueError( "Досягнута максимальна кількість ітерацій." )

def click_btn():
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) >= 6:
            label.grid_forget()

    if check_norms_jacobi() == False:
        tk.messagebox.showerror('Помилка', 'Метод Якобі для введених коефіцієнтів не збігається')
    elif check_norms_jacobi() == True:
        x = jacobi_iteration()
        print(x)
        root1_label = tk.Label(root, text=f"x1 = {x[0]}",font=("Comic Sans MS", 18), bg="#191970", fg="white")
        root1_label.grid(row=6, column=1, columnspan=8)
        root2_label = tk.Label(root, text=f"x2 = {x[1]}",font=("Comic Sans MS", 18), bg="#191970", fg="white")
        root2_label.grid(row=7, column=1, columnspan=8)
        root3_label = tk.Label(root, text=f"x3 = {x[2]}",font=("Comic Sans MS", 18), bg="#191970", fg="white")
        root3_label.grid(row=8, column=1, columnspan=8)

root = tk.Tk()
root.title("Лабораторна робота № 5 (метод Якобі)")
root.geometry('1100x600')
root['bg'] = '#191970'
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)
root.grid_columnconfigure(7, weight=1)
root.grid_columnconfigure(8, weight=1)

label_name = tk.Label(root, text = "Система лінійних рівнянь: ", font=("Comic Sans MS", 30), bg='#191970', fg='white').grid(row=1, column=1, columnspan=8, sticky='w')

entry_x1_1 = tk.Entry(root, font=("Comic Sans MS", 18), width=6)
entry_x1_1.grid(row=2, column=1, sticky='ew')
label_x1_1 = tk.Label(root, text = "*x1 + ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x1_1.grid(row=2, column=2, sticky='ew')

entry_x2_1 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_x2_1.grid(row=2, column=3, sticky='ew')
label_x2_1 = tk.Label(root, text = "*x2 + ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x2_1.grid(row=2, column=4, sticky='ew')

entry_x3_1 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_x3_1.grid(row=2, column=5, sticky='ew')
label_x3_1 = tk.Label(root, text = "*x3 = ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x3_1.grid(row=2, column=6, sticky='ew')

entry_res_1 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_res_1.grid(row=2, column=7, sticky='ew')

entry_x1_2 = tk.Entry(root, font=("Comic Sans MS", 18), width=6)
entry_x1_2.grid(row=3, column=1, sticky='ew')
label_x1_2 = tk.Label(root, text = "*x1 + ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x1_2.grid(row=3, column=2, sticky='ew')

entry_x2_2 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_x2_2.grid(row=3, column=3, sticky='ew')
label_x2_2 = tk.Label(root, text = "*x2 + ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x2_2.grid(row=3, column=4, sticky='ew')

entry_x3_2 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_x3_2.grid(row=3, column=5, sticky='ew')
label_x3_2 = tk.Label(root, text = "*x3 = ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x3_2.grid(row=3, column=6, sticky='ew')

entry_res_2 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_res_2.grid(row=3, column=7, sticky='ew')

entry_x1_3 = tk.Entry(root, font=("Comic Sans MS", 18), width=6)
entry_x1_3.grid(row=4, column=1, sticky='ew')
label_x1_3 = tk.Label(root, text = "*x1 + ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x1_3.grid(row=4, column=2, sticky='ew')

entry_x2_3 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_x2_3.grid(row=4, column=3, sticky='ew')
label_x2_3 = tk.Label(root, text = "*x2 + ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x2_3.grid(row=4, column=4, sticky='ew')

entry_x3_3 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_x3_3.grid(row=4, column=5, sticky='ew')
label_x3_3 = tk.Label(root, text = "*x3 = ", font=("Comic Sans MS", 18), bg='#191970', fg='white')
label_x3_3.grid(row=4, column=6, sticky='ew')

entry_res_3 = tk.Entry(root, font=("Comic Sans MS", 18) , width=6)
entry_res_3.grid(row=4, column=7, sticky='ew')

button_read_file = tk.Button(root, text="Зчитати\nкоефіцієнти\nз файлу", font=("Comic Sans MS", 24), command=open_file ).grid(row=2, rowspan=3, column = 8)

button_resolving = tk.Button(root, text="Знайти розв`язки системи", font=("Comic Sans MS", 20), command=click_btn).grid(row=5, column=1, columnspan=8, sticky='ew')

root.mainloop()
