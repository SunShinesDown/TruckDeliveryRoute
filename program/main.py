# student ID: 010057350
import datetime
from re import M
from Truck import Truck
from Package import Package
from LoadDistanceData import loadDistanceData, loadAddressData
from LoadPackageData import loadPackageData
from HashTable import HashTable
from statusEnum import Status

packages = HashTable(20)
distanceData = []
addressData = []

loadDistanceData(distanceData)
loadAddressData(addressData)
loadPackageData(packages)

# function to return distance between 2 addresses
def distanceBetween(address1, address2):
    toReturn = distanceData[addressData.index(address1)][addressData.index(address2)]
    if toReturn == "":
        toReturn = distanceData[addressData.index(address2)][addressData.index(address1)]
    return toReturn

# function using greedy algorithm for delivering packages based on the next closest address
def deliverPackages(truck):
    for i in range(len(truck.packages)):
        minMiles = ''
        nextPackage = truck.packages[i]
        for j in range(len(truck.packages)):
            if truck.packages[j].status != Status.delivered: 
                curr = distanceBetween(truck.current_location, truck.packages[j].address)
                curr = float(curr)
                if "wrong address" in truck.packages[j].specialNotes.lower() and j < len(truck.packages) - 1:
                    if truck.current_time < datetime.time(10, 20):
                        continue
                    else:
                            truck.packages[j].address = "410 South State St"
                            truck.packages[j].zipcode = "84111"
                if minMiles == '':
                    minMiles = curr
                    nextPackage = truck.packages[j]
                elif curr < minMiles:
                    minMiles = curr
                    nextPackage = truck.packages[j]
        truck.total_miles += round(float(minMiles), 2)
        truck.current_location = nextPackage.address
        mins = round((float(minMiles) / (18 / 60)))
        currentTimeMins = (truck.current_time.hour * 60) + truck.current_time.minute + mins
        currentTimeHours = currentTimeMins // 60
        currentTimeMins %= 60
        truck.current_time = datetime.time(currentTimeHours, currentTimeMins)
        nextPackage.deliveryTime = truck.current_time
        nextPackage.status = Status.delivered
    truck.current_location = "HUB"

# function for loading the truck
def loadTruck(truck, packages, time):
    truck.packages = packages
    truck.current_time = time
    truck.load_time = time
    for package in truck.packages:
        package.status = Status.inRoute
        package.loadingTime = truck.load_time
        package.truck = truck.name
# findPackage function that finds the package in hashtable and returns the object
def findPackage(hashTable, key):
    return hashTable.search(key)

# lookup function that takes in a package id and returns a list containing each component of that specific package
def lookup(key):
    package = packages.search(key)
    components = [package.address, package.deadline, package.city, package.zipcode, package.weight, package.status]
    return components

# prints choices for user input in commandline interface when called.
def printOptions():
    print("choose from the following: ")
    print("view package info and status for a specific package at a specific time: input 'package Id #' and then time in the format 'hour,mintue' (0-23, 0-59)")
    print("view package info and status for all packages at a specific time: input 'all' and then time when asked in the format 'hour,minute' (0-23, 0-59)")
    print("view total mileage of all three trucks: input 'total'")
    print("quit application: input q/quit")


# lines group packages for each truck based on requirements
truck1Packages = [
    packages.search(1),
    packages.search(13),
    packages.search(14),
    packages.search(15),
    packages.search(16),
    packages.search(20),
    packages.search(29),
    packages.search(11),
    packages.search(34),
    packages.search(2),
    packages.search(4),
    packages.search(5),
    packages.search(7),
    packages.search(17),
    packages.search(19),
    packages.search(8),
]
truck2Packages = [
    packages.search(37),
    packages.search(40),
    packages.search(12),
    packages.search(30),
    packages.search(10),
    packages.search(31),
    packages.search(25),
    packages.search(6),
    packages.search(23),
    packages.search(18),
    packages.search(24),
    packages.search(33),
    packages.search(3),
    packages.search(35),
    packages.search(36),
    packages.search(38),
]
truck3Packages = [
    packages.search(27),
    packages.search(9),
    packages.search(26),
    packages.search(28),
    packages.search(32),
    packages.search(21),
    packages.search(39),
    packages.search(22),
]

# initialize the 3 trucks
truck1 = Truck("truck 1")
truck2 = Truck("truck 2")
truck3 = Truck("truck 3")

# load the truck1 and truck 2 with their packages, truck3 waits until one of the 2 drivers is back
loadTruck(truck1, truck1Packages, datetime.time(8,0))
loadTruck(truck2, truck2Packages, datetime.time(9,5))

# deliver truck1 and truck2 packages. have the driver that returns first load and deliver truck3 packages.
for truck in [truck1, truck2]:
    deliverPackages(truck)
        
if truck1.current_time < truck2.current_time:
    loadTruck(truck3, truck3Packages, truck1.current_time)
else:
    loadTruck(truck3, truck3Packages, truck2.current_time)

deliverPackages(truck3)

# commandline interface
printOptions()
userInput = input()
while userInput.lower() != "q" and userInput.lower() != "quit":
    if userInput.lower() == "all":
        timeInput = input().split(",")
        hour = timeInput[0].strip()
        minute = timeInput[1].strip()
        if hour.isdigit() and minute.isdigit():
            hour = int(hour)
            minute = int(minute)
            if 0 <= hour < 24 and 0 <= minute < 60:
                print(f"\nall packages with status at time {hour}:{minute}")
                print()
                print("package ID, address, city, zipcode, deadline, weight, delivery time, status, truck")
                print()
                for i in range(1,41):
                    status = None
                    package = findPackage(packages, i)
                    if datetime.time(hour, minute) <= package.loadingTime:
                        status = "at hub"
                    elif package.loadingTime < datetime.time(hour, minute) < package.deliveryTime:
                        status = "in route"
                    elif package.deliveryTime <= datetime.time(hour, minute):
                        status = "delivered"
                    holder = package.address
                    holderZ = package.zipcode
                    if i == 9:
                        if datetime.time(hour, minute) < datetime.time(10, 20):
                            package.address = "300 State St"
                            package.zipcode = "84103"
                    print(str(package) + ", " + status + ", " + package.truck)
                    package.address = holder
                    package.zipcode = holderZ
            else:
                print("Invalid entry. hour and minute should be 0-23 and 0-59 respectively.")
        else:
            print("Invalid entry. time input should be in 'hour,minute' format.")
    elif userInput.isdigit():
        if int(userInput) in range(1,41):
            timeInput = input().split(",")
            hour = timeInput[0].strip()
            minute = timeInput[1].strip()
            if hour.isdigit() and minute.isdigit():
                hour = int(hour)
                minute = int(minute)
                if 0 <= hour < 24 and 0 <= minute < 60:
                    print(f"\n package with id {int(userInput.strip())} with status at time {hour}:{minute}")
                    print()
                    print("package ID, address, city, zipcode, deadline, weight, delivery time, status, truck")
                    print()
                    status = None
                    package = findPackage(packages, int(userInput.strip()))
                    if datetime.time(hour, minute) <= package.loadingTime:
                        status = "at hub"
                    elif package.loadingTime < datetime.time(hour, minute) < package.deliveryTime:
                        status = "in route"
                    elif package.deliveryTime <= datetime.time(hour, minute):
                        status = "delivered"
                    holder = package.address
                    holderZ = package.zipcode
                    if int(userInput) == 9:
                        if datetime.time(hour, minute) < datetime.time(10, 20):
                            package.address = "300 State St"
                            package.zipcode = "84103"
                    print(str(package) + ", " + status + ", " + package.truck)
                    package.address = holder
                    package.zipcode = holderZ
                else:
                    print("Invalid entry. hour and minute should be 0-23 and 0-59 respectively.")
            else:
                print("Invalid entry. time input should be in 'hour,minute' format.")
        else:
            print("invalid entry. package ID must be in range 1-40")
    elif userInput.lower() == "total":
        total = truck1.total_miles + truck2.total_miles + truck3.total_miles
        print(f"truck 1: {truck1.total_miles:.2f}")
        print(f"truck 2: {truck2.total_miles:.2f}")
        print(f"truck 3: {truck3.total_miles:.2f}")
        print(f"total mileage: {total:.2f}")
    else:
        print("wrong entry. choose from provided options.")
    print()
    printOptions()
    userInput = input()

print("you have successfully quited the application")




