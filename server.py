"""
CIS 433: Computer Network and Security
Project: Cryptocurrency Mining Models
Authors: Danny Lu, Syd Lynch, Charlie Plachno

Description: The file contains code for the server to distribute work over a network
of machines.

    Example:
        Let our server only have one client connected

    Server:
        Sends "0-1000-3-Hello World" to client and waits for a response

    Client:
        Receives "0-1000-3-Hello World", passes the message into decodeMess function.
        The values for the range, target and base string are extracted and are passed
        into proof_of_work to compute the hashes with the specified range.
        Once the client is done, they will notify the Server if the wanted hash was
        found or not. If not, the server will allocate more work to compute.
"""
import socket
import sys
import threading
import os
from random import choice
from string import ascii_letters
from timeit import default_timer as timer

global cond_var
global curr_count
global base
global connections

curr_count = -1
base = "Hello World!"
#True = locked, False = unlocked
cond_var = False
connections = {}


def randString(length):
	return(''.join(choice(ascii_letters) for i in range(length)))

#Send a range of work to clients
#Example of range: "1-1000"(Add each number in this range at the end of the base string
#to compute a new hash, keep doing this until the desired hash is found.)
def send_work(conn, addr):
    global curr_count
    global base
    global cond_var
    global connections

    start = timer()
    duration = 0
    while True:
        print(connections)
        duration = timer() - start
        print(duration)
        if duration > 60:
            print(curr_count)
            break
        if (cond_var == False):
            cond_var = True
            message = str(curr_count + 1) + '-' + str(curr_count + 1000000) + '-' + '10' + '-' + base
            #Statically allocate a range to clients to compute
            curr_count += 1000000
            print(curr_count)

            print("sent:", message)
            conn.send(message.encode('utf-8'))
            cond_var = False

            #Wait for the client to compute the work and respond with
            #the findings of the specified range
            client_in = str(conn.recv(1024))
            print("received:", client_in, "from:", addr)

            if client_in[2:6] != "done":
                found = client_in.split(" ")[0]
                print(">>>" + found)
                return found
            else:
                hps = client_in.split(" ")[1]
                connections[addr[0]] = hps

    return 0

#Wait for connections, for each new client the server creates a thread
#to communicate with the client.
def main():
    global connections
    global counter

    soc = socket.socket()
    host = "0.0.0.0"
    port = 6500
    soc.bind((host,port))

    thread_list = []
    soc.listen()
    input("Press enter to distribute work to all connected clients.")

    while True:
        connection, address = soc.accept()

        print(address, "connected to server")

        thread = threading.Thread(target = send_work, args = (connection, address))
        thread_list.append(thread)
        thread.start()



main()
