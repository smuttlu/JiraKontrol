import time
import requests
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException



chrome_options = Options()
chrome_options.add_argument("--start-maximized")  

driver = webdriver.Chrome(options=chrome_options)
url= (				jira url giriniz)
driver.get(url)
time.sleep(5)

def load_page_with_retry(url):
    
    while True:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-form-username')))
            print("Sayfa başarıyla yüklendi.")
            return  
        except (TimeoutException, WebDriverException) as e:
            print("Sayfa yüklenemedi, internet bağlantısı olabilir:", e)
            time.sleep(35)  


load_page_with_retry('http://ticket.kariyer.net/projects/SDK/queues/1')

try:
    username_field = driver.find_element(By.ID, 'login-form-username')
    password_field = driver.find_element(By.ID, 'login-form-password')
    login_button = driver.find_element(By.ID, 'login-form-submit')

    username_field.send_keys(		kullanıcı adı giriniz)
    password_field.send_keys(		sifre bilgisini giriniz)
    login_button.click()

    time.sleep(20)
except Exception as e:
    print("Giriş işlemi sırasında hata oluştu:", e)

def search_in_page(keyword):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        if keyword in body_text:
            print(f"'{keyword}' kelimesi bulundu.")
            send_teams_message("Yeni bir JIRA ticket'ı oluşturuldu!")
            return True
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False

def check_for_new_tickets():
    try:
        first_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pinnednav-opts-sd.queues"]/div[3]/div/div/ul/li[3]/a/span[1]'))
        )
        first_area.click()
        time.sleep(10)

        search_in_page('SDK')

        driver.back()
        time.sleep(10)

        second_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pinnednav-opts-sd.queues"]/div[3]/div/div/ul/li[1]/a/span[1]'))
        )
        second_area.click()
        time.sleep(10)

        search_in_page('SDK')

    except Exception as e:
        print("Hata oluştu:", e)

def send_teams_message(message):
    teams_webhook_url = 				teams webhook bilgisini giriniz
    data = {
        "text": message
    }
    try:
        response = requests.post(teams_webhook_url, json=data)
        response.raise_for_status()
        print("Teams'e mesaj gönderildi.")
    except requests.exceptions.RequestException as e:
        print(f"Teams'e mesaj gönderirken hata oluştu: {e}")

if __name__ == '__main__':
    while True:
        check_for_new_tickets()
        time.sleep(20)
