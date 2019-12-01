#!/usr/bin/python3

import math

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()

masses = [int(x) for x in contents]

print(sum([math.floor(mass / 3) - 2 for mass in masses]))

