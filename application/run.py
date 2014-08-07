__author__ = 'guillermo'

from wi.domain.model.observation import create_observation


def main():
    obs = create_observation(issued='date', ref_indicator='ind01',
                             ref_area='Spain',
                             ref_year=2001, data_set="DataSet01", computation='090',
                             label='Observation of Spain', publisher="WebFoundation",
                             obs_type="Observation", status='Some Status', value=12.1)
    obs_id = obs.id
    obs.ref_area = 'France'
    obs.ref_year = 2000
    return obs


if __name__ == '__main__':
    print main()