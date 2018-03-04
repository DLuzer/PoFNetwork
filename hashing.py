import hashlib
import socket
import sys
from timeit import default_timer as timer

def proof_of_work(source, dest, target, base_str):
    #used to add to the end of the string to compute a different hash
    counter = source
    #stiring for hashing
    string = base_str
    work = str(hashlib.sha256(string.encode("utf-8")).hexdigest())
    while(check_hash(work,target) == False):
        if counter == dest:
            return "done"
        counter += 1
        work = str(hashlib.sha256((string+str(counter)).encode("utf-8")).hexdigest())
        #prints all the predicted hashes
        #print(work)

    #prints the counter and how many iterations to get to the desired hash
    print("found:" + str(counter))
    return counter

def check_hash(hashcode, target):
    zeros = 0
    check_index = 0
    for index in range(len(hashcode)):
        if (hashcode[index] == "0") and (index == check_index):
            zeros += 1
            check_index += 1
        elif (zeros == target):
            return True
        else:
            return False
    return False

def decodeMess(message):
    split_mess = message.split('-')
    start_hash = int(split_mess[0])
    end_hash = int(split_mess[1])
    target = int(split_mess[2])
    base_str = split_mess[3]

    return start_hash, end_hash, target, base_str

def main():
    soc = socket.socket()
    host = socket.gethostname()
    #host = "10.111.194.128"
    port = 6500

    soc.connect((host, port))
    while True:
        raw_in = str(soc.recv(1024))
        server_in = raw_in[2:len(raw_in)-1]

        start, end, tar, base = decodeMess(server_in)
        start_time = timer()
        answer = proof_of_work(start, end, tar, base)
        duration = timer() - start_time
        if answer == "done":
            print("Didn't get the hash")
            print("Duration =", duration)
            print("Hashes computed per second =", (end-start)/duration)
            hash_per_second = (end-start)/duration
        else:
            hash_per_second = (answer - start)/duration
            print(answer)
        answer += " " + str(hash_per_second)

        answer = answer.encode('utf-8')
        soc.sendto(answer,(host,port))

main()
