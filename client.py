import socket
import threading
from queue import Queue
 
host = '192.168.100.15'
port = int(input("Masukkan Port : "))
grup = input("Input nama group chat : ")
 
s = None
 
max_user = 5
 
user = {}
 
#untuk membuat socket
 
def buat_socket():
    try:
        global s
        s = socket.socket()
    except socket.error as err:
        print("socket error : ", str(err))
 
#bind socket
def bind_socket():
    try:
        global host
        global port
        global s
        s.bind((host,port))
        s.listen(max_user)
        print("Socket telah dibuat")
    except socket.error as err:
        print("Socket error : "+ str(err) + "menghubungkan ulang...")
        bind_socket()
 
#menerima user baru
def terima():
    global s
    while True:
        try:
            conn, add = s.accept() 
            s.setblocking(1)  #untuk mencegah timeout
 
            t = threading.Thread(target = pesan, args = [conn, add])
            t.daemon = True
            t.start()
 
            print("User masuk dari IP : " + str(add[0]) + " dari port : " + str(add[1]))
 
        except socket.error as err:
            print("Socket error : ", str(err))
    s.close()
 
 
#menangkap pesan dari client
def pesan(connection, address):
    name = None
    while not name:
        name = connection.recv(1024).decode()
        if not name:
            connection.sendall(("Masukkan nama : ").encode())
        else:
            user[address[1]] = [name , connection]
            break
 
    connection.sendall((f"Selamat datang di Server {user[address[1]][0]}!").encode())
    connection.sendall((f"Anda masuk di group chat : {grup}").encode())
 
    sebar(address, "Masuk ke Group Chat")
 
 
 
    while True:
        msg = connection.recv(1024).decode()
        print(msg)
        sebar(address, msg)
        if msg == 'exit':
            del user[address[1]]
            break
 
    connection.close()
 
 
#menyebarkan pesan ke semua user
def sebar(address, msg):
    for x in user:
        try:
            if msg == 'exit':
                if x == address[1]:
                    user[x][1].sendall((msg).encode())
                else:
                    user[x][1].sendall((f"{user[address[1]][0]} keluar dari group chat").encode())
 
            else:
                if x!= address[1]:
                    user[x][1].sendall((f"{user[address[1]][0]} : {msg}").encode())
 
        except socket.error as err:
            print("Socket Error : ", str(err))
 
buat_socket()
bind_socket()
terima()
