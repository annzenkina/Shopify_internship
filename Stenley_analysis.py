import twitter
import urllib

api = twitter.Api(consumer_key='secret',
                  consumer_secret='secret',
                  access_token_key='secret',
                  access_token_secret='secret')

def GetSearch(client, raw_query):
    url = '%s/search/tweets.json' % client.base_url
    parameters = {}

    if raw_query is not None:
        url = "{url}?{raw_query}".format(
            url=url,
            raw_query=raw_query)
        print(url)
        resp = client._RequestUrl(url, 'GET')
    else:
        resp = client._RequestUrl(url, 'GET', data=parameters)

    data = client._ParseAndCheckTwitter(resp.content.decode('utf-8'))
    metadata = data.get('search_metadata')

    return {
        'tweets': [twitter.Status.NewFromJsonDict(x) for x in data.get('statuses', '')],
        'count': metadata
    }


cities = [
    {
        'city': 'Ottawa',
        'team': 'Ottawa Senators',
        'coords': ['45.2502975','-76.0804397', '15mi'],
        'query': 'Senators OR Sens OR #GoSensGo since:2017-05-24 until:2017-05-26'
    },
    {
        'city': 'Pittsburgh',
        'team': 'Pittsburgh Penguins',
        'coords': ['40.431478','-80.0505405', '15mi'],
        'query': 'Penguins OR Pens OR #GoPens since:2017-05-24 until:2017-05-26',
    },
    {
        'city': 'Nashville',
        'team': 'Nashville Predators',
        'coords': ['36.1868683','-87.0654327', '15mi'],
        'query': 'Predators OR Preds OR #GoPreds since:2017-05-21 until:2017-05-23',
    },
    {
        'city': 'Anaheim',
        'team': 'Anaheim Ducks',
        'coords': ['34.0802382','-118.8013119', '15mi'],
        'query': 'AnaheimDucks OR #NHLDucks OR #LetsGoDucks since:2017-05-21 until:2017-05-23',
    }
]

for item in cities:
    query = 'geocode:' + ','.join(item['coords']) + ' ' + item['query']
    query_params = { 'q': query, 'result_type': 'recent'}
    results = GetSearch(api, raw_query=urllib.parse.urlencode(query_params))
    print(query)
    print(results['count'])
