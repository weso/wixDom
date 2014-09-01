__author__ = 'guillermo'
from webindex.domain.model.area import region
from config import port, db_name, host
from .mongo_connection import connect_to_db
from response_status import error


class AreaRepository(region.Repository):
    """Concrete mongodb repository for Areas.
    """

    def __init__(self):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)

    def find_countries_by_code(self, area_code):
        area_code_upper = area_code.upper()
        area = self._db['areas'].find_one({"$or": [{"iso3": area_code},
                                                   {"iso3": area_code_upper},
                                                   {"iso2": area_code},
                                                   {"iso2": area_code_upper},
                                                   {"name": area_code}]})
        return area

    def find_continents(self):
        areas = self._db['areas'].find({"area": None})
        continents = []

        for continent in areas:
            name = continent["name"]
            continent["countries"] = self._db['areas'].find({"area": name})
            continents.append(continent)

        return continents

    def find_countries(self):
        countries = self._db['areas'].find({"area": {"$ne": None}})
        return countries

    def area_error(self, area_code):
        return error("Invalid Area Code: {}".format(area_code))

    def areas_where(self, predicate, area_ids=None):
        pass
