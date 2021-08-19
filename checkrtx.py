from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import telegram
import os
import logging
import sys
from webdriver_manager.chrome import ChromeDriverManager

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

original = 'Coming Soon'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("window-size=1400,2100") 
chrome_options.add_argument('--disable-gpu')

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"  #  interactive

url = os.getenv('URL')
txt_clase = os.getenv('TXT_CLASE')
link = os.getenv('LINK')
custom_message = os.getenv('MESSAGE')
sleep_sec = os.getenv('TIME')
chatid = os.getenv('CHAT')

try:
    driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps, chrome_options=chrome_options)
    driver.get(url)    
    notice=driver.find_element_by_class_name(txt_clase).text
    driver.close()
    if notice != 'Add to Cart':
        original = notice
    while True:
        driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps, chrome_options=chrome_options)
        driver.get(url)
        notice=driver.find_element_by_class_name(txt_clase).text        
        driver.close()
        root.debug(f"text getted: {str(notice)}")
        if notice != original:
            original = notice
            bot=telegram.Bot('1906920746:AAEObw_eBqg1PkIBOSiwkIMTkzCWOtgNRUk')
            bot.send_message(chat_id=chatid, text = f'{notice} {custom_message} {link}')
            root.info('chat')
        else:
            root.info('nothing change')
        time.sleep(int(sleep_sec))
finally:
    driver.close()
