from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc
import pyperclip

import time

import json

from config import REGISTRATION_LINK, LOGIN_LINK, NAME, SURNAME, WORK,JOB_TITLE, PASSWORD


def browser():
    s = Service('geckodriver.exe')
    options = Options()
    firefox = webdriver.Firefox(service=s, options=options)
    firefox.implicitly_wait(20)
    firefox.set_page_load_timeout(20)
    print("///RUN FIREFOX TO GET API'S")
    return firefox


def register_temp_mail(driver: uc.Chrome, wait: WebDriverWait):
    driver.get('https://temp-mail.org/ru/10minutemail')
    pyperclip.copy("Загрузка")
    while True:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mail"]'))).click()
        a = ActionChains(driver)
        time.sleep(0.5)
        a.key_down(Keys.CONTROL).send_keys("C").key_up(Keys.CONTROL).perform()
        email_address: object = pyperclip.paste()
        time.sleep(2)
        if 'Загрузка' not in email_address:
            break
    print(f'TEMP EMAIL: {email_address}')
    return email_address


def register_on_apicraft(driver: webdriver.Firefox, wait: WebDriverWait, email_address: str):
    driver.get(REGISTRATION_LINK)
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[1]/div[1]/div/div/input"))).send_keys(NAME)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[1]/div[2]/div/div/input"))).send_keys(
        SURNAME)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[2]/div/input"))).send_keys(WORK)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[3]/div/input"))).send_keys(JOB_TITLE)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[4]/div/input"))).send_keys(email_address)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[5]/div/input"))).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[6]/div/input"))).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div/div/div[2]/form/div/div[8]/button"))).click()
    time.sleep(2)


def get_confirmation_link(driver: uc.Chrome, wait: WebDriverWait):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a/span[3]'))).click()
    time.sleep(2)
    mail_text = driver.find_element(By.XPATH,
                                    '//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/p').text
    link = "http" + mail_text.split("http")[1]
    return link


def login_get_apikey(driver: webdriver.Firefox, wait: WebDriverWait):
    time.sleep(3)
    driver.get(LOGIN_LINK)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div[2]/div/div[2]/form/div/div[1]/div/input"))).send_keys(
        temp_address)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div[2]/div/div[2]/form/div/div[2]/div/input"))).send_keys(
        PASSWORD)
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[3]/div/div[2]/div/div[2]/form/div/div[4]/button"))).click()
    time.sleep(2)
    api_key = driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div/div/div[2]/form/div/div/div[2]/div/div['
                                            '2]/div[2]/div[2]/div/div/div/input').get_attribute('value')
    return api_key


def write_keys(api_key: str):
    with open('keys.txt', 'a') as f:
        f.write(json.dumps(api_key) + '\n')


if __name__ == "__main__":
    wd_for_register = browser()
    wait_register_wd = WebDriverWait(wd_for_register, 10)
    api_keys = []
    while True:
        try:
            print('RUN CHROME DRIVER')
            wd_for_mail = uc.Chrome(use_subprocess=True)
            wait_wd_for_mail = WebDriverWait(wd_for_mail, 120)
            temp_address = register_temp_mail(driver=wd_for_mail, wait=wait_wd_for_mail)
            register_on_apicraft(driver=wd_for_register, wait=wait_register_wd, email_address=temp_address)
            confirm_link = get_confirmation_link(driver=wd_for_mail, wait=wait_wd_for_mail)
            wd_for_register.get(confirm_link)
            wd_for_mail.quit()
            api_key = login_get_apikey(wd_for_register, wait_register_wd)
            print(f"GOT API_KEY: {api_key}")
            write_keys(api_key)
        except KeyboardInterrupt:
            wd_for_register.quit()
