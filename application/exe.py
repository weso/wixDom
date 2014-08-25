__author__ = 'guillermo'

from wi.domain.model.observation.observation import create_observation

obs = create_observation(label='Observation of Spain')
print obs
comp = obs.add_new_computation("Some computation", "grouped")
print obs.computation
