class ListNode:
    def __init__(self, data):
        self._data = data
        self._next: None | ListNode = None
        self._prev: None | ListNode = None

    @property
    def data(self):
        return self._data

    @property
    def next(self):
        return self._next

    @property
    def prev(self):
        return self._prev


class MyList:
    def __init__(self):
        self._head: None | ListNode = None
        self._tail: None | ListNode = None
        self._size = 0

    @property
    def head(self):
        return self._head

    def add(self, data):
        temp = ListNode(data)
        temp._prev = self._tail
        if self._tail is not None:
            self._tail._next = temp
        if self._head is None:
            self._head = temp
        self._tail = temp
        self._size += 1

    def print_list(self):
        t = self._head
        while t is not None:
            print(t._data, end=" ")
            t = t._next

    def delete(self, data):
        current = self._head
        while current is not None:
            if current._data == data:
                if current == self._head:
                    self._head = current._next
                    if self._head:
                        self._head._prev = None
                    else:
                        self._tail = None
                elif current == self._tail:
                    self._tail = current._prev
                    if self._tail:
                        self._tail._next = None
                else:
                    current._prev._next = current._next
                    current._next._prev = current._prev
                self._size -= 1
                return True
            current = current._next
        return False

    def remove_by_value(self, val):
        current = self._head
        while current:
            if current._data == val:
                if current._prev:
                    current._prev._next = current._next
                else:
                    self._head = current._next
                if current._next:
                    current._next._prev = current._prev
                else:
                    self._tail = current._prev
                self._size -= 1
                return True
            current = current._next
        return False

    def contains(self, value):
        current = self._head
        while current:
            if current._data == value:
                return True
            current = current._next
        return False

    def get_size(self):
        return self._size

    def is_empty(self):
        return self._head is None

    def __getitem__(self, index):
        if not 0 <= index < self._size:
            raise IndexError("Index out of bounds")
        current = self._head
        for _ in range(index):
            current = current._next
        return current._data

    def __setitem__(self, index, value):
        if not 0 <= index < self._size:
            raise IndexError("Index out of bounds")
        current = self._head
        for _ in range(index):
            current = current._next
        current._data = value
