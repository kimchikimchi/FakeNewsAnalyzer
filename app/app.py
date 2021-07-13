# Library Imports
import flask
import pickle
import traceback
import pandas as pd
from flask import Flask, json, request, jsonify, render_template, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score


# importing model passive-aggressive-classifier model (PAC)
with open('model/pac_model.pkl', 'rb') as f:
    classifier = pickle.load(f)

# import vectorizer
with open('model/tfidf_vectorizer.pkl','rb') as f:
    tfidf_vectorizer = pickle.load(f)


# instantiate  Flask app
app = Flask(__name__)


# html routes
@app.route("/")
def index():
    return render_template("index.html")


# Fake news prediction
@app.route("/api/v1.0/analyze", methods=["POST"])
def invokeAnalyzer():
    try:
        body = request.get_json()
        article_title = body["title"]
        article_text = body["body"]

        # Constructing a fake Series
        # text = pd.Series(['a day after the candidates squared off in a fiery debate, they came to columbia, south carolina, and largely agreed that while kings impact can still be felt today, work still needs to be done to guarantee racial equality.\n\n"yes, the challenges we face are many, but so are the quiet heroes working in every corner of america today doing their part to make our country a better place," said the former secretary of state. "i for one receive much inspiration from that simple fact."\n\nthere was symbolism in the event organized by the naacp: in front of a statehouse that flew the confederate battle flag until it was taken down last year. all three candidates noted the flag being removed.\n\n"the flag is down but we are still here because that flag was just one piece of something bigger," clinton said. "dr. king died with his work unfinished and it is up to us to see through."\n\nsanders argued that king is not just a historic figure, but someone whose moral compass should guide people today. repeating the phrase "i think if he were here today," sanders argued that if king were alive today"'])

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