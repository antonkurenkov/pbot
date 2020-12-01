from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import pyderman as dr

from src.cradle import Producer
import time
import requests
#
#
# resp = requests.get('http://118.24.52.95/get_all').json()
# print(resp)
#
# for i in resp:
#     p = Producer()
#     p.create_user()
#     p.create_driver()
#     proxy = i['proxy']
#     if proxy:
#         webdriver.DesiredCapabilities.CHROME['proxy'] = {
#             "httpProxy": proxy,
#             # "ftpProxy": proxy,
#             "sslProxy": proxy,
#             "proxyType": "MANUAL",
#         }
#     try:
#         # p.driver.get('https://api.ipify.org?format=json')
#         p.driver.get('https://www.payqrcode.ru')
#         body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
#         # print(body.text)
#         if p.driver.title == 'Payment QR-code generator':
#             print(f'GOOD {proxy}')
#     except:
#         print(f'BAD {proxy}')
#     p.driver.quit()
#
# # p = Producer()
# # p.create_user()
# # p.create_driver()
# # # required_block, optional_block = p.produce_data()
# # p.driver.get('https://api.ipify.org?format=json')
# # body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
# # print(body.text)
# # # time.sleep(10000)
# # p.driver.quit()

#
# import asyncio
# from urllib.parse import urlparse
#
# import aiohttp
#
# from proxybroker import Broker, ProxyPool
# from proxybroker.errors import NoProxyError
#
#
# async def get_pages(urls, proxy_pool, timeout=10, loop=None):
#     tasks = [fetch(url, proxy_pool, timeout, loop) for url in urls]
#     for task in asyncio.as_completed(tasks):
#         url, content = await task
#         print('Done! url: %s; content: %.30s' % (url, content))
#
#
# async def fetch(url, proxy_pool, timeout, loop):
#     resp, proxy = None, None
#     try:
#         proxy = await proxy_pool.get(scheme=urlparse(url).scheme)
#         proxy_url = 'http://%s:%d' % (proxy.host, proxy.port)
#         with aiohttp.Timeout(timeout, loop=loop):
#             async with aiohttp.ClientSession(loop=loop) as session:
#                 async with session.get(url, proxy=proxy_url) as response:
#                     resp = await response.read()
#     except (aiohttp.errors.ClientOSError, aiohttp.errors.ClientResponseError,
#             aiohttp.errors.ServerDisconnectedError, asyncio.TimeoutError,
#             NoProxyError) as e:
#         print('Error. url: %s; error: %r', url, e)
#     finally:
#         if proxy:
#             proxy_pool.put(proxy)
#             # proceed(proxy)
#         return (url, resp)
#
#
# def proceed(proxy):
#
#     p = Producer()
#     p.create_user()
#     proxy = '%s:%d' % (proxy.host, proxy.port)
#     p.create_driver(proxy=proxy)
#     try:
#         p.driver.get('https://api.ipify.org?format=json')
#         # p.driver.get('https://www.payqrcode.ru')
#         time.sleep(10)
#         body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
#         # print(body.text)
#         print(f' {str(proxy)}')
#         if p.driver.title == 'Payment QR-code generator':
#             print(f'GOOD {proxy}')
#     except:
#         print(f'BAD {proxy}')
#     p.driver.quit()
#
#
# def main():
#     loop = asyncio.get_event_loop()
#
#     proxies = asyncio.Queue(loop=loop)
#     proxy_pool = ProxyPool(proxies)
#
#     judges = ['http://httpbin.org/get?show_env',
#               'https://httpbin.org/get?show_env']
#
#     providers = [
#         'http://www.proxylists.net/',
#         'http://fineproxy.org/eng/fresh-proxies/',
#         'http://118.24.52.95/get_all/'
#     ]
#
#     broker = Broker(
#         proxies, timeout=8, max_conn=1000, max_tries=3, verify_ssl=False,
#         judges=judges, providers=providers, loop=loop)
#
#     types = [
#         ('HTTP', (
#             'Anonymous', 'High', 'Transparent')),
#         # ('HTTPS'),
#         # ('SOCKS4'),
#         # ('SOCKS5'),
#         # ('CONNECT:80'),
#         # ('CONNECT:25')
#     ]
#     countries = ['US', 'DE', 'FR']
#
#     urls = [
#         # 'http://www.payqrcode.ru'
#         'https://api.ipify.org?format=json'
#         # 'http://httpbin.org/get', 'http://httpbin.org/redirect/1',
#         # 'http://httpbin.org/anything', 'http://httpbin.org/status/404'
#         ]
#
#     tasks = asyncio.gather(
#         broker.find(types=types, countries=countries, strict=True, limit=10),
#         get_pages(urls, proxy_pool, loop=loop))
#     loop.run_until_complete(tasks)
#
#     # broker.show_stats(verbose=True)
#
#
# if __name__ == '__main__':
#     main()

# """Run a local proxy server that distributes
#    incoming requests to external proxies."""

# import asyncio
# import aiohttp
#
# from proxybroker import Broker
#
#
# async def get_pages(urls, proxy_url):
#     tasks = [fetch(url, proxy_url) for url in urls]
#     for task in asyncio.as_completed(tasks):
#         url, content = await task
#         print('Gotcha! url: %s; content: %.100s;' % (url, content))
        # p = Producer()
        # p.create_user()
        # p.create_driver(proxy='127.0.0.1:8888')
        # # p.create_driver(proxy=valid_proxy)
        # try:
        #     p.driver.get('https://api.ipify.org?format=json')
        #     # p.driver.get('https://www.payqrcode.ru')
        #     time.sleep(10)
        #     body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
        #     if p.driver.title == 'Payment QR-code generator':
        #         print(f'GOOD {valid_proxy}')
        # except:
        #     print(f'BAD {valid_proxy}')
        # p.driver.quit()


# async def fetch(url, proxy_url):
#     resp = None
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, proxy=proxy_url) as response:
#                 resp = await response.read()
#     except (aiohttp.errors.ClientOSError, aiohttp.errors.ClientResponseError,
#             aiohttp.errors.ServerDisconnectedError) as e:
#         print('Error. url: %s; error: %r' % (url, e))
#     finally:
#         if resp:
#             return (url, resp)
#
#
#
#
# def main():
#     host, port = '127.0.0.1', 8888  # by default
#
#     loop = asyncio.get_event_loop()
#
#     types = [('HTTP', 'High'), 'HTTPS', 'CONNECT:80']
#     codes = [200, 301, 302]
#
#     broker = Broker(max_tries=1, loop=loop)
#
#     # Broker.serve() also supports all arguments that are accepted
#     # Broker.find() method: data, countries, post, strict, dnsbl.
#     broker.serve(host=host, port=port, types=types, limit=10, max_tries=3,
#                  prefer_connect=True, min_req_proxy=5, max_error_rate=0.5,
#                  max_resp_time=8, http_allowed_codes=codes, backlog=100)
#
#     urls = [
#         'https://api.ipify.org?format=json',
#         # 'http://httpbin.org/get',
#         # 'https://httpbin.org/get',
#         # 'http://httpbin.org/redirect/1',
#         # 'http://httpbin.org/status/404',
#     ]
#
#     proxy_url = 'http://%s:%d' % (host, port)
#     loop.run_until_complete(get_pages(urls, proxy_url))
#
#     broker.stop()
#
#
# if __name__ == '__main__':
#     main()


"""Find 10 working HTTP(S) proxies and save them to a file."""

import random
import asyncio
from proxybroker import Broker


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
            f.write(row)

def main():

    while True:
        try:
            proxies = asyncio.Queue()
            broker = Broker(proxies)
            tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=10),
                                   save(proxies, filename='../proxies.txt'))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(tasks)

            with open('../proxies.txt') as file:
                pool = file.read().split()
            for i in pool:
                p = Producer()
                p.create_user()
                proxy = i.split('//')[-1]
                p.create_driver(proxy, headless=True)

                try:
                    p.driver.get('https://api.ipify.org?format=json')
                    time.sleep(1)
                    body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
                    if '"ip"' in body.text:
                        p.driver.get('https://www.payqrcode.ru')
                        if p.driver.title == 'Payment QR-code generator':
                            with open('../tested_proxies.txt', 'a+') as file:
                                file.write(proxy + '\n')
                            p.driver.quit()
                            return proxy
                except Exception as e:
                    print(f'BAD {proxy}')
                    p.driver.quit()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    main()