import aiohttp
import asyncio
import re
from key import API_KEY

async def scrape_places(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            #print("Status:", response.status)
            if response.status != 200:
                print ("BAD REQUEST")
            #print("Content-type:", response.headers['content-type'])

            html = await response.text()
            return html

def parse_loc(loc):
    coords = re.findall( "([+-]\d+(?:\.\d+)?)", loc)
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
        #print ("Latitude: %s, Longitude: %s" %(coords[0], coords[1]))
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
    return (coords, r, b)

def construct_url(loc, r, b):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
    url += loc[0] + "," + loc[1] + "&radius=" + str(r) + "&key=" + API_KEY
    return url

async def get_places_data(loc, r, b):
    url = construct_url(loc, r, b)
    #print (url)
    data = await scrape_places(url)
    return data

async def main():
    locs = "-34+117.23049"

    loc, r, b = query_user()
    data = await get_places_data(loc, r, b)
    print (data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

