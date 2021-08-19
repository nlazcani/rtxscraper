from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import telegram
import os
import logging
import sys
import json
from webdriver_manager.chrome import ChromeDriverManager

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)

original = []

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("window-size=1400,2100")
chrome_options.add_argument("--disable-gpu")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"  # interactive

link = os.getenv("LINK")
custom_message = os.getenv("MESSAGE")
sleep_sec = os.getenv("TIME")
chatid = os.getenv("CHAT")
DATA_FOLDER = "data"
urls = []
notice = []
with open(os.path.join(DATA_FOLDER, "urls.json"), "r") as file:
    for line in file:
        urls.append(json.loads(line))

try:
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        desired_capabilities=caps,
        chrome_options=chrome_options,
    )
    for i, url in enumerate(urls):
        driver.get(url["url"])
        notice.append("")
        try:
            notice[i] = driver.find_element_by_class_name(url["class"]).text
        except Exception:
            pass
        original.append(notice[i])
    driver.close()
    while True:
        for i, url in enumerate(urls):
            driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                desired_capabilities=caps,
                chrome_options=chrome_options,
            )
            driver.get(url["url"])
            try:
                notice[i] = driver.find_element_by_class_name(url["class"]).text
            except Exception:
                notice[i] = ""
            driver.close()
            root.debug(f"text getted: {str(notice[i])}")
            if notice[i] != original[i]:
                original[i] = notice[i]
                bot = telegram.Bot("1906920746:AAEObw_eBqg1PkIBOSiwkIMTkzCWOtgNRUk")
                bot.send_message(
                    chat_id=chatid, text=f"{notice[i]} {url['message']} {link}"
                )
                root.info("chat")
            else:
                root.info("nothing change")
            root.info(msg=f"waitng for { int(sleep_sec)/len(urls) } seconds")
            time.sleep(int(sleep_sec) / len(urls))
finally:
    driver.close()
