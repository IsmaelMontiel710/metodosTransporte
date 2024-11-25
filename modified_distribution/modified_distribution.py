# modified_distribution/modified_distribution.py

def modified_distribution_method(costs, supply, demand):
    """
    Implementación del Método de Distribución Modificada (DIMO) para el Problema de Transporte.
    
    Este método es una variante del Método de Costo Mínimo que incluye modificaciones para mejorar la eficiencia.
    
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
    
    # Crear una lista de todas las celdas con sus costos
    cells = []
    for i in range(num_supply):
        for j in range(num_demand):
            cells.append((costs[i][j], i, j))
    
    # Ordenar las celdas por costo ascendente
    cells.sort()
    
    for cost, i, j in cells:
        if supply_remaining[i] == 0 or demand_remaining[j] == 0:
            continue  # Pasar si la oferta o demanda es 0
        
        # Asignar la cantidad mínima entre oferta y demanda
        allocation = min(supply_remaining[i], demand_remaining[j])
        allocations.append(((i, j), allocation))
        
        # Actualizar las ofertas y demandas restantes
        supply_remaining[i] -= allocation
        demand_remaining[j] -= allocation
    
    return allocations
