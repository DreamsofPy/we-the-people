import requests
import urllib

from apiclient.discovery import build
from urllib2 import URLError

API_KEY = 'AIzaSyDF8CmHI9LAKDuT7pOg3E-j9fsDnBWZ7A0'

class Elections(object):
    """
    Google Civic Information API Client Library.
    """

    def __init__(self):
        """
        Initialize standard values.
        """
        self.service = build('civicinfo', 'us_v1', developerKey=API_KEY)
        self.collection = self.service.elections()

    def get_elections(self):
        """
        Gets the list of available elections to query.

        Use this to provide an `election_id` to `get_voter_info`.
        """
        request = self.collection.electionQuery()

        try:
            response = request.execute()
        except URLError:
            response = {}

        return response.get('elections', [])

    def get_voter_info(self, election_id, address):
        """
        Looks up information for the `election_id` provided relevant to a voter
        based on the voter's registered `address`.
        """
        body = {'address': address}
        request = self.collection.voterInfoQuery(
            electionId=election_id,
            body=body
        )

        try:
            response = request.execute()
        except URLError:
            response = {}

        return response.get('contests', [])


def bing_query(query, issues = None, top=6):
    """Wrapper for bing news search"""

    key = "nvlGQnxPcpay6X4rWtEfvJJrX5aQXQL+/+p/7jZjgs0="
    result = {}
    for issue in issues:
        query_formatted = "%27" + query.replace(" ","%27")
        issue_formatted = "%27" + issue.replace(" ","%27")
        query_formatted += issue_formatted + "%27"

        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='
        url += query_formatted + "&$top=" + str(top) + '&$format=json'

        response = requests.get(url, auth=(key,key))
        response_json = response.json()

        result[issue] = response_json.get('d', 'No response').get('results', 'No response')

    return result


def tweets(tweets=None):
    # Test data
    if not tweets:
        tweets = ['I love barack obama', 'Obamas alright', 'I hate war', 
                  'I am in love', 'I have a positive outlook on life']

    endpoint = 'https://api.sentigem.com/external/get-sentiment?'
    key = 'cec3b93e5e83066c4fff43a94282b3055h8nOLzo14VDwHJZ9UmaWC-AxpN0gBFb'

    score = 0

    for tweet in tweets:
        text = {
            'api-key': key,
            'text': tweet
        }
        url = endpoint + urllib.urlencode(text)
        response = requests.get(url)
        response_json = response.json()

        # Polarity can either be positive, neutral, or negative
        polarity = response_json.get('polarity', 'neutral')

        if polarity == 'positive':
            score += 100
        elif polarity == 'neutral':
            score += 50

        print polarity

    score /= len(tweets)
    return score
