__author__ = 'guillermo'
from wi.domain.model.observation.repository import Repository


class ObservationRepository(Repository):
    """ Concrete Observations repository for MongoDB persistence
    """
    
    def observations_where(self, predicate, obs_ids=None):
        pass