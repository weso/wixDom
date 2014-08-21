__author__ = 'guillermo'

from wi.domain.model.observation.factories import create_observation
from infrastructure.mongo_repos.mongo_connection import MongoConnection
from config import *
from bson.objectid import ObjectId


def connect_to_db():
    con = MongoConnection(host, port, db_name)
    db = con.db
    return db


def main():
    db = connect_to_db()
    for x in xrange(10000):
        obs = create_observation(issued='date', ref_indicator='ind01',
                             ref_area='Spain' + str(x),
                             ref_year=2001, data_set="DataSet01", computation='090',
                             label='Observation of Spain', publisher="WebFoundation",
                             obs_type="Observation", status='Some Status', value=12.1)

        obs.__dict__['_id'] = ObjectId(oid=str(obs.id))

        observations = db['observations']

        observations.insert(obs.__dict__)


if __name__ == '__main__':
    print main()