from requests.models import PreparedRequest
from urllib.parse import urljoin

# Build out the API string


def buildRequest(url, endpoint, queryParams):
    requestGenerator = PreparedRequest()
    requestGenerator.prepare_url(url=urljoin(url, endpoint), params=queryParams)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    url = requestGenerator.url
    return url, headers
