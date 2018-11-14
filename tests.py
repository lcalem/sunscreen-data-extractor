import requests

from main import SunscreenDataExctractor


def dict_equal(d1, d2):
    '''
    simple dict equality check without recursivity which checks the exact equivalence of the values
    '''
    assert set(d1.keys()) == set(d2.keys()), "Keys are diffrent"
    for k, v in d1.items():
        assert d2[k] == v, "Key %s is different (%s vs %s)" % (k, d1[k], d2[k])
    return True


def test_url():
    raw_ingredients = "Water , Homosalate , Ethylhexyl Salicylate , Dipropylene Glycol , Alcohol Denat. , Methyl Methacrylate Crosspolymer , Butyl Methoxydibenzoylmethane , Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine , Isoamyl p-Methoxycinnamate , Octocrylene , Methoxy PEG/PPG-25/4 Dimethicone , Bis-PEG/PPG-20/5 PEG/PPG-20/5 Dimethicone , Acrylates/C10-30 Alkyl Acrylate Crosspolymer , Caprylic/Capric, Triglyceride , Sodium Acrylate/Sodium Acryloyldimethyl Taurate Copolymer , Caprylyl Glycol , Fragrance , Dimethicone , Isohexadecane , Ethylhexylglycerin , Polysorbate 80 , 1,2-Hexanediol , BHT , Sodium Hydroxide , Disodium EDTA , Sorbitan Oleate , Butylene Glycol , Donkey milk , Lavandula Angustifolia (Lavender) Flower/Leaf/Stem Extract , Citrus Aurantifolia (Lime) Fruit Extract, Citrus Limon (Lemon) Fruit Extract , Calendula Officinalis Flower Extract , Propylene Glycol , Glycerin , Phenoxyethanol , Alcohol , Aloe Barbadensis Leaf Extract , Centella Asiatica Extract , Jasminum Officinale (Jasmine) Flower Extract , Sodium Hyaluronate , Chamomilla Recutita (Matricaria) Flower Water "
    analysis_url = SunscreenDataExctractor().build_analysis_url(raw_ingredients)
    ground_truth_url = "https://www.skincarisma.com/products/analyze?utf8=%E2%9C%93&product%5Bingredient%5D=Water+%2C+Homosalate+%2C+Ethylhexyl+Salicylate+%2C+Dipropylene+Glycol+%2C+Alcohol+Denat.+%2C+Methyl+Methacrylate+Crosspolymer+%2C+Butyl+Methoxydibenzoylmethane+%2C+Bis-Ethylhexyloxyphenol+Methoxyphenyl+Triazine+%2C+Isoamyl+p-Methoxycinnamate+%2C+Octocrylene+%2C+Methoxy+PEG%2FPPG-25%2F4+Dimethicone+%2C+Bis-PEG%2FPPG-20%2F5+PEG%2FPPG-20%2F5+Dimethicone+%2C+Acrylates%2FC10-30+Alkyl+Acrylate+Crosspolymer+%2C+Caprylic%2FCapric%2C+Triglyceride+%2C+Sodium+Acrylate%2FSodium+Acryloyldimethyl+Taurate+Copolymer+%2C+Caprylyl+Glycol+%2C+Fragrance+%2C+Dimethicone+%2C+Isohexadecane+%2C+Ethylhexylglycerin+%2C+Polysorbate+80+%2C+1%2C2-Hexanediol+%2C+BHT+%2C+Sodium+Hydroxide+%2C+Disodium+EDTA+%2C+Sorbitan+Oleate+%2C+Butylene+Glycol+%2C+Donkey+milk+%2C+Lavandula+Angustifolia+%28Lavender%29+Flower%2FLeaf%2FStem+Extract+%2C+Citrus+Aurantifolia+%28Lime%29+Fruit+Extract%2C+Citrus+Limon+%28Lemon%29+Fruit+Extract+%2C+Calendula+Officinalis+Flower+Extract+%2C+Propylene+Glycol+%2C+Glycerin+%2C+Phenoxyethanol+%2C+Alcohol+%2C+Aloe+Barbadensis+Leaf+Extract+%2C+Centella+Asiatica+Extract+%2C+Jasminum+Officinale+%28Jasmine%29+Flower+Extract+%2C+Sodium+Hyaluronate+%2C+Chamomilla+Recutita+%28Matricaria%29+Flower+Water+"
    assert analysis_url == ground_truth_url


def test_product():
    '''
    TODO: should load a dump from the html
    '''
    test_url = "https://beautytap.com/product/a-pieu-pure-block-aqua-sun-gel/"
    expected_analysis = {
        'actives': ['octinoxate',
                    'octocrylene',
                    'octisalate',
                    'avobenzone',
                    'tinosorb s'],
        'alcohol': True,
        'avobenzone': True,
        'ewg_safety': [79, 11, 4, 7],
        'fragrance': True,
        'nb_ingredients': 28,
        'octinoxate': True,
        'octocrylene': True,
        'type': 'organic'
    }

    extractor = SunscreenDataExctractor()
    product_html = requests.get(test_url).text
    product_results = extractor.parse_product(product_html)

    assert len(product_results["INCI"]) > 0
    assert product_results["product_name"] == "A’Pieu Pure Block Aqua Sun Gel 50ml"
    assert product_results["score40"] > 0

    from pprint import pprint
    pprint(product_results["analysis"])
    assert dict_equal(product_results["analysis"], expected_analysis)

    
