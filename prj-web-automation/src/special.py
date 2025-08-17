import sys
import os
import importlib
import json
import pickle
import uuid
import copy
import tqdm
import requests
import urllib.parse
from urllib.parse import urlparse, unquote
from pathlib import Path

curr_path = Path.cwd()
while curr_path.name != 'tasks' and curr_path != curr_path.parent:
    curr_path = curr_path.parent

if curr_path.name == 'tasks':
    sys.path.append(str(curr_path))
else:
    raise FileNotFoundError("Could not find 'tasks' folder in parent hierarchy.")

import numpy as np
import pandas as pd

from pack import helper as h
from pack.wiki import wikipedia_connect as wc

import requests
from bs4 import BeautifulSoup
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

def is_human(wikipedia_url):
    wikidata_id = wc.get_wikidata_id_from_wikipedia_url(wikipedia_url)
    
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = f"""
    ASK WHERE {{
      wd:{wikidata_id} wdt:P31 wd:Q5 .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result['boolean']

def get_date_of_birth(wikipedia_url):
    wikidata_id = wc.get_wikidata_id_from_wikipedia_url(wikipedia_url)
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = f"""
    SELECT ?dob WHERE {{
      wd:{wikidata_id} wdt:P569 ?dob .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    bindings = results.get('results', {}).get('bindings', [])
    if bindings:
        return bindings[0]['dob']['value']
    return None

def get_ymd_and_above_1950(raw_dob):
    try:
        dob = raw_dob[:10]
        if int(dob[:4]) >= 1950:
            return dob
        else:
            return None
    except:
        return None

# def get_name_from_link(link):
#     return link.replace('https://en.wikipedia.org/wiki/','').replace('_', ' ')

def get_name_from_link(url):
    page_name = url.replace('https://en.wikipedia.org/wiki/','')
    page_name = page_name.replace('_',' ')
    page_name = urllib.parse.unquote(page_name)
    if ':' in page_name:
        return None
    return page_name