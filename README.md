## Project Overview

This project implements a package delivery routing system that solves a variant of the Traveling Salesman Problem (TSP). The system manages a fleet of three delivery trucks that must deliver 40 packages efficiently while meeting specific delivery deadlines and constraints.

### Problem Requirements

- **Fleet Size:** 3 trucks with 16-package capacity each
- **Package Count:** 40 packages total across Salt Lake City
- **Speed Limit:** 18 mph for all trucks  
- **Working Hours:** 8:00 AM - 5:00 PM
- **Special Constraints:** 
  - Some packages have delivery deadlines
  - Package #9 has a delayed address correction at 10:20 AM
  - Certain packages must be delivered together or on specific trucks

## Technical Implementation

### Core Data Structures

#### Hash Table (`hashTable.py`)
- **Purpose:** Efficient package storage and retrieval
- **Implementation:** Chaining collision resolution with dynamic resizing
- **Time Complexity:** O(1) average case for insert, lookup, and delete
- **Features:**
  - Load factor monitoring (resizes at 95% capacity)
  - Automatic shrinking when load factor drops below 25%
  - Minimum capacity of 8 buckets

#### Package Class (`package.py`)
- Stores all package information (ID, address, deadline, weight, etc.)
- Implements dynamic status tracking based on current time
- Handles special case for Package #9 address correction

#### Truck Class (`truck.py`)  
- Manages truck properties (capacity, speed, current location, mileage)
- Tracks departure times and current delivery status

### Algorithm Implementation

The system uses a **Greedy Nearest Neighbor Algorithm** for route optimization:

1. **Package Assignment:** Packages are manually assigned to trucks based on constraints
2. **Route Optimization:** For each truck, repeatedly select the closest undelivered package
3. **Time Tracking:** Updates delivery times based on distance and truck speed
4. **Status Management:** Real-time package status updates based on user queries

### Key Features

- **Real-time Package Tracking:** Query any package status at any time
- **Route Optimization:** Minimizes total mileage using nearest neighbor approach  
- **Constraint Handling:** Manages special delivery requirements and deadlines
- **Interactive CLI:** User-friendly command-line interface for package queries
- **Dynamic Address Updates:** Handles Package #9's delayed address correction

## File Structure

```
project/
├── main.py              # Main program logic and CLI interface
├── hashTable.py         # Custom hash table implementation  
├── package.py           # Package class definition
├── truck.py            # Truck class definition
└── package + distance files/CSV/
    ├── WGUPS Distance Table.csv    # Distance matrix between addresses
    ├── WGUPS Package File.csv      # Package details and requirements
    └── Address.csv                 # Address lookup table
```

## Installation and Usage

### Prerequisites
- Python 3.x
- Required CSV files in the `package + distance files/CSV/` directory

### Running the Program

```bash
python main.py
```

### Using the Interface

1. **View Total Mileage:** Displayed on startup
2. **Time Query:** Enter time in HH:MM:SS format (24-hour)
3. **Package Options:**
   - Enter `1` to check a specific package by ID
   - Enter `all` to view all package statuses
4. **Exit:** Type `quit` to exit the program

### Example Usage

```
Western Governors University Parcel Service (WGUPS)
The total mileage for all routes is: 125.4

Please enter a time to check package status (HH:MM:SS) or 'quit' to exit: 10:30:00

Enter '1' to check a single package or 'all' to view all packages: 1
Enter the package ID (1-40): 15

Package Status:
Assigned to Truck: 1
Package ID: 15, Address: 300 State St, City: Salt Lake City, State: UT, 
Zipcode: 84103, Deadline: 9:00 AM, Weight: 4, Status: Delivered at 9:12:00
```

## Algorithm Analysis

### Time Complexity
- **Package Lookup:** O(1) average case using hash table
- **Route Calculation:** O(n²) for nearest neighbor algorithm per truck
- **Overall System:** O(n²) where n is the number of packages

### Space Complexity
- **Hash Table:** O(n) for package storage
- **Distance Matrix:** O(m²) where m is the number of addresses
- **Overall:** O(n + m²)

### Performance Results
- **Total Mileage:** Typically under 140 miles for all routes
- **Delivery Success:** All packages delivered within constraints
- **Time Efficiency:** All deliveries completed well before 5:00 PM deadline

## Design Decisions

### Package Assignment Strategy
Packages are pre-assigned to trucks based on:
- Delivery deadlines (urgent packages on early trucks)
- Geographic clustering (nearby addresses on same truck)
- Special requirements (grouped deliveries, truck-specific packages)

### Algorithm Choice: Greedy Nearest Neighbor
**Advantages:**
- Simple to implement and understand
- Provides reasonably good solutions for small problem sizes
- Fast execution time
- Meets project requirements effectively

**Trade-offs:**
- Not guaranteed to find optimal solution
- Can get stuck in local optima
- Performance degrades with problem size

**Alternative Considerations:**
- Genetic Algorithm: Better optimization but more complex
- Dynamic Programming: Optimal but exponential time complexity
- Simulated Annealing: Good optimization but harder to tune

## Special Constraints Handled

1. **Package #9 Address Correction:** Automatically updates address at 10:20 AM
2. **Delivery Deadlines:** Packages assigned to appropriate trucks to meet deadlines
3. **Truck Capacity:** Maximum 16 packages per truck enforced
4. **Working Hours:** All deliveries completed within business hours
5. **Package Dependencies:** Related packages assigned to same truck

## Learning Outcomes

This project demonstrates mastery of:
- Custom data structure implementation (hash tables)
- Algorithm design and analysis
- Object-oriented programming principles
- File I/O and CSV processing
- Problem-solving for real-world logistics challenges
- Time and space complexity analysis

---

*This project successfully demonstrates the application of data structures and algorithms to solve a practical logistics optimization problem while meeting all specified constraints and requirements.*
