import requests
import urllib.parse

from pprint import pprint

from crawler import Crawler
from parsers import BeautytapParser, SkinCharismaParser, SunscreenException


class SunscreenDataExctractor(object):

    def __init__(self):
        self.beautytap_parser = BeautytapParser()
        self.skincharisma_parser = SkinCharismaParser()

    def build_analysis_url(self, raw_ingredients):
        base_url = "https://www.skincarisma.com/products/analyze"
        base_url += "?utf8=%E2%9C%93"                   # add utf8 parameter
        base_url += "&product%5Bingredient%5D="         # product ingredients parameter

        base_url += urllib.parse.quote_plus(raw_ingredients)
        return base_url

    def compute_score(self, analysis_results):
        '''
        I have a personal score (out of 100) for every sunscreen that includes many factors including
        ones that I can only get after testing the product.
        Here I output a part of the score (out of 40) that is easily computed with the analysis results
        - 10: avobenzone yes/no
        - 10: octocrylene yes/no
        - 10: octinoxate yes/no
        - 10: EWG safety data
        TODO: add the UVA part (need to extract the UVA protection value from name / desc)
        '''
        score = 0
        for component in ["avobenzone", "octocrylene", "octinoxate"]:
            if analysis_results[component] is False:
                score += 10

        # EWG
        score += (100 - (sum(analysis_results["ewg_safety"][1:]))) / 10

        return score

    def parse_product(self, product_html):

        product_results = self.beautytap_parser.parse_html(product_html)

        analysis_url = self.build_analysis_url(product_results["ingredients"])
        # for this website the whole ingredient list is a get parameter so if it's too long we get a 414 (so we skip it here)
        if len(analysis_url) >= 8190:
            raise SunscreenException("analysis url too long, skipping product")

        analysis_html = requests.get(analysis_url).text
        analysis_results = self.skincharisma_parser.parse_html(analysis_html)

        results = {
            "product_name": product_results["product_name"],
            "INCI": product_results["ingredients"],
            "analysis": analysis_results,
            "score40": self.compute_score(analysis_results)
        }
        return results

    def extract_sunscreens(self):
        beautytap_crawler = Crawler("beautytap")

        for product_html in beautytap_crawler.crawl():
            try:
                results = self.parse_product(product_html)
                pprint(results)
            except SunscreenException as err:
                print(str(err))


def main():
    '''
    TODO: merge crawling and parsing
    TODO: handle non-200 requests
    '''
    extractor = SunscreenDataExctractor()
    extractor.extract_sunscreens()

if __name__ == '__main__':
    main()