__author__ = 'guillermo'

from webindex.domain.model.observation.observation import create_observation
from webindex.domain.model.observation.year import Year
from webindex.domain.model.data_set import create_data_set
from webindex.domain.model.slice import create_slice
from webindex.domain.model.indicator import create_indicator
from webindex.domain.model.component import create_component
from webindex.domain.model.subindex import create_sub_index
from webindex.domain.model.index import create_index
from webindex.domain.model.area.region import create_region
from pprint import pprint as pp


#Observations
obs1 = create_observation(label='Observation of Spain')
obs2 = create_observation(label='Observation of UK')
print obs1

compu = obs1.add_computation("raw")
obs1.ref_year = Year(2001)
print obs1

print "****************************************************************************"
#Slices
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
print "****************************************************************************"

#DataSets
data_set = create_data_set(title='My DataSet')
print data_set
data_set.add_slice(slice1)
data_set_slices = data_set.slice_ids()
print "Slices in dataset {} ->".format(data_set.title), [sb for sb in data_set_slices]
print "****************************************************************************"

# Indicators
ind1 = create_indicator(_type='secondary')
ind2 = create_indicator(_type='primary')
indicators = [ind1, ind2]
pp(indicators)

#Components
comp1 = create_component()
comp2 = create_component()

for i in indicators:
    comp1.add_indicator(i)

component_grouped_indicators = comp1.indicator_ids()

print "Indicators in component {} ->".format(comp1.type), [ind for ind in
                                                           component_grouped_indicators]
print comp1.__contains__(ind2)
print "****************************************************************************"

#SubIndexes
sub_index1 = create_sub_index()
sub_index2 = create_sub_index()
print sub_index1
components = [comp1, comp2]
for sb in components:
    sub_index1.add_component(sb)
print "Components in subindex {} ->".format(sub_index1.type), [sb for sb in
                                                               sub_index1.component_ids()]
print sub_index1
print "****************************************************************************"

#Index
index = create_index()
print index
sub_indexes = [sub_index1, sub_index2]
for s in sub_indexes:
    index.add_sub_index(s)
print "SubIndexes in index {} ->".format(index.type), [sb for sb in
                                                       index.sub_index_ids()]
print "****************************************************************************"

#Area
region = create_region("Europe")
country = region.relate_country(iso2_code="SP", label="Spain")
print region
print country


# References by ID
obs1.reference_indicator(index)
obs1.reference_area(country)
print obs1.ref_area, obs1.ref_indicator