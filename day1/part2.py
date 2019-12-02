#!/usr/bin/python3

import math

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()

masses = [int(x) for x in contents]

def calc_fuel(mass):
    partial_fuel = math.floor(mass / 3) - 2

    if partial_fuel <= 0:
        return 0
    else:
        return partial_fuel + calc_fuel(partial_fuel)

print(sum([calc_fuel(mass) for mass in masses]))

