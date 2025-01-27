#premades
def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state): #not actually the right name
    for myplanet in state.my_planets():
        for eplanet in state.enemy_planets():
            if(eplanet.num_ships < myplanet.num_ships/2):
                return True
    return False

#my checks
def CloseOccupation(state):
    if(not state.my_planets()):
        return False
    divider = 2 #change if you want to send ships even though you don't have that many
    for myplanet in state.my_planets():
        for nplanet in state.neutral_planets():
            if(state.distance(myplanet.ID, nplanet.ID) < 5 and myplanet.num_ships/divider > nplanet.num_ships):
                return True
    return False


def IsStealable(state):
    for efleet in state.enemy_fleets():
        if (state.planets[efleet.destination_planet] in state.neutral_planets() or state.my_planets()):
            return True
    return False

def IsDefendable(state):
    for efleet in state.enemy_fleets():
        if (state.planets[efleet.destination_planet] in state.my_planets()):
            return True
    return False