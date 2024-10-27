from statusEnum import Status

# package class with fields for each data component
class Package:
    def __init__(self, packageId, address, deadline, city, zipcode, weight, specialNotes):
        self.id = packageId
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.specialNotes = specialNotes
        self.status = Status.atHub
        self.loadingTime = None
        self.deliveryTime = None
        self.truck = None
    # called when printing, displays each of the components separated by comma
    def __str__(self):
        return f'{self.id}, {self.address}, {self.city}, {self.zipcode}, {self.deadline}, {self.weight}, {self.deliveryTime}'
