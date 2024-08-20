import os
import pdb
from zipfile import ZipFile
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QProgressBar, QFrame
from PyQt5.QtCore import Qt
# from QApplication import processEvents


class BackupApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backup Creator")
        self.setGeometry(100, 100, 300, 150)
        self.setAcceptDrops(True)

        # Layout y widgets
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Selecciona o arrastra la carpeta para respaldar:", self)
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


        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.separator)

        
        # Ruta personalizada
        self.use_custom_path_checkbox = QCheckBox("Usar ruta personalizada", self)
        self.use_custom_path_checkbox.stateChanged.connect(self.toggle_custom_path)
        self.layout.addWidget(self.use_custom_path_checkbox)

        self.select_custom_path_btn = QPushButton("Seleccionar Ruta", self)
        self.select_custom_path_btn.setEnabled(False)
        self.select_custom_path_btn.clicked.connect(self.select_custom_path)
        self.layout.addWidget(self.select_custom_path_btn)

        self.create_backup_btn = QPushButton("Crear Backup", self)
        self.create_backup_btn.clicked.connect(self.create_backup)
        self.create_backup_btn.setEnabled(False)
        self.layout.addWidget(self.create_backup_btn)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)


        # self.folder_path = self.selected_folders[0] if self.selected_folders else ""
        self.custom_path = ""
        
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            folder = url.toLocalFile()
            if os.path.isdir(folder) and folder not in self.selected_folders:
                self.selected_folders.append(folder)
        self.update_folder_list()
        self.create_backup_btn.setEnabled(bool(self.selected_folders))
        
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
        
        
    def toggle_custom_path(self, state):
        self.select_custom_path_btn.setEnabled(state == Qt.Checked)
        if not state:
            self.custom_path = ""
        
    def select_custom_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta para Guardar Backups", options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folder:
            self.custom_path = folder
            self.select_custom_path_btn.setText(f"Ruta seleccionada: {os.path.basename(self.custom_path)}")

        
        
    def toggle_folder(self, state, folder):
        if state == Qt.Checked and folder not in self.selected_folders:
            self.selected_folders.append(folder)
        elif state == Qt.Unchecked and folder in self.selected_folders:
            self.selected_folders.remove(folder)
        self.update_folder_list()
        self.create_backup_btn.setEnabled(bool(self.selected_folders))
        
    def create_backup(self):
        if not self.selected_folders:
            return

        total_files = sum(len([file for root, dirs, files in os.walk(folder) for file in files]) for folder in self.selected_folders)
        file_count = 0

        for folder in self.selected_folders:
            files_to_zip = []
            script_name = os.path.basename(__file__)

            # Recopilar archivos para el ZIP
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file != script_name and not ("backup" in file.lower() and file.endswith('.zip')) and not file.endswith('.1~') and not file.endswith('.2~') and not file.endswith('.3~'):
                        relative_path = os.path.relpath(os.path.join(root, file), folder)
                        files_to_zip.append((os.path.join(root, file), relative_path))

            # Generar nombre único para el archivo ZIP basado en la carpeta
            if self.use_custom_path_checkbox.isChecked() and self.custom_path:
                backup_folder = self.custom_path
            else:
                backup_folder = folder 

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = os.path.basename(folder)
            zip_filename = os.path.join(backup_folder, f"Backup_{folder_name}_{timestamp}.zip")

            # Crear el archivo ZIP
            with ZipFile(zip_filename, 'w') as zip_file:
                for file_path, arcname in files_to_zip:
                    if os.path.isfile(file_path):
                        zip_file.write(file_path, arcname)
                        file_count += 1
                        # Actualizar barra de progreso
                        self.progress_bar.setValue(int((file_count / total_files) * 100))


            # Mostrar mensaje de éxito
            self.label.setText(f"¡Backup creado exitosamente en: {zip_filename}!")
            QApplication.processEvents()  # Asegura que la interfaz de usuario se actualice
        # Reiniciar la barra de progreso
        self.progress_bar.setValue(0)


# pdb.set_trace()
if __name__ == "__main__":
    app = QApplication([])
    window = BackupApp()
    window.show()
    app.exec_()
