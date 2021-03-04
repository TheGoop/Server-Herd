# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



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





def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
