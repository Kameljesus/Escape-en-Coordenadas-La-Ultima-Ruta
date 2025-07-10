'''
🧪 Ejercicio 1: Crea un mapa vacío

📌 Objetivo: Escribir una función que reciba el alto y el ancho, y cree una matriz de "_".
Instrucciones:

    Pide al usuario el alto y ancho.

    Crea un mapa (lista de listas) de tamaño alto × ancho con "_".

    Muestra el mapa en consola.

✏️ Tu tarea: Escribe el código tú mismo.
'''

alto = int(input("Dame el alto de tu tablero: "))
ancho = int(input("Dame el ancho de tu tablero: "))

def crear_tablero(alto, ancho):
    tablero = [["_" for columnas in range(ancho)] for filas in range(alto)]
    for fila in tablero:
        print(" ".join(fila))

    print()
    return tablero

'''
🧪 Ejercicio 2: Coloca una entrada (E) y una salida (S)

📌 Objetivo: Permitir al usuario seleccionar dos posiciones válidas para entrada y salida, y reflejarlas en el mapa.
Instrucciones:

    Pide al usuario una coordenada para la entrada E.

    Pide otra distinta para la salida S.

    Asegúrate de que estén dentro del mapa y no se repitan.

    Actualiza el mapa y muéstralo.

✏️ Tu tarea: Agrega esto sobre tu código del ejercicio 1.
'''
def colocar_entrada_salida (tablero):
    # Para evitar "acoplamiento innecesario":
    alto = len(tablero)
    ancho = len(tablero[0])

    while True:
        entrada = (int(input("Dame la fila de tu entrada: ")), int(input("Dame la columna de tu entrada: ")))
        print()

        if 0 <= entrada[0] < alto and 0 <= entrada[1] < ancho:
           tablero[entrada[0]][entrada[1]] = 'E'
           for fila in tablero:
               print(" ".join(fila))
           print()
           break
        
        else: 
            print("Por favor, coloque un valor valido")


    while True:
        salida = (int(input("Dame la fila de tu salida: ")), int(input("Dame la columna de tu salida: ")))
        print("")

        if salida != entrada and 0 <= salida[0] < alto and 0 <= salida[1] < ancho:
            tablero[salida[0]][salida[1]] = 'S'
            for fila in tablero:
               print(" ".join(fila))
            print()
            return entrada, salida

        else:
            print("Por favor, coloque un número y que este dentro del tablero por favor")

tablero = crear_tablero(alto, ancho)
entrada, salida = colocar_entrada_salida(tablero)

'''
🧪 Ejercicio 3: Agrega obstáculos (#)

📌 Objetivo: Permitir al usuario colocar obstáculos dentro del mapa.
Instrucciones:

    Pregunta si desea agregar un obstáculo.

    Si responde que sí, pide fila y columna.

    Verifica que no esté en E ni en S.

    Permite repetir hasta que diga que no.

✏️ Tu tarea: Sigue construyendo sobre tu código anterior.
'''

def agregar_obstaculos(tablero, entrada, salida):
    obstaculos = []
    alto = len(tablero)
    ancho = len(tablero[0])

    while True:
        pregunta_obstaculos = input("Desea agregar obstaculos? (S/N): ").lower()
        print()

        if pregunta_obstaculos != 's':
            return obstaculos

        else:
            obs_agregado = (int(input("Dame la fila de tu obstaculo: ")), int(input("Dame la columna de tu obstaculo: ")))
            print()
            
            if obs_agregado != entrada and obs_agregado != salida and 0 <= obs_agregado[0] < alto and 0 <= obs_agregado[1] < ancho:
                obstaculos.append(obs_agregado)
                for x, y in obstaculos:
                    tablero[x][y] = '#'
                for fila in tablero:
                    print(" ".join(fila))
            
            else:
                print("Por favor, coloque un valor valido")

agregar_obstaculos(tablero, entrada, salida)
        
'''
🧪 Ejercicio 4: Crea tu propia función de A* básica

📌 Objetivo: Implementar una función a_estrella(entrada, salida, mapa) que busque el camino usando heurística Manhattan y lo pinte con "x".
Instrucciones:

    Usa una lista como cola de prioridad (puedes ordenar por f = g + h).

    Lleva un conjunto de visitados.

    Ve guardando el camino recorrido.

    Marca "x" en el mapa si forma parte del camino.

✏️ Tu tarea: Construye la base del algoritmo. Puedo ayudarte paso a paso si me dices “muéstrame el paso 1 del A*”.
'''

import heapq
def distancia_manhattan(x1, x2, y1, y2):
    return abs(x1 - x2) + abs (y1 - y2)

def a_estrella(tablero, entrada, salida, obstaculos):
    alto = len(tablero)
    ancho = len(tablero[0])
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    cola = []

    heuristica = distancia_manhattan(entrada[0], salida[0], entrada[1], salida[1])

    heapq.heappush(cola(heuristica, 0, (entrada), [(entrada)]))

    visitados = set() 

    while cola:
        f, g, (x, y), camino = heapq.heappop(cola)

        if (x, y) == salida:
            for (x, y) in camino:
                tablero[x][y] = 'X'
        
        visitados.add(x, y)
        
        for dx, dy in movimientos:
            nueva_x = x + dx
            nueva_y = y + dy
            nueva_coordenada = (nueva_x, nueva_y)

            if 0 <= nueva_coordenada[0] < alto and 0 <= nueva_coordenada[1] < ancho and nueva_coordenada not in visitados:
                f = distancia_manhattan(nueva_coordenada[0], salida[0], nueva_coordenada[1], salida[1])


        


'''
🧪 Ejercicio 5: Modo paso a paso

📌 Objetivo: Que el usuario vea cómo se va expandiendo el camino paso a paso presionando Enter.
Instrucciones:

    Detén la ejecución en cada paso hasta que el usuario presione Enter.

    Actualiza el mapa visualmente con el nodo actual ("x").

    Opción para salir con 'q'.

✏️ Tu tarea: Modifica el A* para que funcione paso a paso.
'''