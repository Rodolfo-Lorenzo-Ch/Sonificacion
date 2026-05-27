import numpy as np
from PIL import Image
from scipy.io import wavfile

# 1. AQUÍ DEFINES LA FUNCIÓN (Se queda con los nombres de las variables, no cambies nada aquí)
def imagen_a_sonido(ruta_imagen, ruta_audio, duracion_segundos=5, sample_rate=44100):
    img = Image.open(ruta_imagen).convert('L')
    
    ancho, alto = 100, 60
    img = img.resize((ancho, alto))
    matriz = np.array(img)
    
    frecuencias = np.linspace(2000, 200, alto) 
    tiempo_total = np.linspace(0, duracion_segundos, int(sample_rate * duracion_segundos))
    muestras_por_columna = len(tiempo_total) // ancho
    
    audio_final = np.array([], dtype=np.float32)
    
    for x in range(ancho):
        columna_audio = np.zeros(muestras_por_columna)
        t_columna = np.linspace(0, duracion_segundos / ancho, muestras_por_columna)
        
        for y in range(alto):
            brillo = matriz[y, x] / 255.0
            if brillo > 0.1:
                frecuencia = frecuencias[y]
                onda = brillo * np.sin(2 * np.pi * frecuencia * t_columna)
                columna_audio += onda
                
        audio_final = np.append(audio_final, columna_audio)
        
    if np.max(np.abs(audio_final)) > 0:
        audio_final = audio_final / np.max(np.abs(audio_final))
        
    audio_final = (audio_final * 32767).astype(np.int16)
    wavfile.write(ruta_audio, sample_rate, audio_final)
    print(f"¡Audio guardado exitosamente en: {ruta_audio}!")

# 2. AQUÍ ABAJO ES DONDE LE PASAS TUS RUTAS REALES (Al llamar a la función)
# Nota: Ponlas entre comillas porque son cadenas de texto (strings)
imagen_a_sonido(
    "/home/rudul/practicas_python/nebulosa.jpg", 
    "/home/rudul/practicas_python/resultado_sonoro2.wav", 
    duracion_segundos=20
)