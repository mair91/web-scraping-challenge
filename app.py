import scrape_mars
from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import sys

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    marsInfo=mongo.db.mars_db.find_one()
    return render_template("index.html", marsmars=marsInfo)

@app.route("/scrape")
def scrape():     
    marsInfo = mongo.db.marsInfo
    marsData=scrape_mars.scrape_news()
    marsData=scrape_mars.scrape_image()
    marsData=scrape_mars.scrape_weather()
    marsData=scrape_mars.scrape_facts()
    marsData=scrape_mars.scrape_hemi()
    mongo.db.collection.update({}, marsData, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)