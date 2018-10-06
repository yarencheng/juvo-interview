from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from logger import logger
import time

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

def main():
    """
    [{
        name: "服裝 / 飾品 / 配件",              // layer 1 category
        sub_categories: [{
            name: "流行女裝",                   // layer 2 category
            link: "http://...",
            sub_categories: [{
                name: "換季必備外套",            // layer 3 category
                link: "http://...",
                sub_categories: [{
                    name: "風衣外套",           // layer 4 category
                    link: "http://...",
                    hot_items: [{
                        "product_name": "aaa", "product_price": "123"
                    }, ... ]
                }, ... ]
            }, ... ]
        }, ... ]
    }, ... ]
    """
    hot_sale_info = []

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
    layer_1_categories = category_all.find_elements_by_class_name("zone")
    for zone in layer_1_categories:
        title = zone.find_element_by_class_name("title")
        logger.info("Get layer 1 category: [%s]", title.text)
        hot_sale_info.append({
            "name": title.text
        })

    ##
    ## Collect layer 2 category
    ##
    for layer_1_category in layer_1_categories:
        layer_2_categories = layer_1_category.find_elements_by_class_name("site-list")
        for site in layer_2_categories:
            logger.info("Get layer 2 category: [%s]", site.text)

if __name__ == "__main__":
    main()