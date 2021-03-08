# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession
from message import MessageExtractor, IAMAT, WHATSAT
import time
from places import get_places_data

'''
Commands:
    IAMAT - server saves location and propagates it among the herd
    WHATSAT - server calls google places api to check what is near
            given client and sends result back to caller

Communication:
Client-Server Communication: WHATSAT
    Clients can ask what is near one of the clients
    <Command> <Client-Name> <Radius> <Number of Results>
    WHATSAT kiwi.cs.ucla.edu 10 5

    Query Google Places API, preserve JSON format but remove duplicate newlines

Request to server:
    <Name-Of-Command> <Client-ID> <+-><lat><+-><long> <POSIX-timestamp>
    IAMAT kiwi.cs.ucla.edu +34.06-118.445 15203002039.01239813

Response from server:
    <Name-Of-Response> <Server-Name> <TimeStamp-Diff> <Client-ID> <+-><lat><+-><long> <POSIX-timestamp>
    AT Hill +0.230942 kiwi.cs.ucla.edu +34.06-118.445 15203002039.01239813

Must handle invalid messages:
    - messages can contain any number of newlines/spaces between words
        - can wait for EOF by using reader.read()
    - "WHATSAT kiwi (missing parts)"
    - respond with "? <recieved message>"
        - "? WHATSAT kiwi"

Testing:
    - use telnet or nc (netcat)
    - telnet <server-name> <port-num>
        - telnet ucla.edu 80 (usually use 80
'''

'''

asyncio.run(), introduced in Python 3.7, is responsible for getting the event loop, 
running tasks until they are marked as complete, and then closing the event loop.

There’s a more long-winded way of managing the asyncio event loop, with get_event_loop(). 
The typical pattern looks like this:

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()

however asyncio.run() should suffice

'''



servers = ['Riley', 'Jaquez', 'Juzang', 'Campbell', 'Bernard']
ports = [15240, 15241, 15242, 15243, 15244]
host = '127.0.0.1'
serverToPorts = dict()
for i in zip(servers, ports):
    serverToPorts[i[0]] = i[1]

_neighbors = dict()
_neighbors["Riley"] = ["Jaquez", "Juzang"]
_neighbors["Juzang"] = ["Campbell"]
_neighbors["Bernard"] = ['Jaquez', 'Juzang', 'Campbell', 'Bernard']
_neighbors["Jaquez"] = ["Riley", "Bernard"] #bidrectional
_neighbors["Campbell"] = ["Juzang", "Bernard"] #bidrectional



class Server:
    def __init__(self, name, neighbors, port):
        self.name = name
        self.neighbors = neighbors
        self.port = port
        self.lat = None
        self.long = None
        self.timestamp = float("-inf")

    def connection_made(self, transport):
        self.transport = transport
    def data_received(self, data):
        self.transport.write(data)

    def handle_IAMAT(self, data):
        if data["type"] != IAMAT:
            raise ValueError("Incorrect type of data to update server")

        if data["timestamp"] > self.timestamp:
            self.lat = data["lat"]
            self.long = data["long"]
            self.timestamp = data["timestamp"]

    def response_IAMAT(self, data):
        if "type" not in data or data["type"] != IAMAT:
            raise ValueError("Incorrect data for response")

        s = "AT " + self.name + " "
        try:
            time_diff = time.time() - float(data["timestamp"])
        except:
            print ("Some error with subtracting times")
            exit(1)
        if time_diff > 0:
            s += "+"
        s += time_diff + " " + data["id"] + " " + data["lat"] + data["long"] + " " + str(data["timestamp"])

        return s

    async def response_WHATSAT(self, data):
        if "type" not in data or data["type"] != WHATSAT:
            raise ValueError("Incorrect data for response")

        t = time.time() - data["timestamp"]
        s = "AT " + name + " "
        if t >= 0:
            s += "+"
        s += str(t)
        s += data["id"] + " "
        s += self.lat
        s += self.long
        s += " " + data["timestamp"] + "\n"

        place_data = await get_places_data(self.lat+self.long, data["radius"], data["bound"])
        s += place_data
        return s


    async def handle_client(self, reader, writer):
        data = await reader.read()
        msg = data.decode()

        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (msg, addr))

        parsed = MessageExtractor(msg)
        is_bad = parsed.load_info()

        #if we are given that the msg is bad, we return that is_bad message
        if is_bad:
            pass

        if parsed.type == IAMAT:
            self.handle_IAMAT(parsed.get_data())
            response = self.response_IAMAT(parsed.get_data())

        elif parsed.type == WHATSAT:
            response = self.response_WHATSAT(parsed.get_data())
        pass



async def main():
    if (not sys.argv or len(sys.argv) != 2):
        print("ERR - INCORRECT NUMBER OF ARGS")
        exit(1)
    name = sys.argv[1]
    if (name not in serverToPorts):
        print ("ERR - INCORRECT SERVER NAME")
        exit(1)

    s = Server(name=name, neighbors=_neighbors[name], port=serverToPorts[name])

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(s.handle_client, '127.0.0.1', s.port, loop=loop)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()



if __name__ == '__main__':
    asyncio.run(main())