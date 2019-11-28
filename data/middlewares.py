# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re
from os import environ

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.binary_location = '/usr/bin/google-chrome'
browser = webdriver.Chrome(executable_path='/opt/google/chrome/chromedriver', chrome_options=options)
loggedin = False
where_i_am_now = ''
searched_same = False

class DataSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DataDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def jump_to_page_num(self, page_num):
        try:
            page_link = browser.find_element_by_link_text(str(page_num))
        except NoSuchElementException:
            return 0
        page_link.click()
        return page_num

    def leapfrog_to_page_num(self, page_num):
        page_link = browser.find_element_by_link_text('10')
        page_link.click()
        try:
            page_link = browser.find_element_by_link_text(str(page_num))
        except NoSuchElementException:
            return 0
        page_link.click()
        return page_num

    def move_to_the_page(self, page_num):
        page = 0
        if page_num == 1:
            return page_num
        if page_num <= 10:
            page = self.jump_to_page_num(page_num)
        else:
            page = self.leapfrog_to_page_num(page_num)
        return page

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        home_url = 'https://webapps1.chicago.gov/activegcWeb/'
        if request.url.startswith(home_url):
            page_num = request.cb_kwargs['page_num']
            browser.get('https://webapps1.chicago.gov/activegcWeb/')
            page = self.move_to_the_page(page_num)
            if not page == 0:
                body = browser.page_source
                # minify html
                body = body.replace('\t', '')
                body = body.replace('\n', '')
                body = re.sub('>\s*<', '><', body, 0, re.M)
                # minify html
                return HtmlResponse(home_url, body=body, encoding='utf-8', request=request) #
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
