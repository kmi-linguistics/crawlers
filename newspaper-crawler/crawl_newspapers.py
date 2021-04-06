'''
Code author: Ritesh Kumar
For comments / requests, contact: riteshkr.kmi@gmail.com

Function: Given an URL, it collects article from 5 different newspapers - indiafacts, newslaundary (both en and hin), opindia, tfipost / rightlog and the wire. It could also do a generic collection of texts from any website.

Input: CSV file(s) with an ID and list of all URLs from where data is to be collected. All CSV files should be put in the same folder. It is assumed that each CSV file will contain URLs from different sources.

Output: The articles and associated metadata

Possible improvement: Integrate with a crawler such that only a seed URL is needed for crawling the whole website.

Library requirements: URLLIB and BeautifulSoup

'''

import csv
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup

#indiafacts
def get_indiafacts(soup):
    title = ''
    article = ''

    #content = soup.find (id='content')
    headings = soup.find_all ('div', class_='title-top')

    for heading in headings:
        title = heading.find ('h5').text

    paras = soup.find_all('p')
    for para in paras:
        para = para.text.strip().replace('\n', '')
        if para != '':
            article = article + para + '\n'

    return title, article

#newslaundary, newslaundary_hindi
def get_newslaundary(soup):
    title = ''
    article = ''

    title = soup.find(attrs={"data-testid" : "headline"}).text

    full_txt = soup.find (attrs={"data-testid" : "story-card"})
    paras = full_txt.find_all('p')

    for para in paras:
        para = para.text.strip().replace('\n', '')
        if para != '':
            article = article + para + '\n'

    return title, article

#opindia
def get_opinida (soup):
    title = ''
    article = ''

    footer_txt_1 = 'Subscribe to our NewsletterEach morning, get an email to keep updated with all the news, opinions and analysis published by OpIndia'
    footer_txt_2 = "Whether NDTV or 'The Wire', they never have to worry about funds"

    title = soup.find("h1", class_="tdb-title-text").text

    paras = soup.find_all('p')

    for para in paras:
        para = para.text

        if footer_txt_1 in para or footer_txt_2 in para:
            break
        else:
            para = para.strip().replace('\n', '')
            if para != '':
                article = article + para + '\n'

    return title, article

#tfipost.in; tfipost.com, rightlog.in
def get_tfipost(soup):
    title = ''
    article = ''

    try:
        title = soup.find ('h1', class_= "jeg_post_title").text
    except:
        title = ''
    
    full_txt = soup.find ('div', class_='content-inner')

    paras = ''
    try:
        paras = full_txt.find_all('p')
    except:
        paras = soup.find_all('p')
    
    for para in paras:
        para = para.text.strip().replace('\n', '')
        if para != '':
            article = article + para + '\n'

    return title, article

#the wire
def get_thewire(soup):
    title = ''
    article = ''

    title = soup.find ('h1', class_= "title").text
    
    paras = soup.find_all('p')
    for para in paras:
        para = para.text.strip().replace('\n', '')
        if para != '':
            article = article + para + '\n'

    return title, article

#simple generic function to get all 'p' content on the web page
def get_generic(soup):
    article = ''

    paras = soup.find_all('p')
    for para in paras:
        para = para.text.strip().replace('\n', '')
        if para != '':
            article = article + para + '\n'

    return article





title = ''
article = ''

write_dir = 'articles'
if not os.path.isdir(write_dir):
	 os.makedirs(write_dir)

for cur_file in os.listdir():
    write_file = os.path.join(write_dir, cur_file.replace('.csv', '_articles.csv'))
    source = cur_file.replace('.csv', '').lower()

    if cur_file.endswith('.csv'):
        with open (cur_file) as f_r, open (write_file, 'w') as f_w, open (write_dir + '/generic_posts.csv', 'w') as f_g:
            print ('Processing', cur_file)
            reader = csv.reader(f_r)
            writer = csv.writer (f_w)
            writerg = csv.writer(f_g)

            for row in reader:
                written = False
                if row[0] != 'source':
                    cur_id = row[0].strip()
                    cur_url = row[1].strip()

                    if cur_url.startswith('http'):
                        try:
                            url = urllib.parse.unquote(cur_url)
                            page = requests.get(url)
                            soup = BeautifulSoup(page.content, 'html.parser')
                            
                            try:
                                if 'laundry' in source:
                                    if 'newslaundry.com' in url:
                                        title, article = get_newslaundary(soup)
                                elif 'wire' in source:
                                    if 'thewire' in url:
                                        title, article = get_thewire(soup)
                                elif 'tfi' in source or 'frustrate' in source:
                                    if 'tfipost' in url or 'rightlog.in' in url:
                                        title, article = get_tfipost(soup)
                                elif 'opindia' in source:
                                    if 'bit.ly' in url or 'opindia' in url:
                                        title, article = get_opinida(soup)
                                elif 'indiafacts' in source:
                                    if 'indiafacts.co.in' in url:
                                        title, article = get_indiafacts(soup)
                                else:                               
                                    print ('None match in', source)
                                    print (url)
                                    article = get_generic(soup)
                                    title = 'NA'
                                    writerg.writerow([source, url, cur_id, title, article])
                                    written = True
                                    
                            except Exception as e:
                                print ('Exception in getting data from', source)
                                print (e)
                                article = get_generic(soup)
                                title = 'NA'
                                writerg.writerow([source, url, cur_id, title, article])
                                written = True
                                
                            if not written:
                                writer.writerow([source, url, cur_id, title, article])
                        
                        except Exception as e2:
                            print ('Exception in reading URL from', source)
                            print (url)
                            print (e2)
                    else:
                        print ('Invalid URL', cur_url)
                    
