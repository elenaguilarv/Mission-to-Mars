# Mission-to-Mars
Webscraping and storing article summaries, images, and table of facts from Mars in MongoDB and presenting through a Flask webpage. The code has the ability to refresh the scrape and display the latest news and facts.

## Challenge
Include 4 images of Mars' hemispheres from a scraping friendly website.

 ### Objectives
- Use BeautifulSoup and Splinter to automate a web browser and scrape high-resolution images
- Use a MongoDB database to store data from the web scrape
- Update the web application and Flask to display the data from the web scrape
- Use Bootstrap to style the web app

### Workflow
In order to scrape the four hemisphere images, I created an empty list (hemis_images) to append the results there, then performed a for loop that could iterate through the appropriate image indexes (4,8) to scrape their URLs and titles and store them as a dictionary as {title:url}. Before the loop could move to the next photo, I had to call the browser.back() function so that it could continue to run without errors.

#### Portfolio
![alt text](https://github.com/elenaguilarv/Mission-to-Mars/blob/master/challenge/mars_webpage.PNG)
