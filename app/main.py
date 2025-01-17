import socket
import threading
import sys
import os
import re
import gzip

OK_RESPONSE = "HTTP/1.1 200 OK\r\n\r\n".encode()
NOTFOUND_RESPONSE = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

def parse_request(resquest_data): 

    lines = resquest_data.split('\r\n')
    start_line = lines[0]
    method, path, version = start_line.split(" ")
    return method, path, version


def handle_request(client_socket, client_address):
    
    with client_socket: 
        data = client_socket.recv(1024)
        response = NOTFOUND_RESPONSE
        #print(data)
        method, path, version = parse_request(data.decode())
        #print(method, path, version) 
        encoding = re.search("gzip", data.decode())
        
        data_post = data.decode().split('\n')[-1]
       
        if path == "/": 
            response = OK_RESPONSE
           
        elif path.startswith("/echo/"):
            string = path.split("/")[-1]
                       
            if not encoding:
                encode_string = ""
                compress_body = ""
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            else:
                encode_string = encoding.group(0)
                compress_body = gzip.compress(string.encode())    
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: {encode_string}\r\nContent-Length: {len(compress_body)}\r\n\r\n".encode() + compress_body
            
            
        elif path.startswith("/user-agent"):
            string = data.decode().split(":")[-1].lstrip(" ").rstrip("\r\n\r\n")
            
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            
               
        elif path.startswith("/files/") and method == "GET":
            file_name = path.split("/")[-1]
            directory = sys.argv[2]
            file_path = os.path.join(directory, file_name)
            print(file_path)
            try:         
                with open(file_path, "r", encoding='utf-8') as file: 
                    content = file.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
            except Exception as e:
                response = NOTFOUND_RESPONSE
        elif path.startswith("/files/") and method == "POST":
            print("method is post")
            if path.startswith("/files"): 
                file_name = path.split("/")[-1]
                directory = sys.argv[2]
                file_path = os.path.join(directory, file_name)
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(data_post)
                    response = f"HTTP/1.1 201 Created\r\n\r\n".encode()
                except Exception as e:
                    response = f"file cannot be created".encode()          

        else:
            response = NOTFOUND_RESPONSE
            
        client_socket.sendall(response)

        


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    #
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:    
        client_socket, client_addr = server_socket.accept()
        threading.Thread(target=handle_request, args = (client_socket, client_addr)).start()

                
if __name__ == "__main__":
    main()
