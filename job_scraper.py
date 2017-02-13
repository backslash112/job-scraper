#!/usr/bin/env python

#
# Job Scraper from the www.lagou.com
#

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from urllib.request import urlopen
import ssl
from scrapy.selector import Selector
import time
import csv

class JobScraper(object):
    "Job Scraper Object"

    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context

    # def build_urls(titles):
    #     urls = []
    #     city = "深圳"
    #     for title in titles:
    #         template_url = "https://www.lagou.com/jobs/list_{0}?px=default&city={1}#filterBox"
    #         url = template_url.format(title, city)
    #         urls.append(url)
    #     return urls

    def open_main_page(self):
        print("opening the main page...")
        url = "https://www.lagou.com/"
        # executable_path = 'libs/phantomjs-2.1.1/bin/phantomjs'
        # self.driver = webdriver.PhantomJS(executable_path=executable_path)
        chromedriver = "/Applications/Google Chrome.app/Contents/MacOS/chromedriver"
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.get(url)
        try:
            self.driver.find_elements_by_class_name('tab')[0].click()
        except Exception as e:
            pass
        finally:
            pass
            # self.search_with_titles()

    def back_to_main_page(self):
        # print("back to the main page...")
        self.driver.back()

    # def search_with_titles():
    #     all_job_links = []
    #     for title in titles:
    #         job_links = self.get_job_links_with_title(self.driver, title)
    #         all_job_links += job_links
    #         print("--------------------- all_job_links: ", len(all_job_links))
    #     print("===================== all_job_links: ", len(all_job_links))

    def get_job_links(self):
        # Get all the job links in every page
        job_links = []
        job_element_list = self.driver.find_elements_by_class_name('position_link')
        for job_element in job_element_list:
            job_link = job_element.get_attribute("href")
            print(job_link)
            job_links.append(job_link)
            time.sleep(0.1)
        return job_links

    def focus_pager(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def click_next_page_button(self):
        # Click the next page
        next_page = self.driver.find_element_by_class_name('pager_next')
        # print("next_page: ", next_page.text)
        next_page.click()
        # print("click the next page button...")
        time.sleep(1)
        print("get_current_page_number: ", self.get_current_page_number())

    def get_current_page_number(self):
        current_page = self.driver.find_element_by_class_name('pager_is_current')
        return int(current_page.text)

    def get_job_links_with_title(self, title):
        self.driver.find_element_by_id('search_input').send_keys(title)
        self.driver.find_element_by_id('search_button').click()
        print("Search with {0}".format(title))

        title_job_links = []
        job_links = self.get_job_links()
        title_job_links += job_links
        prev_page_number = 0
        while self.get_current_page_number() == prev_page_number + 1:
            prev_page_number = self.get_current_page_number()
            self.focus_pager()
            time.sleep(0.3)
            self.click_next_page_button()
            job_links = self.get_job_links()
            title_job_links += job_links

        return title_job_links


    def open_job(self, url):
        html = urlopen(url)
        self.parse_job(html.read())

    def parse_job(self, body):
        response = Selector(text=body)
        job_id = response.xpath('//input[@id="jobid"]/@value').extract_first()
        title = response.css('span.name::text').extract_first()
        salary = response.css('span.salary::text').extract_first().strip()
        years =  response.css('span::text').re(r'经验\d-\d年')[0]
        degree = response.css('span.salary').xpath('../span/text()').extract()[3].strip()[:-2]
        post_date = response.css('p.publish_time::text').extract_first().split('\xa0')[0]
        description = response.css('dd.job_bt').extract_first()
        location = response.xpath('//div/a[contains(@href, "district")]/text()').extract_first()
        address = response.xpath('//input[@name="positionAddress"]/@value').extract()
        company_short_name = response.xpath('//div').css('h2.fl::text').extract_first().strip()
        company_full_name = response.xpath('//img[@height=96]/@alt').extract_first()
        # url = scrapy.Field()

    def parseJobList(self, body):
        # bsObj = BeautifulSoup(html)


        job_urls = []
        return job_urls

    def parseJob(self, body):
        # bsObj = BeautifulSoup(html)
        pass

    def parseCompany(self, body):
        # bsObj = BeautifulSoup(html)
        pass

def save_to_csv(title, job_urls):
    with open('{0}-links.csv'.format(title), 'w', newline='') as fp:
        a = csv.writer(fp, delimiter="\n")
        # a = csv.writer(fp)
        a.writerow([title])
        a.writerows([job_urls])

def run():
    job_scraper = JobScraper()
    job_scraper.open_main_page()
    all_job_links = []
    titles = ['技术经理', '技术总监', '架构师', '高级软件', '高级开发', '开发工程师', '软件工程师', 'Python', '爬虫', '程序员', '研发']
    for title in titles:
        title_job_links = job_scraper.get_job_links_with_title(title)
        save_to_csv(title, title_job_links)
        job_scraper.back_to_main_page()


if __name__ == "__main__":
    run()
