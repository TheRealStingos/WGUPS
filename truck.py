# Create class for delivery trucks
class Truck:
    def __init__(self, truck_number, capacity, speed, load, packages, mileage, address, departure_time):
        self.truck_number = truck_number
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.time = departure_time


        # return string so user can easily see truck information
        def __str__(self):
            return f"Truck {self.truck_number} - Capacity: {self.capacity}, Speed: {self.speed}, Load: {self.load}, Packages: {self.packages}, Mileage: {self.mileage}, Address: {self.address}"