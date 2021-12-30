from socket import *
import os

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("The server is ready!")
while True:
    connectionSocket, address = serverSocket.accept()
    # sentence = connectionSocket.recv(2048).decode()
    # capitalizedSentence = sentence.upper()
    # print(capitalizedSentence.encode())
    # connectionSocket.send(capitalizedSentence.encode())
    try:
        message = connectionSocket.recv(5000).decode()  # Fill in code to read GET request
        file = message.split()[1]
        filename = file[1:]
        filelocation = os.getcwd() + "\\" + filename
        print(filelocation)
        # Fill in security code
        f = open(filelocation, "rb")
        outputdata = f.read()
        connectionSocket.send('\nHTTP/1.1 200 OK\n\n'.encode())

        connectionSocket.send(outputdata)
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
        connectionSocket.close()
    except IndexError:
        print("IndexError")