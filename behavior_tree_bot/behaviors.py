import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
#my actions
def heuristic(state, myplanet): #returns the best planet to populate and the heuristic value from one of my planets
    dweight = 2
    pweight = 1
    gweight = 10

    bestpc = 100000
    bestp = myplanet

    for nplanet in state.neutral_planets():
        dist = dweight * state.distance(myplanet.ID, nplanet.ID)
        pop = pweight * nplanet.num_ships
        grow = gweight * nplanet.growth_rate
        total = dist + pop - grow
        if(total < bestpc):
            bestp = nplanet
            bestpc = total
    return bestp, bestpc

def SendToBestNeutralPlanet(state):
    # Use a generator to find the best neutral planet and the corresponding myplanet
    result = min(
        ((myplanet, *heuristic(state, myplanet)) for myplanet in state.my_planets()), 
        key=lambda x: x[2],  # Compare based on the heuristic value (bestpc, which is the third element in the tuple)
        default=(None, None, float('inf'))  # Handle cases where there are no planets
    )
    myplanet, best_planet, bestpc = result  # Unpack the result
    
    if best_planet:
        # Ensure the source planet can send enough ships
        if (state.distance(myplanet.ID, best_planet.ID) + best_planet.num_ships <= myplanet.num_ships and not any(fleet.destination_planet == best_planet.ID for fleet in state.my_fleets())):
            return issue_order(state, myplanet.ID, best_planet.ID, best_planet.num_ships + 1)
    return False

def StealPlanet(state):
    for efleet in state.enemy_fleets():
        if(state.planets[efleet.destination_planet] in state.neutral_planets() or state.my_planets()):
            for mplanet in state.my_planets():
                total = efleet.num_ships - state.planets[efleet.destination_planet].num_ships + (state.planets[efleet.destination_planet].growth_rate * (state.distance(mplanet.ID, efleet.destination_planet) - efleet.turns_remaining)) + 5 #how many ships there will be by the time our fleet arrives + 5
                isfleet = any(fleet.destination_planet == efleet.destination_planet for fleet in state.my_fleets()) #is there already a fleet going there
                if(efleet.turns_remaining < state.distance(mplanet.ID, efleet.destination_planet) and total < mplanet.num_ships) and total > 0 and not isfleet:
                    return issue_order(state, mplanet.ID, efleet.destination_planet, total)
    return False

            
def Reinforce(state):
    for efleet in state.enemy_fleets():
        if(state.planets[efleet.destination_planet] in state.my_planets()):
            for mplanet in state.my_planets():
                total = efleet.num_ships - (state.planets[efleet.destination_planet].num_ships + state.planets[efleet.destination_planet].growth_rate * efleet.turns_remaining) + 5 #how many ships there will be by the time our fleet arrives + 5
                isfleet = any(fleet.destination_planet == efleet.destination_planet for fleet in state.my_fleets()) #is there already a fleet going there
                if(efleet.turns_remaining > state.distance(mplanet.ID, efleet.destination_planet) and total < mplanet.num_ships) and total > 0 and not isfleet:
                    return issue_order(state, mplanet.ID, efleet.destination_planet, total)
    return False



def attack_value(state, myplanet, eplanet):
    return myplanet.num_ships - (eplanet.num_ships + eplanet.growth_rate * state.distance(myplanet.ID, eplanet.ID))

#premades
def attack_weakest_enemy_planet(state):
    myp = None
    ep = None
    bestvalue = 0
    for myplanet in state.my_planets():
        for eplanet in state.enemy_planets():
            if(attack_value(state, myplanet, eplanet) > bestvalue):
                myp = myplanet
                ep = eplanet
                bestvalue = attack_value(state, myplanet, eplanet)
    if(myp == None or ep == None):
        return False
    total = ep.num_ships + (ep.growth_rate * state.distance(myp.ID, ep.ID)) + 5
    if(myp.num_ships > total and total > 0):
        return issue_order(state, myp.ID, ep.ID, total)
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
