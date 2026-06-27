import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, jsonify, session
import numpy as np

app = Flask(__name__)
app.secret_key = "movierec123"

# Load data
ratings = pd.read_csv('ml-100k/u.data', sep='\t',
                       names=['user_id', 'movie_id', 'rating', 'timestamp'])

movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1',
                      names=['movie_id', 'title', 'release_date', 'video_date',
                             'imdb_url', 'unknown', 'Action', 'Adventure',
                             'Animation', 'Childrens', 'Comedy', 'Crime',
                             'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
                             'Horror', 'Musical', 'Mystery', 'Romance',
                             'Sci-Fi', 'Thriller', 'War', 'Western'])

# Popularity filter — movies with at least 50 ratings
movie_rating_counts = ratings.groupby('movie_id')['rating'].count()
popular_movies = movie_rating_counts[movie_rating_counts >= 50].index

# User-movie matrix
user_movie_matrix = ratings.pivot_table(
    index='user_id', columns='movie_id', values='rating').fillna(0)

# Cosine similarity
user_similarity = cosine_similarity(user_movie_matrix)
user_similarity_df = pd.DataFrame(user_similarity,
                                   index=user_movie_matrix.index,
                                   columns=user_movie_matrix.index)

genres = ['Action', 'Adventure', 'Animation', 'Childrens', 'Comedy',
          'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
          'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Thriller', 'War', 'Western']

@app.route("/")
def index():
    # Get 50 popular movies to rate
    popular_movie_ids = popular_movies.tolist()
    sample_movies = movies[movies['movie_id'].isin(popular_movie_ids)].sample(100)
    movies_list = sample_movies[['movie_id', 'title']].to_dict('records')
    return render_template("rate.html", movies=movies_list)

@app.route("/genres", methods=["POST"])
def genres_page():
    # Save ratings from step 1 in session
    user_ratings = {}
    for key, value in request.form.items():
        if value and value != "0":
            user_ratings[int(key)] = int(value)
    
    if len(user_ratings) < 15:
        return "Please rate at least 15 movies.", 400
    
    session['user_ratings'] = user_ratings
    return render_template("genres.html", genres=genres)

@app.route("/recommend", methods=["POST"])
def recommend():
    user_ratings = session.get('user_ratings', {})
    selected_genres = request.form.getlist('genres')
    
    # Collaborative part
    # Build a ratings vector for the new user
    new_user_vector = pd.Series(0, index=user_movie_matrix.columns)
    for movie_id, rating in user_ratings.items():
        if movie_id in new_user_vector.index:
            new_user_vector[movie_id] = rating
    
    # Find most similar existing user
    similarities = cosine_similarity([new_user_vector], user_movie_matrix)[0]
    most_similar_user = user_movie_matrix.index[similarities.argmax()]
    
    # Get their highly rated movies
    similar_user_movies = ratings[
        (ratings['user_id'] == most_similar_user) &
        (ratings['rating'] >= 4)
    ]['movie_id'].tolist()
    
    # --- Content part ---
    # Get movies matching selected genres
    if selected_genres:
        genre_filter = movies[selected_genres].any(axis=1)
        genre_movies = movies[genre_filter]['movie_id'].tolist()
    else:
        genre_movies = []
    
    # --- Hybrid scoring ---
    scored = {}
    rated_movies = set(user_ratings.keys())
    
    for movie_id in popular_movies:
        if movie_id in rated_movies:
            continue
        score = 0
        if movie_id in similar_user_movies:
            score += 2  # collaborative boost
        if movie_id in genre_movies:
            score += 1  # genre boost
        if score > 0:
            scored[movie_id] = score
    
    # Sort by score
    top_movie_ids = sorted(scored, key=scored.get, reverse=True)[:20]
    
    # Get movie titles
    recommended = movies[movies['movie_id'].isin(top_movie_ids)][['movie_id', 'title']].to_dict('records')
    
    return render_template("results.html", movies=recommended, genres=selected_genres)

if __name__ == "__main__":
    app.run(debug=True)