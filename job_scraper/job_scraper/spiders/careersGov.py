import scrapy
import random
import json
import time
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from job_scraper.items import JobItem
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from job_scraper.settings import KEYWORDS, DRIVER_PATH


class CareersgovSpider(scrapy.Spider):
    name = "careersGov"
    allowed_domains = ["jobs.careers.gov.sg"]
    # start_urls = ["https://jobs.careers.gov.sg/?s={}".format(KEYWORDS.replace(" ", "+"))]

    # rules = [Rule(LinkExtractor(), callback="parse_item", follow=True)]
    def _random_sleep(self):
       sleep_time = random.randint(10,20)
       self.logger.info('Sleeping for {} seconds.\n'.format(sleep_time))
       time.sleep(sleep_time)

    def start_requests(self):
        service = webdriver.ChromeService(DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://jobs.careers.gov.sg/?s={}".format(KEYWORDS.replace(" ", "+")))

        while True:
            try:
                self._random_sleep()
                sel = Selector(text=self.driver.page_source)
                jobs = sel.xpath('//article/a/@href').extract()
                for job in jobs:
                    url = 'https://jobs.careers.gov.sg/' + job
                    yield(Request(url, callback=self.parse_job))

                next_page = self.driver.find_element(By.XPATH, '//button[@aria-label="Next page"]')
                if not next_page.is_enabled(): break
                next_page.click()

            except NoSuchElementException:
                self.logger.info("No more page.\n")
                break

        self.logger.info("Closing browser.\n")        
        self.driver.quit()

    def parse_job(self, response):
        json_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_data = json.loads(json_data)
        jobItem = JobItem()
        
        jobItem['url'] = response.url 
        jobItem['title'] = json_data['title']
        jobItem['company'] = json_data['hiringOrganization']['name']
        jobItem['details'] = json_data['description'] #
        jobItem['datePosted'] = json_data['datePosted']
        jobItem['employmentType'] = json_data['employmentType']
        jobItem['location'] = "Singapore"
        jobItem['salary'] = None
        yield jobItem
        # yield response.url