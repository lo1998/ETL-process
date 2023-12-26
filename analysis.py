#importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#reading the merged file
df = pd.read_csv('merged_final.csv')
#create new column by combining the revenue from box office mojo and the movie database
df['revenue_all'] = np.where(df['revenue_t'].isnull(), df['worldwide box office_m'],
                   np.where(df['revenue_t'] == 0, df['worldwide box office_m'],
                  df['worldwide box office_m']))
#create another column by giving ranking the revenue
df_sorted = df.sort_values(by='revenue_all', ascending=False)
df_sorted['revenue_rank'] = df_sorted['revenue_all'].rank(method='min', ascending=False)

df['revenue_rank'] = df_sorted['revenue_rank']
#create correlation values between three rating services and revenue all
correlation_imdb = df['imdb rating_i'].corr(df['revenue_all'])
correlation_metascore = df['metascore_i'].corr(df['revenue_all'])
correlation_moviedb = df['rating_x_t'].corr(df['revenue_all'])
#displaying them
print(correlation_imdb)
print(correlation_metascore)
print(correlation_moviedb)
#create scatter plot with the ratings and revenues
#here is use the imdb scale up so all the three ratings are between 1 and 100
plt.figure(figsize=(10, 6))
plt.scatter(df['imdb rating scaled up_i'], df['revenue_all'], color='blue', alpha=0.5, label='IMDb Rating')
plt.scatter(df['metascore_i'], df['revenue_all'], color='green', alpha=0.5, label='Metascore')
plt.scatter(df['rating_x_t'], df['revenue_all'], color='red', alpha=0.5, label='Rating X')
plt.title('Correlation between Ratings and Revenue')
plt.xlabel('Ratings')
plt.ylabel('Revenue (in millions)')
plt.legend()
plt.grid(True)
#saving the scatter plot
plt.savefig('correlation.png')

#create new dataframes for slicing each one to see which top 10 rated movies per
#rating service are in top 50 highest grossing movies
top10_imdb = df.sort_values(by='imdb rating_i', ascending=False).head(10)
top10_metascore = df.sort_values(by='metascore_i', ascending=False).head(10)
top10_moviedb = df.sort_values(by='rating_x_t', ascending=False).head(10)
top50_revenue = df.sort_values(by='revenue_all', ascending=False).head(50)
#combining the new rating dataframes
combined_top10 = pd.concat([top10_imdb, top10_metascore, top10_moviedb])
unique_top10_movies = combined_top10['title'].unique()
#print out the overlap between highest ranked movies and highest grossing movies
overlap = top50_revenue[top50_revenue['title'].isin(unique_top10_movies)]
print(overlap)

selected_columns = overlap[['title', 'rating_x_t', 'rank_i', 'imdb rating_i', 'metascore_i', 'revenue_all', 'revenue_rank']]
print(selected_columns)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 20)
table_string = selected_columns.to_string(index=False)
#displaying those movies in a table format
print(table_string)
#to the same thing again but now with top 50 highest rated movies and
#top 50 highest grossing movies
top50_imdb = df.sort_values(by='imdb rating_i', ascending=False).head(50)
top50_metascore = df.sort_values(by='metascore_i', ascending=False).head(50)
top50_moviedb = df.sort_values(by='rating_x_t', ascending=False).head(50)
top50_revenue = df.sort_values(by='revenue_all', ascending=False).head(50)

combined_top50 = pd.concat([top50_imdb, top50_metascore, top50_moviedb])
unique_top50_movies = combined_top50['title'].unique()
overlap2 = top50_revenue[top50_revenue['title'].isin(unique_top50_movies)]
#print out the overlap again
print(overlap2)

selected_columns2 = overlap2[['title', 'rating_x_t', 'rank_i', 'imdb rating_i', 'metascore_i', 'revenue_all', 'revenue_rank']]
print(selected_columns2)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 20)
table_string = selected_columns2.to_string(index=False)
#displaying it in a table format
print(table_string)
