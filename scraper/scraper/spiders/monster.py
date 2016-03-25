# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scraper.scraper.items import ScraperItem
from scraper.scraper.config import KEYWORDS, EMAIL, PASSWORD, CV_PATH
from scraper.scraper.comm.utils import gen_start_urls


class MonsterSpider(CrawlSpider):

    name = 'monster'
    allowed_domains = ['monster.fr']
    start_urls = gen_start_urls("http://offres.monster.fr/offres-d-emploi/?q=%s", KEYWORDS, "-")
    login_page = 'https://login.monster.fr/Login/SignIn'
    rules = [Rule(LinkExtractor(allow=['.*jobPosition=.*?']), 'parse_job',), Rule(LinkExtractor(allow=('.*&pg=.*?', )), follow=True)]

    def parse_job(self, response):
        job = ScraperItem()
        sel = Selector(response)
        job['url'] = response.url
        job_offer = sel.xpath('//title/text()').extract()
        job_offer = job_offer[0].strip()
        job_offer = job_offer.split('-')
        job['name'] = job_offer[0]
        job["email"] = None
        job["phone"] = None
        return job

    @staticmethod
    def execute_js():
        from scraper.scraper.models import Jobs, db_connect
        from selenium.webdriver.common.action_chains import ActionChains
        from sqlalchemy.orm import sessionmaker
        from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
        from selenium import webdriver
        import re
        import time

        # Get DB engine
        engine = db_connect()
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        # Iterate through job urls
        urls = []
        q = session.query(Jobs).filter((Jobs.url.like('http://offre-emploi.monster.fr%')) & (Jobs.processed == False)).all()
        for url in q:
            urls.append(url.url)

        # Init browser
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        browser = webdriver.Firefox(profile)
        action = ActionChains(browser)

        # Login to user space
        browser.get("https://login.monster.fr/Login/SignIn", )
        browser.find_element_by_name("EmailAddress").send_keys(EMAIL)
        browser.find_element_by_name("Password").send_keys(PASSWORD)

        elem = browser.find_element_by_xpath("//*[@id=\"signInContent\"]/form/div[3]/input[1]")
        action.move_to_element(elem).click().perform()
        time.sleep(5)

        # for each url, click on 'postuler'
        link = "http://offre-emploi.monster.fr/Apply/Apply.aspx?JobID="
        for url in urls:
            apply_link = re.findall(r"\b\d{6}\w+", url)
            try:
                apply_link = link+apply_link[0]
                print "* Processing %s" % url
                browser.get(apply_link)
                if 'Vous postulez' in browser.page_source.encode("utf-8"):
                    browser.find_element_by_css_selector("#CoverLetter1_DropDownListLetters > option:nth-child(2)").click()
                    browser.find_element_by_css_selector("#rbAuthorizedNo0").click()

                    # Click on "POSTULER"
                    browser.find_element_by_id('btnSubmit').click()
                    time.sleep(5)

                else:
                    pass

            except NoSuchElementException:
                raise

            except UnexpectedAlertPresentException:
                alert = browser.switch_to_alert()
                #alert.dismiss()
                continue

            finally:
                # Update database
                session.query(Jobs).filter(Jobs.url == url).update({'processed': True})
                session.commit()
                session.close()

        browser.close()

if __name__ == "__main__":
    MonsterSpider.execute_js()
