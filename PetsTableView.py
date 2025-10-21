from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QMenu, QDialog, QLineEdit, QPushButton, QFormLayout,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from ViewTable import ViewTable
from avl_tree import Grade
from hash_table import Student
import re
from avl_tree import  AVLTree

pattern1 = r"[А-ЯЁ][а-яё]+"
pattern2 = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"

class ArrtTableView(QWidget):
    def __init__(self, mainw):
        super().__init__()
        self.mainw = mainw

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.refresh_table()

        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

    def refresh_table(self):
        table_data = []
        for data in self.mainw.arrt:
            if self.mainw.table.is_key(data._name, data._owner):
                table_data.append(data)

        self.table_widget.setRowCount(len(table_data))
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Имя", "Тип", "Владелец"])

        for i, data in enumerate(table_data):
            items = [
                QTableWidgetItem(data._name),
                QTableWidgetItem(data._type),
                QTableWidgetItem(data._owner),
            ]
            for j, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_widget.setItem(i, j, item)
        self.table_widget.resizeColumnsToContents()

    def show_context_menu(self, position):
        menu = QMenu()
        open_hash_action = menu.addAction("Открыть хеш-таблицу")  # 🔹 новый пункт
        add_action = menu.addAction("Добавить")
        delete_action = menu.addAction("Удалить")
        find_action = menu.addAction("Найти")
        export_action = menu.addAction("Экспортировать")
        action = menu.exec(self.table_widget.mapToGlobal(position))

        if action == open_hash_action:
            self.open_hash_table_window()
        elif action == add_action:
            self.show_insert_dialog()
        elif action == delete_action:
            self.show_delete_dialog()
        elif action == find_action:
            self.show_find_dialog()
        elif action == export_action:
            self.export_data()

    def show_insert_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить запись")
        layout = QFormLayout()

        name_input = QLineEdit()
        type_input = QLineEdit()
        owner_input = QLineEdit()
        layout.addRow("Кличка (пример: Барсик):", name_input)
        layout.addRow("Тип (пример: Кот):", type_input)
        layout.addRow("Владелец (пример: Иван Сергеевич Петров):", owner_input)

        btn = QPushButton("Добавить")
        layout.addWidget(btn)

        def on_add_clicked():
            name = name_input.text()
            type_ = type_input.text()
            owner = owner_input.text()

            if not name or not type_ or not owner:
                QMessageBox.warning(dialog, "Ошибка", "Все поля обязательны для ввода.")
                return

            if not (re.fullmatch(pattern1, name) and re.fullmatch(r"[А-Я][а-я]+( [а-я]+)*", type_) and re.fullmatch(
                    pattern2, owner)):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных.")
                return


            if self.mainw.table.is_full():
                QMessageBox.warning(dialog, "Ошибка", "Хеш-таблица переполнена. Добавление невозможно.")
                return

            index = len(self.mainw.arrt)
            new_data = Student(name, type_, owner, index)
            self.mainw.arrt.append(new_data)

            if not self.mainw.table.is_unique(new_data):
                QMessageBox.warning(dialog, "Ошибка", "Не удалось вставить элемент в справочник, он уже существует.")
                return
            if not self.mainw.table.insert(new_data):
                QMessageBox.warning(dialog, "Ошибка", "Не удалось вставить элемент в справочник.")
                return


            self.refresh_table()
            if hasattr(self.mainw, "view_table") and self.mainw.view_table:
                self.mainw.view_table.refresh_table()
            dialog.accept()

        btn.clicked.connect(on_add_clicked)
        dialog.setLayout(layout)
        dialog.exec()

    def open_hash_table_window(self):
        self.mainw.view_table = ViewTable(
            self.mainw.table, self.mainw.tree, self.mainw.view_tree1, self.mainw
        )
        self.mainw.view_table.show()
    def show_delete_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Удалить запись")
        layout = QFormLayout()

        name_input = QLineEdit()
        owner_input = QLineEdit()
        layout.addRow("Кличка (пример: Барсик):", name_input)
        layout.addRow("Владелец (пример: Иван Сергеевич Петров):", owner_input)

        btn = QPushButton("Удалить")

        def on_delete_clicked():
            name = name_input.text()
            owner = owner_input.text()


            if not re.fullmatch(pattern1, name) or not re.fullmatch(pattern2, owner):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных.")
                return

            for i, data in enumerate(self.mainw.arrt):
                if data._name == name and data._owner == owner:
                    # Удалить из хеш-таблицы
                    if i != len(self.mainw.arrt) - 1:
                        last = self.mainw.arrt.pop()
                        last._index = i
                        self.mainw.arrt[i] = last
                    else:
                        self.mainw.arrt.pop()

                    found = self.mainw.table.find(name, owner)
                    if found:
                        self.mainw.table.delete(found)

                    node = self.mainw.tree.find(Grade(name, owner))
                    if node:
                        cur = node.get_list()._head
                        indices_to_remove = []

                        while cur:
                            idx = cur._data
                            if 0 <= idx < len(self.mainw.all_data):
                                indices_to_remove.append(idx)
                            cur = cur._next


                        for idx in sorted(indices_to_remove):
                            last_index = len(self.mainw.all_data) - 1

                            if idx == last_index:

                                self.mainw.tree._root, _ = self.mainw.tree.remove_index(self.mainw.all_data[idx], idx)
                                self.mainw.all_data.pop()
                            else:

                                while last_index in indices_to_remove and last_index != idx:

                                    self.mainw.tree._root, _ = self.mainw.tree.remove_index(
                                        self.mainw.all_data[last_index], last_index)
                                    self.mainw.all_data.pop()
                                    last_index = len(self.mainw.all_data) - 1


                                if idx >= len(self.mainw.all_data):
                                    continue

                                last_item = self.mainw.all_data[last_index]


                                self.mainw.tree._root, _ = self.mainw.tree.remove_index(self.mainw.all_data[idx], idx)


                                self.mainw.tree._root, _ = self.mainw.tree.remove_index(last_item, last_index)


                                self.mainw.all_data[idx] = last_item


                                self.mainw.tree._root, _ = self.mainw.tree.insert(last_item, idx, self.mainw.tree._root)


                                self.mainw.all_data.pop()


                    self.mainw.view_tree1.tree = self.mainw.tree
                    self.mainw.view_tree1.refresh_table()
                    self.refresh_table()
                    if hasattr(self.mainw, "view_table") and self.mainw.view_table:
                        self.mainw.view_table.refresh_table()
                    dialog.accept()
                    return

            QMessageBox.warning(dialog, "Ошибка", "Питомец не найден, нечего удалять.")

        btn.clicked.connect(on_delete_clicked)
        layout.addWidget(btn)
        dialog.setLayout(layout)
        dialog.exec()

    def show_find_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Найти запись")
        layout = QFormLayout()

        name_input = QLineEdit()
        owner_input = QLineEdit()
        layout.addRow("Кличка (пример: Барсик):", name_input)
        layout.addRow("Владелец (пример: Иван Сергеевич Петров):", owner_input)

        btn = QPushButton("Найти")

        def on_find():
            name = name_input.text()
            owner = owner_input.text()


            if not re.fullmatch(pattern1, name) or not re.fullmatch(pattern2, owner):
                QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных.")
                return

            for i, data in enumerate(self.mainw.arrt):
                if data._name == name and data._owner == owner:
                    QMessageBox.information(self, "Найдено", f"{data._name}, {data._type}, {data._owner}")
                    dialog.accept()
                    return
            QMessageBox.warning(dialog, "Ошибка", "Питомец не найден.")

        btn.clicked.connect(on_find)
        layout.addWidget(btn)
        dialog.setLayout(layout)
        dialog.exec()

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "Text Files (*.txt);;All Files (*)")
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                for data in self.mainw.arrt:
                    file.write(f"{data._name} {data._type} {data._owner}\n")
            QMessageBox.information(self, "Успех", "Файл сохранён.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
