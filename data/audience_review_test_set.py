import pickle
from bs4 import BeautifulSoup
import time
import datetime
import requests
import json

base_url_1 = 'https://www.rottentomatoes.com/user/id/'
base_url_2 = '/ratings'

dope_ass_audience_test_set = {}
path = 'project/CS591B1/data/'

def import_pickle():
    try:
        dat_movie_data = pickle.load(open(path + 'movie_keys.pkl', 'rb'))
        return dat_movie_data
    except FileNotFoundError:
        print('I want to fucking die (TM)')
        return None

movieKeys = import_pickle()
audienceFuckChads = []
audienceFuckChadData = []

cap = 100

for i in range(0, 1000000):
    url = base_url_1 + str(i) + base_url_2
    request = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(request, 'lxml')

    if(soup.find(id='error404')) is None:
       ratings = [0]*len(movieKeys)
       audienceMember = soup.find('title').text
       print(audienceMember)
       start_time = time.time()
       reviews = soup.find_all(class_='media bottom_divider')
       if(len(reviews) > 0):
           for review in reviews:
               movie = review.find(class_='media-heading').find('a')
               
               if movie.text in movieKeys:
                   stars = review.find_all(class_='glyphicon glyphicon-star')
                   if len(stars) > 2:
                       ratings[movieKeys.index(movie.text)] = 1
                   else:
                        ratings[movieKeys.index(movie.text)] = -1
           audienceFuckChads.append(audienceMember)
           audienceFuckChadData.append(ratings)
           print('Runtime: %s' %(time.time() - start_time))
    if(len(audienceFuckChads) == cap):
        break

pickle.dump(audienceFuckChadData, open('audience_test_data.pkl', 'wb'))
pickle.dump(audienceFuckChads, open('audience_names.pkl', 'wb'))
           

##dat_movie_data = import_pickle()
##dat_sweet_test_set = []
##print(dat_movie_data['Equinox'].keys())
##for x in dat_movie_data:
##    if 'release date' in dat_movie_data[x]:
##        if int(dat_movie_data[x]['release date'])%100 == 16:
##            dat_sweet_test_set.append(x)
##    

