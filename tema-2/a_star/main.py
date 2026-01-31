from cities_data import CITIES_COORDINATES, CONNECTIONS
from a_star import a_star_search # type: ignore -> No afecta a la ejecución del programa

def main():
    print("=== Cálculo de Ruta Óptima entre Capitales de Provincia (A*) ===")
    print(f"Total de ciudades disponibles: {len(CITIES_COORDINATES)}")
    print("Ejemplos: Madrid, Barcelona, Sevilla, Valencia, Bilbao, A Coruña...")
    
    print("\n")
    start = input("Introduce la ciudad de origen: ").strip()
    goal = input("Introduce la ciudad de destino: ").strip()
    
    start = " ".join(word.capitalize() for word in start.split())
    goal = " ".join(word.capitalize() for word in goal.split())

    
    if start not in CITIES_COORDINATES or goal not in CITIES_COORDINATES:
        print("Error: Una o ambas ciudades no están en la base de datos.")
        return

    print(f"\nCalculando ruta de {start} a {goal}...")
    
    path, distance = a_star_search(start, goal, CONNECTIONS, CITIES_COORDINATES)
    
    if path:
        print("\n¡Ruta encontrada!")
        print(" -> ".join(path))
        print(f"Distancia total estimada: {distance:.2f} km")
    else:
        print("\nNo se encontró una ruta posible entre estas ciudades con las conexiones actuales.")

if __name__ == "__main__":
    main()
