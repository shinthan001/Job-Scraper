import time
import random
import scrapy
import json
from selenium.webdriver import Chrome, ChromeService
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
# from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from job_scraper.items import JobItem
from job_scraper.settings import DRIVER_PATH, LOCATION, KEYWORDS


class JobstreetSpider(scrapy.Spider):
   name = "jobstreet"
   allowed_domains = ["sg.jobstreet.com"]
   # start_urls = ["https://sg.jobstreet.com/{}-jobs/in-{}".format(KEY_WORDS,WHERE)]

   def __init__(self):
       self.service = ChromeService(executable_path=DRIVER_PATH)
       self.driver = Chrome(service=self.service)
       self.start_urls = ["https://sg.jobstreet.com/{}-jobs/in-{}".format(KEYWORDS,LOCATION)]
       self.driver.get(self.start_urls[0])
       self.driver.maximize_window()

   def _random_sleep(self):
       sleep_time = random.randint(5,10)
       self.logger.info('Sleeping for {} seconds.\n'.format(sleep_time))
       time.sleep(sleep_time)

   def parse(self, response):

       jobItem = JobItem()
       while True:
           try:
               # scraping current page
               self._random_sleep()
               sel = Selector(text=self.driver.page_source)
               posts = sel.xpath('//a[@data-automation="job-list-view-job-link"]/@href').extract()
               parent_url = self.driver.current_url

               # crawling each job post
               for post in posts:
                   url = "https://sg.jobstreet.com" + post
                   self.driver.get(url)
                   self._random_sleep()

                   # parse job post
                   sel = Selector(text=self.driver.page_source)
                   json_data = sel.xpath('//script[@type="application/ld+json"]/text()').extract()
                   json_data = json.loads(json_data[1])

                   jobItem['url'] = self.driver.current_url 
                   jobItem['title'] = json_data['title']
                   jobItem['company'] = json_data['hiringOrganization']['name']
                   jobItem['details'] = json_data['description'] #
                   jobItem['datePosted'] = json_data['datePosted']
                   jobItem['employmentType'] = json_data['employmentType']

                #    jobItem['title'] = sel.xpath('//h1[@data-automation="job-detail-title"]/text()').get()
                #    jobItem['company'] = sel.xpath('//span[@data-automation="advertiser-name"]/text()').get()
                   jobItem['location'] = sel.xpath('//span[@data-automation="job-detail-location"]/text()').get()
                   jobItem['salary'] = sel.xpath('//span[@data-automation="job-detail-salary"]/text()').get()
                #    jobItem['details'] = sel.xpath('//div[@data-automation="jobAdDetails"]/div').get() 
                   yield jobItem
                                       
               # navigating to next page
               self.driver.get(parent_url)
               self._random_sleep()
               next_page = self.driver.find_element(By.XPATH, '//a[@rel="nofollow next"]')
               if not next_page.is_enabled(): break
               next_page.click() 

           except NoSuchElementException:
               self.logger.info('No more page.\n')
               break
        
       self.logger.info("Closing browser.\n")        
       self.driver.quit()

   def close(self):
       pass