__author__ = 'guillermo'

from infrastructure.mongo_repos.area_repository import AreaRepository
from infrastructure.mongo_repos.indicator_repository import IndicatorRepository


def main():
    #Areas
    area_repo = AreaRepository()
    print "Country: ", area_repo.find_countries_by_code("es")
    print "Continents: ", area_repo.find_continents()
    print "Countries: ", [country for country in area_repo.find_countries()]
    print "Area Error", area_repo.area_error("sd")

    #Indicators
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

if __name__ == '__main__':
    main()