'''
S es entrada
G es salida
1 es obstaculos (X)
0 es camino libre (.)
'''

def generar_mapa(filas, columnas):   
    mapa = [['0' for columna in range(columnas)] for fila in range(filas)] 
    return mapa

def agregar_inicio_fin(mapa, inicio, fin):
    mapa[inicio[0]][inicio[1]] = 'S'
    mapa[fin[0]][fin[1]] = 'G'

def agregar_obstaculos(mapa, obstaculos):
    for (x3, y3) in obstaculos:
        mapa[x3][y3] = '1'

def mostrar_mapa(mapa):
    for fila in mapa:
        linea = []
        for columna in fila:
            if columna == '0':
                linea.append('.')
            elif columna == '1':
                linea.append('X')
            else:
                linea.append(columna)
        print(" ".join(linea))
            

def main():
    # TODO: pedir filas, columnas, entrada, salida, obstaculos

    # Pedir filas y columnas:
    while True:
        try:
            filas = int(input("Dame la cantidad de filas que quieres para el tablero: "))
            columnas = int(input("Dame la cantidad de columnas que quieres para el tablero: "))
            break
                
        except ValueError:
                print('Por favor, coloque un valor válido')

    print("")
    mapa = generar_mapa(filas, columnas)
    mostrar_mapa(mapa)
    print("")

    # Pedir entrada:
    while True:
        inicio = (int(input('Dame la columna de tu entrada: ')), int(input('Dame la fila de tu entrada: ')))

        if 0 <= inicio[0] < filas and 0 <= inicio[1] < columnas:
            print("")
            break
        
        else:
            print('Por favor, coloque un valor válido')

    # Pedir salida:    
    while True:
        fin = (int(input('Dame la columna de tu salida: ')), int(input('Dame la fila de tu salida: ')))

        if fin != inicio and 0 <= fin[0] < filas and 0 <= fin[1] < columnas:
            print("")
            break
        
        else:
            print('Por favor, coloque un valor válido')
            print("La salida y la entrada no pueden estar en el mismo lugar")
    
    print("")
    agregar_inicio_fin(mapa, inicio, fin)
    mostrar_mapa(mapa)
    print("")

    # Colocar Obstaculos:
    obstaculos = []
    while True:
        pregunta = input('Desea agregar obstaculos? (S/N): ').lower()

        if pregunta != 's':
            break
            
        else:
            print("")
            fila_obstaculo = int(input("Dame la fila de tu obstáculo: "))
            columna_obstaculo = int(input("Dame la columna de tu obstáculo: "))

            if 0 <= fila_obstaculo < filas and 0 <= columna_obstaculo < columnas and (fila_obstaculo, columna_obstaculo) != inicio and (fila_obstaculo, columna_obstaculo) != fin:
                obstaculos.append((fila_obstaculo, columna_obstaculo))

    print("")
    agregar_obstaculos(mapa, obstaculos)
    mostrar_mapa(mapa)
    print("")


main()