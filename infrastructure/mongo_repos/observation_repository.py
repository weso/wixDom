__author__ = 'guillermo'
from webindex.domain.model.observation.observation import Repository
from config import port, db_name, host
from .mongo_connection import connect_to_db
from .indicator_repository import IndicatorRepository
from .response_status import success
from .area_repository import AreaRepository


class ObservationRepository(Repository):
    def __init__(self):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)
        self._indicator = IndicatorRepository()
        self._area = AreaRepository()

    def find_observations(self, indicator_code=None, area_code=None, year=None):
        filters = []
        if indicator_code is not None:
            indicator_code = indicator_code.upper()

            # Check that the indicator exists
            indicator = self._db['indicators'].find_one({"indicator": indicator_code})

            if indicator is None:
                return self._indicator.indicator_error(indicator_code)

            filters.append({"indicator": indicator_code})

        if area_code is not None:
            area_code = area_code.upper()

            # Check that the area exists
            area = self._db['areas'].find_one({"iso3": area_code})

            if area is None:
                return self._area.area_error(area_code)

            filters.append({"area": area_code})

        if year is not None:
            filters.append({"year": year})

        search = {}

        if len(filters) > 0:
            search = {"$and": filters}

        observations = self._db["observations"].find(search)
        observation_list = []

        for observation in observations:
            observation_list.append(observation)

        return success(observation_list)