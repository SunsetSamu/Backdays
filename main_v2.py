import os
from zipfile import ZipFile
from datetime import datetime

# Obtener el nombre del script para excluirlo del archivo zip
script_name = os.path.basename(__file__)

# Listar todos los archivos en el directorio actual
files_to_zip = []
for root, dirs, files in os.walk('.'):
    for file in files:
        # Excluir el script actual y archivos ZIP que contengan "backup" en el nombre
        if file != script_name and not ("backup" in file.lower() and file.endswith('.zip')):
            files_to_zip.append(os.path.join(root, file))


# Generar nombre único para el archivo ZIP basado en fecha y hora
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_filename = f"Backup_{timestamp}.zip"

# Escribir en el archivo ZIP
with ZipFile(zip_filename, 'w') as zip_file:
    for file in files_to_zip:
        zip_file.write(file)

print(f"¡Archivo ZIP '{zip_filename}' creado exitosamente!")
