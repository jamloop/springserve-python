
from . import _VDAPIService, _VDAPIResponse, _VDAPIMultiResponse

from datetime import datetime

import pandas

class _ReportingResponse(_VDAPIMultiResponse):
    
    def to_dataframe(self):
        return pandas.DataFrame(self.raw)

class _ReportingAPI(_VDAPIService):

    __API__ = "report"
    __RESPONSES_OBJECT__ = _ReportingResponse
    
    INTERVALS = ("hour", "day", "cumulative")

    def _format_date(self, date):
        
        if isinstance(date, datetime):
            return date.strftime("%Y-%m-%d")
        return date
    
    def run(self, start_date, end_date, interval=None, dimensions=None):
        payload = {
            'start_date': self._format_date(start_date),
            'end_date': self._format_date(end_date),
        }

        if interval:
            if interval not in self.INTERVALS:
                raise Exception("not a valid interval")
            payload['interval'] = interval

        if dimensions:
            payload['dimensions'] = dimensions

        return self.post(data=payload)


 
