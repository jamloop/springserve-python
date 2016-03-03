
from . import _VDAPIService, _VDAPIResponse

class _DomainListResponse(_VDAPIResponse):
    """
    Override to give you access to the actual domains
    """

    def get_domains(self):
        return self._service.get("{}/domains".format(self.id))

class _DomainListAPI(_VDAPIService):

    __API__ = "domain_lists"
    __RESPONSE_OBJECT__ = _DomainListResponse

    
