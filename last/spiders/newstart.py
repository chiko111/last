
import scrapy
from scrapy.selector import Selector
from ..items import LastItem
from selenium import webdriver
import json
import time
class newstartSpider(scrapy.Spider):
    name = "newstart"
    allowed_domains = ["shop.mango.com"]
    def start_requests(self):
        url = "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"
        yield scrapy.Request(url = url, callback=self.parse_new, cookies={'bg':'1000'})
 # webDriver and passing button cookie
    def parse_new(self, response):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        with open("urls.json", "r") as f:
            temp_list = json.load(f)
        urls = list(map(lambda x: x["url"], temp_list))
        count = 0
        for i, url in enumerate(urls):
            driver.get(url)
            driver.implicitly_wait(1000)
            driver.find_element_by_id("onetrust-accept-btn-handler").click()
            time.sleep(2)
# Hand-off between Selenium and Scrapy happens here
            sel = Selector(text=driver.page_source)
            
# Extract names,prices,sizes,colors
            count += 1
            name = sel.xpath('//*[@id="headerMNG"]text()').getall()
            price = sel.xpath('//*[@id="app"]/main/div/div[3]/div[1]/div[2]/span[3]').getall()
            size = sel.xpath('//*[@id="sizeSelector"]/div').getall()
            color = sel.xpath('//*[@id="colorsContainer"]').getall()
            print(name)
            print(price)
            print(size)
            print(color)
#Crawl data           
            
            item = LastItem()              
            item["names"] = name
            item["prices"] = price
            item["sizes"] = size
            item["colors"] = color
            yield item
            
        else:
                # Logging the info of locations that do not have PM2.5 data for manual checking
                logger.error(f"{location} in {city},{country} does not have PM2.5")
# Terminating and reinstantiating webdriver every 200 URL to reduce the load on RAM
        if (i != 0) and (i % 200 == 0):
                driver.quit()
                driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
                logger.info("Chromedriver restarted") 
        
        driver.quit()
                