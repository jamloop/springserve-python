
#import all of this version information
__version__ = '0.0.1'
__author__ = 'dave@springserve.com'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Springserve'
__title__ = 'springserve'


import sys as _sys
import json as _json

from link import lnk as _lnk

_API = None

def API():
    global _API

    if _API is None:
       _API = _lnk.apis.springserve_optimization
    
    return _API

class _TabComplete(object):
    """
    this class exists to make any other class 
    have a tab completion function that is already 
    hooked into ipython 
    """
    def _tab_completions(self):
        return []


class _VDAPIResponse(_TabComplete):

    def __init__(self, service, api_response):
        super(_VDAPIResponse, self).__init__()
        self._service = service
        self._raw_response = api_response
    
    def __iter__(self):
        if isinstance(self.raw, list):
            for x in self.raw:
                yield self._service.__RESPONSE_OBJECT__(self._service, x)
        else:
            yield self

    @property
    def raw(self):
        return self._raw_response

    def __getitem__(self, key):

        if isinstance(key, str):
            return self._raw_response[key]

    def __getattr__(self, key):
        """
        This is where the magic happens that allows you to treat this as an
        object that has all of the fields that the api returns.  I seperate all
        of the returned data in self._data
        """

        # if it's not there then try to get it as an attribute
        try:
            return self.__getattribute__(key)
        except AttributeError as e:
            return self._raw_response[key]
    
    def _tab_completions(self):

        if not self.raw:
            return []

        return self.raw.keys()

    def __setattr__(self, attr, value):
        """
        If it's a property that was already defined when the class
        was initialized that let it exist.  If it's new than let's slap it into
        _data.  This allows us to set new attributes and save it back to the api
        """
        # allows you to add any private field in the init
        # I could do something else here but I think it makes
        # sense to enforce private variables in the ConsoleObject
        if attr.startswith('_'):
            self.__dict__[attr] = value

        if attr in self.__dict__:
            self.__dict__[attr] = value
        else:
            # TODO - this is the only place where appnexus object fields get changed?
            self._raw_response[attr] = value
    
    def save(self):
        return self._service.put(self.id, self.raw)

def _format_url(endpoint, path_param, query_params):

    _url = endpoint

    if path_param:
        _url += "/{}".format(path_param)

    if query_params and isinstance(query_params, dict):
        params = "&".join(["{}={}".format(key, value) for key,value in
                           query_params.iteritems()])
        _url += "?{}".format(params)

    return _url
 
class _VDAPIService(object):
    
    __API__ = None
    __RESPONSE_OBJECT__ = _VDAPIResponse
    
    def __init__(self):
        pass 

    @property
    def endpoint(self):
        return "/" + self.__API__
    
   
    def build_response(self, api_response):
        return self.__RESPONSE_OBJECT__(self, api_response.json)

    def get(self, path_param=None, query_params=None):
        global API
        return self.build_response(
                API().get(_format_url(self.endpoint, path_param, query_params))
        )
    
    def put(self, path_param, data, query_params=None):
        global API
        return self.build_response(
                API().put(_format_url(self.endpoint, path_param, query_params),
                          data = _json.dumps(data)
                         )
        )
 

from _supply import _SupplyTagAPI
from _demand import _DemandTagAPI
from _common import _DomainListAPI

supply_tags = _SupplyTagAPI()
demand_tags = _DemandTagAPI()
domain_lists = _DomainListAPI()


def raw_get(path_param, query_params=None):
    global API
    return API().get(_format_url("", path_param, query_params)).json


def _install_ipython_completers():  # pragma: no cover

    from IPython.utils.generics import complete_object

    @complete_object.when_type(_TabComplete)
    def complete_report_object(obj, prev_completions):
        """
        Add in all the methods of the _wrapped object so its
        visible in iPython as well
        """
        prev_completions+=obj._tab_completions()
        return prev_completions


# Importing IPython brings in about 200 modules, so we want to avoid it unless
# we're in IPython (when those modules are loaded anyway).
# Code attributed to Pandas, Thanks Wes 
if "IPython" in _sys.modules:  # pragma: no cover
    try:
        _install_ipython_completers()
    except Exception:
        msg.debug("Error loading tab completers")
        pass 

