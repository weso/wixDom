# import rdflib
from namespaces_handler import *
from rdflib.namespace import RDF

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
        #The next two dicts will be used to check if the triples of certain country/indicator
        #had already been added to the graph. It will make a faster execution.
        countries_added_dict = {}
        indicatros_added_dict = {}
        self._add_country_triples(observation, graph, countries_added_dict)
        self._add_indicator_triples(observation, graph, indicatros_added_dict)
        self._add_observation_triples(observation, graph)


    def _add_country_triples(self, observation, graph, countries_dict):
        if observation['area'] in countries_dict:
            return  # It means that the triplets of this country had already been added

        countries_dict[observation['area']] = True  # It means we are adding this country triplets
                                                    # The next attempt over this country will return
                                                    # without computing nothing
        country_dict = self._find_country_dict(observation['area'])
        country_term = example.term(observation['area'])
        graph.add(country_term,
                  RDF.type,
                  cex.term("Area"))
        graph.add((example.term()))

        ### [And the rest os possible country triples]




    def _find_country_dict(self, iso3_code):
        result = self._area_repository.find_countries_by_code_or_income(iso3_code)['data']
        if result is None:
            raise ValueError("Unknown country while trying to add rdf triplets: {}".format(iso3_code))
        return result








