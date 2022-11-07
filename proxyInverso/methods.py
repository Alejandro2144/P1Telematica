import constants
import logging

logging.basicConfig(level = logging.INFO, filename = constants.BASE_DIR + "/logging.log", filemode = "w", format = "%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

def log(msg):
    print(msg)
    logger.info(msg)

def find_bytes_in_bytes(cur_bytes, search_bytes, start=0, end=-1):
        if end == -1:
            end = len(cur_bytes)
        for i in range(start, end):
            if cur_bytes[i:i+len(search_bytes)] == search_bytes:
                return i
        return -1

def get_header(initial_message):
    HTTP_HEADER_DELIMITER = b'\r\n\r\n'
    return initial_message[:find_bytes_in_bytes(initial_message, HTTP_HEADER_DELIMITER)]

def get_file(server_response):
    HTTP_HEADER_DELIMITER = b'\r\n\r\n'
    return server_response[find_bytes_in_bytes(server_response, HTTP_HEADER_DELIMITER)+4:]