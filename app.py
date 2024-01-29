from multiprocessing import Process
from time import sleep
from flask import Flask,jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from db import connect_db
from dotenv import load_dotenv
import os
from flask_cors import CORS
load_dotenv()
app = Flask(__name__)
CORS(app)
connector,cursor=connect_db()

@app.route("/api/v1/get_betting_results", methods=["GET"])
def getResult():
    query = "SELECT * from RESULTS ORDER BY id DESC LIMIT 10000"
    cursor.execute(query)
    result = cursor.fetchall()
    connector.commit()
    results = []
    for betting_result in result:
        results +=betting_result[1]
    return jsonify({"betting_results":results})


def startScraping():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--force-dark-mode")
    chrome_options.add_argument("--window-size=1024,768")
    
    try:
        _extracted_from_startScraping_8(chrome_options)
    except Exception as e:
          print(e)


# TODO Rename this here and in `startScraping`
def _extracted_from_startScraping_8(chrome_options):
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options,
    )
    browser.get("https://luck.bet/live-casino/game/1170048?provider=Evolution")
    print("loading finished")
    _extracted_from_startScraping_14(
        browser, "MULTICHANNEL", "dev1", "input email"
    )
    _extracted_from_startScraping_14(
        browser, "PASSWORD", "10203040A", "input password"
    )
    browser.find_element(By.ID, "signIn").click()
    print("credentials sent successfully")
    sleep(20)
    browser.execute_script('document.querySelector("button[data-id=\'id\']").click()')
    print("cookie")
   
    iframe1 = browser.find_element(By.XPATH, "//*[@id=\"game-window\"]/iframe")
    browser.switch_to.frame(iframe1)
    iframe2 = browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/iframe")
    browser.switch_to.frame(iframe2)
    actions = ActionChains(browser)
    while True:
        try:
            text = browser.find_element(By.TAG_NAME, "text")
            print(text.text)
            query = f"INSERT INTO RESULTS(value) values(\'{text.text}\')"
            cursor.execute(query)
            connector.commit()
            text_elements = browser.find_elements(By.TAG_NAME, "text")
            values = [text.text for text in text_elements]
        except Exception as e:
            print(e)
        while True:
            sleep(5)
            try:
                # window_size = browser.get_window_size()
                # window_width = window_size['width']
                # window_height = window_size['height']
                # center_x = int(window_width / 2)
                # center_y = int(window_height / 2)
                element=browser.find_element(By.TAG_NAME,"html")
                actions.move_to_element(element).click().perform()
                new_text_elements = browser.find_elements(By.TAG_NAME, "text")
                new_values = [text.text for text in new_text_elements]
                state = any(values[i] != new_values[i] for i in range(15))
                if state:
                    break
            except Exception as e:
                print(e)
            


# TODO Rename this here and in `startScraping`
def _extracted_from_startScraping_14(browser, arg1, arg2, arg3):
        # input("Press Enter to close the browser...")
    email = browser.find_element(By.ID, arg1)
    email.send_keys(arg2)
    print(arg3)

def startServer(port, host):
    app.run(host=host, port=port)

if __name__ == "__main__":
    app_process = Process(target=startServer, args=(os.getenv("PORT"), "0.0.0.0"))
    app_process.start()
    print("server is running at port 5000")
    # Start the long-running task in another process
    scraping_process = Process(target=startScraping)
    scraping_process.start()
    
    
    # Wait for both processes to finish
    app_process.join()
    scraping_process.join()
    disable_inactivity.join()