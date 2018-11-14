import urllib.parse

from crawler import Crawler
from parsers import BeautytapParser, SkinCharismaParser


def build_analysis_url(raw_ingredients):
    base_url = "https://www.skincarisma.com/products/analyze"
    base_url += "?utf8=%E2%9C%93"                   # add utf8 parameter
    base_url += "&product%5Bingredient%5D="         # product ingredients parameter

    base_url += urllib.parse.quote_plus(raw_ingredients)
    return base_url


def compute_score(analysis_results):
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


def main():
    beautytap_crawler = Crawler("beautytap")
    beautytap_parser = BeautytapParser()

    skincharisma_crawler = Crawler("skincharisma")
    skincharisma_parser = SkinCharismaParser()

    for product_html in beautytap_crawler.crawl():
        product_results = beautytap_parser.parse_html(product_html)

        analysis_url = build_analysis_url(product_results["ingredients"])
        analysis_html = skincharisma_crawler.crawl_url(analysis_url)
        analysis_results = skincharisma_parser.parse_html(analysis_html)

        results = {
            "product_name": product_results["product_name"],
            "INCI": product_results["ingredients"],
            "analysis": analysis_results
        }


def test_url():
    raw_ingredients = "Water , Homosalate , Ethylhexyl Salicylate , Dipropylene Glycol , Alcohol Denat. , Methyl Methacrylate Crosspolymer , Butyl Methoxydibenzoylmethane , Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine , Isoamyl p-Methoxycinnamate , Octocrylene , Methoxy PEG/PPG-25/4 Dimethicone , Bis-PEG/PPG-20/5 PEG/PPG-20/5 Dimethicone , Acrylates/C10-30 Alkyl Acrylate Crosspolymer , Caprylic/Capric, Triglyceride , Sodium Acrylate/Sodium Acryloyldimethyl Taurate Copolymer , Caprylyl Glycol , Fragrance , Dimethicone , Isohexadecane , Ethylhexylglycerin , Polysorbate 80 , 1,2-Hexanediol , BHT , Sodium Hydroxide , Disodium EDTA , Sorbitan Oleate , Butylene Glycol , Donkey milk , Lavandula Angustifolia (Lavender) Flower/Leaf/Stem Extract , Citrus Aurantifolia (Lime) Fruit Extract, Citrus Limon (Lemon) Fruit Extract , Calendula Officinalis Flower Extract , Propylene Glycol , Glycerin , Phenoxyethanol , Alcohol , Aloe Barbadensis Leaf Extract , Centella Asiatica Extract , Jasminum Officinale (Jasmine) Flower Extract , Sodium Hyaluronate , Chamomilla Recutita (Matricaria) Flower Water "
    analysis_url = build_analysis_url(raw_ingredients)
    ground_truth_url = "https://www.skincarisma.com/products/analyze?utf8=%E2%9C%93&product%5Bingredient%5D=Water+%2C+Homosalate+%2C+Ethylhexyl+Salicylate+%2C+Dipropylene+Glycol+%2C+Alcohol+Denat.+%2C+Methyl+Methacrylate+Crosspolymer+%2C+Butyl+Methoxydibenzoylmethane+%2C+Bis-Ethylhexyloxyphenol+Methoxyphenyl+Triazine+%2C+Isoamyl+p-Methoxycinnamate+%2C+Octocrylene+%2C+Methoxy+PEG%2FPPG-25%2F4+Dimethicone+%2C+Bis-PEG%2FPPG-20%2F5+PEG%2FPPG-20%2F5+Dimethicone+%2C+Acrylates%2FC10-30+Alkyl+Acrylate+Crosspolymer+%2C+Caprylic%2FCapric%2C+Triglyceride+%2C+Sodium+Acrylate%2FSodium+Acryloyldimethyl+Taurate+Copolymer+%2C+Caprylyl+Glycol+%2C+Fragrance+%2C+Dimethicone+%2C+Isohexadecane+%2C+Ethylhexylglycerin+%2C+Polysorbate+80+%2C+1%2C2-Hexanediol+%2C+BHT+%2C+Sodium+Hydroxide+%2C+Disodium+EDTA+%2C+Sorbitan+Oleate+%2C+Butylene+Glycol+%2C+Donkey+milk+%2C+Lavandula+Angustifolia+%28Lavender%29+Flower%2FLeaf%2FStem+Extract+%2C+Citrus+Aurantifolia+%28Lime%29+Fruit+Extract%2C+Citrus+Limon+%28Lemon%29+Fruit+Extract+%2C+Calendula+Officinalis+Flower+Extract+%2C+Propylene+Glycol+%2C+Glycerin+%2C+Phenoxyethanol+%2C+Alcohol+%2C+Aloe+Barbadensis+Leaf+Extract+%2C+Centella+Asiatica+Extract+%2C+Jasminum+Officinale+%28Jasmine%29+Flower+Extract+%2C+Sodium+Hyaluronate+%2C+Chamomilla+Recutita+%28Matricaria%29+Flower+Water+"
    assert analysis_url == ground_truth_url


if __name__ == '__main__':
    # main()

    test_url()