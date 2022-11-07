import os
import time
import threading
import constants
from Queue import Queue
from methods import find_bytes_in_bytes,  get_header

class LRUCache():
    def __init__(self):
        self.queue = Queue()
        self.dictionary = {}
        self.cur_size = 0
        self.lock = threading.Lock()

    def insert(self, request, file, size):
        with self.lock:
            if size > constants.CACHE_SIZE or not self.check_get_request(request):
                return
            while self.cur_size + size > constants.CACHE_SIZE:
                node = self.queue.pop_front()
                if node is None:
                    break
                del self.dictionary[node.key]
                self.cur_size -= node.size
            file_name = self.get_file_name(request)
            node = self.queue.push_back(request, file_name, size)
            self.dictionary[request] =  node
            self.write_to_file(file_name, file)
            self.cur_size += size
    
    def check_get_request(self, request):
        end = find_bytes_in_bytes(request, b'\r\n')
        get_GET = find_bytes_in_bytes(request, b'GET', 0, end)
        return get_GET != -1

    def get_file_name(self, request):
        start = find_bytes_in_bytes(request, b' ')
        end = find_bytes_in_bytes(request, b' ', start+1)
        full_file_name = request[start + 1:end]
        end = 0
        final_slash = 0
        while end != -1:
            final_slash = end
            end = find_bytes_in_bytes(full_file_name, b'/', final_slash+1)
        file_name = str(full_file_name[final_slash:], constants.ENCONDING_FORMAT)
        print(file_name)
        if file_name[-1] == '/':
            file_name = file_name + 'index.html'
        return file_name

    def get(self, request):
        with self.lock:
            if request in self.dictionary:
                node = self.dictionary[request]
                self.move_to_front(node)
                file = self.read_file(node)
                responce = self.create_response(node, file)
                return responce
            return None

    def move_to_front(self, node):
        self.queue.pop_node(node)
        self.queue.push_back(node.key, node.file_name, node.size)

    def create_response(self, node, file):
        header = (
            b'HTTP/1.1 200 OK\r\n' + 
            b'Content-Length: ' + bytes(str(node.size), constants.ENCONDING_FORMAT) + b'\r\n' +
            b'Server: Proxy' +
            b'\r\n\r\n')
        return header + file

    def update(self):
        self.update_ttl()

    def update_ttl(self):
        while self.queue.head is not None and time.time() - self.queue.head.created_time > constants.TTL:
            node = self.queue.pop_front()
            os.remove(f"{constants.BASE_DIR}/cache{node.file_name}")
            del self.dictionary[node.key]

    
    def write_to_file(self, file_name, file):
        print('File name',file_name)
        with open(f"{constants.BASE_DIR}/cache{file_name}", "wb") as binary_file:
            binary_file.write(file)

    def read_file(self, node):
        with open(f"{constants.BASE_DIR}/cache{node.file_name}", "rb") as binary_file:
            return binary_file.read(node.size)
