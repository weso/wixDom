__author__ = 'guillermo'

from wi.domain.model.observation import create_observation


def main():
    return (create_observation(issued='date' + str(obs), ref_indicator='ind01',
                               ref_area='Spain',
                               ref_year=2001, data_set="DataSet01", computation='090',
                               label='Observation of Spain', publisher="WebFoundation",
                               obs_type="Observation", status='Some Status', value=12.1)
            for obs in xrange(5))


if __name__ == '__main__':
    for x in main():
        print x