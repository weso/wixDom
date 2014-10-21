__author__ = 'Dani'

from config import port, db_name, host
from .mongo_connection import connect_to_db


class RankingRepository(object):
    """
    It does not have inheritance relationships.
    It does not represent an entity, but an abstract group of data handy only for visualizations.
    """


    def __init__(self, url_root):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)
        self._url_root = url_root

