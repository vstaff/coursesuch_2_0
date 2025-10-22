# from operator import itruediv


class HasgTableStudent:
    def __init__(self, fio="", class_="", dob="", index=None):
        self.fio = fio
        self.class_ = class_
        self.dob = dob
        self.key = sum(ord(c) for c in (fio + dob))
        self.status = 0
        self.index = index

    def __eq__(self, other):
        return (
                isinstance(other, HasgTableStudent)
                and self.fio == other.fio
                and self.class_ == other.class_
                and self.index == other.index
        )


def filesize(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


class Hash_Table:
    def __init__(self, arr, size):
        self.__size = size
        self.__table = [HasgTableStudent() for _ in range(self.__size)]
        self.init_table(arr)

    def get_pos(self, key):
        hash1 = self.hash_func1(key)
        if self.__table[hash1].key == key:
            return self.__table[hash1].index
        else:
            hash2 = self.kvadratich_poisk(key, 1)
            j = 2
            while self.__table[hash2].key != key:
                hash2 = self.kvadratich_poisk(key, j)
                j += 1
            return self.__table[hash2].index

    def keys(self):
        keys = []
        for i in range(self.__size):
            item = self.__table[i].fio + self.__table[i].dob
            if item == " " or item == "":
                continue
            keys.append(item)
        return set(keys)

    def ifFull(self):
        i = 0
        while self.__table[i].status == 1:
            i += 1
            if i >= self.__size:
                return True
        return False

    def isUniq(self, data):
        for i in range(self.__size):
            hash = self.kvadratich_poisk(data.key, i)
            if self.__table[hash].key != data.key:
                continue
            elif (
                    self.__table[hash].key == data.key and self.__table[hash].status == 2
            ):
                continue
            elif (
                    self.__table[hash].key == data.key and self.__table[hash].status == 1
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
            pos = self.kvadratich_poisk(data.key, i)
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
            key = str(data.key) if data.key is not None else ""
            fio = str(data.fio) if data.fio is not None else ""
            class_ = str(data.class_) if data.class_ is not None else ""
            dob = str(data.dob) if data.dob is not None else ""
            index = str(data.index) if data.index is not None else ""
            status = str(data.status) if data.status is not None else ""

            print(
                f"{i:<6}{key:<60}{fio:<20}{class_:<20}{dob:<50}{index:<10}{status:<8}"
            )

    def search_with_steps(self, name, dob):
        key = sum(ord(c) for c in (name + dob))
        steps = 0
        first_addr = self.hash_func1(key)
        second_addr = self.kvadratich_poisk(key, 1)

        for i in range(self.__size):
            pos = self.kvadratich_poisk(key, i)
            steps += 1
            item = self.__table[pos]
            if item.status == 0:
                return None, steps, first_addr, second_addr
            if (
                    item.key == key
                    and item.status == 1
                    and item.fio == name
                    and item.dob == dob
            ):
                return item, steps, first_addr, second_addr
        return None, steps, first_addr, second_addr

    def search(self, name, dob):
        key = sum(ord(c) for c in (name + dob))
        for i in range(self.__size):
            pos = self.kvadratich_poisk(key, i)
            item = self.__table[pos]
            if item.status == 0:
                return None
            if (
                item.key == key
                and item.status == 1
                and item.fio == name
                and item.dob == dob
            ):
                return item
        return None

    def delete(self, data):
        for i in range(self.__size):
            hash = self.kvadratich_poisk(data.key, i)
            if self.__table[hash] == data and self.__table[hash].status == 1:
                self.__table[hash].status = 2
                return True
            if self.__table[hash].status == 0:
                return False
        return False

    def get_size(self):
        return self.__size

    def is_key(self, fio, dob):
        key = sum(ord(c) for c in (fio + dob))
        for i in range(self.__size):
            pos = self.kvadratich_poisk(key, i)
            item = self.__table[pos]

            if item.status == 0:
                return False

            if (
                item.status == 1
                and item.key == key
                and item.fio == fio
                and item.dob == dob
            ):
                return True

        return False
