"""
Filter criteria that can be applied to documents
"""

from dateutil.parser import parse as parse_date


class Filter():

    def __call__(self, item: list):
        raise NotImplementedError

    def apply(self, items: any):
        return [item for item in items if self(item)]


class DateFilter(Filter):
    
    def __init__(self, after=None, before=None):
        self._after = parse_date(after) if after else None
        self._before = parse_date(before) if before else None
        
    def _get_date(self, item: any):
        raise NotImplementedError

    def __call__(self, item: any):
        d = self._get_date(item)
        if self._after and self._after > d:
            return False
        if self._before and self._before < d:
            return False
        return True


class PublicationDateFilter(DateFilter):
    
    def _get_date(self, item: any):
        return parse_date(getattr(item, "publication_date"))


class FilingDateFilter(DateFilter):
    
    def _get_date(self, item: any):
        return parse_date(getattr(item, "filing_date"))


class PriorityDateFilter(DateFilter):
    
    def _get_date(self, item: any):
        return parse_date(getattr(item, "priority_date"))


class DocTypeFilter(Filter):
    
    def __init__(self, doctype):
        self._type = doctype
    
    def __call__(self, item: any):
        return getattr(item, "type") == self._type
