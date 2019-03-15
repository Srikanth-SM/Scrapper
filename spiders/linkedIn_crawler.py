# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import os
from scrapy.utils.response import open_in_browser
from scrapy.spiders.init import InitSpider


class LinkedinCrawlerSpider(InitSpider):
    name = 'linkedIn_crawler'
    # allowed_domains = ['http://linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = ['https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A84%22%2C%22us%3A49%22%5D&origin=FACETED_SEARCH']
    user_name = os.getenv("username")
    password = os.getenv("password")

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def after_login(self, response):
        # if "authentication failed" in response.body:
        #     self.log("Login failed", level=log.ERROR)
        #     return   
        # print(dir(response), response.url)
        # open_in_browser(response.url)
        return self.initialized()
        
    def login(self, response):
        token = response.xpath('//*[@name="loginCsrfParam"]/@value').extract_first()
        print(self.user_name, token)
        return FormRequest.from_response(response, formdata={
            "session_key": self.user_name,
            "session_password": self.password,
            # "loginCsrfParam": token,
            # "isJsEnabled": False,
            # "fp_data": False
            },
            callback=self.after_login)
    
    def parse(self, response):
        name = response.css('span::text').getall()
        print("Inside parse", name)