import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from IPython.display import FileLink
import re
import time
from os import replace
# from neo4j import GraphDatabase


data=pd.read_csv('/content/drive/MyDrive/sample_data (1).csv')
title_list=list(data['Name'])
year_list=list(data['Year'])
duration_list=list(data['Duration'])
rated_list=list(data['Rated'])
actor_list=list(data['Actor'])
director_list=list(data['Director'])
rating_list=list(data['Rating'])
genre_list=list(data['Genre'])
comments_list=list(data['Comments'])
nlp_score=list(data['NLP Score'])
sentiment_list=list(data['Sentiment'])
data.head()

data.to_csv('sample_data.csv', index=False)
data = pd.read_csv('sample_data.csv')
print(data.shape)
data = data.drop_duplicates(subset=['Name'], keep='last')
data.to_csv('sample_data.csv', index=False)
print(data.shape)

# download csv
FileLink('sample_data.csv')

# from google.colab import files
# files.download('sample_data.csv')


G = nx.from_pandas_edgelist(data, 'Name', 'Actor')

genre_edges = list(zip(data['Name'], data['Genre']))
G.add_edges_from(genre_edges)

# year_edges = list(zip(data['Name'], data['Year']))
# G.add_edges_from(year_edges)

# rated_edges = list(zip(data['Name'], data['Rated']))
# G.add_edges_from(rated_edges)

# duration_edges = list(zip(data['Name'], data['Duration']))
# G.add_edges_from(duration_edges)

# rating_edges = list(zip(data['Name'], data['Rating']))
# G.add_edges_from(rating_edges)

# actor_edges = list(zip(data['Name'], data['Actor']))
# G.add_edges_from(actor_edges)

director_edges = list(zip(data['Name'], data['Director']))
G.add_edges_from(director_edges)

# comments_edges = list(zip(data['Name'], data['Comments']))
# G.add_edges_from(comments_edges)

# nlp_edges = list(zip(data['Name'], data['NLP Score']))
# G.add_edges_from(nlp_edges)

# sentiment_edges = list(zip(data['Name'], data['Sentiment']))
# G.add_edges_from(sentiment_edges)