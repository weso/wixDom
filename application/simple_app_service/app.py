__author__ = 'guillermo'

from infrastructure.mongo_repos.area_repository import AreaRepository


def main():
    area_repo = AreaRepository()
    print "Country: ", area_repo.find_countries_by_code("es")
    print "Continents: ", area_repo.find_continents()
    print "Countries: ", [country for country in area_repo.find_countries()]
    print "Error", area_repo.area_error("sd")

if __name__ == '__main__':
    main()