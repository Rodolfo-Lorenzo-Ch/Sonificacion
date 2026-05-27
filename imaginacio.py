from PIL import Image
from scipy.io import wavfile

def sonido_a_imagen(ruta_audio, ruta_imagen, ancho=100, alto=60):
    # 1. Leer el archivo de audio
    sample_rate, datos_audio = wavfile.read(ruta_audio)
    
    # Si el audio es estéreo (2 canales), lo convertimos a mono promediándolos
    if len(datos_audio.shape) > 1:
        datos_audio = datos_audio.mean(axis=1)
    
    # Normalizar el audio entrante entre -1 y 1
    datos_audio = datos_audio / np.max(np.abs(datos_audio))
    
    # 2. Configurar el mismo mapa de frecuencias del script anterior
    frecuencias_objetivo = np.linspace(2000, 200, alto)
    
    # Dividir el audio en la cantidad de columnas (ancho de la imagen)
    muestras_por_columna = len(datos_audio) // ancho
    
    # Crear una matriz vacía para la imagen (filas x columnas)
    matriz_imagen = np.zeros((alto, ancho), dtype=np.uint8)
    
    # 3. Analizar el audio columna por columna
    for x in range(ancho):
        # Extraer el fragmento de audio que corresponde a esta columna de tiempo
        inicio = x * muestras_por_columna
        fin = inicio + muestras_por_columna
        fragmento = datos_audio[inicio:fin]
        
        t_columna = np.linspace(0, muestras_por_columna / sample_rate, muestras_por_columna)
        
        # Para cada fila (frecuencia), medimos qué tanto "encaja" con el fragmento de audio
        for y in range(alto):
            frecuencia = frecuencias_objetivo[y]
            
            # Creamos una onda de referencia pura con la frecuencia que buscamos
            onda_referencia = np.sin(2 * np.pi * frecuencia * t_columna)
            
            # Multiplicamos el fragmento por la referencia (esto es una correlación básica)
            # Si la frecuencia existe en el audio, el resultado será un número alto
            energia = np.abs(np.sum(fragmento * onda_referencia))
            
            # Guardamos la energía en la matriz
            matriz_imagen[y, x] = energia

    # 4. Normalizar el brillo de la imagen para que se vea correctamente
    max_energia = np.max(matriz_imagen)
    if max_energia > 0:
        # Escalamos los valores para que el máximo sea 255 (blanco puro)
        matriz_imagen = ((matriz_imagen / max_energia) * 255).astype(np.uint8)
    
    # 5. Crear la imagen y guardarla
    img = Image.fromarray(matriz_imagen, 'L')
    img.save(ruta_imagen)
    print(f"¡Imagen reconstruida con éxito en: {ruta_imagen}!")

# 6. EJECUCIÓN DEL PROGRAMA
# Usamos el audio que generaste antes para ver cómo se reconstruye
sonido_a_imagen(
    "/home/rudul/practicas_python/resultado_sonoro.wav", 
    "/home/rudul/practicas_python/noche_reconstruida.jpg"
)