__author__ = 'guillermo'
from abc import ABCMeta, abstractmethod
# =======================================================================================
# Repository


class Repository(object):
    """
    Abstract implementation of generic queries for managing observations.
    This will be sub-classed with an infrastructure specific implementation
    which will customize all the queries
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(Repository, self).__init__(**kwargs)

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