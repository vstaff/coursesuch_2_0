from List import List


class Priem:
    def __init__(self, name="", owner="", diagonz="", doctor="", date=""):
        self._name = name
        self._owner = owner
        self._dianoz = diagonz
        self._doctor = doctor
        self._date = date


class Node:
    def __init__(self, obj, index):
        self._key = obj.fio + obj.dob
        self._right = None
        self._list = List()
        self._list.add(index)
        self._left = None
        self._balance = 0

    def get_lst(self):
        return self._list


class AVLT:
    def __init__(self, lst):
        self._root = None
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
        key = data.fio + data.dob

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

        else:  # key == p.key
            if p._list.is_empty():
                p._list.add(index)
            elif not p._list.contains(index):
                p._list.add(index)
            height_changed = False

        return p, height_changed

    def init_tree(self, lst):

        for idx, item in enumerate(lst):
            self._root, _ = self.insert(item, idx, self._root)

    def search(self, data):
        key = data.fio + data.dob
        current = self._root
        while current is not None:
            if key < current.key:
                current = current._left
            elif key > current.key:
                current = current._right
            else:
                return current
        return None

    def remove_max(self, p, temp):
        if p._right is None:
            temp.key = p.key
            temp._list = p._list
            return p._left, True
        else:
            p._right, height_changed = self.remove_max(p._right, temp)
            if height_changed:
                if p._balance == -1:
                    p = self.balance_left(p)
                    height_changed = p._balance != 0
                elif p._balance == 0:
                    p._balance = -1
                    height_changed = False
                else:  # p._balance == 1
                    p._balance = 0
                    height_changed = True
            return p, height_changed

    def node_exists(self, key, node=None):
        if node is None:
            node = self._root
        while node:
            if key < node._key:
                node = node._left
            elif key > node._key:
                node = node._right
            else:
                return True
        return False

    def remove(self, data, p=None, height_changed=False):
        if p is None:
            p = self._root
            root_call = True
        else:
            root_call = False

        if p is None:
            return None, False

        key = data.fio + data.dob

        if key < p._key:
            p._left, height_changed = self.remove(data, p._left, height_changed)
            if height_changed:
                if p._balance == 1:
                    p = self.balance_right(p)
                    height_changed = p._balance == 0
                elif p._balance == 0:
                    p._balance = 1
                    height_changed = False
                else:
                    p._balance = 0
                    height_changed = True
        elif key > p._key:
            p._right, height_changed = self.remove(data, p._right, height_changed)
            if height_changed:
                if p._balance == -1:
                    p = self.balance_left(p)
                    height_changed = p._balance == 0
                elif p._balance == 0:
                    p._balance = -1
                    height_changed = False
                else:
                    p._balance = 0
                    height_changed = True
        else:
            if p._left is None:
                return p._right, True
            elif p._right is None:
                return p._left, True
            else:
                p._left, height_changed = self.remove_max(p._left, p)
                if height_changed:
                    if p._balance == 1:
                        p = self.balance_right(p)
                        height_changed = p._balance == 0
                    elif p._balance == 0:
                        p._balance = 1
                        height_changed = False
                    else:
                        p._balance = 0
                        height_changed = True

        if root_call:
            self._root = p
        return p, height_changed

    def remove_index(self, data, index, p=None):
        if p is None:
            p = self._root
            root_call = True
        else:
            root_call = False

        if p is None:
            return p, False

        key = data.fio + data.dob

        if key < p._key:
            p._left, removed = self.remove_index(data, index, p._left)
        elif key > p._key:
            p._right, removed = self.remove_index(data, index, p._right)
        else:
            removed = p._list.remove_by_value(index)
            if not removed:
                return p, False
            if p._list.is_empty():
                if p._left is None:
                    return p._right, True
                elif p._right is None:
                    return p._left, True
                else:
                    p._left, _ = self.remove_max(p._left, p)

        if root_call:
            self._root = p
        return p, removed

    def find_exact(self, data):
        key = data.fio + data.dob
        node = self._root
        while node is not None:
            if key < node.key:
                node = node._left
            elif key > node.key:
                node = node._right
            else:
                current = node._list._head
                while current is not None:
                    yield current._data
                    current = current._next
                return
        return

    def find_index_by_data(self, data, node=None):
        if node is None:
            node = self._root

        key = data.fio + data.dob
        while node is not None:
            if key < node._key:
                node = node._left
            elif key > node._key:
                node = node._right
            else:
                current = node._list._head
                while current is not None:
                    yield current._data
                    current = current._next
                return
        return

    def inOrder(self, node):
        if node is None:
            return []

        result = []
        result.extend(self.inOrder(node._left))
        result.append(node._list)
        result.extend(self.inOrder(node._right))
        return result
