import requests
import numpy as np
import cvlib as cv
import cv2
import time
import base64
import uuid
import os
import sys
from exceptions import get_exceptions_args

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException


class CNN:

    @staticmethod
    def is_valid(url, obj):
        while True:
            try:
                image = requests.get(url)
                nparr = np.frombuffer(image.content, np.uint8)
                im = cv2.imdecode(nparr, flags=1)
                objects = cv.detect_common_objects(im, confidence=0.5, nms_thresh=1, enable_gpu=False)[1]
                if obj.lower() in objects:
                    # print(f'[CNN] object is a {obj} from [{objects}]')
                    return True
                # print(f'[CNN] object is not a {obj} from [{objects}]')
                return False
            except Exception as e:
                print(e)

    @staticmethod
    def get_nparray(img):
        return np.frombuffer(img, np.uint8)

    @staticmethod
    def calc_image_hash(raw_img):
        img_data = base64.b64decode(raw_img)
        fname = f'{uuid.uuid4()}.png'
        with open(fname, 'wb') as file:
            file.write(img_data)

        image = cv2.imread(fname)  # Прочитаем картинку
        os.remove(fname)
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
        avg = gray_image.mean()  # Среднее значение пикселя
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

        # Рассчитаем хэш
        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"

        return _hash

    # @staticmethod
    # def compare_hash(hash1, hash2):
    #     l = len(hash1)
    #     i = 0
    #     count = 0
    #     while i < l:
    #         if hash1[i] != hash2[i]:
    #             count = count + 1
    #         i = i + 1
    #     return count == 0


class Solver(CNN):

    def __init__(self):
        self.driver = None
        self.presence_of_challenge = None
        self.done = False

    def locate_captcha(self, on_login_page=False):
        try:
            captchas_list = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="select-wrapper"]')))
            captchas_list.click()
            time.sleep(1)
            items = captchas_list.find_elements_by_tag_name("li")

            for elem in items:
                if elem.text == 'hCaptcha':
                    elem.click()
            self.solve_hcaptcha(on_login_page=on_login_page)
        except:
            print('[SOLVER] NO CAPTCHA TO SOLVE')

    def process_grid(self, obj):
        try:
            for i in range(1, 10):  # for 9 images in grid
                try:
                    image_wrapper = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((
                            By.XPATH, f'//div[@class="task-image"][{i}]/div[@class="image-wrapper"]')))
                    image_path = image_wrapper.get_attribute('innerHTML').split('&quot;')[-2]
                    if self.is_valid(url=image_path, obj=obj):
                        try:
                            image_btn = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((
                                    By.XPATH, f'//div[@class="task-image"][{i}]')))
                            image_btn.click()
                        except StaleElementReferenceException as e:
                            print("[SOLVER] MISSED THE IMAGE CLICK...")
                except TimeoutException as e:
                    # print(f"{(get_exceptions_args())} {e.args[0]}")
                    print("[SOLVER] LOST IMAGES GRID")
                    return
        except Exception as e:
            print(f"[SOLVER] {obj.upper()} DETECTION CHALLENGE FAILED WITH {(get_exceptions_args())} {e.args[0]}")

    def solve_challenge(self, obj):
        while True:
            try:
                self.process_grid(obj=obj)
                button = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//div[@class="button-submit button"]')))
                time.sleep(1)
                btn_txt = button.text
                button.click()
                if btn_txt == 'Check':
                    print(f'[SOLVER] SOLVED CHALLENGE: {obj.upper()}')
                    return
            except ElementClickInterceptedException as e:
                print('[SOLVER] NO CHALLENGE GRID')
                return

    def process_popup(self, on_login_page):
        try:
            hcaptcha_popup = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//iframe[@title="Main content of the hCaptcha challenge"]')))
                    # (By.XPATH, '//iframe[@title="widget containing checkbox for hCaptcha security challenge"]')))
            self.driver.switch_to.frame(hcaptcha_popup)
        except TimeoutException as e:
            print('[SOLVER] NO POPUP')
            self.done = True
            return
        if on_login_page:
            self.driver.execute_script("window.scrollBy(0,2000)")
        obj = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="prompt-text"]'))) \
            .text.split(' ')[-1] \
            .replace("motorbus", "bus")

        print(f'[SOLVER] PROCESS POPUP: {obj.upper()}')
        self.solve_challenge(obj)
        self.driver.switch_to.default_content()

    def solve_hcaptcha(self, on_login_page=False):
        print('[SOLVER] SOLVING HCAPTCHA...')
        hcaptcha = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="h-captcha"]/iframe')))
        hcaptcha.click()
        while True:
            # self.presence_of_challenge = True
            # self.driver.switch_to.default_content()
            try:
                self.process_popup(on_login_page)
                time.sleep(1)
                if self.done:
                    return
            except Exception as e:
                print(f"[SOLVER] ERROR.. {(get_exceptions_args())} {e.args[0]}")
                self.driver.switch_to.default_content()
                return

