import requests

from apiclient.discovery import build

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
        response = request.execute()
        return response

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
        response = request.execute()
        return response


def bing_query(query, issue = None, top=6):
    """Wrapper for bing news search"""

    key = "nvlGQnxPcpay6X4rWtEfvJJrX5aQXQL+/+p/7jZjgs0="

    query_formatted = "%27" + query.replace(" ","%27")
    issue_formatted = "%27" + issue.replace(" ","%27")
    query_formatted += issue_formatted + "%27"

    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='
    url += query_formatted + "&$top=" + str(top) + '&$format=json'

    response = requests.get(url, auth=(key,key))
    response_json = response.json()

    result = qpp =qp.json().get('d', 'No response').get('results', 'No response')

    return result
