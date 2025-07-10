# Knowledge Graph-Based Movie Recommendation System

This repository contains the code for a **Knowledge Graph-Based Movie Recommendation System**. It leverages knowledge graph embeddings to understand relationships between movies and other entities (like actors, genres) and provides personalized movie recommendations.

-----

## Features

  * **Knowledge Graph Data Processing:** Converts raw knowledge graph data (nodes and relationships in JSON format) into a structured CSV format.
  * **Knowledge Graph Embeddings (TransE):** Implements a simplified TransE-like model to learn numerical representations (embeddings) for nodes (e.g., movies, actors) and relationships within the knowledge graph. These embeddings capture semantic relationships.
  * **Similarity-Based Recommendations:** Utilizes cosine similarity on the learned embeddings to find movies similar to a given input movie.
  * **Interactive Recommendation Interface:** Provides a simple HTML/JavaScript interface within an IPython/Colab environment to input a movie title and get a ranked list of similar movie recommendations.

-----

## How It Works

The system operates in three main stages:

1.  **Data Structuring (`createDatabase.py`)**: This script takes two JSON files, one containing node information and another with relation information, and transforms them into a single CSV file. This CSV file has columns for "start node", "relation", and "end node", making the graph structure explicit in a tabular format.
2.  **Embedding Generation (`doTransE.py`)**: This script reads the relations and nodes (presumably from the same source as `createDatabase.py` or similar JSONs). It then trains a simplified TransE model to learn low-dimensional vector embeddings for each unique node and relation type. The output is a CSV file (`output.csv`) that includes the original triple information ("start node", "relation", "end node") along with their corresponding learned embeddings.
3.  **Recommendation Engine (`recomendationSystem.py`)**: This is the core recommendation logic. It loads the `output.csv` generated from the previous step, extracts movie titles and their learned embeddings. It then calculates cosine similarity between the embedding of a target movie (provided by the user) and all other movie embeddings to find the most similar movies. The results are presented through an interactive HTML interface.

-----

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

  * Python 3.x
  * `pip` (Python package installer)
  * It is assumed that you have `relations.json` and `nodes.json` files containing your knowledge graph data.

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
    pip install pandas scikit-learn numpy ipython beautifulsoup4
    ```

### Data Preparation

This system relies on `relations.json` and `nodes.json` files. Ensure these files are present in the same directory where you run the scripts, or update the file paths in the scripts accordingly.

  * `relations.json`: Should contain a list of dictionaries, where each dictionary has a key `r` representing a relation, including `startNodeElementId`, `endNodeElementId`, and `type`.
  * `nodes.json`: Should contain a list of dictionaries, where each dictionary has a key `n` representing a node, including `elementId` and `properties` (with a `name` property).

-----

## Usage

Follow these steps to run the recommendation system.

1.  **Step 1: Create a basic CSV representation of your graph (Optional but good for overview):**
    This step helps you see the basic structure of your graph data.

    ```bash
    python createDatabase.py
    ```

    This will generate an `output.csv` file with "start node", "relation", and "end node" columns.

2.  **Step 2: Generate Node and Relation Embeddings:**
    This is the crucial step where the TransE-like embeddings are trained and appended to the CSV.

    ```bash
    python doTransE.py
    ```

    This script will read `relations.json` and `nodes.json`, train the embeddings, and output an `output.csv` file that now includes "start node embedding", "relation embedding", and "end node embedding" columns.

      * **Note:** You can adjust the `embedding_dim`, `epochs`, `learning_rate`, and `margin` parameters within the `create_csv_from_json` function call in `doTransE.py`'s `if __name__ == "__main__":` block to fine-tune the embedding training.

3.  **Step 3: Run the Recommendation System Interface:**
    After `output.csv` is generated with embeddings, you can run the recommendation system. This script is designed to be run in an IPython environment (like Jupyter Notebook or Google Colab) as it uses `IPython.display.HTML` to render the interactive interface.

    To run it:

      * Open a Jupyter Notebook or Google Colab session.
      * Upload `recomendationSystem.py` and the generated `output.csv` to your session environment.
      * Execute the cells in your notebook that contain the content of `recomendationSystem.py`.

    You will see an HTML interface where you can enter a movie title, and it will display similar movie recommendations based on the learned embeddings.

-----

## Project Structure

```
Knowledge-Graphs-Movie-Recommendation-System/
├── createDatabase.py         # Script to convert JSON graph data to simple CSV
├── doTransE.py               # Script for TransE-like embedding training and outputting embeddings to CSV
├── recomendationSystem.py    # Main script for the movie recommendation engine and UI
├── relations.json            # (Assumed) Input file for relations data
├── nodes.json                # (Assumed) Input file for nodes data
├── output.csv                # Output file containing triples with embeddings (generated by doTransE.py)
└── README.md                 # This README file
└── requirements.txt          # (Not provided, but would list Python dependencies)
```

-----

## License

This project is licensed under the MIT License.

-----

## Acknowledgements

  * This project leverages fundamental concepts from knowledge graph embeddings, particularly the TransE model.
  * Built with Python, `pandas`, `scikit-learn`, and `numpy`.
  * Uses `IPython.display` for the interactive web interface.
