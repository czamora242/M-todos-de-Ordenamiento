import random
import time
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview, Entry, Button, Label

# Algoritmos de ordenamiento
def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def selection_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x <= pivot]
    greater = [x for x in arr[1:] if x > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = merge_sort(arr[:mid])
        R = merge_sort(arr[mid:])
        return merge(L, R)
    return arr

def merge(left, right):
    result = []
    while left and right:
        result.append(left.pop(0) if left[0] < right[0] else right.pop(0))
    result.extend(left or right)
    return result

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n//2 - 1, -1, -1):
        heapify(a, n, i)
    for i in range(n-1, 0, -1):
        a[i], a[0] = a[0], a[i]
        heapify(a, i, 0)
    return a

# --- Función para medir tiempos ---
def medir_tiempos(arr):
    algoritmos = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort
    }
    tiempos = {}
    for nombre, func in algoritmos.items():
        inicio = time.time()
        func(arr)
        fin = time.time()
        tiempos[nombre] = (fin - inicio) * 1000
    return tiempos

# --- Interfaz gráfica ---
def mostrar_resultados():
    style = Style(theme="superhero")  # Tema más colorido y moderno
    root = style.master
    root.title("Comparación de Algoritmos de Ordenamiento")
    root.geometry("600x400")

    # Título
    title_label = Label(root, text="Comparación de Algoritmos", font=("Helvetica", 18, "bold"), bootstyle="info")
    title_label.pack(pady=10)

    # Contenedor de entrada
    entry_frame = tk.LabelFrame(root, text="Configuración", bg="#2b2b2b", fg="white", padx=10, pady=10)
    entry_frame.pack(padx=10, pady=5, fill="x")

    lbl = Label(entry_frame, text="Cantidad de números aleatorios:", bootstyle="info")
    lbl.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    entry = Entry(entry_frame, width=20, bootstyle="dark")
    entry.grid(row=0, column=1, padx=5, pady=5)

    # Botón de ejecutar
    def ejecutar():
        try:
            cantidad = int(entry.get())
            arr = [random.randint(1, 10000) for _ in range(cantidad)]
            tiempos = medir_tiempos(arr)

            for row in tree.get_children():
                tree.delete(row)
            for alg, tiempo in tiempos.items():
                tree.insert("", "end", values=(alg, f"{tiempo:.4f} ms"))
        except ValueError:
            print("Ingresa un número válido")

    btn = Button(entry_frame, text="Ejecutar", bootstyle="success-outline", command=ejecutar)
    btn.grid(row=0, column=2, padx=10, pady=5)

    # Tabla de resultados
    tree = Treeview(root, columns=("Algoritmo", "Tiempo"), show="headings", bootstyle="dark")
    tree.heading("Algoritmo", text="Algoritmo")
    tree.heading("Tiempo", text="Tiempo (ms)")
    tree.column("Algoritmo", anchor="center", width=200)
    tree.column("Tiempo", anchor="center", width=150)
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    root.mainloop()

# --- Ejecutar interfaz ---
if __name__ == "__main__":
    mostrar_resultados()
