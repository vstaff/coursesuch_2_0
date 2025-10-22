from List import List


class PetsPriem:
    def __init__(self, name="", type="", owner="", diagonz="", doctor="", date=""):
        self._name = name
        self._type = type
        self._owner = owner
        self._dianoz = diagonz
        self._doctor = doctor
        self._date = date

    def __str__(self):
        return (
            f"Name: {self._name}, Owner: {self._owner}, "
            f"Diagnosis: {self._dianoz}, Doctor: {self._doctor}, Date: {self._date}"
        )


class Node:
    def __init__(self, obj, index):
        self._key = obj._date
        self._right = None
        self._list = List()
        self._list.add(index)
        self._left = None
        self._balance = 0


class AVLT2:
    def __init__(self, lst, hashtable):
        self._root = None
        self.hashtable = hashtable
        self.init_tree(lst)

    def balance_left(self, p):
        p1 = p._left
        if p1._balance == -1:
            p._left = p1._right
            p1._right = p
            p._balance = 0
            p1._balance = 0
            return p1
        else:
            p2 = p1._right
            p1._right = p2._left
            p2._left = p1
            p._left = p2._right
            p2._right = p
            if p2._balance == -1:
                p._balance = 1
            else:
                p._balance = 0
            if p2._balance == 1:
                p1._balance = -1
            else:
                p1._balance = 0
            p2._balance = 0
            return p2

    def balance_right(self, p):

        p1 = p._right
        if p1._balance == 1:
            p._right = p1._left
            p1._left = p
            p._balance = 0
            p1._balance = 0
            return p1
        else:
            p2 = p1._left
            p1._left = p2._right
            p2._right = p1
            p._right = p2._left
            p2._left = p
            if p2._balance == 1:
                p._balance = -1
            else:
                p._balance = 0
            if p2._balance == -1:
                p1._balance = 1
            else:
                p1._balance = 0
            p2._balance = 0
            return p2

    def insert(self, data, index, p):
        if p is None:
            return Node(data, index), True

        height_changed = False
        key = data._date

        if key < p.key:
            p._left, height_changed = self.insert(data, index, p._left)
            if height_changed:
                if p._balance == -1:
                    p = self.balance_left(p)
                    height_changed = False
                elif p._balance == 0:
                    p._balance = -1
                    height_changed = True
                else:
                    p._balance = 0
                    height_changed = False
        elif key > p.key:
            p._right, height_changed = self.insert(data, index, p._right)
            if height_changed:
                if p._balance == 1:
                    p = self.balance_right(p)
                    height_changed = False
                elif p._balance == 0:
                    p._balance = 1
                    height_changed = True
                else:
                    p._balance = 0
                    height_changed = False
        else:
            p._list.add(index)
            height_changed = False
        return p, height_changed

    def init_tree(self, lst):

        for idx, item in enumerate(lst):
            type = self.hashtable.search(item._name, item._owner)._type
            temp = PetsPriem(
                item._name, type, item._owner, item._dianoz, item._doctor, item._date
            )
            self._root, _ = self.insert(temp, idx, self._root)

    def inOrder(self, node):
        if node is None:
            return []

        result = []
        result.extend(self.inOrder(node._left))
        result.append(node._list)
        result.extend(self.inOrder(node._right))
        return result

    def search(self, date):
        key = date
        current = self._root
        while current is not None:
            if key < current.key:
                current = current._left
            elif key > current.key:
                current = current._right
            else:
                return True
        return False
