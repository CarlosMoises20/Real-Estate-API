from abc import ABC
import requests

class BaseApiDataRetrieval(ABC):
    
    # Constructor
    # url: url of the api
    # params: parameters of the api
    # headers: headers of the api
    def __init__(self, url, params=None, headers=None):
        self._url = url
        self._params = params
        self._headers = headers
    
    """Retrieve data from an API.
    NOTE: If, in the future, new APIs are added and these use a different data format than JSON,
    this method is adaptable to retrieve the data.
    
    """
    def get_api_data(self, timeout=45):
        response = requests.get(url=self._url, params=self._params, headers=self._headers, timeout=timeout)
        response.raise_for_status()
        return response
    
    
    