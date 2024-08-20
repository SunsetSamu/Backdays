import os
import json
from zipfile import ZipFile
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QProgressBar, QFrame, QMessageBox
from PyQt5.QtGui import QDragEnterEvent
from PyQt5.QtCore import Qt
# from QApplication import processEvents

class BackupApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backdays v6 - Backuper")
        self.setGeometry(100, 100, 300, 150)
        self.setAcceptDrops(True)

        # Layout and widgets
        self.layout = QVBoxLayout()
        
        # Import and Export buttons
        self.import_btn = QPushButton("Import Settings", self)
        self.import_btn.clicked.connect(self.import_settings)
        self.layout.addWidget(self.import_btn)

        self.export_btn = QPushButton("Export Settings", self)
        self.export_btn.clicked.connect(self.export_settings)
        self.layout.addWidget(self.export_btn)

        # Separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.separator)

        self.label = QLabel("Select or drag the folder to back up:", self)
        self.layout.addWidget(self.label)

        # Main container configuration
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
        # Folder container
        self.selected_folders = []
        self.folder_list_layout = QVBoxLayout()
        self.layout.addLayout(self.folder_list_layout)
        
        # Buttons
        self.select_folder_btn = QPushButton("Select Folder", self)
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_btn)

        # Separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.separator)
        
        # Custom path option
        self.use_custom_path_checkbox = QCheckBox("Use custom path", self)
        self.use_custom_path_checkbox.stateChanged.connect(self.toggle_custom_path)
        self.layout.addWidget(self.use_custom_path_checkbox)

        self.select_custom_path_btn = QPushButton("Select Path", self)
        self.select_custom_path_btn.setEnabled(False)
        self.select_custom_path_btn.clicked.connect(self.select_custom_path)
        self.layout.addWidget(self.select_custom_path_btn)

        self.create_backup_btn = QPushButton("Create Backup", self)
        self.create_backup_btn.clicked.connect(self.create_backup)
        self.create_backup_btn.setEnabled(False)
        self.layout.addWidget(self.create_backup_btn)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)


        # self.folder_path = self.selected_folders[0] if self.selected_folders else ""
        self.custom_path = ""
        
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
        
        
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            folder = url.toLocalFile()
            if os.path.isdir(folder) and folder not in self.selected_folders:
                self.selected_folders.append(folder)
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.json'):
                self.import_settings(file_path)
        self.update_folder_list()
        self.create_backup_btn.setEnabled(bool(self.selected_folders))
        
        
    def select_folder(self):
        folders = QFileDialog.getExistingDirectory(self, "Select Folder", options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folders:
            if folders not in self.selected_folders:
                self.selected_folders.append(folders)
                self.folder_path = self.selected_folders[0]  # Update self.folder_path
                self.update_folder_list()
            self.create_backup_btn.setEnabled(True)
        
        
    def update_folder_list(self):
        # Clear the previous layout
        for i in reversed(range(self.folder_list_layout.count()):
            widget = self.folder_list_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add the new folders with checkboxes
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
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Save Backups", options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folder:
            self.custom_path = folder
            self.select_custom_path_btn.setText(f"Selected path: {os.path.basename(self.custom_path)}")
        
    def toggle_folder(self, state, folder):
        if state == Qt.Checked and folder not in self.selected_folders:
            self.selected_folders.append(folder)
        elif state == Qt.Unchecked and folder in self.selected_folders:
            self.selected_folders.remove(folder)
        self.update_folder_list()
        self.create_backup_btn.setEnabled(bool(self.selected_folders))
            
    def import_settings(self, file_name=None, file_path=None):
        data = None

        if file_path:  # If file_path is provided, use it
            with open(file_path, 'r') as file:
                data = json.load(file)
        elif file_name:  # If no file_path but file_name is provided, use it
            with open(file_name, 'r') as file:
                data = json.load(file)
        else:  # If neither is provided, open dialog to select a file
            file_name, _ = QFileDialog.getOpenFileName(self, "Import Settings", "", "JSON Files (*.json)")
            if file_name:
                with open(file_name, 'r') as file:
                    data = json.load(file)

            # Update selected folders
        if data:
            self.selected_folders = [folder for folder in data.get('folders', []) if os.path.isdir(folder)]
            self.update_folder_list()

            if 'custom_path' in data:
                self.custom_path = data['custom_path']
                if self.custom_path and not os.path.isdir(self.custom_path):  # Check if the folder exists
                    os.makedirs(self.custom_path)  # Create the folder if it doesn't exist
                if self.custom_path:
                    self.use_custom_path_checkbox.setChecked(bool(self.custom_path))
                    self.select_custom_path_btn.setEnabled(bool(self.custom_path))
                    self.select_custom_path_btn.setText(f"Selected path: {os.path.basename(self.custom_path)}")
                else:
                    self.use_custom_path_checkbox.setChecked(False)
                    self.select_custom_path_btn.setEnabled(False) 
            # Enable the create backup button if folders are selected
            self.create_backup_btn.setEnabled(bool(self.selected_folders))
        
        
    def export_settings(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Settings", "", "JSON Files (*.json)")
        if file_name:
            data = {
                'folders': self.selected_folders,
                'custom_path': self.custom_path if self.use_custom_path_checkbox.isChecked() else ""
            }
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)
        
        
    def create_backup(self):
        if not self.selected_folders:
            return

        total_files = sum(len([file for root, dirs, files in os.walk(folder) for file in files]) for folder in self.selected_folders)
        file_count = 0

        for folder in self.selected_folders:
            files_to_zip = []
            script_name = os.path.basename(__file__)

            # Collect files for the ZIP
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file != script_name and not ("backup" in file.lower() and file.endswith('.zip')) and not file.endswith('.1~') and not file.endswith('.2~') and not file.endswith('.3~'):
                        relative_path = os.path.relpath(os.path.join(root, file), folder)
                        files_to_zip.append((os.path.join(root, file), relative_path))

            # Generate unique name for the ZIP file based on the folder
            if self.use_custom_path_checkbox.isChecked() and self.custom_path:
                backup_folder = self.custom_path
            else:
                backup_folder = folder 

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = os.path.basename(folder)
            zip_filename = os.path.join(backup_folder, f"Backup_{folder_name}_{timestamp}.zip")

            # Create the ZIP file
            with ZipFile(zip_filename, 'w') as zip_file:
                for file_path, arcname in files_to_zip:
                    if os.path.isfile(file_path):
                        zip_file.write(file_path, arcname)
                        file_count += 1
                        # Update progress bar
                        self.progress_bar.setValue(int((file_count / total_files) * 100))


            # Show success message
            self.label.setText(f"Backup successfully created at: {zip_filename}!")
            QApplication.processEvents()  # Ensure the UI updates
        # Reset the progress bar
        self.progress_bar.setValue(0)


# pdb.set_trace()
if __name__ == "__main__":
    app = QApplication([])
    window = BackupApp()
    window.show()
    app.exec_()
