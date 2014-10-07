__author__ = 'guillermo'

from webindex.domain.model.entity import Entity
from webindex.domain.model.events import DomainEvent, publish
import uuid
from .computation import Computation
from utility.mutators import mutate, when
from ...exceptions import DiscardedEntityError
from abc import ABCMeta


# =======================================================================================
# Observation aggregate root entity
# =======================================================================================
class Observation(Entity):
    """ Observation aggregate root entity
    """

    class Created(Entity.Created):
        pass

    class Discarded(Entity.Discarded):
        pass

    class ComputationAdded(DomainEvent):
        pass

    class ReferencedArea(DomainEvent):
        pass

    class ReferencedIndicator(DomainEvent):
        pass

    def __init__(self, event):
        super(Observation, self).__init__(event.originator_id, event.originator_version)
        self._computation = None
        self._issued = event.issued
        self._publisher = event.publisher
        self._type = event.obs_type
        self._label = event.label
        self._status = event.status
        self._ref_indicator_id = None
        self._ref_area_id = None
        self._value = event.value
        self._ref_year = None

    def __repr__(self):
        return "{d}Observation(id={id!r}," \
               "computation={computation!r}, issued={issued!r}, " \
               "publisher={publisher!r}, type={obs_type!r}, label={label!r}, " \
               "status={status!r}, " \
               "ref_indicator={ref_indicator!r}, value={value!r}, " \
               "ref_area={ref_area!r}, ref_year={ref_year!r}) ". \
            format(d="*Discarded* " if self.discarded else "", id=self._id,
                   computation=self._computation if self.computation else
                   "no computation added yet",
                   issued=self._issued, publisher=self._publisher,
                   obs_type=self._type, label=self._label,
                   status=self._status, ref_indicator=self._ref_indicator_id,
                   value=self._value, ref_area=self._ref_area_id,
                   ref_year=self._ref_year)

    # =======================================================================================
    # Properties
    # =======================================================================================
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
        return self._ref_area_id

    @property
    def ref_indicator(self):
        self._check_not_discarded()
        return self._ref_indicator_id

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
        self._ref_year = value
        self.increment_version()

    # =======================================================================================
    # Commands
    # =======================================================================================
    def discard(self):
        """Discard this observation.

        After a call to this method, the observation can no longer be used.
        """
        self._check_not_discarded()
        event = Observation.Discarded(originator_id=self.id,
                                      originator_version=self.version)

        self._apply(event)
        publish(event)

    @staticmethod
    def validate_computation_type(_type):
        if _type not in ["raw", "normalized", "ranked", "scored", "grouped"]:
            raise ValueError("There is no {} computation type".format(_type))
        return _type

    def add_computation(self, _type=None, reason=None, _slice=None,
                        dimension=None, mean=None, std_deviation=None, value_max=None,
                        value_min=None, component=None, data_set=None,
                        filter_dimension=None, filter_value=None):

        self._check_not_discarded()
        event = Observation.ComputationAdded(
            originator_id=self.id, originator_version=self.version,
            computation_id=uuid.uuid4().hex[:24], computation_version=0,
            type=self.validate_computation_type(_type), reason=reason, slice=_slice,
            dimension=dimension, mean=mean, std_deviation=std_deviation,
            value_max=value_max, value_min=value_min, component=component,
            data_set=data_set, filter_dimension=filter_dimension,
            filter_value=filter_value)

        self._apply(event)
        publish(event)
        return self.computation

    def reference_indicator(self, indicator):
        """Reference an indicator from this observation.

        Args:
            indicator: The Indicator to be referenced from this observation.

        Raises:
            DiscardedEntityError: If this observation or the indicator has been discarded.
            """
        self._check_not_discarded()

        if indicator.discarded:
            raise DiscardedEntityError("Cannot reference {!r}".format(indicator))

        event = Observation.ReferencedIndicator(originator_id=self.id,
                                                originator_version=self.version,
                                                indicator_id=indicator.id)
        self._apply(event)
        publish(event)

    def reference_area(self, area):
        """Reference an area from this observation.

        Args:
            area: The area (Region or Country) to be referenced from this observation.

        Raises:
            DiscardedEntityError: If this observation or the area has been discarded.
            """

        self._check_not_discarded()
        if area.discarded:
            raise DiscardedEntityError("Cannot reference {!r}".format(area))

        event = Observation.ReferencedArea(originator_id=self.id,
                                           originator_version=self.version,
                                           area_id=area.id)
        self._apply(event)
        publish(event)

    def _apply(self, event):
        mutate(self, event)


# =======================================================================================
# Observation aggregate root factory
# =======================================================================================
def create_observation(issued=None, publisher=None, data_set=None, obs_type=None,
                       label=None, status=None, ref_indicator=None, value=None,
                       ref_area=None, ref_year=None):
    obs_id = uuid.uuid4().hex[:24]
    event = Observation.Created(originator_id=obs_id, originator_version=0, issued=issued,
                                publisher=publisher, data_set=data_set, obs_type=obs_type,
                                label=label, status=status, ref_indicator=ref_indicator,
                                value=value, ref_area=ref_area, ref_year=ref_year)
    obs = when(event)
    publish(event)
    return obs


# =======================================================================================
# Mutators
# =======================================================================================
@when.register(Observation.Created)
def _(event):
    """Create a new aggregate root"""
    obs = Observation(event)
    obs.increment_version()
    return obs


@when.register(Observation.Discarded)
def _(event, obs):
    obs.validate_event_originator(event)
    obs._discarded = True
    obs.increment_version()
    return obs


@when.register(Observation.ComputationAdded)
def _(event, obs):
    obs.validate_event_originator(event)
    computation = Computation(event, obs)
    obs._computation = computation
    obs.increment_version()
    return obs


@when.register(Observation.ReferencedIndicator)
def _(event, obs):
    obs.validate_event_originator(event)
    obs._ref_indicator_id = event.indicator_id
    obs.increment_version()
    return obs


@when.register(Observation.ReferencedArea)
def _(event, obs):
    obs.validate_event_originator(event)
    obs._ref_area_id = event.area_id
    obs.increment_version()
    return obs


# =======================================================================================
# Observations Repository
# =======================================================================================
class Repository(object):
    """Abstract implementation of generic queries for managing observations."""
    __metaclass__ = ABCMeta

    def find_observations(self, indicator_code=None, area_code=None, year=None):
        pass

    def get_indicators_by_code(self, code):
        pass

    def get_countries_by_code_name_or_income(self, code):
        pass

    def get_years(self, year):
        pass

    def observation_uri(self, observation):
        pass

    def set_observation_country_and_indicator_name(self, observation):
        pass

    def insert_observation(self, observation, area_iso3_code=None, indicator_code=None, year_literal=None):
        """
        The info related to area, indicator and year could be provided using the observation
        object internal fields or, in some context, directly using the parameters
        area_iso3_code, indicator_code and year literal. Each implementation will choose
        :param observation: observation object of the model
        :param area_iso3_code:  iso3_code of a country
        :param indicator_code: code of an indicator (not id)
        :param year_literal: inst/string year, not an object year of the model
        :return:
        """
        pass