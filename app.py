from flask import request
from flask import Flask, request #import main Flask class and request object

app = Flask(__name__) #create the Flask app

@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None
    framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    website = request.args.get('website')

    return '''<h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)


@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

import pandas as pd
import numpy as np
from scipy import sparse
import itertools
from datetime import datetime
import random
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.metrics import mean_squared_error

from math import sqrt
import warnings; warnings.simplefilter('ignore')

data = pd.read_excel('Latestpredictiondata.xlsx')

data['category'] = (data['category'].fillna(''))
data['colour'] = (data['colour'].fillna(''))
data['size(inches)'] = str(data['size(inches)'].fillna(''))
data['weight (g)'] = str(data['weight (g)'].fillna(''))

items = data['item']

items['features'] = data['category'] + data['colour'] + data['size(inches)'] + data['weight (g)']

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(items['features'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
cosine_sim[0]

data = data.reset_index()
item_name = data['item'] 
indices = pd.Series(data.index, index = data['item'])

# Function that get item recommendations based on the cosine similarity score of items

def item_recommendations(item): 
    idx = indices[item]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    user_indices = [i[0] for i in sim_scores]
    return item_name.iloc[user_indices] 


def get_features(item_list):
    items_userwise = data['item'].isin(item_list)
    df1 = pd.DataFrame(data = data[items_userwise], columns=['item'])
    itemlist = df1['item'].tolist() 
    item_list = data['item'].isin(itemlist)     
    df_temp = pd.DataFrame(data = data[item_list], columns=['item','CustomerId','bilNumber','category'])
    return df_temp 
   
@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()   
        
    item = req_data['item']
    
    return '''
The item is: {}'''.format(get_features(item_recommendations(item)))       

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000