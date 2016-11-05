from bs4 import BeautifulSoup
import requests
import time
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = 'https://www.rottentomatoes.com/browse/dvd-all/?services=amazon;amazon_prime;fandango_now;hbo_go;itunes;netflix_iw;vudu'

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'

def parse_movie_urls():
    '''Creates dictionary of all movies under Browse All of RT using div class = "mb-movie"
    	and storing it as {title:url}'''
    
    #create dict
    movie_list = {}

    #start selenium test
    headers = {'User-Agent' : user_agent}
    response = requests.get(base_url, headers=headers)
    html = response.text.encode('utf-8')
    soup = BeautifulSoup(html,"lxml")
    return soup

if __name__ == '__main__':
	#run scraper and print completion time
	print('Running')
	start = time.time()
	test = parse_movie_urls()
	end = time.time() - start
	print("Completed, time: " + str(end) + " secs")
