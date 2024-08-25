import socket

#Define socket host and port
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

#create socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((SERVER_HOST,SERVER_PORT))
server_socket.listen(1)
print("Listening on port:%s......." %SERVER_PORT)


while True:
    #wait for client to connect
    client_connection,client_address = server_socket.accept()

    #get the client request
    request = client_connection.recv(1024).decode()
    print("CLIENT REQUEST:\n"+request)

    #parse HTTP header
    headers = request.split('\n')
    print("HEADER:")
    print(headers)
    if len(headers)>0:
        filename = headers[0].split()[1]
        print("PARSED FILENAME:\n"+filename)
    else:
        filename = '/index.html'
    
    #get the content of file
    if filename == '/' or filename == '/favicon.ico':
        filename = '/index.html'
    
    try:
        fin = open("website"+filename)
        content = fin.read()
        fin.close()
        print("CONTENT OF FILE:\n"+content)
        #send HTTP response
        response = 'HTTP/1.0 200 OK\n\n'+ content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
        
    print("RESPONSE:\n"+response)
    client_connection.sendall(response.encode())
    client_connection.close()

#close socket
server_socket.close()