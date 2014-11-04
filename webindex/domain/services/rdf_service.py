import rdflib

__author__ = 'miguel'


class RDFService(object):

    def __init__(self, area_repository, indicator_repository):
        self._area_repository = area_repository
        self._indicator_repository = indicator_repository

    def generate_dataset(self, graph, observations):
        for observation in observations:
            self._process_observation(observation, graph)
        return graph  # We will see if this is the thing to return or not

    def _process_observation(self, observation, graph):
        self._add_country_triplets(observation, graph)
        self._add_indicator_triplets(observation, graph)
        self._add_observation_triplets(observation, graph)




