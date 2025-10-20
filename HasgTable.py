from operator import itruediv


class Data:
    def __init__(self, name="", type="", owner="", index=""):
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


class Hash_Table:
    def __init__(self, arr, size):
        self.__size = size
        self.__table = [Data() for _ in range(self.__size)]
        self.init_table(arr)

    def get_pos(self, key):
        hash1 = self.hash_func1(key)
        if self.__table[hash1]._key == key:
            return self.__table[hash1]._index
        else:
            hash2 = self.kvadratich_poisk(key, 1)
            j = 2
            while self.__table[hash2]._key != key:
                hash2 = self.kvadratich_poisk(key, j)
                j += 1
            return self.__table[hash2]._index

    def keys(self):
        keys = []
        for i in range(self.__size):
            item = self.__table[i]._name + self.__table[i]._owner
            if item == " " or item == "":
                continue
            keys.append(item)
        return set(keys)

    def ifFull(self):
        i = 0
        while self.__table[i]._status == 1:
            i += 1
            if i >= self.__size:
                return True
        return False

    def isUniq(self, data):
        for i in range(self.__size):
            hash = self.kvadratich_poisk(data._key, i)
            if self.__table[hash]._key != data._key:
                continue
            elif (
                self.__table[hash]._key == data._key and self.__table[hash]._status == 2
            ):
                continue
            elif (
                self.__table[hash]._key == data._key and self.__table[hash]._status == 1
            ):
                return False
        return True

    def hash_func1(self, key):
        return abs(key % self.__size)

    def kvadratich_poisk(self, key, i):
        return (self.hash_func1(key) + i * 1 + i * i) % self.__size

    def lin_prob(self, key, i):
        return (self.hash_func1(key) + i) % self.__size

    def insert(self, data):
        if self.ifFull():
            print("Не добавлено, таблица заполнена")
            return False

        first_deleted_pos = None

        for i in range(self.__size):
            pos = self.kvadratich_poisk(data._key, i)
            item = self.__table[pos]

            if item._status == 1 and item._key == data._key:

                print("Не добавлено, уже существует")
                return False

            if item._status == 2 and first_deleted_pos is None:
                first_deleted_pos = pos

            if item._status == 0:
                insert_pos = first_deleted_pos if first_deleted_pos is not None else pos
                self.__table[insert_pos] = data
                self.__table[insert_pos]._status = 1
                print("Добавлено")
                return True

        if first_deleted_pos is not None:
            self.__table[first_deleted_pos] = data
            self.__table[first_deleted_pos]._status = 1
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
            key = str(data._key) if data._key is not None else ""
            name = str(data._name) if data._name is not None else ""
            type_ = str(data._type) if data._type is not None else ""
            owner = str(data._owner) if data._owner is not None else ""
            index = str(data._index) if data._index is not None else ""
            status = str(data._status) if data._status is not None else ""

            print(
                f"{i:<6}{key:<60}{name:<20}{type_:<20}{owner:<50}{index:<10}{status:<8}"
            )

    def search(self, name, owner):
        key = sum(ord(c) for c in (name + owner))
        for i in range(self.__size):
            pos = self.kvadratich_poisk(key, i)
            item = self.__table[pos]
            if item._status == 0:
                return None
            if (
                item._key == key
                and item._status == 1
                and item._name == name
                and item._owner == owner
            ):
                return item
        return None

    def delete(self, data):
        for i in range(self.__size):
            hash = self.kvadratich_poisk(data._key, i)
            if self.__table[hash] == data and self.__table[hash]._status == 1:
                self.__table[hash]._status = 2
                return True
            if self.__table[hash]._status == 0:
                return False
        return False

    def get_size(self):
        return self.__size

    def is_key(self, name, owner):
        key = sum(ord(c) for c in (name + owner))
        for i in range(self.__size):
            pos = self.kvadratich_poisk(key, i)
            item = self.__table[pos]

            if item._status == 0:
                return False

            if (
                item._status == 1
                and item._key == key
                and item._name == name
                and item._owner == owner
            ):
                return True

        return False
