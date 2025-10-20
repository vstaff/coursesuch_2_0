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

import re
from AVL_Tree import AVLT
import sys

pattern = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
pattern2 = (
    r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
)


class Data:
    def __init__(self, name="", type="", owner="", index=None):
        self._name = name
        self._type = type
        self._owner = owner
        self._key = sum(ord(c) for c in (name + owner))
        self._status = 0
        self._index = index

    def __eq__(self, other):
        return (
            isinstance(other, Data)
            and self._name == other._name
            and self._type == other._type
            and self._owner == other._owner
        )


class Priem:
    def __init__(self, name="", owner="", diagonz="", doctor="", date=""):
        self._name = name
        self._owner = owner
        self._dianoz = diagonz
        self._doctor = doctor
        self._date = date

    def __eq__(self, other):
        if isinstance(other, Priem):
            return (
                self._name == other._name
                and self._owner == other._owner
                and self._dianoz == other._dianoz
                and self._doctor == other._doctor
                and self._date == other._date
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
    arr = [Data() for _ in range(filesize(filename))]
    with open(filename, "r", encoding="utf-8") as file:
        i = 0
        for line in file:
            parts = line.strip().split()
            if len(parts) < 5 and len(parts) >= 10:
                continue
            lname, fname, sname = parts[-3], parts[-2], parts[-1]
            patsname = parts[0]
            patstype_parts = parts[1:-3]
            patstype = " ".join(patstype_parts)
            if not (
                re.fullmatch(r"[А-Я][а-я]+", lname)
                and re.fullmatch(r"[А-Я][а-я]+", fname)
                and re.fullmatch(r"[А-Я][а-я]+", sname)
                and re.fullmatch(r"[А-Я][а-я]+", patsname)
                and re.fullmatch(r"[А-Я][а-я]+( [а-я]+)*", patstype)
            ):
                continue
            fio = f"{lname} {fname} {sname}"
            temp = Data(patsname, patstype, fio, i)
            if temp in arr:
                continue
            arr[i] = temp
            i += 1
    return arr


def init_arr2(filename, table):
    arr = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 11:
                continue

            patsname = parts[0]
            lname, fname, sname = parts[1], parts[2], parts[3]
            fio = lname + " " + fname + " " + sname

            # Ищем позицию даты в конце
            date_parts = parts[-3:]
            date = " ".join(date_parts)
            if not re.fullmatch(pattern2, date):
                continue

            # Имя врача — три слова перед датой
            doctor_parts = parts[-6:-3]
            doctor = " ".join(doctor_parts)
            if not re.fullmatch(pattern, doctor):
                continue

            # Всё, что между ФИО и doctor — это диагноз
            diagnoz_parts = parts[4:-6]
            if not diagnoz_parts:
                continue
            diagnoz = " ".join(diagnoz_parts)

            # Проверка: диагноз — каждое слово начинается с заглавной только первое, остальные — с маленькой
            if not re.fullmatch(r"[А-ЯЁ][а-яё]+( [а-яё]+)*", diagnoz):
                continue

            if not (
                re.fullmatch(r"[А-ЯЁ][а-яё]+", patsname) and re.fullmatch(pattern, fio)
            ):
                continue

            temp = Priem(patsname, fio, diagnoz, doctor, date)
            if temp._name + temp._owner not in table.keys():
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
