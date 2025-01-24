import sys
sys.path.insert(0, '../')
from planet_wars import PlanetWars, Planet, Fleet, issue_order
from functools import *
from typing import List
import logging

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def not_enough_planets(state):
    return len(state.my_planets()) <= 6


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


def have_smallest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           < sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_most_planets(state):
    return len(state.my_planets()) > len(state.enemy_planets())

def have_fewest_planets(state):
    return len(state.my_planets()) < len(state.enemy_planets())

def have_strongest_planet(state):
    my_strongest = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    enemy_strongest = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    
    if my_strongest is None:
        return False
    if enemy_strongest is None:
        return True
    
    return my_strongest.num_ships > enemy_strongest.num_ships