__author__ = 'guillermo'

from webindex.domain.model.observation.observation import create_observation
from infrastructure.mongo_repos.mongo_connection import MongoConnection
from infrastructure.mongo_repos.config import host, port, db_name
from bson.objectid import ObjectId


def connect_to_db():
    con = MongoConnection(host, port, db_name)
    db = con.db
    return db


def main():
    db = connect_to_db()
    for x in xrange(1000):
        obs = create_observation(issued='date', ref_indicator='ind01',
                                 ref_area='Spain' + str(x),
                                 ref_year=2001, data_set="DataSet01",
                                 label='Observation of Spain', publisher="WebFoundation",
                                 obs_type="Observation", status='Some Status', value=12.1)

        #comp = obs.add_new_computation("My computation", "raw")

        obs.__dict__['_id'] = ObjectId(oid=str(obs.id))

        observations = db['observations']

        observations.insert(obs.__dict__)

if __name__ == '__main__':
    print main()