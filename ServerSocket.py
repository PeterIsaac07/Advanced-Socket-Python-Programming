import socket
# Server socket that will handle multiple clients, with the support of events
from ClientSocket import ClientSocket


class ServerSocket:
    def __init__(self):
        self.__InnerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__IsListening = False
        self.__Port = None
        self.__Clients = list()

    def GetClients(self):
        return self.__Clients.copy()

    def Listen(self, Port):
        self.__Port = Port
        if self.__IsListening is False:
            try:
                self.__InnerSock.bind(("0.0.0.0", Port))
                self.__InnerSock.listen()
            finally:
                self.__IsListening = True
                print("Server is listening on port: ", self.__Port)
        else:
            print("Server is already listening on port: ", self.__Port)

    def ClientAcceptor(self):
        while self.__IsListening is True:
            ClientSock, ClientAddress = self.__InnerSock.accept()
            Client = ClientSocket(ClientSock, ClientAddress)
            Client.SetHeaderSize(4)  # 4 Bytes
            Client.SetMaximumMessageSize(1024 * 1024 * 5)  # 1 MB
            Client.StartReceiver()
            for i in range(553):
                f = open("images/par_t"+str(i)+".jpg", "rb")
                file = f.read()
                data = bytearray(file)
                Client.Send(data)
                f.close()
            self.__Clients.append(Client)
            print("Client Connected: ", Client.GetAddress())

    def Shutdown(self):
        if self.__IsListening is True:
            for Client in self.__Clients:
                print(Client.GetAddress())  # Disconnect
                Client.Disconnect()
            self.__InnerSock.shutdown(socket.SHUT_RDWR)
            self.__InnerSock.close()


