# import lxml

class Parser(object):

    def __init__(self):
        pass

    def parse_html(self, raw_html):
        raise NotImplementedError


class BeautytapParser(Parser):

    def parse_html(self, raw_html):
        '''
        html for one product page
        output should be a dict with 2 fields:
            - product_name: str
            - ingredients: list
        TODO: parse UVA information
        '''
        pass


class SkinCharismaParser(Parser):

    def parse_html(self, raw_html):
        '''
        parse the analysis results for one product ingredient list
        output: {
            alcohol: bool,
            fragrance: bool,
            actives: [str],          # list of UV filters
            type: str,               # combo / organic / inorganic
            ewg_safety: [int, int, int, int],       # [low_risk, medium_risk, high_risk, unknown]
            avobenzone: bool,
            octocrylene: bool,
            octinoxate: bool
        }
        '''
        pass