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
        years_added = {}
        self._add_country_triples(observation, graph, countries_added_dict)
        self._add_indicator_triples(observation, graph, indicators_added_dict)
        self._add_year_triples(observation, graph, years_added)
        self._add_observation_triples(observation, graph)


    def _add_year_triples(self, observation, graph, years_added_dict):
        if observation['year'] in years_added_dict:
            return  # It means that the triplets of this year had already been added

        years_added_dict[observation['year']] = True  # It means we are adding this year triplets
                                                    # The next attempt over this year will return
                                                    # without computing anything
        year_term = example.term(observation['year'])

        graph.add(year_term,
                  RDF.type,
                  example.term("year"))
        graph.add(year_term,
                  RDFS.label,
                  Literal("Year" + observation['year'], lang="en"))
        graph.add(year_term,
                  example.term("value"),
                  Literal(int(observation['year']), datatype=XSD.integer))


    def _add_observation_triples(self, observation, graph):
        #### Initializing observation term
        observation_term = country_term = example.term(self._build_observation_id(observation))

        #### Adding Literal and type triples
        graph.add(observation_term,
                  RDF.type,
                  example.term("Observation"))

        graph.add(observation_term,
                  RDFS.label,
                  Literal(self._build_observation_label(observation), lang="en"))

        graph.add(observation_term,
                  example.term("uri_api"),
                  Literal(observation['uri']))

        graph.add(observation_term,
                  cex.term("Raw"),
                  Literal(observation['value'], datatype=XSD.double))

        if observation['normalized'] is not None:
            graph.add(observation_term,
                      cex.term("Normalized"),
                      Literal(observation['normalized'], datatype=XSD.double))

        if observation['scored'] is not None:
            graph.add(observation_term,
                      cex.term("RankingScore"),
                      Literal(observation['scored'], datatype=XSD.double))

        if observation['ranked'] is not None:
            graph.add(observation_term,
                      cex.term("Ranked"),
                      Literal(observation['ranked'], datatype=XSD.integer))

        #### Linking observation with other subjects

            graph.add(observation_term,
                      example.term("ref-indicator"),
                      example.term(observation['indicator']))

            graph.add(observation_term,
                      example.term("ref-year"),
                      example.term(observation['year']))

            graph.add(observation_term,
                      example.term("ref-area"),
                      example.term(observation_term['area']))


    @staticmethod
    def _build_observation_id(observation_dict):
        return "OBS_{}_{}_{}".format(observation_dict["indicator"],
                                     observation_dict["area"],
                                     observation_dict["year"])

    @staticmethod
    def _build_observation_label(observation_dict):
        return "Observation for {} over the indicator {} during {}".format(observation_dict["area"],
                                                                           observation_dict['indicator',
                                                                           observation_dict['year']])



    def _add_country_triples(self, observation, graph, countries_added_dict):
        if observation['area'] in countries_added_dict:
            return  # It means that the triplets of this country had already been added

        countries_added_dict[observation['area']] = True  # It means we are adding this country triplets
                                                    # The next attempt over this country will return
                                                    # without computing anything
        #### Looking for country and continent information
        country_dict = self._find_country_dict(observation['area'])
        continent_dict = self._find_country_dict(observation['continent'])

        #### Initializing subjects to be used
        country_term = example.term(observation['area'])
        continent_term = example.term(observation['continent'])
        income_term = example.term(continent_dict['income'])

        #### Adding continent triples
        graph.add(continent_term,
                  RDF.type,
                  cex.term("Area"))
        graph.add(continent_term,
                  RDFS.label,
                  Literal(None, lang="en"))

        #### Adding income triples
        graph.add(income_term,
                  RDF.type,
                  example.term("income"))

        graph.add(income_term,
                  RDFS.label,
                  Literal(self._get_income_label(continent_dict['income']), lang="en"))
        #TODO: This is some kind of official code, probably we can put aun URI/URL here
        #TODO: to reference the source and complete the information

        #### Adding country triples
        graph.add(country_term,
                  RDF.type,
                  cex.term("Area"))

        graph.add(country_term,
                  RDFS.label,
                  Literal(country_dict['name'], lang="en"))

        graph.add(country_term,
                  example.term("iso2"),
                  Literal(country_dict['iso2']))

        graph.add(country_term,
                  example.term("iso3"),
                  Literal(country_dict['iso3']))

        graph.add(country_term,
                  example.term("iso_num"),
                  Literal(country_dict['iso_num']))

        graph.add(country_term,
                  example.term("is_part_of"),
                  continent_term)

        graph.add(country_term,
                  example.term("short_name"),
                  Literal(country_dict['short_name'], lang='en'))

        graph.add(country_term,
                  example.term("income_level"),
                  income_term)


    def _get_income_label(self, income_code):
        #### The income information is not stored is not supposed to be
        #### stored in the database... so we need to do this dirty shortcut
        if income_code == "LIC":
            return "Low income"
        elif income_code == "NOC":
            return "High income: nonOECD"
        elif income_code == "UMC":
            return "Upper middle income"
        elif income_code == "UMC":
            return "Upper middle income"
        elif income_code == "OEC":
            return "High income: OECD"
        elif income_code == "LMC":
            return "Lower middle income"
        elif income_code == "INX":
            return "Not classified"
        else:
            raise ValueError("Unknown income code while generating triples: {}".format(income_code))

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
        result = self._area_repository.find_countries_by_code_or_income(iso3_code)
        if not result['success']  or result['data'] is None:
            raise ValueError("Unknown country while trying to add rdf triples: {}".format(iso3_code))
        return result['data']

    def _find_indicator_dict(self, indicator_code):
        result = self._indicator_repository.find_indicators_by_code(indicator_code)
        if not result['success'] or result['data'] is None:
            raise ValueError("Unknown indicator while trying to add rdf triples: {}".format(indicator_code))
        return result['data']








