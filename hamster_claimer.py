from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup
from requests import get

from time import sleep

token: str = "API_TOKEN"
urls: list = [
    "YOUR_URL"]
admins: list = [
    1234567890
]


def send_message(chat_id: int, text: str) -> dict:
    payload: dict = {
        "chat_id": chat_id,
        "text": text
    }
    response: dict = get(
        f"https://api.telegram.org/bot{token}/sendmessage", data=payload).json()
    return response


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
web = webdriver.Firefox(options=options)

for admin in admins:
    send_message(admin, "started")

for url in urls:
    web.get(url)

    sleep(15)

    # value (claimed hamsters)
    value = web.find_element(
        By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div[2]/div/div/div[2]/div[2]").text

    # click claim
    web.find_element(
        By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div[2]/div/button").click()

    sleep(10)

    # balance (after claim value)
    balance = web.find_element(
        By.XPATH, "/html/body/div[1]/div/main/div[2]/div[2]/div/p").text

    # name
    name = web.find_element(
        By.XPATH, "/html/body/div[1]/div/main/header/div[1]/div/p").text.replace(" (CEO)", "")

    # get pph (profit per hour)
    pph = web.find_element(
        By.XPATH, "/html/body/div[1]/div/main/div[1]/div[2]/div/div/div[1]/div[2]").text

    # level (for example: GrandMaster)
    level = web.find_element(
        By.XPATH, "/html/body/div[1]/div/main/div[1]/div[1]/a/div[1]/div[1]/p").text
    
    print("{} claimed {}".format(name, value))

    for admin in admins:
        send_message(admin, f"name: {name} ({level})\n\nPPH: {pph}\n\nclaim: {value}\n\nbalance: {balance}")

web.close()
