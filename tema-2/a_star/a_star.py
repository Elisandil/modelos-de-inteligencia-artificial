import math
import heapq

class Node:
    
    def __init__(self, name, parent=None, g=0.0, h=0.0):
        self.name = name
        self.parent = parent
        self.g = g  
        self.h = h  
        self.f = g + h  

    def __lt__(self, other):
        return self.f < other.f

def haversine_distance(coord1, coord2):
    """
    Calcula la distancia del círculo máximo entre dos puntos 
    en una esfera dado su latitud y longitud.
    """
    R = 6371 
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2)**2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def get_neighbors(city_name, graph):
    return graph.get(city_name, {}).items()

def reconstruct_path(node):
    path = []
    current = node
    while current:
        path.append(current.name)
        current = current.parent
    return path[::-1]

def a_star_search(start_city, goal_city, graph, coordinates):
    """
    Algoritmo A* para encontrar el camino más corto.
    """
    open_list = []
    closed_set = set()

    start_h = haversine_distance(coordinates[start_city], coordinates[goal_city])
    start_node = Node(start_city, None, 0, start_h)

    heapq.heappush(open_list, start_node)

    g_costs = {start_city: 0}
    
    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.name in closed_set:
            continue
        if current_node.name == goal_city:
            return reconstruct_path(current_node), current_node.g
        
        closed_set.add(current_node.name)
        
        for neighbor_name, distance in get_neighbors(current_node.name, graph):
            
            if neighbor_name in closed_set:
                continue
                
            tentative_g = current_node.g + distance
            
            if neighbor_name not in g_costs or tentative_g < g_costs[neighbor_name]:
                g_costs[neighbor_name] = tentative_g
                h = haversine_distance(coordinates[neighbor_name], coordinates[goal_city])
                neighbor_node = Node(neighbor_name, current_node, tentative_g, h)
                heapq.heappush(open_list, neighbor_node)
                
    return None, 0 
