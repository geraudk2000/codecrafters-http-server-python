import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    #server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n") # wait for client

    conn, addr = server_socket.accept()
    with conn:
        while True: 
            data = conn.recv(1024)
            request_data = data.decode().split("\r\n")
            response = b"HTTP/1.1 200 OK\r\n\r\n"
            if not data:
                break
            #conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            if request_data[0].split(" ")[1] != "/":
                response =  b"HTTP/1.1 404 Not Found\r\n\r\n"
            conn.sendall(response)


if __name__ == "__main__":
    main()
