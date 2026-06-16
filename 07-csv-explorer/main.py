import pandas as pd

def show_basic_stats(df):
    print(f"Total movies: {df.shape[0]}")
    print(f"Average IMDB score: {df['imdb_score'].mean():.1f}")
    print(f"Highest gross: {df['gross'].max()}")
    print(f"Year range: {int(df['title_year'].min())} - {int(df['title_year'].max())}")

def filter_by_score(df):
    min_score = float(input("Enter the min IMDB score: "))
    print(df[df["imdb_score"] > min_score])

def top_grossing(df):
    print(df.sort_values("gross", ascending=False).head(10))

def movies_by_director(df):
    director = input("Enter the director name: ")
    result = df[df["director_name"].str.lower() == director.lower()]
    print(result)

def main():
    df = pd.read_csv("movies.csv")
    show_basic_stats(df)
    filter_by_score(df)
    top_grossing(df)
    movies_by_director(df)

main()