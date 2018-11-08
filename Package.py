# from main import masterPackageList
# from PackageStatus import PackageStatus

# class Package:
#     def __init__(self, packId, address, city, zipCode, deadline=None, weight=0, locationIndex=0, status=2):
#         self.packId = packId
#         self.address = address
#         self.city = city
#         self.zipCode = zipCode
#         self.weight = weight
#         self.deadline = deadline
#         self.locationIndex = locationIndex
#         self.status = PackageStatus(status)

#         masterPackageList[packId] = self

#         # Insert into hash table
#         if address in masterPackageList:
#             masterPackageList[address] += [self]
#         else:
#             masterPackageList[address] = [self]

#         if city in masterPackageList:
#             masterPackageList[city] += [self]
#         else:
#             masterPackageList[city] = [self]

#         if deadline in masterPackageList:
#             masterPackageList[deadline] += [self]
#         else:
#             masterPackageList[deadline] = [self]

#         if zipCode in masterPackageList:
#             masterPackageList[zipCode] += [self]
#         else:
#             masterPackageList[zipCode] = [self]

#         if str(weight) in masterPackageList:
#             masterPackageList[str(weight)] += [self]
#         else:
#             masterPackageList[str(weight)] = [self]

#         if PackageStatus(status).name in masterPackageList:
#             masterPackageList[PackageStatus(status).name] += [self]
#         else:
#             masterPackageList[PackageStatus(status).name] = [self]

#     def __str__(self):
#         return "Package Id #" + str(self.packId) + "\n" + "Address: " + str(self.address) + "\n" + "Deadline: " + str(self.deadline) + "\n" + "City: " + str(self.city) + "\n" + "Zip Code: " + str(self.zipCode) + "\n" + "Weight: " + str(self.weight) + "\n" + "Status: " + str(self.status.name)

