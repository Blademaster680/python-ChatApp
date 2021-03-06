#!/usr/bin/env python3
"""
Script for Tkinter GUI chat client.
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def recieve():
    """
    Handles recieving messages.
    :return:
    """
    while True:
        try:
            msg = client_socket.recv(BUFFSIZ).decode("utf8") + "\n"
            msg_text.insert(tkinter.END, msg)
            msg_text.see(tkinter.END)
        except OSError:
            break

def send(event=None):
    """
    Handles sending of messages
    :param event:
    :return:
    """
    msg = my_msg.get()
    my_msg.set("") # Clears the input field
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    """
    This function is to be called when the window is closed.
    :param event:
    :return:
    """
    my_msg.set("{quit}")
    send()


# The GUI

top = tkinter.Tk()
top.title("Chatter App by Blademaster680")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() # For the messages to be send.
scrollbar = tkinter.Scrollbar(messages_frame) # To navigate through past messages

msg_text = tkinter.Text(top, height=15, width=50)
msg_text.pack()

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

# If the user closes the app
top.protocol("WM_DELETE_WINDOW", on_closing)


HOST = input('Enter host: ')
PORT = input('Enter Port: ')

if not PORT:
    PORT = 33000 # Default value.
else:
    PORT = int(PORT)

BUFFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


recieve_thread = Thread(target=recieve)
recieve_thread.start()
tkinter.mainloop() # Start GUI execution