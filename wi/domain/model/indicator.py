__author__ = 'guillermo'


from wi.domain.model.entity import Entity
from abc import ABCMeta, abstractmethod
import uuid
from singledispatch import singledispatch
from wi.domain.model.events import DomainEvent
from wi.domain.model.events import publish

# =======================================================================================
# Indicator aggregate root entity
#


class Indicator(Entity):
    """ Indicator aggregate root entity
    """
    class Created(Entity.Created):
        pass

    class Discarded(Entity.Discarded):
        pass

    def __init__(self, event):
        super(Indicator, self).__init__(event.originator_id, event.originator_version)
        self._country_coverage = event.country_coverage
        self._provider_link = event.provider_link
        self._republish = event.republish
        self._component = event.component
        self._high_low = event.high_low
        self._ind_type = event.ind_type
        self._label = event.label
        self._comment = event.comment
        self._notation = event.notation
        self._interval_starts = event.interval_starts
        self._interval_ends = event.interval_ends

    def __repr__(self):
        return "{d}Indicator(id={id!r}," \
               "country_coverage={country_coverage!r}, provider_link={provider_link!r}," \
               "republish={republish!r}, component={component!r}, " \
               "high_low={high_low!r}, ind_type={ind_type!r}, label={label!r}, " \
               "comment={comment!r}, notation={notation!r}" \
               "interval_starts={interval_starts!r}, interval_ends={interval_ends!r}, ".\
               format(d="*Discarded* " if self._discarded else "", id=self._id,
                      country_coverage=self._country_coverage,
                      provider_link=self._provider_link, republish=self._republish,
                      component=self._component, high_low=self._high_low,
                      ind_type=self._ind_type, label=self._label, comment=self._comment,
                      notation=self._notation, interval_starts=self._interval_starts,
                      interval_ends=self._interval_ends)

# =======================================================================================
# Accessors
#

    @property
    def country_coverage(self):
        self._check_not_discarded()
        return self._country_coverage

    @country_coverage.setter
    def country_coverage(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's country coverage cannot be empty")
        self._country_coverage = value
        self.increment_version()

    @property
    def provider_link(self):
        self._check_not_discarded()
        return self._provider_link

    @provider_link.setter
    def provider_link(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's provider_link cannot be empty")
        self._provider_link = value
        self.increment_version()

    @property
    def republish(self):
        self._check_not_discarded()
        return self._republish

    @republish.setter
    def republish(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's republish cannot be empty")
        self._republish = value
        self.increment_version()

    @property
    def component(self):
        self._check_not_discarded()
        return self._component

    @component.setter
    def component(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's component cannot be empty")
        self._component = value
        self.increment_version()

    @property
    def high_low(self):
        self._check_not_discarded()
        return self._high_low

    @high_low.setter
    def high_low(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's high_low cannot be empty")
        self._high_low = value
        self.increment_version()

    @property
    def ind_type(self):
        self._check_not_discarded()
        return self._ind_type

    @ind_type.setter
    def ind_type(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's ind_type cannot be empty")
        self._ind_type = value
        self.increment_version()

    @property
    def label(self):
        self._check_not_discarded()
        return self._label

    @label.setter
    def label(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's label cannot be empty")
        self._label = value
        self.increment_version()

    @property
    def comment(self):
        self._check_not_discarded()
        return self._comment

    @comment.setter
    def comment(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's comment cannot be empty")
        self._comment = value
        self.increment_version()

    @property
    def notation(self):
        self._check_not_discarded()
        return self._notation

    @notation.setter
    def notation(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's notation cannot be empty")
        self._notation = value
        self.increment_version()

    @property
    def interval_starts(self):
        self._check_not_discarded()
        return self._interval_starts

    @interval_starts.setter
    def interval_starts(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's interval_starts cannot be empty")
        self._interval_starts = value
        self.increment_version()

    @property
    def interval_ends(self):
        self._check_not_discarded()
        return self._interval_ends

    @interval_ends.setter
    def interval_ends(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Indicator's interval_ends cannot be empty")
        self._interval_ends = value
        self.increment_version()