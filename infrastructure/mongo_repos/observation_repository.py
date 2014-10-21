__author__ = 'guillermo'
from webindex.domain.model.observation.observation import Repository
from config import port, db_name, host
from .mongo_connection import connect_to_db
from .indicator_repository import IndicatorRepository
from .area_repository import AreaRepository
<<<<<<< HEAD
from utils import success, random_float
=======
from .visualization_repository import VisualizationRepository
from utils import success
>>>>>>> 6ea31b50ad378d912280b39143e414624bd1674f


class ObservationRepository(Repository):
    def __init__(self, url_root):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)
        self._indicator = IndicatorRepository(url_root=url_root)
        self._area = AreaRepository(url_root=url_root)
        self._visualization = VisualizationRepository(url_root=url_root)
        self._url_root = url_root

    def find_visualisations_new(self, indicator_code=None, area_code=None, year=None, max_bars=7):
        observations = self.find_observations(indicator_code, area_code, year)

        # Ranking bar chart and general (ALL) map
        barChart = self.find_observations(indicator_code, "ALL", year)

        # mean and median
        mean = 0
        median = []

        for observation in observations["data"]:
            value = observation["value"]
            mean += value
            median.append(value)

        length = len(observations["data"])
        mean = 0 if length <= 0 else mean / length
        median = self.getMedian(median)

        mean = round(mean, 2)
        median = round(median, 2)

        # higher and lower
        higher = observations["data"][0] if length > 0 else ""
        lower = observations["data"][length - 1] if length > 0 else ""

        # Get list of countries
        queryCountries = "ALL"

        if observations["success"] and area_code is not None and area_code != "ALL":
            areas = self.get_countries_by_code_name_or_income(area_code)

            queryCountries = areas["countries"]

        secondVisualisation = None
        byCountry = self.get_visualisations(observations, indicator_code, area_code, year, max_bars)
        years = self.get_year_array()

        if barChart["success"] and observations["success"]:
            # set selected countries
            for observation in barChart["data"]:
                if queryCountries == "ALL":
                   observation["selected"] = True
                else:
                    code = observation["code"]
                    observation["selected"] = code in queryCountries

            observations["data"] = {
                "observations": observations["data"],
                "bars": barChart["data"],
                "secondVisualisation": secondVisualisation,
                "mean": mean,
                "median": median,
                "higher": higher,
                "lower": lower,
                "byCountry": byCountry,
                "years": years
            }

        return observations

    def get_visualisations(self, observations, indicator_code, area_code, year, max_bars):
        if observations["success"] and area_code is not None and area_code != "ALL":
            areas = self.get_countries_by_code_name_or_income(area_code)

            queryCountries = areas["countries"]
            areas = areas["areas"]

            if areas is None:
                return self._area.area_error(area_code)

            previousRegion = areas[0]
            sameRegion = True

            for area in areas:
                if area != previousRegion:
                    sameRegion = False
                    break
                previousRegion = area

            region = previousRegion if sameRegion else "ALL"

        regionObservations = self.find_observations(indicator_code, region, year)

        # Several countries bar chart
        if regionObservations["success"]:
            data1 = observations["data"]
            data2 = regionObservations["data"]

            if len(data2) < max_bars - len(data1):
                data2 = data2 + self.find_observations(indicator_code, "ALL", year)["data"]

            processedCountries = []

            # Set selected field
            for observation in data1:
                observation["selected"] = True
                processedCountries.append(observation["code"])

            index = 0
            right = 0
            left = 0
            top = len(data2) - 1

            right_stopped = False
            left_stopped = False

            # data is completed with countries of the region (higher and lower)
            while len(data1) < max_bars:
                if right_stopped and left_stopped:
                    break

                if index % 2 == 0:
                    if right < len(data2):
                        if data2[right]["code"] not in processedCountries:
                            data1.append(data2[right])
                            processedCountries.append(data2[right]["code"])
                        right += 1
                    else:
                        right_stopped = True
                else:
                    pos = top - left
                    if pos >= 0 and pos < len(data2):
                        if data2[pos]["code"] not in processedCountries:
                            data1.append(data2[pos])
                            processedCountries.append(data2[pos]["code"])
                        left += 1
                    else:
                        left_stopped = True

                index += 1

            def sort_by_value(a, b):
                return cmp(b["value"], a["value"])

            data1.sort(sort_by_value)

            for observation in data1:
                observation["value"] = round(observation["value"], 2)

            # Several countries line chart

            # Get selected countries from previous query
            selectedCountries = []

            for observation in data1:
                country = observation["area"]
                selectedCountries.append(country)

            return self._visualization.get_visualizations(indicator_code, selectedCountries)

        return []

    def find_visualisations(self, indicator_code=None, area_code=None, year=None, max_bars=7):
        observations = self.find_observations(indicator_code, area_code, year)
        all_years = self.find_observations(indicator_code, area_code)["data"]

        observationsByCountry = self.group_observations_by_country(all_years)
        byCountry = observationsByCountry["byCountry"]
        years = observationsByCountry["years"]

        secondVisualisation = None

        queryCountries = "ALL"

        # Set continent info
        if observations["success"] and area_code == "ALL":
            secondVisualisation = list(observations["data"])

            for observation in secondVisualisation:
                area = observation["area"]
                area = self._db["areas"].find({ "iso3": area })

                for element in area:
                    observation["continent"] = element["area"]
                    observation["value"] = round(observation["value"], 2)
                    # We set ISO3 AS name
                    observation["name"] = element["iso3"]

        # Country visualisations
        if observations["success"] and area_code is not None and area_code != "ALL":
            areas = self.get_countries_by_code_name_or_income(area_code)

            queryCountries = areas["countries"]
            areas = areas["areas"]

            if areas is None:
                return self._area.area_error(area_code)

            previousRegion = areas[0]
            sameRegion = True

            for area in areas:
                if area != previousRegion:
                    sameRegion = False
                    break
                previousRegion = area

            region = previousRegion if sameRegion else "ALL"

            regionObservations = self.find_observations(indicator_code, region, year)

            # Several countries bar chart
            if regionObservations["success"]:
                data1 = observations["data"]
                data2 = regionObservations["data"]

                if len(data2) < max_bars - len(data1):
                    data2 = data2 + self.find_observations(indicator_code, "ALL", year)["data"]

                processedCountries = []

                # Set selected field
                for observation in data1:
                    observation["selected"] = True
                    processedCountries.append(observation["code"])

                index = 0
                right = 0
                left = 0
                top = len(data2) - 1

                right_stopped = False
                left_stopped = False

                # data is completed with countries of the region (higher and lower)
                while len(data1) < max_bars:
                    if right_stopped and left_stopped:
                        break

                    if index % 2 == 0:
                        if right < len(data2):
                            if data2[right]["code"] not in processedCountries:
                                data1.append(data2[right])
                                processedCountries.append(data2[right]["code"])
                            right += 1
                        else:
                            right_stopped = True
                    else:
                        pos = top - left
                        if pos >= 0 and pos < len(data2):
                            if data2[pos]["code"] not in processedCountries:
                                data1.append(data2[pos])
                                processedCountries.append(data2[pos]["code"])
                            left += 1
                        else:
                            left_stopped = True

                    index += 1

                def sort_by_value(a, b):
                    return cmp(b["value"], a["value"])

                data1.sort(sort_by_value)

                for observation in data1:
                    observation["value"] = round(observation["value"], 2)

                # Several countries line chart

                # Get selected countries from previous query
                selectedCountries = ""

                for observation in data1:
                    country = observation["area"]

                    if selectedCountries != "":
                        selectedCountries += ","

                    selectedCountries += country

                timeObservations = self.find_observations(indicator_code, selectedCountries, None)

                if timeObservations["success"]:
                    secondVisualisation = self.group_observations_by_country(timeObservations["data"])
                    byCountry = secondVisualisation["byCountry"]
                    years = secondVisualisation["years"]

        # Ranking bar chart and general (ALL) map
        barChart = self.find_observations(indicator_code, "ALL", year)

        # mean and median
        mean = 0
        median = []

        for observation in observations["data"]:
            value = observation["value"]
            mean += value
            median.append(value)

        length = len(observations["data"])
        mean = 0 if length <= 0 else mean / length
        median = self.getMedian(median)

        mean = round(mean, 2)
        median = round(median, 2)

        # higher and lower
        higher = observations["data"][0] if length > 0 else ""
        lower = observations["data"][length - 1] if length > 0 else ""

        if barChart["success"] and observations["success"]:
            # set selected countries
            for observation in barChart["data"]:
                if queryCountries == "ALL":
                   observation["selected"] = True
                else:
                    code = observation["code"]
                    observation["selected"] = code in queryCountries

            observations["data"] = {
                "observations": observations["data"],
                "bars": barChart["data"],
                "secondVisualisation": secondVisualisation,
                "mean": mean,
                "median": median,
                "higher": higher,
                "lower": lower,
                "byCountry": byCountry,
                "years": years
            }

        return observations

    def find_observations(self, indicator_code=None, area_code=None, year=None):
        filters = []

        if indicator_code is not None:
            # Check that the indicator exists
            indicator_filter = self.get_indicators_by_code(indicator_code)

            if indicator_filter is None:
                return self._indicator.indicator_error(indicator_code)

            filters.append(indicator_filter)

        if area_code is not None and area_code != "ALL":
            area_filter = self.get_countries_by_code_name_or_income(area_code)

            if area_filter is not None:
                area_filter = area_filter["area_filter"]

            if area_filter is None:
                return self._area.area_error(area_code)

            filters.append(area_filter)

        year_filter = self.get_years(year)

        if year_filter is not None:
            filters.append(year_filter)

        search = {}

        if len(filters) > 0:
            search = {"$and": filters}

        observations = self._db["observations"].find(search).sort("value", -1)
        observation_list = []

        for observation in observations:
            self.observation_uri(observation)
            self.set_observation_country_and_indicator_name(observation)
            observation_list.append(observation)
            # Extra info
            observation["code"] = observation["area"]
            observation["name"] = observation["area_name"]
            #observation["values"] = [ round(observation["value"], 2) ]
            #observation["previous-value"] = self.get_previous_value(observation)

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
        areas = []

        for code in codes:
            code_upper = code.upper()

            # by ISO3
            countries = self._db["areas"].find({ "$and": [{"iso3": code_upper}, { "area": { "$ne": None } }] })

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
                area = country["area"]
                areas.append(area)

        return {
            "area_filter": {"area": {"$in": country_codes}},
            "areas": areas,
            "countries": country_codes
        }

    def get_years(self, year):
        if year is None:
            return None

        years = year.strip().split(",")

        year_list = []

        for year in years:
            interval = year.split("-")

            if len(interval) == 1 and interval[0].isdigit():
                year_list.append(interval[0])
            elif len(interval) == 2 and interval[0].isdigit() and interval[
                1].isdigit():
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

    def get_year_array(self):
        years = self._db['observations'].distinct("year")
        years.sort(reverse = True)

        return success(years)

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

    def insert_observation(self, observation, observation_uri=None, area_iso3_code=None, indicator_code=None,
                           year_literal=None, area_name=None, indicator_name=None, previous_value=None,
                           year_of_previous_value=None, republish=None):
        """
        It takes the info of indicator and area through the optional params area_iso3_code,
        indicator_code and year_literal
        :param observation:
        :param area_iso3_code:
        :param indicator_code:
        :param year_literal:
        :return:
        """
        norm_value = self._look_for_computation("normalized", observation)

        observation_dict = {}
        observation_dict['_id'] = observation.id
        observation_dict['normalized'] = norm_value
        observation_dict['area'] = area_iso3_code
        observation_dict['area_name'] = area_name
        observation_dict['indicator'] = indicator_code
        observation_dict['indicator_name'] = indicator_name
        observation_dict['value'] = observation.value
        observation_dict['year'] = str(observation.ref_year.value)
        observation_dict['values'] = [norm_value]  # An array of one element
        observation_dict['uri'] = observation_uri
        observation_dict['previous_value'] = self._build_previous_value_object(previous_value, year_of_previous_value)
        observation_dict['republish'] = republish
        observation_dict['scored'] = self._look_for_computation("scored", observation)

        self._db['observations'].insert(observation_dict)

    def normalize_plain_observation(self, area_iso3_code=None, indicator_code=None, year_literal=None,
                                    normalized_value=None):
        observation = self.find_observations(indicator_code=indicator_code, area_code=area_iso3_code, year=year_literal)
        if observation["success"] and len(observation["data"]) > 0:
            observation = observation["data"][0]
            observation['normalised'] = normalized_value
            self._db['observations'].update({'_id':observation["_id"]}, {"$set": observation}, upsert=False)

    @staticmethod
    def _build_previous_value_object(value, year):
        if value is None or year is None:
            return None
        else:
            return {'value': value, 'year': str(year)}


    @staticmethod
    def _look_for_computation(comp_type, observation):
        for comp in observation.computations:
            if comp.comp_type == comp_type:
                return comp.value

        ### This lines are here temporally, for fake data
        if comp_type == "normalized":
            return random_float(-4, 4)
        elif comp_type == "scored" and observation.obs_type != "raw":
            return random_float(1, 99)
        ###

        return None


    def group_observations_by_country(self, observations):
        years = []

        grouped_by_country = {}

        for observation in observations:
            country = observation["area"]
            country_name = observation["area_name"]
            year = observation["year"]

            if year not in years:
                years.append(year)

            if country not in grouped_by_country:
                grouped_by_country[country] = {
                    "name": country_name,
                    "code": country,
                    "observations": {}
                }

            grouped_by_country[country]["observations"][year] = observation

        years.sort()
        series = []
        byCountry = {}

        for country in grouped_by_country:
            values = []

            for year in years:
                observation = grouped_by_country[country]["observations"][year] if grouped_by_country[country]["observations"][year] else None
                value = observation["value"] if observation else None
                value = round(value, 2) if value else None
                values.append(value)

            code = grouped_by_country[country]["code"]

            serie = {
                "name": grouped_by_country[country]["name"],
                "code": code,
                "values": values
            }

            series.append(serie)

            byCountry[code] = serie

        return {
            "series": series,
            "years": years,
            "byCountry": byCountry
        }

    def getMedian(self, numericValues):
        theValues = sorted(numericValues)

        if len(theValues) == 0:
            return 0
        elif len(theValues) % 2 == 1:
            return theValues[(len(theValues)+1)/2 - 1]
        else:
            lower = theValues[len(theValues)/2 - 1]
            upper = theValues[len(theValues)/2]
            return (float(lower + upper)) / 2

    # def get_previous_value(self, observation):
    #     country = observation["area"]
    #     indicator = observation["indicator"]
    #     year = observation["year"]
    #     value = float(observation["value"])
    #     previousYear = str(int(year) - 1)
    #
    #     filter = { "$and": [
    #         {
    #             "area": country
    #         },
    #         {
    #             "indicator": indicator
    #         },
    #         {
    #             "year": previousYear
    #         }
    #     ]}
    #
    #     previousObservation = indicator = self._db["observations"].find_one(filter)
    #
    #     if previousObservation:
    #         previousValue = float(previousObservation["value"])
    #
    #         tendency = 0
    #
    #         if value > previousValue:
    #             tendency = 1
    #
    #         if value < previousValue:
    #             tendency = -1
    #
    #         return {
    #             "value": previousObservation["value"],
    #             "tendency": tendency
    #         }
    #
    #     return None
