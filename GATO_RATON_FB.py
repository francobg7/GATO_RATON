import random
import time

# Crear un tablero de juego con dimensiones 5x5
filas = 5
columnas = 5

# Variables globales para las posiciones del gato y la rata
filas_gato, columna_gato, filas_rata, columna_rata = None, None, None, None

# Representación del gato y la rata en el tablero
gato = "G"
rata = "R"

# Movimientos posibles: izquierda, derecha, abajo, arriba
movimientos = [(0, -1), (0, 1), (1, 0), (-1, 0)]

# Función para calcular la distancia de Manhattan entre dos posiciones
def distancia(pos1: tuple, pos2: tuple):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

# Función para imprimir el estado actual del tablero
def imprimir_tablero(turno_actual, jugador_actual):
    print(f"Turno: {turno_actual}, Jugador: {jugador_actual}")
    tablero = [["."] * columnas for _ in range(filas)]  # Crear un tablero vacío
    tablero[filas_gato][columna_gato] = gato  # Colocar el gato en el tablero
    tablero[filas_rata][columna_rata] = rata  # Colocar la rata en el tablero

    for fila in tablero:  # Imprimir cada fila del tablero
        print(" ".join(fila))
    print()

# Función para colocar el gato y la rata en posiciones aleatorias
def colocar_gato_y_raton():
    global filas_gato, columna_gato, filas_rata, columna_rata
    while True:
        columna_rata = random.randint(0, columnas - 1)
        filas_rata = random.randint(0, filas - 1)
        columna_gato = random.randint(0, columnas - 1)
        filas_gato = random.randint(0, filas - 1)
        if (columna_gato != columna_rata or filas_gato != filas_rata):  # Asegurar que no están en la misma posición
            break

# Función para mover al gato o a la rata a una nueva posición
def mover_posicion(nueva_posicion: tuple, player: str):
    global filas_gato, columna_gato, filas_rata, columna_rata
    if player == "gato":
        filas_gato, columna_gato = nueva_posicion  # Actualizar la posición del gato
    elif player == "rata":
        filas_rata, columna_rata = nueva_posicion  # Actualizar la posición de la rata

# Función Minimax para determinar el mejor movimiento
def Minimax(posicion_actual, objetivo, depth, maximizando, prev_pos=None):
    if depth == 0 or posicion_actual == objetivo:  # Condición de parada
        return distancia(posicion_actual, objetivo), None

    if maximizando:  # Si estamos maximizando (jugando como rata)
        max_eval = float('-inf')
        mejor_movimiento = None
        for mov in movimientos:
            nueva_posicion = (posicion_actual[0] + mov[0], posicion_actual[1] + mov[1])
            if (0 <= nueva_posicion[0] < filas and 0 <= nueva_posicion[1] < columnas and nueva_posicion != prev_pos):
                eval, _ = Minimax(nueva_posicion, objetivo, depth - 1, False, posicion_actual)
                if eval > max_eval:
                    max_eval = eval
                    mejor_movimiento = nueva_posicion
        return max_eval, mejor_movimiento
    else:  # Si estamos minimizando (jugando como gato)
        min_eval = float('inf')
        mejor_movimiento = None
        for mov in movimientos:
            nueva_posicion = (posicion_actual[0] + mov[0], posicion_actual[1] + mov[1])
            if (0 <= nueva_posicion[0] < filas and 0 <= nueva_posicion[1] < columnas and nueva_posicion != prev_pos):
                eval, _ = Minimax(nueva_posicion, objetivo, depth - 1, True, posicion_actual)
                if eval < min_eval:
                    min_eval = eval
                    mejor_movimiento = nueva_posicion
        return min_eval, mejor_movimiento

# Función para mover al gato utilizando el algoritmo Minimax
def mover_gato_inteligente():
    if distancia((filas_gato, columna_gato), (filas_rata, columna_rata)) == 1:
        mover_posicion((filas_rata, columna_rata), "gato")  # Mover directamente al ratón si está a un movimiento
    else:
        _, mejor_movimiento = Minimax((filas_gato, columna_gato), (filas_rata, columna_rata), 3, False)
        if mejor_movimiento:
            mover_posicion(mejor_movimiento, "gato")

# Función para mover a la rata utilizando el algoritmo Minimax
def mover_raton_inteligente():
    _, mejor_movimiento = Minimax((filas_rata, columna_rata), (filas_gato, columna_gato), 3, True)
    if mejor_movimiento:
        mover_posicion(mejor_movimiento, "rata")

# Función principal del juego que alterna los movimientos entre el gato y la rata
def juego():
    global filas_gato, columna_gato, filas_rata, columna_rata
    turno = "rata"  # El ratón comienza primero
    turnos = 0
    max_turnos = 15  # Número máximo de turnos antes de que el ratón escape
    while turnos < max_turnos:
        if turno == "gato":
            mover_gato_inteligente()
            imprimir_tablero(turnos + 1, "Gato")
            if (filas_gato, columna_gato) == (filas_rata, columna_rata):  # El gato atrapa al ratón
                print("El gato atrapó al ratón. ¡Fin del juego!")
                break
            turno = "rata"
        else:
            mover_raton_inteligente()
            imprimir_tablero(turnos + 1, "Ratón")
            if (filas_gato, columna_gato) == (filas_rata, columna_rata):  # El ratón es atrapado
                print("El ratón fue atrapado. ¡Fin del juego!")
                break
            turno = "gato"
        turnos += 1
        time.sleep(1)  # Añadir un retraso de 1 segundo entre los movimientos
    else:
        print("Terminaron los turnos. ¡El ratón escapó feliz!")

# Inicializar el juego colocando al gato y a la rata en el tablero
colocar_gato_y_raton()
imprimir_tablero(0, "Inicio")
juego()