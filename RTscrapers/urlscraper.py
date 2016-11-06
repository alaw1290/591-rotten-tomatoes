from bs4 import BeautifulSoup
import requests
import time
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = 'https://www.rottentomatoes.com/browse/dvd-all/?services=amazon;amazon_prime;fandango_now;hbo_go;itunes;netflix_iw;vudu'

def parse_movie_urls():
    '''Creates dictionary of all movies under Browse All of RT using div class = "mb-movie"
    	and storing it as {title:url}'''
    
    #create dict
    movie_list = {}

    #start selenium driver, route to url
    driver = webdriver.Firefox()
    driver.get(base_url)

    #while show more is there, keep clicking it
    elem = driver.find_element_by_xpath('//*[@id="show-more-btn"]/button')

    for i in range(100):
        currrentpage = driver.find_element_by_id("content-column")
        elem.click()
        WebDriverWait(driver, 10)
    #driver.close()
    
  

if __name__ == '__main__':
	#run scraper and print completion time
	print('Running')
	start = time.time()
	parse_movie_urls()
	end = time.time() - start
	print("Completed, time: " + str(end) + " secs")
