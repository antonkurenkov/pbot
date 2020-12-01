from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from cradle import Producer
import time
import os

"""Find 10 working HTTP(S) proxies and save them to a file."""

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
                                   save(proxies, filename='proxies.txt'))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(tasks)

            with open(os.path.join(os.getcwd(), 'proxies.txt')) as file:
                pool = file.read().split()
            for i in pool:
                p = Producer()
                p.create_user()
                proxy = i.split('//')[-1]
                try:
                    p.create_driver(proxy, headless=True)
                    p.driver.get('https://api.ipify.org?format=json')
                    time.sleep(1)
                    body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
                    if '"ip"' in body.text:
                        p.driver.get('https://www.payqrcode.ru')
                        if p.driver.title == 'Payment QR-code generator':
                            with open(os.path.join(os.getcwd(), 'tested_proxies.txt'), 'a+') as file:
                                file.write(proxy + '\n')
                            # p.driver.quit()
                            return p.driver, proxy
                except Exception as e:
                    print(f'BAD {proxy}')
                    p.driver.quit()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    main()