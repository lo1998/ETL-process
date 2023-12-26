#importing libraries
import pandas as pd
import numpy as np
#read the impured csv file
imdb_df = pd.read_csv('impured_data.csv')
#cleaning the data in different steps
#Step 1: remove duplicates
imdb_df = imdb_df.drop_duplicates()
#Step 2: drop rows that have nothing to do with the ranks
rows_to_drop = list(range(250, 257))
imdb_df = imdb_df.drop(rows_to_drop).reset_index(drop=True)
#Step 3: make rows positive again
imdb_df['IMDB Rating'] = imdb_df['IMDB Rating'].abs()
#which column have missing values
na_count_per_column = imdb_df.isna().sum()
print(na_count_per_column)

#Step 4: for imdb rating column, replace the na values with the one a row below,
# because it is already ranked in the dataframe and the value will be the same or similar
imdb_df['IMDB Rating'] = imdb_df['IMDB Rating'].bfill()
#Step 5: put away the .0 by converting to int
imdb_df['Metascore'] = imdb_df['Metascore'].astype('Int64')
imdb_df['Release Year'] = imdb_df['Release Year'].fillna(0).astype(int)
#Step 6: split the values in column 'Rank' into new colums 'Rank' and 'Title'
imdb_df[['Rank', 'Title']] = imdb_df['Rank'].str.extract(r'(\d+)\.\s*(.*)')
imdb_df['Rank'] = imdb_df['Rank'].astype(int)
#calculation 1
#change the column IMDB Rating and make the values new from 1 to 100 so i can compare it with the movie databank
#becuase the others are from 1 to 100. For adjusting I need to muliply the IMDB
# rating with 10. If others would be for example from 1 to 5 then we would need
# to normalize the values
#convert to integer after
imdb_df['IMDB Rating scaled up'] = imdb_df['IMDB Rating'] * 10
imdb_df['IMDB Rating scaled up'] = imdb_df['IMDB Rating scaled up'].fillna(0).astype(int)
#Step 7: replace missing values from Metascore with the value from IMDB Rating scaled up
imdb_df['Metascore'] = imdb_df['Metascore'].fillna(imdb_df['IMDB Rating scaled up'])

unique_values = imdb_df['Duration'].unique()
print(unique_values)
#change the named values to missing values
#regular expression pattern for valid duration format
duration_pattern = r'^\d+h \d+m$'
imdb_df['Duration'] = imdb_df['Duration'].fillna('invalid')
valid_durations_mask = imdb_df['Duration'].str.match(duration_pattern)
# Replace invalid durations with NaN
imdb_df.loc[~valid_durations_mask, 'Duration'] = np.nan
imdb_df['Duration'].replace('invalid', np.nan, inplace=True)
#caluclation 2
#define a function to transform the Duration column to float,
# so 2h22min is like 2,XX so its later easier to calculate
def convert_duration(duration):
    # Check if the input is a string before attempting to split
    if isinstance(duration, str):
        parts = duration.split()
        hours = 0
        minutes = 0
        for part in parts:
            if 'h' in part:
                hours = float(part.replace('h', ''))
            elif 'm' in part:
                minutes = float(part.replace('m', '')) / 60
        return hours + minutes
    else:
        # If it's not a string, it might already be a float or int
        return duration
# Apply the conversion to the 'Duration' column
imdb_df['Duration'] = imdb_df['Duration'].apply(convert_duration)
#change the nan values in duration and replace it the the mean value of duratoin column
mean_duration = imdb_df['Duration'].mean()
imdb_df['Duration'].fillna(mean_duration, inplace=True)
#calculation 3
#calculate a new column by subtracting the release year from this year to see how old the movie is
imdb_df['Movie Age'] = 2023 - imdb_df['Release Year']
imdb_df = imdb_df.drop(imdb_df.index[imdb_df.index >= 250])

filename = "cleaned_data1.csv"
#save the cleaned data as a csv file and hand it over to studen C, so the
#data can be merged, I had to use utf-8-sig, for the special characters
#utf-8 would not work for all the different movie titles
imdb_df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"Data has been written to {filename}")
