import asyncio
import time
import csv
import numpy as np
import aiohttp
from aiohttp.client import ClientSession

res = [[0]*21 for i in range(3)]

def main():
    print('springboot httpclient sync')
    test_url("http://192.168.0.59:8080/springboot-httpclient-test",0)

    print('springboot httpclient async')
    test_url("http://192.168.0.59:8080/springboot-httpclient-async-test",1)

    print('webflux webclient')
    test_url("http://192.168.0.59:8082/webflux-webclient-test",2)

    print(res)
    header=['a1','a2','a3','a4','a5','a6','a7','b1','b2','b3','b4','b5','b6','b7','c1','c2','c3','c4','c5','c6','c7']

    with open("response_times.csv","w+") as my_csv:
       csvWriter = csv.writer(my_csv,delimiter=',')
       csvWriter.writerow(header)
       csvWriter.writerows(res)

async def download_link(url:str,session:ClientSession):
    async with session.get(url) as response:
        result = await response.text()
#        print(f'Read {len(result)} from {url}')

async def download_all(urls:list):
    my_conn = aiohttp.TCPConnector(limit=10000)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_link(url=url,session=session))
            tasks.append(task)
        await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session

def run_test(url:str,delay:int,lim:int,axis:int,index:int):
    url=url+'?delay='+str(delay)
    url_list = [url]*lim
    start = time.time()
    asyncio.run(download_all(url_list))
    end = time.time()
    print(f'download {len(url_list)} links with {delay} backend delay in {end - start} seconds')
    res[axis][index]=end-start

def test_url(url:str, axis:int):
   conc_users=[100,200,400,800,2000,4000,8000]
   delays=[100,500,2000]
   i=0
   for delay in delays:
      for users in conc_users:
        run_test(url,delay,users,axis,i)
        i+=1

if __name__ == "__main__":
    main()


