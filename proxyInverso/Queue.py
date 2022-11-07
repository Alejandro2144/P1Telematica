import time

class Node():
    def __init__(self, key, file_name, size, prev=None, next=None) -> None:
        self.key = key
        self.file_name = file_name
        self.created_time = time.time()
        self.size = size
        self.prev = prev
        self.next = next

class Queue():
    def __init__(self):
        self.head = None
        self.tail = None
    
    def push_back(self, key, file_name, size):
        node = Node(key, file_name, size)
        if self.tail is None:
            self.head = node
            self.tail = node
            return node
        node.prev = self.tail
        self.tail.next = node
        self.tail = node
        return node

    def pop_front(self):
        if self.head is None:
            return None
        node = self.head
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return node
        self.head = self.head.next
        self.head.prev = None
        return node
    
    def pop_node(self, node):
        if node is self.head:
            self.pop_front()
            node.next = None
            return node
        if node is self.tail:
            node.prev.next = None
            node.tail = node.prev
            node.prev = None
            return node
        node.prev.next = node.next
        node.next.prev = node.prev
        return node
