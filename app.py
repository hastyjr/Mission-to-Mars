# Import Flask, PyMongo, and scraping.py
from xml.dom.minidom import Document
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

## set up Flask ##
app = Flask(__name__)
## app.debug = True ## <-- uncomment this line to debug ##

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

## set up Flask routes ##
## define the route for the HTML page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    # holding newly scraped data, referencing scrape_all() function in scraping.py file
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return "Scraping Successful"

if __name__ == "__main__":
    app.run(debug=True)
