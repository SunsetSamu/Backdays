import os
import pdb
from zipfile import ZipFile
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox
from PyQt5.QtCore import Qt
# from QApplication import processEvents


class BackupApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backup Creator")
        self.setGeometry(100, 100, 300, 150)

        # Layout y widgets
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Selecciona la carpeta para respaldar:", self)
        self.layout.addWidget(self.label)

        # Configuración del contenedor principal
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
        # Contenedor de carpetas
        self.selected_folders = []
        self.folder_list_layout = QVBoxLayout()
        self.layout.addLayout(self.folder_list_layout)
     
        # Botones
        self.select_folder_btn = QPushButton("Seleccionar Carpeta", self)
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_btn)

        self.create_backup_btn = QPushButton("Crear Backup", self)
        self.create_backup_btn.clicked.connect(self.create_backup)
        self.create_backup_btn.setEnabled(False)
        self.layout.addWidget(self.create_backup_btn)

        self.folder_path = self.selected_folders[0] if self.selected_folders else ""
        
    def select_folder(self):
        folders = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folders:
            if folders not in self.selected_folders:
                self.selected_folders.append(folders)
                self.folder_path = self.selected_folders[0]  # Actualizar self.folder_path
                self.update_folder_list()
            self.create_backup_btn.setEnabled(True)
        
        
    def update_folder_list(self):
        # Limpiar el layout anterior
        for i in reversed(range(self.folder_list_layout.count())):
            widget = self.folder_list_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Agregar las nuevas carpetas con casillas de verificación
        for folder in self.selected_folders:
            checkbox = QCheckBox(folder, self)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state, folder=folder: self.toggle_folder(state, folder))
            self.folder_list_layout.addWidget(checkbox)
        
    def toggle_folder(self, state, folder):
        if state == Qt.Checked and folder not in self.selected_folders:
            self.selected_folders.append(folder)
        elif state == Qt.Unchecked and folder in self.selected_folders:
            self.selected_folders.remove(folder)
        self.update_folder_list()
        self.create_backup_btn.setEnabled(bool(self.selected_folders))
        
    """    
    def create_backup(self):
        if not self.folder_path:
            return

        files_to_zip = []
        script_name = os.path.basename(__file__)

        for folder in self.selected_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file != script_name and not ("backup" in file.lower() and file.endswith('.zip')) and not file.endswith('.1~') and not file.endswith('.2~') and not file.endswith('.3~'):
                        files_to_zip.append(os.path.join(root, file))

        # Generar nombre único para el archivo ZIP basado en fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = os.path.basename(self.selected_folders[0]) if self.selected_folders else "Backup"
        zip_filename = os.path.join(self.folder_path, f"Backup_{folder_name}_{timestamp}.zip")


        # Escribir en el archivo ZIP
        with ZipFile(zip_filename, 'w') as zip_file:
            for file in files_to_zip:
                if os.path.isfile(file):
                    zip_file.write(file, os.path.relpath(file, folder))


        self.label.setText(f"¡Backup creado exitosamente en: {zip_filename}!")
    """
    def create_backup(self):
        if not self.selected_folders:
            return

        for folder in self.selected_folders:
            files_to_zip = []
            script_name = os.path.basename(__file__)

            # Recopilar archivos para el ZIP
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file != script_name and not ("backup" in file.lower() and file.endswith('.zip')):
                        relative_path = os.path.relpath(os.path.join(root, file), folder)
                        files_to_zip.append((os.path.join(root, file), relative_path))

            # Generar nombre único para el archivo ZIP basado en la carpeta
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = os.path.basename(folder)
            zip_filename = os.path.join(folder, f"Backup_{folder_name}_{timestamp}.zip")

            # Crear el archivo ZIP
            with ZipFile(zip_filename, 'w') as zip_file:
                for file_path, arcname in files_to_zip:
                    if os.path.isfile(file_path):
                        zip_file.write(file_path, arcname)

            # Mostrar mensaje de éxito
            self.label.setText(f"¡Backup creado exitosamente en: {zip_filename}!")
            QApplication.processEvents()  # Asegura que la interfaz de usuario se actualice
    


# pdb.set_trace()
if __name__ == "__main__":
    app = QApplication([])
    window = BackupApp()
    window.show()
    app.exec_()
