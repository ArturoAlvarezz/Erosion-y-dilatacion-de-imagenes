import numpy as np

# Supongamos que "img" es tu array RGB original (alto, ancho, 3)
# Donde img.shape = (alto, ancho, 3)
def agregar_borde(img):
    alto, ancho, canales = img.shape
    
    # Crear una nueva imagen con un tamaño aumentado en 2 filas y 2 columnas
    nueva_img = np.zeros((alto + 2, ancho + 2, canales), dtype=img.dtype)
    
    # Copiar la imagen original en el centro del nuevo array
    nueva_img[1:alto+1, 1:ancho+1] = img
    
    # Copiar los bordes de la imagen original en el borde de la nueva imagen
    # Bordes horizontales
    nueva_img[0, 1:ancho+1] = img[0, :]  # Fila superior
    nueva_img[-1, 1:ancho+1] = img[-1, :]  # Fila inferior
    
    # Bordes verticales
    nueva_img[1:alto+1, 0] = img[:, 0]  # Columna izquierda
    nueva_img[1:alto+1, -1] = img[:, -1]  # Columna derecha
    
    # Esquinas
    nueva_img[0, 0] = img[0, 0]  # Esquina superior izquierda
    nueva_img[0, -1] = img[0, -1]  # Esquina superior derecha
    nueva_img[-1, 0] = img[-1, 0]  # Esquina inferior izquierda
    nueva_img[-1, -1] = img[-1, -1]  # Esquina inferior derecha
    
    return nueva_img