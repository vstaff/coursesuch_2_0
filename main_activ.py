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
)
from dataclasses import dataclass

import re
from avl_tree import AVLTree
import sys

from hash_table import HashTable

pattern_fio = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+" # это я так понял для ФИО
pattern_date = (
    r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
) # это для даты
pattern_subject = r"^[А-ЯЁа-яё]+(?:[-–—][А-ЯЁа-яё]+)*(?:\s+[А-ЯЁа-яё]+(?:[-–—][А-ЯЁа-яё]+)*)*$" # для названия предмета
pattern_class = r"[1-9][АБВГ]|10[АБВГ]|11[АБВГ]|[1-9][абвг]|10[абвг]|11[абвг]"


# первый справочник
class Student:
    def __init__(self, name="", class_="", date="", index=None):
        self._name = name
        self._class_ = class_
        self._date = date
        self._key = sum(ord(c) for c in (name + date))
        self._status = 0
        self._index = index

    @property
    def name(self):
        return self._name

    @property
    def class_(self):
        return self._class_

    @property
    def date(self):
        return self._date

    @property
    def key(self) -> int:
        return self._key

    @property
    def status(self) -> int:
        return self._status

    def __eq__(self, other):
        return (
            isinstance(other, Student)
            and self._name == other._name
            and self._class_ == other._class_
            and self._date == other._date
        )

# второй справочник
@dataclass
class Grade:
    student_name: str
    subject: str
    grade: str
    birth_date: str


def get_unique_lines_amount(filename: str):
    unique_lines = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and line not in unique_lines:
                unique_lines.append(line)
    return len(unique_lines)


# инициализация первого массива со студентами
def init_arr1(filename):
    arr = [Student() for _ in range(get_unique_lines_amount(filename))]
    with open(filename, "r", encoding="utf-8") as file:
        i = 0
        for line in file:
            parts = line.strip().split()
            if len(parts) != 7:
                continue
            # фамилия имя отчество
            last_name, first_name, middle_name = parts[0], parts[1], parts[2]
            class_ = parts[3]
            date = " ".join(parts[4:])
            if not (
                re.fullmatch(r"[А-Я][а-я]+", last_name)
                and re.fullmatch(r"[А-Я][а-я]+", first_name)
                and re.fullmatch(r"[А-Я][а-я]+", middle_name)
                and re.fullmatch(pattern_class, class_)
                and re.fullmatch(pattern_date, date)
            ):
                continue
            full_name = " ".join([last_name, first_name, middle_name])
            temp = Student(full_name, class_, date, i)
            if temp in arr:
                continue
            arr.append(temp)
            i += 1
    return arr


# инициализация второго массива с оценками
def init_arr2(filename, table: HashTable):
    arr: list[Grade] = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 8:
                continue

            fio = " ".join(parts[0:3])
            subject = " ".join(parts[3:len(parts) - 4])
            grade = parts[len(parts) - 4]
            date = " ".join(parts[len(parts) - 3:])

            if not re.fullmatch(pattern_fio, fio):
                continue

            if not re.fullmatch(pattern_subject, subject):
                continue

            if not re.fullmatch(pattern_class, grade):
                continue

            if not re.fullmatch(pattern_date, date):
                continue

            temp = Grade(fio, subject, grade, date)
            if temp.student_name + temp.birth_date not in table.get_keys():
                continue
            if temp in arr:
                continue

            arr.append(temp)
    return arr


def main():
    from StartWindow import StartWindow

    app = QApplication(sys.argv)
    start = StartWindow()
    start.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
