#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()

orbit_listings = [x.split(')') for x in contents]

orbit_dict = {listing[1]: listing[0] for listing in orbit_listings}

print(orbit_dict)

class Node:
    def __init__(self, label):
        self.label = label
        self.parent = None 
        self.children = []

    def add_child(self, node):
        self.children.append(node)

root = None
node_dict = {}

for orbit in orbit_dict.items():
    orbitee = orbit[1]
    orbiter = orbit[0]

    if orbitee not in node_dict:
        node_dict[orbitee] = Node(orbitee)
        if orbitee == 'COM':
            root = node_dict[orbitee]
    if orbiter not in node_dict:
        node_dict[orbiter] = Node(orbiter)

    node_dict[orbiter].parent = node_dict[orbitee]
    node_dict[orbitee].add_child(node_dict[orbiter])

def count_parents(node):
    if node.parent == None:
        return 0
    else:
        return count_parents(node.parent) + 1

total_orbits = 0

for node in node_dict.values():
    total_orbits += count_parents(node)

print(total_orbits)

