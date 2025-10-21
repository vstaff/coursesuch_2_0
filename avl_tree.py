from MyList import MyList
from dataclasses import dataclass


# справочник 2
@dataclass
class Grade:
    student_name: str = ""
    subject: str = ""
    grade: str = ""
    date: str = ""


class Node:
    def __init__(self, grade: Grade, index: int):
        self._key = grade.student_name
        self._right: None | Node = None
        self._list = MyList()
        self._list.add(index)
        self._left: None | Node = None
        self._balance = 0

    @property
    def key(self) -> str:
        return self._key

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, obj) -> None:
        assert isinstance(obj, Node | None), f"left must be a Node or None, received {type(obj)}"
        self._left = obj

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, obj) -> None:
        assert isinstance(obj, Node | None), f"right must be a Node or None, received {type(obj)}"
        self._right = obj

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        assert isinstance(value, int), f"balance must be a int, received {type(value)}"
        self._balance = value

    @property
    def list(self):
        return self._list


class AVLTree:
    def __init__(self, lst):
        self._root: None | Node = None
        self.init_tree(lst)

    # утил методы (вспомогательные)
    def _height(self, node: Node):
        if not node:
            return 0
        return max(self._height(node.left), self._height(node.right)) + 1

    def _get_balance(self, node):
        if not node:
            return 0
        return self._height(node.right) - self._height(node.right)

    def _update_balance(self, node):
        if node:
            node._balance = self._get_balance(node)

    def _rotate_left(self, z):
        y = z._right
        t2 = y._left

        # поворачиваю
        y._left = z
        z._right = t2

        # меняю баланс
        self._update_balance(z)
        self._update_balance(y)
        return y

    def _rotate_right(self, z):
        y = z._left
        t3 = y._right

        # делаю поворот
        y._right = z
        z._left = t3

        # обновляюбаланс
        self._update_balance(z)
        self._update_balance(y)
        return y

        #

    # methods для балансировки
    def _rebalance(self, node):
        self._update_balance(node)
        if node.balance < -1:
            # Левое поддерево тяжелее
            if self._get_balance(node._left) > 0:
                node._left = self._rotate_left(node._left)
            return self._rotate_right(node)
        elif node.balance > 1:
            # Правое поддерево тяжелее
            if self._get_balance(node._right) < 0:
                node._right = self._rotate_right(node._right)
            return self._rotate_left(node)
        return node

    def insert(self, obj: Grade, index: int):
        self._root = self._insert(self._root, obj, index)

    def _insert(self, node, obj, index):
        if not node:
            return Node(obj, index)

        key = obj.student_name + obj.subject

        if key < node.key:
            node._left = self._insert(node._left, obj, index)
        elif key > node.key:
            node._right = self._insert(node._right, obj, index)
        else:
            # такой ключ уже есть — просто добавляем индекс
            node.get_list().add(index)
            return node

        # Балансировка
        node = self._rebalance(node)
        return node

    @staticmethod
    def _find_min_right(node: Node):
        current = node
        while current.left is not None:
            current = current.left
        return current



    def delete(self, obj: Grade):
        key = obj.student_name + obj.subject
        self._root = self._delete(self._root, key)

    def _delete(self, node: Node, key):
        if not node:
            return None

        if key < node.key:
            node._left = self._delete(node.left, key)
        elif key > node.key:
            node._right = self._delete(node.right, key)
        else:
            # Нашли узел для удаления
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Заменяем на минимальный справа
                min_node = self._find_min_right(node.right)
                node._key = min_node.key
                node._list = min_node.list
                node._right = self._delete(node.right, min_node.key)

        # Балансировка
        node = self._rebalance(node)
        return node

    # === ОБХОД (СПРАВА-НАЛЕВО) ===
    def traverse(self):
        result = []
        self._traverse(self._root, result)
        return result

    def _traverse(self, node, result):
        if node:
            self._traverse(node.right, result)
            result.append((node.right, node.get_list()))
            self._traverse(node.left, result)

    # вспомогательная хуйня для отладки
    def print_tree(self, node: None | Node = None, level=0):
        if node is None:
            node = self._root
        if node.right:
            self.print_tree(node.right, level + 1)
        print("    " * level + f"{node.key} (bal={node.balance})")
        if node.left:
            self.print_tree(node.left, level + 1)

    def find(self, obj_or_key: str | Grade):
        if isinstance(obj_or_key, Grade):
            key = obj_or_key.student_name + obj_or_key.subject
        else:
            key = obj_or_key
        return self._find(self._root, key)

    def _find(self, node: Node, key: str):
        if not node:
            return None

        if key < node.key:
            return self._find(node.left, key)
        elif key > node.key:
            return self._find(node.right, key)
        else:
            return node  # Нашли

    def init_tree(self, lst):
        for idx, item in enumerate(lst):
            self.insert(item, idx)

    def node_exists(self, key: str, node: Node | None=None):
        if node is None:
            node = self._root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return True
        return False

    def remove_index(self, data: Grade, index, p: None | Node=None):
        if p is None:
            p = self._root
            root_call = True
        else:
            root_call = False

        if p is None:
            return p, False

        key = data.student_name

        if key < p.key:
            p._left, removed = self.remove_index(data, index, p.left)
        elif key > p.key:
            p._right, removed = self.remove_index(data, index, p.left)
        else:
            removed = p.list.remove_by_value(index)
            if not removed:
                return p, False
            if p.list.is_empty():
                if p.left is None:
                    return p.right, True
                elif p.right is None:
                    return p.left, True
                else:
                    p._left, _ = self.remove_max(p.left, p)

        if root_call:
            self._root = p
        return p, removed

    def remove_max(self, p: Node | None, temp: Node):
        if p.right is None:
            temp._key = p.key
            temp._list = p.list
            return p.left, True
        else:
            p._right, height_changed = self.remove_max(p.right, temp)
            if height_changed:
                if p.balance == -1:
                    p = self._rotate_left(p)
                    height_changed = p._balance != 0
                elif p.balance == 0:
                    p._balance = -1
                    height_changed = False
                else:  # p._balance == 1
                    p._balance = 0
                    height_changed = True
            return p, height_changed

    def find_exact(self, data: Grade):
        key = data.student_name
        node = self._root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                current = node.list.head
                while current is not None:
                    yield current.data
                    current = current.next
                return
        return

    def find_index_by_data(self, data: Grade, node=None):
        if node is None:
            node = self._root

        key = data.student_name
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                current = node.list.head
                while current is not None:
                    yield current.data
                    current = current.next
                return
        return

    def in_order(self, node: None | Node):
        if node is None:
            return []

        result = []
        result.extend(self.in_order(node.left))
        result.append(node.list)
        result.extend(self.in_order(node.right))
        return result
