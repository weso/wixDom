__author__ = 'guillermo'

from wi.domain.model.observation import create_observation


def main():
    obs = create_observation(ref_area='Spain', ref_year=2001)
    obs._discarded = True
    return obs


if __name__ == '__main__':
    print main()