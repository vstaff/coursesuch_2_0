from PyQt6.QtWidgets import (
    # QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    # QHBoxLayout,
    # QTableWidget,
    # QTableWidgetItem,
    QPushButton,
    QLineEdit,
    # QLabel,
    QMessageBox,
    # QGraphicsView,
    # QGraphicsScene,
    # QGraphicsEllipseItem,
    # QGraphicsTextItem,
    # QGraphicsLineItem,
    QDialog,
    QFormLayout,
)
# from PyQt6.QtGui import QPen
# from PyQt6.QtCore import Qt
from HasgTable import Hash_Table
from AVL_Tree import AVLT
import re
# from ViewTable import ViewTable
from PetsTableView import ArrtTableView
# from ViewAVLT import AVLGraphicsView
from ViewTreeTable import AVLTableView
# from ViewAVLT import AVLWindow
# from OtchetTreeView import AVL2Window
from TableOtchet import OtchetTable
# from Otchet import AVLT2

pattern = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
pattern2 = (
    r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
)
# Регулярки для проверки
CLASS = r"\d{1,2}[А-ЯЁ]?"
GRADE = r"[2-5]"
DOB = r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"


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
    def __init__(self, table: Hash_Table, tree: AVLT, arr2, arrt):
        super().__init__()
        self.tree = tree
        self.table = table
        self.setWindowTitle("Предметная область школа")
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

    def show_filtered_report(self, filters):
        """
        Формирует таблицу отчёта по трём полям фильтра:
        Класс, Оценка, Дата рождения.
        Использует связку между ХТ (ученики) и АВЛ (оценки).
        """

        # Извлекаем значения фильтров
        klass_filter = filters["klass"].strip()
        grade_filter = filters["grade"].strip()
        date_filter = filters["date"].strip()

        # Проверяем форматы (если заполнены)
        if klass_filter and not re.fullmatch(CLASS, klass_filter):
            QMessageBox.warning(self, "Ошибка", "Неверный формат класса (например, 10А)")
            return
        if grade_filter and not re.fullmatch(GRADE, grade_filter):
            QMessageBox.warning(self, "Ошибка", "Неверная оценка (2–5)")
            return
        if date_filter and not re.fullmatch(DOB, date_filter):
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты (10 дек 2007)")
            return

        report_rows = []

        # Проходим по всем узлам дерева (оценки)
        def traverse(node):
            if not node:
                return
            traverse(node._left)
            cur = node._list._head
            while cur:
                idx = cur._data
                if 0 <= idx < len(self.all_data):
                    record = self.all_data[idx]  # MainActiveGrade = оценка
                    # Получаем класс ученика из хеш-таблицы (по ключу ФИО+дата)
                    try:
                        student = self.table.search(record.fio, record.owner)
                        klass = student._type if student else ""
                    except Exception:
                        klass = ""

                    # Проверяем фильтр
                    if (klass_filter == "" or klass_filter.lower() == klass.lower()) and \
                            (grade_filter == "" or grade_filter == record._doctor) and \
                            (date_filter == "" or date_filter == record.owner):
                        report_rows.append((
                            record.fio,  # ФИО
                            klass,  # Класс
                            record.owner,  # Дата рождения
                            record._dianoz,  # Предмет
                            record._doctor,  # Оценка
                            ""  # пустая "дата", просто чтобы совпадало с шаблоном отчёта
                        ))
                cur = cur._next
            traverse(node._right)

        # Рекурсивный обход
        traverse(self.tree._root)

        # Создаём и открываем окно отчёта
        self.report_window = OtchetTable(None, self)
        self.report_window.update_table(report_rows)
        self.report_window.show()

    def on_but_click(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Фильтрация отчета")
        layout = QFormLayout(dialog)

        type_input = QLineEdit()
        doctor_input = QLineEdit()
        date_input = QLineEdit()

        layout.addRow("Класс (например, 10А):", type_input)
        layout.addRow("Оценка (2–5):", doctor_input)
        layout.addRow("Дата рождения (10 дек 2007):", date_input)

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
                    re.fullmatch(CLASS, type_text)
                    and re.fullmatch(GRADE, doctor_text)
                    and re.fullmatch(DOB, date_text)
            ):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат входных данных")
                return
            result["klass"] = type_text
            result["grade"] = doctor_text
            result["date"] = date_text
            dialog.accept()  # Закрыть окно

        apply_button.clicked.connect(apply_filter)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.show_filtered_report(result)
