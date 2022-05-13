import asyncio
from http import HTTPStatus
from re import I
from tabnanny import check
from urllib import response
from bs4 import BeautifulSoup
import aiohttp
from matplotlib.pyplot import table
from urllib.request import Request, urlopen
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from fake_useragent import UserAgent 
 

class TypeProxy:
    def __init__(self, ip:str, port:str, https:str):
        self.ip = ip
        self.port = int(port)
        self.is_https = https == 'yes'

    def __str__(self):
        return f"{'https' if self.is_https else 'http'}://{self.ip}:{self.port}"

class ProxyHunter:

    sources = ["https://www.socks-proxy.net/", "https://free-proxy-list.net/", "https://www.us-proxy.org/", "https://free-proxy-list.net/uk-proxy.html", "https://www.sslproxies.org/", "https://free-proxy-list.net/anonymous-proxy.html"]
    testurl = 'http://example.com'
    timeout = 4
    ua = UserAgent()
    
    def __init__(self):
        self.getallproxy()    
        
    def getallproxy(self):
        return self.checkproxy(set([prox for proxs in [self.getproxy(url) for url in self.sources] for prox in proxs]))

    def getproxy(self, url):
        proxies_req = Request(url)
        proxies_req.add_header('User-Agent', self.ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        for table in soup.find_all('table'):    
                if 'table-striped' in table['class']:
                    tempt = table.find_all('td')
                    return [ str(TypeProxy(x[0], x[1], x[6])) for x in [ [el.text for el in tempt[i:i+8]] for i in range(0,len(tempt),8)]]    

    async def checkproxyhttp(self, ipport):
        try:
            session = aiohttp.ClientSession()
            await session.get(self.testurl, proxy=ipport, timeout=self.timeout)
            await session.close()
            return ipport
        except:
            await session.close()

    def checkproxy(self,proxy_list):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [asyncio.ensure_future(self.checkproxyhttp(item)) for item in proxy_list]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        return [[i.result()] for i in tasks if i.result()]
        