from abc import ABC
import requests


"""
This is the abstract class used to retrieve relevant data from a specific API

This includes the url, parameters and headers
It also includes the method get_api_data, which will be used by all the subclasses representing 
each one a different API, to get the data from the API through the indicated URL, and using the optionally
indicated parameters and headers

"""
class BaseApiDataRetrieval(ABC):
    
    # Constructor
    # url: url of the api
    # params: parameters of the api
    # headers: headers of the api
    def __init__(self, url, params=None, headers=None):
        self._url = url
        self._params = params
        self._headers = headers
    
    """Retrieve data from an API."""
    def get_api_data(self, timeout=45):
        response = requests.get(url=self._url, params=self._params, headers=self._headers, timeout=timeout)
        response.raise_for_status()
        return response
    
    
    