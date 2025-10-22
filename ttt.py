import re


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


def filesize(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


def init_arr1(filename):
    arr = [Data() for _ in range(filesize(filename))]
    with open(filename, "r", encoding="utf-8") as file:
        i = 0
        for line in file:
            parts = line.strip().split()
            if len(parts) < 5:
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
            arr[i] = Data(patsname, patstype, fio, i)
            i += 1
    return arr


def h(arr, s):
    for i in arr:
        s.append(abs(i.key % 10))
    return s


arr = init_arr1("Client.txt")

f = arr[0]

# for c in arr[0].fio + arr[0].owner:
#      print(ord(c))
s = "Рекс Собака Артем Валерьевич Зуев"
print(sum(ord(c) for c in s) % 10)

# if i != len(self.mainw.arrt) - 1:
#                         last = self.mainw.arrt.pop()
#                         last.index = i
#                         self.mainw.arrt[i] = last
#                     else:
#                         self.mainw.arrt.pop()
#
#                     found = self.mainw.table.search(name, owner)
#                     if found:
#                         self.mainw.table.delete(found)
