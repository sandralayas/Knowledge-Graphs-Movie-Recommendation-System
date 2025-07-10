# NLP

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from IPython.display import FileLink
import re
import time
from os import replace
# from neo4j import GraphDatabase

from scrapping import comments_list

nlp_score=[]
sentiment_list=[]

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

for movie in comments_list:
  nlp=0

  vgood=0
  good=0
  bad=0
  vbad=0

  for comment in movie[:20]:
    blob=TextBlob(comment)
    score=blob.sentiment.polarity

    nlp+=score

    if score>0:
      if score>0.5:vgood+=1
      else:good+=1
    elif score<0:
      if score<-0.5:vbad+=1
      else:bad+=1

  if len(movie)==0:divide=1
  else:divide=len(movie)

  nlp_score.append(nlp/divide)

  sentiment=(vbad,bad,good,vgood)
  if max(sentiment)==0:
    sentiment_list.append('Neutral')
  else:
    max_sentiment=max(sentiment)
    if max_sentiment==vgood:sentiment_list.append('Best')
    elif max_sentiment==good:sentiment_list.append('Good')
    elif max_sentiment==bad:sentiment_list.append('Bad')
    else:sentiment_list.append('Worst')
