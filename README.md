# Hot Peppers 🌶️🌶️

A fun side project exploring hot peppers!

I grew up with very little spice in my diet -- my mother is Irish, what can I say? -- and get regularly mocked for my lack of spice tolerance. I figured that I'd do some research into these nuggets of suffering and glory so that the next time I am prompted to eat a pepper, I can distract my mocking friends enough to escape the actual act of pepper consumption.

## Technology & Skills
- Web scraping (Requests, urllib, nonces)
- HTML parsing (BeautifulSoup, Selenium)
- Data sanitization (Pandas, fuzzywuzzy, Regex)
- Regression analysis (scikit-learn)
- Code design (Python, modules, OOP, scalability)

## Data

### Background

The data is currently curated from [PepperScale](https://www.pepperscale.com/hot-pepper-list/),  [ChiliWorld](https://www.chilliworld.com/factfile/scoville-scale#ChilliPepperScovilleScale), [Uncle Steve's Hot Stuff](http://ushotstuff.com/Heat.Scale.htm), [Cayenne Diane](https://www.cayennediane.com/the-scoville-scale/), and [Pepperheads for Life](https://pepperheadsforlife.com/the-scoville-scale/). I have no affiliation with any of the sites, but am grateful for their work!

While this project is in the "data sanitization" phase, you can find the most up-to-date set in `data/`. Both `.json` and `.csv` formats are available! If you plan on using the data, I'd love to know about it :)

### Schema

Field | Description
--- | ---
"name"| String; name of the pepper; unique
"species" | String; pepper species. All hot peppers belong to the Capsicum genus (part of the nightshade family), but there are multiple species within it.
"heat" | Categorical; how hot the pepper is perceived to be: "Mild", "Medium", "Extra Hot", "Super Hot" ([their](https://www.pepperscale.com/hot-pepper-list/) categories, not mine)
"region" | Categorical; region of the world in which the pepper grows; based on provided origin. (Standardized origin)
"origin" | String; where the pepper grows; values are country, region, or continent as listed
"min_shu" | Float; Scoville Heat Units (SHU) for the mildest variation of the pepper
"max_shu" | Float; Scoville Heat Units (SHU) for the hottest variation of the pepper
"min_jrp" | Float; Jalapeño Reference Point (JRP) for the minimum number of times hotter than a jalapeño the pepper is
"max_jrp" | Float; Jalapeño Reference Point (JRP) for the maximum number of times hotter than a jalapeño the pepper is
"detail_link" | String; link to more information on the pepper
"source_link" |  String; data source link
"source_name" | String; name of source site from which pepper data came

Pepper hotness is based on the **Scoville Scale**, a measurement of the pungency of chili peppers running from mild to extreme. If you're interested in the scale -- along with its many pros and cons -- I recommend you read PepperScale's article on the subject [here](https://www.pepperscale.com/what-is-the-scoville-scale/), or trusty [Wikipedia](https://en.wikipedia.org/wiki/Scoville_scale).

Basis for min/max [Scoville heat units (SHU)](https://www.pepperscale.com/scoville-heat-units/): Individual hot peppers have a range of heat, depending on where they are grown, how long they’ve matured, and the amount of sun they’ve received.

Basis for min/max [Jalapeno Reference Point (JRP)](https://www.pepperscale.com/jalapeno-peppers/): The JRP is a subjective comparison of a pepper against a reference point most everyone has tried, resulting in a range of opinions. A negative number (like -50) means the amount of times the pepper is milder. A zero (0) means equal heat. Any positive numbers show the amount of times that the pepper is hotter than a jalapeño.

## Helpful resources

### Technical
- [How to Scrape an AJAX Website using Python](https://www.codementor.io/codementorteam/how-to-scrape-an-ajax-website-using-python-qw8fuitvi)
- [Explanation of the "json": {"key":"value"} addition to the POST request (missing in the Requests documentation...?)](https://stackoverflow.com/questions/9733638/post-json-using-python-requests)
- When my scraper broke the day after I built it, I learned about [nonces](https://codex.wordpress.org/WordPress_Nonces) in WordPress. I had to find a way to fetch the daily nonce to complete the AJAX request.
- scikit-learn's [description of linear models](http://scikit-learn.org/stable/modules/linear_model.html)
- [How to handle outliers](http://www.theanalysisfactor.com/outliers-to-drop-or-not-to-drop/)

### Topical
- FiveThirtyEight's article on [Rating Chili Peppers](https://fivethirtyeight.com/features/rating-chili-peppers-on-a-scale-of-1-to-oh-dear-god-im-on-fire/)
- Guinness Book of World Records on the [Hottest Chili](http://www.guinnessworldrecords.com/world-records/hottest-chili)

## Progress tracker & contributions

Check out my [Trello board](https://trello.com/b/PTT5nKqH/hot-peppers-%F0%9F%8C%B6%EF%B8%8F) for insight into my process, what's been done, and what's on the docket.

I welcome any and all contributions from the world at large! If you're interested in collaborating, please consider the following:
- Git flow: fork the repository, submit PR
- Request to be added as a member to the Trello board

![Alt Text](https://media.giphy.com/media/3oriO5w4cPs5SECFmU/giphy.gif)
