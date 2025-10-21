from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsTextItem,
    QGraphicsLineItem,
    QDialog,
    QFormLayout,
)
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from hash_table import HashTable
from avl_tree import AVLTree
import re
from ViewTable import ViewTable
from PetsTableView import ArrtTableView
from ViewAVLT import AVLGraphicsView
from ViewTreeTable import AVLTableView
from ViewAVLT import AVLWindow
from OtchetTreeView import AVL2Window
from TableOtchet import OtchetTable
from Otchet import AVLT2

pattern = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
pattern2 = (
    r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
)


class PetsPriem:
    def __init__(self, name="", type="", owner="", diagonz="", doctor="", date=""):
        self._name = name
        self._type = type
        self._owner = owner
        self._dianoz = diagonz
        self._doctor = doctor
        self._date = date

    def __str__(self):
        return (
            f"Name: {self._name}, Owner: {self._owner}, "
            f"Diagnosis: {self._dianoz}, Doctor: {self._doctor}, Date: {self._date}"
        )


class MainWindow(QMainWindow):
    def __init__(self, table: HashTable, tree: AVLTree, arr2, arrt):
        super().__init__()
        self.tree = tree
        self.table = table
        self.setWindowTitle("Ветеринарная клиника")
        self.setGeometry(100, 100, 1600, 800)
        self.next_index = 1
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.all_data = arr2
        self.free_indices = []
        self.manual_data = []
        self.arr = []
        self.arrt = arrt
        # self.view_tree = AVLGraphicsView(tree, self, table)
        self.view_tree1 = AVLTableView(tree, self, table)
        self.view_arrt_table = ArrtTableView(self)
        self.top_button = QPushButton("Сформировать отчет")
        self.top_button.clicked.connect(self.on_but_click)
        layout.addWidget(self.top_button)
        layout.addWidget(self.view_arrt_table)
        layout.addWidget(self.view_tree1)

    def show_filtered_report(self, type_filter, doctor_filter, date_filter):
        report_tree = AVLT2(self.all_data, self.table)
        matching_rows = []

        current = report_tree._root
        while current is not None:
            if date_filter < current._key:
                current = current._left
            elif date_filter > current._key:
                current = current._right
            else:
                for i in range(current._list.get_size()):
                    idx = current._list[i]
                    if 0 <= idx < len(self.all_data):
                        record = self.all_data[idx]
                        if record is None:
                            continue
                        if doctor_filter in record._doctor.lower():
                            try:
                                type_from_hash = self.table.search(
                                    record._name, record._owner
                                )._type
                            except Exception:
                                type_from_hash = record._type
                            if type_filter in type_from_hash.lower():
                                matching_rows.append(
                                    (
                                        record._name,
                                        type_from_hash,
                                        record._owner,
                                        record._dianoz,
                                        record._doctor,
                                        record._date,
                                    )
                                )
                break

        # Открываем окно отчета в любом случае, даже если список пуст
        self.report_window = OtchetTable(None, self)
        self.report_window.update_table(matching_rows)
        self.report_window.show()

    def on_but_click(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Фильтрация отчета")
        layout = QFormLayout(dialog)

        type_input = QLineEdit()
        doctor_input = QLineEdit()
        date_input = QLineEdit()

        layout.addRow("Тип животного:", type_input)
        layout.addRow("Имя врача:", doctor_input)
        layout.addRow("Дата (например, 10 мар 2024):", date_input)

        apply_button = QPushButton("Применить")
        layout.addWidget(apply_button)

        result = {}

        def apply_filter():
            type_text = type_input.text().strip()
            doctor_text = doctor_input.text().strip()
            date_text = date_input.text().strip()

            if not type_text or not doctor_text or not date_text:
                QMessageBox.warning(dialog, "Ошибка", "Заполните все поля")
                return

            if not (
                re.fullmatch(r"[А-Я][а-я]+", type_text)
                and re.fullmatch(pattern, doctor_text)
                and re.fullmatch(pattern2, date_text)
            ):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат входных данных")
                return

            result["type"] = type_text.lower()
            result["doctor"] = doctor_text.lower()
            result["date"] = date_text.lower()
            dialog.accept()  # Закрыть окно

        apply_button.clicked.connect(apply_filter)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.show_filtered_report(result["type"], result["doctor"], result["date"])
