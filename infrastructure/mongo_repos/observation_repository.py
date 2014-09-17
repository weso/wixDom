__author__ = 'guillermo'
from webindex.domain.model.observation.observation import Repository
from config import port, db_name, host
from .mongo_connection import connect_to_db
from .indicator_repository import IndicatorRepository
from .area_repository import AreaRepository
from utils import success


class ObservationRepository(Repository):
    def __init__(self, url_root):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)
        self._indicator = IndicatorRepository(url_root=url_root)
        self._area = AreaRepository(url_root=url_root)
        self._url_root = url_root

    def find_observations(self, indicator_code=None, area_code=None, year=None):
        filters = []

        if indicator_code is not None:
            # Check that the indicator exists
            indicator_filter = self.get_indicators_by_code(indicator_code)

            if indicator_filter is None:
                return self._indicator.indicator_error(indicator_code)

            filters.append(indicator_filter)

        if area_code is not None:
            area_filter = self.get_countries_by_code_name_or_income(area_code)

            if area_filter is None:
                return self._area.area_error(area_code)

            filters.append(area_filter)

        year_filter = self.get_years(year)

        if year_filter is not None:
            filters.append(year_filter)

        search = {}

        if len(filters) > 0:
            search = {"$and": filters}

        observations = self._db["observations"].find(search)
        observation_list = []

        for observation in observations:
            self.observation_uri(observation)
            self.set_observation_country_and_indicator_name(observation)
            observation_list.append(observation)

        return success(observation_list)

    def get_indicators_by_code(self, code):
        codes = code.upper().strip().split(",")

        for code in codes:
            # Check that the indicator exists
            indicator = self._db['indicators'].find_one({"indicator": code})

            if indicator is None:
                return None

        return {"indicator": {"$in": codes}}

    def get_countries_by_code_name_or_income(self, code):
        codes = code.split(",")

        country_codes = []

        for code in codes:
            code_upper = code.upper()

            # by ISO3
            countries = self._db["areas"].find({"iso3": code_upper})

            # by ISO2
            if countries is None or countries.count() == 0:
                countries = self._db["areas"].find({"iso2": code_upper})

            # by name
            if countries is None or countries.count() == 0:
                countries = self._db["areas"].find({"name": code})

            # by Continent

            if countries is None or countries.count() == 0:
                countries = self._db["areas"].find({"area": code})

            # by Income
            if countries is None or countries.count() == 0:
                countries = self._db["areas"].find({"income": code_upper})

            if countries is None or countries.count() == 0:
                return None

            for country in countries:
                iso3 = country["iso3"]
                country_codes.append(iso3)

        return {"area": {"$in": country_codes}}

    def get_years(self, year):
        if year is None:
            return None

        years = year.strip().split(",")

        year_list = []

        for year in years:
            interval = year.split("-")

            if len(interval) == 1 and interval[0].isnumeric():
                year_list.append(interval[0])
            elif len(interval) == 2 and interval[0].isnumeric() and interval[
                1].isnumeric():
                for i in range(int(interval[0]), int(interval[1]) + 1):
                    year_list.append(str(i))

        return {"year": {"$in": year_list}}

    def get_year_list(self):
        years = self._db['observations'].distinct("year")
        years.sort(reverse = True)

        year_list = []

        for year in years:
            year_list.append({
                "value": year
            })

        return success(year_list)

    def observation_uri(self, observation):
        indicator_code = observation["indicator"]
        area_code = observation["area"]
        year = observation["year"]
        observation["uri"] = "%sobservations/%s/%s/%s" % (self._url_root,
                                                          indicator_code, area_code, year)

    def set_observation_country_and_indicator_name(self, observation):
        indicator_code = observation["indicator"]
        area_code = observation["area"]

        indicator = self._db["indicators"].find_one({"indicator": indicator_code})
        area = self._db["areas"].find_one({"iso3": area_code})

        observation["indicator_name"] = indicator["name"]
        observation["area_name"] = area["name"]