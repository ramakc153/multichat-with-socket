import socket
import time
from threading import Thread
import sys

sock = socket.socket()

def connecting():
    try:
        tujuan = input("Masukkan IP tujuan : ")
        port = int(input("Masukkan port : "))
        sock.connect((tujuan,port))
        print("Socket Terhubung")
        user = input("Masuk Sebagai : ")
        sock.sendall((user).encode())
    except:
        print("\n IP / PORT Salah. Silahkan cek kembali IP/PORT tujuan anda.")
        time.sleep(1)
        return "Error"

def send():
    while True:
        try:
            message = input("")
            sock.sendall((message).encode())
        except socket.error as err:
            print("Socket error : ", str(err))
            sock.close()
            sys.exit()

def recv():
    while True:
        try:
            time.sleep(0.3)
            enc = sock.recv(1024).decode()
            print(enc)
        except socket.timeout:
            pass

if __name__ == "__main__":
    try:
        if connecting() == 'Error':
            print("Error occured in program")
            print("Program will close...")
            sys.exit()
        
        else:
            threadsend = Thread(target=send, args = ())
            threadrecv = Thread(target=recv, args = ())
            threadsend.start()
            threadrecv.start()
        
    except:
        print("Exit.")
        threadrecv.join()
        threadsend.join()
        sock.close()
        sys.exit()


