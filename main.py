from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from logger import logger
import time

def get_driver():
    while True:
        try:
            driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME
            )
            return driver
        except:
            logger.warning("Connect to selenium failed. Sleep 1 seconds and try again")
            time.sleep(1)

def main():
    driver = get_driver()

    driver.get("https://tw.buy.yahoo.com/help/helper.asp?p=sitemap")

if __name__ == "__main__":
    main()