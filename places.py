import aiohttp
import asyncio
import re
from key import API_KEY

async def get_place_info(loc, r, bound):

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print (html)
            print("Body:", html[:15], "...")

def parse_loc(loc):
    coords = re.findall( "([+-]\d+(?:\.\d+)?)", loc)
    print (coords)
    if len(coords) != 2:
        raise ValueError("Invalid location string")
    try:
        lat, long = float(coords[0]), float(coords[1])
    except:
        raise ValueError("Invalid lat/longs given - NaN")

    return coords

def query_user():
    loc = input("Enter latitude,longitude location string: ")
    r = input("Enter radius (km): ")
    b = input("Enter information upper bound: ")
    try:
        coords = parse_loc(loc)
        print ("Latitude: %s, Longitude: %s" %(coords[0], coords[1]))
    except ValueError as err:
        print (err.args[0])
        exit(1)

    try:
        r = float(r)
    except:
        print("Invalid radius")
        exit(1)

    try:
        if "." in b:
            raise ValueError
        b = int(b)
        if b > 20 or b < 0:
            raise ValueError
    except:
        print("Invalid information upper bound value")
        exit(1)



async def main():
    locs = "-34+117.23049"
    print ()
    query_user()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print (API_KEY)
