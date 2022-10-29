import time

class Node():
    def __init__(self, key, size, next=None) -> None:
        self.key = key
        self.created_time = time.time()
        self.size = size
        self.next = next

class Queue():
    def __init__(self):
        self.head = None
        self.tail = None
    
    def push_back(self, key, size):
        node = Node(key, size)
        if self.tail is None:
            self.head = node
            self.tail = node
            return
        self.tail.next = node
        self.tail = node

    def pop_front(self):
        if self.head is None:
            return None
        node = self.head
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return node
        self.head = self.head.next
        return node
