# from flask import Flask,render_template,request
# import numpy as np
# import pandas as pd
# import pickle
#
# popular_df = pickle.load(open('popular.pkl','rb'))
# pt = pickle.load(open('pt.pkl','rb'))
# books = pickle.load(open('books.pkl','rb'))
# similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('index.html',
#                            book_name = list(popular_df['Book-Title'].values),
#                            author = list(popular_df['Book-Author'].values),
#                            image = list(popular_df['Image-URL-M'].values),
#                            votes = list(popular_df['num_Ratings'].values),
#                            ratings = list(popular_df['Book-Rating'].values),
#                            )

# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')
#
# @app.route('/recommend_books',methods=['post'])
# def recommend():
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_Ratings'].values),
                           ratings=list(popular_df['Book-Rating'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if user_input not in pt.index:
        return "User input not found in the dataset. Please try another."

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]  # Top 5 excluding the input book

    data = []
    for i in similar_items:
        book_title = pt.index[i[0]]
        temp_df = books[books['Book-Title'] == book_title]

        if not temp_df.empty:
            temp_df = temp_df.drop_duplicates('Book-Title')
            item = [
                temp_df['Book-Title'].values[0],
                temp_df['Book-Author'].values[0],
                temp_df['Image-URL-M'].values[0]
            ]
            data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
