import sys
import enum
import wguPackages
import wguDistances


class PackageStatus(enum.Enum):
    """
    Enum class for tracking package status.
    """
    inaccessible = 1
    at_hub = 2
    in_transit = 3
    delivered = 4


class Truck:
    """
    Class that represents a Truck object. handles package logic when loading and delivering.
    """

    def __init__(self, truck_number):
        """
        Truck Ctor. Takes a number for identification of truck.

        Time: O(1)
        """
        self.truck_number = truck_number
        self.packages = []
        self.times = []
        self.route = []
        self.driver = None
        self.time_passed = 0
        self.miles = 0

    def addPackage(self, package):
        """
        When a package is added, recalculate the route, and update the times on a 1:1
        mapping to the respective delivery time per package. Tracks when the last package
        was loaded onto the truck for logging purposes.

        Note that adding a package will trigger re-routing so that the times and route
        reflect an accurate and efficient ETA.

        Time: Calls functions that are O(N^2)
        """
        package.status = PackageStatus.in_transit
        self.time_passed = clock.time_passed
        self.packages.append(package)
        self.determine_optimal_route()
        self.update_delivery_times()

    def remove_package(self, package_id):
        """
        Removes a package from the truck with the passed package_id

        Time: O(N)
        """
        i = 0
        for package in self.packages:
            if package.package_id == package_id:
                return self.packages.pop(i)
            i += 1
        return None

    def deliver_package(self, package_id, time):
        """
        Delivers a package, marks package in the system as being "delivered".

        Time: O(1)
        """
        deliveredPackage = package_hash_table[package_id]
        package_hash_table[deliveredPackage.package_id].status = PackageStatus.delivered
        package_hash_table[deliveredPackage.package_id].delivered_at = str(
            clock) + " by truck #" + str(self.truck_number)
        if PackageStatus.delivered.name in package_hash_table:
            package_hash_table[PackageStatus.delivered.name] += [deliveredPackage]
        else:
            package_hash_table[PackageStatus.delivered.name] = [
                deliveredPackage]
        try:
            package_hash_table[PackageStatus.in_transit.name].remove(
                deliveredPackage)
        except:
            pass

    def determine_optimal_route(self):
        """
        Will use the package indexes referenced against the location table to determine
        the best route to use.

        Time: Equals runtime of find_best_route aka. O(N^2)
        """
        self.route = find_best_route(
            [package.locationIndex for package in self.packages])

    def update_delivery_times(self):
        """
        Updates the times that each package is anticipated as being delivered.

        Time: O(N)
        """
        # print("my route is:" + str(self.route))
        self.times = [calc_route_time([0, self.route[0]])]
        for i in range(len(self.route)-1):
            self.times.append(calc_route_time(
                [self.route[i], self.route[i+1]])+self.times[i])

    def update_package_status(self, time):
        """
        Runs an update to check if any of the packages currently on board the truck have
        been delievered. If they have been, then it marks the packages appropriately.

        Time: O(N)
        """
        for i in range(len(self.times)):
            if (time + self.time_passed) >= self.times[i]:
                if (self.packages[i].status != PackageStatus.delivered):
                    self.deliver_package(
                        self.packages[i].package_id, self.times[i])
                    self.miles += calc_distance(self.route[i], self.route[i-1])


class Clock:
    """
    Clock class that manages a 24 hour clock. Allows adding arbirtrary minutes while maintaining
    correct time up to 2400.
    """

    def __init__(self):
        """
        Clock Ctor
        """
        self.hour = 8
        self.minute = 0.0
        self.time_passed = 0

    def __str__(self):
        return str(int(self.hour)) + str("%02d" % int(self.minute))

    def add_minutes(self, minutes=1):
        """
        Adds passed minutes to the clock.

        Time: O(1)
        """
        self.minute += minutes
        self.time_passed += minutes

        # Calculates overage of hour in the minutes, and updates time accordingly.
        if self.minute >= 60:
            if self.minute == 60:
                self.hour += 1
                self.minute = 0
            else:
                over = self.minute - 60
                self.hour += 1 + (over // 60)
                self.minute = over % 60


class Package:
    """
    Package Class. These things get delivered to various places around Salt Lake City.
    """

    def __repr__(self):
        """
        The package is represented by its destination node id.
        """
        return str(self.locationIndex)

    def __init__(self, package_id, address, city, zipCode, deadline=None, weight=0, locationIndex=0, status=2):
        """
        Ctor function whick also adds all values to package hash table.

        Each property corresnsponds to data tied to each aspect of the package.

        Time: O(1)
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zipCode = zipCode
        self.weight = weight
        self.deadline = deadline
        self.locationIndex = locationIndex
        self.status = PackageStatus(status)
        self.delivered_at = "N/A"

        package_hash_table[package_id] = self

        # Insert into hash table
        if address in package_hash_table:
            package_hash_table[address] += [self]
        else:
            package_hash_table[address] = [self]

        if city in package_hash_table:
            package_hash_table[city] += [self]
        else:
            package_hash_table[city] = [self]

        if deadline in package_hash_table:
            package_hash_table[deadline] += [self]
        else:
            package_hash_table[deadline] = [self]

        if zipCode in package_hash_table:
            package_hash_table[zipCode] += [self]
        else:
            package_hash_table[zipCode] = [self]

        if str(weight) in package_hash_table:
            package_hash_table[str(weight)] += [self]
        else:
            package_hash_table[str(weight)] = [self]

        if PackageStatus(status).name in package_hash_table:
            package_hash_table[PackageStatus(status).name] += [self]
        else:
            package_hash_table[PackageStatus(status).name] = [self]

    def __str__(self):
        """
        Returns a nicely formatted way to view the package status in string form.

        Time: O(1)
        """
        return (
            "Package Id #" + str(self.package_id) + "\tStatus: " + str(self.status.name) + "\tDeadline: " + str(self.deadline) + " \tDelivered At: " + str(self.delivered_at) + " \tAddress: " + str(self.address) + " \tCity: " + str(
                self.city) + " \tZip Code: " + str(self.zipCode) + " \tWeight: " + str(self.weight)
        )

# System functions


def lookup_package(key):
    """
    This function will take either an integer for looking up ids or strings for looking up any other package
    value in the package hash table.

    Time: O(1)
    """
    if type(key) is int and key in package_hash_table:
        print(package_hash_table[key])
    else:
        try:
            for package in package_hash_table[str(key)]:
                print(package)
        except:
            print("no packages found")


def show_all_package_status(miles):
    """
    This returns all of the statuses of the packages in the system, sorted by ID.

    Time: O(N) if scaled, but in our case, N is limited to 40 packages, so really O(1).
    """
    print("\nWGUPS Status -- Time: " + str(clock) + " | Total Miles Driven: "+ str(round(sum(miles),3)) + " | Truck #1:" +
          str(round(miles[0],3))+" | Truck #2:" + str(round(miles[1],3))+" | Truck #3:" + str(round(miles[2],3)))
    for package in range(1, 41):
        print(package_hash_table[package])


def calc_distance(pointA, pointB):
    """
    Returns the distance between two location nodes, accepting parameters that correspond
    to their respoective location indexes on the node list.

    Time: O(1)
    """
    distances = wguDistances.distances
    return distances[min(pointA, pointB)][max(pointA, pointB)-min(pointA, pointB)]


def calc_route_time(route):
    """
    Calculate the total trip distance divided by 18 mph, multiplied by 60 minutes per hour.

    Time: O(1)
    """
    return round((total_distance(route) / 18) * 60, 2)


def total_distance(locations):
    """
    Accepts a list of location indexes and calculates the total distance between all of them.

    Time: O(N)
    """
    return sum([calc_distance(location, locations[index + 1]) for index, location in enumerate(locations[:-1])])


def find_best_route(nodes, start=0):
    """
    This function will map out the best route based on nearest neighbor of last node in path.

    Time: O(N^2)
    """
    not_visited = nodes
    path = []
    nearest_node = get_nearest_neighbor(start, not_visited)
    path.append(nearest_node)
    not_visited.remove(nearest_node)

    while not_visited:
        nearest_node = get_nearest_neighbor(path[-1], not_visited)
        path.append(nearest_node)
        not_visited.remove(nearest_node)
    return path


def get_nearest_neighbor(current_node, available_nodes):
    """
    Accepts a node index, and returns the nearest neighbor of that node that is in the list of
    nodes available.

    Time: O(N)
    """
    return min(available_nodes, key=lambda x: calc_distance(current_node, x))


def get_farthest_neighbor(current_node, available_nodes):
    """
    Accepts a node index, and returns the farthest neighbor of that node that is in the list of
    nodes available.

    Time: O(N)
    """
    return max(available_nodes, key=lambda x: calc_distance(current_node, x))


def longest_path(locations, start=0):
    """
    This function will create the longest path of nodes from node given in order to help sort packages
    by helping split the available packages and picking the farthest apart to go on separate trucks.

    Time: O(N^2)
    """
    start = locations[start]
    not_visited = locations
    path = [start]
    not_visited.remove(start)
    while not_visited:
        nearest = max(not_visited, key=lambda x: calc_distance(path[-1], x))
        path.append(nearest)
        not_visited.remove(nearest)
    return path


def divide_packages(packages):
    """
    We have only two drivers, but a handful of packages. In order to divide the packages so that they
    are taken on efficient routes, we can take two lists of packages, choose the farthest neighbor
    from the hub, and then choose the farthest node from that neighbor as a starting point for the second truck.

    Those starting points will be the farthest apart from each other, so we can then choose the nearest node
    for each one and work our way through the remaining packages.

    The third load returned will be the truck that leaves after the first two trucks have made their deliveries

    Note that we have hardcoded values based on the list provided to WGUPS. This could be automated if a 
    consistent list delivery system was specified, which would help improve scalability.

    The third load will be loaded assuming it is a delayed package truck.

    Time: O(2N^2)
    """
    # loads correspond to the truck that will carry them, 0 = truck 1 load, 1 = truck 2 load, 2 = truck 3 load
    loads = [[], [], []]

    # Start at Hub/Node 0
    last_node_selected = 0
    load_index = 0

    # packages that have until EOD to be delivered should be added after priority packages.
    no_deadline_packages = [
        package for package in packages if package.package_id in [2, 4, 5, 7, 8, 10, 11, 12, 17, 19, 21, 22, 23, 24, 26, 27, 33, 35, 39]]
    # packages that must be on truck two.
    special_truck_packages = [
        package for package in packages if package.package_id in [3, 18, 36, 38]]

    delayed_packages = [
        package for package in packages if package.package_id in [6, 28, 32, 25, 9]
    ]

    grouped_packages = [
        package for package in packages if package.package_id in [13, 15, 20, 14, 16]
    ]

    packages_to_divide = [
        package for package in packages if package.status != PackageStatus.inaccessible
    ]
    for package in no_deadline_packages + special_truck_packages + delayed_packages + grouped_packages:
        try:
            packages_to_divide.remove(package)
        except:
            pass

    # put all the priority packages on the first truck.
    loads[0] += grouped_packages

    # put all delayed packages on the last truck.
    loads[2] += delayed_packages + special_truck_packages

    while packages_to_divide:
        remaining_stops = get_remaining_stops(packages_to_divide)
        # Select node that is farthest from currently selected one so that division is on the far ends
        # of the limits of delivery zone.
        next_node = get_farthest_neighbor(
            last_node_selected, remaining_stops)

        last_node_selected = next_node
        # Add all packages to a single load that have a shared destination
        for package in packages_to_divide:
            if package.locationIndex == next_node:
                # if the truck is full, use the next truck
                while len(loads[load_index % 2]) >= 15:
                    load_index += 1
                loads[load_index % 2].append(package)
                packages_to_divide.remove(package)
        # Alternate this value so that each load gets evenly distributed
        load_index += 1

    # priority pacakges have been sorted and added to truck loads. Get regular mail now to sort.
    packages_to_divide = no_deadline_packages

    while packages_to_divide:
        remaining_stops = get_remaining_stops(packages_to_divide)
        # Select node that is farthest from currently selected one so that division is on the far ends
        # of the limits of delivery zone.
        next_node = get_farthest_neighbor(
            last_node_selected, remaining_stops)

        last_node_selected = next_node
        # Add all packages to a single load that have a shared destination
        for package in packages_to_divide:
            if package.locationIndex == next_node:
                # if the truck is full, use the next truck
                while len(loads[load_index % 3]) >= 15:
                    load_index += 1
                loads[load_index % 3].append(package)
                packages_to_divide.remove(package)
        # Alternate this value so that each load gets evenly distributed
        load_index += 1
    return (loads[0], loads[1], loads[2])


def get_remaining_stops(packages):
    """
    Returns a list of unique stops remaining for list of packages passed. This is used while
    dividing packages to determine if packages can be grouped.

    Time: O(N)
    """
    return list(set([package.locationIndex for package in packages]))


# This is the hash table where packages are tracked.
package_hash_table = {}
# Clock object for keeping track of the time while deliveries are taking place.
clock = Clock()


def main():
    # Hard coded trucks since WGUPS doesn't have many resources, and why complicate things?
    truck_one = Truck(1)
    truck_two = Truck(2)
    truck_three = Truck(3)

    all_packages = []

    for package in (wguPackages.packages + wguPackages.priority_packages +
                    wguPackages.grouped_packages + wguPackages.truck_two_packages +
                    wguPackages.delayed_packages + wguPackages.wrong_address_packages):
        all_packages.append(Package(
            package[0], package[1], package[2], package[3], package[4], package[5], package[6], package[7]))

    # Divide tha packages and put into a loads tuple. Loads[2] corresponds to packages that cannot
    # be delivered at the first minute, since there's something holding them up.
    loads = divide_packages(all_packages)

    total_miles = [truck_one.miles, truck_two.miles, truck_three.miles]
    # Show all packages before loading.
    show_all_package_status(total_miles)

    # Load packages that have been divided to correspond to appropriate truck.
    for load in loads[0]:
        truck_one.addPackage(load)
    for load in loads[1]:
        truck_three.addPackage(load)

    minutes_passed = 0

    # Check status every minute of 8 hour day.
    while(minutes_passed < 480):
        minutes_passed += 1
        clock.add_minutes(1)
        total_miles = [truck_one.miles, truck_two.miles, truck_three.miles]

        if minutes_passed == 65:
            for load in loads[2]:
                truck_two.addPackage(load)
            # add time that's passed to correctly calculate delivery times.
            # We add the offset because there is a buffer of having two drivers for three trucks.
            # After any truck finishes, this time would be added from whichever truck finishes first.
            offset = min(max(truck_one.times), max(truck_three.times))
            truck_two.times = [time + 65 + offset for time in truck_two.times]

        if minutes_passed == 60:
            show_all_package_status(total_miles)
        if minutes_passed == 125:
            show_all_package_status(total_miles)
        if minutes_passed == 185:
            show_all_package_status(total_miles)

        truck_one.update_package_status(minutes_passed)
        truck_two.update_package_status(minutes_passed)
        truck_three.update_package_status(minutes_passed)

    # Day finished. Show final statuses.
    show_all_package_status(total_miles)


if __name__ == '__main__':
    main()
