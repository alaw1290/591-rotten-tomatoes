
# coding: utf-8

# In[223]:

from bs4 import BeautifulSoup
from selenium import webdriver
import statsmodels.api as sm
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
import json
import datetime
import pickle

#sequence to initiate webpage for scraping
#change url for chromedriver accordingly
driver = webdriver.Chrome("/Users/aditi/Desktop/cs591B/github/CS591B1/RTscrapers/chromedriver")
movie = {}
error = 0

def scraper(title, url):
#     url = "https://www.rottentomatoes.com/m/bowfinger"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    try:
        #for All Critics
        movie[title]["all critics"] = {}
        all_critics = soup.find("div", { "id" : "all-critics-numbers" })

        #tomatometer score
        movie[title]["all critics"]["tomatometer"] = int(all_critics.find("a", { "id" : 'tomato_meter_link' }).text.strip().replace("%", ""))

        all_critics_2 = all_critics.find("div", { "id" : "scoreStats" })

        #all_critics_average_rating
        movie[title]["all critics"]["average_rating"] = float(all_critics_2.find("div", { "class" : 'superPageFontColor' }).text.split("\n")[2].strip().replace("/10", ""))
        all_critics_info = all_critics_2.findAll("span", { "class" : '' })

        #all_critics_reviews_counted
        movie[title]["all critics"]["reviews_counted"] = int(all_critics_info[0].text)


        #all_critics_fresh
        movie[title]["all critics"]["fresh"] = int(all_critics_info[1].text)

        #all_critics_rotten
        movie[title]["all critics"]["rotten"] = int(all_critics_info[2].text)


        #for Top Critics
        find_top = soup.find("div", { "id" : "top-critics-numbers" }).text
        if "Not Available" in find_top:
            pass
        else:
            movie[title]["top critics"] = {}
            top_critics = soup.find("div", { "id" : "top-critics-numbers" })

            #tomatometer score
            movie[title]["top critics"]["tomatometer"] = int(top_critics.find("a", { "id" : 'tomato_meter_link' }).text.strip().replace("%", ""))

            top_critics_2 = top_critics.find("div", { "id" : "scoreStats" })

            #top_critics_average_rating
            movie[title]["top critics"]["average_rating"] = float(top_critics_2.find("div", { "class" : 'superPageFontColor' }).text.split("\n")[2].strip().replace("/10", ""))

            top_critics_info = top_critics_2.findAll("span", { "class" : '' })

            #top_critics_reviews_counted
            movie[title]["top critics"]["reviews_counted"] = int(top_critics_info[0].text)

            #top_critics_fresh
            movie[title]["top critics"]["fresh"] = int(top_critics_info[1].text)  

            #top_critics_rotten
            movie[title]["top critics"]["rotten"] = int(top_critics_info[2].text)


        #audience score
        movie[title]["audience"] = {}
        movie[title]["audience"]["score"] = int(soup.find("div", { "class" : "meter-value" }).text.split("\n")[1].replace("%",""))

        """Consider using a strip() first before split"""
        audience_info =  soup.find("div", { "class" : 'audience-info hidden-xs superPageFontColor' }).text.split("\n")

        #audience_average_rating
        movie[title]["audience"]["average rating"] = float(audience_info[3].strip().replace("/5",""))
        #audience_number_of_ratings
        movie[title]["audience"]["number of ratings"] = int(audience_info[7].strip().replace(",", ""))

        #Number of Videos
        find_videos = soup.find("div", { "class" : 'clickForMore viewMoreVideos' })
        if find_videos is None:
            pass
        else:
            movie[title]["number of videos"] = int(soup.find("div", { "class" : 'clickForMore viewMoreVideos' }).text.strip().split(" ")[3].replace("(","").replace(")",""))
        
        #Number of Photos
        find_photos = soup.find("div", { "class" : 'clickForMore viewMorePhotos' })
        if find_photos is None:
            pass
        else:
            movie[title]["number of photos"] = int(soup.find("div", { "class" : 'clickForMore viewMorePhotos' }).text.strip().split(" ")[3].replace("(","").replace(")",""))
        
        
        #Movie Info
        movie_info = soup.find("div", { "class" : 'info' })
        movie_info_list = movie_info.findAll("div")
        
        for i in range(0, len(movie_info_list)):
            #Age Rating
            if "Rating:" in str(movie_info_list[i]):
                movie[title]["age rating"] = movie_info_list[i+1].text.split(" ")[0]
                
            #Genres
            if "Genre:" in str(movie_info_list[i]):
                list_of_genres = movie_info_list[i+1].text.split(",")
                movie[title]["number of genres"] = len(list_of_genres)
                genres = []
                for j in list_of_genres:
                    string1 = str(j.strip())
                    genres.append(string1)
                movie[title]["genres"] = genres
            
            #Directors
            if "Directed By:" in str(movie_info_list[i]):
                list_of_movie_directors = movie_info_list[i+1].text.strip().split(",")
                movie[title]["number of directors"] = len(list_of_movie_directors)
                directors = [] 
                for j in list_of_movie_directors:
                    string1 = str(j.strip())
                    directors.append(string1)
                movie[title]["directors"] = directors
            
            #Writers
            if "Written By:" in str(movie_info_list[i]):     
                list_of_movie_writers = movie_info_list[i+1].text.strip().split(",")
                movie[title]["number of writers"] = len(list_of_movie_writers)
                writers = [] 
                for j in list_of_movie_writers:
                    string1 = str(j.strip())
                    writers.append(string1)
                movie[title]["writers"] = writers
            
            #Release Date
            if "In Theaters:" in str(movie_info_list[i]): 
                #Relase Date and Type
                release_info = movie_info_list[i+1].text.strip().split("\n")

                #Date in Theatres
                string_of_release_date = str(release_info[0].replace(",",""))
                movie[title]["release date"] = datetime.datetime.strptime(string_of_release_date, '%b %d %Y').strftime('%d%m%y')

                #Release Type
                if release_info[1] is not None:
                    movie[title]["release type"] = release_info[1].strip()

            #DVD Release Date
            if "On DVD:" in str(movie_info_list[i]):    
                string_of_DVD_date = str(movie_info_list[i+1].text.strip().replace(",",""))
                movie[title]["DVD date"] = datetime.datetime.strptime(string_of_DVD_date, '%b %d %Y').strftime('%d%m%y')
            
            #Box Office
            if "Box Office:" in str(movie_info_list[i]):    
                movie[title]["box office revenue"] = float(movie_info_list[i+1].text.replace(",","").replace("$",""))

            #Runtime
            if "Runtime:" in str(movie_info_list[i]):    
                movie[title]["runtime"] = int(movie_info_list[i+1].text.strip().replace(" minutes",""))
            
            #Studio
            if "Studio:" in str(movie_info_list[i]):    
                movie[title]["studio"] = str(movie_info_list[i+1].text.strip())            
                

        #Cast Info
        cast_info = soup.find("div", { "class" : 'castSection '})
        if cast_info is None:
            movie[title]["number of cast"] = 0
        else:
            cast = []
            counter = 0

            for i in cast_info.findAll("a", { "class" : 'unstyled articleLink'}):
                string1 = i.text.strip()
                if string1 == "Show More Cast":
                    continue
                else:
                    cast.append(string1)
                    counter += 1
            movie[title]["cast"] = cast
            movie[title]["number of cast"] = counter
    
    except Exception as e:
        print(title)
        #movie.pop(title, None)
        
def main_scraper():
    base_url = 'https://www.rottentomatoes.com'
    
    with open('movie_urls.txt') as data_file:    
        data = json.load(data_file)
    
    count = 0
    for title in data:
        movie[str(title)] = {}
        add_on = data[str(title)]
        url = base_url + add_on
        scraper(title, url)
            
main_scraper()

#save all info in pickle format - binary
with open('movie_data.pkl', 'wb') as f:
    pickle.dump(movie, f, pickle.HIGHEST_PROTOCOL)      
        
        
        
# import pickle

# with open('movie_data.pkl', 'wb') as f:
#     pickle.dump(movie, f, pickle.HIGHEST_PROTOCOL)      
# with open('movie_data.pkl', 'rb') as f:
#     return pickle.load(f)
        

