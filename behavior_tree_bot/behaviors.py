import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    

def attack_strongest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False
    
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the strongest enemy planet.
    strongest_enemy_planet = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not strongest_enemy_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the strongest enemy planet.
        return issue_order(state, strongest_planet.ID, strongest_enemy_planet.ID, strongest_planet.num_ships / 2)
    

def destory_strongest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False
    
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the strongest enemy planet.
    strongest_enemy_planet = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not strongest_enemy_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send all the ships from my strongest planet to the strongest enemy planet.
        return issue_order(state, strongest_planet.ID, strongest_enemy_planet.ID, strongest_planet.num_ships -1)
    
def spread_to_nuetral_minimum_fleet(state):
    # (1) Create a set to keep track of targeted neutral planets.
    targeted_planets = set(fleet.destination_planet for fleet in state.my_fleets())
    # (2) Sort planets based on strenth
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)

    # (3) Find the weakest neutral planet for each
    for planet in my_planets:
        weakest_planet = None
        min_distance = float('inf')
        for nuetral in state.neutral_planets():
            if nuetral.ID not in targeted_planets:
                distance = state.distance(planet.ID, nuetral.ID)
                if distance < min_distance and nuetral.num_ships < (planet.num_ships - 1):
                    min_distance = distance
                    weakest_planet = nuetral
        
        if weakest_planet:
            ships_to_send = weakest_planet.num_ships + 1
            if planet.num_ships - ships_to_send > 20:
                targeted_planets.add(weakest_planet.ID)
                return issue_order(state, planet.ID, weakest_planet.ID, ships_to_send)
    return False

def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    
def spread_to_strongest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the strongest neutral planet.
    strongest_planet = max(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not strongest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, strongest_planet.ID, strongest_planet.num_ships / 2)
