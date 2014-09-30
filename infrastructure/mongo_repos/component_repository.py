__author__ = 'Dani'

from webindex.domain.model.component import Repository
from config import port, db_name, host
from .mongo_connection import connect_to_db
from utils import normalize_group_name


class ComponentRepository(Repository):
    """Concrete mongodb repository for Component.
    """

    def __init__(self, url_root):
        self._db = connect_to_db(host=host, port=port, db_name=db_name)
        self._url_root = url_root

    def insert_component(self, component, subindex_name=None, index_name=None):
        component_dict = {}
        component_dict['_id'] = component.id
        component_dict['index'] = normalize_group_name(index_name)
        component_dict['subindex'] = normalize_group_name(subindex_name)
        component_dict['component'] = normalize_group_name(component.label)
        component_dict['indicator'] = None
        component_dict['name'] = component.label
        component_dict['description'] = None
        component_dict['_type'] = component.type
        component_dict['parent'] = normalize_group_name(subindex_name)

        self._db['indicators'].insert(component_dict)  # This is OK. it will be stored in "indicators"
