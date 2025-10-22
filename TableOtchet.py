from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHeaderView,
    QMessageBox,
    QFileDialog,
)
from PyQt6.QtCore import Qt
import re
from OtchetTreeView import AVL2Window
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


class OtchetTable(QWidget):
    def __init__(self, tree, main_window):
        super().__init__()
        self.tree = tree
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.resize(1000, 600)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.setWindowTitle("Отчет по приёмам")

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Имя", "Тип", "Владелец", "Диагноз", "Доктор", "Дата"]
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        for i in range(6):
            self.table.setColumnWidth(i, 100)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.context_menu_requested)

    def refresh_table(self):
        self.filtered_rows = self.get_all_rows()
        self.update_table(self.filtered_rows)

    def get_all_rows(self):
        rows = []
        result_nodes = self.tree.inOrder(self.tree._root)
        for node_list in result_nodes:
            for i in range(node_list.get_size()):
                idx = node_list[i]
                if 0 <= idx < len(self.main_window.all_data):
                    p = self.main_window.all_data[idx]
                    if p is None:
                        continue
                    try:
                        type_ = self.main_window.table.search(p.fio, p.owner)._type
                    except:
                        type_ = p._type
                    rows.append(
                        (p.fio, type_, p.owner, p._dianoz, p._doctor, p._date)
                    )
        return rows

    def update_table(self, rows):
        self.table.setRowCount(len(rows))
        for row, (name, type_, owner, diag, doctor, date) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(type_))
            self.table.setItem(row, 2, QTableWidgetItem(owner))
            self.table.setItem(row, 3, QTableWidgetItem(diag))
            self.table.setItem(row, 4, QTableWidgetItem(doctor))
            self.table.setItem(row, 5, QTableWidgetItem(date))

    def context_menu_requested(self, pos):
        menu = QMenu(self)
        show_tree_action = menu.addAction("Показать дерево")
        export_action = menu.addAction("Экспортировать")

        action = menu.exec(self.table.mapToGlobal(pos))
        if action is None:
            return
        elif action == show_tree_action:
            self.show_tree_view()
        elif action == export_action:
            self.export_data()

    def show_tree_view(self):
        report_tree = AVLT2(self.main_window.all_data, self.main_window.table)
        self.tree_window = AVL2Window(report_tree, self.main_window.all_data)
        self.tree_window.show()

    def open_filter_dialog(self):
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

            self.apply_filters(
                type_text.lower(), doctor_text.lower(), date_text.lower()
            )
            dialog.accept()

        apply_button.clicked.connect(apply_filter)
        dialog.exec()

    def apply_filters(self, type_filter, doctor_filter, date_filter):
        filtered = []
        for row in self.get_all_rows():
            name, type_, owner, diag, doctor, date = row
            if (
                (not type_filter or type_filter in type_.lower())
                and (not doctor_filter or doctor_filter in doctor.lower())
                and (not date_filter or date_filter in date.lower())
            ):
                filtered.append(row)
        self.update_table(filtered)

    def reset_filters(self):
        self.refresh_table()

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                for p in self.main_window.arr:
                    if p is None:
                        continue
                    line = f"{p.fio} {p._type} {p.owner} {p._dianoz} {p._doctor} {p._date}"
                    file.write(line + "\n")
            QMessageBox.information(
                self, "Экспорт завершён", "Данные успешно экспортированы."
            )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")
