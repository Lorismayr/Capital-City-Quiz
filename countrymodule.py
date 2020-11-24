class Country():
    country_name = None
    capital_city = None
    picturename = None
    alternate_names = []

    # constructor
    def __init__(self, country_name, capital_city, other=[], picturename=None):
        self.country_name = country_name
        self.capital_city = capital_city
        self.alternate_names = other
        self.picturename = "Pictures/" + picturename

    # getter for capital city of self
    def getCap(self):
        return self.capital_city

    # getter for country of self
    def getCountry(self):
        return self.country_name
