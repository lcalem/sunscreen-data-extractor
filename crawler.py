import lxml.html
import requests

from crawling_info import CRAWLING_INFO


class Crawler(object):
    '''
    will crawl a website to get sunscreen products htmls
    '''

    def __init__(self, website):
        if website not in CRAWLING_INFO:
            raise Exception("Unsupported website %s" % website)

        self.config = CRAWLING_INFO[website]

    def crawl(self):
        '''
        get the listing url content and yield the html of each product
        TODO: handle non 200 requests
        '''
        listing_url = self.config["listing_url"]
        listing_html = requests.get(listing_url).text

        htmldoc = lxml.html.fromstring(listing_html)

        product_urls = htmldoc.cssselect(self.config["listing_selector"])
        for url_element in product_urls:
            url = url_element.get("href")
            print("found product url %s" % url)
            yield requests.get(url).text


