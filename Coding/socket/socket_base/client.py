import socket
import pickle

HEADRESIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.67", 1234))


full_msg = b""
new_msg = True
while True:
    msg = s.recv(16)
    if new_msg:
        print(f'new message length :{msg[:HEADRESIZE]}')
        msglen = int(msg[:HEADRESIZE])
        new_msg = False

    full_msg += msg

    if len(full_msg) - HEADRESIZE == msglen:
        print("full msg recvd")
        print(full_msg[HEADRESIZE:])
        d = pickle.loads(full_msg[HEADRESIZE:])
        print(d)
        new_msg = True
        full_msg = b''

print(full_msg)
