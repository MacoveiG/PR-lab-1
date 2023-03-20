import os
import re
from Socket import get_socket_connection
from urllib.parse import urlparse
import threading


class DownloadImages:
    def __init__(self, host, port, images_links):
        self.host = host
        self.port = port
        self.images_links = images_links
        self.sem = threading.Semaphore(2)

    def download(self):
        while len(self.images_links):
            self.sem.acquire()

            if not len(self.images_links):
                break

            print(f"{threading.current_thread()}")

            link = self.images_links.pop()
            sock = get_socket_connection(self.host, self.port)
            url = urlparse(link)
            request = "GET {} HTTP/1.0\r\nHost: {}\r\n\r\n".format(url.path, self.host)

            sock.sendall(request.encode())
            response = sock.recv(1024)
            headers, image_data = response.split(b"\r\n\r\n", 1)

            content_length_match = re.search(r'content-length:\s*(\d+)', headers.decode().lower())
            content_length = int(content_length_match.group(1))

            while len(image_data) < content_length:
                image_data += sock.recv(1024)

            image_path = "C:/Users/macov/OneDrive/Desktop/img/" + os.path.basename(url.path)
            with open(image_path, "wb") as f:
                f.write(image_data)

            sock.close()
            self.sem.release()

    def multithreading(self):
        t1 = threading.Thread(target=self.download)
        t2 = threading.Thread(target=self.download)
        t3 = threading.Thread(target=self.download)
        t4 = threading.Thread(target=self.download)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
