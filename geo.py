from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from exceptions import get_exceptions_args
from cradle import Producer
import time
import os
import subprocess
import random

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


def get_judges():
    age = random.randint(18, 55)
    if age in range(18, 25):
        arr = (
            'https://pikabu.ru',
            'https://www.tiktok.com/',
            'https://steamcommunity.com/',
            'https://www.dota2.com/play',
            'https://login.leagueoflegends.com/',
            'https://blizzard.com/'
        )
    elif age in range(25, 35):
        arr = (
            'https://www.instagram.com/',
            'https://www.facebook.com/',
            'https://www.reddit.com/',
            'https://youtube.com/'
        )
    else:
        arr = (
            'https://www.ria.ru/',
            'https://tass.com/',
            'https://www.newsru.com/',
            'https://www.pfrf.ru/',
            'https://www.vesti.ru/',
            'https://live.russia.tv/channel/3?utm_compaign=article',
            'https://vesti.ua/'
        )

    sex = random.choice(['male', 'male', 'male', 'female'])
    history = {
        'female': [
            'тушь для ресниц',
            'помада для губ',
            'тональный крем купить',
            'макияж',
            'свадебное платье',
            'летуаль',
            'рив гош',
            'prada',
            'gucci',
            'versace',
            'barbie',
            'куртка женская',
            'шуба женская',
            'сапоги женские купить в москве'
        ],
        'male': [
            'порно',
            'porn',
            'дота 2',
            'армия 2020',
            'призыв 2021',
            'призывной возраст',
            'отсрочка от армии',
            'военный билет'
            'nvidia geforce gtx 3090',
            'рыболовные блесны купить',
            'пикап форум',
            'как познакомиться с девушкой в интернете',
            'кроссовки мужские',
            'тренировочный костюм мужской недорого',
        ]
    }
    get_request = lambda: random.choice(history[sex])
    get_seq = lambda x: ''.join([str(random.randint(0, 10)) for _ in range(x)])
    get_url = lambda request: f'https://yandex.ru/search/?msid={get_seq(10)}.{get_seq(5)}.{get_seq(5)}.{get_seq(6)}&text={request}&suggest_reqid={get_seq(33)}'

    search_history = [get_request() for _ in range(random.randint(0, 3))]
    search_urls = [get_url(query.replace(' ', '+')) for query in search_history]

    direct_urls = [random.choice(arr) for _ in range(random.randint(0, 3))]

    j = direct_urls + search_urls
    random.shuffle(j)
    j.append('https://www.payqrcode.ru')  # to test if it is possible at least to reach it
    print(f'JUDGES: {j}')
    return j


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

        judges = get_judges()
        proxy = None
        for i in pool:
            p = Producer()
            p.create_user()
            proxy = i.split('//')[-1]
            try:
                p.create_driver(proxy, headless=True)
                any_of_judges = False
                for jj in judges:
                    try:
                        p.driver.get(jj)
                        if p.driver.title:
                            any_of_judges = True
                            print(f'reached judge {jj}')
                            print(p.driver.title)
                            # time.sleep(random.randint(1, 10))
                            continue  # proceed to next judge
                    except Exception as e:
                        if 'ERR_TUNNEL_CONNECTION_FAILED' in str(e):
                            print(f'ERR_TUNNEL_CONNECTION_FAILED with {proxy}')
                            continue  # get new judge
                        elif 'ERR_PROXY_CONNECTION_FAILED' in str(e):
                            print(f'ERR_PROXY_CONNECTION_FAILED {e} with {proxy}')
                            break  # skip all judges, any_of_judges=False
                if any_of_judges:
                    break  # exit loop because reached one of judges, return proxy
                else:
                    print(f'BAD {proxy}; FOR ALL OF JUDGES')
                    continue  # get new proxy and judges
            except Exception as e:
                print(f'BAD {proxy}; {e}')
                try:
                    if p.driver:
                        p.driver.quit()
                except:
                    pass
                proxy = None
                continue  # get new proxy
        if proxy is None:
            continue  # get new proxy pool

        return proxy



        # body = WebDriverWait(p.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
        # if '"ip"' in body.text:
        #     p.driver.get('https://www.payqrcode.ru')
        #     if p.driver.title == 'Payment QR-code generator':
        #         with open(os.path.join(os.getcwd(), 'tested_proxies.txt'), 'a+', encoding="utf-8") as file:
        #             file.write(proxy + '\n')
        #         try:
        #             if p.driver:
        #                 p.driver.quit()
        #         except:
        #             pass
        #         return proxy
        #     else:
        #         print(f'WRONG TITLE {p.driver.title}')
        #         try:
        #             if p.driver:
        #                 p.driver.quit()
        #         except:
        #             continue
        # else:
        #     print(f'WRONG JUDGE {jj}')
        #     try:
        #         if p.driver:
        #             p.driver.quit()
        #     except:
        #         continue
        # # except Exception as e:
        # #     print(f'BAD {proxy}; {e}')
        # #     p.driver.quit()
        # #     continue



if __name__ == '__main__':
    main()