import pandas as pd 
import json

# Reading in CSV files with our data and extracting only the columns we need
credits = pd.read_csv("credits.csv")
credits = credits [['id', 'cast', 'crew']]
meta = pd.read_csv("movies_metadata.csv")
meta = meta [['id', 'title', 'genres']]
keywords = pd.read_csv("keywords.csv")

# Our initial data is very messy, so we'll create a function that converts it to a format
# that allows us to extract what we need
def clean_cast(col):
    col = str(col)
    col = col.replace("'",'"').replace("None","3").replace('.', '')
    col = json.loads(col) 
    for i in range(len(col)):
        col[i] = col[i]['name'].lower().replace(' ', '')
    return col

# Applying our function to each DataFrame in turn. Going row by row with a try block isn't ideal,
# but it lets us bypass finding every last obscure error in the formatting of the data
for i in range(len(meta['genres'])):
    try:
        meta.at[i,'genres'] = ' '.join(clean_cast(meta.at[i,'genres']))
    except:
        meta = meta.drop([i], axis=0)

for i in range(len(credits)):
    try:
        credits.at[i,'cast'] = ' '.join(clean_cast(credits.at[i,'cast']))
        credits.at[i,'crew'] = clean_cast(credits.at[i,'crew'])
    except:
        credits = credits.drop([i], axis=0)

for i in range(len(keywords['keywords'])):
    try:
        keywords.at[i,'keywords'] = ' '.join(clean_cast(keywords.at[i,'keywords']))
    except:
        keywords = keywords.drop([i], axis=0)

# Time to merge our dataframes together, so we'll first make sure the ID columns are the right type
for i in range(len(meta)):
    try:
        meta.at[i, 'id'] = int(meta.at[i, 'id'])
    except:
        meta = meta.drop([i], axis = 0)

# Merging 
credits = pd.merge(left=credits, right=meta, how='left', on='id')
df = pd.merge(left=credits, right=keywords, how='left', on='id')

# Taking the first name of our crew column (just the director)
for i in range(len(df['crew'])):
    df.at[i, 'crew'] = df.at[i, 'crew'][:1]
    df.at[i, 'crew'] = ' '.join(df.at[i,'crew'])

# Taking the first three actors from the cast of each movie
for i in range(len(df['cast'])):
    df.at[i,'cast'] = str(df.at[i,'cast'])
    df.at[i,'cast'] = df.at[i,'cast'].split()
    df.at[i,'cast'] = df.at[i,'cast'][:3]
    df.at[i,'cast'] = ' '.join(df.at[i,'cast'])

# Creating lists for each column so we can zip them together
cast = [df.at[i,'cast'] for i in range(len(df['cast']))]
crew = [df.at[i,'crew'] for i in range(len(df['crew']))]
keywords = [df.at[i,'keywords'] for i in range(len(df['keywords']))]
genres = [df.at[i,'genres'] for i in range(len(df['genres']))]

# Zipping our columns together and deleting any null values
info = [str(c) + " " + str(d) + " " + str(k) + " " + str(g) for c, d, k, g in zip(cast, crew, keywords, genres)]
info = [inf.replace(' nan', '') for inf in info]

# Adding our mega column to our DataFrame and deleting the other columns
df['info'] = info
df = df[['id', 'title', 'info']]

df.to_csv('cleanmovies.csv', index=False)