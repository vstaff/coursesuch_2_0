from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QMenu,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
)
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt


from HasgTable import Hash_Table, HasgTableStudent
from HasgTable import HasgTableStudent
import re
from ViewAVLT import AVLGraphicsView
from AVL_Tree import AVLT
from ViewTreeTable import AVLTableView
from AVL_Tree import Priem

pattern2 = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
pattern1 = r"[А-ЯЁ][а-яё]+"


class ViewTable(QMainWindow):
    def __init__(
        self, table: Hash_Table, avl_tree: AVLT, avl_view: AVLTableView, mainw
    ):
        super().__init__()
        self.avl_tree = avl_tree
        self.avl_view = avl_view
        self.table_obj = table
        self.mainw = mainw
        self.setWindowTitle("Хеш-таблица")
        self.setGeometry(100, 100, 1000, 600)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.refresh_table()

        # self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

    def refresh_table(self):
        data_list = self.table_obj.get_table()
        self.table_widget.setRowCount(len(data_list))
        self.table_widget.setColumnCount(9)
        self.table_widget.setHorizontalHeaderLabels(
            ["Index", "Primary Hash", "Secondary Hash (i=1)", "Key", "ФИО", "Класс", "Дата рождения", "Position",
             "Status"]
        )

        for i, data in enumerate(data_list):
            primary_hash = self.table_obj.hash_func1(data.key)
            secondary_hash = self.table_obj.kvadratich_poisk(data.key, 1)
            items = [
                QTableWidgetItem(str(i)),
                QTableWidgetItem(str(primary_hash)),
                QTableWidgetItem(str(secondary_hash)),
                QTableWidgetItem(str(data.key)),
                QTableWidgetItem(data.fio),
                QTableWidgetItem(data._type),
                QTableWidgetItem(data.owner),
                QTableWidgetItem(str(data.index)),
                QTableWidgetItem(str(data.status)),
            ]
            for j, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_widget.setItem(i, j, item)

        self.table_widget.resizeColumnsToContents()

    # def show_context_menu(self, position):
    #     menu = QMenu()
    #     add_action = menu.addAction("Добавить")
    #     delete_action = menu.addAction("Удалить")
    #     find_action = menu.addAction("Найти")
    #     export_action = menu.addAction("Экспортировать")
    #     action = menu.exec(self.table_widget.mapToGlobal(position))
    #     if action == add_action:
    #         self.show_insert_dialog()
    #     elif action == delete_action:
    #         self.show_delete_dialog()
    #     elif action == find_action:
    #         self.show_find_dialog()
    #     elif action == export_action:
    #         self.export_data()
    #
    # def show_insert_dialog(self):
    #     dialog = QDialog(self)
    #     dialog.setWindowTitle("Добавить запись")
    #     layout = QFormLayout()
    #
    #     name_input = QLineEdit()
    #     type_input = QLineEdit()
    #     owner_input = QLineEdit()
    #     layout.addRow("Имя:", name_input)
    #     layout.addRow("Тип:", type_input)
    #     layout.addRow("Владелец:", owner_input)
    #
    #     btn = QPushButton("Добавить")
    #
    #     def on_add_clicked():
    #         name = name_input.text()
    #         type_ = type_input.text()
    #         owner = owner_input.text()
    #
    #         if not name or not type_ or not owner:
    #             QMessageBox.warning(dialog, "Ошибка", "Все поля обязательны для ввода.")
    #             return
    #
    #         if not (re.fullmatch(pattern1, name) and re.fullmatch(r"[А-Я][а-я]+( [а-я]+)*", type_) and re.fullmatch(pattern2, owner)):
    #             QMessageBox.warning(dialog, "Ошибка", "Неверный формат вводимых данных.")
    #             return
    #         self.mainw.arrt.append(MainActiveStudent(name,type_,owner))
    #         self.insert_action(dialog, name, type_, owner)
    #
    #     btn.clicked.connect(on_add_clicked)
    #     layout.addWidget(btn)
    #
    #     dialog.setLayout(layout)
    #     dialog.exec()
    #
    # def show_delete_dialog(self):
    #     dialog = QDialog(self)
    #     dialog.setWindowTitle("Удалить запись")
    #     layout = QFormLayout()
    #
    #     name_input = QLineEdit()
    #     owner_input = QLineEdit()
    #     layout.addRow("Имя:", name_input)
    #     layout.addRow("Владелец:", owner_input)
    #
    #     btn = QPushButton("Удалить")
    #     btn.clicked.connect(lambda: self.delete_action(dialog, name_input.text(), owner_input.text()))
    #     layout.addWidget(btn)
    #
    #     dialog.setLayout(layout)
    #     dialog.exec()
    #
    # def show_find_dialog(self):
    #     dialog = QDialog(self)
    #     dialog.setWindowTitle("Найти запись")
    #     layout = QFormLayout()
    #
    #     name_input = QLineEdit()
    #     owner_input = QLineEdit()
    #     layout.addRow("Имя:", name_input)
    #     layout.addRow("Владелец:", owner_input)
    #
    #     btn = QPushButton("Найти")
    #     btn.clicked.connect(lambda: self.find_action(dialog, name_input.text(), owner_input.text()))
    #     layout.addWidget(btn)
    #
    #     dialog.setLayout(layout)
    #     dialog.exec()

    def insert_action(self, dialog, name, type_, owner):
        if not name or not type_ or not owner:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для ввода.")
            return
        if self.table_obj.ifFull():
            QMessageBox.warning(self, "Ошибка", "Таблица переполнена.")
            return
        index = len(self.mainw.arrt)
        data = HasgTableStudent(name, type_, owner, index)
        if self.table_obj.insert(data):
            self.refresh_table()
            dialog.accept()
        else:
            QMessageBox.warning(
                self, "Ошибка", "Не удалось вставить элемент, он уже существует."
            )

    def delete_action(self, dialog, name, owner):
        if not name or not owner:
            QMessageBox.warning(self, "Ошибка", "Имя и владелец обязательны.")
            return

        temp = self.table_obj.search(name, owner)
        if temp is None:
            QMessageBox.warning(self, "Ошибка", "Элемент не найден.")
            return

        if self.table_obj.delete(temp):
            if (len(self.mainw.arrt) - 1) == temp.index:
                temp = name + owner
                key = name + owner
                node = self.avl_tree.search(Priem(name, owner))
                if node:
                    indices_to_remove = []
                    cur = node.get_lst()._head
                    while cur:
                        idx = cur._data
                        if 0 <= idx < len(self.mainw.all_data):
                            indices_to_remove.append(idx)
                        cur = cur._next

                    for idx in sorted(indices_to_remove, reverse=True):
                        self.mainw.all_data.pop(idx)

                    self.avl_tree = AVLT(self.mainw.all_data)
                    self.avl_view.tree = self.avl_tree
                    self.avl_view.refresh_table()
            else:
                tmp = self.mainw.arrt.pop()
                tmp.index = temp.index
                self.mainw.arrt[temp.index] = tmp
                temp = name + owner
                key = name + owner
                node = self.avl_tree.search(Priem(name, owner))
                if node:
                    indices_to_remove = []
                    cur = node.get_lst()._head
                    while cur:
                        idx = cur._data
                        if 0 <= idx < len(self.mainw.all_data):
                            indices_to_remove.append(idx)
                        cur = cur._next

                    for idx in sorted(indices_to_remove, reverse=True):
                        self.mainw.all_data.pop(idx)

                    self.avl_tree = AVLT(self.mainw.all_data)
                    self.avl_view.tree = self.avl_tree
                    self.avl_view.refresh_table()

            self.table_widget.clearContents()
            self.refresh_table()
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить элемент.")

    def find_action(self, dialog, name, owner):
        if not name or not owner:
            QMessageBox.warning(self, "Ошибка", "Введите имя и владельца.")
            return
        result = self.table_obj.search(name, owner)
        if result:
            QMessageBox.information(
                self,
                "Найдено",
                f"Найдено: {result.fio}, {result._type}, {result.owner}, {result.index}",
            )
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Элемент не найден.")

    # def export_data(self):
    #     tble = self.table_obj.get_table()
    #     file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "Text Files (*.txt);;All Files (*)")
    #     if not file_path:
    #         return
    #
    #     try:
    #         with open(file_path, 'w', encoding='utf-8') as file:
    #             for i in range(len(tble)):
    #                  if tble[i].status == 1:
    #                     full_name = tble[i].owner.strip()
    #                     line = f"{tble[i].fio} {tble[i]._type} {full_name}"
    #                     file.write(line + '\n')
    #         QMessageBox.information(self, "Экспорт завершён", "Данные успешно экспортированы.")
    #     except Exception as e:
    #         QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")
