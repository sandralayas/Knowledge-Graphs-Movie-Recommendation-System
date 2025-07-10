# Knowledge-Graphs-Movie-Recommendation-System
Enhance movie recommendations by utilizing knowledge graphs to capture complex relationships between movies and user preferences, providing personalized suggestions using NLP.

-----

# Knowledge Graph-Based Movie Recommendation System

This repository contains the code for a **Knowledge Graph-Based Movie Recommendation System**, designed to offer personalized movie suggestions by leveraging the rich, interconnected data within a knowledge graph. Unlike traditional recommendation systems that primarily rely on collaborative filtering or content-based methods, this system utilizes semantic relationships between movies, actors, directors, genres, and other entities to provide more accurate and contextually relevant recommendations.

-----

## Features

  * **Knowledge Graph Construction:** Builds a knowledge graph from movie metadata (e.g., IMDB, TMDb data) linking various entities like movies, actors, directors, genres, keywords, and plot summaries.
  * **Semantic Understanding:** Utilizes the graph structure to understand relationships between entities, going beyond simple keyword matching.
  * **Personalized Recommendations:** Generates movie recommendations tailored to user preferences based on their viewing history and interactions within the knowledge graph.
  * **Explainable Recommendations:** The graph-based approach can potentially offer explanations for why a particular movie was recommended, by tracing the paths and relationships in the knowledge graph.
  * **Scalable Architecture:** Designed to handle a growing database of movies and user interactions.

-----

## How It Works

The system operates in several key phases:

1.  **Data Ingestion & Preprocessing:** Movie data from various sources is collected, cleaned, and processed. This involves extracting relevant attributes and identifying unique entities.
2.  **Knowledge Graph Creation:** Entities (e.g., "Movie," "Actor," "Director," "Genre") and their relationships (e.g., "ACTED\_IN," "DIRECTED," "HAS\_GENRE") are defined. The preprocessed data is then used to populate nodes and edges within a graph database (e.g., Neo4j).
3.  **Recommendation Algorithm:**
      * **User Profiling:** User preferences are inferred from their watched movies, ratings, or explicit inputs.
      * **Graph Traversal/Querying:** Algorithms (e.g., pathfinding, similarity measures, or graph embeddings) are applied to the knowledge graph. For instance, if a user likes a movie, the system might find other movies connected through shared actors, directors, or similar genres and themes within the graph.
      * **Recommendation Generation:** A ranked list of movies is generated based on their relevance and proximity to the user's preferences within the graph.

-----

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

  * Python 3.8+
  * `pip` (Python package installer)
  * **Neo4j Desktop or Server** (for the graph database)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/sandralayas/Knowledge-Graphs-Movie-Recommendation-System.git
    cd Knowledge-Graphs-Movie-Recommendation-System
    ```

2.  **Set up a Python virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Neo4j:**

      * Download and install [Neo4j Desktop](https://www.google.com/search?q=https://neo4j.com/download/neo4j-desktop/) or [Neo4j Server](https://www.google.com/search?q=https://neo4j.com/download/neo4j-community-edition/).
      * Start a new local database instance.
      * Note down the **Bolt URL** (e.g., `bolt://localhost:7687`), **username** (default: `neo4j`), and **password** (default: `neo4j` or one you set during initial setup).

5.  **Configure Environment Variables:**
    Create a `.env` file in the project root directory and add your Neo4j credentials:

    ```
    NEO4J_URI=bolt://localhost:7687
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=your_neo4j_password
    ```

### Data Preparation

This system relies on movie metadata. You'll need to acquire and prepare your datasets.

1.  **Acquire Data:** The paper likely used datasets like IMDB, TMDb, or MovieLens. You can download these publicly available datasets. *Specify expected data file names/locations here, e.g., `data/movies.csv`, `data/credits.csv`.*
2.  **Run Data Preprocessing Scripts:**
    Navigate to the `data_processing` directory and run the scripts to clean and format the data for graph ingestion.
    ```bash
    python data_processing/clean_data.py
    python data_processing/prepare_for_graph.py
    ```
    *(Adjust script names as per actual file structure if different.)*

### Build the Knowledge Graph

Once your data is prepared, you can ingest it into Neo4j to build the knowledge graph.

1.  **Run the graph ingestion script:**
    ```bash
    python graph_builder/build_graph.py
    ```
    This script will connect to your Neo4j instance and create nodes and relationships based on your processed movie data. This might take some time depending on the dataset size.

-----

## Usage

After the knowledge graph is built, you can start using the recommendation system.

### Running Recommendations

1.  **Start the recommendation service/script:**

    ```bash
    python recommendation_engine/recommend.py
    ```

    *(This is a placeholder for your main recommendation script.)*

2.  **Interact with the system:**
    The script might prompt you for user IDs or movie preferences. Follow the on-screen instructions to get recommendations.

### Example Queries (Neo4j Browser)

You can also explore the knowledge graph directly using the Neo4j Browser (usually at `http://localhost:7474/`).

  * **Find a movie and its director:**
    ```cypher
    MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director)
    WHERE m.title = 'Inception'
    RETURN m.title, d.name
    ```
  * **Find actors in a specific movie:**
    ```cypher
    MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
    WHERE m.title = 'The Matrix'
    RETURN a.name
    ```
  * **Find movies with similar genres:**
    ```cypher
    MATCH (m1:Movie)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(m2:Movie)
    WHERE m1.title = 'Interstellar' AND m1 <> m2
    RETURN m2.title, COUNT(g) AS commonGenres
    ORDER BY commonGenres DESC
    LIMIT 10
    ```

-----

## Project Structure

```
Knowledge-Graphs-Movie-Recommendation-System/
├── .env                  # Environment variables (e.g., Neo4j credentials)
├── requirements.txt      # Python dependencies
├── README.md             # This README file
├── data/                 # Raw and processed data files
│   ├── raw/
│   │   └── movies.csv
│   │   └── credits.csv
│   └── processed/
│       └── processed_movies.csv
├── data_processing/      # Scripts for data cleaning and preparation
│   ├── clean_data.py
│   └── prepare_for_graph.py
├── graph_builder/        # Scripts for building and managing the Neo4j knowledge graph
│   ├── build_graph.py    # Main script to ingest data into Neo4j
│   └── neo4j_utils.py    # Helper functions for Neo4j connection
├── recommendation_engine/# Core recommendation algorithms
│   └── recommend.py      # Main script to run recommendations
│   └── algorithms.py     # Recommendation logic (e.g., graph traversal, similarity)
├── models/               # (Optional) Saved trained models if any ML component exists
└── utils/                # Utility functions
    └── logger.py
```

*(This structure is an example and should be adjusted to match the actual repository content.)*

-----

## Contributing

Contributions are welcome\! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

-----

## License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

-----

## Acknowledgements

  * This project is inspired by research in Knowledge Graph-based Recommendation Systems.
  * Thanks to the maintainers of Neo4j, TensorFlow/PyTorch, and other open-source libraries that made this project possible.

-----

Feel free to customize this README further with more specific details about your implementation, the exact datasets used, any unique algorithms you've developed, and results/metrics if available.
