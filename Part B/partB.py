
import socket as socket1
from socket import *
import re


class server:
    serverPort = 12000
    def __init__(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('',server.serverPort))
        self.serverSocket.listen(1)
        print(f'Server is ready on port: {server.serverPort}')
        self.main()

    def main(self):
        while True:
            self.connectionSocket, address = self.serverSocket.accept()
            websiteURL = ''
            directories = ''
            fileDirectories = ''
            try:
                clientMessage = self.connectionSocket.recv(5000).decode()
                clientMessage = clientMessage.split()
                allPath = clientMessage[1].split("/")
                websiteURL = allPath[1]
                directories = '/'.join(allPath[2:])
                fileDirectories = '_'.join(re.split('[<>:"/\\\|?*]',clientMessage[1]))
                toSend = b''

                #----------------------------------
                # readFile
                with open(fileDirectories, 'rb') as file:
                    bin = file.readline()
                    while bin:
                        toSend += bin
                        bin = file.readline()

                    self.connectionSocket.send(toSend)
                    self.connectionSocket.close()
                #-----------------------------------
            except FileNotFoundError:
                self.fetchData(websiteURL, directories, fileDirectories)
            except IndexError:
                print("")

    def fetchData(self, host, directories, fileDirectories):
        try:
            tempFetchSocket = socket(AF_INET, SOCK_STREAM)
            tempFetchSocket.connect((socket1.gethostbyname(host), 80))
            tempFetchSocket.send(f'GET /{directories} HTTP/1.1\r\nHost:{host}\r\n\r\n'.encode())
            receivedResponse = tempFetchSocket.recv(102400000)
            self.writeFile(receivedResponse, fileDirectories)
            tempFetchSocket.close()
            self.connectionSocket.send(receivedResponse)
        except gaierror:
            print("Cannot locate the IP address of the given URL")
            self.connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
            self.connectionSocket.close()

    def writeFile(self, text, fullUrl):
        with open(fullUrl, 'xb') as file:
            file.write(text)
def main():
    server()

main()



