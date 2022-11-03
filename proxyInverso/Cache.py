import time
import threading
import constants
from Queue import Queue
from methods import find_bytes_in_bytes

class LRUCache():
    def __init__(self):
        self.lock = threading.Lock()
        self.read_file()

    def insert(self, request, response, size):
        with self.lock:
            if size > constants.CACHE_SIZE or not self.check_get_request(request):
                return
            while self.cur_size + size > constants.CACHE_SIZE:
                node = self.queue.pop_front()
                if node is None:
                    break
                del self.dictionary[node.key]
                self.cur_size -= node.size
            self.queue.push_back(request, size)
            self.dictionary[request] =  response
            self.cur_size += size

    def check_get_request(self, request):
        end = find_bytes_in_bytes(request, b'\r\n')
        get_GET = find_bytes_in_bytes(request, b'GET', 0, end)
        return get_GET != -1

    def get(self, request):
        with self.lock:
            if request in self.dictionary:
                return self.dictionary[request]
            return None

    def update(self):
        self.update_ttl()
        self.write_to_file()

    def update_ttl(self):
        while self.queue.head is not None and time.time() - self.queue.head.created_time > constants.TTL:
            node = self.queue.pop_front()
            del self.dictionary[node.key]
    
    def write_to_file(self):
        with open(constants.BASE_DIR + "/cache.bytes", "wb") as binary_file:
            binary_file.write(bytes(str(self.cur_size) + '\r\n', 'utf-8'))
            binary_file.write(bytes(str(len(self.dictionary)) + '\r\n', 'utf-8'))
            node = self.queue.head
            while node is not None:
                binary_file.write(bytes(str(len(node.key)) + '\r\n', 'utf-8'))
                binary_file.write(node.key)
                binary_file.write(bytes(str(len(self.dictionary[node.key])) + '\r\n', 'utf-8'))
                binary_file.write(self.dictionary[node.key])
                node = node.next

    def read_file(self):
        self.queue = Queue()
        self.dictionary = {}
        self.cur_size = 0
        with open(constants.BASE_DIR + "/cache.bytes", "rb") as binary_file:
            first_line = binary_file.readline()
            if first_line == b'':
                self.cur_size = 0
                return
            self.cur_size = int(first_line)
            dictionary_length = int(binary_file.readline())
            for i in range(dictionary_length):
                request_size = int(binary_file.readline())
                request = binary_file.read(request_size)
                response_size = int(binary_file.readline())
                response = binary_file.read(response_size)
                self.insert(request, response, len(request)+len(response))

