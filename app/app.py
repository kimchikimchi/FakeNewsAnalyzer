from flask import Flask, json, request, jsonify, render_template, redirect

# instatiate Flask app
app = Flask(__name__)

# routes
# html routes
@app.route("/")
def index():
    return render_template("index.html")

# start/run server
if __name__ == "__main__":
    app.run(debug=True)