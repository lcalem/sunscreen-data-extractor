import lxml.html

from pprint import pprint

from crawling_info import CRAWLING_INFO


class SunscreenException(Exception):
    pass


class Parser(object):

    def __init__(self, website):
        if website not in CRAWLING_INFO:
            raise Exception("Unsupported website %s" % website)

        self.config = CRAWLING_INFO[website]

    def parse_html(self, raw_html):
        raise NotImplementedError


class BeautytapParser(Parser):

    def __init__(self):
        Parser.__init__(self, "beautytap")

    def parse_html(self, product_html):
        '''
        html for one product page
        output should be a dict with 2 fields:
            - product_name: str
            - ingredients: list
        TODO: parse UVA information
        '''
        htmldoc = lxml.html.fromstring(product_html)

        return {
            "product_name": htmldoc.cssselect(self.config["product_name_selector"])[0].text_content(),
            "ingredients": htmldoc.cssselect(self.config["product_ingredients_selector"])[0].text_content()
        }


class SkinCharismaParser(Parser):

    def __init__(self):
        Parser.__init__(self, "skincharisma")

        self.filter_data = {
            "homosalate": ("homosalate", "organic"),
            "oxybenzone": ("oxybenzone", "organic"),
            "ethylhexyl methoxycinnamate": ("octinoxate", "organic"),
            "isoamyl p-methoxycinnamate": ("amiloxate", "organic"),
            "cinoxate": ("cinoxate", "organic"),
            "butyl methoxydibenzoylmethane": ("avobenzone", "organic"),
            "ethylhexyl salicylate": ("octisalate", "organic"),
            "bemotrizinol": ("bemotrizinol", "organic"),
            "enzacamene": ("enzacamene", "organic"),
            "aminobenzoic acid": ("paba", "organic"),
            "octocrylene": ("octocrylene", "organic"),
            "padimate-o": ("padimate-o", "organic"),
            "ethylhexyl methoxycinnamate": ("octinoxate", "organic"),
            "octyl methoxycinnamate": ("octinoxate", "organic"),
            "phenylbenzimidazole sulfonic acid": ("ensulizole", "organic"),
            "bisoctrizole methylene bis-benzotriazolyl tetramethylbutylphenol": ("tinosorb m", "organic"),
            "bis-ethylhexyloxyphenol methoxyphenyl triazine": ("tinosorb s", "organic"),
            "ecamsule": ("mexoryl sx", "organic"),
            "diethylamino hydroxybenzoyl hexyl benzoate": ("uvinul a plus", "organic"),
            "ethylhexyl triazone": ("uvinul t 150", "organic"),
            "mexoryl xl": ("mexoryl xl", "organic"),
            "zinc oxide": ("zinc oxide", "inorganic"),
            "titanium oxide": ("titanium oxide", "inorganic"),
            "parsol slx": ("polysilicone-15", "organic"),
            "polysilicone-15": ("polysilicone-15", "organic"),
            "dioxybenzone": ("dioxybenzone", "organic"),
            "meradimate menthyl anthranilate": ("eradimate menthyl anthranilate", "organic"),
            "sulisobenzone": ("sulisobenzone", "organic"),
            "trolamine salicylate": ("trolamine salicylate", "organic")
        }

    def get_filter(self, filter_name):
        '''
        from INCI uv filter name retrieve the simpler name if any
        and the filter type (organic / inorganic)
        '''
        if filter_name in self.filter_data:
            return self.filter_data[filter_name]

        else:
            print("Unknown filter %s!" % filter_name)
            return (filter_name, "organic")           # since inorganic are only zinc and titanium if we don't know it it's probably organic

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
        product_analysis = {
            "alcohol": False,
            "fragrance": False,
            "avobenzone": False,
            "octocrylene": False,
            "octinoxate": False,
            "actives": list()
        }

        filter_types = set()
        nb_ingredients = 0

        htmldoc = lxml.html.fromstring(raw_html)

        # parse all ingredients
        for ingredient_tr in htmldoc.cssselect(self.config["ingredients_table"]):
            ingredient_name = ingredient_tr.cssselect("td:nth-child(3)")[0].text_content().split("(")[0].strip().lower()
            nb_ingredients += 1

            if ingredient_name == "fragrance":
                product_analysis["fragrance"] = True

            # check labels for alcohol and uv-protection indicators
            for label in ingredient_tr.cssselect("td:nth-child(4) span.badge .badge-label"):
                if label.text_content().lower() == "alcohol":
                    product_analysis["alcohol"] = True

                if label.text_content().lower() == "uv protection":
                    uv_filter_name, uv_filter_type = self.get_filter(ingredient_name)
                    product_analysis["actives"].append(uv_filter_name)
                    filter_types.add(uv_filter_type)

        product_analysis["nb_ingredients"] = nb_ingredients

        if len(product_analysis["actives"]) == 0:
            raise SunscreenException("Not a sunscreen!")

        # add type of sunscreen
        if len(filter_types) == 2:
            product_analysis["type"] = "combo"
        else:
            product_analysis["type"] = filter_types.pop()

        # ewg safety data
        ewg_safety = list()
        for safety_level in ["safe", "moderate", "hazard", "dark-gainsboro"]:
            ewg_safety.append(int(htmldoc.cssselect(".card-body .progress .progress-bar.bg-%s" % safety_level)[0].text_content().split("%")[0]))
        product_analysis["ewg_safety"] = ewg_safety

        pprint(product_analysis)
        return product_analysis
