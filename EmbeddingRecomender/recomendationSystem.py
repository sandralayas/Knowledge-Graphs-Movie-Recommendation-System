import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import HTML, display
import json  # To safely parse the string embeddings

# Load the output.csv file
try:
    movie_df = pd.read_csv('output.csv')
except FileNotFoundError:
    print("Error: 'output.csv' not found. Please make sure the file is in the same directory as your Colab notebook or provide the correct path.")
    exit()

# Assuming your CSV has columns named 'start node' and 'start node embedding'
# You might need to adjust these names based on your actual CSV structure
if 'start node' not in movie_df.columns or 'start node embedding' not in movie_df.columns:
    print("Error: The CSV file must contain columns named 'start node' and 'start node embedding'. Please check your file.")
    exit()

# Rename columns for clarity
movie_df.rename(columns={'start node': 'title', 'start node embedding': 'embedding_str'}, inplace=True)

# Function to safely parse the string embedding into a list of floats
def parse_embedding(embedding_str):
    try:
        return json.loads(embedding_str)
    except (TypeError, json.JSONDecodeError):
        return None

# Apply the parsing function to the embedding string column
movie_df['embedding'] = movie_df['embedding_str'].apply(parse_embedding)
movie_df.dropna(subset=['embedding'], inplace=True) # Remove rows with unparseable embeddings

def get_similar_movies_df(movie_title, df, top_n=10):
    if movie_title not in df['title'].values:
        return "Movie not found in the database."

    target_embedding = df[df['title'] == movie_title]['embedding'].iloc[0]

    # Calculate cosine similarities
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity([target_embedding], [x])[0][0])

    # Sort by similarity and get the top N similar movies (excluding the input movie itself)
    similar_movies_df = df[df['title'] != movie_title].sort_values(by='similarity', ascending=False).head(top_n)
    return similar_movies_df['title'].tolist()

def display_movie_recommendation_interface(movie_list):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nearest Nodes</title>
        <style>
            body { font-family: sans-serif; }
            .input-container { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="text"] { width: 300px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            button:hover { background-color: #0056b3; }
            #recommendations { margin-top: 20px; border: 1px solid #eee; padding: 15px; border-radius: 4px; background-color: #f9f9f9; }
            #recommendations h3 { margin-top: 0; }
            .rank-list { list-style: none; padding: 0; }
            .rank-list li { margin-bottom: 8px; }
        </style>
    </head>
    <body>
        <h2>Nearest Nodes</h2>
        <div class="input-container">
            <label for="movieInput">Enter a movie title:</label>
            <input type="text" id="movieInput" name="movieInput">
            <button onclick="getRecommendations()">Go</button>
        </div>

        <div id="recommendations" style="display: none;">
            <h3>Rank 1 (Top 3 Movies):</h3>
            <ul id="rank1-list" class="rank-list"></ul>
            <h3>Rank 2 (Top 3 by Actor):</h3>
            <ul id="rank2-list" class="rank-list"></ul>
            <h3>Rank 3 (Top 3 by Genre):</h3>
            <ul id="rank3-list" class="rank-list"></ul>
        </div>

        <script>
            const movies = """ + json.dumps(movie_list) + """;
            const getSimilarMoviesJS = (targetMovie, allMovies, topN = 9) => {
                if (!allMovies.some(movie => movie.title === targetMovie)) {
                    return "Movie not found in the database.";
                }

                const targetEmbedding = allMovies.find(movie => movie.title === targetMovie).embedding;

                const withSimilarity = allMovies.map(movie => {
                    if (movie.title === targetMovie || movie.embedding === null || targetEmbedding === null) {
                        return {...movie, similarity: -1}; // Avoid recommending the same movie or comparing with null embeddings
                    }

                    let dotProduct = 0;
                    let normA = 0;
                    let normB = 0;
                    for (let i = 0; i < Math.min(targetEmbedding.length, movie.embedding.length); i++) {
                        dotProduct += targetEmbedding[i] * movie.embedding[i];
                        normA += Math.pow(targetEmbedding[i], 2);
                        normB += Math.pow(movie.embedding[i], 2);
                    }
                    const similarity = dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
                    return {...movie, similarity: similarity};
                });

                const sortedMovies = withSimilarity.sort((a, b) => b.similarity - a.similarity);
                return sortedMovies.slice(1, topN + 1).map(movie => movie.title);
            };

            function getRecommendations() {
                const movieInput = document.getElementById("movieInput").value;
                const recommendationsDiv = document.getElementById("recommendations");
                const rank1List = document.getElementById("rank1-list");
                const rank2List = document.getElementById("rank2-list");
                const rank3List = document.getElementById("rank3-list");
                rank1List.innerHTML = ""; // Clear previous recommendations
                rank2List.innerHTML = "";
                rank3List.innerHTML = "";

                const similarMovies = getSimilarMoviesJS(movieInput, movies);

                if (typeof similarMovies === 'string') {
                    rank1List.innerHTML = `<li style="color: red;">${similarMovies}</li>`;
                    recommendationsDiv.style.display = "block";
                } else if (similarMovies.length > 0) {
                    recommendationsDiv.style.display = "block";
                    const top3 = similarMovies.slice(0, 3);
                    const next3 = similarMovies.slice(3, 6);
                    const last3 = similarMovies.slice(6, 9);

                    top3.forEach(movie => {
                        const listItem = document.createElement("li");
                        listItem.textContent = movie;
                        rank1List.appendChild(listItem);
                    });

                    next3.forEach(movie => {
                        const listItem = document.createElement("li");
                        listItem.textContent = movie;
                        rank2List.appendChild(listItem);
                    });

                    last3.forEach(movie => {
                        const listItem = document.createElement("li");
                        listItem.textContent = movie;
                        rank3List.appendChild(listItem);
                    });

                } else {
                    rank1List.innerHTML = "<li>No similar movies found.</li>";
                    recommendationsDiv.style.display = "block";
                }
            }
        </script>
    </body>
    </html>
    """
    display(HTML(html))

# Prepare the movie data in a format suitable for the JavaScript function
if 'title' in movie_df.columns and 'embedding' in movie_df.columns:
    movie_data_for_js = movie_df[['title', 'embedding']].to_dict('records')
    # Display the HTML interface only if the DataFrame is properly loaded and processed
    display_movie_recommendation_interface(movie_data_for_js)
else:
    print("Error: Could not prepare movie data for the interface. Ensure 'title' and 'embedding' columns exist.")