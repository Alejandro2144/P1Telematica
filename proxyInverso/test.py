test = b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nsec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "macOS"\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: csrftoken=Bz5exAC9lbi1JIuKonrUnn2Fem3kBJ8dMqJVbiz6hULL9dj5fvvSonFyY2bn8UeB\r\nIf-None-Match: W/"6b7-183848cf105"\r\nIf-Modified-Since: Wed, 28 Sep 2022 14:42:52 GMT'

CONTENT_LENGTH_FIELD = b'Content-Length: '

def get_content_length_field(head):
    start = find_bytes_in_bytes(head, CONTENT_LENGTH_FIELD) # + len(CONTENT_LENGTH_FIELD)
    if start == -1:
        return len(head)
    end = find_bytes_in_bytes(head, b'\r\n', start)
    print(head[start:start + len(CONTENT_LENGTH_FIELD)])
    # return len(head) + int(head[start:end].decode())

def find_bytes_in_bytes(bytes, search_bytes, start=0):
    for i in range(start, len(bytes)):
        if bytes[i:i+len(search_bytes)] == search_bytes:
            return i
    print(-1)
    return -1

print(get_content_length_field(test))