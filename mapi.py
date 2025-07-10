import pygame # Importa pygame (obviamente)
import sys 
import heapq
'''

Este módulo forma parte de la biblioteca estándar de Python, y se usa principalmente para controlar el sistema de ejecución del programa.
¿Qué cosas útiles tiene sys?

    sys.exit(): 💥 Termina completamente el programa. Sin sys.exit(), el programa puede quedar "colgado" en memoria después de cerrar la ventana de Pygame.

    sys.argv: 📦 Accede a argumentos pasados por consola.

    sys.path: 📂 Ve las rutas de búsqueda de módulos.

'''

pygame.init()

ancho_de_pantalla = 800
alto_de_pantalla = 800

ancho_de_tablero = 640
alto_de_tablero = 640


# Posición X donde empiezan los botones (justo a la derecha del tablero):
botones_x = ancho_de_tablero + 20

# Diccionario que guarda cada botón con su posición y tamaño:
botones = {
    "obstaculo": pygame.Rect(botones_x, 50, 120, 40),
    "entrada": pygame.Rect(botones_x, 110, 120, 40),
    "salida": pygame.Rect(botones_x, 170, 120, 40),
    "algoritmo": pygame.Rect(botones_x, 230, 120, 40),
    "manual":pygame.Rect(botones_x, 290, 120, 40),
    "reset":pygame.Rect(botones_x, 350, 120, 40)

    # botones_x: posición horizontal (eje X) donde empieza el botón, en píxeles desde la izquierda de la ventana.
    # 230: posición vertical (eje Y) donde empieza el botón, en píxeles desde arriba.
    # 120: ancho del botón, en píxeles.
    # 40: alto del botón, en píxeles.
}


#Solicitud de ancho y alto al usuario:
num_filas = int(input("Elija cuantas filas quiere en su laberinto: "))
num_columnas = int(input("Elija cuantas columnas quiere de su laberinto: "))


#Setup básico de pygame:
screen = pygame.display.set_mode((ancho_de_pantalla, alto_de_pantalla))
pygame.display.set_caption("Google Maps Veneco:")
clock = pygame.time.Clock() # Para definir los fps de mi juego.
running = True


# Configuración de celdas:
celda_libre = 0
celda_obstaculo = 1
celda_inicio = 2
celda_fin = 3
celda_ruta = 4
celda_jugador = 5

# Calculamos ambos posibles tamaños (ancho/columnas y alto/filas)
tam_celda_x_posible = ancho_de_tablero//num_columnas
tam_celda_y_posible = alto_de_tablero//num_filas

# Elegimos el mínimo para que la celda sea cuadrada sin pasarse del tablero
tam_celda = min(tam_celda_x_posible, tam_celda_y_posible)

# Definimos el ancho y alto de la celda igual al tamaño cuadrado
tam_celda_x = tam_celda
tam_celda_y = tam_celda


# Crear tablero:
mapa = [[celda_libre for columna in range(num_columnas)] for fila in range(num_filas)]

# Coordenadas de entrada y salida:
entrada_fila = None
entrada_columna = None
salida_fila = None
salida_columna = None
# 'None' indica que no han sido definidas por el usuario (después las definirá, obviamente).
# Tambien se le puede poner '-1' si solo influye en el pygame.

# Configuración de colores:
GRIS = (200, 200, 200) 
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (30, 80, 160)
COLOR_JUGADOR = (0, 200, 255)  # Un celeste fuerte

# Fuente para el texto de los botones (definida globalmente):
fuente = pygame.font.SysFont("Arial", 24)


# Función de Imprimir Tablero:
def mostrar_tablero():
    for fila_indice in range(num_filas):
        for columna_indice in range(num_columnas):

            # Crea un rectangulo y ponle sus medidas:
            x = columna_indice * tam_celda_x
            y = fila_indice * tam_celda_y
            rectangulo = pygame.Rect(x, y, tam_celda_x, tam_celda_y)
            relleno = pygame.Rect(x + 4, y + 4, tam_celda_x - 8, tam_celda_y - 8)


            # Muestrame el rectangulo:
            if mapa[fila_indice][columna_indice] == celda_libre:
                pygame.draw.rect(screen, GRIS, rectangulo, 8) 
            elif mapa[fila_indice][columna_indice] == celda_obstaculo:
                pygame.draw.rect(screen, NEGRO, relleno)
            elif mapa[fila_indice][columna_indice] == celda_inicio:
                pygame.draw.rect(screen, VERDE, relleno)
            elif mapa[fila_indice][columna_indice] == celda_fin:
                pygame.draw.rect(screen, ROJO, relleno)
            elif mapa[fila_indice][columna_indice] == celda_ruta:
                pygame.draw.rect(screen, AZUL, relleno)
            elif mapa[fila_indice][columna_indice] == celda_jugador:
                pygame.draw.rect(screen, COLOR_JUGADOR, relleno)


    # Mostrar cuando el boton esta "clickeado" o "activo":
    for nombre, rect in botones.items():

        if nombre == modo_actual:
            pygame.draw.rect(screen, NEGRO, rect)  # Fondo negro para activo
            texto = fuente.render(nombre.capitalize(), True, BLANCO)  # Texto blanco

        else:
            pygame.draw.rect(screen, BLANCO, rect)  # Fondo blanco para inactivo
            texto = fuente.render(nombre.capitalize(), True, NEGRO)  # Texto negro

        pygame.draw.rect(screen, NEGRO, rect, 2)  # Borde negro siempre
        texto_rect = texto.get_rect(center=rect.center)
        screen.blit(texto, texto_rect)
            

def juego_manual(entrada_fila, entrada_columna, salida_fila, salida_columna):
    jugador_fila = entrada_fila
    jugador_columna = entrada_columna
    
    # Contador de movimientos:
    minutos = 0

    # Marcar la posición inicial del jugador
    mapa[jugador_fila][jugador_columna] = celda_jugador

    jugador = True

    while jugador:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            # Significa: si el usuario presiona una tecla, entonces vamos a ver cuál fue (flechas o WASD) y mover al jugador:
            if event.type == pygame.KEYDOWN:
                nueva_fila = jugador_fila
                nueva_columna = jugador_columna


                # Movimientos y sus teclas:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                        nueva_fila -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        nueva_fila += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        nueva_columna -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        nueva_columna += 1
                

                # Validar movimiento:
                if (0 <= nueva_fila < num_filas and 0 <= nueva_columna < num_columnas and
                    mapa[nueva_fila][nueva_columna] != celda_obstaculo):

                    # Sumamos al contador:
                    minutos += 1
                    
                    # Marcar la celda anterior como ruta (excepto si es la entrada)
                    if (jugador_fila, jugador_columna) != (entrada_fila, entrada_columna):
                        mapa[jugador_fila][jugador_columna] = celda_ruta
                    
                    # Modificar coordenadas para el movimiento:
                    jugador_fila = nueva_fila
                    jugador_columna = nueva_columna

                    # ¿Llegó a la salida?
                    if jugador_fila == salida_fila and jugador_columna == salida_columna:

                        print("")
                        print("🎉 ¡Ganaste! Llegaste a la salida.")
                        print("")
                        print(f'Te tomó {minutos}0 min.')
                        
                        # Marcar la salida para ver toda la ruta bien:
                        mapa[salida_fila][salida_columna] = celda_fin
                        jugador = False

                    else:
                        # Marca la posicion nueva del jugador:
                        mapa[jugador_fila][jugador_columna] = celda_jugador
                    
                    # Marcar siempre la entrada por si volvió a esta:
                    mapa[entrada_fila][entrada_columna] = celda_inicio
                
                else:
                    print("")
                    print('No se puede pasar por los obstaculos ni salirse del mapa')


        # Actualizar pantalla
        screen.fill("gray")
        mostrar_tablero()
        pygame.display.flip()
        clock.tick(60)


def distancia_manhattan_heuristica(primera_x, segunda_x, primera_y, segunda_y):
    return abs(primera_x - segunda_x) + abs(primera_y - segunda_y)

def algoritmo(entrada_fila, entrada_columna, salida_fila, salida_columna):
    
    # Le damos las coordenadas al algoritmo:
    x1 = entrada_fila
    y1 = entrada_columna
    x2 = salida_fila
    y2 = salida_columna

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

        # Marcar la celda actual como visitada (para mostrar el progreso)
        if mapa[x][y] == celda_libre:
            mapa[x][y] = celda_ruta

        # Pausa para mostrar el progreso paso a paso
        pygame.time.wait(200)  # Pausa entre cada paso

        # Permitir interacción durante el algoritmo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Permitir modificar el mapa durante la ejecución
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                fila_click = y_mouse // tam_celda
                columna_click = x_mouse // tam_celda
                
                # Solo permitir agregar/quitar obstáculos
                if (0 <= fila_click < num_filas and 0 <= columna_click < num_columnas and
                    mapa[fila_click][columna_click] != celda_inicio and mapa[fila_click][columna_click] != celda_fin):
                    
                    if mapa[fila_click][columna_click] == celda_libre:
                        mapa[fila_click][columna_click] = celda_obstaculo
                    elif mapa[fila_click][columna_click] == celda_obstaculo:
                        mapa[fila_click][columna_click] = celda_libre

        # Actualizar pantalla para mostrar el progreso
        screen.fill("gray")
        mostrar_tablero()
        pygame.display.flip()
        clock.tick(60)

        # Si llegamos a la salida, terminamos
        if (x, y) == (x2, y2):
            for px, py in camino:
                if mapa[px][py] == celda_ruta:
                    mapa[px][py] = celda_jugador
            print("")
            print(f"🎯 Camino encontrado! Tiempo estimado: {len(camino)}0 min.")
            return camino  # Camino encontrado
        

        # Marcamos como visitado
        visitados.add((x, y))

        # Revisamos vecinos
        for dx, dy in movimientos:
            nueva_x, nueva_y = x + dx, y + dy
            if (0 <= nueva_x < num_filas and 0 <= nueva_y < num_columnas and
                    mapa[nueva_x][nueva_y] != celda_obstaculo) and (nueva_x, nueva_y) not in visitados:
                    # Esta condición también evita que las coordenadas (x, y) no se repitan, porque sino volverian al punto de entrada siempre. 
                    
                    # Caminamos 1 paso más:
                    nuevo_g = g + 1

                    # Calculamos la heuristica actual:
                    h = distancia_manhattan_heuristica(nueva_x, x2, nueva_y, y2)

                    # Hacemos el calculo de f:
                    nuevo_f = nuevo_g + h

                    # Lo agregamos a la cola de prioridad:
                    heapq.heappush(cola, (nuevo_f, nuevo_g, (nueva_x, nueva_y), camino + [(nueva_x, nueva_y)]))


    # No se encontró camino
    print("")
    print("No hay camino posible")
    return None  # No se encontró camino


# Modo (funcion actual) del click:
modo_actual = "obstaculo"  # Puede ser: "obstaculo", "entrada", "salida"

while running:

    # Obten todo los eventos que sucedan en cada frame
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False # Este es mi break


        # Significa: “si se presionó el botón del mouse (cualquier clic)”.
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()


            # Verificar si se clickeó algún botón
            boton_clickeado = False
            for nombre_boton, rect in botones.items():
                if rect.collidepoint(x_mouse, y_mouse):
                    boton_clickeado = True

                    # Detectar si hizo clic en reset
                    if nombre_boton == "reset":
                        # Limpiar todo el tablero
                        mapa = [[celda_libre for columna in range(num_columnas)] for fila in range(num_filas)]
                        # Resetear coordenadas de entrada y salida
                        entrada_fila = None
                        entrada_columna = None
                        salida_fila = None
                        salida_columna = None
                        print("")
                        print("🧹 Tablero limpiado completamente.")


                    # Detectar si hizo clic en algoritmo o juego_manual
                    elif nombre_boton == "algoritmo" or nombre_boton == "manual":
                        # Verificar que la entrada y salida estén definidas
                        if (entrada_fila is not None and entrada_columna is not None and
                            salida_fila is not None and salida_columna is not None):

                            if nombre_boton == "algoritmo":
                                 # Aquí se llamará la función de resolución automática:
                                resultado = algoritmo(entrada_fila, entrada_columna, salida_fila, salida_columna) 
                                
                                if resultado:
                                    # Mostrar resultado por 5 segundos
                                    inicio_tiempo = pygame.time.get_ticks()
                                    while pygame.time.get_ticks() - inicio_tiempo < 5000:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                        screen.fill("gray")
                                        mostrar_tablero()
                                        pygame.display.flip()
                                        clock.tick(60)


                            elif nombre_boton == "manual":
                                
                                # Aquí se llamará la función de juego manual
                                juego_manual(entrada_fila, entrada_columna, salida_fila, salida_columna)  

                        else:
                            print("")
                            print("⚠️ Primero debes definir la entrada y la salida.")
                        
                    else:
                        # Cambiar modo para otros botones
                        modo_actual = nombre_boton

                    break  


            # "Si no clickeaste en botón, entonces clickeaste en el tablero":
            if not boton_clickeado:
                fila = y_mouse // tam_celda
                columna = x_mouse // tam_celda
                

                # Esto permite que puedas poner y quitar con clicks los elementos de modo:
                if 0 <= fila < num_filas and 0 <= columna < num_columnas:
                    if modo_actual == "obstaculo":
                        if mapa[fila][columna] == celda_libre:
                            mapa[fila][columna] = celda_obstaculo
                        elif mapa[fila][columna] == celda_obstaculo:
                            mapa[fila][columna] = celda_libre

                    elif modo_actual == "entrada":
                        # Limpiar entrada previa
                        for f in range(num_filas):
                            for c in range(num_columnas):
                                if mapa[f][c] == celda_inicio:
                                    mapa[f][c] = celda_libre
                        mapa[fila][columna] = celda_inicio
                        # Definimos las coordenadas para cualquiera de las dos funciones:
                        entrada_fila = fila
                        entrada_columna = columna


                    elif modo_actual == "salida":
                        # Limpiar salida previa
                        for f in range(num_filas):
                            for c in range(num_columnas):
                                if mapa[f][c] == celda_fin:
                                    mapa[f][c] = celda_libre
                        mapa[fila][columna] = celda_fin
                        # Definimos las coordenadas para cualquiera de las dos funciones:
                        salida_fila = fila
                        salida_columna = columna

    
    screen.fill("gray") # Esto es el fondo de mi pantalla
    mostrar_tablero()


    pygame.display.flip() # Permite mostrar en pantalla lo que se actualiza. Pygame no dibuja en la ventana automáticamente. Primero dibuja en memoria, y cuando hacés display.flip(), muestra todo eso en la pantalla de golpe.
    clock.tick(60) # Esta es la velocidad que quiero a la que vaya mi programa.

pygame.quit()
sys.exit()