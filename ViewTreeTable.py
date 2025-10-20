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


pattern = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
pattern2 = (
    r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
)


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
            ["Кличка", "Владелец", "Диагноз", "Доктор", "Дата", "Индекс"]
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

                rows.append((p._name, p._owner, p._dianoz, p._doctor, p._date, idx))
                cur = cur._next
            traverse(node._right)

        traverse(self.tree._root)

        self.table.setRowCount(len(rows))
        for row, (name, owner, diag, doctor, date, idx) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(owner))
            self.table.setItem(row, 2, QTableWidgetItem(diag))
            self.table.setItem(row, 3, QTableWidgetItem(doctor))
            self.table.setItem(row, 4, QTableWidgetItem(date))
            self.table.setItem(row, 5, QTableWidgetItem(str(idx)))

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
        dialog.setWindowTitle("Добавить приём")
        layout = QFormLayout(dialog)

        name = QLineEdit()
        owner = QLineEdit()
        diag = QLineEdit()
        doctor = QLineEdit()
        date = QLineEdit()

        layout.addRow("Кличка (пример: Барсик):", name)
        layout.addRow("Владелец (пример: Иван Сергеевич Петров):", owner)
        layout.addRow("Диагноз (пример: Гастрит):", diag)
        layout.addRow("Доктор (пример: Иван Сергеевич Петров):", doctor)
        layout.addRow("Дата (пример 10 дек 2023):", date)

        btn = QPushButton("Добавить")
        layout.addWidget(btn)

        def add():
            if not name.text() or not owner.text():
                QMessageBox.warning(dialog, "Ошибка", "Имя и владелец обязательны")
                return
            if not (
                re.fullmatch(r"[А-Я][а-я]+", name.text())
                and re.fullmatch(pattern, owner.text())
                and re.fullmatch(r"[А-Я][а-я]+( [а-я]+)*", diag.text())
                and re.fullmatch(pattern, doctor.text())
                and re.fullmatch(pattern2, date.text())
            ):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных")
                return
            if not self.table_data.is_key(name.text(), owner.text()):
                QMessageBox.warning(
                    dialog, "Ошибка", "Такой клиент не найден в таблице"
                )
                return

            data = Priem(
                name.text(), owner.text(), diag.text(), doctor.text(), date.text()
            )

            existing = False
            to_remove = []

            for idx in list(self.tree.find_index_by_data(data)):
                if 0 <= idx < len(self.main_window.all_data):
                    p = self.main_window.all_data[idx]
                    if p is None:
                        to_remove.append(idx)
                    elif (
                        p._name == data._name
                        and p._owner == data._owner
                        and p._dianoz == data._dianoz
                        and p._doctor == data._doctor
                        and p._date == data._date
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

    def show_delete_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Удалить приём")
        layout = QFormLayout(dialog)

        name = QLineEdit()
        owner = QLineEdit()
        diag = QLineEdit()
        doctor = QLineEdit()
        date = QLineEdit()

        layout.addRow("Кличка (пример: Барсик):", name)
        layout.addRow("Владелец (пример: Иван Сергеевич Петров):", owner)
        layout.addRow("Диагноз (пример: Гастрит):", diag)
        layout.addRow("Доктор (пример: Иван Сергеевич Петров):", doctor)
        layout.addRow("Дата (пример 10 дек 2023):", date)

        btn = QPushButton("Удалить")
        layout.addWidget(btn)

        def delete():
            if not name.text() or not owner.text():
                QMessageBox.warning(dialog, "Ошибка", "Имя и владелец обязательны")
                return

            # 🔍 Добавляем проверку формата
            if not (
                re.fullmatch(r"[А-Я][а-я]+", name.text())
                and re.fullmatch(pattern, owner.text())
                and re.fullmatch(r"[А-Я][а-я]+( [а-я]+)*", diag.text())
                and re.fullmatch(pattern, doctor.text())
                and re.fullmatch(pattern2, date.text())
            ):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных")
                return

            data = Priem(
                name.text(), owner.text(), diag.text(), doctor.text(), date.text()
            )

            found_index = None
            for idx in self.tree.find_index_by_data(data):
                if 0 <= idx < len(self.main_window.all_data):
                    p = self.main_window.all_data[idx]
                    if (
                        p
                        and p._name == data._name
                        and p._owner == data._owner
                        and p._dianoz == data._dianoz
                        and p._doctor == data._doctor
                        and p._date == data._date
                    ):
                        found_index = idx
                        break

            if found_index is None:
                QMessageBox.warning(
                    dialog, "Ошибка", "Запись не найдена, удалять нечего"
                )
                return

            last_index = len(self.main_window.all_data) - 1

            if found_index == last_index:
                self.tree._root, removed = self.tree.remove_index(data, found_index)
                if removed:
                    self.main_window.all_data.pop()
            else:
                last_item = self.main_window.all_data.pop()
                self.tree._root, removed = self.tree.remove_index(data, found_index)
                if removed:
                    self.tree._root, _ = self.tree.remove_index(last_item, last_index)
                    self.main_window.all_data[found_index] = last_item
                    self.tree._root, _ = self.tree.insert(
                        last_item, found_index, self.tree._root
                    )

            if removed:
                self.refresh_table()
                dialog.accept()
                QMessageBox.information(dialog, "Успех", "Запись удалена")
            else:
                QMessageBox.warning(dialog, "Ошибка", "Не удалось удалить запись")

        btn.clicked.connect(delete)
        dialog.exec()

    def show_find_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Найти приём")
        layout = QFormLayout(dialog)

        name = QLineEdit()
        owner = QLineEdit()
        layout.addRow("Кличка (пример: Барсик):", name)
        layout.addRow("Владелец (пример: Иван Сергеевич Петров):", owner)

        btn = QPushButton("Найти")
        layout.addWidget(btn)

        def find():
            if not name.text() or not owner.text():
                QMessageBox.warning(dialog, "Ошибка", "Имя и владелец обязательны")
                return

            if not (
                re.fullmatch(r"[А-Я][а-я]+", name.text())
                and re.fullmatch(pattern, owner.text())
            ):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных")
                return

            data = Priem(name.text(), owner.text())
            node = self.tree.search(data)

            if not node:
                QMessageBox.warning(dialog, "Результат", "Приём не найден")
                return

            info_dialog = QDialog(self)
            info_dialog.setWindowTitle("Информация об узле")
            layout_info = QVBoxLayout(info_dialog)

            layout_info.addWidget(QLabel(f"<b>Ключ:</b> {node._key}"))
            layout_info.addWidget(QLabel(f"<b>Баланс:</b> {node._balance}"))
            layout_info.addWidget(QLabel("<b>Приёмы:</b>"))

            if node._list is None or node._list._head is None:
                layout_info.addWidget(QLabel("Нет приёмов в этом узле."))
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
                            f"Имя: {p._name}\n"
                            f"Владелец: {p._owner}\n"
                            f"Диагноз: {p._dianoz}\n"
                            f"Доктор: {p._doctor}\n"
                            f"Дата: {p._date}\n"
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
                        line = f"{i._name} {i._owner} {i._dianoz} {i._doctor} {i._date}"
                        file.write(line + "\n")
                        cur = cur._next
                    traverse(node._right)

                traverse(self.tree._root)
            QMessageBox.information(
                self, "Экспорт завершён", "Данные успешно экспортированы."
            )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")
