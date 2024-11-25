# sequential_steps/sequential_steps.py

def sequential_steps_method(costs, supply, demand):
    """
    Implementación del Método de Pasos Secuenciales (Banquillo) para el Problema de Transporte.
    
    Parámetros:
        costs (list of list of float): Matriz de costos.
        supply (list of float): Oferta de cada proveedor.
        demand (list of float): Demanda de cada consumidor.
    
    Retorna:
        allocations (list of tuple): Lista de asignaciones en formato ((proveedor, consumidor), cantidad).
    """
    allocations = []
    num_supply = len(supply)
    num_demand = len(demand)
    
    # Crear copias para no modificar las originales
    supply_remaining = supply.copy()
    demand_remaining = demand.copy()
    
    # Iterar sobre cada celda de la matriz en orden secuencial (fila por fila)
    for i in range(num_supply):
        for j in range(num_demand):
            if supply_remaining[i] == 0:
                break  # Pasar al siguiente proveedor si la oferta es 0
            if demand_remaining[j] == 0:
                continue  # Pasar al siguiente consumidor si la demanda es 0
            
            # Asignar la cantidad mínima entre oferta y demanda
            allocation = min(supply_remaining[i], demand_remaining[j])
            allocations.append(((i, j), allocation))
            
            # Actualizar las ofertas y demandas restantes
            supply_remaining[i] -= allocation
            demand_remaining[j] -= allocation
    
    return allocations
