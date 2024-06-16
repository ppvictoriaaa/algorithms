import time
import numpy as np

import tkinter as tk
from tkinter import messagebox, ttk, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def is_valid_input(input_str):
    try:
        numbers = input_str.split()
        for num in numbers:
            int(num)
        return True
    except ValueError:
        return False

def read_values_from_file(entries):
    file_path = filedialog.askopenfilename( title="Оберіть файл", filetypes=[("Text files", "*.txt")] )
    if file_path:
        try:
            with open( file_path, 'r' ) as file:
                lines = file.readlines()
                for i, line in enumerate( lines ):
                    if i < len( entries ):
                        numbers = line.strip().split()
                        if is_valid_input( ' '.join( numbers ) ):
                            entries[i].delete( 0, 'end' )
                            entries[i].insert( 0, ' '.join( numbers ) )
                        else:
                            messagebox.showinfo( 'Помилка', 'Файл містить неправильні дані.' )
                            break
                    else:
                        break
        except FileNotFoundError:
            messagebox.showinfo( 'Помилка', 'Файл не знайдено.' )
        except Exception as e:
            messagebox.showinfo( 'Помилка', f'Виникла помилка: {str( e )}' )

def graph_input(sizes_list, times_list):
    root1 = tk.Tk()
    root1.title( 'Графік згідно даних')
    root1.geometry( "600x300" )

    fig = Figure( figsize=(5, 4), dpi=100 )
    plot = fig.add_subplot( 111 )

    plot.plot( sizes_list, times_list, linestyle='-', color='green' )
    plot.set_title( 'Графік' )
    plot.set_xlabel( 'Розмір' )
    plot.set_ylabel( 'Час' )

    canvas = FigureCanvasTkAgg( fig, master=root1 )
    canvas.draw()
    canvas.get_tk_widget().pack( side=tk.TOP, fill=tk.BOTH, expand=1 )
    tk.mainloop()

def graph_teor(test_arrays):
    sizes_list = []
    k_values = [max(map(len, map(str, sublist))) for sublist in test_arrays]

    for test_array in test_arrays:
        sizes_list.append(len(test_array))

    root = tk.Tk()
    root.title( 'Теоретичний графік' )
    root.geometry( "600x300" )

    fig = Figure( figsize=(5, 4), dpi=100 )
    plot = fig.add_subplot( 111 )

    x = np.array( sizes_list )
    O = np.array( k_values ) * x
    plot.plot( O, x, linestyle='-', color='green', label='O(n*k)' )

    plot.set_title( 'Графік' )
    plot.set_xlabel( 'Розмір' )
    plot.set_ylabel( 'кількість операцій' )

    plot.legend( loc='upper left' )

    canvas = FigureCanvasTkAgg( fig, master=root )
    canvas.draw()
    canvas.get_tk_widget().pack( side=tk.TOP, fill=tk.BOTH, expand=1 )
    tk.mainloop()

def countingSort(array, place):
    size = len( array )
    output = [0] * size
    count = [0] * 10

    for i in range( 0, size ):
        index = array[i] // place
        count[index % 10] += 1

    for i in range( 1, 10 ):
        count[i] += count[i - 1]

    i = size - 1
    while i >= 0:
        index = array[i] // place
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1

    for i in range( 0, size ):
        array[i] = output[i]


def radixSort(array):
    max_neg = 0
    if any( num < 0 for num in array ):
        max_neg = min( array )
        for i in range( len( array ) ):
            array[i] = array[i] - max_neg

    max_element = max( array )
    place = 1
    while max_element // place > 0:
        countingSort( array, place )
        place *= 10
    for i in range( len( array ) ):
        array[i] = array[i] + max_neg

def generate_ten_arrays(page, row_):
    def generation():
        test_arrays = []
        sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000]
        for size in sizes:
            random_array = np.random.randint(-10000, 10000, size)
            test_arrays.append(random_array)
        return test_arrays

    ten_arrays = generation()
    sizes_list = []
    times_list = []
    for i, array in enumerate( ten_arrays ):
        start_time = time.time()
        radixSort( array )
        end_time = time.time()
        elapsed_time = end_time - start_time

        sizes_list.append( len( array ) )
        times_list.append( elapsed_time )

        print( f"Test Array {i + 1} (Size: {len( array )}): {array[:10]}... Sorting Time: {elapsed_time:.10f} seconds" )
    print( sizes_list, times_list )

    label_generation = tk.Label( page, text="10 масивів згенеровано", font=("Courier New", 20) )
    label_generation.grid( row=row_, column=0 )

    button_graph_input = tk.Button( page, text="Побудувати графік згідно даним", font=("Courier New", 18), command=lambda:graph_input(sizes_list, times_list) )
    button_graph_input.grid( row=row_ + 1, column=0 , sticky="ew", columnspan=2)

    button_graph_teor = tk.Button( page, text="Побудувати теоретичний графік", font=("Courier New", 18), command=lambda: graph_teor(ten_arrays))
    button_graph_teor.grid( row=row_ + 2, column=0 , sticky="ew", columnspan=2)


app = tk.Tk()
app.title("Лабораторна робота №2")
app.geometry("800x500")
# Створення планшету
notebook = ttk.Notebook(app)
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Courier New", 12))

# Створення нульової сторінки
page0 = ttk.Frame(notebook)
label1 = ttk.Label(page0, text="Група ІО-24\nПекур Вікторія Ігорівна\nВаріант 21", font=("Courier New", 20))
label1.pack(padx=0, pady=90)
notebook.add(page0, text="Ім'я студентки")

# Створення першої сторінки
page1 = ttk.Frame(notebook)
page1.grid_rowconfigure(0, weight=0)
page1.grid_rowconfigure(1, weight=0)
page1.grid_rowconfigure(2, weight=1)
page1.grid_rowconfigure(3, weight=0)
page1.grid_rowconfigure(4, weight=1)

page1.grid_columnconfigure(0, weight=1)
def sort_entry(entry_input):
    input_str = entry_input.get()
    if is_valid_input(input_str):
        number_list = input_str.split()
        number_list = [int(num) for num in number_list]
        radixSort(number_list)
        label_output = tk.Label(page1, text=f"{' '.join(map(str, number_list))}", font=("Courier New", 20))
        label_output.grid(row=4, column=0)
    else:
        messagebox.showinfo('Помилка', 'Введіть цілі числа через пробіл!')
        entry_input.delete( 0, tk.END )

label_input = ttk.Label(page1, text="Введіть список для сортування (через пробіл)\nабо\n", font=("Courier New", 20))
label_input.grid(row=0, column=0)
entry_input = tk.Entry(page1, font=("Courier New", 20))
entry_input.grid(row=2, column=0, sticky="ew", columnspan=2)
entry_input_list=[]
entry_input_list.append(entry_input)

btn_input=tk.Button(page1, text='Зчитати дані з файлу', font=("Courier New", 20), command=lambda: read_values_from_file(entry_input_list))
btn_input.grid(row=1, column=0, sticky="ew", columnspan=2)

btn_input=tk.Button(page1, text='Сортувати', font=("Courier New", 20), command=lambda: sort_entry(entry_input))
btn_input.grid(row=3, column=0, sticky="ew", columnspan=2)

notebook.add(page1, text="Порозрядне сортування")

# Створення другої сторінки
page2 = ttk.Frame(notebook)
page2.grid_rowconfigure(0, weight=0)
page2.grid_rowconfigure(1, weight=0)
page2.grid_rowconfigure(2, weight=0)
page2.grid_rowconfigure(3, weight=0)

page2.grid_columnconfigure(0, weight=1)

button_generation = tk.Button(page2, text="Згенерувати 10 масивів", font=("Courier New", 18), command=lambda: generate_ten_arrays(page2, 1))
button_generation.grid(row=0, column=0, sticky="ew", columnspan=2)

notebook.add(page2, text="Генерація")

# Створення третьої сторінки
page3 = ttk.Frame(notebook)
page3.grid_rowconfigure(0, weight=0)
page3.grid_rowconfigure(1, weight=0)
page3.grid_rowconfigure(2, weight=0)
page3.grid_rowconfigure(3, weight=0)

page3.grid_columnconfigure(0, weight=1)
page3.grid_columnconfigure(1, weight=1)

label_input_arrays = tk.Label(page3, text="Введіть 5 масивів (через пробіл)", font=("Courier New", 20))
label_input_arrays.grid(row=0, column=0, sticky="ew", columnspan=2)

label_input_array1 = tk.Label(page3, text="Масив 1:", font=("Courier New", 18))
label_input_array1.grid(row=1, column=0, sticky="ew")
entry_input_array1 = tk.Entry(page3, font=("Courier New", 20))
entry_input_array1.grid(row=1, column=1, sticky="ew")

label_input_array2 = tk.Label(page3, text="Масив 2:", font=("Courier New", 18))
label_input_array2.grid(row=2, column=0, sticky="ew")
entry_input_array2 = tk.Entry(page3, font=("Courier New", 20))
entry_input_array2.grid(row=2, column=1, sticky="ew")

label_input_array3 = tk.Label(page3, text="Масив 3:", font=("Courier New", 18))
label_input_array3.grid(row=3, column=0, sticky="ew")
entry_input_array3 = tk.Entry(page3, font=("Courier New", 20))
entry_input_array3.grid(row=3, column=1, sticky="ew")

label_input_array4 = tk.Label(page3, text="Масив 4:", font=("Courier New", 18))
label_input_array4.grid(row=4, column=0, sticky="ew")
entry_input_array4 = tk.Entry(page3, font=("Courier New", 20))
entry_input_array4.grid(row=4, column=1, sticky="ew")

label_input_array5 = tk.Label(page3, text="Масив 5:", font=("Courier New", 18))
label_input_array5.grid(row=5, column=0, sticky="ew")
entry_input_array5 = tk.Entry(page3, font=("Courier New", 20))
entry_input_array5.grid(row=5, column=1, sticky="ew")

entries=[entry_input_array1, entry_input_array2, entry_input_array3, entry_input_array4, entry_input_array5]

def sort_arrays_page3(entries):
    list_ = []
    sizes_list = []
    times_list = []
    for i in range( 0, 5 ):
        input_str = entries[i].get()
        if is_valid_input( input_str ):
            number_list = input_str.split()
            number_list = [int( num ) for num in number_list]
            start_time = time.time()
            radixSort( number_list )
            end_time = time.time()
            elapsed_time = end_time - start_time
            list_.append( number_list )
            sizes_list.append( len( number_list ))
            times_list.append( elapsed_time )
        else:
            messagebox.showinfo( 'Помилка', 'Введіть цілі числа через пробіл!' )
            for entry in entries:
                entry.delete( 0, tk.END )
            return

    for i, entry in enumerate( entries ):
        entry.delete( 0, tk.END )
        entry.insert( 0, ' '.join( map( str, list_[i] ) ) )

    label_res = tk.Label( page3, text="Масиви відсортовано", font=("Courier New", 18) )
    label_res.grid( row=6, column=0, sticky="ew", columnspan=2 )

    btn_graph = tk.Button( page3, text="Побудувати графік", font=("Courier New", 18),
                           command=lambda: graph_input( sizes_list, times_list ) )
    btn_graph.grid( row=9, column=0, sticky="ew", columnspan=2 )

    btn_graph_teor = tk.Button( page3, text="Побудувати теоретичний графік", font=("Courier New", 18),
                                command=lambda: graph_teor( list_ ) )
    btn_graph_teor.grid( row=10, column=0, sticky="ew", columnspan=2 )

btn_sort_arrays = tk.Button(page3, text='Сортувати', font=("Courier New", 18), command=lambda: sort_arrays_page3(entries))
btn_sort_arrays.grid(row=8, column=0, sticky="ew", columnspan=2 )

btn_read_arrays = tk.Button(page3, text='Зчитати дані з файлу', font=("Courier New", 18), command=lambda: read_values_from_file(entries))
btn_read_arrays.grid(row=7, column=0, sticky="ew", columnspan=2 )


notebook.add(page3, text="Ручний ввід")

notebook.pack(padx=10, pady=10, fill="both", expand=True)

notebook.pack(padx=10, pady=10)

app.mainloop()


