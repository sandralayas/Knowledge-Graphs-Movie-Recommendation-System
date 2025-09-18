# 🚀 KnowledgeGraph: Building the Brains Behind Your Movie Recommendations\! 🧠🎬

Welcome to the heart of our Movie Recommendation System\! This `KnowledgeGraph` directory is where the magic happens – we build a smart, interconnected web of movie data that helps us suggest films you'll absolutely love. Think of it as creating a "brain" that truly understands movies, actors, genres, and how people interact with them\!

## ✨ What's This All About? (Introduction)

Ever wondered why you get certain movie recommendations? Traditional systems can be a bit basic. Our Knowledge Graph component takes it to the next level by:

  * **Mapping the Movie Universe:** We turn movies, actors, directors, genres, and even *you* (the user\!) into connected pieces of information. 🧩
  * **Smarter Recommendations:** This isn't just about what similar users watched. We can ask super cool questions like, "Show me movies starring actors who also worked with **that** director and are in *my favorite* genre\!" 🤯
  * **Explainable Magic:** No more mysterious recommendations\! We can actually show *why* a movie was suggested because our data is so neatly organized. transparency FTW\! 🕵️‍♀️

**In short: This is where we create a powerful Knowledge Graph to make movie recommendations intelligent and insightful\!** 💡

## 🎯 Our Mission (Purpose and Role)

This `KnowledgeGraph` module is your go-to for:

  * **Data Whisperer:** Taking messy raw movie info (like IMDb data\! 😉) and transforming it into beautiful, graph-ready pieces. ✨
  * **Schema Architect:** Designing the blueprint for our movie universe – defining who's a `Movie` 🎥, who's an `Actor` 🎭, and how they're all linked\!
  * **Graph Populator:** Filling up our chosen database (Neo4j\!) with all this awesome, structured movie knowledge. ✍️
  * **Query Master:** Making it easy for other parts of our system to ask the graph smart questions to get those perfect movie suggestions\! ❓➡️✅

## 📂 Peek Inside (Directory Structure)

Here's how our KnowledgeGraph brain is organized:

```
KnowledgeGraph/
├── data/                    # 📊 Where our movie ingredients live!
│   ├── raw/                 # 🍚 Original, untouched data (like your MovieLens downloads)
│   └── processed/           # 🧼 Cleaned and shiny data, ready for action!
├── scripts/                 # 🐍 Our Python brainpower!
│   ├── build_graph.py       # 🏗️ The main builder – creates and fills the graph
│   ├── data_preprocessing.py# 🧹 Cleans up the raw data
│   └── query_examples.py    # 💡 (Optional) How to ask the graph smart questions
├── notebooks/               # 📓 Interactive playgrounds for testing
│   ├── graph_construction.ipynb # 🚀 See the graph being built step-by-step
│   └── kg_exploration.ipynb # 🗺️ Explore the finished graph!
├── config.py                # ⚙️ Your settings for connecting to the database, etc.
└── README.md                # 📖 You are here!
```

*(Psst\! Make sure the names above perfectly match your actual files for zero confusion\!)*

## 🛠️ Tech Toolbox (Key Technologies)

We built this intelligence using some cool tools:

  * **Python 3.x:** Our trusty coding language. 🐍
  * **Neo4j:** Our awesome **Graph Database**\! This is where all our interconnected movie knowledge lives. It's like a super-smart spiderweb for data\! 🕸️
  * **[Graph Driver/Client Library (e.g., python-neo4j)]:** The Python bridge to talk to Neo4j. 🌉
  * **pandas:** For whipping our data into shape – loading, cleaning, transforming. 🐼
  * **Web Scraping Libraries (e.g., BeautifulSoup, Requests):** Because we got some awesome movie details directly from **IMDb**\! 🌐🎬
  * *(Add any other cool libraries you used here\!)*

## 🗺️ The Movie Universe Map (Knowledge Graph Schema)

This is the blueprint of our movie brain\! We connect different types of "things" (nodes) with "how they relate" (relationships):

### Nodes (The "Things"):

  * `:Movie` 🎥: A film (e.g., *title*, *releaseYear*, *plotSummary*, *averageRating*).
  * `:Actor` 🎭: An actor (e.g., *name*, *gender*).
  * `:Director` 🎬: A director (e.g., *name*, *gender*).
  * `:Genre` 🎨: A movie category (e.g., "Action", "Comedy").
  * `:User` 👤: You\! (e.g., *userId*).

### Relationships (How They're Connected):

  * `(:Movie)-[:HAS_GENRE]->(:Genre)`: A movie *belongs to* a genre.
  * `(:Movie)-[:DIRECTED_BY]->(:Director)`: A movie *was directed by* a director.
  * `(:Actor)-[:ACTED_IN]->(:Movie)`: An actor *performed in* a movie.
  * `(:User)-[:RATED {score: <rating_value>}]->(:Movie)`: A user *gave a rating* to a movie.
  * `(:Movie)-[:SIMILAR_TO]->(:Movie)`: (Optional) Movies that are alike\!

*(Remember to update this section if your graph has unique nodes or relationships\!)*

## 🚀 Get Started\! (Setup and Usage)

Ready to build your own movie brain? Follow these easy steps:

### Prerequisites:

1.  **Python 3.x:** Make sure it's installed\! 🐍
2.  **Neo4j Database:** Get Neo4j Community Edition up and running\! It needs to be accessible on your machine.
      * [Download Neo4j Desktop/Server](https://neo4j.com/download/)
      * Start a new database instance.

### Installation:

1.  **Navigate to the root of your project:**
    ```bash
    cd <your_project_root_directory>
    ```
2.  **Install the necessary Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If you don't have a `requirements.txt` in the root, or it's specific to this folder, use: `cd KnowledgeGraph` then `pip install pandas beautifulsoup4 requests neo4j` (or your specific Neo4j driver).)*

### Configuration:

1.  Open `config.py` and update it with your Neo4j database connection details (URI, username, password). You might also need to set correct paths for your data files.

### Data Preparation:

1.  **Get Your Raw Data:**

      * Download the MovieLens Latest Small Dataset from [MovieLens](https://grouplens.org/datasets/movielens/latest/).
      * Place `movies.csv` and `ratings.csv` into the `data/raw/` directory.
      * **Crucially:** Ensure your **IMDb web scraped data** is also available and integrated or placed where your `data_preprocessing.py` can find it\! 🌐✨

2.  **Clean and Process Data:**

    ```bash
    python scripts/data_preprocessing.py
    ```

    *(This script will take the raw data, including your IMDb scrapes, clean it up, and save the processed files in `data/processed/`.)*

### Build and Populate the Graph:

1.  **Time to build the brain\!**
    ```bash
    python scripts/build_graph.py
    ```
    *(This script will connect to Neo4j, define the schema, and ingest all your processed data, including the rich IMDb details, into the graph\! Go grab a coffee, it might take a moment\! ☕)*

### Explore and Test:

1.  Open your **Neo4j Browser** (usually at `http://localhost:7474/`) to visually explore your freshly built Knowledge Graph\! See the nodes and relationships come alive\! 🎉
2.  Dive into `notebooks/kg_exploration.ipynb` (if available) for interactive Python examples on how to query and analyze your graph. Get ready to ask some smart questions\! 🧐

## 📚 Data Sources

Our amazing Knowledge Graph is built using:

  * **MovieLens Latest Small Dataset:**
      * Source: [https://grouplens.org/datasets/movielens/latest/](https://grouplens.org/datasets/movielens/latest/)
      * Files: `movies.csv` (for core movie info) and `ratings.csv` (for user interactions).
  * **IMDb Web Scraping:** We went directly to **IMDb.com** to gather richer, more detailed information about movies, actors, and directors\! This greatly enhances the depth of our graph. 🌐⭐
  * *(Add any other cool APIs or datasets you integrated\!)*

## 🔍 Dig Deeper\! (Further Exploration)

  * Want to see how this brain fits into the whole recommendation system? Check out the main project's `README.md` in the root directory\!
  * Explore the Jupyter notebooks (`notebooks/`) for a step-by-step journey through data processing and graph querying.

## ❤️ Contribute\!

Got ideas or want to make this brain even smarter? We'd love your help\! Please refer to the main project's `CONTRIBUTING.md` file in the root directory for guidelines.


To generate a comprehensive README file for the provided Python script, I'll need to analyze the code and understand its purpose and functionality.

Here's what the code does:

1.  **Imports**: It imports necessary libraries like `BeautifulSoup` for web scraping, `requests` for making HTTP requests, `pandas` for data manipulation, and others.
2.  **Global Lists**: It initializes several global lists to store scraped data: `title_list`, `year_list`, `duration_list`, `rated_list`, `actor_list`, `director_list`, `rating_list`, `genre_list`, and `comments_list`.
3.  **`movie_scrapping` function**: This is the core function that performs the web scraping.
      * It takes a URL and the global lists as arguments.
      * It uses `requests` and `BeautifulSoup` to parse the HTML content of the IMDB page.
      * **`fetch_movies`**: This nested function extracts movie titles, years, durations, and ratings from the main page. The logic for handling `year_rated_duration` seems a bit complex and might have some issues with the `try-except` block and the `while` loop.
      * **`get_sublinks`**: This function gets the individual movie page URLs (sub-links).
      * **Looping through sub-links**: It then iterates through each movie's sub-link to scrape more detailed information:
          * **`actor_list`**: Scrapes the main actor's name.
          * **`director_list`**: Scrapes the director's name.
          * **`rating_list`**: Scrapes the user rating.
          * **`genre_list`**: Scrapes the movie's genre.
          * **`comments_list`**: Navigates to the movie's review page and scrapes the review titles.
      * It handles `None` values by replacing them with `'na'`.
      * Finally, it returns all the populated lists.
4.  **Main Execution Block**:
      * It constructs a specific URL for IMDB to search for movies with a user rating between 9 and 10.
      * It calls the `movie_scrapping` function with this URL.
      * The returned lists are appended to the global lists.
      * There are commented-out sections of the code that suggest the script was intended to scrape a wider range of genres and ratings but is currently configured to run only for a specific rating range.
5.  **Output**: The script as it is doesn't write the data to a file or display it in a structured way (like a DataFrame). The scraped data is stored in global lists, and the program simply ends.

The README should clearly explain these points to a user. It should cover:

  * What the script does (its purpose).
  * What prerequisites are needed (libraries).
  * How to install the prerequisites.
  * How to run the script.
  * A brief explanation of the code's structure and what data it scrapes.
  * What to expect as output.
  * A note on the commented-out code for future development.

Based on this analysis, I will now create the README file.

````markdown
# IMDB Movie Scraper 🎬

This Python script is a web scraper designed to extract movie data from the Internet Movie Database (IMDb). It navigates through movie search results and then scrapes detailed information for each movie, including its title, year, duration, rating, director, actors, genre, and user review titles.

## ✨ Features

- **Movie Information**: Scrapes essential details like movie titles, release years, and user ratings.
- **Detailed Data**: Fetches in-depth information such as the director, main actor, and genre for each film.
- **Review Titles**: Gathers a list of review titles from each movie's dedicated review page.
- **Dynamic Scraping**: The code can be easily modified to scrape movies based on different search parameters (e.g., genre, rating range).

## 🚀 Getting Started

### Prerequisites

To run this script, you need to have Python installed on your system. You'll also need a few libraries, which you can install using `pip`.

```bash
pip install beautifulsoup4 requests pandas
````

  * `requests`: Used to make HTTP requests to the IMDB website.
  * `beautifulsoup4`: A library for parsing HTML and XML documents.
  * `pandas`: Used for data manipulation, although the current script stores data in lists, a `pandas` DataFrame would be a good next step for data organization.

### How to Run

1.  Save the code in a file named `imdb_scraper.py`.
2.  Open your terminal or command prompt.
3.  Navigate to the directory where you saved the file.
4.  Run the script using the following command:

<!-- end list -->

```bash
python imdb_scraper.py
```

## 📝 Script Overview

The main functionality is encapsulated in the `movie_scrapping` function. It performs the following steps:

1.  **Initial Scraping**: It first scrapes the main search results page to get a list of movie titles, years, durations, and content ratings.
2.  **Sub-page Navigation**: It then extracts the unique URL for each movie and loops through them.
3.  **Detailed Scraping**: For each movie's page, it scrapes the director, main actor, IMDB user rating, and genre.
4.  **Review Scraping**: It constructs a new URL to visit the movie's reviews page and scrapes the titles of the top reviews.

The scraped data is stored in various global lists (e.g., `title_list`, `director_list`). While the script currently runs and populates these lists, it doesn't output the data to a file or a more structured format like a CSV or Excel file. This is a potential area for future development.

**Note**: The script is currently configured to scrape movies with a user rating between 9 and 10. The commented-out code shows how the script can be extended to scrape other genres or a wider range of ratings.

## ⚠️ Disclaimer

Web scraping can be a sensitive activity. Please be respectful of the website's terms of service and robots.txt file. This script is intended for educational purposes and personal use only. Excessive or rapid requests can lead to your IP being temporarily blocked. Adding delays between requests (e.g., using `time.sleep()`) is a good practice to prevent this.

```
```
