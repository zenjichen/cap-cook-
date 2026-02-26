
import sys
import os
import json
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class AntiCapCutTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TIKTOK CAPCUT BYPASS TOOL")
        self.setFixedSize(500, 350)
        self.default_path = os.path.join(os.environ['LOCALAPPDATA'], 
                                        r"CapCut\User Data\Projects\com.lveditor.draft")
        self.initUI()
        self.refresh_projects()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("CAPCUT BYPASS PRO")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ff0050; margin: 10px;")
        main_layout.addWidget(title_label)

        # Project Path
        path_layout = QHBoxLayout()
        self.path_label = QLabel(f"Project Folder: ...{self.default_path[-40:]}")
        self.path_label.setStyleSheet("color: #555;")
        btn_browse = QPushButton("Browse")
        btn_browse.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(btn_browse)
        main_layout.addLayout(path_layout)

        # Project Selector
        main_layout.addWidget(QLabel("Select Project:"))
        self.combo_projects = QComboBox()
        main_layout.addWidget(self.combo_projects)

        # Action Buttons
        btn_refresh = QPushButton("Refresh Projects")
        btn_refresh.clicked.connect(self.refresh_projects)
        main_layout.addWidget(btn_refresh)

        self.btn_bypass = QPushButton("BYPASS PROJECT (REMOVE PRO)")
        self.btn_bypass.setStyleSheet("""
            QPushButton {
                background-color: #00f2ea;
                color: black;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00d2ca;
            }
        """)
        self.btn_bypass.clicked.connect(self.execute_bypass)
        main_layout.addWidget(self.btn_bypass)

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Links
        links_layout = QVBoxLayout()
        contact_label = QLabel("Nếu cần xin liên hệ:")
        contact_label.setAlignment(Qt.AlignCenter)
        contact_label.setStyleSheet("color: #333; font-style: italic; margin-top: 10px;")
        links_layout.addWidget(contact_label)

        btn_fb = QPushButton("FACEBOOK")
        btn_fb.setFlat(True)
        btn_fb.setStyleSheet("color: blue; text-decoration: underline; font-weight: bold;")
        btn_fb.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.facebook.com/NguyenManhHaOfficial")))
        
        links_layout.addWidget(btn_fb)
        main_layout.addLayout(links_layout)

    def browse_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select CapCut Project Folder", self.default_path)
        if dir_path:
            self.default_path = dir_path
            self.path_label.setText(f"Project Folder: ...{self.default_path[-40:]}")
            self.refresh_projects()

    def is_project_folder(self, path):
        # A CapCut project folder must have draft_content.json or draft_meta.json
        return os.path.exists(os.path.join(path, "draft_content.json")) or \
               os.path.exists(os.path.join(path, "draft_meta.json"))

    def get_project_name(self, path):
        meta_path = os.path.join(path, "draft_meta.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    return meta.get('draft_name', os.path.basename(path))
            except:
                pass
        return os.path.basename(path)

    def refresh_projects(self):
        self.combo_projects.clear()
        if not os.path.exists(self.default_path):
            self.status_label.setText("Error: Path not found")
            return

        projects = []
        
        # Scenario 1: The selected folder is the project itself
        if self.is_project_folder(self.default_path):
            projects.append((self.get_project_name(self.default_path), self.default_path))
        
        # Scenario 2: Always check subfolders as well (in case user picked parent)
        try:
            for item in os.listdir(self.default_path):
                project_dir = os.path.join(self.default_path, item)
                if os.path.isdir(project_dir) and self.is_project_folder(project_dir):
                    # Avoid duplicate if already added in Scenario 1
                    if project_dir != self.default_path:
                        projects.append((self.get_project_name(project_dir), project_dir))
        except:
            pass
            
        # UI update
        for name, path in projects:
            self.combo_projects.addItem(name, path)

        if self.combo_projects.count() == 0:
            self.status_label.setText("No projects found.")
        else:
            self.status_label.setText(f"Found {self.combo_projects.count()} projects.")

    def execute_bypass(self):
        project_name = self.combo_projects.currentText()
        project_dir = self.combo_projects.currentData()
        
        if not project_dir:
            QMessageBox.warning(self, "Warning", "Please select a project.")
            return

        draft_content_path = os.path.join(project_dir, "draft_content.json")
        if not os.path.exists(draft_content_path):
            QMessageBox.critical(self, "Error", "draft_content.json not found in this project.")
            return

        try:
            # Backup
            backup_path = draft_content_path + ".bak"
            shutil.copy2(draft_content_path, backup_path)

            with open(draft_content_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            # Deep search and replace Pro flags
            modified_count = self.remove_pro_flags(content)

            with open(draft_content_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=4)

            QMessageBox.information(self, "Success", 
                                    f"Bypass successful for '{project_name}'!\n"
                                    f"Modified {modified_count} flags.\n"
                                    f"You can now export the project in CapCut.")
            self.status_label.setText(f"Bypassed: {project_name}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to bypass: {str(e)}")

    def remove_pro_flags(self, obj):
        count = 0
        if isinstance(obj, dict):
            # Check for pro-related keys
            pro_keys = ['is_pro', 'is_pro_resource', 'paid_feature', 'pro_asset']
            for key in list(obj.keys()):
                if any(pkg in key.lower() for pkg in pro_keys):
                    if obj[key] is True or (isinstance(obj[key], int) and obj[key] > 0):
                        obj[key] = False if isinstance(obj[key], bool) else 0
                        count += 1
                count += self.remove_pro_flags(obj[key])
        elif isinstance(obj, list):
            for item in obj:
                count += self.remove_pro_flags(item)
        return count

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiCapCutTool()
    window.show()
    sys.exit(app.exec_())
