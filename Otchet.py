from MyList import MyList
from hash_table import HashTable


class StudentGrade:
    def __init__(self, full_name="", class_="", birth_date="", subject="", grade=0):
        self._full_name = full_name
        self._class_ = class_
        self._birth_date = birth_date
        self._subject = subject
        self._grade = grade

    def __str__(self):
        return (
            f"ФИО: {self._full_name}, Класс: {self._class_}, Дата Рождения: {self._birth_date}, "
            f"Предмет: {self._subject}, Оценка: {self._grade}"
        )

    @property
    def full_name(self):
        return self._full_name

    @property
    def class_(self):
        return self._class_

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def subject(self):
        return self._subject

    @property
    def grade(self):
        return self._grade


class Node:
    def __init__(self, obj: StudentGrade, index):
        self._key = obj.birth_date
        self._right: Node | None = None
        self._list = MyList()
        self._list.add(index)
        self._left: Node | None = None
        self._balance = 0

    @property
    def key(self):
        return self._key

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        assert isinstance(value, Node), "правый узел должен быть экземпляра класса Node"
        self._right = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        assert isinstance(value, Node), "левый узел должен быть экземпляром класса Node"
        self._left = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    @property
    def list(self):
        return self._list


class AVLTree2:
    def __init__(self, lst, hashtable: HashTable):
        self._root: None | Node = None
        self.hashtable = hashtable
        self.init_tree(lst)

    @staticmethod
    def balance_left(p):
        p1 = p.left
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

    @staticmethod
    def balance_right(p: Node):

        p1 = p.right
        if p1.balance == 1:
            p._right = p1.left
            p1._left = p
            p._balance = 0
            p1._balance = 0
            return p1
        else:
            p2 = p1.left
            p1._left = p2.right
            p2._right = p1
            p._right = p2.left
            p2._left = p
            if p2.balance == 1:
                p.balance = -1
            else:
                p._balance = 0
            if p2.balance == -1:
                p1._balance = 1
            else:
                p1._balance = 0
            p2._balance = 0
            return p2

    def insert(self, data: StudentGrade, index: int, p: Node):
        if p is None:
            return Node(data, index), True

        key = data.birth_date

        if key < p.key:
            p._left, height_changed = self.insert(data, index, p.left)
            if height_changed:
                if p.balance == -1:
                    p = self.balance_left(p)
                    height_changed = False
                elif p.balance == 0:
                    p._balance = -1
                    height_changed = True
                else:
                    p._balance = 0
                    height_changed = False
        elif key > p.key:
            p._right, height_changed = self.insert(data, index, p.right)
            if height_changed:
                if p.balance == 1:
                    p = self.balance_right(p)
                    height_changed = False
                elif p.balance == 0:
                    p._balance = 1
                    height_changed = True
                else:
                    p._balance = 0
                    height_changed = False
        else:
            p.list.add(index)
            height_changed = False
        return p, height_changed

    def init_tree(self, lst: list[StudentGrade]):

        for idx, item in enumerate(lst):
            # class_ = self.hashtable.search(item.full_name, item.birth_date).class_
            temp = StudentGrade(
                item.full_name, item.class_, item.birth_date, item.subject, item.grade
            )
            self._root, _ = self.insert(temp, idx, self._root)

    def in_order(self, node: Node):
        if node is None:
            return []

        result = []
        result.extend(self.in_order(node.left))
        result.append(node.list)
        result.extend(self.in_order(node.right))
        return result

    def search(self, date: str):
        key = date
        current = self._root
        while current is not None:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return True
        return False
