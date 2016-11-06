from bs4 import BeautifulSoup
import requests
import time
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = 'https://www.rottentomatoes.com/'
browse_url = 'https://www.rottentomatoes.com/browse/in-theaters/#'

def parse_movie_urls():
    '''Creates dictionary of all movies under Browse All of RT using div class = "mb-movie"
    	and storing it as {title:url}'''
    
    #create dict
    movie_list = {}

    # #start selenium driver
    driver = webdriver.Firefox()

    # #start selenium headless driver
    # driver = webdriver.PhantomJS()
    # driver.maximize_window()

    driver.get(browse_url)

    #clicking loop: keep expanding page till it is showing all movies
    elem = driver.find_element_by_xpath('//*[@id="show-more-btn"]/button')


    while(current_count <= total_count):
        #check current count vs total count
        soup = BeautifulSoup(driver.page_source,"lxml")
        show_count = soup.findAll('span',attrs={'id':'showing-count'})[0].text
        current_count = int(show_count.split(' ')[1])
        total_count = int(show_count.split(' ')[3])

        print(str(current_count) +  ", " + str(total_count))

        #if it has finished clicking, break out of while loop
        if(current_count == total_count):
            break

        else:
            #continue clicking
            elem.click()
            try:
                WebDriverWait(driver, 10)
            except TimeoutException:
                break

    #record each movie title and its url inside dict
    soup = BeautifulSoup(driver.page_source,"lxml")
    movies = soup.find('div', {'class' :"mb-movies"})
    for movie in movies:
        
        print(movie.find('a',{'class' : "popoverTrigger"})['href'])
        print(movie.find('h3',{'class' : "movieTitle"}).text)
        break

    driver.close()
    
  

if __name__ == '__main__':
	#run scraper and print completion time
	print('Running')
	start = time.time()
	parse_movie_urls()
	end = time.time() - start
	print("Completed, time: " + str(end) + " secs")
