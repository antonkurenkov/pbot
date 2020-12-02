from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from solver import Solver
from cradle import Producer
from geo import main as get_proxy_from_geo
from exceptions import get_exceptions_args

import subprocess
import random
import time


class User(Solver, Producer):

    def __init__(self, url, local, virtual=False, proxy=None, headless=True):
        super().__init__()
        self.virtual = virtual
        self.proxy = proxy
        if not self.virtual:

            self.create_user()
            self.create_driver(proxy=proxy, headless=headless)
            self.required_block, self.optional_block = self.produce_data()
            self.done = False
            self.speed = 1 + (random.randint(-7, 5) / 10)

    @staticmethod
    def happened(probability_coeff=100, always=False):
        """
        # 2 = 2%
        # 5 = 3.5%
        # 10 = 6%
        # 20 = 10%
        # 30 = 16%
        # 50 = 25%
        # 100 = 50%
        # 200 = 75%
        # 250 = 80%
        # 500 = 90%
        # 1000 = 95%
        # 10000 = 99%
        """
        luck = random.random() + random.random()
        if always:
            luck = 10000
        return random.randint(0, int(probability_coeff * luck)) >= random.randint(0, 100)

    def typewrite(self, string, elem):
        seed = self.speed / 10
        if not any(map(str.isalpha, string)):
            seed *= 5
        for idx, letter in enumerate(string):
            elem.send_keys(letter)
            time.sleep(seed)
            if letter == ' ':
                time.sleep(1)
            if not idx % random.randint(4, 6):
                time.sleep(1)

    def find_required_fields_for_input(self, required_block=None):
        print('find_required_fields_for_input')
        if self.virtual:
            return
        order = ('Name', 'PersonalAcc', 'BankName', 'BIC', 'CorrespAcc')
        fields = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="wrap-input100 validate-input m-b-23"]/input[@class="input100"]')))
        for f, data in zip(fields, order):
            self.scroll(px=random.randint(30, 120), scrollback=False)
            f.click()
            time.sleep(random.randint(1, 5) + random.random())
            self.typewrite(string=self.required_block[data], elem=f)
            time.sleep(random.randint(1, 5) + random.random())

    def find_optional_fields_for_input(self, optional_block=None):
        print('find_optional_fields_for_input')
        if self.virtual:
            return
        order = ('Sum', 'Purpose', 'FirstName', 'LastName', 'MiddleName', 'PayeeINN',  'KPP', 'PayerAdress')
        fields = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="wrap-input100 m-b-23"]/input[@class="input100"]')))
        for f, data in zip(fields, order):
            self.scroll(px=random.randint(30, 120), scrollback=False)
            if self.happened(probability_coeff=1000):
                f.click()
                time.sleep(random.randint(1, 5) + random.random())
                self.typewrite(string=self.optional_block[data], elem=f)
                time.sleep(random.randint(1, 5) + random.random())
            if order == 'Purpose' and self.happened(probability_coeff=250):
                break
            if self.happened(probability_coeff=10):
                break

    def scroll(self, px=None, scrollback=True, forward=True):
        print('scroll')
        if not forward:
            forward = -1
        if self.virtual:
            return
        if px is None:
            seed = random.randint(500, 1000)
        else:
            seed = px
        scrolled = 0

        while True:
            mouse_wheel_move = round(random.randint(2, 12) * self.speed)
            self.driver.execute_script(f"window.scrollBy(0,{mouse_wheel_move * forward})")
            scrolled += mouse_wheel_move
            if scrolled >= seed:
                break
            if time.time() % mouse_wheel_move:
                time.sleep(random.random() / 100)
        time.sleep(random.random())

        if scrollback:
            while True:
                mouse_wheel_move = -round(random.randint(2, 12) * self.speed)
                self.driver.execute_script(f"window.scrollBy(0,{mouse_wheel_move * forward})")
                scrolled += mouse_wheel_move
                if scrolled <= 0:
                    break
                if time.time() % mouse_wheel_move:
                    time.sleep(random.randint(0, 1) / float(random.randint(1, 100)))
            time.sleep(random.random())

        time.sleep(random.randint(1, 5))

    def solve_captcha(self, on_login_page):
        print('solve_captcha')
        if self.virtual:
            return
        self.solve_hcaptcha(on_login_page=on_login_page)

    def submit_form(self):
        print('submit_form')
        if self.virtual:
            return
        self.driver.switch_to.default_content()
        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="login100-form-btn"]')))
        time.sleep(random.random())
        button.click()

    def click_back(self):
        print('click_back')
        if self.virtual:
            return

        def inner():
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="login100-form-btn"]')))
            time.sleep(random.random())
            button.click()

        def outer():
            self.driver.execute_script('history.back();')

        func = random.choice([inner, outer])
        func()

    def click_random_button(self):
        print('click_random_button')
        if self.virtual:
            return

        def fake_submit():
            try:
                buttons = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button')))
                b = random.choice(buttons)
                time.sleep(random.random())
                b.click()
                time.sleep(random.randint(1, 3))
                self.driver.switch_to.default_content()
            except:
                pass

        def fake_click():
            try:
                forms = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input')))
                f = random.choice(forms)
                time.sleep(random.random())
                f.submit()
                time.sleep(random.randint(1, 3))
                self.driver.switch_to.default_content()
            except:
                pass

        func = random.choice([fake_click, fake_submit])
        func()

    def click_on_adv_banner(self):
        print('click_on_adv_banner')
        if self.virtual:
            return
        self.scroll(px=2000, scrollback=False)
        button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//footer/div/p/a')))
        time.sleep(random.random())
        button.click()
        self.driver.switch_to.default_content()

    def do_random_stuff(self):
        print('do_random_stuff')
        for _ in range(random.randint(0, 5)):
            try:
                self.scroll()
                self.click_random_button()
            except:
                break

    def do_job(self):
        print('do_job on website')

        def redirected(probability_coeff=250):
            # probability_coeff = 100000  # TODO
            if self.happened(probability_coeff=probability_coeff):
                self.click_on_adv_banner()
                if self.happened(probability_coeff=50):  # 25%
                    self.do_random_stuff()
                return True

        # if self.happened(probability_coeff=50):  # 25%
        #     self.scroll()
        # if self.happened(probability_coeff=20):  # 25%
        #     if not self.virtual:
        #         time.sleep(random.randint(1, 6))
        #
        # if not redirected(probability_coeff=20):  # 10%
        #
        #     if self.happened(probability_coeff=500):  # 90%
        #         self.find_required_fields_for_input()
        #         self.scroll(px=random.randint(100, 200), scrollback=False)
        #
        #         if self.happened(probability_coeff=20):  # 25%
        #             if not self.virtual:
        #                 time.sleep(random.randint(1, 6))
        #
        #         if not redirected(probability_coeff=1):  # 2%
        #
        #             if self.happened(probability_coeff=100):  # 50%
        #                 self.find_optional_fields_for_input()
        #
        #                 if self.happened(probability_coeff=20):
        #                     self.scroll(forward=False)
        #
        #             if self.happened(probability_coeff=20):  # 25%
        #                 if not self.virtual:
        #                     time.sleep(random.randint(1, 6))
        #
        #             if self.happened(probability_coeff=500):  # 90%
        self.scroll(forward=True, scrollback=False, px=2000)
        self.solve_captcha(on_login_page=True)

        if not redirected(probability_coeff=5):  # 3.5%

            if self.happened(probability_coeff=20):
                self.scroll(forward=False)

            self.submit_form()

            if not redirected(probability_coeff=10):  # 6%

                if self.happened(probability_coeff=20):  # 10%
                    self.click_back()

                    if self.happened(probability_coeff=20):  # 25%
                        if not self.virtual:
                            time.sleep(random.randint(1, 6))

                    redirected(probability_coeff=10)  # 6%

    def be_human(self, url: str):
        if not self.virtual:
            self.driver.get(url)
        if self.virtual or self.driver.title == 'Payment QR-code generator':
            if not self.virtual:
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
            self.do_job()
            success = True
        else:
            print(self.driver.title)
            success = False
        return success


if __name__ == '__main__':

    url_to_visit = 'https://www.payqrcode.ru'
    # url_to_visit = 'http://localhost:5000/'
    # url_to_visit = 'http://aqr-coder.herokuapp.com'
    users_local = False
    virtual = False
    bot_number = 76

    used_queue = []
    # for i in range(bot_number):
    while True:
        try:
            proxy = get_proxy_from_geo()
            # proxy = None
            try:
                u = User(url_to_visit, local=users_local, virtual=virtual, proxy=proxy, headless=True)  # or proxy=True to take random from tested.txt
                redirected = u.get_redirected_url()
            except Exception as e:
                print(f'user init failed with {e} on {get_exceptions_args()}')
                raise e

            try:
                print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}] VISIT {redirected} over {proxy}')
                success = u.be_human(redirected)
            except Exception as e:
                print(f'user walk failed with {e} on {get_exceptions_args()}')
                raise e
            # if success:
            #     if not virtual:
            #         time.sleep(random.randint(1, 10))
            #     used_queue.append(u.proxy)
            # u.driver.quit()
        except Exception as e:
            try:
                if u.driver:
                    u.driver.quit()
                    time.sleep(random.randint(1, 10))
            except:
                pass

            print(f'Exc = {e}')
            success = False
        print('---')

        processes = subprocess.getoutput(['pgrep chrome'])
        if processes:
            killed = subprocess.check_output(f'sudo kill -9 {processes}'.split())
            processes = processes.replace('\n', ' ')
            print(f'killed {processes}')

        if not virtual and success:
            zzz = random.randint(10, 1800)
            print(f'sleeping {zzz}s')
            time.sleep(zzz)


#  https://aviso.bz/?r=bohdanknyaz