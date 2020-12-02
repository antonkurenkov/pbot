import random
import time
import os
from faker import Faker
from fake_useragent import UserAgent
import pyderman as dr

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as CO
from selenium.webdriver.firefox.options import Options as FO
from selenium.webdriver.opera.options import Options as OO


class Producer:

    def __init__(self):
        self.virtual = None

        self.lastname = None
        self.middlename = None
        self.firstname = None
        self.sex = None
        self.bankname = None
        self.purpose = None
        self.adress = None

        self.useragent = None
        self.driver = None

    def validate_user(self, items):
        self.lastname = None
        self.middlename = None
        self.firstname = None
        self.sex = None
        for i in items:
            if i.endswith('ович') or i.endswith('овна') or i.endswith('евич') or i.endswith('евич'):
                self.middlename = i
                continue

            if i.endswith('ова') or i.endswith('ева'):
                self.lastname = i
                self.sex = 'female'
                continue
            if i.endswith('ов') or i.endswith('ев'):
                self.lastname = i
                self.sex = 'male'
                continue

            self.firstname = i

        # cut 3/4 of all cases because of mostly male audience
        if self.sex == 'female' and random.randint(1, 100) >= 20:
            return
        else:
            return self.firstname and self.middlename and self.lastname

    def create_useragent(self):
        while True:
            try:
                return UserAgent().random
            except:
                pass

    def create_user(self):
        while True:
            f = Faker('ru_RU')
            i = f.name().split(' ')
            if self.validate_user(i):
                self.adress = f.address()
                self.useragent = self.create_useragent()
                break

        return self.firstname, self.middlename, self.lastname

    def create_driver(self, proxy=None, headless=False):
        if self.virtual:
            return
        if proxy and not isinstance(proxy, str):
            with open(os.path.join(os.getcwd(), 'tested_proxies.txt')) as file:
                lines = file.read().split()
                proxy = random.choice(lines).strip()
        choice = random.choice([
            ['chrome', dr.chrome],
            ['chrome', dr.chrome],
            ['chrome', dr.chrome],
            # ['firefox', dr.firefox],
            # ['opera', dr.opera],
            # dr.phantomjs
        ])
        path = dr.install(browser=choice[1], file_directory='src/lib/', verbose=True, chmod=True, overwrite=False,
                          version=None, filename=None, return_info=False)

        if choice[0] == 'chrome':
            options = CO()
            if proxy:
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    "httpProxy": proxy,
                    "ftpProxy": proxy,
                    "sslProxy": proxy,
                    "proxyType": "MANUAL",
                }
        elif choice[0] == 'firefox':
            options = FO()
            if proxy:
                webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                    "httpProxy": proxy,
                    "ftpProxy": proxy,
                    "sslProxy": proxy,
                    "proxyType": "MANUAL",
                }
        elif choice[0] == 'opera':
            options = OO()
            if proxy:
                webdriver.DesiredCapabilities.OPERA['proxy'] = {
                    "httpProxy": proxy,
                    "ftpProxy": proxy,
                    "sslProxy": proxy,
                    "proxyType": "MANUAL",
                }
            # opera_profile = '/Users/antonkurenkov/Proj/pbot/archive'
            # opera_profile = '	/Users/antonkurenkov/Library/Application Support/com.operasoftware.Opera'
            # options.add_argument('user-data-dir=' + opera_profile)

        options.add_argument(self.useragent)
        options.headless = headless

        if random.randint(0, 100) >= 30:
            options.add_argument('--start-maximized')
        elif random.randint(0, 100) >= 30:
            options.add_argument("window-size=1920,1080")
        elif random.randint(0, 100) >= 30:
            options.add_argument("window-size=1024,768")

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        # options.add_argument("--disable-setuid-sandbox")
        options.add_experimental_option('useAutomationExtension', False)
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if choice[0] == 'chrome':
            self.driver = webdriver.Chrome(options=options, executable_path=path)
        elif choice[0] == 'firefox':
            self.driver = webdriver.Firefox(options=options, executable_path=path)
        elif choice[0] == 'opera':
            self.driver = webdriver.Opera(options=options, executable_path=path)

    def produce_data(self):
        with open(os.path.join(os.getcwd(), 'userdata', 'banknames.txt')) as file:
        # with open('/Users/antonkurenkov/Proj/pbot/userdata/banknames.txt') as file:
            self.bankname = random.choice(file.read().split('\n'))
        with open(os.path.join(os.getcwd(), 'userdata', 'purposes.txt')) as file:
        # with open('/Users/antonkurenkov/Proj/pbot/userdata/purposes.txt') as file:
            self.purpose = random.choice(file.read().split('\n'))
        obligatory_block = {
            'Name': f'{self.lastname} {self.firstname} {self.middlename}',
            'PersonalAcc': ''.join([str(random.randint(0, 9)) for _ in range(20)]),
            'BankName': self.bankname,
            'BIC': ''.join([str(random.randint(0, 9)) for _ in range(9)]),
            'CorrespAcc': random.choice(['0', ''.join([str(random.randint(0, 9)) for _ in range(20)])])
        }

        optional_block = {
            'Sum': str((random.randint(1, 100) * 1000) + (random.randint(1, 100) * 100 if random.choice([True, False, False, False]) else 0)),
            'Purpose': self.purpose,
            'FirstName': self.create_user()[0],
            'MiddleName': self.create_user()[1],
            'LastName': self.create_user()[2],
            'PayeeINN': ''.join([str(random.randint(0, 9)) for _ in range(12)]),
            'KPP': ''.join([str(random.randint(0, 9)) for _ in range(9)]),
            'PayerAdress': self.adress
        }

        return obligatory_block, optional_block

    @staticmethod
    def get_redirected_url():

        def num_postfix():
            return f'{"".join([random.choice(letters) for _ in range(random.randint(1, 5))])}={"".join([random.choice(nums) for _ in range(random.randint(1, 10))])}'

        def letter_postfix():
            return f'{"".join([random.choice(letters) for _ in range(random.randint(1, 5))])}={"".join([random.choice(arr) for _ in range(random.randint(16, 50))])}'

        letters = 'abcdefghijklmnopqrstuvwxyz'
        letters_upper = 'abcdefghijklmnopqrstuvwxyz'.upper()
        nums = '0123456789'
        uu = '_-'
        arr = letters + letters_upper + nums + uu

        fake_args = '&'.join([random.choice([num_postfix, letter_postfix])() for _ in range(random.randint(1, 3))])

        data_dict = {
            'social': [
                f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
                f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
                f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
                f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
                f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
                f'https://www.payqrcode.ru/?lr=2&redircnt={"".join([str(random.randint(1, 9)) for _ in range(10)])}.{random.randint(1, 9)}',
                f'https://www.payqrcode.ru/?fbclid={"".join([random.choice(arr) for _ in range(63)])}',
                f'https://www.payqrcode.ru/?{fake_args}'
            ],
            'direct': [
                'https://payqrcode.ru',
                'https://payqrcode.ru',
                'https://www.payqrcode.ru',
                'https://www.payqrcode.ru',
                'https://www.payqrcode.ru/',
                'https://www.payqrcode.ru/index',
                'https://www.payqrcode.ru/index',
                # 'http://www.payqrcode.ru',
                # 'http://www.payqrcode.ru/index',
                # 'http://payqrcode.ru',
                # 'http://payqrcode.ru/index',
            ]
        }
        source = data_dict[random.choice(list(data_dict.keys()))]
        return random.choice(source)


if __name__ == '__main__':
    p = Producer()
    p.create_user()
    p.create_driver(proxy=True)
    # required_block, optional_block = p.produce_data()
    p.driver.get('https://api.ipify.org?format=json')
    time.sleep(10)
    print(p.driver.title)
    p.driver.quit()
