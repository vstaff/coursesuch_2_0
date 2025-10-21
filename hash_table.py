


# первый справочник
class Student:
    def __init__(self, name="", class_="", date="", index=""):
        self._name: str = name
        self._class_ = class_
        self._date = date
        self._key: int = sum(ord(c) for c in (name + date))
        self._status = 0
        self._index = index

    def __eq__(self, other):
        return (
                isinstance(other, Student)
                and self._name == other._name
                and self._class_ == other._class_
                and self._date == other._date
        )

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
    def key(self):
        return self._key

    @property
    def index(self):
        return self._index

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: int):
        assert (value in [0, 1, 2]), "status must be 0, 1 or 2"
        self._status = value


def get_rows_amount(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


class HashTable:
    def __init__(self, arr, size):
        self.__size = size
        self.__table = [Student() for _ in range(self.__size)]
        self.init_table(arr)

    def get_pos(self, key):
        hash1 = self.hash_func1(key)
        if self.__table[hash1].key == key:
            return self.__table[hash1].index
        else:
            hash2 = self.quadratic_search(key, 1)
            j = 2
            while self.__table[hash2].key != key:
                hash2 = self.quadratic_search(key, j)
                j += 1
            return self.__table[hash2].index

    def get_keys(self):
        keys: list[int] = []
        for i in range(self.__size):
            item = self.__table[i].key
            if item == " " or item == "":
                continue
            keys.append(item)
        return set(keys)

    def is_full(self):
        i = 0
        while self.__table[i].status == 1:
            i += 1
            if i >= self.__size:
                return True
        return False

    def is_unique(self, data: Student):
        for i in range(self.__size):
            quadratic_hash = self.quadratic_search(data.key, i)
            if self.__table[quadratic_hash].key != data.key:
                continue
            elif (
                    self.__table[quadratic_hash].key == data.key and self.__table[quadratic_hash].status == 2
            ):
                continue
            elif (
                    self.__table[quadratic_hash].key == data.key and self.__table[quadratic_hash].status == 1
            ):
                return False
        return True

    def hash_func1(self, key):
        return abs(key % self.__size)

    def quadratic_search(self, key, i):
        return (self.hash_func1(key) + i * 1 + i * i) % self.__size

    def lin_prob(self, key, i):
        return (self.hash_func1(key) + i) % self.__size

    def insert(self, data: Student):
        if self.is_full():
            print("Не добавлено, таблица заполнена")
            return False

        first_deleted_pos = None

        for i in range(self.__size):
            pos = self.quadratic_search(data.key, i)
            item = self.__table[pos]

            if item.status == 1 and item.key == data.key:
                print("Не добавлено, уже существует")
                return False

            if item.status == 2 and first_deleted_pos is None:
                first_deleted_pos = pos

            if item.status == 0:
                insert_pos = first_deleted_pos if first_deleted_pos is not None else pos
                self.__table[insert_pos] = data
                self.__table[insert_pos].status = 1
                print("Добавлено")
                return True

        if first_deleted_pos is not None:
            self.__table[first_deleted_pos] = data
            self.__table[first_deleted_pos].status = 1
            print("Добавлено (в удалённую)")
            return True

        print("Не добавлено")
        return False

    def init_table(self, arr):
        for temp in arr:
            self.insert(temp)

    def get_table(self):
        return self.__table

    def print_table(self):
        print(
            f"{'Index':<6}{'Key':<60}{'Name':<20}{'Type':<20}{'FIO':<50}{'position':<10}{'Status':<8}"
        )
        print("-" * 170)
        for i, data in enumerate(self.__table):
            key = str(data.key) or ""
            name = data.name or ""
            class_ = data.class_ or ""
            date = data.date or ""
            status = str(data.status) or ""
            index = str(data.index) or ""

            print(
                f"{i:<6}{key:<60}{name:<20}{class_:<20}{date:<50}{index:<10}{status:<8}"
            )

    def search(self, name: str, date: str):
        key = sum(ord(c) for c in (name + date))
        for i in range(self.__size):
            pos = self.quadratic_search(key, i)
            item = self.__table[pos]
            if item.status == 0:
                return None
            if (
                    item.key == key
                    and item.status == 1
                    and item.name == name
                    and item.date == date
            ):
                return item
        return None

    def delete(self, data):
        for i in range(self.__size):
            quadratic_hash = self.quadratic_search(data.key, i)
            if self.__table[quadratic_hash] == data and self.__table[quadratic_hash].status == 1:
                self.__table[quadratic_hash].status = 2
                return True
            if self.__table[quadratic_hash].status == 0:
                return False
        return False

    def get_size(self):
        return self.__size

    def is_key(self, name, date: str):
        key = sum(ord(c) for c in (name + date))
        for i in range(self.__size):
            pos = self.quadratic_search(key, i)
            item = self.__table[pos]

            if item.status == 0:
                return False

            if (
                    item.status == 1
                    and item.key == key
                    and item.name == name
                    and item.date == date
            ):
                return True

        return False
