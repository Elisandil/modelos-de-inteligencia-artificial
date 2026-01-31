import math

# Coordenadas de capitales de provincia y ciudades autónomas de España
# (Latitud, Longitud)
CITIES_COORDINATES = {
    "A Coruña": (43.3623, -8.4115),
    "Albacete": (38.9943, -1.8585),
    "Alicante": (38.3452, -0.4810),
    "Almería": (36.8340, -2.4637),
    "Ávila": (40.6565, -4.7002),
    "Badajoz": (38.8794, -6.9706),
    "Barcelona": (41.3851, 2.1734),
    "Bilbao": (43.2630, -2.9350),
    "Burgos": (42.3439, -3.6969),
    "Cáceres": (39.4757, -6.3723),
    "Cádiz": (36.5271, -6.2886),
    "Castellón": (39.9864, -0.0513),
    "Ceuta": (35.8894, -5.3213),
    "Ciudad Real": (38.9848, -3.9274),
    "Córdoba": (37.8882, -4.7794),
    "Cuenca": (40.0704, -2.1374),
    "Girona": (41.9794, 2.8214),
    "Granada": (37.1773, -3.5986),
    "Guadalajara": (40.6328, -3.1632),
    "Huelva": (37.2614, -6.9447),
    "Huesca": (42.1361, -0.4087),
    "Jaén": (37.7796, -3.7849),
    "León": (42.5987, -5.5671),
    "Lleida": (41.6176, 0.6200),
    "Logroño": (42.4623, -2.4449),
    "Lugo": (43.0121, -7.5558),
    "Madrid": (40.4168, -3.7038),
    "Málaga": (36.7213, -4.4214),
    "Melilla": (35.2923, -2.9381),
    "Murcia": (37.9922, -1.1307),
    "Ourense": (42.3358, -7.8639),
    "Oviedo": (43.3619, -5.8494),
    "Palencia": (42.0095, -4.5241),
    "Palma": (39.5696, 2.6502),
    "Pamplona": (42.8125, -1.6458),
    "Pontevedra": (42.4299, -8.6446),
    "Salamanca": (40.9701, -5.6635),
    "San Sebastián": (43.3183, -1.9812),
    "Santa Cruz de Tenerife": (28.4636, -16.2518),
    "Santander": (43.4623, -3.8099),
    "Segovia": (40.9429, -4.1088),
    "Sevilla": (37.3891, -5.9845),
    "Soria": (41.7640, -2.4688),
    "Tarragona": (41.1189, 1.2445),
    "Teruel": (40.3456, -1.1065),
    "Toledo": (39.8628, -4.0273),
    "Valencia": (39.4699, -0.3763),
    "Valladolid": (41.6523, -4.7245),
    "Vitoria": (42.8467, -2.6716),
    "Zamora": (41.5063, -5.7446),
    "Zaragoza": (41.6488, -0.8891)
}

def haversine_distance(coord1, coord2):
    """Calcula la distancia en km entre dos coordenadas."""
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

def generate_graph(cities_coords, k=4):
    """
    Genera un grafo conectando cada ciudad con sus k vecinos más cercanos.
    Esto simula una red de carreteras.
    """
    graph = {}
    
    for city, coord in cities_coords.items():
        distances = []
        for other_city, other_coord in cities_coords.items():
            if city == other_city:
                continue
            dist = haversine_distance(coord, other_coord)
            distances.append((other_city, dist))

        distances.sort(key=lambda x: x[1])
        nearest_neighbors = distances[:k]
        
        graph[city] = {neighbor: dist for neighbor, dist in nearest_neighbors}
        
    return graph

# Generar el grafo dinámicamente
CONNECTIONS = generate_graph(CITIES_COORDINATES, k=5)
