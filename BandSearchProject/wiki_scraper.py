# pip install requests beautifulsoup4 rich regex spotipy

import requests
from bs4 import BeautifulSoup
from rich import print
from urllib.parse import urlparse
from urllib.parse import parse_qs
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

class Search:
    query = None
    iStart = None
    iEnd = None
    bands = None
    
    def __init__(self, query, result_index_start, result_index_end=None):
        self.query = query
        self.iStart = result_index_start
        self.iEnd = result_index_end if result_index_end else result_index_start + 1
        self.bands = set()

    def find(self, text):
        res = re.findall(self.query, text)
        if len(res) > 0:
            for item in res:
                self.addBandInItem(item)
                
    def addBandInItem(self, item):
        tokens = re.split(', | - | ', item)
        if len(tokens) > 0:
            possibleTerms = []
            
            for i in range(self.iStart, min(len(tokens), self.iEnd)):
                if tokens[i] != '' and tokens[i][0].isupper():
                    possibleTerms.append(tokens[i])

            possibleNames = []
            #for term in possibleTerms:

                
            for name in possibleNames:
                self.bands.add(name)

def findArtist():
    artistName = input("Enter the name of the artist: ")
    query = "{} band".format(artistName)
    url = "https://www.google.com/search?q={}".format(query)
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    bands = set()
    
    for res in extract_results(soup):
        bands = bands.union(findBandsOnPage(res['link']))

    for band in bands:
        print('pre-validation:', band)
        if scrapeSpotifyForArtist(band):
            print(band)

def findBandsOnPage(url):
    bands = set()
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pTags = soup.find_all(['p', 'title', 'a'])
    
    for tag in pTags:
        sMembers = Search('.*members', -2)
        sBand = Search('band .+', 1, 4)
        sAbout = Search('About.*', 2, 4)

        sMembers.find(tag.text)
        sBand.find(tag.text)
        sAbout.find(tag.text)
        
        bands = bands.union(sMembers.bands)
        bands = bands.union(sBand.bands)
        bands = bands.union(sAbout.bands)
        
    return bands

def extract_results(soup):
    main = soup.select_one("#main")

    res = []
    for gdiv in main.select('.g, .fP1Qef'):
        extract = extract_section(gdiv)
        if extract:
            res.append(extract)

    return res

def extract_section(gdiv):
    title = gdiv.select_one('h3')
    link = gdiv.select_one('a')
    description = gdiv.find('.BNeawe')
    title_result = title.text if title else None
    link_result = extract_href(link['href']) if link else None
    description_result = description.text if description else None
    if title_result and condition(title_result) or link_result and condition(link_result) or description_result and condition(description_result):
        return {
            'title': title_result,
            'link' : link_result,
            'description': description_result
        }
    else:
        return None

def extract_href(href):
    url = urlparse(href)
    query = parse_qs(url.query)
    if not ('q' in query and query['q'] and len(query['q']) > 0):
        return None
    return query['q'][0]

def condition(string):
    s = string.lower()
    return s.find('band') != -1 or s.find('about') != -1
    

def scrapeSpotifyForArtist(query):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="104420b75bf949718b8dec71b04482ea",
                                                           client_secret="00dfc232fa2e4da5b1cd9a7e575b5443"))

    results = sp.search(q=query, limit=50, type='artist')

    for idx, item in enumerate(results['artists']['items']):
        if item['name'] == query:
            url = item['external_urls']['spotify']
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            tags = soup.find_all(string='About')
            for tag in tags:
                print(tag.text)
            return True

    return False

#findArtist()
scrapeSpotifyForArtist('MAC')
