from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from IPython.display import FileLink
import re
import time
from os import replace
# from neo4j import GraphDatabase

title_list=[]
year_list=[]
duration_list=[]
rated_list=[]
actor_list=[]
director_list=[]
rating_list=[]
genre_list=[]
comments_list=[]

def movie_scrapping(url,title_list,year_list,duration_list,rated_list,actor_list,director_list,rating_list,genre_list,comments_list):#,nlp_score,sentiment_list):
  HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
  page = requests.get(url, headers=HEADERS)
  soup = BeautifulSoup(page.content, "html.parser")

  def fetch_movies(soup,title_list,year_list,duration_list,rated_list):
    for i in soup.find_all('a',class_="ipc-title-link-wrapper"):
      title=i.get_text(strip=True)
      title=title[title.index('.')+2:]
      title_list.append(title)

    year_rated_duration=(soup.find_all('span',class_="sc-b189961a-8 kLaxqf dli-title-metadata-item"))

    count=0
    while len(year_list)!=len(title_list):
      try:
        year=year_rated_duration[count].get_text(strip=True)
        duartion=year_rated_duration[count+1].get_text(strip=True)
        rated=year_rated_duration[count+2].get_text(strip=True)

        if year.isnumeric()==True and duartion.isnumeric()==True:
          year_list.append(year)
          duration_list.append('na')
          rated_list.append('na')
          count+=1
        elif year.isnumeric()==True and duartion.isnumeric()!=True:
          for each in (year,duartion,rated):
            if len(str(each))==4:year_list.append(year)
            if 'h' in duartion:duration_list.append(duartion)
            if rated in ['Aprroved','NC-17','TV-MA','G','PG','PG-13','R','Not Rated']:rated_list.append(each)
          count+=3
      except:pass

    # for each in range(len(year_rated_duration)-2):
    #   year=year_rated_duration[each].get_text(strip=True)
    #   duartion=year_rated_duration[each+1].get_text(strip=True)
    #   rated=year_rated_duration[each+2].get_text(strip=True)

    #   if year.isnumeric()==False:pass
    #   else:
    #     year_list.append(year)
    #     if 'h' and 'm' in duartion:duration_list.append(duartion)
    #     else:duration_list.append(None)
    #     if rated in ['Aprroved','NC-17','TV-MA','G','PG','PG-13','R']:rated_list.append(rated)
    #     else:rated_list.append(None)

    return title_list,year_list,duration_list,rated_list

  title_list,year_list,duration_list,rated_list=fetch_movies(soup,title_list,year_list,duration_list,rated_list)

  sub_links=[]

  def get_sublinks(soup,sub_links):
    movies_list=soup.find_all('a',class_='ipc-title-link-wrapper')
    for each in movies_list:
      sub_links.append(each.get('href'))
    return sub_links

  sub_links=get_sublinks(soup,sub_links)

  rooturl='https://www.imdb.com'

  for sub in sub_links:
    url=rooturl+sub
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")

    cast=soup.find('a',class_='sc-bfec09a1-1 gCQkeh')
    actor_list.append(cast.get_text(strip=True))

    director=soup.find('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
    director_list.append(director.get_text(strip=True))

    rating=soup.find('span',class_="sc-eb51e184-1 cxhhrI")
    if rating==None:rating_list.append(None)
    else:rating_list.append(rating.get_text(strip=True))

    genre=soup.find('span',class_="ipc-chip__text")
    genre_list.append(genre.get_text(strip=True))

    index=(rooturl+sub).index('?ref')

    comment_url=(rooturl+sub)[:index]+'reviews?ref_=tt_urv'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    page1 = requests.get(comment_url, headers=HEADERS)
    soup1 = BeautifulSoup(page1.content, "html.parser")

    temp=[]
    for comment in soup1.find_all('a',class_='title'):
      temp.append(comment.get_text(strip=True))

    comments_list.append(temp)

  lists=[title_list,year_list,duration_list,rated_list,rating_list,director_list]
  for col in lists:
    for row in col:
      if row==None:col[int(col.index(row))]='na'

  return title_list,year_list,duration_list,rated_list,actor_list,director_list,rating_list,genre_list,comments_list#,nlp_score,sentiment_list


# genre=('action','adventure','animation','biography','comedy','crime')#,'documentary','drama','family','fantasy','film-Noir','game-Show','history','horror','music','musical','mystery','news','reality-TV','romance','sci-Fi','short','sport','talk-Show','thriller','war','western')
# for each in genre:
#   url='https://www.imdb.com/search/title/?title_type=feature&genres='+each

# x=0
# while x<=10:
url='https://www.imdb.com/search/title/?title_type=feature&user_rating='+str(10)+','+str(9)#+str(i/100)+','+str((i/100)-0.50)

f1,f2,f3,f4,f5,f6,f7,f8,f9=movie_scrapping(url,title_list,year_list,duration_list,rated_list,actor_list,director_list,rating_list,genre_list,comments_list)# ,nlp_score,sentiment_list)
title_list+=f1
year_list+=f2
duration_list+=f3
rated_list+=f4
actor_list+=f5
director_list+=f6
rating_list+=f7
genre_list+=f8
comments_list+=f9

  # x+=0.1

# for j in range(10):
#   for i in range(10)
#     url='https://www.imdb.com/search/title/?title_type=feature&user_rating='+str(i)+','+str(i-1)#+str(i/100)+','+str((i/100)-0.50)

#     f1,f2,f3,f4,f5,f6,f7,f8,f9=movie_scrapping(url,title_list,year_list,duration_list,rated_list,actor_list,director_list,rating_list,genre_list,comments_list)# ,nlp_score,sentiment_list)
#     title_list+=f1
#     year_list+=f2
#     duration_list+=f3
#     rated_list+=f4
#     actor_list+=f5
#     director_list+=f6
#     rating_list+=f7
#     genre_list+=f8
#     comments_list+=f9
#     # nlp_score+=f10
#     # sentiment_list+=f11