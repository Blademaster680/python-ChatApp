#!/usr/bin/env python3
"""
Server for multithreaded (asynchronous) chat application.
"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system


system("title Chatter Server by Blademaster680")


def accept_incoming_connections():
    """
    Sets up handling for incoming clients.
    """
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings!\n"+
                          "Please type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    """
    Handles a single client connection.
    :param client: Takes the client socket as the argument.
    :return:
    """
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s!' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            print("We are in the else!")
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % client, "utf8"))
            print("%s has disconnected" % client)
            break


def broadcast(msg, prefix=""):
    """
    Broadcasts a message to all the clients
    :param msg:
    :param prefix:
    :return:
    """
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for a connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
