# M-todos-de-Ordenamiento
import random
import time
import tkinter as tk
from tkinter.ttk import Progressbar, Combobox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview, Entry, Button, Label

# --- Algoritmos de ordenamiento ---
def ordenamiento_burbuja(lista):
    copia = lista.copy()
    n = len(copia)
    for i in range(n):
        for j in range(0, n - i - 1):
            if copia[j] > copia[j + 1]:
                copia[j], copia[j + 1] = copia[j + 1], copia[j]
    return copia

def ordenamiento_insercion(lista):
    copia = lista.copy()
    for i in range(1, len(copia)):
        clave = copia[i]
        j = i - 1
        while j >= 0 and clave < copia[j]:
            copia[j + 1] = copia[j]
            j -= 1
        copia[j + 1] = clave
    return copia

def ordenamiento_seleccion(lista):
    copia = lista.copy()
    for i in range(len(copia)):
        min_idx = i
        for j in range(i + 1, len(copia)):
            if copia[j] < copia[min_idx]:
                min_idx = j
        copia[i], copia[min_idx] = copia[min_idx], copia[i]
    return copia

def ordenamiento_rapido(lista):
    if len(lista) <= 1:
        return lista
    else:
        pivote = lista[0]
        menores = [x for x in lista[1:] if x <= pivote]
        mayores = [x for x in lista[1:] if x > pivote]
        return ordenamiento_rapido(menores) + [pivote] + ordenamiento_rapido(mayores)

def ordenamiento_merge(lista):
    if len(lista) <= 1:
        return lista
    mitad = len(lista) // 2
    izquierda = ordenamiento_merge(lista[:mitad])
    derecha = ordenamiento_merge(lista[mitad:])
    return combinar_listas(izquierda, derecha)

def combinar_listas(izquierda, derecha):
    resultado = []
    while izquierda and derecha:
        resultado.append(izquierda.pop(0) if izquierda[0] < derecha[0] else derecha.pop(0))
    resultado.extend(izquierda or derecha)
    return resultado

def heapify(lista, n, i):
    mayor = i
    izquierda = 2 * i + 1
    derecha = 2 * i + 2
    if izquierda < n and lista[izquierda] > lista[mayor]:
        mayor = izquierda
    if derecha < n and lista[derecha] > lista[mayor]:
        mayor = derecha
    if mayor != i:
        lista[i], lista[mayor] = lista[mayor], lista[i]
        heapify(lista, n, mayor)

def ordenamiento_heap(lista):
    copia = lista.copy()
    n = len(copia)
    for i in range(n // 2 - 1, -1, -1):
        heapify(copia, n, i)
    for i in range(n - 1, 0, -1):
        copia[i], copia[0] = copia[0], copia[i]
        heapify(copia, i, 0)
    return copia

# --- Medición de tiempo ---
def medir_tiempos(lista, repeticiones=10):
    algoritmos = {
        "Burbuja": ordenamiento_burbuja,
        "Inserción": ordenamiento_insercion,
        "Selección": ordenamiento_seleccion,
        "Rápido": ordenamiento_rapido,
        "Merge": ordenamiento_merge,
        "Heap": ordenamiento_heap
    }
    tiempos = {}
    for nombre, funcion in algoritmos.items():
        total = 0
        for _ in range(repeticiones):
            copia = lista.copy()
            inicio = time.time()
            funcion(copia)
            fin = time.time()
            total += (fin - inicio)
        tiempos[nombre] = (total / repeticiones) * 1000  # milisegundos
    return tiempos

# --- Interfaz Gráfica ---
def mostrar_resultados():
    estilo = Style(theme="morph")  # Tema inicial
    ventana = estilo.master
    ventana.title("Comparación de Algoritmos de Ordenamiento")
    ventana.geometry("800x650")
    claro = "morph"
    oscuro = "darkly"

    Label(ventana, text="Comparación de Algoritmos", font=("Arial", 20, "bold"), bootstyle="info").pack(pady=10)

    # Selección de tema
    frame_tema = tk.Frame(ventana)
    frame_tema.pack(padx=10, pady=5, fill="x")

    Label(frame_tema, text="Selecciona un tema:", bootstyle="info").grid(row=0, column=0, padx=5, pady=5)

    temas_disponibles = [claro, oscuro]
    combobox_tema = Combobox(frame_tema, values=temas_disponibles, state="readonly")
    combobox_tema.grid(row=0, column=1, padx=5, pady=5)
    combobox_tema.set("morph")  # Tema por defecto

    def cambiar_tema(event):
        nuevo_tema = combobox_tema.get()
        estilo.theme_use(nuevo_tema)

    combobox_tema.bind("<<ComboboxSelected>>", cambiar_tema)

    # Entrada de cantidad
    frame_entrada = tk.Frame(ventana)
    frame_entrada.pack(padx=10, pady=5, fill="x")

    Label(frame_entrada, text="Cantidad de números (máx 200):", bootstyle="info").grid(row=0, column=0, padx=5, pady=5)

    entrada_cantidad = Entry(frame_entrada, width=10, bootstyle="dark")
    entrada_cantidad.grid(row=0, column=1, padx=5, pady=5)

    boton_ejecutar = Button(frame_entrada, text="Ejecutar", bootstyle="success")
    boton_ejecutar.grid(row=0, column=2, padx=10, pady=5)

    # Barra de progreso
    barra_progreso = Progressbar(ventana, mode="indeterminate", length=200)
    barra_progreso.pack(pady=10)

    # Tabla de resultados
    tabla_resultados = Treeview(ventana, columns=("Algoritmo", "Tiempo"), show="headings", bootstyle="dark")
    tabla_resultados.heading("Algoritmo", text="Algoritmo")
    tabla_resultados.heading("Tiempo", text="Tiempo (ms)")
    tabla_resultados.column("Algoritmo", anchor="center", width=200)
    tabla_resultados.column("Tiempo", anchor="center", width=150)
    tabla_resultados.pack(padx=10, pady=10, fill="both", expand=True)

    etiqueta_estado = Label(ventana, text="", font=("Arial", 12, "italic"), bootstyle="secondary")
    etiqueta_estado.pack(pady=5)

    def ejecutar():
        try:
            cantidad = int(entrada_cantidad.get())
            if cantidad < 1 or cantidad > 200:
                etiqueta_estado.config(text="⚠️ Ingresa un número entre 1 y 200.")
                return

            lista_numeros = [random.randint(1, 10000) for _ in range(cantidad)]

            barra_progreso.start(10)
            ventana.after(1500, lambda: mostrar_resultado_final(lista_numeros))
        except ValueError:
            etiqueta_estado.config(text="⚠️ Ingresa un número válido.")

    def mostrar_resultado_final(lista_numeros):
        tiempos = medir_tiempos(lista_numeros)
        barra_progreso.stop()
        etiqueta_estado.config(text="✅ Procesamiento completo")

        for fila in tabla_resultados.get_children():
            tabla_resultados.delete(fila)

        for algoritmo, tiempo in tiempos.items():
            tabla_resultados.insert("", "end", values=(algoritmo, f"{tiempo:.4f} ms"))

    boton_ejecutar.config(command=ejecutar)
    ventana.mainloop()

# --- Ejecutar programa ---
if __name__ == "__main__":
    mostrar_resultados() 
