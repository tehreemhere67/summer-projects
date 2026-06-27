# Movie Recommendation Engine

A hybrid movie recommendation system built with Python and Flask. Users rate movies they've seen, select their preferred genres, and get personalized recommendations combining collaborative filtering and content-based filtering.

## How it works
- Collaborative filtering: finds the most similar user in the MovieLens database based on your ratings, recommends what they liked
- Content-based filtering: filters recommendations by your selected genres
- Popularity filter: only recommends movies with 50+ ratings to ensure quality
- Hybrid scoring: combines both approaches for better recommendations

## Dataset
Uses the MovieLens 100K dataset — 100,000 ratings from 943 users across 1682 movies collected by the GroupLens Research Project.
