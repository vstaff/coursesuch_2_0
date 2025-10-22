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
    QMessageBox,
    QHeaderView,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
import re
from AVL_Tree import Priem
from ViewAVLT import AVLWindow

# паттерны:
FIO = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
DOB = r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
SUBJECT = r"[А-ЯЁа-яё\- ]+"
GRADE = r"[2-5]"


class AVLTableView(QWidget):
    def __init__(self, tree, main_window, table):
        super().__init__()
        self.tree = tree
        self.main_window = main_window
        self.table_data = table

        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ФИО", "Дата рождения", "Предмет", "Оценка", "—", "Индекс"]
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
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        self.refresh_table()

    def open_graphic_tree(self):
        self._graphic_window = AVLWindow(self.tree, self.main_window, self.table_data)
        self._graphic_window.show()

    def refresh_table(self):
        rows = []

        def traverse(node):
            if not node:
                return
            traverse(node._left)
            cur = node._list._head
            while cur:
                idx = cur._data
                p = None
                if 0 <= idx < len(self.main_window.all_data):
                    p = self.main_window.all_data[idx]

                if p is None:
                    p = Priem("[Удалено]", "[Удалено]", "-", "-", "-")

                rows.append((p.fio, p.subject, p.grade, p.dob, idx))
                cur = cur._next
            traverse(node._right)

        traverse(self.tree._root)

        self.table.setRowCount(len(rows))
        for row, (fio, subject, grade, dob, idx) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(fio))
            self.table.setItem(row, 1, QTableWidgetItem(subject))
            self.table.setItem(row, 2, QTableWidgetItem(grade))
            self.table.setItem(row, 3, QTableWidgetItem(dob))
            self.table.setItem(row, 4, QTableWidgetItem(idx))

    def show_context_menu(self, pos):
        menu = QMenu()
        add_action = menu.addAction("Добавить")
        delete_action = menu.addAction("Удалить")
        find_action = menu.addAction("Найти")
        export_action = menu.addAction("Экспортировать")
        show_tree_action = menu.addAction("Показать дерево")  # ✅ Новый пункт меню

        action = menu.exec(self.table.mapToGlobal(pos))
        if action == add_action:
            self.show_insert_dialog()
        elif action == delete_action:
            self.show_delete_dialog()
        elif action == find_action:
            self.show_find_dialog()
        elif action == export_action:
            self.export_data()
        elif action == show_tree_action:
            self.open_graphic_tree()  # ✅ Открытие дерева

    def show_insert_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить оценку")
        layout = QFormLayout(dialog)

        name = QLineEdit()
        owner = QLineEdit()
        diag = QLineEdit()
        doctor = QLineEdit()
        date = QLineEdit()

        layout.addRow("ФИО:", name)
        layout.addRow("Дата рождения:", owner)
        layout.addRow("Предмет:", diag)
        layout.addRow("Оценка (2-5):", doctor)
        layout.addRow("— (не используется):", date)

        btn = QPushButton("Добавить")
        layout.addWidget(btn)

        def add():
            if not name.text() or not owner.text():
                QMessageBox.warning(dialog, "Ошибка", "ФИО и дата рождения обязательны")
                return
            if not (
                    re.fullmatch(FIO, name.text())
                    and re.fullmatch(DOB, owner.text())
                    and re.fullmatch(SUBJECT, diag.text())
                    and re.fullmatch(GRADE, doctor.text())
            ):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных")
                return
            if not self.table_data.is_key(name.text(), owner.text()):
                QMessageBox.warning(dialog, "Ошибка", "Такой ученик не найден в справочнике 'Ученики'")
                return

            data = Priem(
                name.text(), owner.text(), diag.text(), doctor.text(), ""
            )

            existing = False
            to_remove = []

            for idx in list(self.tree.find_index_by_data(data)):
                if 0 <= idx < len(self.main_window.all_data):
                    p = self.main_window.all_data[idx]
                    if p is None:
                        to_remove.append(idx)
                    elif (
                            (p.fio or "") == (data.fio or "")
                            and (p.dob or "") == (data.dob or "")
                            and (p._dianoz or "") == (data._dianoz or "")
                            and (p._doctor or "") == (data._doctor or "")
                    ):
                        existing = True
                        break

            for idx in to_remove:
                self.tree._root, _ = self.tree.remove_index(data, idx)
                self.main_window.free_indices.append(idx)

            if existing:
                QMessageBox.warning(dialog, "Ошибка", "Такая запись уже существует")
                return

            if self.main_window.free_indices:
                index = self.main_window.free_indices.pop(0)
                if index >= len(self.main_window.all_data):
                    self.main_window.all_data.append(data)
                else:
                    self.main_window.all_data[index] = data
            else:
                index = len(self.main_window.all_data)
                self.main_window.all_data.append(data)

            self.tree._root, _ = self.tree.insert(data, index, self.tree._root)
            dialog.accept()
            self.refresh_table()

        btn.clicked.connect(add)
        dialog.exec()

    def show_find_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Найти оценки ученика")
        layout = QFormLayout(dialog)

        name = QLineEdit()
        owner = QLineEdit()
        layout.addRow("ФИО:", name)
        layout.addRow("Дата рождения:", owner)

        btn = QPushButton("Найти")
        layout.addWidget(btn)

        def find():
            if not (re.fullmatch(FIO, name.text()) and re.fullmatch(DOB, owner.text())):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных")
                return

            data = Priem(name.text(), owner.text())
            node = self.tree.search(data)

            if not node:
                QMessageBox.warning(dialog, "Результат", "Оценки не найдены")
                return

            info_dialog = QDialog(self)
            info_dialog.setWindowTitle("Узел дерева (оценки)")
            layout_info = QVBoxLayout(info_dialog)

            layout_info.addWidget(QLabel(f"<b>Ключ:</b> {node.key}"))
            layout_info.addWidget(QLabel(f"<b>Баланс:</b> {node._balance}"))
            layout_info.addWidget(QLabel("<b>Список оценок:</b>"))

            if node._list is None or node._list._head is None:
                layout_info.addWidget(QLabel("Нет оценок в этом узле."))
            else:
                cur = node._list._head
                while cur:
                    idx = cur._data
                    p = None
                    if 0 <= idx < len(self.main_window.all_data):
                        p = self.main_window.all_data[idx]
                    if p:
                        info = (
                            f"Индекс: {idx}\n"
                            f"ФИО: {p._name}\n"
                            f"Дата рождения: {p._owner}\n"
                            f"Предмет: {p._dianoz}\n"
                            f"Оценка: {p._doctor}\n"
                        )
                        layout_info.addWidget(QLabel(info))
                    else:
                        layout_info.addWidget(QLabel(f"[Индекс {idx} не найден]"))
                    cur = cur._next

            close_btn = QPushButton("Закрыть")
            close_btn.clicked.connect(info_dialog.accept)
            layout_info.addWidget(close_btn)

            info_dialog.setLayout(layout_info)
            info_dialog.exec()

        btn.clicked.connect(find)
        dialog.exec()

    def export_data(self):
        lst = self.main_window.all_data
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as file:

                def traverse(node):
                    if not node:
                        return
                    traverse(node._left)
                    cur = node._list._head
                    while cur:
                        idx = cur._data
                        i = self.main_window.all_data[idx]
                        line = f"{i.fio} {i.owner} {i._dianoz} {i._doctor} {i._date}"
                        file.write(line + "\n")
                        cur = cur._next
                    traverse(node._right)

                traverse(self.tree._root)
            QMessageBox.information(
                self, "Экспорт завершён", "Данные успешно экспортированы."
            )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")
