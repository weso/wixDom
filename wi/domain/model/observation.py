__author__ = 'guillermo'

from wi.domain.model.entity import Entity
from abc import ABCMeta, abstractmethod
import uuid

# =======================================================================================
# Observation aggregate root entity
#


class Observation(Entity):
    """ Observation root entity
    """
    def __init__(self, obs_id, obs_version, ref_area, ref_year):
        super(Observation, self).__init__(obs_id, obs_version)
        self._ref_area = ref_area
        self._ref_year = ref_year

    def __repr__(self):
        """
        Checks if an object is discarded or not
        """
        return "{d}Observation(id={id!r}, ref_area={ref_area!r}, ref_year={ref_year!r})".\
            format(d="*Discarded* " if self._discarded else "", id=self._id,
                   ref_area=self._ref_area, ref_year=self._ref_year)

    @property
    def obs_area(self):
        """
        Checks for object's properties
        """
        self._check_not_discarded()
        return self._ref_area

    @obs_area.setter
    def obs_area(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation area cannot be empty")
        self._ref_area = value
        self._increment_version()

    @property
    def obs_year(self):
        """
        Checks for object's properties
        """
        self._check_not_discarded()
        return self._ref_year

    @obs_year.setter
    def obs_year(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation year cannot be empty")
        self._ref_year = value
        self._increment_version()

# =======================================================================================
# Related Entities

# =======================================================================================
# Factories - Aggregate root factory


def create_observation(ref_area, ref_year):
    """
    Factory for creating observations
    """
    observation = Observation(obs_id=uuid.uuid4().hex, obs_version=0, ref_area=ref_area,
                              ref_year=ref_year)
    return observation

# =======================================================================================
# Mutators

# =======================================================================================
# Repository


class ObservationRepository(object):
    """
    Abstract implementation of generic queries for managing observations.
    This will be sub-classed with an infrastructure specific implementation
    which will customize all the queries
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ObservationRepository, self).__init__(**kwargs)

    def all_observations(self, obs_ids=None):
        return self.observations_where(lambda obs: True, obs_ids)

    def observation_from_area(self, ref_area, obs_ids=None):
        return self.observations_where(lambda obs: obs.ref_area == ref_area, obs_ids)

    def observation_with_id(self, obs_id):
        try:
            return self.all_observations(obs_id)
        except ValueError:
            print "No Observation with id {}".format(obs_id)
            raise

    @abstractmethod
    def observations_where(self, predicate, obs_ids=None):
        """
        Subclass implementations must override at least this method
        """
        raise NotImplementedError

# =======================================================================================
# Exceptions