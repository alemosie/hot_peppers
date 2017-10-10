# Hot Peppers

A fun side project exploring hot peppers!

I grew up with very little spice in my diet -- my mother is Irish, what can I say? -- and get regularly mocked for my lack of spice tolerance. I figured that I'd do some research into these nuggets of suffering and glory so that the next time I am prompted to eat a pepper, I can distract my mocking friends enough to escape the actual act of pepper consumption.

## Data

Data is from [PepperScale's Hot Pepper List](https://www.pepperscale.com/hot-pepper-list/).

I used Python, [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), and [Pandas](https://pandas.pydata.org/pandas-docs/stable/) to extract, sanitize, and convert the data into `data/peppers.json`, available for your enjoyment.

### Background

The data is from [PepperScale](https://www.pepperscale.com), a website that seems to be entirely dedicated to the topic of peppers. I have no affiliation with the site, but am grateful for their work!

Pepper hotness is based on the **Scoville Scale**, a measurement of the pungency chili peppers running from mild to extreme. If you're interested in the scale -- along with its many pros and cons -- I recommend you read PepperScale's article on the subject [here](https://www.pepperscale.com/what-is-the-scoville-scale/), or trusty [Wikipedia](https://en.wikipedia.org/wiki/Scoville_scale).

### Schema

Field | Description
--- | ---
"name"| Name of the pepper; unique
"species" | Pepper species. All hot peppers belong to the Capsicum genus (part of the nightshade family), but there are multiple species within it.
"heat" | How hot the pepper is perceived to be: "Mild", "Medium", "Extra Hot", "Super Hot" ([their](https://www.pepperscale.com/hot-pepper-list/) categories, not mine)
"region" | Region of the world in which the pepper grows; based off of provided origin
"origin" | Origin of the pepper
"min_shu" | The mildest a pepper could be, recorded in [Scoville heat units (SHU)](https://www.pepperscale.com/scoville-heat-units/)
"max_shu" | The hottest a pepper could be, recorded in [Scoville heat units (SHU)](https://www.pepperscale.com/scoville-heat-units/)
"min_jrp" | Jalapeño Reference Point (JRP); minimum recorded value for number of times hotter than a jalapeño the pepper in question is. A negative number is milder than a jalapeño; a positive number is hotter than a jalapeño.
"max_jrp" | Jalapeño Reference Point (JRP); maximum recorded value for number of times hotter than a jalapeno the pepper in question is. A negative number is milder than a jalapeño; a positive number is hotter than a jalapeño.
"link" | PepperScale article containing more information on the pepper


![Alt Text](https://media.giphy.com/media/3oriO5w4cPs5SECFmU/giphy.gif)
