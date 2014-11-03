from pyld import jsonld
import json
import requests

observations_context = {
    "scored": {"@id": "http://purl.org/weso/ontology/computex#RankingScore", "@type": "@id"},
    "indicator:": {"@id": "http://purl.org/weso/ontology/computex#Indicator", "@type": "@id"},
    "area_name:": {"@id": "http://schema.org/Country", "@type": "@id"},
    "ranked:": {"@id": "http://purl.org/weso/ontology/computex#Ranked", "@type": "@id"},
    "normalized": {"@id": "http://purl.org/weso/ontology/computex#Normalized", "@type": "@id"},
    "continent": {"@id": "http://schema.org/Continent", "@type": "@id"}}


r = requests.get('http://intertip.webfoundation.org/api/observations')
obs = r.json()


def get_observations():
    for ob in obs['data']:
        yield ob


def annotate_observations():
    for o in get_observations():
        o['@id'] = o.pop('uri')
        o['http://purl.org/weso/ontology/computex#Indicator'] = o.pop('indicator')
        o['http://purl.org/weso/ontology/computex#Ranked'] = o.pop('ranked')
        o['http://purl.org/weso/ontology/computex#Normalized'] = o.pop('normalized')
        o['http://schema.org/Continent'] = o.pop('continent')
        o['http://schema.org/Country'] = o.pop('area_name')
        yield o


def compact_json():
    with open('compacted_json.json', mode='w') as compacted:
        json.dump(jsonld.compact(obs, observations_context), compacted)
        for doc in annotate_observations():
            json.dump(doc, compacted, indent=2)
            print doc


if __name__ == '__main__':
    annotate_observations()
    compact_json()