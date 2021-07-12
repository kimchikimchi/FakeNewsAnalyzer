from flask import Flask, json, request, jsonify, render_template, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
import flask
import pickle
import traceback
import pandas as pd


# initiate  Flask app
app = Flask(__name__)

# Initialize a TfidfVectorizer. 
# See for details https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

# importing models
with open('model/pac_model.pkl', 'rb') as f:
    classifier = pickle.load(f)

with open('model/model_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)

# html routes
@app.route("/")
def index():
    return render_template("index.html")

# Fake news prediction
@app.route('/predict', methods=['POST','GET'])
def predict():
  
   if flask.request.method == 'GET':
       return "Prediction page"
 
   if flask.request.method == 'POST':
        try:
            json_ = request.json
            print(json_)
            # Convert json object
            query_ = pd.get_dummies(pd.DataFrame(json_))
            query = query_.reindex(columns = model_columns, fill_value= 0)

            print(type(qyery))
                            
            from pprint import pprint
            pprint(query)

            tfidf_test = tfidf_vectorizer.transform(query)
            prediction = list(classifier.predict(query))
    
            return jsonify({
                "prediction":str(prediction)
            })
 
        except:
            return jsonify({
                "trace": traceback.format_exc()
                })

# start/run server
if __name__ == "__main__":
    app.run(debug=True)