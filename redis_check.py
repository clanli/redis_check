#!/usr/bin/python
''' Simple script that swaps master-slave for redis '''

import socket
import redis
import argparse

# hostList = ["appk01", "appk02", "appk03", "appk04", "appk05"]
hostList = ["redisk01", "redisk02"]
port = 6379


class RedConnect(object):

    def __init__(self):
        self.redDict = {}
        for x in hostList:
            self.redDict[x] = {'role': 'dummy', 'state': 'not-running'}

        for host in hostList:
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            location = (host, port)
            result_of_check = a_socket.connect_ex(location)

            if result_of_check == 0:
                self.redDict[host]['state'] = 'running'
            else:
                self.redDict[host]['state'] = 'not-running'
            a_socket.close()

    def checkMasterSlave(self):
        '''Testing which node that is writeable (eg. master) '''

        for key, value in self.redDict.items():
            try:
                pool = redis.ConnectionPool(host=key, port=6379, db=0)
                r = redis.Redis(connection_pool=pool)
                r.delete("msg:hello")
                r.set("msg:hello", "Hello Redis")
                self.redDict[key]['role'] = 'master'
            except:
                self.redDict[key]['role'] = 'slave'

    def swapMasterSlave(self):
        '''Change master-slave role between nodes '''

        for key, value in self.redDict.items():
            if (self.redDict[key]['role'] == 'master'):
                new_slave = key
            if (self.redDict[key]['role'] == 'slave'):
                new_master = key

        for key, value in self.redDict.items():
            if (self.redDict[key]['role'] == 'master'):
                pool = redis.ConnectionPool(host=key, port=6379, db=0)
                r = redis.Redis(connection_pool=pool)
                r.slaveof(host=new_master, port=port)

            if (self.redDict[key]['role'] == 'slave'):
                pool = redis.ConnectionPool(host=key, port=6379, db=0)
                r = redis.Redis(connection_pool=pool)
                r.slaveof('no', 'one')

    def printDict(self):
        '''Prints the dictionary that holds info about master slave '''

        for key, value in self.redDict.items():
            print key, value


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--swap", help="swaps the master slave roles",
                        action="store_true")
    parser.add_argument("-c", "--check", help="check the master slave roles",
                        action="store_true")
    args = parser.parse_args()

    if not (args.swap or args.check):
        print "No action requested, add -s (--swap) or -c (--check) as argument"

    if args.check:
        redobj = RedConnect()
        redobj.checkMasterSlave()
        print "-- Current state"
        redobj.printDict()

    if args.swap:
        redobj = RedConnect()
        redobj.checkMasterSlave()
        print "-- Current state"
        redobj.printDict()
        redobj.swapMasterSlave()
        redobj.checkMasterSlave()
        print "-- New state"
        redobj.printDict()
