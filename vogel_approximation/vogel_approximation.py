# vogel_approximation.py

import copy

def vogel_approximation_method(costs, supply, demand):
    supply = supply.copy()
    demand = demand.copy()
    costs = copy.deepcopy(costs)
    allocations = []
    rows = len(supply)
    cols = len(demand)
    row_covered = [False] * rows
    col_covered = [False] * cols

    while True:
        # Calcular penalizaciones para filas
        row_penalties = []
        for i in range(rows):
            if not row_covered[i]:
                sorted_costs = sorted([costs[i][j] for j in range(cols) if not col_covered[j]])
                if len(sorted_costs) >= 2:
                    penalty = sorted_costs[1] - sorted_costs[0]
                elif len(sorted_costs) == 1:
                    penalty = sorted_costs[0]
                else:
                    penalty = 0
                row_penalties.append((penalty, i))
        # Calcular penalizaciones para columnas
        col_penalties = []
        for j in range(cols):
            if not col_covered[j]:
                sorted_costs = sorted([costs[i][j] for i in range(rows) if not row_covered[i]])
                if len(sorted_costs) >= 2:
                    penalty = sorted_costs[1] - sorted_costs[0]
                elif len(sorted_costs) == 1:
                    penalty = sorted_costs[0]
                else:
                    penalty = 0
                col_penalties.append((penalty, j))
        if not row_penalties and not col_penalties:
            break
        # Encontrar la máxima penalización
        if row_penalties and col_penalties:
            max_row = max(row_penalties, key=lambda x: x[0])
            max_col = max(col_penalties, key=lambda x: x[0])
            if max_row[0] >= max_col[0]:
                penalty, row = max_row
                # Encontrar la columna con el costo mínimo en esta fila
                min_cost = float('inf')
                min_col = -1
                for j in range(cols):
                    if not col_covered[j] and costs[row][j] < min_cost:
                        min_cost = costs[row][j]
                        min_col = j
                selected = (row, min_col)
            else:
                penalty, col = max_col
                # Encontrar la fila con el costo mínimo en esta columna
                min_cost = float('inf')
                min_row = -1
                for i in range(rows):
                    if not row_covered[i] and costs[i][col] < min_cost:
                        min_cost = costs[i][col]
                        min_row = i
                selected = (min_row, col)
        elif row_penalties:
            penalty, row = max(row_penalties, key=lambda x: x[0])
            min_cost = float('inf')
            min_col = -1
            for j in range(cols):
                if not col_covered[j] and costs[row][j] < min_cost:
                    min_cost = costs[row][j]
                    min_col = j
            selected = (row, min_col)
        else:
            penalty, col = max(col_penalties, key=lambda x: x[0])
            min_cost = float('inf')
            min_row = -1
            for i in range(rows):
                if not row_covered[i] and costs[i][col] < min_cost:
                    min_cost = costs[i][col]
                    min_row = i
            selected = (min_row, col)
        i, j = selected
        alloc = min(supply[i], demand[j])
        allocations.append(((i, j), alloc))
        supply[i] -= alloc
        demand[j] -= alloc
        if supply[i] == 0:
            row_covered[i] = True
        if demand[j] == 0:
            col_covered[j] = True
    return allocations
