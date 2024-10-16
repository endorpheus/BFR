import sys
import os
import random
import string
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel,
    QLineEdit, QMessageBox, QCheckBox, QSpinBox, QHBoxLayout, QTreeView, QFileSystemModel,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QIcon, QAction
from collections import defaultdict
from about_dialog import AboutDialog  # Import the AboutDialog class

class BFR(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BFR - Bulk File Renamer")
        self.setWindowIcon(QIcon("icons/robot_icon.png"))  # Set the application icon
        self.selected_files = []
        self.init_ui()
        self.create_menu()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.setup_file_tree(layout)
        self.setup_rename_options(layout)
        self.setup_rename_button(layout)

    def create_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        about_dialog = AboutDialog(
            self,
            title="About BFR",
            app_name="Bulk File Renamer",
            version="1.0.0",
            description="A powerful tool for renaming multiple files at once.",
            author="Ryon Shane Hall",
            email="endorpheus@gmail.com",
            website="https://github.com/endorpheus/BFR",
        )
        about_dialog.exec()

    def setup_file_tree(self, layout):
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(os.path.expanduser("~"))

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(os.path.expanduser("~")))
        self.file_tree.setSelectionMode(QTreeView.ExtendedSelection)
        self.file_tree.setColumnWidth(0, 300)
        self.file_tree.selectionModel().selectionChanged.connect(self.update_selected_files)
        layout.addWidget(self.file_tree)

    def setup_rename_options(self, layout):
        layout.addWidget(QLabel("Rename pattern (excluding numbering):"))
        self.rename_pattern_input = QLineEdit()
        layout.addWidget(self.rename_pattern_input)

        self.keep_extensions_checkbox = QCheckBox("Keep original file extensions")
        self.keep_extensions_checkbox.setChecked(True)
        layout.addWidget(self.keep_extensions_checkbox)

        self.add_numbering_checkbox = QCheckBox("Add numbering")
        layout.addWidget(self.add_numbering_checkbox)

        padding_layout = QHBoxLayout()
        padding_layout.addWidget(QLabel("Number padding:"))
        self.padding_spinner = QSpinBox()
        self.padding_spinner.setRange(1, 10)
        self.padding_spinner.setValue(3)
        padding_layout.addWidget(self.padding_spinner)
        layout.addLayout(padding_layout)

        self.numbering_position_checkbox = QCheckBox("Place number at the beginning of the filename")
        self.numbering_position_checkbox.setChecked(True)
        layout.addWidget(self.numbering_position_checkbox)

        self.use_random_names_checkbox = QCheckBox("Generate random filenames")
        layout.addWidget(self.use_random_names_checkbox)

        random_name_length_layout = QHBoxLayout()
        random_name_length_layout.addWidget(QLabel("Random name length:"))
        self.random_name_length_spinner = QSpinBox()
        self.random_name_length_spinner.setRange(5, 30)
        self.random_name_length_spinner.setValue(10)
        random_name_length_layout.addWidget(self.random_name_length_spinner)
        layout.addLayout(random_name_length_layout)

    def setup_rename_button(self, layout):
        self.rename_button = QPushButton("Rename Files")
        self.rename_button.clicked.connect(self.rename_files)
        layout.addWidget(self.rename_button)

    def update_selected_files(self):
        self.selected_files = [
            self.file_model.filePath(index)
            for index in self.file_tree.selectionModel().selectedRows()
            if os.path.isfile(self.file_model.filePath(index))
        ]

    def rename_files(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Error", "No files selected for renaming.")
            return

        pattern = self.rename_pattern_input.text().strip()
        keep_extension = self.keep_extensions_checkbox.isChecked()
        add_numbering = self.add_numbering_checkbox.isChecked()
        padding_digits = self.padding_spinner.value()
        numbering_at_start = self.numbering_position_checkbox.isChecked()
        use_random_names = self.use_random_names_checkbox.isChecked()
        random_name_length = self.random_name_length_spinner.value()

        if not pattern and not add_numbering and not use_random_names:
            QMessageBox.warning(self, "Error", "Please specify a rename pattern, enable numbering, or choose random filename generation.")
            return

        try:
            new_filenames, conflicts = self.generate_new_filenames(
                self.selected_files, pattern, keep_extension, add_numbering, padding_digits, 
                numbering_at_start, use_random_names, random_name_length
            )
            if conflicts:
                self.resolve_conflicts(new_filenames, conflicts, add_numbering, padding_digits, 
                                       numbering_at_start, use_random_names, random_name_length)
            self.perform_renaming(new_filenames)
            QMessageBox.information(self, "Success", "Files renamed successfully!")
            self.file_model.setRootPath(self.file_model.rootPath())  # Refresh the file view
        except OSError as e:
            QMessageBox.critical(self, "Error", f"Failed to rename files: {str(e)}\n\nPlease check file permissions and ensure the files exist.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def generate_new_filenames(self, files_to_rename, pattern, keep_extension, add_numbering, 
                               padding_digits, numbering_at_start, use_random_names, random_name_length):
        new_filenames = {}
        conflicts = defaultdict(list)
        for i, filepath in enumerate(files_to_rename):
            if not os.path.exists(filepath):
                raise OSError(f"The file {filepath} does not exist.")
            
            directory, old_filename = os.path.split(filepath)
            name, extension = os.path.splitext(old_filename)

            if use_random_names:
                new_name = self.generate_random_name(random_name_length)
            else:
                new_name = pattern if pattern else name

            if add_numbering:
                file_number = f"{i + 1:0{padding_digits}d}"
                new_name = f"{file_number}-{new_name}" if numbering_at_start else f"{new_name}-{file_number}"

            if keep_extension:
                new_name += extension

            new_filepath = os.path.join(directory, new_name)
            
            if new_filepath in new_filenames.values() or os.path.exists(new_filepath):
                conflicts[new_filepath].append(filepath)
            else:
                new_filenames[filepath] = new_filepath

        return new_filenames, conflicts

    def resolve_conflicts(self, new_filenames, conflicts, add_numbering, padding_digits, 
                          numbering_at_start, use_random_names, random_name_length):
        for conflicted_new_path, original_paths in conflicts.items():
            directory, conflicted_name = os.path.split(conflicted_new_path)
            name, ext = os.path.splitext(conflicted_name)
            
            for i, original_path in enumerate(original_paths):
                if use_random_names:
                    new_name = self.generate_random_name(random_name_length)
                elif add_numbering:
                    file_number = f"{len(new_filenames) + i + 1:0{padding_digits}d}"
                    if numbering_at_start:
                        new_name = f"{file_number}-{name}"
                    else:
                        new_name = f"{name}-{file_number}"
                else:
                    new_name = f"{name}_{i + 1}"
                
                if self.keep_extensions_checkbox.isChecked():
                    new_name += ext
                
                new_path = os.path.join(directory, new_name)
                while new_path in new_filenames.values() or os.path.exists(new_path):
                    if use_random_names:
                        new_name = self.generate_random_name(random_name_length)
                    else:
                        new_name += "_"
                    if self.keep_extensions_checkbox.isChecked():
                        new_name += ext
                    new_path = os.path.join(directory, new_name)
                
                new_filenames[original_path] = new_path

    def generate_random_name(self, length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def perform_renaming(self, new_filenames):
        for original_filepath, new_filepath in new_filenames.items():
            os.rename(original_filepath, new_filepath)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BFR()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())
