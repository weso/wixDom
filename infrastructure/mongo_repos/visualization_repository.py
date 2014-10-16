__author__ = 'Dani'

from config import port, db_name, host
from .mongo_connection import connect_to_db
from utils import normalize_group_name


class VisualizationRepository(object):
    """
    This is the only class of this package that does not have inheritance relationships.
    It does not represent an entity, but an abstract group of data handy only for visualizations.
    """


    def __init__(self, url_root):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)
        self._url_root = url_root
        self._FIRST_YEAR, self._LAST_YEAR = self._get_first_and_last_year()

    @staticmethod
    def _get_first_and_last_year():
        # I am still thinking if im going to consume an API method to discover this data
        # or config, or constants, or params or what...
        return 2007, 2014

    def insert_visualization(self, observations, area_iso3_code, area_name, indicator_code, indicator_name):
        visualization_dict = {}
        visualization_dict['area'] = area_iso3_code
        visualization_dict['area_name'] = area_name
        visualization_dict['indicator'] = normalize_group_name(indicator_code)
        visualization_dict['indicator_name'] = indicator_name
        visualization_dict['values'] = self._build_values_object(observations)

        self._db['visualizations'].insert(visualization_dict)

    def _build_values_object(self, observations):
        """
        It receives a list of observations and return an array with as many positions as the total number
        of available years stored in the system. Each position of the array will represent the value of a year.
        Example: if we had 2002, 2003, 2004, 2005 and 2006 as available years and we receive and array of 3
        observations with years and values as follows: 2003 --> 3, 2004 --> 4, 2006 --> 6, then the method
         will return an array such as: [None, 3, 4, None, 6]

        :param observations:
        :return:
        """

        result = []
        for i in range(self._FIRST_YEAR, self._LAST_YEAR + 1):
            result.append(self._look_for_a_value_for_a_year(i, observations))  # The method could return None. NP =)
        return result


    @staticmethod
    def _look_for_a_value_for_a_year(year_target, observations):
        for obs in observations:
            year_obs = obs.ref_year.value
            if str(year_obs) == str(year_target):
                return obs.value
        return None  # No observation found for target_year in this list