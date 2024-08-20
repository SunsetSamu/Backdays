## Features

- **GUI:** Powered by PyQt5.
- **Drag & Drop:** Import settings or select folders by dragging them directly into the application window.
- **Persistent settings:** Save and load backup settings with JSON files.
- **Custom Path:** Choose a specific destination path for backup files.
- **Backup Progress:** View the progress of the backup process via a progress bar.

---

## Installation
```bash
# 1. Clone the repo
git clone https://github.com/SunsetSamu/Backdays.git
cd Backdays

# 2. Install the dependencies
pip install -r requirements.txt

# 1. Start the application
python main_v6_latest.py
```
---

## Usage

**Select folders to backup:**
- **Drag and drop** folders directly into the application window, or
- Click the **"Select Folder"** button and choose a folder from the dialog that appears.

**Set a custom path (optional):**
- Check the **"Use custom path"** box to enable selecting a custom destination path for your backups.
- Click the **"Select Path"** button and choose the folder where you want to save the backup files.

**Create the backup:**
- Click **"Create Backup"** to start the process of creating the ZIP file with the contents of the selected folders.

**Import or export settings:**
- **Import settings:** Drag and drop a JSON file with saved settings, or use the **"Import Settings"** button to select a file from the dialog.
- **Export settings:** Use the **"Export Settings"** button to save the current settings to a JSON file.

---

## Requirements

- Python 3.x
- PyQt5

---

## Changelog

### V6_latest

1. Translated comments and GUI to english.

---

### V6:
#### Practical Changelog

1. **Import and Export Settings:** Buttons have been added to import and export settings in JSON format. This allows users to save and load their selected folder and custom path settings.

2. **Drag and Drop Import Support:** You can now import settings by dragging and dropping JSON files into the application window. This makes it easier to load settings without having to use the import buttons.

3. **Custom Path Verification and Creation:** When importing settings, if the custom path does not exist, it is automatically created. Additionally, the existence of the custom path is validated to ensure that it can be used.

4. **Custom Path Label Update:** The label for the custom path selection button now displays the name of the selected folder instead of the full path.

#### Technical Changelog

1. **Import and Export Settings:**
- Added two buttons to import (`import_btn`, lines 22-24) and export (`export_btn`, lines 26-28) settings, each connected to their respective methods (`import_settings` and `export_settings`).
- Implemented `import_settings()` method to load settings from a JSON file and update the selected folders and custom path (lines 149-181).
- Implemented `export_settings()` method to save the current settings to a JSON file (lines 184-192).

2. **Drag and Drop Import Support:**
- Changed the `dropEvent()` method to handle dragged and dropped JSON files in addition to folders (lines 95-100).
- Updated the `import_settings()` method to accept a `file_path` from `dropEvent()` and load the settings from the dragged JSON file (lines 152-157).

3. **Custom Path Checking and Creation:**
- In `import_settings()`, added logic to check if the custom path exists and create it if not (lines 171-172).

4. **Custom Path Label Update:**
- The `select_custom_path_btn` button text now displays the name of the selected folder (lines 137-139).

5. **Minor Improvements:**
- Updated the `dragEnterEvent()` method to use `event.accept()` instead of `event.acceptProposedAction()` to better handle drag and drop (lines 85-89).

---

### V5: 
#### Practical Changelog

1. **Drag and Drop Support:** Added functionality to drag and drop folders directly into the application window. This makes it easier to add folders for backup without having to navigate through selection dialogs.

2. **Custom Backup Path:** Users can now choose a custom path to save backups. This option is controlled by a checkbox and a button to select the destination path.

3. **Progress Indicator:** A progress bar has been added to show the progress of the backup creation process. This provides visual feedback on the progress of the backup.

#### Technical Changelog

1. **Drag and Drop Functionality:**
- Enabled support for dragging and dropping folders into the application window with `setAcceptDrops(True)` (line 16).
- Implemented `dragEnterEvent()` and `dropEvent()` methods to handle dragging and dropping folders (lines 71-84).

2. **Custom Backup Path:**
- Added a checkbox (`QCheckBox`) to allow users to select a custom path for backup (`lines 47-49`).
- Added a button to select the custom path (`select_custom_path_btn`, lines 51-54) and its functionality (`toggle_custom_path()` (lines 111-114) and `select_custom_path()` (lines 116-120)).

3. **Progress Bar:**
- Added a `QProgressBar` to show the progress of the backup creation process (lines 61-64).
- Calculated the total number of files to backup and updated the progress bar based on the number of files processed (line 136).
- The progress bar is updated during ZIP file creation to reflect the percentage of files processed (lines 165-167).

4. **Interface Separator:**
- Added a horizontal line `QFrame` to visually separate the folder selection section and the path configuration (lines 40-43).

---

### V4:
#### Practical Changelog

1. **Multiple Folder Support:** The application now allows selecting and managing multiple folders for backup. Users can select multiple folders and each will be included in the backup process.

2. **Dynamic List of Selected Folders:** A checkbox system has been implemented to manage selected folders. Users can check or uncheck individual folders to include or exclude them from the backup.

3. **Improved User Interface:** Improvements have been made to the interface to dynamically display selected folders and allow management of these folders via checkboxes.

#### Technical Changelog

1. **Multiple Folder Support:**
- Folder selection handling has been modified to allow multiple selections, by storing the folders in `self.selected_folders` (line 34).
- Logic to dynamically update and display selected folders using checkboxes (`QCheckBox`) has been added in `update_folder_list()` (lines 55-67).

2. **Dynamic Folder Management:**
- `toggle_folder()` method has been added to handle toggling folders on and off in the list (lines 69-75).
- The "Create Backup" button is enabled only if there is at least one folder selected (line 75).

3. **Backup Logic Update:**
- The `create_backup()` method has been updated to handle multiple folders. Files from all selected folders are collected and separate ZIP files are created for each folder (lines 106-134).
- Files in the ZIP are now added with specific relative paths (`arcname`) to maintain the directory structure (lines 127-130).

4. **UI Improvements:**
- Added `QApplication.processEvents()` at the end of the backup process to ensure that the UI is updated correctly during the execution of the ZIP creation process (line 134).
- The `folder_path` variable is updated only when selecting a folder, and is changed to the first selected folder by default (line 50).

5. **Debugging and Code Cleanup:**
- Added `pdb` module (line 2) for debugging, although the code is commented out.
- Removed commented lines and refactored the code to simplify the backup process logic.

---

### V3:
#### Practical Changelog

1. **Graphical User Interface (GUI):** A graphical interface based on PyQt5 was added, allowing users to select a folder and create backups more intuitively.

2. **Folder Selection:** The user can now select the specific folder to be backed up, offering greater flexibility and control over the backup process.

3. **Extended File Exclusion:** In addition to ZIP files and the script, temporary editing files (`.1~`, `.2~`, `.3~`) are excluded, improving backup accuracy.

#### Technical Changelog

1. **Added PyQt5 for GUI:**
- Imported `QApplication`, `QMainWindow`, `QFileDialog`, `QPushButton`, `QLabel`, `QVBoxLayout`, and `QWidget` from PyQt5 to create a graphical interface (line 4).
- Created `BackupApp` class that inherits from `QMainWindow`, where the application's main window, buttons, labels, and layouts are configured (lines 6-33).

2. **User Folder Selection:**
- Added `select_folder` method that uses `QFileDialog.getExistingDirectory` to allow the user to select a folder from the graphical interface (lines 35-42).
- The path of the selected folder is stored in `self.folder_path` and displayed in the interface.

3. **Backup Creation from Selected Folder:**
- The `create_backup` method now works with the user-selected folder (lines 42-60).
- File exclusion was expanded to include temporary files (`.1~`, `.2~`, `.3~`).

4. **Dynamic Path Generation for ZIP:**
- The ZIP file name now also includes the name of the selected folder (`folder_name`), in addition to the timestamp, for better identification (lines 53-54).

---

### V2:
#### Practical Changelog

1. **Better file exclusion:** The script now excludes both the script file and any ZIP file containing "backup" in its name, improving efficiency and avoiding redundancies.
  
2. **Unique ZIP file name:** The generated ZIP file now includes a unique timestamp (date and time) in its name, preventing overwrites and making it easier to identify backups.

#### Technical Changelog

1. **Excluding ZIP files with "backup" in the name:**
- On line 13, added `not ("backup" in file.lower() and file.endswith('.zip'))` condition to exclude ZIP files that contain "backup" in their name and that might have been generated in previous runs.

2. **Generating unique name for ZIP file:**
- Added import of `datetime` from `datetime` (line 3).
- Created a `timestamp` variable (line 18) that uses `datetime.now().strftime("%Y%m%d_%H%M%S")` to get the current date and time in a specific format.
- The ZIP file name is now defined as `Backup_{timestamp}.zip` (line 19), where `{timestamp}` is replaced with the timestamp.

3. **Renamed and improved code structure:**
- Renamed the `Script_dir` variable to `script_name` to better reflect its contents (line 6).
- Removed the previous loop for listing and handling folders, simplifying the logic to a single loop that loops through all files (lines 9-14).
- The write block in the ZIP file was kept similar, but with the new dynamically generated filename (`zip_filename`) (lines 22-24).
