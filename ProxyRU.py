import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pyderman as ddd


class ProxyRU:

    @staticmethod
    def get_proxy():

        with open(os.path.join(os.getcwd(), 'proxies.txt'), encoding="utf-8") as file:
            pool = file.read().split()
        random.shuffle(pool)
        os.remove(os.path.join(os.getcwd(), 'proxies.txt'))

        for p in pool:
            # proxies = {
            #     "http": p,
            #     "https": p,
            # }
            try:
                path = ddd.install(browser=ddd.chrome, file_directory='src/lib/', verbose=True, chmod=True,
                                   overwrite=False,
                                   version=None, filename=None, return_info=False)
                options = Options()
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    "httpProxy": p,
                    "ftpProxy": p,
                    "sslProxy": p,
                    "proxyType": "MANUAL",
                }
                options.headless = False
                options.add_argument('--start-maximized')
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                dr = webdriver.Chrome(executable_path=path, options=options)

                dr.get(
                    'https://www.payqrcode.ru/?&Ffbclid=DIwAR2ofk1GPgjyscpitWKkIBdY_7i6KE6V0ybX3DpY3GTh0qG9t3Bwkfjn3jw')
                (
                            '&h=AT3Vv6So3ncpmvMOwc4HHyb2WAh7kYRovYWt8qvdQKStFDd4oF-LQFWWAUaFHZhEU3GtKv8wOURioVlFhs4j_kW6sfvRW1xfaTtiTnS5HIIRZQPSUmF18YoqflxG2wNtv1-NXBHMAw' +
                            '&__tn__=-UK-R' +
                            '&c[0]=AT22LLR7aEYoGYL-IlqGhRKfpGGKtR86lyqhhZ8o9C1II0YLuf2XYW0mOH685hUFXPlnWINKjB2axV4xCvxG8iFzN6_Bi5ETzuZUDuXvNPos1Oz6r9UFszylAItm9-L0zp0E')
                raw_html = WebDriverWait(dr, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//body'))).text

                if dr.title == 'Payment QR-code generator' and 'Block 1' in raw_html:
                    with open(os.path.join(os.getcwd(), 'proxies.txt'), 'a+', encoding="utf-8") as file:
                        file.write(p)
                        file.write('\n')
                    time.sleep(5)
                    dr.get('http://2ip.ru')
                    time.sleep(10)

                    dr.quit()
                    return p

            except Exception as e:
                print(e)
                dr.quit()
                raise e

    @staticmethod
    def get_proxies_from_free_cz():
        path = ddd.install(browser=ddd.chrome, file_directory='src/lib/', verbose=True, chmod=True, overwrite=False,
                           version=None, filename=None, return_info=False)
        options = Options()
        options.headless = True

        options.add_argument('--start-maximized')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        dr = webdriver.Chrome(executable_path=path, options=options)

        for i in [
            '',
            # '2',
            # '3'
        ]:
            url = f'http://free-proxy.cz/ru/proxylist/country/RU/all/ping/all/{i}'
            dr.get(url)
            time.sleep(1)
            # hosts = [h.text for h in dr.find_elements_by_xpath('//table[@id="proxy_list"]/tbody/tr/td[1]') if h.text != '']
            # ports = [p.text for p in dr.find_elements_by_xpath('//tbody/tr/td[2]')]

            hosts = [
                h.text for h in WebDriverWait(dr, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//table[@id="proxy_list"]/tbody/tr/td[1]'))
                ) if h.text != ''
            ]

            ports = [
                p.text for p in WebDriverWait(dr, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[2]'))
                )
            ]

            ru_pool = [f'http://{i[0]}:{i[1]}' for i in list(zip(hosts, ports))]
            if os.path.isfile(os.path.join(os.getcwd(), 'proxies.txt')):
                with open(os.path.join(os.getcwd(), 'proxies.txt'), 'r', encoding="utf-8") as file:
                    poool = file.read().split()
                    ru_pool += poool

            random.shuffle(ru_pool)
            with open(os.path.join(os.getcwd(), 'proxies.txt'), 'w+', encoding="utf-8") as file:
                file.write('\n'.join(ru_pool))
                file.write('\n')
        dr.quit()


if __name__ == '__main__':
    ProxyRU.get_proxies_from_free_cz()
    PP = ProxyRU.get_proxy()
    print(f'proxy={PP}')
