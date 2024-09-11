import numpy as np
from PIL import Image
import utils.bordes as bordes
from multiprocessing import Pool, cpu_count

def erosionar_la_imagen(args):
    img_array, start, end, width, figura = args

    if start == 0:
        start = 1
    if end >= img_array.shape[0]:
        end = img_array.shape[0] - 1

    img_resultado = np.zeros((end - start, width - 2, 3), dtype=np.uint8)

    for i in range(start, end):
        for j in range(1, width - 1):

            match figura:
                case "figura_original":
                    vecinos = [
                        img_array[i-1, j],  # Arriba (RGB)
                        img_array[i+1, j],  # Abajo (RGB)
                        img_array[i, j],    # Centro (RGB)
                        img_array[i, j-1],  # Izquierda (RGB)
                        img_array[i, j+1]   # Derecha (RGB)
                    ]
                case "figura1":
                    vecinos = [
                        img_array[i+1, j],  # Abajo (RGB)
                        img_array[i, j-1],  # Izquierda (RGB)
                        img_array[i, j]   # Centro (RGB)
                    ]
                case "figura2":
                    vecinos = [
                        img_array[i-1, j],  # Arriba (RGB)
                        img_array[i, j-1],  # Izquierda (RGB)
                        img_array[i, j]   # Centro (RGB)
                    ]
                case "figura3":
                    vecinos = [
                        img_array[i, j+1],  # Derecha (RGB)
                        img_array[i, j],   # Centro (RGB)
                        img_array[i, j-1]  # Izquierda (RGB)
                    ]
                case "figura4":
                    vecinos = [
                        img_array[i, j],    # Centro (RGB)
                        img_array[i+1, j],  # Abajo (RGB)
                    ]
                case "figura5":
                    vecinos = [
                        img_array[i-1,j-1],  # Arriba Izquierda (RGB)
                        img_array[i-1,j+1],  # Arriba Derecha (RGB)
                        img_array[i,j],      # Centro (RGB)
                        img_array[i+1,j-1],  # Abajo Izquierda (RGB)
                        img_array[i+1,j+1]   # Abajo Derecha (RGB)

                    ]
      
            vecinos = np.array(vecinos)
            
            max_rgb = np.max(vecinos, axis=0)
            
            img_resultado[i-start, j-1] = max_rgb
    
    return img_resultado

def erosion(img_array, figura, multithreading):
    img_array = bordes.agregar_borde(img_array)
    height, width, _ = [len(img_array), len(img_array[0]), len(img_array[0][0])]

    if not multithreading:
        return erosionar_la_imagen((img_array, 1, height - 1, width, figura))
    
    num_processes = cpu_count()
    chunk_size = height // num_processes + 1
    
    pool = Pool(processes=num_processes)
    args = [(img_array, i * chunk_size, (i + 1) * chunk_size, width, figura) for i in range(num_processes)]
    results = pool.map(erosionar_la_imagen, args)
    
    img_resultado = np.vstack(results)

    return img_resultado