from flask import Flask, render_template,request
import pickle
import numpy as np
import pandas as pd

pbr_df = pickle.load(open('PopularBookRecommendation.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
book = pickle.load(open('book.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

dt = pd.read_csv("data/data.csv", on_bad_lines = 'skip')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(pbr_df['Book-Title'].values),
                           author = list(pbr_df['Book-Author'].values),
                           publisher=list(pbr_df['Publisher'].values),
                           image = list(pbr_df['Image-URL-M'].values),
                           votes = list(pbr_df['Num_rating'].values),
                           rating = list(pbr_df['Avg_rating'].values),
                           categories = list(dt['categories'].values))

@app.route('/recommendation')
def recommendation_ui():
    return render_template('recommendation.html')

@app.route('/recommend_books',methods=['post'])
def recommendation():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1],reverse=True)[1:9]

    data = []
    for i in similar_items:
        item = []
        temp_df = book[book['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('recommendation.html',data=data)


@app.route('/categories')
def categories():
    return render_template('categories.html')


@app.route('/recommend_categories', methods=['POST'])
def recommend_categories():
    categories_name = request.form.get('categories_name')  # Safely access form data using get method
    if categories_name is None:
        return "Category name not provided."
    
    filtered_books = dt[dt['categories'] == categories_name]
    if not filtered_books.empty:
        sorted_books = filtered_books.sort_values(by='average_rating', ascending=False)
        if len(sorted_books) >= 10:
            return sorted_books.head(5).to_html()
        else:
            return sorted_books.to_html()
    else:
        return "No recommendations available for this category."



if __name__ == '__main__':
    app.run(debug=True)