
# coding: utf-8

# In[ ]:




# In[14]:

from bs4 import BeautifulSoup
from selenium import webdriver
import statsmodels.api as sm
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )


#sequence to initiate webpage for scraping
driver = webdriver.Chrome("/Users/aditi/CS591B/chromedriver")
url = "https://www.rottentomatoes.com/m/star_trek_beyond"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")


# In[94]:

#for All Critics

all_critics = soup.find("div", { "id" : "all-critics-numbers" })
all_critics_tomatometer = int(str(all_critics.find("a", { "id" : 'tomato_meter_link' }).text)[2:4])
print(all_critics_tomatometer)


all_critics_2 = all_critics.find("div", { "id" : "scoreStats" })

# all_critics_average_rating
all_critics_average_rating = float((str(all_critics_2.find("div", { "class" : 'superPageFontColor' }).text))[50:53])
print(all_critics_average_rating)


count = 0
for x in all_critics_2.findAll("span", { "class" : '' }):
    if count == 0:
        # all_critics_reviews_counted
        all_critics_reviews_counted = int(x.text)
        count += 1
    elif count == 1:
        # all_critics_fresh
        all_critics_fresh = int(x.text)
        count += 1
    else:
        # all_critics_rotten
        all_critics_rotten = int(x.text)
        
        
print(all_critics_reviews_counted)
print(all_critics_fresh)
print(all_critics_rotten)


# In[95]:

#for Top Critics

all_critics = soup.find("div", { "id" : "top-critics-numbers" })
all_critics_tomatometer = int(str(all_critics.find("a", { "id" : 'tomato_meter_link' }).text)[2:4])
print(all_critics_tomatometer)


all_critics_2 = all_critics.find("div", { "id" : "scoreStats" })

# all_critics_average_rating
all_critics_average_rating = float((str(all_critics_2.find("div", { "class" : 'superPageFontColor' }).text))[50:53])
print(all_critics_average_rating)


count = 0
for x in all_critics_2.findAll("span", { "class" : '' }):
    if count == 0:
        # all_critics_reviews_counted
        all_critics_reviews_counted = int(x.text)
        count += 1
    elif count == 1:
        # all_critics_fresh
        all_critics_fresh = int(x.text)
        count += 1
    else:
        # all_critics_rotten
        all_critics_rotten = int(x.text)
        
        
print(all_critics_reviews_counted)
print(all_critics_fresh)
print(all_critics_rotten)

