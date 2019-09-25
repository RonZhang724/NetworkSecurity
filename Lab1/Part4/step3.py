import socket 

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("www.baiwanzhan.com", 80))
    q1 = b"GET /service/site/search.aspx?query=%E6%B3%95"
    q2 = b"%E8%BD%AE HTTP/1.1"
    s.send(q1)
    s.send(q2)
    response = s.recv(1024)
    print(response)
    s.close()

main()

