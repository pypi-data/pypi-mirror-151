# -*- coding: utf-8 -*-
"""
Created on Fri May 20 16:07:36 2022

@author: oriol
"""

import pandas as pd
from prognosis.helper import get
from prognosis.com import topic_tickers


topics = [
 'RGDP',
 'RPRC',
 'RPUC',
 'RGFCF',
 'REXP',
 'RIMP',
 'CPI',
 'PPI',
 'GSPE',
 'GREV',
 'GBAL',
 'GDEBT',
 'EXPMON',
 'IMPMON',
 'M3YD',
 'Y10YD',
 'RETA',
 'IP',
 'OILPROD',
 'OILDEM',
 'GASODEM',
 'GASOPROD',
 'GASDEM',
 'GASPROD']


class CountryGroup():
    def __init__(self, country_list):
        self.country_list = country_list

    def get_topic(self, name):
        assert name in topics, 'Choose among %s' % str(topics)
        codes = [name+x for x in self.country_list]
        return get(codes)
