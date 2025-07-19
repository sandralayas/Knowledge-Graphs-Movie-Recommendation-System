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
