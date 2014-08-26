__author__ = 'guillermo'

from wi.domain.model.entity import Entity
import uuid
from .events import DomainEvent, publish
from utility.mutators import when, mutate
from ..exceptions import ConstraintError


class Slice(Entity):
    """ Slice aggregate root entity"""
    class Created(Entity.Created):
        pass

    class Discarded(Entity.Discarded):
        pass

    def __init__(self, event):
        super(Slice, self).__init__(event.originator_id, event.originator_version)
        self._type = event.type
        self._year = event.year
        self._indicator = None

