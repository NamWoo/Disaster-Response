## 2020-05-04
## v0.5
## https://github.com/NamWoo

import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    Load and merge messages and categories datasets

    Args:
        messages_filepath: string. Filepath for csv file containing messages dataset.
        categories_filepath: string. Filepath for csv file containing categories dataset.
       
    Returns:
        df: dataframe. Dataframe containing merged content of messages and categories datasets.
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    # .merge(categories, how = 'left', on = ['id'])
    return pd.merge(messages, categories, on='id')


def clean_data(df):
    """
    Clean dataframe
    
    Args:
        df: dataframe. Dataframe containing merged content of messages and categories datasets.
       
    Returns:
        df: dataframe. Dataframe containing cleaned version of input dataframe.
    """
    categories = df['categories'].str.split(';', expand = True)
    row = categories.iloc[0]    #row = categories[:1]
    category_colnames = row.transform(lambda x: x[:-2]).tolist()
    categories.columns = category_colnames

    for column in categories:
        categories[column] = categories[column].transform(lambda x: x[-1:])
        categories[column] = pd.to_numeric(categories[column])

    df = df.drop('categories', axis = 1, inplace = False)
    df = pd.concat([df, categories], axis = 1)
    df.drop_duplicates(inplace = True)
    return df[df['related'] != 2]


def save_data(df, database_filename):
    """
    Save SQLite database.
    
    Args:
        df: dataframe. Dataframe containing cleaned version of merged message and categories data.
        database_filename: string. Filename for output database.
       
    Returns:
        None
    """
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('Messages', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()