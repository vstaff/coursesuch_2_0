from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QHBoxLayout,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from HasgTable import Hash_Table
from AVL_Tree import AVLT
from MainWindow import MainWindow
from main_activ import init_arr1, init_arr2
import sys


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добро пожаловать")
        self.setGeometry(400, 200, 600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        greeting = QLabel("Добро пожаловать в систему")
        greeting.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        greeting.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(greeting)

        layout.addWidget(QLabel("Файл справочника Питомцы:"))
        self.hash_path_input = QLineEdit()
        self.hash_path_input.setReadOnly(True)
        hash_button = QPushButton("Выбрать файл")
        hash_button.clicked.connect(self.select_hash_file)

        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Размер таблицы (опционально)")

        hash_layout = QHBoxLayout()
        hash_layout.addWidget(self.hash_path_input)
        hash_layout.addWidget(hash_button)
        layout.addLayout(hash_layout)
        layout.addWidget(self.size_input)

        layout.addWidget(QLabel("Файл справочника Приёмы (необязательно):"))
        self.tree_path_input = QLineEdit()
        self.tree_path_input.setReadOnly(True)
        tree_button = QPushButton("Выбрать файл")
        tree_button.clicked.connect(self.select_tree_file)

        tree_layout = QHBoxLayout()
        tree_layout.addWidget(self.tree_path_input)
        tree_layout.addWidget(tree_button)
        layout.addLayout(tree_layout)

        confirm_btn = QPushButton("Подтвердить")
        confirm_btn.clicked.connect(self.load_and_open_main)
        layout.addWidget(confirm_btn)

    def select_hash_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл для справочника Питомцы",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if file_path:
            self.hash_path_input.setText(file_path)

    def select_tree_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл для справочника Приёмы",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if file_path:
            self.tree_path_input.setText(file_path)

    def load_and_open_main(self):
        hash_path = self.hash_path_input.text().strip()
        tree_path = self.tree_path_input.text().strip()

        if not hash_path:
            QMessageBox.warning(self, "Внимание", "Выберите файл справочника Питомцы.")
            return

        try:
            arr = init_arr1(hash_path)

            size_text = self.size_input.text().strip()
            size = len(arr)

            if size_text:
                if size_text.isdigit():
                    parsed_size = int(size_text)
                    if parsed_size > 0:
                        size = parsed_size
                    elif parsed_size == 0:
                        size = len(arr)
                    else:
                        QMessageBox.warning(
                            self,
                            "Ошибка",
                            "Размер таблицы должен быть положительным числом.",
                        )
                        return
                else:
                    QMessageBox.warning(
                        self, "Ошибка", "Размер таблицы должен быть целым числом."
                    )
                    return

            table = Hash_Table(arr, size)

            if not tree_path:
                arr2 = []
                tree = AVLT([])
            else:
                arr2 = init_arr2(tree_path, table)
                if len(arr2) == 0:
                    QMessageBox.warning(
                        self,
                        "Внимание",
                        "Файлы справочников пусты или имеют неверный формат данных.",
                    )
                    return
                tree = AVLT(arr2)

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось загрузить данные:\n{str(e)}"
            )
            return

        self.main_window = MainWindow(table, tree, arr2, arr)
        self.main_window.show()
        self.close()
