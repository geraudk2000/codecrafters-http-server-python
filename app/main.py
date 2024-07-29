import socket
import threading
import argparse
import os

OK_RESPONSE = "HTTP/1.1 200 OK\r\n\r\n".encode()
NOTFOUND_RESPONSE = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

def parse_request(resquest_data): 

    lines = resquest_data.split('\r\n')
    start_line = lines[0]
    method, path, version = start_line.split(" ")
    return method, path, version


def handle_request(client_socket, client_address, directory):
    
    with client_socket: 
        data = client_socket.recv(1024)
        response = NOTFOUND_RESPONSE
        #print(data)
        method, path, version = parse_request(data.decode())
        #print(method, path, version) 
        print(path)
        if path == "/": 
            response = OK_RESPONSE
            #client_socket.sendall(response)
        elif path.startswith("/echo/"):
            string = path.lstrip("/echo/")
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            #client_socket.sendall(response)
        elif path.startswith("/user-agent"):
            string = data.decode().split(":")[-1].lstrip(" ").rstrip("\r\n\r\n")
            #print(string)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            #print(response)
            #client_socket.sendall(response)    
        elif path.startswith("/files/"):
            file_name = path.split("/")[-1]
            #print(file_name)
            file_path = os.path.join(directory, file_name)
            #print(file_path)
            try:         
                with open(file_path, "r", encoding='utf-8') as file: 
                    string = file.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            except FileNotFoundError:
                response = NOTFOUND_RESPONSE

        else:
            response = NOTFOUND_RESPONSE
            #client_socket.sendall(NOTFOUND_RESPONSE)
        client_socket.sendall(response)
    


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    #
    parser = argparse.ArgumentParser(description="folder for HTTP Server")
    parser.add_argument("--directory")
    arguments = parser.parse_args()
    folder = arguments.directory
    print("this is folder ->" + folder)
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:    
        client_socket, client_addr = server_socket.accept()
        threading.Thread(target=handle_request, args = (client_socket, client_addr, folder)).start()

    
    
            
if __name__ == "__main__":
    main()
