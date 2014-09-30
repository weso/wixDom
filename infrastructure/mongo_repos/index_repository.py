__author__ = 'Dani'

from webindex.domain.model.index import Repository
from config import port, db_name, host
from .mongo_connection import connect_to_db
from utils import normalize_group_name


class IndexRepository(Repository):
    """Concrete mongodb repository for Component.
    """

    def __init__(self, url_root):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)
        self._url_root = url_root

    def insert_index(self, index):
        index_dict = {}
        index_dict['_id'] = index.id
        index_dict["index"] = normalize_group_name(index.label)
        index_dict['subindex'] = None
        index_dict['component'] = None
        index_dict['indicator'] = None
        index_dict['name'] = index.label
        index_dict['description'] = None
        index_dict['type'] = index.type
        index_dict['parent'] = None

        self._db['indicators'].insert(index_dict)
