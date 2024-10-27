# truck class to keep track of a truck's total miles, current location, and other information that may be needed.
class Truck:
    def __init__(self, name):
        self.name = name
        self.packages = []
        self.total_miles = 0
        self.current_location = "HUB"
        self.speed = 18
        self.load_time = None
        self.current_time = None
