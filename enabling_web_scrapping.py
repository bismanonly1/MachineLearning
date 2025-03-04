#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import sys
import requests
import re
from bs4 import BeautifulSoup  

def get_page():
    global url
    
    url = input("Enter url of a medium article: ")  
    
    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid website, or make sure it is a medium article')
        sys.exit(1)

    try:
        res = requests.get(url)
    except requests.RequestExcption as e:
        print(f"An errorocurred: {e}")
        return None

    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub(r'\<(.*?)\>', '', text)
    return text

def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'
    
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)
    
    print(f'File saved in directory {fname}')

if __name__ == '__main__':
    text = collect_text(get_page())
    save_file(text)
    


# In[ ]:




