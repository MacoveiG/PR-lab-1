import re
from Socket import get_socket_connection
from DownloadImages import DownloadImages

pattern = r'<img.*?src=[\'"](.*?\.(?:jpg|png|gif))[\'"].*?>'

n = int(input('Alegeti:\n   1) me.utm.md\n   2) utm.md\n>> '))

if n == 1:
    scheme, host, port = 'http', 'me.utm.md', 80
else:
    scheme, host, port = 'https', 'utm.md', 443

sock = get_socket_connection(host, port)

request = 'GET / HTTP/1.0'\
                '\r\nHOST: {}' \
                '\r\nAccept: text/html' \
                '\r\nAccept-Language: ro,en' \
                '\r\nAllow: GET' \
                '\r\nDNT: 1' \
                '\r\nSave-Data: on\r\n\r\n'.format(host)

sock.sendall(request.encode())

source = b''
while True:
    data = sock.recv(2048)
    if not data:
        break
    source += data

sock.close()

source = source.decode()

_images_links_ = re.findall(pattern, source)
images_links = []
for link in _images_links_:
    if scheme not in link:
        link = f"{scheme}://{host}/{link}"
    images_links.append(link)

DownloadImages(host, port, images_links).multithreading()