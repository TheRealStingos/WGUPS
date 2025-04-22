# Create class for packages
import datetime


class Package:
    def __init__(self, p_id, address, city, state, zipcode, delivery_deadline, weight,status ):
        self.p_id = p_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = status
        self.delivery_time = None
        self.departure_time = None
        self.truck_number = None

    # return package information to user
    def __str__(self):
        truck_info = f", truck: {self.truck_number}" if self.truck_number else ""
        return f"Package ID: {self.p_id}, Address: {self.address}, City: {self.city}, State: {self.state}, Zipcode: {self.zipcode}, Deadline: {self.delivery_deadline}, Weight: {self.weight}, Status: {self.status}"

    # package status update method
    def update_status(self, current_time):

        if self.p_id == 9:
            address_change_time = datetime.timedelta(hours=10, minutes=20)
            if current_time >= address_change_time:
                self.address = "410 S. State St."
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zipcode = "84111"
            else:
                self.address = "300 State St."
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zipcode = "84103"

        truck_departure_times = {
            1: datetime.timedelta(hours=8),
            2: datetime.timedelta(hours=9, minutes = 5),
            3: datetime.timedelta(hours=10, minutes = 20),
        }

        truck_departure_time = truck_departure_times[self.truck_number]

        if self.truck_number is None:
            self.status = "At hub"
            return

        if current_time < truck_departure_time:
            self.status = f"Loaded onto Truck {self.truck_number}"

        elif self.delivery_time and current_time >= self.delivery_time:
            self.status = f"Delivered at {self.delivery_time}"

        elif current_time >= truck_departure_time:
            self.status = f"En route on Truck {self.truck_number}"
        else:
            self.status = f"At hub"