import utils.erosion as erosion
import utils.dilatacion as dilatacion
import utils.sal_y_pimienta as sal_y_pimienta
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import time
from tkinter import filedialog


# Función para actualizar la imagen en el label
def update_image(label):
    img = Image.fromarray(img_array_global)
    
    # Ajustar la imagen al tamaño de la ventana
    max_width = window.winfo_screenwidth() - 100  # Un margen para la ventana
    max_height = window.winfo_screenheight() - 350  # Un margen para la barra superior e inferior
    img.thumbnail((max_width, max_height))  # Redimensionar manteniendo la proporción
    
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk  # Evitar que la imagen sea recolectada por el garbage collector

def aplicar_erocion(img_array, figura, multithreading):
    global img_array_global
    start_time = time.time()  # Captura el tiempo de inicio
    img_array_global = erosion.erosion(img_array, figura, multithreading)
    end_time = time.time()  # Captura el tiempo de finalización
    execution_time = end_time - start_time
    update_image(label)
    tiempo_ejecucion.config(text=f"{execution_time:.3f} segundos")


def aplicar_dilatacion(img_array, figura, multithreading):
    global img_array_global
    start_time = time.time()  # Captura el tiempo de inicio
    img_array_global = dilatacion.dilatacion(img_array, figura, multithreading)
    end_time = time.time()  # Captura el tiempo de finalización
    execution_time = end_time - start_time
    update_image(label)
    tiempo_ejecucion.config(text=f"{execution_time:.3f} segundos")

def aplicar_ruido(img_array, noise_level):
    global img_array_global 
    start_time = time.time()  # Captura el tiempo de inicio
    img_array_global = sal_y_pimienta.add_noise(img_array, noise_level)
    end_time = time.time()  # Captura el tiempo de finalización
    execution_time = end_time - start_time
    update_image(label)
    tiempo_ejecucion.config(text=f"{execution_time:.3f} segundos")

def reset_image(image_path):
    global img_array_global
    img = Image.open(image_path)
    img_array_global = np.array(img)
    update_image(label)

def seleccionar_figura(figura, nombre):
    global figura_seleccionada
    global nombre_figura_seleccionada
    figura_seleccionada = figura
    nombre_figura_seleccionada = nombre
    update_figura(figura_seleccionada_label, figura_seleccionada)

def update_figura(label, figura):
    figura_tk = ImageTk.PhotoImage(figura)
    label.config(image=figura_tk)
    label.image = figura_tk

def seleccionar_imagen():
    global image_path
    image_path = filedialog.askopenfilename()
    img = Image.open(image_path)
    img_array = np.array(img)
    global img_array_global
    img_array_global = img_array
    
    # Ajustar la imagen al tamaño de la ventana
    max_width = window.winfo_screenwidth() - 100  # Un margen para la ventana
    max_height = window.winfo_screenheight() - 350  # Un margen para la barra superior e inferior
    img.thumbnail((max_width, max_height))  # Redimensionar manteniendo la proporción
    
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk  # Evitar que la imagen sea recolectada por el garbage collector
    width, height = img.size

    if width < 550:
        width = 550

    window.geometry(f"{width}x{height+230}")

    label.pack(pady=10)

    seleccionar_imagen_label.pack_forget()
    seleccionar_imagen_button.pack_forget()

    control_frame.pack(pady=10)
    nivel_ruido_label.pack(side=LEFT, padx=5)
    nivel_ruido.pack(side=LEFT, padx=2)
    agregar_ruido.pack(side=LEFT, padx=10)

    figura_frame.pack(pady=10)
    figura_label_seleccionada.pack(side=LEFT, padx=5)
    figura_seleccionada_label.pack(side=LEFT, padx=5)
    figura_label.pack(side=LEFT, padx=5)
    figura_original_button.pack(side=LEFT, padx=5)
    figura1_button.pack(side=LEFT, padx=5)
    figura2_button.pack(side=LEFT, padx=5)
    figura3_button.pack(side=LEFT, padx=5)
    figura4_button.pack(side=LEFT, padx=5)
    figura5_button.pack(side=LEFT, padx=5)

    button_frame.pack(pady=10)
    erosion_button.pack(side=LEFT, padx=10)
    dilatacion_button.pack(side=LEFT, padx=10)
    reset_button.pack(side=LEFT, padx=10)

    multithreading_frame.pack(pady=10)
    multithreading_label.pack(side=LEFT, padx=5)
    multithreading_checkbutton.pack(side=LEFT, padx=5)
    tiempo_label.pack(side=LEFT, padx=15)
    tiempo_ejecucion.pack(side=LEFT, padx=5)



# Crear la ventana
window = Tk()
window.title("Procesamiento de Imágenes")
window.configure(background="black")

window.geometry("300x300")

# Etiqueta "Seleccionar imagen"
seleccionar_imagen_label = Label(window, text="Seleccionar imagen:", bg="black", fg="white")
seleccionar_imagen_label.place(relx=0.5, rely=0.3, anchor="center")  # Centrado en el 30% de la altura

# Botón para seleccionar imagen
seleccionar_imagen_button = Button(window, text="Seleccionar imagen", command=seleccionar_imagen)
seleccionar_imagen_button.place(relx=0.5, rely=0.5, anchor="center")  # Centrado en el 50% de la altura


# Label para mostrar la imagen
label = Label(window)
label.pack_forget()

# Crear un frame para los controles debajo de la imagen
control_frame = Frame(window, bg="black")
control_frame.pack_forget()

# Etiqueta para "Nivel de ruido"
nivel_ruido_label = Label(control_frame, text="Nivel de ruido:", bg="black", fg="white")
nivel_ruido_label.pack_forget()

# Input para nivel de ruido
nivel_ruido = Entry(control_frame, width=4)
nivel_ruido.pack_forget()

# Botón para agregar ruido
agregar_ruido = Button(control_frame, text="Agregar ruido", command=lambda: aplicar_ruido(img_array_global, float(nivel_ruido.get())))
agregar_ruido.pack_forget()

# Frame para seleccionar la figura
figura_frame = Frame(window, bg="black")
figura_frame.pack_forget()

# Etiqueta para "Figura seleccionada"
figura_label_seleccionada = Label(figura_frame, text="Figura seleccionada:", bg="black", fg="white")
figura_label_seleccionada.pack_forget()

# Inicializar la figuras
figura_original = Image.open("./assets/figura_original.png")
figura_original = figura_original.resize((20, 20))
figura_original_tk = ImageTk.PhotoImage(figura_original)

figura1 = Image.open("./assets/figura1.png")
figura1 = figura1.resize((20, 20))
figura1_tk = ImageTk.PhotoImage(figura1)

figura2 = Image.open("./assets/figura2.png")
figura2 = figura2.resize((20, 20))
figura2_tk = ImageTk.PhotoImage(figura2)

figura3 = Image.open("./assets/figura3.png")
figura3 = figura3.resize((30, 20))
figura3_tk = ImageTk.PhotoImage(figura3)

figura4 = Image.open("./assets/figura4.png")
figura4 = figura4.resize((15, 20))
figura4_tk = ImageTk.PhotoImage(figura4)

figura5 = Image.open("./assets/figura5.png")
figura5 = figura5.resize((20, 20))
figura5_tk = ImageTk.PhotoImage(figura5)

# Figura seleccionada

figura_seleccionada = figura_original
nombre_figura_seleccionada = "figura_original"

figura_seleccionada_tk = ImageTk.PhotoImage(figura_seleccionada)

figura_seleccionada_label = Label(figura_frame, image=figura_seleccionada_tk)
figura_seleccionada_label.pack_forget()
figura_seleccionada_label.image = figura_seleccionada_tk

# Etiqueta para "Seleccionar figura"
figura_label = Label(figura_frame, text="Seleccionar figura:", bg="black", fg="white")
figura_label.pack_forget()

# Botón para seleccionar figura original
figura_original_button = Button(figura_frame, image=figura_original_tk, command=lambda: seleccionar_figura(figura_original, "figura_original"))
figura_original_button.pack_forget()
figura_original_button.image = figura_original_tk

# Botón para seleccionar figura 1
figura1_button = Button(figura_frame, image=figura1_tk, command=lambda: seleccionar_figura(figura1, "figura1"))
figura1_button.pack_forget()
figura1_button.image = figura1_tk

# Botón para seleccionar figura 2
figura2_button = Button(figura_frame, image=figura2_tk, command=lambda: seleccionar_figura(figura2, "figura2"))
figura2_button.pack_forget()
figura2_button.image = figura2_tk

# Botón para seleccionar figura 3
figura3_button = Button(figura_frame, image=figura3_tk, command=lambda: seleccionar_figura(figura3, "figura3"))
figura3_button.pack_forget()
figura3_button.image = figura3_tk

# Botón para seleccionar figura 4
figura4_button = Button(figura_frame, image=figura4_tk, command=lambda: seleccionar_figura(figura4, "figura4"))
figura4_button.pack_forget()
figura4_button.image = figura4_tk

# Botón para seleccionar figura 5
figura5_button = Button(figura_frame, image=figura5_tk, command=lambda: seleccionar_figura(figura5, "figura5"))
figura5_button.pack_forget()
figura5_button.image = figura5_tk


# Frame para los botones de procesamiento de imágenes
button_frame = Frame(window, bg="black")
button_frame.pack_forget()

# Botón para aplicar erosión
erosion_button = Button(button_frame, text="Aplicar erosión", command=lambda: aplicar_erocion(img_array_global, nombre_figura_seleccionada, multithreading.get()))
erosion_button.pack_forget()

# Botón para aplicar dilatación
dilatacion_button = Button(button_frame, text="Aplicar dilatación", command=lambda: aplicar_dilatacion(img_array_global, nombre_figura_seleccionada, multithreading.get()))
dilatacion_button.pack_forget()

# Botón para resetear la imagen
img_reset = Image.open("./assets/reset.png")
img_reset = img_reset.resize((20, 20))
reset_img = ImageTk.PhotoImage(img_reset)  # Convert PIL Image to PhotoImage
reset_button = Button(button_frame, image=reset_img, command=lambda: reset_image(image_path))
reset_button.pack_forget()
reset_button.image = reset_img

# Frame para activar multithreading
multithreading_frame = Frame(window, bg="black")
multithreading_frame.pack_forget()

# Etiqueta para "Multithreading"
multithreading_label = Label(multithreading_frame, text="Multithreading:", bg="black", fg="white")
multithreading_label.pack_forget()

# Variable para activar/desactivar multithreading
multithreading = IntVar()
multithreading_checkbutton = Checkbutton(multithreading_frame, variable=multithreading)
multithreading_checkbutton.pack_forget()

# Etiqueta para "Tiempo de ejecución"
tiempo_label = Label(multithreading_frame, text="Tiempo de ejecución: ", bg="black", fg="white")
tiempo_label.pack_forget()

# Etiqueta para mostrar el tiempo de ejecución
tiempo_ejecucion = Label(multithreading_frame, text="    ", fg="black")
tiempo_ejecucion.pack_forget()

# Ejecutar el loop de la ventana
window.mainloop()