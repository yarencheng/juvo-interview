from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from logger import logger
import time
import csv

def get_driver():
    url = 'http://selenium:4444/wd/hub'
    while True:
        try:
            logger.info("connect to [%s]", url)
            driver = webdriver.Remote(
                command_executor=url,
                desired_capabilities=DesiredCapabilities.CHROME
            )
            return driver
        except:
            logger.warning("Connect to selenium failed. Sleep 1 seconds and try again")
            time.sleep(1)

def skip_alert_pop_windows_if_present(driver):
    try:
        a1 = driver.switch_to.alert
        logger.warning("Get alert: [%s]", a1.text)
        a1.accept()
        return True
    except:
        return False


def main():
    logger.info("start")
    driver = get_driver()

    ##
    ## Locate <div> '全部商品分類'
    ##
    driver.get("https://tw.buy.yahoo.com/help/helper.asp?p=sitemap")
    category_all = driver.find_elements_by_xpath("//*[text()='全部商品分類']")

    if len(category_all) != 2:
        logger.error("Locate [%s] failed", '全部商品分類')
        return

    category_all = category_all[1] ## first element is <title>
    logger.debug("category_all = %s", category_all.text)

    category_all = category_all.find_element_by_xpath("..") ## get parent element
    logger.debug("category_all = %s", category_all.text)

    ###
    ### Collect layer 1 category
    ###
    layer_1_info = []
    zones = category_all.find_elements_by_class_name("zone")
    for zone in zones:
        title = zone.find_element_by_class_name("title")
        logger.info("Get layer 1 category: [%s]", title.text)
        layer_1_info.append({
            "name": title.text,
            "element": zone
        })

    ##
    ## Collect layer 2 category
    ##
    layer_2_info = []
    for layer_1_category in layer_1_info:
        layer_2_categories = layer_1_category["element"].find_elements_by_class_name("site-list")
        for site in layer_2_categories:
            logger.info("Get layer 2 category: [%s]", site.text)

            link = site.find_element_by_css_selector("*").get_attribute("href")

            layer_2_info.append({
                "parent": layer_1_category["name"],
                "name": title.text,
                "element": site,
                "link": link,
            })

    ##
    ## Collect layer 3 category
    ##
    layer_3_info = []
    for layer_2_category in layer_2_info:
        try:
            logger.debug("layer_2_category: [%s]", layer_2_category["name"])
            logger.debug("Get URL: [%s]", layer_2_category["link"])
            driver.get(layer_2_category["link"])

            sitelists = driver.find_elements_by_class_name("sitelist")
            for sitelist in sitelists:
                try:
                    title = sitelist.find_element_by_class_name("stitle")
                except:
                    continue

                logger.info("Get layer 3 category: [%s]", title.text)
                layer_3_info.append({
                    "parent": layer_2_category["name"],
                    "name": title.text,
                    "element": sitelist
                })
        except:
            logger.warning("Failed to get layer 3 info from [%s]", layer_2_category["name"])
            skip_alert_pop_windows_if_present(driver)

        # break ## debug

    ##
    ## Collect layer 4 category
    ##
    layer_4_info = []
    for layer_3_category in layer_3_info:
        try:
            logger.debug("layer_3_category: [%s]", layer_3_category["name"])
            lists = layer_3_category["element"].find_elements_by_class_name("list")
            for l in lists:
                if len(l.text) == 0:
                    continue
                logger.info("Get layer 4 category: [%s]", l.text)
                link = l.find_element_by_css_selector("*").get_attribute("href")

                layer_4_info.append({
                    "parent": layer_3_category["name"],
                    "name": l.text,
                    "element": l,
                    "link": link,
                })
        except:
            logger.warning("Failed to get layer 4 info from [%s]", layer_3_category["name"])
        # break ## debug

    ##
    ## Collect item info
    ##
    item_info = []
    for layer_4_category in layer_4_info:
        logger.debug("layer_4_category: [%s]", layer_4_category["name"])
        logger.debug("Get URL: [%s]", layer_4_category["link"])
        driver.get(layer_4_category["link"])

        near_hot = None
        try:
            near_hot = driver.find_element_by_xpath("//*[text()='近期熱銷']")
        except:
            logger.warning("Missing '近期熱銷' in [%s]", layer_4_category["name"])
            continue
        near_hot = near_hot.find_element_by_xpath("..") ## get parent
        link = near_hot.get_attribute("href")
        logger.debug("Get URL: [%s]", link)
        driver.get(link)

        items = driver.find_elements_by_class_name("wrap")
        for item in items:
            title = item.find_element_by_class_name("srp-pdtitle")
            price = item.find_element_by_xpath("//span[@class='srp-listprice-class']")

            logger.info("Item: [%s] [%s] [%s]", layer_4_category["name"], title.text, price.text)

            item_info.append({
                "parent": layer_4_category["name"],
                "name": title,
                "price": price
            })

    ##
    ## Dump to csv
    ##

if __name__ == "__main__":
    # main()
    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['姓名', '身高', '體重'])
        writer.writerow(['令狐沖', 175, 60])
        writer.writerow(['岳靈珊', 165, 57])
