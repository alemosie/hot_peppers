# Hot Peppers 🌶️🌶️

A fun side project exploring hot peppers!

I grew up with very little spice in my diet -- my mother is Irish, what can I say? -- and get regularly mocked for my lack of spice tolerance. I figured that I'd do some research into these nuggets of suffering and glory so that the next time I am prompted to eat a pepper, I can distract my mocking friends enough to escape the actual act of pepper consumption.

## Technology & Skills
- Web scraping (Requests, urllib, nonces)
- HTML parsing (BeautifulSoup)
- Data sanitization (Pandas)
- Scalability: static vs dynamic data fetching, modularization
- Python 2 -> Python 3

## Data

### Background

The base data is from [PepperScale](https://www.pepperscale.com), a website that seems to be entirely dedicated to the topic of peppers. I have no affiliation with the site, but am grateful for their work! I specifically curated this dataset from their [Hot Pepper List](https://www.pepperscale.com/hot-pepper-list/).

Pepper hotness is based on the **Scoville Scale**, a measurement of the pungency of chili peppers running from mild to extreme. If you're interested in the scale -- along with its many pros and cons -- I recommend you read PepperScale's article on the subject [here](https://www.pepperscale.com/what-is-the-scoville-scale/), or trusty [Wikipedia](https://en.wikipedia.org/wiki/Scoville_scale).

I used Python, [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [Requests](http://docs.python-requests.org/en/master/) and [Pandas](https://pandas.pydata.org/pandas-docs/stable/) to extract, sanitize, and convert the data into `data/peppers.json`, available for your enjoyment.

### Schema

Field | Description
--- | ---
"name"| Name of the pepper; unique
"species" | Pepper species. All hot peppers belong to the Capsicum genus (part of the nightshade family), but there are multiple species within it.
"heat" | How hot the pepper is perceived to be: "Mild", "Medium", "Extra Hot", "Super Hot" ([their](https://www.pepperscale.com/hot-pepper-list/) categories, not mine)
"region" | Region of the world in which the pepper grows; based on provided origin. (Standardized origin)
"origin" | Where the pepper grows; values are country, region, or continent as listed
"min_shu" | Scoville Heat Units (SHU) for the mildest variation of the pepper
"max_shu" | Scoville Heat Units (SHU) for the hottest variation of the pepper
"min_jrp" | Jalapeño Reference Point (JRP); minimum value for number of times hotter than a jalapeño the pepper is
"max_jrp" | Jalapeño Reference Point (JRP); maximum value for number of times hotter than a jalapeño the pepper is
"link" | PepperScale article containing more information on the pepper

Basis for min/max [Scoville heat units (SHU)](https://www.pepperscale.com/scoville-heat-units/): Individual hot peppers have a range of heat, depending on where they are grown, how long they’ve matured, and the amount of sun they’ve received.

Basis for min/max [Jalapeno Reference Point (JRP)](https://www.pepperscale.com/jalapeno-peppers/): The JRP is a subjective comparison of a pepper against a reference point most everyone has tried, resulting in a range of opinions. A negative number (like -50) means the amount of times the pepper is milder. A zero (0) means equal heat. Any positive numbers show the amount of times that the pepper is hotter than a jalapeño.

### Future data to compare against/incorporate
- https://www.chilliworld.com/factfile/scoville-scale#ChilliPepperScovilleScale
- http://ushotstuff.com/Heat.Scale.htm
- https://www.cayennediane.com/the-scoville-scale/

## Helpful resources

### Technical
- [How to Scrape an AJAX Website using Python](https://www.codementor.io/codementorteam/how-to-scrape-an-ajax-website-using-python-qw8fuitvi)
- [Explanation of the "json": {"key":"value"} addition to the POST request (missing in the Requests documentation...?)](https://stackoverflow.com/questions/9733638/post-json-using-python-requests)
- When my scraper broke the day after I built it, I learned about [nonces](https://codex.wordpress.org/WordPress_Nonces) in WordPress. I had to find a way to fetch the daily nonce to complete the AJAX request.

### Topical
- FiveThirtyEight's article on [Rating Chili Peppers](https://fivethirtyeight.com/features/rating-chili-peppers-on-a-scale-of-1-to-oh-dear-god-im-on-fire/)
- Guinness Book of World Records on the [Hottest Chili](http://www.guinnessworldrecords.com/world-records/hottest-chili)

## Sanitization/analysis to-do

- Explore "heat" categorical. What are the cutoff scores for each category? Why is there no regular "hot?" Should there be?

- Examine the two heat measurement scales: JRP & SHU. Do they follow the same distribution? Do they share outliers?

![Alt Text](https://media.giphy.com/media/3oriO5w4cPs5SECFmU/giphy.gif)
