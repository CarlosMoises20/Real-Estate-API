from abc import ABC
import time, requests


"""
This is the abstract class used to retrieve relevant data from a specific API

This includes the url, parameters and headers
It also includes the method get_source_data, which will be used by all the subclasses representing 
each one a different API, to get the data from the API through the indicated URL, and using the optionally
indicated parameters and headers

"""
class BaseSourceDataRetrieval(ABC):
    
    """
    Constructor
        # url: url of the api
        # params: parameters of the api
        # headers: headers of the api
        
    """
    def __init__(self, url, params=None, headers=None):
        self._url = url
        self._params = params
        self._headers = headers
    
    """Retrieve data from an indicated source, using the url, parameters and headers indicated in the constructor"""
    def get_source_data(self, retries=5):
        
        for attempt in range(retries):
            try:
                response = requests.get(url=self._url, params=self._params, headers=self._headers, timeout=(10, 60))
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException:
                if attempt == retries - 1:
                    raise
    
                wait = 2 ** attempt
                print(f"Request failed. New attempt in {wait}s...")
                time.sleep(wait)
    
    
    