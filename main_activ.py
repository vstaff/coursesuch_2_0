from PyQt6.QtWidgets import (
    QApplication,
    # QMainWindow,
    # QWidget,
    # QVBoxLayout,
    # QHBoxLayout,
    # QTableWidget,
    # QTableWidgetItem,
    # QPushButton,
    # QLineEdit,
    # QLabel,
    # QMessageBox,
    # QGraphicsView,
    # QGraphicsScene,
    # QGraphicsEllipseItem,
    # QGraphicsTextItem,
    # QGraphicsLineItem,
)

import re
# from AVL_Tree import AVLT
import sys

# Формат дат оставляем прежним (янв..дек), чтобы не ломать остальной код:
MONTHED_DATE = r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
FIO = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
CLASS = r"[1-9][АБВГабвг]|10[АБВГабвг]|11[АБВГабвг]"                  # 1, 10, 11А и т.п.
SUBJECT = r"[А-ЯЁа-яё\- ]+"                # предмет — русские буквы/пробел/дефис
GRADE = r"[2-5]"                           # школьная оценка


class MainActiveStudent:
    def __init__(self, fio="", class_="", dob="", index=None):
        self.fio = fio
        self.class_ = class_
        self.dob = dob
        self.key = sum(ord(c) for c in (fio + dob))
        self._status = 0
        self._index = index

    def __eq__(self, other):
        return (
                isinstance(other, MainActiveStudent)
                and self.fio == other.fio
                and self.class_ == other.class_
                and self.dob == other.dob
        )


class MainActiveGrade:
    def __init__(self, fio="", subject="", grade="", dob=""):
        self.fio = fio
        self.subject = subject
        self.grade = grade
        self.dob = dob

    def __eq__(self, other):
        if isinstance(other, MainActiveGrade):
            return (
                    self.fio == other.fio
                    and self.subject == other.subject
                    and self.grade == other.grade
                    and self.dob == other.dob
            )
        return False


def filesize(filename):
    unique_lines = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and line not in unique_lines:
                unique_lines.append(line)
    return len(unique_lines)


def init_arr1(filename):
    """
    Ученики: каждая строка -> 'ФИО;Класс;ДатаРождения'
    Например: 'Иванов Иван Иванович;10А;12 мар 2007'
    """
    arr = []
    with open(filename, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # допускаем как; так и таб/много пробелов
            parts = line.split(";")
            if len(parts) != 3:
                continue

            fio, klass, dob = parts
            if not (re.fullmatch(FIO, fio) and re.fullmatch(CLASS, klass) and re.fullmatch(MONTHED_DATE, dob)):
                continue

            # MainActiveStudent(name=fio, type=klass, owner=dob, index=...)
            idx = len(arr)
            arr.append(MainActiveStudent(fio, klass, dob, idx))
    return arr



def init_arr2(filename, table):
    """
    Оценки: каждая строка -> 'ФИО;Предмет;Оценка;Дата(=дата рождения ученика)'
    Например: 'Иванов Иван Иванович;Русский язык;5;12 мар 2007'
    """
    arr = []
    with open(filename, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split(";")
            if len(parts) != 4:
                continue

            fio, subject, grade, dob = parts
            if not (re.fullmatch(FIO, fio) and re.fullmatch(SUBJECT, subject) and re.fullmatch(GRADE, grade) and re.fullmatch(MONTHED_DATE, dob)):
                continue

            # Проверяем, что ученик есть в ХТ (ключ = fio+dob)
            if not table.is_key(fio, dob):
                # пропускаем записи без "родителя" в ХТ
                continue

            # MainActiveGrade(name=fio, owner=dob, diagonz=subject, doctor=grade, date="")
            arr.append(MainActiveGrade(fio, dob, subject, grade))

    return arr


def main():
    from StartWindow import StartWindow

    app = QApplication(sys.argv)
    start = StartWindow()
    start.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
