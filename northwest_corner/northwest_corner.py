# northwest_corner.py

def northwest_corner_method(costs, supply, demand):
    supply = supply.copy()
    demand = demand.copy()
    i, j = 0, 0
    allocations = []
    while i < len(supply) and j < len(demand):
        alloc = min(supply[i], demand[j])
        allocations.append(((i, j), alloc))
        supply[i] -= alloc
        demand[j] -= alloc
        if supply[i] == 0 and i < len(supply)-1:
            i += 1
        elif demand[j] == 0 and j < len(demand)-1:
            j += 1
        else:
            i += 1
            j += 1
    return allocations
