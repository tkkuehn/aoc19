#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()

orbit_listings = [x.split(')') for x in contents]

orbit_dict = {listing[1]: listing[0] for listing in orbit_listings}

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

santa = node_dict['SAN']
you = node_dict['YOU']

santa_ancestors = {}
you_ancestors = {}

steps = 0
current = santa

while True:
    steps += 1
    santa_ancestors[current.parent] = steps
    current = current.parent
    if current == root:
        break

steps = 0
current = you 

while True:
    steps += 1
    you_ancestors[current.parent] = steps
    current = current.parent
    if current == root:
        break

common_ancestors = set(santa_ancestors.keys()) & set(you_ancestors.keys())

nearest_common_ancestor = min(common_ancestors,
    key=lambda node: you_ancestors[node])

print(you_ancestors[nearest_common_ancestor] - 1
    + santa_ancestors[nearest_common_ancestor] - 1)

