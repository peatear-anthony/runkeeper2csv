import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ChromeOptions

class Runkeeper:
    def __init__(self):
        load_dotenv()
    
    def __start_driver(self):
        chrome_driver = os.getenv("CHROME-DRIVER")
        userdata_dir = os.getenv("USER-DATA-DIR")
        print(chrome_driver)
        print(userdata_dir)
        options = ChromeOptions()
        options.add_argument('--user-data-dir=' + userdata_dir)
        #options.add_argument('--profile-directory=Peter') 
        self.driver =  webdriver.Chrome(executable_path=chrome_driver, options=options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.google.co.in")

    def test(self):
        self.__start_driver()


if __name__ == "__main__":
    runkeeper = Runkeeper()
    runkeeper.test()