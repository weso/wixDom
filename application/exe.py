__author__ = 'guillermo'

from wi.domain.model.observation.observation import create_observation
from wi.domain.model.observation.year import Year
from wi.domain.model.data_set import create_data_set

obs = create_observation(label='Observation of Spain')
print obs
comp = obs.add_computation("raw")
year1 = Year(2001)
obs.ref_year = year1.value
print obs

data_set = create_data_set(title='Dataset Title')
print data_set