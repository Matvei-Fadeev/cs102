class Node:
    def __init__(self, value=None, next=None):
        self.contained_object = value
        self.next = next


class MyQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, value):
        if not self.head:
            self.head = Node(value)
            self.tail = self.head
        else:
            self.head = Node(value, self.head)

    def clear(self):
        self.head = None
        self.tail = None

    def remove(self):
        if self.head:
            self.head = self.head.next
        elif self.head == self.head:
            clear()

    def get_list(self):
        queue = []
        while self.head:
            queue.append(self.head.contained_object)
            self.head = self.head.next
        return queue


#
