"""
CIS 433: Computer Network and Security
Project: Cryptocurrency Mining Models
Authors: Danny Lu, Syd Lynch, Charlie Plachno

Description: The file contains code for the server to distribute work over a network
of machines.
"""
import socket
import sys
import threading
import os
import math
from random import choice
from string import ascii_letters

global cond_var
global curr_count
global base
global connections
global initial_work

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
	global initial_work

	initial_work = 100000
	hps = initial_work

	while True:
		print(connections)
		if (cond_var == False):
			cond_var = True
			message = str(curr_count + 1) + '-' + str(curr_count + math.floor((hps/initial_work)*initial_work)) + '-' + '6' + '-' + base
			#Statically allocate a range to clients to compute
			curr_count += math.floor((hps/initial_work)*initial_work)
			print(curr_count)

			print("sent:", message)
			conn.send(message.encode('utf-8'))
			cond_var = False

			#Wait for the client to compute the work and respond with
			#the findings of the specified range
			client_in = str(conn.recv(1024))
			print("received:", client_in, "from:", addr)

			if client_in[2:6] != "done":
				print(">>>" + client_in.split(" ")[0])
				break
			else:
				hps = float(client_in.split(" ")[1][0:-2])
				connections[addr[0]] = hps

	return 0

#Wait for connections, for each new client the server creates a thread
#to communicate with the client.
def main():
	global connections

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
