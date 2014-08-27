__author__ = 'guillermo'

from wi.domain.model.observation.observation import create_observation
from wi.domain.model.observation.year import Year
from wi.domain.model.data_set import create_data_set
from wi.domain.model.slice import create_slice

obs1 = create_observation(label='Observation of Spain')
obs2 = create_observation(label='Observation of UK')
print obs1

comp = obs1.add_computation("raw")
year1 = Year(2001)
obs1.ref_year = year1.value
print obs1

slice1 = create_slice(_type='Slice1')
slice2 = create_slice(_type='Slice2')

slice1.add_observation(obs1)
slice2.add_observation(obs2)

slice1_observations = slice1.observation_ids()
slice2_observations = slice2.observation_ids()

print "Observations in slice {} ->".format(slice1.type), \
    [obs for obs in slice1_observations]
print "Observations in slice {} ->".format(slice2.type), \
    [obs for obs in slice2_observations]

data_set = create_data_set(title='My DataSet')
print data_set
data_set.add_slice(slice1)
data_set_slices = data_set.slice_ids()
print "Slices in dataset {} ->".format(data_set.title), [slc for slc in data_set_slices]