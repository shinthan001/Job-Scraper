import pandas as pd
from pymongo import MongoClient

import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def _connect_mongo(host, port, username, password, db):
# reference: https://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas    
    if(username and password):
        mongo_uri = "mongodb://%s:%s@%s:%s/%s".format(username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]

def read_mongo(db:str, collection:str, query:dict={}, host:str='localhost', 
               port:int=27017, username:str=None, password:str=None, no_id:bool=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

def display_pdseries_fw(pdseries:pd.Series):
    """Full width display of pandas series"""
    with pd.option_context('display.max_colwidth', None):
        print(pdseries)

def plot_barh(x:list,y:list,xlabel:str,ylabel:str,title:str,figsize:tuple=(6, 5), color:str='skyblue'):
    """Horizontal bar plot"""
    fig = plt.figure(figsize=figsize)
    bars = plt.barh(x, y, color=color)
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y(),
             f'{bar.get_width():.2f}', fontsize=7)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.show()

def plot_lineplot(data: pd.DataFrame,xlabel:str,ylabel:str,title:str,figsize:tuple=(6, 5), color:str='skyblue'):
    """Line plot"""
    fig = plt.figure(figsize=figsize)
    sns.lineplot(data=data, x=xlabel, y=ylabel, color=color)
    plt.title(title)
    plt.xticks(rotation = 90)
    plt.grid()
    plt.show()

def render_wordcloud(freq_data: pd.DataFrame):
    """Wordcloud"""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_data)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()