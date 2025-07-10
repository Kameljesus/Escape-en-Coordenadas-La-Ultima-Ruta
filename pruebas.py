alto = int(input("Elija el alto de su laberinto: "))
ancho = int(input("Elija el ancho de su laberinto: "))
print("")

mapa = [["_" for columna in range(ancho)] for fila in range(alto)]


# Función de Imprimir Tablero:
def mostrar_tablero(mapa):
    for fila in mapa:
        print(" ".join(fila))
    print("")

mostrar_tablero(mapa)


def colocar_entrada():
    while True:
        print("Selecciona la posicion de tu entrada (en coordenadas):")

        x1 = int(input("Fila: "))
        y1 = int(input("Columna: "))
        print("")


        if 0 <= x1 < alto and 0 <= y1 < ancho:
            mapa[x1][y1] = "E"
            mostrar_tablero(mapa)
            return x1, y1

        else:
            print("Coordenada Invalida: Lugar fuera del mapa")
            print("Por favor, seleccion un sitio en el mapa")

entrada = colocar_entrada()


def colocar_salida():
    while True:
        print("Selecciona la posicion de tu salida (en coordenadas):")

        x2 = int(input("Fila: "))
        y2 = int(input("Columna: "))
        print("")

        if (x2, y2) == entrada:
            print("La salida no puede estar en la misma posición que la entrada.")
            continue
        
        if 0 <= x2 < alto and 0 <= y2 < ancho:
            mapa[x2][y2] = "S"
            mostrar_tablero(mapa)
            return x2, y2

        else:
            print("Coordenada Invalida: Lugar fuera del mapa")
            print("Por favor, seleccion un sitio en el mapa") 

salida = colocar_salida()


def colocacion_de_obstaculos(entrada, salida):
    print("Seleccione la posicion del obstaculo (en coordenandas):")

    x4 = int(input("Fila: "))
    y4 = int(input("Columna: "))
    print("")

    if 0 <= x4 < alto and 0 <= y4 < ancho and (x4, y4) != entrada and (x4, y4) != salida:
        mapa[x4][y4] = "#"
        mostrar_tablero(mapa)
    
    else:
        print("No se puede colocar obsculos en la entrada, salida o fuera del mapa")

def while_de_obstaculos(entrada, salida):
    while True:
        pregunta_obstaculos = input("Desea poner uno o mas obstaculos? (S/N):").lower()

        if pregunta_obstaculos == "s":
            colocacion_de_obstaculos(entrada, salida)

        else:
            print("")
            break

while_de_obstaculos(entrada, salida)


import heapq

def distancia_manhattan_heuristica(primera_x, segunda_x, primera_y, segunda_y):
    return abs(primera_x - segunda_x) + abs(primera_y - segunda_y)

def a_estrella(entrada, salida):
    x1, y1 = entrada
    x2, y2 = salida

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
    
    # Formula general de A*: f = g + h
    # "g" es igual a el costo (en este caso, distancia) que nos llevó moverse desde el principio hasta ese punto.
    # "h" (heuristica) es el costo de la casilla actual hasta la meta.
    # "f" es la suma de 'g' y 'h'

    # Creamos una lista vacía llamada cola, que será usada como heap/cola de prioridad.
    cola = []

    # Calculamos la heurística (h) desde la entrada hasta la salida.
    heuristica = distancia_manhattan_heuristica(x1, x2, y1, y2)


    heapq.heappush(cola, (heuristica, 0, (x1, y1), [(x1, y1)]))
    # Hey, agrega esta celda inicial (x1, y1) a la cola de prioridad, con:
    
        # "f = heurística (porque g = 0 al principio),"

        # "g = 0 (no he caminado nada aún),"

        # "su posición actual (x1, y1),"

        # "y su camino recorrido hasta ahora: solo ella misma [(x1, y1)]."

    # Además, ordena automáticamente la cola de forma que la celda con menor f quede siempre al frente.”

    visitados = set()
    # set(): lista que no se puede repetir elementos.

    while cola:
        f, g, (x, y), camino = heapq.heappop(cola)
        # Saca el nodo con menor 'f' (puntaje) de la cola

        # Si llegamos a la salida, terminamos
        if (x, y) == salida:
            for px, py in camino:
                if mapa[px][py] == "_":
                    mapa[px][py] = "x"
            return camino  # Camino encontrado

        # Marcamos como visitado
        visitados.add((x, y))

        # Revisamos vecinos
        for dx, dy in movimientos:
            nueva_x, nueva_y = x + dx, y + dy
            if 0 <= nueva_x < alto and 0 <= nueva_y < ancho:
                if (nueva_x, nueva_y) not in visitados and mapa[nueva_x][nueva_y] != "#":
                    nuevo_g = g + 1  # Caminamos 1 paso más
                    h = distancia_manhattan_heuristica(nueva_x, x2, nueva_y, y2)
                    nuevo_f = nuevo_g + h
                    heapq.heappush(cola, (nuevo_f, nuevo_g, (nueva_x, nueva_y), camino + [(nueva_x, nueva_y)]))

    return None  # No se encontró camino


# Movimiento de jugador manual:
def juego_manual(entrada, salida):
# Movimientos:
    movimientos = {
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1)
    }
    
    x1, y1 = entrada
    x2, y2 = salida
    
    # Esto es para que la entrada no se mueva de su lugar a la hora de moverse.
    x3, y3 = entrada

    camino_manual = [(x1, y1)]
    # Lista de tooodo el recorrido.

    while True:
        # Condición de salida (si llega a la 'S'):
        if (x1, y1) == (x2, y2):
            print("")
            print("¡Has llegado a la salida!")
            print(f"Tu recorrido tomó: {len(camino_manual)}0 min.")
            break

        direccion = input("Mover (w/a/s/d): ").lower()

        if direccion not in movimientos:
            print("Dirección inválida. Usa w/a/s/d")
            continue

        dx, dy = movimientos[direccion]
        nueva_x1 = x1 + dx
        nueva_y1 = y1 + dy

        # Verifica que la nueva posición esté dentro del laberinto
        if 0 <= nueva_x1 < alto and 0 <= nueva_y1 < ancho and mapa[nueva_x1][nueva_y1] != "#":
            mapa[x1][y1] = "."
            
            # Poner la entrada otra vez:
            mapa[x3][y3] = "E"

            # Actualiza a la nueva posición
            x1, y1 = nueva_x1, nueva_y1
            mapa[x1][y1] = "O"

            camino_manual.append((x1, y1))  
            # Guardamos la nueva celda visitada

            # Muestra el laberinto actualizado
            print("")
            mostrar_tablero(mapa)

        else:
            print("")
            print("No se puede chocar con paredes ni salir de los límites")
            print("")


def eleccion_del_usuario(entrada, salida):
    while True:
        decision = input("Desea que el juego se resuelva manualmente? (S/N):").lower()

        if decision == "s":
            juego_manual(entrada, salida)
            break

        else:
            camino = a_estrella(entrada, salida)

            if camino:
                mostrar_tablero(mapa)
                print(f"Te tomó {len(camino)}0 min. llegar a la salida.")
            else:
                print("No se encontró un camino.")
            break

eleccion_del_usuario(entrada, salida) 