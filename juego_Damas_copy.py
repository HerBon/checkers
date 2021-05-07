from copy import deepcopy
import time
import math

'''asigna un color  a estas varibles '''
ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"


class Node:
    def __init__(self, tablero, move=None, padre=None, valor=None):
        self.tablero = tablero
        self.valor = valor
        self.move = move 
        self.padre = padre # padre

    def generar_hijos(self, minimizando_jugador, salto_obligatorio):
        '''obtine los hijos y  retorna rna una lista con los estados de los mismos'''
        estado_actual = deepcopy(self.tablero)
        movimientos_disponibles = []
        hijos_estado = []
        letra_grande = ""
        fila_reina = 0
        if minimizando_jugador is True:
            movimientos_disponibles = juego_damas.encontrar_movimientos_disponibles(estado_actual, salto_obligatorio)
            letra_grande = "C"
            fila_reina = 7
        else:
            movimientos_disponibles = juego_damas.find_player_movimientos_disponibles(estado_actual, salto_obligatorio)
            letra_grande = "B"
            fila_reina = 0
        for i in range(len(movimientos_disponibles)):
            viejo_i = movimientos_disponibles[i][0]
            viejo_j = movimientos_disponibles[i][1]
            nuevo_i = movimientos_disponibles[i][2]
            nuevo_j = movimientos_disponibles[i][3]
            estado = deepcopy(estado_actual)
            juego_damas.make_a_move(estado, viejo_i, viejo_j, nuevo_i, nuevo_j, letra_grande, fila_reina)
            hijos_estado.append(Node(estado, [viejo_i, viejo_j, nuevo_i, nuevo_j]))
        return hijos_estado

    def set_valor(self, valor):
        self.valor = valor

    def get_valor(self):
        return self.valor

    def get_tablero(self):
        return self.tablero

    def get_padre(self):
        return self.padre

    def set_padre(self, padre):
        self.padre = padre


class juego_damas:

    def __init__(self):
        self.matriz = [[], [], [], [], [], [], [], []]
        self.turno_jugador = True
        self.piezas_computadora = 12
        self.piezas_jugador = 12
        self.movimientos_disponibles = []
        self.salto_obligatorio = False

        for row_fila in self.matriz:
            for i in range(8):
                row_fila.append("---")

        self.posicion_computadora()
        self.posicion_jugador()

    def posicion_computadora(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matriz[i][j] = ("c" + str(i) + str(j))

    def posicion_jugador(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matriz[i][j] = ("b" + str(i) + str(j))

    def imprimir_matriz(self):
        i = 0
        print()
        for row_fila in self.matriz:
            '''Grafica la fial vertical 0  !, 1  ! con un salto de linea '''
            print(i, end="  |")
            i += 1
            for elem in row_fila:
                '''toma los elemtos de la de (fila_row_fila, columna_elemt) '''
                print(elem, end=" ")
            print()
        print()
        for j in range(8):
            if j == 0:
                j = "     0"
            print(j, end="   ")
        print("\n")

    def get_player_input(self):
        movimientos_disponibles = juego_damas.find_player_movimientos_disponibles(self.matriz, self.salto_obligatorio)
        if len(movimientos_disponibles) == 0:
            if self.piezas_computadora > self.piezas_jugador:
                print(
                    ansi_red + "You have no moves left, and you have fewer pieces than the computer.YOU LOSE!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "You have no available moves.\nGAME ENDED!" + ansi_reset)
                exit()
        self.piezas_jugador = 0
        self.piezas_computadora = 0
        while True:

            coord1 = input("Which piece[i,j]: ")
            if coord1 == "":
                print(ansi_cyan + "Game ended!" + ansi_reset)
                exit()
            elif coord1 == "s":
                print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
                exit()
            coord2 = input("Where to[i,j]:")
            if coord2 == "":
                print(ansi_cyan + "Game ended!" + ansi_reset)
                exit()
            elif coord2 == "s":
                print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
                exit()
            old = coord1.split(",")
            new = coord2.split(",")

            if len(old) != 2 or len(new) != 2:
                print(ansi_red + "Illegal input" + ansi_reset)
            else:
                viejo_i = old[0]
                viejo_j = old[1]
                nuevo_i = new[0]
                nuevo_j = new[1]
                if not viejo_i.isdigit() or not viejo_j.isdigit() or not nuevo_i.isdigit() or not nuevo_j.isdigit():
                    print(ansi_red + "Illegal input" + ansi_reset)
                else:
                    move = [int(viejo_i), int(viejo_j), int(nuevo_i), int(nuevo_j)]
                    if move not in movimientos_disponibles:
                        print(ansi_red + "Illegal move!" + ansi_reset)
                    else:
                        juego_damas.make_a_move(self.matriz, int(viejo_i), int(viejo_j), int(nuevo_i), int(nuevo_j), "B", 0)
                        for m in range(8):
                            for n in range(8):
                                if self.matriz[m][n][0] == "c" or self.matriz[m][n][0] == "C":
                                    self.piezas_computadora += 1
                                elif self.matriz[m][n][0] == "b" or self.matriz[m][n][0] == "B":
                                    self.piezas_jugador += 1
                        break

    @staticmethod
    def encontrar_movimientos_disponibles(tablero, salto_obligatorio):
        movimientos_disponibles = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if tablero[m][n][0] == "c":
                    if juego_damas.check_moves(tablero, m, n, m + 1, n + 1):
                        movimientos_disponibles.append([m, n, m + 1, n + 1])
                    if juego_damas.check_moves(tablero, m, n, m + 1, n - 1):
                        movimientos_disponibles.append([m, n, m + 1, n - 1])
                    if juego_damas.check_jumps(tablero, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if juego_damas.check_jumps(tablero, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif tablero[m][n][0] == "C":
                    if juego_damas.check_moves(tablero, m, n, m + 1, n + 1):
                        movimientos_disponibles.append([m, n, m + 1, n + 1])
                    if juego_damas.check_moves(tablero, m, n, m + 1, n - 1):
                        movimientos_disponibles.append([m, n, m + 1, n - 1])
                    if juego_damas.check_moves(tablero, m, n, m - 1, n - 1):
                        movimientos_disponibles.append([m, n, m - 1, n - 1])
                    if juego_damas.check_moves(tablero, m, n, m - 1, n + 1):
                        movimientos_disponibles.append([m, n, m - 1, n + 1])
                    if juego_damas.check_jumps(tablero, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if juego_damas.check_jumps(tablero, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if juego_damas.check_jumps(tablero, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if juego_damas.check_jumps(tablero, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        if salto_obligatorio is False:
            available_jumps.extend(movimientos_disponibles)
            return available_jumps
        elif salto_obligatorio is True:
            if len(available_jumps) == 0:
                return movimientos_disponibles
            else:
                return available_jumps

    @staticmethod
    def check_jumps(tablero, viejo_i, viejo_j, via_i, via_j, nuevo_i, nuevo_j):
        if nuevo_i > 7 or nuevo_i < 0:
            return False
        if nuevo_j > 7 or nuevo_j < 0:
            return False
        if tablero[via_i][via_j] == "---":
            return False
        if tablero[via_i][via_j][0] == "C" or tablero[via_i][via_j][0] == "c":
            return False
        if tablero[nuevo_i][nuevo_j] != "---":
            return False
        if tablero[viejo_i][viejo_j] == "---":
            return False
        if tablero[viejo_i][viejo_j][0] == "b" or tablero[viejo_i][viejo_j][0] == "B":
            return False
        return True

    @staticmethod
    def check_moves(tablero, viejo_i, viejo_j, nuevo_i, nuevo_j):

        if nuevo_i > 7 or nuevo_i < 0:
            return False
        if nuevo_j > 7 or nuevo_j < 0:
            return False
        if tablero[viejo_i][viejo_j] == "---":
            return False
        if tablero[nuevo_i][nuevo_j] != "---":
            return False
        if tablero[viejo_i][viejo_j][0] == "b" or tablero[viejo_i][viejo_j][0] == "B":
            return False
        if tablero[nuevo_i][nuevo_j] == "---":
            return True

    @staticmethod
    def calculate_heuristics(tablero):
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if tablero[i][j][0] == "c" or tablero[i][j][0] == "C":
                    mine += 1

                    if tablero[i][j][0] == "c":
                        result += 5
                    if tablero[i][j][0] == "C":
                        result += 10
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        continue
                    if (tablero[i + 1][j - 1][0] == "b" or tablero[i + 1][j - 1][0] == "B") and tablero[i - 1][
                        j + 1] == "---":
                        result -= 3
                    if (tablero[i + 1][j + 1][0] == "b" or tablero[i + 1][j + 1] == "B") and tablero[i - 1][j - 1] == "---":
                        result -= 3
                    if tablero[i - 1][j - 1][0] == "B" and tablero[i + 1][j + 1] == "---":
                        result -= 3

                    if tablero[i - 1][j + 1][0] == "B" and tablero[i + 1][j - 1] == "---":
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if (tablero[i + 1][j - 1][0] == "B" or tablero[i + 1][j - 1][0] == "b") and tablero[i + 2][
                        j - 2] == "---":
                        result += 6
                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if (tablero[i + 1][j + 1][0] == "B" or tablero[i + 1][j + 1][0] == "b") and tablero[i + 2][
                        j + 2] == "---":
                        result += 6

                elif tablero[i][j][0] == "b" or tablero[i][j][0] == "B":
                    opp += 1

        return result + (mine - opp) * 1000

    @staticmethod
    def find_player_movimientos_disponibles(tablero, salto_obligatorio):
        movimientos_disponibles = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if tablero[m][n][0] == "b":
                    if juego_damas.check_player_moves(tablero, m, n, m - 1, n - 1):
                        movimientos_disponibles.append([m, n, m - 1, n - 1])
                    if juego_damas.check_player_moves(tablero, m, n, m - 1, n + 1):
                        movimientos_disponibles.append([m, n, m - 1, n + 1])
                    if juego_damas.check_player_jumps(tablero, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if juego_damas.check_player_jumps(tablero, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                elif tablero[m][n][0] == "B":
                    if juego_damas.check_player_moves(tablero, m, n, m - 1, n - 1):
                        movimientos_disponibles.append([m, n, m - 1, n - 1])
                    if juego_damas.check_player_moves(tablero, m, n, m - 1, n + 1):
                        movimientos_disponibles.append([m, n, m - 1, n + 1])
                    if juego_damas.check_player_jumps(tablero, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if juego_damas.check_player_jumps(tablero, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if juego_damas.check_player_moves(tablero, m, n, m + 1, n - 1):
                        movimientos_disponibles.append([m, n, m + 1, n - 1])
                    if juego_damas.check_player_jumps(tablero, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if juego_damas.check_player_moves(tablero, m, n, m + 1, n + 1):
                        movimientos_disponibles.append([m, n, m + 1, n + 1])
                    if juego_damas.check_player_jumps(tablero, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        if salto_obligatorio is False:
            available_jumps.extend(movimientos_disponibles)
            return available_jumps
        elif salto_obligatorio is True:
            if len(available_jumps) == 0:
                return movimientos_disponibles
            else:
                return available_jumps

    @staticmethod
    def check_player_moves(tablero, viejo_i, viejo_j, nuevo_i, nuevo_j):
        if nuevo_i > 7 or nuevo_i < 0:
            return False
        if nuevo_j > 7 or nuevo_j < 0:
            return False
        if tablero[viejo_i][viejo_j] == "---":
            return False
        if tablero[nuevo_i][nuevo_j] != "---":
            return False
        if tablero[viejo_i][viejo_j][0] == "c" or tablero[viejo_i][viejo_j][0] == "C":
            return False
        if tablero[nuevo_i][nuevo_j] == "---":
            return True

    @staticmethod
    def check_player_jumps(tablero, viejo_i, viejo_j, via_i, via_j, nuevo_i, nuevo_j):
        if nuevo_i > 7 or nuevo_i < 0:
            return False
        if nuevo_j > 7 or nuevo_j < 0:
            return False
        if tablero[via_i][via_j] == "---":
            return False
        if tablero[via_i][via_j][0] == "B" or tablero[via_i][via_j][0] == "b":
            return False
        if tablero[nuevo_i][nuevo_j] != "---":
            return False
        if tablero[viejo_i][viejo_j] == "---":
            return False
        if tablero[viejo_i][viejo_j][0] == "c" or tablero[viejo_i][viejo_j][0] == "C":
            return False
        return True

    def evaluate_estados(self):
        t1 = time.time()
        estado_actual = Node(deepcopy(self.matriz))

        first_computer_moves = estado_actual.generar_hijos(True, self.salto_obligatorio)
        if len(first_computer_moves) == 0:
            if self.piezas_jugador > self.piezas_computadora:
                print(
                    ansi_yellow + "Computer has no available moves left, and you have more pieces left.\nYOU WIN!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "Computer has no available moves left.\nGAME ENDED!" + ansi_reset)
                exit()
        dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            valor = juego_damas.minimax(child.get_tablero(), 4, -math.inf, math.inf, False, self.salto_obligatorio)
            dict[valor] = child
        if len(dict.keys()) == 0:
            print(ansi_green + "Computer has cornered itself.\nYOU WIN!" + ansi_reset)
            exit()
        new_tablero = dict[max(dict)].get_tablero()
        move = dict[max(dict)].move
        self.matriz = new_tablero
        t2 = time.time()
        diff = t2 - t1
        print("Computer has moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(
            move[3]) + ").")
        print("It took him " + str(diff) + " seconds.")

    @staticmethod
    def minimax(tablero, depth, alpha, beta, maximizing_player, salto_obligatorio):
        if depth == 0:
            return juego_damas.calculate_heuristics(tablero)
        estado_actual = Node(deepcopy(tablero))
        if maximizing_player is True:
            max_eval = -math.inf
            for child in estado_actual.generar_hijos(True, salto_obligatorio):
                ev = juego_damas.minimax(child.get_tablero(), depth - 1, alpha, beta, False, salto_obligatorio)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            estado_actual.set_valor(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in estado_actual.generar_hijos(False, salto_obligatorio):
                ev = juego_damas.minimax(child.get_tablero(), depth - 1, alpha, beta, True, salto_obligatorio)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            estado_actual.set_valor(min_eval)
            return min_eval

    @staticmethod
    def make_a_move(tablero, viejo_i, viejo_j, nuevo_i, nuevo_j, letra_grande, fila_reina):
        letter = tablero[viejo_i][viejo_j][0]
        i_difference = viejo_i - nuevo_i
        j_difference = viejo_j - nuevo_j
        if i_difference == -2 and j_difference == 2:
            tablero[viejo_i + 1][viejo_j - 1] = "---"

        elif i_difference == 2 and j_difference == 2:
            tablero[viejo_i - 1][viejo_j - 1] = "---"

        elif i_difference == 2 and j_difference == -2:
            tablero[viejo_i - 1][viejo_j + 1] = "---"

        elif i_difference == -2 and j_difference == -2:
            tablero[viejo_i + 1][viejo_j + 1] = "---"

        if nuevo_i == fila_reina:
            letter = letra_grande
        tablero[viejo_i][viejo_j] = "---"
        tablero[nuevo_i][nuevo_j] = letter + str(nuevo_i) + str(nuevo_j)

    def play(self):
        print(ansi_cyan + "##### WELCOME TO juego_damas ####" + ansi_reset)
        print("\nSome basic rules:")
        print("1.You enter the coordinates in the form i,j.")
        print("2.You can quit the game at any time by pressing enter.")
        print("3.You can surrender at any time by pressing 's'.")
        print("Now that you've familiarized yourself with the rules, enjoy!")
        while True:
            answer = input("\nFirst, we need to know, is jumping mandatory?[Y/n]: ")
            if answer == "Y" or answer == "y":
                self.salto_obligatorio = True
                break
            elif answer == "N" or answer == "n":
                self.salto_obligatorio = False
                break
            elif answer == "":
                print(ansi_cyan + "Game ended!" + ansi_reset)
                exit()
            elif answer == "s":
                print(ansi_cyan + "You've surrendered before the game even started.\nPathetic." + ansi_reset)
                exit()
            else:
                print(ansi_red + "Illegal input!" + ansi_reset)
        while True:
            self.imprimir_matriz()
            if self.turno_jugador is True:
                print(ansi_cyan + "\nPlayer's turn." + ansi_reset)
                self.get_player_input()
            else:
                print(ansi_cyan + "Computer's turn." + ansi_reset)
                print("Thinking...")
                self.evaluate_estados()
            if self.piezas_jugador == 0:
                self.imprimir_matriz()
                print(ansi_red + "You have no pieces left.\nYOU LOSE!" + ansi_reset)
                exit()
            elif self.piezas_computadora == 0:
                self.imprimir_matriz()
                print(ansi_green + "Computer has no pieces left.\nYOU WIN!" + ansi_reset)
                exit()
            elif self.piezas_computadora - self.piezas_jugador == 7:
                wish = input("You have 7 pieces fewer than your opponent.Do you want to surrender?")
                if wish == "" or wish == "yes":
                    print(ansi_cyan + "Coward." + ansi_reset)
                    exit()
            self.turno_jugador = not self.turno_jugador


if __name__ == '__main__':
    juego_damas = juego_damas()
    juego_damas.play()
