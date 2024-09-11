import numpy as np
from PIL import Image
import random

def add_noise(img_array, noise_level):
    # Obtener las dimensiones de la imagen
    height, width, _ = [len(img_array), len(img_array[0]), len(img_array[0][0])]

    # Agregar ruido
    for i in range(height):
        for j in range(width):
            # Probabilidad de agregar ruido
            if random.random() < noise_level:
                
                if random.random() < 0.5:
                    # Ruido sal
                    value = 255
                else:
                    # Ruido pimienta
                    value = 0
                
                # Asignar el valor aleatorio a cada canal de color
                img_array[i, j] = [value, value, value]
    
    return img_array