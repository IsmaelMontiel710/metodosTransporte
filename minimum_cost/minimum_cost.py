# minimum_cost.py

def minimum_cost_method(costs, supply, demand):
    supply = supply.copy()
    demand = demand.copy()
    allocations = []
    rows = len(supply)
    cols = len(demand)
    cost_list = []
    for i in range(rows):
        for j in range(cols):
            cost_list.append((costs[i][j], i, j))
    cost_list.sort()
    for cost, i, j in cost_list:
        if supply[i] > 0 and demand[j] > 0:
            alloc = min(supply[i], demand[j])
            allocations.append(((i, j), alloc))
            supply[i] -= alloc
            demand[j] -= alloc
    return allocations
