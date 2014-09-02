__author__ = 'guillermo'
from webindex.domain.model.indicator.indicator import Repository
from config import port, db_name, host
from .mongo_connection import connect_to_db
from response_status import error


class IndicatorRepository(Repository):
    """Concrete mongodb repository for Indicators.
    """

    def __init__(self):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)

    def find_indicator_by_code(self, indicator_code):
        indicator_code = indicator_code.upper()
        indicator = self._db['indicators'].find_one({"indicator": indicator_code})

        if indicator is None:
            return None

        children = self.find_indicator_children(indicator_code)
        indicator["children"] = children
        return indicator

    def find_indicators_index(self):
        return self.find_indicators_by_level("Index")

    def find_indicators_sub_indexes(self):
        return self.find_indicators_by_level("Subindex")

    def find_indicators_components(self, parent=None):
        return self.find_indicators_by_level("Component", parent)

    def find_indicators_primary(self, parent=None):
        return self.find_indicators_by_level("Primary", parent)

    def find_indicators_secondary(self, parent=None):
        return self.find_indicators_by_level("Secondary", parent)

    def find_indicator_indicators(self, parent=None):
        primary = self.find_indicators_primary(parent)
        secondary = self.find_indicators_secondary(parent)
        primary.append(secondary)
        return primary

    def find_indicators_by_level(self, level, parent=None):
        search = {"type": level}

        if parent is not None:
            code = parent["indicator"]
            _type = parent["type"].lower()
            _filter = {}
            _filter[_type] = code
            search = {"$and": [search, _filter]}

        indicators = self._db["indicators"].find(search)

        processed_indicators = []

        for indicator in indicators:
            code = indicator["indicator"]
            children = self.find_indicator_children(code)
            indicator["children"] = children
            processed_indicators.append(indicator)

        return processed_indicators

    def find_indicator_children(self, ind):
        indicators = self._db["indicators"].find({"parent": ind})
        processed_indicators = []

        for ind in indicators:
            code = ind["indicator"]
            children = self.find_indicator_children(code)
            ind["children"] = children
            processed_indicators.append(ind)

        return processed_indicators

    def indicator_error(self, indicator_code):
        return error("Invalid Indicator Code: %s" % indicator_code)



