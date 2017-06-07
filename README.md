I decided to create this project to make myself more comfortable with Python. The idea was to analyze Stanley Cup fans activity in Twitter and to reveal the most discussed teams.
To begin with, I made a list of Stanley Cup teams and their home cities:

* Montreal Canadiens
* **Ottawa Senators**
* Boston Bruins
* Washington Capitals
* **Pittsburgh Penguins**
* Columbus Blue Jackets
* New York Rangers
* Toronto Maple Leafs
* Chicago Blackhawks
* Minnesota Wild
* St. Louis Blues
* **Anaheim Ducks**
* Edmonton Oilers
* San Jose Sharks
* Calgary Flames
* **Nashville Predators**

For the beginning I chose 5 teams who played with Ottawa Senators (highlighted in the list). The reason to choose Ottawa as a starting point was that it could be comparable with cities of relatively same size. Comparing tweets from Ottawa to tweets from NYC, for example, would not be fair, because it’s population is 10 times different. Also limiting the scope to five cities could help me to validate my idea.

I explored Twitter search query parameters and wrote an example query:

```
Senators OR Sens near:"Ottawa, Ontario" within:15mi since:2017-05-25 until:2017-05-26
```

I realized that `since` and `until` parameters could help me to limit search results to the day of the game and also the day before and after.
The next step was to find the right search keywords (it was not too hard):

```
Senators OR Sens OR #GoSens
Penguins OR Pens OR #GoPens
Predators OR Preds OR #GoPreds
Anaheim Ducks OR #NHLDucks OR #LetsGoDucks
```

In the API documentation I found that `near:"Ottawa, Ontario"` parameter only works from the web search, but not in the API:

> the search operator “near” isn’t available in the API

I had to pass `geocode` parameter with the city coordinates: `geocode: 45.2502975,-76.0804397, 15mi` (coordinates for Ottawa). I had to find coordinates for each city in my list.

To access Twitter API I found two Python libraries: `tweepy` and `python-twitter`. Turned out that the tweepy library only supports OAuth tokens and for this project I needed library that would work with consumer and access tokens. Eventually I switched to python-twitter library.

I looked into search API response format:

```json
{
  "statuses": [
    "... array of statuses"
  ],
  "search_metadata": {
    "max_id": 250126199840518145,
    "since_id": 24012619984051000,
    "refresh_url": "?since_id=250126199840518145&q=%23freebandnames&result_type=mixed&include_entities=1",
    "next_results": "?max_id=249279667666817023&q=%23freebandnames&count=4&include_entities=1&result_type=mixed",
    "count": 4,
    "completed_in": 0.035,
    "since_id_str": "24012619984051000",
    "query": "%23freebandnames",
    "max_id_str": "250126199840518145"
  }
}
```

The response metadata has `count` parameter which I intended to use to estimate fans activity per every team. I wrote a script that iterates over every team and builds the search API query. Then I found out that the “count” field had a value per page not per query. As a result I couldn’t get the count per query with a single API call. To calculate the tweets count for each search query I needed to make tremendous number of API calls that would eventually go over Twitter API limit which is 450 requests per 15 minutes.

My idea to count tweets per team and location didn’t work out, but I learned a lot from it:

* How to create Twitter application and get tokens;
* Got familiar with Twitter libraries for Python;
* Got familiar with search query structure and Twitter API response;
* Got familiar with API limitations;
