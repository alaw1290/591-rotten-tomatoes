
# coding: utf-8

# In[ ]:




# In[2]:

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


# In[127]:

#for All Critics

all_critics = soup.find("div", { "id" : "all-critics-numbers" })
all_critics_tomatometer = int(str(all_critics.find("a", { "id" : 'tomato_meter_link' }).text)[2:4])

all_critics_2 = all_critics.find("div", { "id" : "scoreStats" })

#all_critics_average_rating
all_critics_average_rating = float((str(all_critics_2.find("div", { "class" : 'superPageFontColor' }).text))[50:53])

all_critics_info = all_critics_2.findAll("span", { "class" : '' })

#all_critics_reviews_counted
all_critics_reviews_counted = int(all_critics_info[0].text)

#all_critics_fresh
all_critics_fresh = int(all_critics_info[1].text)  

#all_critics_rotten
all_critics_rotten = int(all_critics_info[2].text)
    


# In[128]:

#for Top Critics

top_critics = soup.find("div", { "id" : "top-critics-numbers" })
top_critics_tomatometer = int(str(top_critics.find("a", { "id" : 'tomato_meter_link' }).text)[2:4])

top_critics_2 = all_critics.find("div", { "id" : "scoreStats" })

#all_critics_average_rating
top_critics_average_rating = float((str(top_critics_2.find("div", { "class" : 'superPageFontColor' }).text))[50:53])
        
top_critics_info = top_critics_2.findAll("span", { "class" : '' })

#all_critics_reviews_counted
top_critics_reviews_counted = int(top_critics_info[0].text)

#all_critics_fresh
top_critics_fresh = int(top_critics_info[1].text)  

#all_critics_rotten
top_critics_rotten = int(top_critics_info[2].text)
        


# In[61]:

#audience score
audience_score = int(soup.find("div", { "class" : "meter-value" }).text.split("\n")[1][0:2])

"""Consider using a strip() first before split"""
audience_info =  soup.find("div", { "class" : 'audience-info hidden-xs superPageFontColor' }).text.split("\n")
#audience_average_rating
audience_average_rating = float(audience_info[3].strip()[0:3])
#audience_number_of_ratings
audience_number_of_ratings = int(audience_info[7].strip().replace(",", ""))


# In[62]:

#Number of Photos and Videos
number_of_videos = int(soup.find("div", { "class" : 'clickForMore viewMoreVideos' }).text.strip()[-3:-1])
number_of_photos = int(soup.find("div", { "class" : 'clickForMore viewMorePhotos' }).text.strip()[-3:-1])


# In[129]:

#Movie Info
movie_info = soup.findAll("div", { "class" : 'col col-sm-19 col-xs-14 text-left' })

#Rating
movie_rating = movie_info[0].text.split(" ")[0]

#Genres - with dictionary present
dict1 = {} 
list_of_genres = movie_info[1].text.split(",")
number_of_genres = len(list_of_genres)
for i in list_of_genres:
    string1 = str(i.strip())
    dict1[string1] = 1


import datetime
#Date On DVD
string_of_DVD_date = str(movie_info[2].text.strip().replace(",",""))
movie_DVD_date = datetime.datetime.strptime(string_of_DVD_date, '%b %d %Y').strftime('%d%m%y')

#Box Office Revenue
movie_box_office_revenue = float(movie_info[3].text.replace(",","").replace("$",""))

#Runtime
movie_runtime = int(movie_info[4].text.strip().replace(" minutes",""))

#Studio
movie_studio = str(movie_info[5].text.strip())



# In[162]:

movie_info_2 = soup.findAll("div", { "class" : 'col-sm-19 col-xs-14 text-left' })

#Movie_director
movie_director = str(movie_info_2[0].text.strip())

#Movie Writer
list_of_movie_writers = movie_info_2[1].text.strip().replace(" ","").replace("\n","").split(",")
number_of_writers = len(list_of_movie_writers)
dict2 = {} 
for i in range(0,len(list_of_movie_writers)):
    string1 = "movie_writer_" + str(i)
    dict1[string1] = list_of_movie_writers[i]

#Relase Date and Type
release_info = movie_info_2[2].text.strip().split("\n")

#Date in Theatres
string_of_release_date = str(release_info[0].replace(",",""))
movie_release_date = datetime.datetime.strptime(string_of_release_date, '%b %d %Y').strftime('%d%m%y')

#Release Type
movie_release_type = release_info[1].strip()


# In[ ]:

#Cast List



















