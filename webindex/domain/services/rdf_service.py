from namespaces_handler import *
from rdflib.namespace import RDF, RDFS
from rdflib import Literal

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
        indicators_added_dict = {}
        self._add_country_triples(observation, graph, countries_added_dict)
        self._add_indicator_triples(observation, graph, indicators_added_dict)
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

    def _add_indicator_triples(self, observation, graph, indicators_dict):
        if observation['indicator'] in indicators_dict:
            return
        indicators_dict[observation['indicator']] = True
        indicator_dict = self._find_indicator_dict(observation['indicator'])
        indicator_term = base_ind.term(observation['indicator'])
        graph.add(indicator_term, RDF.type, cex.term("Indicator"))
        graph.add(indicator_term, RDFS.label, Literal(indicator_dict['name'], lang='en'))
        graph.add(indicator_term, RDFS.comment, Literal(indicator_dict['description'], lang='en'))
        graph.add(indicator_term, lb.term('indicatorType'), cex.term(indicator_dict['type'])) # Check this.
                                                                                              # Is it lb for sure?
        # graph.add((base_ind.term(ind.id), lb.term("measurement"),
        #            Literal(ind.measurement_unit.name)))
        # graph.add((base_ind.term(ind.id), lb.term("last_update"),
        #            Literal(self.time.strftime("%Y-%m-%d"), datatype=XSD.date)))
        # graph.add((base_ind.term(ind.id), lb.term("starred"),
        #            Literal(ind.starred, datatype=XSD.Boolean)))
        # graph.add((base_ind.term(ind.id), lb.term("topic"),
        #            base_topic.term(ind.topic_id)))
        return graph

    def _find_country_dict(self, iso3_code):
        result = self._area_repository.find_countries_by_code_or_income(iso3_code)['data']
        if result is None:
            raise ValueError("Unknown country while trying to add rdf triplets: {}".format(iso3_code))
        return result

    def _find_indicator_dict(self, indicator_code):
        result = self._indicator_repository.find_indicators_by_code(indicator_code)
        if not result['success'] or result['data'] is None:
            raise ValueError("Unknown indicator while trying to add rdf triplets: {}".format(indicator_code))
        return result['data']








