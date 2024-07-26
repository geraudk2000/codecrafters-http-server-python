import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    #
    OK_RESPONSE = "HTTP/1.1 200 OK\r\n\r\n".encode()
    NOTFOUND_RESPONSE = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    #server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n") # wait for client

    client_socket, addr = server_socket.accept()
    with client_socket:
        while True: 
            data = client_socket.recv(1024)
            request_data = data.decode().split("\r\n")
            print(request_data)
            url_path = request_data[0].split(" ")[1]
            print(url_path)
            if url_path == "/":
                client_socket.sendall(OK_RESPONSE)
            elif url_path.startswith("/echo/"):
                string = url_path.strip("/echo/")
                print(string)
                #response =  f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
                client_socket.sendall(response)
            else:
                client_socket.sendall(NOTFOUND_RESPONSE)
            
            
if __name__ == "__main__":
    main()
