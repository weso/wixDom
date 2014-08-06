__author__ = 'guillermo'

from wi.domain.model.entity import Entity
from abc import ABCMeta, abstractmethod
import uuid
from singledispatch import singledispatch
from wi.domain.model.events import DomainEvent
from wi.domain.model.events import publish

# =======================================================================================
# Observation aggregate root entity
#


class Observation(Entity):
    """ Observation aggregate root entity
    """
    class Created(Entity.Created):
        pass

    class Discarded(Entity.Discarded):
        pass

    def __init__(self, event):
        super(Observation, self).__init__(event.originator_id, event.originator_version)
        self._computation = event.computation
        self._issued = event.issued
        self._publisher = event.publisher
        self._data_set = event.data_set
        self._type = event.obs_type
        self._label = event.label
        self._status = event.status
        self._ref_indicator = event.ref_indicator
        self._value = event.value
        self._ref_area = event.ref_area
        self._ref_year = event.ref_year

    def __repr__(self):
        return "{d}Observation(id={id!r}," \
               "computation={computation!r}, issued={issued!r}, " \
               "publisher={publisher!r}, data_set={data_set!r}, " \
               "type={obs_type!r}, label={label!r}, status={status!r}, " \
               "ref_indicator={ref_indicator!r}, value={value!r}" \
               "ref_area={ref_area!r}, ref_year={ref_year!r}, ".\
               format(d="*Discarded* " if self._discarded else "", id=self._id,
                      computation=self._computation, issued=self._issued,
                      publisher=self._publisher, data_set=self._data_set,
                      obs_type=self._type, label=self._label, status=self._status,
                      ref_indicator=self._ref_indicator, value=self._value,
                      ref_area=self._ref_area, ref_year=self._ref_year)

# =======================================================================================
# Accessors
#

    @property
    def computation(self):
        self._check_not_discarded()
        return self._computation

    @computation.setter
    def computation(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's computation cannot be empty")
        self._computation = value
        self.increment_version()

    @property
    def issued(self):
        self._check_not_discarded()
        return self._issued

    @issued.setter
    def issued(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's issue date cannot be empty")
        self._issued = value
        self.increment_version()

    @property
    def publisher(self):
        self._check_not_discarded()
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's publisher cannot be empty")
        self._issued = value
        self.increment_version()

    @property
    def data_set(self):
        self._check_not_discarded()
        return self._data_set

    @data_set.setter
    def data_set(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's data_set cannot be empty")
        self._data_set = value
        self.increment_version()

    @property
    def obs_type(self):
        self._check_not_discarded()
        return self._type

    @obs_type.setter
    def obs_type(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's type cannot be empty")
        self._type = value
        self.increment_version()

    @property
    def label(self):
        self._check_not_discarded()
        return self._label

    @label.setter
    def label(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's label cannot be empty")
        self._label = value
        self.increment_version()

    @property
    def status(self):
        self._check_not_discarded()
        return self._status

    @status.setter
    def status(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's status cannot be empty")
        self._status = value
        self.increment_version()

    @property
    def ref_indicator(self):
        self._check_not_discarded()
        return self._ref_indicator

    @ref_indicator.setter
    def ref_indicator(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's ref_indicator cannot be empty")
        self._ref_indicator = value
        self.increment_version()

    @property
    def value(self):
        self._check_not_discarded()
        return self._value

    @value.setter
    def value(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's value cannot be empty")
        self._value = value
        self.increment_version()

    @property
    def ref_area(self):
        self._check_not_discarded()
        return self._ref_area

    @ref_area.setter
    def ref_area(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's area cannot be empty")
        self._ref_area = value
        self.increment_version()

    @property
    def ref_year(self):
        """
        Checks for object's properties
        """
        self._check_not_discarded()
        return self._ref_year

    @ref_year.setter
    def ref_year(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Observation's year cannot be empty")
        self._ref_year = value
        self.increment_version()

# =======================================================================================
# Related Entities and value objects


# =======================================================================================
# Factories - Aggregate root factory

def create_observation(issued, publisher, data_set, obs_type, label, status,
                       ref_indicator, computation, value, ref_area, ref_year):
    obs_id = uuid.uuid4().hex
    event = Observation.Created(originator_id=obs_id, originator_version=0, issued=issued,
                                publisher=publisher, data_set=data_set, obs_type=obs_type,
                                label=label, status=status, ref_indicator=ref_indicator,
                                computation=computation, value=value, ref_area=ref_area,
                                ref_year=ref_year)
    obs = _when(event)
    publish(event)
    return obs

# =======================================================================================
# Mutators - all aggregate creation and mutation is performed by the generic _when()
# function.
#


def mutate(obj, event):
    return _when(event, obj)


# These dispatch on the type of the first arg, hence (event, self)


@singledispatch
def _when(event, entity):
    """Modify an entity (usually an aggregate root) by replaying an event."""
    raise NotImplementedError("No _when() implementation for {!r}".format(event))


@_when.register(Observation.Created)
def _(event, obj=None):
    """Create a new aggregate root"""
    obs = Observation(event)
    obs.increment_version()
    return obs


@_when.register(Observation.Discarded)
def _(event, obs):
    obs.validate_event_originator(event)

    for column in obs._columns:
        column._discarded = True
    obs._columns.clear()

    obs._discarded = True
    obs.increment_version()
    return obs

# =======================================================================================
# Repository


class ObservationRepository(object):
    """
    Abstract implementation of generic queries for managing observations.
    This will be sub-classed with an infrastructure specific implementation
    which will customize all the queries
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ObservationRepository, self).__init__(**kwargs)

    def all_observations(self, obs_ids=None):
        return self.observations_where(lambda obs: True, obs_ids)

    def observation_from_area(self, ref_area, obs_ids=None):
        return self.observations_where(lambda obs: obs.ref_area == ref_area, obs_ids)

    def observation_with_id(self, obs_id):
        try:
            return self.all_observations(obs_id)
        except ValueError:
            print "No Observation with id {}".format(obs_id)
            raise

    @abstractmethod
    def observations_where(self, predicate, obs_ids=None):
        """
        Subclass implementations must override at least this method
        """
        raise NotImplementedError

# =======================================================================================
# Exceptions