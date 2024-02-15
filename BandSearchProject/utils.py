import requests
from bs4 import BeautifulSoup
import numpy as np

def scrape_url_for_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('p')
    texts = [tag.text for tag in tags]
    return ' '.join(texts)

def form_input(text, artist, band_list):
    x_out = np.zeros(1000)
    y_out = np.zeros(100)
    
    for i in range(len(text)):
        if i < 1000 - len(artist):
            x_out[i] = ord(text[i])

    start_index = min(len(text), 1000 - len(artist))
    for i in range(len(artist)):
        x_out[start_index + i] = ord(artist[i])

    for i in range(len(band_list)):
        y_out[i] = ord(band_list[i])
        
    return(x_out, y_out)
    
