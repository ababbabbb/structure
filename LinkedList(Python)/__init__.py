class LinkedList:
    class Node:
        __slots__ = 'value', 'prev', 'next'

        def __init__(self, value=None, prev=None, next=None):
            self.value = value
            self.prev = prev
            self.next = next

    def __init__(self, iterable=None):
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.length = 0
        if iterable:
            if hasattr(iterable, '__iter__'):
                for value in iterable:
                    self.append(value)
            else:
                self.append(iterable)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return [self[i] for i in range(start, stop, step)]
        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError("list index out of range")
        node = self._get_node(index)
        return node.value

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if step != 1:
                raise ValueError("Can only assign with step 1")
            if len(value) != stop - start:
                raise ValueError(
                    "Attempt to assign sequence of size %d to slice of size %d" % (len(value), stop - start))
            for i in range(start, stop):
                self[i] = value[i - start]
        else:
            if index < 0:
                index += len(self)
            if not 0 <= index < len(self):
                raise IndexError("list assignment index out of range")
            node = self._get_node(index)
            node.value = value

    def __delitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            for i in reversed(range(start, stop, step)):
                del self[i]
        else:
            if index < 0:
                index += len(self)
            if not 0 <= index < len(self):
                raise IndexError("list assignment index out of range")
            node = self._get_node(index)
            node.prev.next = node.next
            node.next.prev = node.prev
            self.length -= 1

    def __iter__(self):
        node = self.head.next
        while node.next is not None:
            yield node.value
            node = node.next

    def __contains__(self, value):
        node = self.head.next
        while node.next is not None:
            if node.value == value:
                return True
            node = node.next
        return False

    def __add__(self, other):
        if not isinstance(other, LinkedList):
            raise TypeError("can only concatenate list (not \"%s\") to list" % type(other).__name__)
        result = LinkedList(self)
        for value in other:
            result.append(value)
        return result

    def __iadd__(self, other):
        if not isinstance(other, LinkedList):
            raise TypeError("can only concatenate list (not \"%s\") to list" % type(other).__name__)
        for value in other:
            self.append(value)
        return self

    def __str__(self):
        result = '>'
        for node in self:
            result += str(node) + ', '

        return result[:-2] + '<'

    def append(self, value):
        node = self.Node(value=value, prev=self.tail.prev, next=self.tail)
        node.prev.next = node
        self.tail.prev = node
        self.length += 1

    def extend(self, iterable):
        for value in iterable:
            self.append(value)

    def insert(self, index, value):
        if index < 0:
            index += len(self)
        if not 0 <= index <= len(self):
            raise IndexError("list index out of range")
        node = self._get_node(index)
        new_node = self.Node(value=value, prev=node.prev, next=node)
        new_node.prev.next = new_node
        node.prev = new_node
        self.length += 1

    def remove(self, value):
        node = self.head.next
        while node.next is not None:
            if node.value == value:
                node.prev.next = node.next
                node.next.prev = node.prev
                self.length -= 1
                return
            node = node.next
        raise ValueError("list.remove(x): x not in list")

    def pop(self, index=-1):
        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError("pop index out of range")
        node = self._get_node(index)
        node.prev.next = node.next
        node.next.prev = node.prev
        self.length -= 1
        return node.value

    def clear(self):
        self.head.next = self.tail
        self.tail.prev = self.head
        self.length = 0

    def index(self, value):
        node = self.head.next
        i = 0
        while node.next is not None:
            if node.value == value:
                return i
            node = node.next
            i += 1
        raise ValueError("list.index(x): x not in list")

    def count(self, value):
        node = self.head.next
        count = 0
        while node.next is not None:
            if node.value == value:
                count += 1
            node = node.next
        return count

    def reverse(self):
        node = self.head.next
        while node.next is not None:
            node.prev, node.next = node.next, node.prev
            node = node.prev
        self.head.next, self.tail.prev = self.tail.prev, self.head.next

    def sort(self, key=None, reverse=False):
        if key is None:
            key = lambda x: x
        if len(self) <= 1:
            return
        pivot = self.head.next
        left = LinkedList()
        right = LinkedList()
        while pivot.next is not None:
            if key(pivot.value) < key(self.tail.prev.value):
                left.append(pivot.value)
            else:
                right.append(pivot.value)
            pivot = pivot.next
        left.sort(key=key, reverse=reverse)
        right.sort(key=key, reverse=reverse)
        self.head.next = left.head.next
        left.tail.prev.next = right.head.next
        right.tail.prev.next = self.tail
        self.tail.prev = right.tail.prev
        if reverse:
            self.reverse()

    def _get_node(self, index):
        if index <= len(self) // 2:
            node = self.head.next
            for i in range(index):
                node = node.next
        else:
            node = self.tail.prev
            for i in reversed(range(index + 1, len(self))):
                node = node.prev
        return node


if __name__ == '__main__':
    my_list = LinkedList(['一', '二', '三', '四', 5, 6])
    print(len(my_list))  # 输出：6
    print(my_list[0])  # 输出：1
    my_list[0] = 0
    print(my_list[0])  # 输出：0
    del my_list[0]
    print(my_list[0])  # 输出：2
    my_list.append(6)
    print(my_list[-1])  # 输出：6
    my_list.insert(1, 1)
    print(my_list[1])  # 输出：1
    my_list.remove('三')
    print(len(my_list))  # 输出：5
    print(my_list.pop())  # 输出：6
    for item in my_list:
        print(item)

    print(my_list)
    print('end')

    # list -> 动态数组 -> 数组
    # 链表 -> node
