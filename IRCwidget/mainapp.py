from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QGridLayout, QFileDialog, QWidget, QLineEdit
import sys
from app_models import ImpResponses
import catcher as ctch

class MainWin(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Ventana principal')
        self.setGeometry(100, 100, 500, 300)
        mainwdgt = QWidget(self)
        layout = QGridLayout()
        mainwdgt.setLayout(layout)
        self.setCentralWidget(mainwdgt)

        #Main menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        help_menu = menu_bar.addMenu('&Help')

        file_menu.addAction('New', lambda: self.text_edit.clear())
        file_menu.addAction('Open', lambda: print('Open'))
        file_menu.addAction('Exit', self.destroy)

        #File browser and directory entry
        
        self.dir_entry = QLineEdit()
        layout.addWidget(self.dir_entry, 0, 0)

        btn_layout = QGridLayout()
        file_browser_btn = QPushButton('Browse')
        file_browser_btn.clicked.connect(self.open_file_dlg)
        btn_layout.addWidget(file_browser_btn, 0, 0)

        save_file_btn = QPushButton('Save in db')
        save_file_btn.clicked.connect(self.save_file)
        btn_layout.addWidget(save_file_btn, 0, 1)

        play_file_btn = QPushButton('Play file')
        play_file_btn.clicked.connect(self.play)
        btn_layout.addWidget(play_file_btn,0,2)
        layout.addLayout(btn_layout, 1, 0)

        self.show()

    def play(self) -> None:
        file_path = self.dir_entry.text()
        ctch.play_audio(file_path)

    def open_file_dlg(self) -> None:
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dlg.setViewMode(QFileDialog.ViewMode.Detail)
        if dlg.exec():
            file_to_get = dlg.selectedFiles()
            if file_to_get:
                file_to_get = file_to_get[0]
                self.dir_entry.setText(file_to_get)

    def save_file(self) -> None:
        file_path = self.dir_entry.text()
        with open(file_path, 'rb') as file:
            binary_file = file.read()
        q = ImpResponses.insert(response_file=binary_file)
        q.execute()
        print(q)
        self.dir_entry.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    sys.exit(app.exec())
