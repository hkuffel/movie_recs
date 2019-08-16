import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv('cleanmovies.csv')

# Setting the index of our DataFrame to be the title of the movie
df.set_index('title', inplace=True)

# Creating a series with movies that we will use to match movies with their similarity values
indices = pd.Series(df.index)

# Setting up our count vectorizer and calculating cosine similarity values
count = CountVectorizer()
count_matrix = count.fit_transform(df['info'].values.astype('U'))
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# function that takes in movie title as input and returns the top six recommended movies
def recommend(title, cosine_sim = cosine_sim):
    recommended_movies = []
    # get the index from our series of titles
    idx = indices[indices == title].index[0]
    # creating a Series of descending similarity scores
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    # making a list of the top six scores
    top_6_indexes = list(score_series.iloc[1:7].index)
    # populating the list with the corresponding movie titles
    for i in top_6_indexes:
        recommended_movies.append(list(df.index)[i]) 
    return recommended_movies

# Finally, creating a command line interface that allows the user to enter a movie
# and see recommendations if the movie is in the database
run = 'y'
print('Welcome!')
while run == 'y':
    choice = input("What's a movie you like? ")
    try:
        recs = recommend(choice)
        print(f'If you like {choice}, you may like {recs}.')
    except:
        print("Don't know that one sorry :(")
    run = input('Would you like to see another list? (y)es or (n)o ')