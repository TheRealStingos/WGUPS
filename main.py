#C950 Data Structures and Algorithms 2 - Justin Moore - WGU ID 011044940
import csv
import datetime
import truck

from hashTable import HashTable
from package import Package

# read distance CSV file
with open("package + distance files/CSV/WGUPS Distance Table.csv", encoding='utf-8-sig') as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)

# read package CSV file
with open("package + distance files/CSV/WGUPS Package File.csv", encoding='utf-8-sig') as csvfile1:
    CSV_Package = csv.reader(csvfile1)
    CSV_Package = list(CSV_Package)

# read address CSV file
with open("package + distance files/CSV/Address.csv", encoding='utf-8-sig') as csvfile2:
    CSV_Address = csv.reader(csvfile2)
    CSV_Address = list(CSV_Address)

# load package data into hashtable
def load_package_info(filename, package_hash_table):
    with open(filename, encoding='utf-8-sig') as package_info:
        package_data = csv.reader(package_info)
        # iterate through each package in CSV file and extract package details
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDelivery_deadline = package[5]
            pWeight = package[6]
            pStatus = "At hub" # set initial status for all packages

            # create new Package object and adds it to the hash table
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDelivery_deadline, pWeight, pStatus)
            package_hash_table.add(pID, p)


# function to calculate distance between two locations
def distance_between(location1_index, location2_index):
    try:
        distance = CSV_Distance[location1_index][location2_index]

        # if distance is blank, check the reverse direction
        if not distance:
            distance = CSV_Distance[location2_index][location1_index]

        return float(distance)
    except: return None

# function to standardize address formats
def standardize_address(address):
    # first, convert to lowercase
    address = address.lower()

    # create a list of replacements
    directions = {
        'south': 's',
        'north': 'n',
        'east': 'e',
        'west': 'w'
    }

    # do each replacement one at a time
    for full_name, abbreviation in directions.items():
        address = address.replace(full_name, abbreviation)

    return address

# function to get address for package from CSV
def get_address(address):
    try:
        # first standardize the input address
        std_address = standardize_address(address)

        # look through each row in the address CSV
        for i, row in enumerate(CSV_Address):
            if len(row) < 2:  # skip empty rows
                continue

            # standardize the address from the CSV
            csv_address = standardize_address(row[0])

            # if they match return address
            if std_address in csv_address:
                return i

            # check if address format is reversed
            if len(row) > 1:
                csv_address_alt = standardize_address(row[1])
                if std_address in csv_address_alt:
                    return i

        # return error if address is not found
        print(f"Warning: Couldn't find address in lookup table: {address}")
        return 0

    # if an error occurs elsewhere, alert user
    except Exception as e:
        print(f"Error looking up address {address}: {str(e)}")
        return 0


# define package assignments for each truck
def get_truck_package_assignments():
    # truck 1 packages - leaves at 8:00 AM
    truck1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

    # truck 2 packages - leaves at 9:05 AM
    truck2_packages = [3, 6, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]

    # truck 3 packages - leaves at 10:20 AM
    truck3_packages = [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33]

    return truck1_packages, truck2_packages, truck3_packages

# create hashtable for package storage
package_hash_table = HashTable()

def initialize_trucks():
    truck1_packages, truck2_packages, truck3_packages = get_truck_package_assignments()

    hub_address = "4001 South 700 East"

    # initialize trucks with their respective departure times and packages
    truck1 = truck.Truck(
        truck_number=1,
        capacity=16,
        speed=18,
        load=None,
        packages=truck1_packages,
        mileage=0.0,
        address=hub_address,
        departure_time=datetime.timedelta(hours=8)
    )

    truck2 = truck.Truck(
        truck_number=2,
        capacity=16,
        speed=18,
        load=None,
        packages=truck2_packages,
        mileage=0.0,
        address=hub_address,
        departure_time=datetime.timedelta(hours=9, minutes=5)
    )

    truck3 = truck.Truck(
        truck_number=3,
        capacity=16,
        speed=18,
        load=None,
        packages=truck3_packages,
        mileage=0.0,
        address=hub_address,
        departure_time=datetime.timedelta(hours=10, minutes=20)
    )

    for package_id in truck1_packages:
        package = package_hash_table.lookup(package_id)
        if package:
            package.truck_number = 1

    for package_id in truck2_packages:
        package = package_hash_table.lookup(package_id)
        if package:
            package.truck_number = 2

    for package_id in truck3_packages:
        package = package_hash_table.lookup(package_id)
        if package:
            package.truck_number = 3

    return truck1, truck2, truck3

truck1, truck2, truck3 = initialize_trucks()

# load all packages into the hash table
load_package_info("package + distance files/CSV/WGUPS Package File.csv", package_hash_table)

# function to deliver packages for truck
def deliver_packages(truck):
    # create list of packages that need to be delivered
    not_delivered = []
    for packageID in truck.packages:
        package = package_hash_table.lookup(packageID)
        package.truck_number = truck.truck_number
        not_delivered.append(package)

    truck.packages.clear()


    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None

        # find the closest package from current location
        for package in not_delivered:
            if distance_between(get_address(truck.address), get_address(package.address)) <= next_address:
                next_address = distance_between(get_address(truck.address), get_address(package.address))
                next_package = package

        # add the closest package to truck's delivery list
        truck.packages.append(next_package.p_id)

        not_delivered.remove(next_package)

        # update trucks mileage
        truck.mileage += next_address

        truck.address = next_package.address

        # update truck's time based on distance and speed
        truck.time += datetime.timedelta(hours=next_address / truck.speed)

        # record delivery and departure times for package
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.time

# deliver packages for each truck
deliver_packages(truck1)
deliver_packages(truck2)

# Wait for first two trucks before starting truck3
deliver_packages(truck3)

# create command line interface function
def run_delivery_gui():
    # Print welcome message and total mileage
    print("Western Governors University Parcel Service (WGUPS)")
    print("The total mileage for all routes is:", truck1.mileage + truck2.mileage + truck3.mileage)

    while True:
        try:
            # Get time input from user
            time_input = input("\nPlease enter a time to check package status (HH:MM:SS) or 'quit' to exit: ")

            if time_input.lower() == 'quit':
                print("Thank you for using WGUPS. Goodbye!")
                break

            # Convert input time to timedelta
            try:
                hours, minutes, seconds = map(int, time_input.split(':'))
                check_time = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except ValueError:
                print("Invalid time format. Please use HH:MM:SS format (e.g., 13:30:00)")
                continue

            # Ask user for status of 1 package or all
            view_option = input("\nEnter '1' to check a single package or 'all' to view all packages: ").lower()

            # single package lookup
            if view_option == '1':
                try:
                    package_id = int(input("Enter the package ID (1-40): "))
                    if 1 <= package_id <= 40:
                        package = package_hash_table.lookup(package_id)
                        if package:
                            package.update_status(check_time)
                            print("\nPackage Status:")
                            print(f"Assigned to Truck: {package.truck_number}")
                            print(str(package))
                        else:
                            print(f"Package {package_id} not found.")
                    else:
                        print("Invalid package ID. Please enter a number between 1 and 40.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # all package lookup
            elif view_option == 'all':
                print("\nAll Packages Status:")
                for package_id in range(1, 41):
                    package = package_hash_table.lookup(package_id)
                    if package:
                        package.update_status(check_time)
                        truck_info = f"Truck {package.truck_number}" if package.truck_number else "Not assigned"
                        print(f"Assigned to Truck: {package.truck_number}")
                        print(str(package))
                        print("-" * 100)

            else:
                print("Invalid option. Please enter '1' or 'all'.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")


# start the interface after all deliveries are calculated
if __name__ == "__main__":
    run_delivery_gui()