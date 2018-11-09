# Maximilian Randolph // ID# 000964198

import sys
import enum
import wguPackages
import wguDistances
from itertools import permutations


class PackageStatus(enum.Enum):
    inaccessible = 1
    at_hub = 2
    in_transit = 3
    delivered = 4


class Truck:
    def __init__(self):
        self.packages = []
        self.times = [0]
        self.route = [0]
        self.driver = None

    def addPackage(self, package):
        """
        When a package is added, recalculate the route, and update the times on a 1:1
        mapping to the respective delivery time per package.
        """
        package.status = PackageStatus.in_transit
        self.packages.append(package)
        self.route_optimal_route()
        self.update_delivery_times()

    def removePackage(self, package_id):
        i = 0
        for package in self.packages:
            if package.package_id == package_id:
                del self.times[i]
                return self.packages.pop(i)
            i += 1
        return None

    def deliver_package(self, package_id):
        deliveredPackage = self.removePackage(package_id)
        package_hash_table[deliveredPackage.package_id].status = PackageStatus.delivered
        package_hash_table[deliveredPackage.package_id].delivered_at = clock.time
        if PackageStatus.delivered.name in package_hash_table:
            package_hash_table[PackageStatus.delivered.name] += [deliveredPackage]
        else:
            package_hash_table[PackageStatus.delivered.name] = [
                deliveredPackage]

    def get_current_location(self):
        return self.route[0]

    def route_optimal_route(self):
        self.route = find_best_route(
            [self.get_current_location()] + [package.locationIndex for package in self.packages])

    def update_delivery_times(self):
        self.times = [0]
        for i in range(len(self.route)-1):
            self.times.append(calc_route_time(
                [self.route[i], self.route[i+1]]) + self.times[i])

    def update_package_status(self, time):
        for i in range(len(self.times)):
            if time >= self.times[i]:
                self.deliver_package(self.packages[i].package_id)

    def remaining_route_time(self):
        return calc_route_time(self.route)


class Clock:
    def __init__(self):
        self.hour = 8
        self.minute = 0.0
        self.time = str(self.hour) + str(self.minute)

    def add_minutes(self, minutes=1):
        self.minute += minutes
        if self.minute >= 60:
            if self.minute == 60:
                self.hour += 1
                self.minute = 0
            else:
                over = self.minute - 60
                self.hour += 1 + (over // 60)
                self.minute = over % 60

    def __str__(self):
        return str(int(self.hour)) + str("%02d" % int(self.minute))

    def minute_tick(self):
        self.add_minutes(1)


class Driver:
    def __init__(self, driverId, name):
        self.driverId = driverId
        self.name = name

    def __str__(self):
        return "Driver #" + str(self.driverId) + "\n" + "Name: " + self.name


class Package:
    def __repr__(self):
        return str(self.locationIndex)

    def __init__(self, package_id, address, city, zipCode, deadline=None, weight=0, locationIndex=0, status=2):
        """
        ctor function and adds all values to package hash table.
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
        package_list.append(self)

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
        return (
            "Package Id #" + str(self.package_id) + " \t " + "Address: " + str(self.address) + "\t" + "Deadline: " + str(self.deadline) + " \t " + "City: " + str(
                self.city) + " \t " + "Zip Code: " + str(self.zipCode) + " \t " + "Weight: " + str(self.weight) + " \t " + "Status: " + str(self.status.name)
            + " \t " + "Delivered At: " + str(self.delivered_at)
        )


def lookup_package(key):
    """
    This function will take either an integer for looking up ids or strings for looking up any other package
    value in the package hash table.
    """
    if type(key) is int and key in package_hash_table:
        print(package_hash_table[key])
    else:
        for package in [str(package) for package in package_hash_table[str(key)]]:
            print(package)


def show_all_package_status():
    """
    This function will take either an integer for looking up ids or strings for looking up any other package
    value in the package hash table.
    """
    for package in package_list:
        print(package)


def calc_distance(pointA, pointB):
    distances = wguDistances.distances
    return distances[min(pointA, pointB)][max(pointA, pointB)-min(pointA, pointB)]


def calc_route_time(route):
    """
    calculate the total trip distance divided by 18 mph, multiplied by 60 minutes per hour.
    """
    return round((total_distance(route) / 18) * 60, 2)


def total_distance(locations):
    return sum([calc_distance(location, locations[index + 1]) for index, location in enumerate(locations[:-1])])


def find_best_route(nodes):
    """
    This function will map out the best route based on nearest neighbor of last node in path.
    """
    not_visited = nodes
    path = [nodes[0]]
    not_visited.remove(nodes[0])
    while not_visited:
        nearest_node = get_nearest_neighbor(path[-1], not_visited)
        path.append(nearest_node)
        not_visited.remove(nearest_node)
    return path


def get_nearest_neighbor(current_node, available_nodes):
    return min(available_nodes, key=lambda x: calc_distance(current_node, x))


def get_farthest_neighbor(current_node, available_nodes):
    return max(available_nodes, key=lambda x: calc_distance(current_node, x))


def longest_path(locations, start=0):
    """
    This function will get the farthest point from point given in order to help sort packages
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


def recall_closest_truck():
    """
    This function should send out an alert to the nearest available truck to come to the hub
    and pick up a package that has arrived late.
    """


def divide_packages(packages):
    """
    We have only two drivers, but a handful of packages. In order to divide the packages so that they
    are taken on efficient routes, we can take two lists of packages, choose the farthest neighbor
    from the hub, and then choose the farthest node from that neighbor as a starting point for the second truck.

    Those starting points will be the farthest apart from each other, so we can then choose the nearest node
    for each one and work our way through the remaining packages.
    """
    load_one = []
    load_two = []

    # Start at Hub/Node 0
    last_node_selected = 0
    add_to_one = True

    while packages:
        remaining_stops = get_remaining_stops(packages)
        # Select node that is farthest from currently selected one so that division is on the far ends
        # of the limits of delivery zone.
        next_node = get_farthest_neighbor(
            last_node_selected, remaining_stops)

        last_node_selected = next_node
        # Add all packages to a single load that have a shared destination
        for package in packages:
            if package.locationIndex == next_node:
                if add_to_one == True:
                    load_one.append(package)
                else:
                    load_two.append(package)
                packages.remove(package)
        # Alternate this value so that each load gets evenly distributed
        add_to_one = add_to_one == False
    return (load_one, load_two)


def get_remaining_stops(packages):
    """
    Returns a list of unique stops remaining for list of packages passed.
    """
    return list(set([package.locationIndex for package in packages]))


package_hash_table = {}
package_list = []
clock = Clock()


def main():
    truck_one = Truck()
    truck_two = Truck()
    truck_three = Truck()

    all_packages = []
    # for package in wguPackages.packages + wguPackages.priority_packages + wguPackages.grouped_packages:
    for package in wguPackages.packages + wguPackages.priority_packages + wguPackages.grouped_packages + wguPackages.delayed_packages + wguPackages.wrong_address_packages + wguPackages.truck_two_packages:
        # truck_one.addPackage()
        all_packages.append(Package(
            package[0], package[1], package[2], package[3], package[4], package[5], package[6]))

    loads = divide_packages(all_packages)
    print(str(loads[0]))
    print(str(loads[1]))

    truck_one.packages = loads[0]
    truck_two.packages = loads[1]

    truck_one.route_optimal_route()
    truck_two.route_optimal_route()

    print(truck_one.times)
    print(truck_two.times)

    show_all_package_status()

    truck_one.update_package_status(37)
    print()
    lookup_package(PackageStatus.delivered.name)


if __name__ == '__main__':
    main()
