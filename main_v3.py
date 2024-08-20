import os
from zipfile import ZipFile
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget

class BackupApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backup Creator")
        self.setGeometry(100, 100, 300, 150)

        # Layout y widgets
        self.layout = QVBoxLayout()

        self.label = QLabel("Selecciona la carpeta para respaldar:", self)
        self.layout.addWidget(self.label)

        self.select_folder_btn = QPushButton("Seleccionar Carpeta", self)
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_btn)

        self.create_backup_btn = QPushButton("Crear Backup", self)
        self.create_backup_btn.clicked.connect(self.create_backup)
        self.create_backup_btn.setEnabled(False)
        self.layout.addWidget(self.create_backup_btn)

        # Configuración del contenedor principal
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.folder_path = ""

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.folder_path = folder
            self.label.setText(f"Carpeta seleccionada: {self.folder_path}")
            self.create_backup_btn.setEnabled(True)

    def create_backup(self):
        if not self.folder_path:
            return

        files_to_zip = []
        script_name = os.path.basename(__file__)

        # Recorrer la carpeta seleccionada para agregar archivos al ZIP
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file != script_name and not ("backup" in file.lower() and file.endswith('.zip')) and not file.endswith('.1~') and not file.endswith('.2~') and not file.endswith('.3~'):
                    relative_path = os.path.relpath(os.path.join(root, file), self.folder_path)
                    files_to_zip.append(relative_path)


        # Generar nombre único para el archivo ZIP basado en fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = os.path.basename(self.folder_path)
        zip_filename = os.path.join(self.folder_path, f"Backup_{folder_name}_{timestamp}.zip")


        # Escribir en el archivo ZIP
        with ZipFile(zip_filename, 'w') as zip_file:
            for file in files_to_zip:
                zip_file.write(file)

        self.label.setText(f"¡Backup creado exitosamente en: {zip_filename}!")

if __name__ == "__main__":
    app = QApplication([])
    window = BackupApp()
    window.show()
    app.exec_()
