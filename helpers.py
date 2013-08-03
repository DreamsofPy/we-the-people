import requests

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
