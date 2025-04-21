import random
import time
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview, Entry, Button, Label

# --- Algoritmos de ordenamiento ---
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
        for j in range(i + 1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        menores = [x for x in arr[1:] if x <= pivot]
        mayores = [x for x in arr[1:] if x > pivot]
        return quick_sort(menores) + [pivot] + quick_sort(mayores)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    L = merge_sort(arr[:mid])
    R = merge_sort(arr[mid:])
    return merge(L, R)

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
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i)
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        heapify(a, i, 0)
    return a

# --- Medición de tiempo (con repeticiones) ---
def medir_tiempos(arr, repeticiones=10):
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
        total = 0
        for _ in range(repeticiones):
            copia = arr.copy()
            inicio = time.time()
            func(copia)
            fin = time.time()
            total += (fin - inicio)
        promedio = (total / repeticiones) * 1000  # milisegundos
        tiempos[nombre] = promedio
    return tiempos

# --- Interfaz Gráfica ---
def mostrar_resultados():
    style = Style(theme="superhero")
    root = style.master
    root.title("Comparación de Algoritmos de Ordenamiento")
    root.geometry("780x620")

    Label(root, text="Comparación de Algoritmos", font=("Helvetica", 18, "bold"), bootstyle="info").pack(pady=10)

    # Entrada
    entry_frame = tk.Frame(root, bg="#2b2b2b")
    entry_frame.pack(padx=10, pady=5, fill="x")

    Label(entry_frame, text="Cantidad de números aleatorios (máx 200):", bootstyle="info").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    entry = Entry(entry_frame, width=20, bootstyle="dark")
    entry.grid(row=0, column=1, padx=5, pady=5)

    btn = Button(entry_frame, text="Ejecutar", bootstyle="success-outline")
    btn.grid(row=0, column=2, padx=10, pady=5)

    Label(root, text="Lista generada:", bootstyle="warning").pack(pady=(10, 0))

    txt_output = ScrolledText(root, height=4, wrap="word", font=("Consolas", 10))
    txt_output.pack(padx=10, pady=5, fill="x")

    tree = Treeview(root, columns=("Algoritmo", "Tiempo"), show="headings", bootstyle="dark")
    tree.heading("Algoritmo", text="Algoritmo")
    tree.heading("Tiempo", text="Tiempo promedio (ms)")
    tree.column("Algoritmo", anchor="center", width=200)
    tree.column("Tiempo", anchor="center", width=180)
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    status_label = Label(root, text="", font=("Helvetica", 10, "italic"), bootstyle="secondary")
    status_label.pack(pady=5)

    animando = {"activo": False}

    def animar_texto():
        if not animando["activo"]:
            return
        puntos = (animar_texto.contador % 4) * "."
        status_label.config(text=f"Analizando algoritmos{puntos}")
        animar_texto.contador += 1
        root.after(300, animar_texto)
    animar_texto.contador = 0

    def ejecutar():
        try:
            cantidad = int(entry.get())
            if cantidad < 1 or cantidad > 200:
                status_label.config(text="⚠️ Ingresa un número entre 1 y 200.")
                return

            arr = [random.randint(1, 200) for _ in range(cantidad)]

            # Mostrar lista generada
            txt_output.delete("1.0", tk.END)
            txt_output.insert(tk.END, str(arr))

            animando["activo"] = True
            animar_texto()

            root.after(200, lambda: mostrar_resultado_final(arr))
        except ValueError:
            status_label.config(text="⚠️ Por favor, ingresa un número válido.")

    def mostrar_resultado_final(arr):
        tiempos = medir_tiempos(arr)
        animando["activo"] = False
        status_label.config(text="✅ Procesamiento completo")

        # Limpiar resultados anteriores
        for row in tree.get_children():
            tree.delete(row)

        for alg, tiempo in tiempos.items():
            if tiempo < 0.001:
                tiempo_str = "< 0.001 ms"
            else:
                tiempo_str = f"{tiempo:.8f} ms"
            tree.insert("", "end", values=(alg, tiempo_str))

    btn.config(command=ejecutar)
    root.mainloop()

# --- Ejecutar programa ---
if __name__ == "__main__":
    mostrar_resultados()
