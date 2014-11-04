import rdflib
from infrastructure.mongo_repos.observation_repository import ObservationRepository

__author__ = 'miguel'


class RDFService(object):

    def __init__(self):
        self._obs_repo = ObservationRepository("127.0.0.1")

    def generate_dataset(self):
        observations_document = self._obs_repo.find_observations()
        if not observations_document["success"]:
            return

