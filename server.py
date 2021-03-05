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

class HTTP_Protocol(asyncio.Protocol):
    def __init__(self):
        pass

    def openSession(self):
        pass

    def closeSession(self):
        pass

class ClientServer_Protocol(asyncio.Protocol):
    def __init__(self):
        pass

class ServerServer_Protocol(asyncio.Protocol):
    def __init__(self):
        pass

async def main():
    print (sys.argv)
    pass

if __name__ == '__main__':
    asyncio.run(main())