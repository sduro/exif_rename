"""
Este programa renombra los archivos JPG en un directorio usando la fecha de captura de la foto.
Si la fecha de captura no está disponible en los datos EXIF, el archivo conserva su nombre original.
"""

import os
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    # Abre la imagen y obtiene los datos EXIF
    image = Image.open(image_path)
    exif_data = image._getexif()
    if not exif_data:
        return None
    # Convierte los datos EXIF en un diccionario legible
    exif = {TAGS.get(tag): value for tag, value in exif_data.items() if tag in TAGS}
    return exif

def get_date_taken(exif_data):
    # Obtiene la fecha de captura de los datos EXIF
    date_taken = exif_data.get('DateTimeOriginal')
    if date_taken:
        # Elimina los dos puntos de la fecha y reemplaza el espacio por un guion bajo
        return date_taken.replace(':', '').replace(' ', '_')
    return None

def rename_files_in_directory(directory):
    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(directory, filename)
            exif_data = get_exif_data(file_path)
            if exif_data:
                date_taken = get_date_taken(exif_data)
                if date_taken:
                    # Construye el nuevo nombre de archivo usando la fecha de captura
                    new_filename = f"{date_taken}.jpg"
                    new_file_path = os.path.join(directory, new_filename)
                    
                    # Renombra el archivo
                    os.rename(file_path, new_file_path)
                    print(f'Renombrado: {filename} a {new_filename}')
                else:
                    print(f'{filename}: No se encontró la fecha de captura en los datos EXIF.')
            else:
                print(f'{filename}: No se encontraron datos EXIF.')

# Cambia 'tu_directorio' por el directorio donde están tus fotos
rename_files_in_directory(r'C:\Users\sduro\Downloads')
