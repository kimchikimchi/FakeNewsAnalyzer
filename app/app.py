# Library Imports
import flask
import pickle
import traceback
import pandas as pd
import os
from flask import Flask, json, request, jsonify, render_template, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

# instantiate  Flask app
app = Flask(__name__)

# Need to dynamically look up absolute path since
# all relative paths are relative to the working directory
MODEL_PATH = os.path.join(app.root_path, 'model')

# importing model passive-aggressive-classifier model (PAC)
with open(f"{MODEL_PATH}/pac_model.pkl", 'rb') as f:
    classifier = pickle.load(f)

# import vectorizer
with open(f"{MODEL_PATH}/tfidf_vectorizer.pkl",'rb') as f:
    tfidf_vectorizer = pickle.load(f)


# html routes
@app.route("/")
def index():
    return render_template("index.html")


# Fake news prediction
@app.route("/api/v1.0/analyze", methods=["POST"])
def invokeAnalyzer():
    try:
        # Assume all objects getting are json objects.
        body = request.get_json(force=True)
        # print(body)
        article_title = body["title"]
        article_text = body["body"].lower()

        # Vectorizer expects Series as input
        text = pd.Series([article_text])

        tfidf_test = tfidf_vectorizer.transform(text)
        prediction = list(classifier.predict(tfidf_test))[0]
        confidence = list(classifier.decision_function(tfidf_test))[0]

        return jsonify({
            "title": article_title,
            "text": article_text,
            "prediction": prediction,
            "confidence": confidence
        })

    except:
        # returns stacktrace dump back
        return jsonify({
            "trace": traceback.format_exc()
        })


# start/run server
if __name__ == "__main__":
    app.run(debug=True)