# Use Flask and Mongo to create web app
# import tools and dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import challenge_mars

# Set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # tells python that our app will connect to Mongo using an URI
mongo = PyMongo(app)

# Set up app flask routes - one for main HTML page and one for scraping new data
@app.route("/")
def index():
   mars = mongo.db.mars_app.find_one()
   return render_template("index.html", mars=mars) # Link our visual representation of our web app to the code that powers it

# Set up a scraping route - the "button" of the web app
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars_app
   mars_data = challenge_mars.scrape_all()
   mars.update({}, mars_data, upsert=True) # .update(query_parameter (create an empty collection using -->), data, scraping options)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()

# refactoring- integrate functions and error handling updates
