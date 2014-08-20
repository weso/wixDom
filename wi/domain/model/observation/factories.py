__author__ = 'guillermo'

from .observation_root import Observation, when
import uuid
from wi.domain.model.events import publish
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
    obs = when(event)
    publish(event)
    return obs