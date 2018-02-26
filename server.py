import socket
import sys
import threading

global cond_var
global curr_count
global base

curr_count = -1
base = "Hello World!"
#True = locked, False = unlocked
cond_var = False

def send_work(conn, addr):
    global curr_count
    global base
    global cond_var

    while True:
        if (cond_var == False):
            cond_var = True
            message = str(curr_count + 1) + '-' + str(curr_count + 100000) + '-' + '6' + '-' + base
            #print(message)
            curr_count += 100000
            print(curr_count)

            print("sent:", message)
            conn.send(message.encode('utf-8'))
            cond_var = False

            client_in = str(conn.recv(1024))
            print("received:", client_in, "from:", addr)

            if client_in[2:6] != "done":
                print(">>>" + client_in.split(':')[1])
                break

    return 0

def main():
    soc = socket.socket()
    #host = socket.gethostname()
    host = "0.0.0.0"
    port = 6500
    soc.bind((host,port))

    thread_list = []

    soc.listen()
    while True:
        connection, address = soc.accept()

        print(address, "connected to server")

        thread = threading.Thread(target = send_work, args = (connection, address))
        thread_list.append(thread)
        thread.start()

main()
