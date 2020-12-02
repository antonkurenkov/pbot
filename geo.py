from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from exceptions import get_exceptions_args
from cradle import Producer
import time
import os
import subprocess

import asyncio
from proxybroker import Broker


async def save(proxies, filename):
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
        except RuntimeError:
            print(f'runtime error, exiting')
            processes = subprocess.getoutput(['pgrep chrome'])
            if processes:
                killed = subprocess.getoutput(f'sudo kill -9 {processes}'.split())
                processes = processes.replace('\n', ' ')
                print(f'killed {processes}')
            exit(1)
        except Exception as e:
            print(f'error in {get_exceptions_args()}, proxy=None')
            break

        with open(os.path.join(os.getcwd(), 'proxies.txt'), encoding="utf-8") as file:
            pool = file.read().split()

        judge = 'https://api.ipify.org?format=json'
        proxy = None
        for i in pool:
            p = Producer()
            p.create_user()
            proxy = i.split('//')[-1]
            try:
                p.create_driver(proxy, headless=True)
                p.driver.get(judge)
                break
            except Exception as e:
                print(f'BAD {proxy}; {e}')
                try:
                    if p.driver:
                        p.driver.quit()
                except:
                    pass
                proxy = None
                continue
        if proxy is None:
            continue

        time.sleep(1)
        body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
        if '"ip"' in body.text:
            p.driver.get('https://www.payqrcode.ru')
            if p.driver.title == 'Payment QR-code generator':
                with open(os.path.join(os.getcwd(), 'tested_proxies.txt'), 'a+', encoding="utf-8") as file:
                    file.write(proxy + '\n')
                try:
                    if p.driver:
                        p.driver.quit()
                except:
                    pass
                return proxy
            else:
                print(f'WRONG TITLE {p.driver.title}')
                try:
                    if p.driver:
                        p.driver.quit()
                except:
                    continue
        else:
            print(f'WRONG JUDGE {judge}')
            try:
                if p.driver:
                    p.driver.quit()
            except:
                continue
        # except Exception as e:
        #     print(f'BAD {proxy}; {e}')
        #     p.driver.quit()
        #     continue



if __name__ == '__main__':
    main()