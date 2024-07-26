import socket
import re

OK_RESPONSE = "HTTP/1.1 200 OK\r\n\r\n".encode()
NOTFOUND_RESPONSE = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

def parse_request(resquest_data): 

    lines = resquest_data.split('\r\n')
    start_line = lines[0]
    method, path, version = start_line.split(" ")
    return method, path, version


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    #

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_addr = server_socket.accept()
    
    with client_socket:
        
        data = client_socket.recv(1024)
        method, path, version = parse_request(data.decode())
        print(path)
        if path == "/": 
            client_socket.sendall(OK_RESPONSE)
        elif path.startswith("/echo/"):
            string = path.lstrip("/echo/")
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
        
            print(response)
            client_socket.sendall(response)
                
        else:
            client_socket.sendall(NOTFOUND_RESPONSE)
            
            
if __name__ == "__main__":
    main()
