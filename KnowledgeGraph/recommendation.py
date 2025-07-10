# recommendation

# Neo4j

from neo4j import GraphDatabase

class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

conn = Neo4jConnection(uri="bolt://54.162.95.224:7687", user="neo4j", pwd="thickness-receptacles-evacuation")

query='''LOAD CSV WITH HEADERS FROM 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQyzVEQHwAfxmFrUoMTTZlZKeQOF8wEtTG2cu6jG-cuhO0z0I5vLkAdpljAQQVQBQwYWKd3MJDUcW1I/pub?gid=2024569982&single=true&output=csv' AS row

// Create or merge the movie nodes
MERGE (m:Movie {name: row.Name, year: row.Year, rated: row.Rated, duration: row.Duration, rating:row.Rating, sentiment:row.Sentiment})

// Create or merge the actor nodes and relationships
WITH row, m
UNWIND split(row.Actor, ':') AS actorName
MERGE (a:Actor {name: actorName})
MERGE (a)-[:ACTED_IN]->(m)

// Create or merge the director nodes and relationships
WITH row, m
MERGE (d:Director {name: row.Director})
MERGE (d)-[:DIRECTED]->(m)

// Create or merge the genre nodes and relationships
WITH row, m
MERGE (g:Genre {name: row.Genre})
MERGE (m)-[:GENRE_IS]->(g)
'''

res=conn.query(query)

query_string = '''MATCH (movie:Movie)
RETURN (movie.name)
'''
movies = conn.query(query_string)

name_html=''
for record in movies:
  temp='\n\t\t\t\t\t<option value="'+record[0]+'">'+record[0]+'</option>'
  name_html+=temp

html_content="""
<!DOCTYPE html>
<html>
<head>
    <title>Movie Database Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
        }
        h1 {
            color: #333;
        }
        label {
            font-weight: bold;
            display: block;
            margin-top: 20px;
        }
        select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: #fff;
            font-size: 16px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        h2 {
            color: #444;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: #f9f9f9;
            margin: 5px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>

<h1>Movie Database Interface</h1>
<form id="queryForm" action="/submit" method="post">
    <label for="movie1">Select First Favorite Movie:</label>
    <select id="movie1" name="movie1">
        """+name_html+"""
    </select>

    <label for="movie2">Select Second Favorite Movie:</label>
    <select id="movie2" name="movie2">
        """+name_html+"""
    </select>

    <label for="movie3">Select Third Favorite Movie:</label>
    <select id="movie3" name="movie3">
        """+name_html+"""
    </select>

    <input type="submit" value="Submit">
</form>

{% if movies %}
<div>
    <h2>Selected Movies</h2>
    <ul>
        {% for movie in movies %}
            <li>{{ movie }}</li>
        {% endfor %}
    </ul>
</div>
{% endif %}

{% if recommendations_actor_director %}
<div>
    <h2>Recommendations Based on Actor and Director</h2>
    <ul>
        {% for movie in recommendations_actor_director %}
            <li>{{ movie }}</li>
        {% endfor %}
    </ul>
</div>
{% endif %}

{% if recommendations_genre %}
<div>
    <h2>Recommendations Based on Genre and Sentiment Analysis</h2>
    <ul>
        {% for movie in recommendations_genre %}
            <li>{{ movie }}</li>
        {% endfor %}
    </ul>
</div>
{% endif %}

<script>
    function submitQuery() {
        const movie1 = document.getElementById('movie1').selectedOptions[0].textContent;
        const movie2 = document.getElementById('movie2').selectedOptions[0].textContent;
        const movie3 = document.getElementById('movie3').selectedOptions[0].textContent;
    }
</script>

</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html_content)

# my_flask_app/app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    movie1 = request.form['movie1']
    movie2 = request.form['movie2']
    movie3 = request.form['movie3']

    movies,recommendations_actor_director,recommendations_genre = recomendation_system(movie1, movie2, movie3)

    # Render template with recommendations
    return render_template('index.html',movies=movies, recommendations_actor_director=recommendations_actor_director,recommendations_genre=recommendations_genre)

def recomendation_system(movie1,movie2,movie3):
    fav_genre=[]
    fav_actor=[]
    fav_director=[]

    for movie in (movie1,movie2,movie3):
        query = "MATCH (genre:Genre)<-[s:GENRE_IS]-(movie:Movie {name: '"+movie+"'}) RETURN genre.name"
        result = conn.query(query)
        for each in result:fav_genre.append(each['genre.name'])

        query = "MATCH (actor:Actor)-[s:ACTED_IN]->(movie:Movie {name: '"+movie+"'}) RETURN actor.name"
        result = conn.query(query)
        for each in result:fav_actor.append(each['actor.name'])

        query = "MATCH (director:Director)-[s:DIRECTED]->(movie:Movie {name: '"+movie+"'}) RETURN director.name"
        result = conn.query(query)
        for each in result:fav_director.append(each['director.name'])

    fav_genre=set(fav_genre)
    fav_actor=set(fav_actor)
    fav_director=set(fav_director)

    print('\nFavorites\n')
    print('Genres :',fav_genre)
    print('Actors :',fav_actor)
    print('Directors :',fav_director)

    recommendations_actor_director=[]

    for each in fav_actor:
        query = "MATCH (actor:Actor {name: '"+each+"'})-[s:ACTED_IN]->(movie:Movie) RETURN movie.name"
        result = conn.query(query)
        for each in result:recommendations_actor_director.append(each['movie.name'])

    for each in fav_director:
        query = "MATCH (director:Director {name: '"+each+"'})-[s:DIRECTED]->(movie:Movie) RETURN movie.name"
        result = conn.query(query)
        for each in result:recommendations_actor_director.append(each['movie.name'])

    print('\nRecommendations based on actors and directors\n')
    recommendations_actor_director=set(recommendations_actor_director)
    #for each in recommendations_actor_director:print(each)

    recommendations_genre=[]
    for each in fav_genre:
        query = "MATCH (genre:Genre {name: '"+each+"'})<-[s:GENRE_IS]-(movie:Movie) RETURN movie.name"
        result = conn.query(query)
        for each in result:
          if each['movie.sentiment'] in ['Best','Good']:
            recommendations_genre.append(each['movie.name'])

    print('\nRecommendations based on genre and sentiment analysis\n')
    recommendations_genre=set(recommendations_genre[:10])
    #for each in recommendations_genre:print(each)

    return [movie1,movie2,movie3],recommendations_actor_director, recommendations_genre
if __name__ == '__main__':
    app.run(debug=True, port=8000)
