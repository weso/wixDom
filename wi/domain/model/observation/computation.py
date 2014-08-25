__author__ = 'guillermo'
from wi.domain.model.entity import Entity


class Computation(Entity):
    """ Computation entity """

    def __init__(self, event, observation):
        super(Computation, self).__init__(event.computation_id, event.computation_version)
        self._observation = observation
        self._name = event.name

        # Raw
        self._type = event.type

        # Ranked
        self._reason = event.reason
        self._slice = event.slice
        self._dimension = event.dimension

        # Normalized
        self._mean = event.mean
        self._std_deviation = event.std_deviation

        # Scored
        self._range_max = 100  # todo check literal value
        self._range_min = 0  # todo check literal value
        self._value_max = event.value_max
        self._value_min = event.value_min

        # Grouped in clusters, sub-indexes and indexes
        self._component = event.component
        self._data_set = event.data_set
        self._filter_dimension = event.filter_dimension
        self._filter_value = event.filter_value

    # TODO Add try except to raise a ValueError on type
    def __repr__(self):
        rep = ""
        if self._type == 'raw':
            rep = "{d}Raw-Computation(id={id!r}, observation_id={c._observation.id}, " \
                  "name={c._name}, type={type})".\
                format(d="Discarded" if self.discarded else "", id=self._id, c=self,
                       type=self._type)
        elif self._type == 'ranked':
            rep = "{d}Ranked-Computation(id={id!r}, observation_id={c._observation.id}," \
                  " name={c._name}, type={type}, reason={rea}, " \
                  "slice={slc}, dimension={dim})".\
                format(d="Discarded" if self.discarded else "", id=self.id, c=self,
                       type=self._type, rea=self._reason, slc=self._slice,
                       dim=self._dimension)
        elif self._type == 'normalized':
            rep = "{d}Normalized-Computation(id={id!r}, " \
                  "observation_id={c._observation.id}, type={type}, mean={mean}, " \
                  "slice={slc}, std_deviation={std})".\
                format(d="Discarded" if self.discarded else "", id=self.id, c=self,
                       type=self._type, mean=self._mean, slc=self._slice,
                       std=self._std_deviation)
        elif self._type == 'scored':
            rep = "{d}Scored-Computation(id={id!r}, observation_id={c._observation.id}," \
                  " name={c._name}, type={type}, range_max={r_max}, " \
                  "range_min={r_min}, value_max={v_max}, value_min={v_min}, " \
                  "slice={slc})".\
                format(d="Discarded" if self.discarded else "", id=self.id, c=self,
                       type=self._type, r_max=self._range_max, r_min=self._range_min,
                       v_max=self._value_max, v_min=self._value_min, slc=self._slice)
        elif self._type == 'grouped':
            rep = "{d}Grouped-Computation(id={id!r}, " \
                  "observation_id={c._observation.id}, name={c._name}, type={type}, " \
                  "component={comp}, data_set={dst}, dimension={dim}, " \
                  "filter_dimension={f_dim}, filter_value={f_val})".\
                format(d="Discarded" if self.discarded else "", id=self.id, c=self,
                       type=self._type, comp=self._component, dst=self._data_set,
                       dim=self._dimension, f_dim=self._filter_dimension,
                       f_val=self._filter_value)
        return rep

# =======================================================================================
# Properties
# =======================================================================================
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's name cannot be empty")
        self._name = value
        self.increment_version()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's type cannot be empty")
        self._type = value
        self.increment_version()

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's reason cannot be empty")
        self._reason = value
        self.increment_version()

    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's dimension cannot be empty")
        self._dimension = value
        self.increment_version()

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's mean cannot be empty")
        self._mean = value
        self.increment_version()

    @property
    def std_deviation(self):
        return self._std_deviation

    @std_deviation.setter
    def std_deviation(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's standard deviation cannot be empty")
        self._std_deviation = value
        self.increment_version()

    @property
    def value_max(self):
        return self._value_max

    @value_max.setter
    def value_max(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's max value cannot be empty")
        self._value_max = value
        self.increment_version()

    @property
    def value_min(self):
        return self._reason

    @value_min.setter
    def value_min(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's min value cannot be empty")
        self._value_min = value
        self.increment_version()

    @property
    def filter_dimension(self):
        return self._filter_dimension

    @filter_dimension.setter
    def filter_dimension(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's filter dimension cannot be empty")
        self._filter_dimension = value
        self.increment_version()

    @property
    def filter_value(self):
        return self._filter_dimension

    @filter_value.setter
    def filter_value(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Computation's filter value cannot be empty")
        self._filter_value = value
        self.increment_version()








