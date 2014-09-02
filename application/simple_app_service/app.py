__author__ = 'guillermo'

from infrastructure.mongo_repos.area_repository import AreaRepository
from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository


def get_areas():
    # Areas
    area_repo = AreaRepository()
    print "Country: ", area_repo.find_countries_by_code("es")
    print "Continents: ", area_repo.find_continents()
    print "Countries: ", [country for country in area_repo.find_countries()]
    print "Area Error", area_repo.area_error("sd")
    print "=============================================================================="


def get_indicators():
    # Indicators
    ind_repo = IndicatorRepository()
    print "Indicator", ind_repo.find_indicator_by_code("itu_g")
    print "Indicator children", ind_repo.find_indicator_children("INDEX")
    print "Indicator index", ind_repo.find_indicators_index()
    print "Indicator sub_indexes", ind_repo.find_indicators_sub_indexes()
    print "Indicator components", ind_repo.find_indicators_components()
    print "Primary indicators", ind_repo.find_indicators_primary()
    print "Secondary indicators", ind_repo.find_indicators_secondary()
    print "Indicator indicators", ind_repo.find_indicator_indicators()
    print "Indicator error", ind_repo.indicator_error("foo")
    print "=============================================================================="


def get_observations():
    # Observations
    obs_repo = ObservationRepository()
    print "Observations", [obs for obs in obs_repo.find_observations()]


def main():
    get_areas()

    get_indicators()

    #get_observations()

if __name__ == '__main__':
    main()