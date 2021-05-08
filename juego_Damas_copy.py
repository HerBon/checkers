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
        '''obtine los hijos y retorna  una lista con el estado y sus posibles moviminentoslos '''
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
            movimientos_disponibles = juego_damas.encontrar_movimientos_del_jugador_disponibles(estado_actual, salto_obligatorio)
            letra_grande = "B"
            fila_reina = 0
        for i in range(len(movimientos_disponibles)):
            viejo_i = movimientos_disponibles[i][0]
            viejo_j = movimientos_disponibles[i][1]
            nuevo_i = movimientos_disponibles[i][2]
            nuevo_j = movimientos_disponibles[i][3]
            estado = deepcopy(estado_actual)
            juego_damas.hacer_un_movimiento(estado, viejo_i, viejo_j, nuevo_i, nuevo_j, letra_grande, fila_reina)
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

    def posicion_computadora(self):#llena las la matris de los valores c(i,i)
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matriz[i][j] = ("c" + str(i) + str(j))

    def posicion_jugador(self): #llena las la matris de los valores b(i,i)
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matriz[i][j] = ("b" + str(i) + str(j))

    def imprimir_matriz(self):
        '''
        imprime esto en cada vuelta
0  |
1  |
2  |-
3  |
4  |
5  |
6  |
7  |

     0   1   2   3   4   5   6   7
        '''
        i = 0
        print()
        for row_fila in self.matriz:
            '''Grafica la fial vertical 0  !, 1  ! con un salto de linea '''
            print(i, end="  |") # imprime los numerso guia de la primera colimna
            i += 1
            for elem in row_fila:
                '''toma los elemtos de la de (fila_row_fila, columna_elemt)'''
                print(elem, end=" ")
            print() # esto a un espacio en las lineas
        print()
        for j in range(8):
            '''imprime los numeros de la ultima fila guia fila '''
            if j == 0:
                j = "     0"
            print(j, end="   ")
        print("\n") # salto de linea 

    def obtener_entrada_jugador(self):

        '''
        recibe todos los datos que el jugador humano introduce desde la consola
        akmacena y recibe  los  datos de la pieza a mover y  su destino 
        '''

        movimientos_disponibles = juego_damas.encontrar_movimientos_del_jugador_disponibles(self.matriz, self.salto_obligatorio)

        if len(movimientos_disponibles) == 0:
            if self.piezas_computadora > self.piezas_jugador:
                print(
                    ansi_red + "No te quedan movimientos y tienes menos piezas que la computadora. ¡TÚ PIERDES! JAJAJA " + ansi_reset)
                exit() # finaliza el programa
            else:
                print(ansi_yellow + "No tienes movimientos disponibles.\nJUEGO TERMINADO!" + ansi_reset)
                exit()

        self.piezas_jugador = 0
        self.piezas_computadora = 0
        
        while True:

            coord_de_pieza_a_mover = input("cual pieza [i,j]: ")
            if coord_de_pieza_a_mover == "":
                print(ansi_cyan + "No me hagas perder mi timepo, ¡El juego a terminado!" + ansi_reset)
                exit() # termina la ejecucin
            elif coord_de_pieza_a_mover == "s":
                print(ansi_cyan + "JAJAJA te rendiste\nCoward." + ansi_reset)
                exit()
            destino_de_Pieza = input("A donde[i,j]:")
            if destino_de_Pieza == "":
                print(ansi_cyan + "El juego termino!" + ansi_reset)
                exit()
            elif destino_de_Pieza == "s":
                print(ansi_cyan + "YJAJAJA te Rendiste\nCoward." + ansi_reset)
                exit()
            coordenada_antigua = coord_de_pieza_a_mover.split(",") # separa en Una lista a partir del parametro que se le pasa ","
                                            # por ejemplo  "4,5 " ====> ["4"," 5"] 
            coordenada_nueva = destino_de_Pieza.split(",")

            if len(coordenada_antigua) != 2 or len(coordenada_nueva) != 2:
                print(ansi_red + "movimiento ilegal" + ansi_reset)
            else:
                viejo_i = coordenada_antigua[0]
                viejo_j = coordenada_antigua[1]
                nuevo_i = coordenada_nueva[0]
                nuevo_j = coordenada_nueva[1]
                if not viejo_i.isdigit() or not viejo_j.isdigit() or not nuevo_i.isdigit() or not nuevo_j.isdigit(): 
                    # comprueba si los valores introducidos son  numeros de un solo digito .isdigit() 
                    print(ansi_red + "Illegal input" + ansi_reset)
                else:
                    move = [int(viejo_i), int(viejo_j), int(nuevo_i), int(nuevo_j)]
                    if move not in movimientos_disponibles:
                        print(ansi_red + "movimiento ilegal!" + ansi_reset)
                    else:
                        juego_damas.hacer_un_movimiento(self.matriz, int(viejo_i), int(viejo_j), int(nuevo_i), int(nuevo_j), "B", 0)
                        for m in range(8):
                            for n in range(8):
                                if self.matriz[m][n][0] == "c" or self.matriz[m][n][0] == "C":
                                    self.piezas_computadora += 1
                                elif self.matriz[m][n][0] == "b" or self.matriz[m][n][0] == "B":
                                    self.piezas_jugador += 1
                        break

    @staticmethod
    def encontrar_movimientos_disponibles(tablero, salto_obligatorio):
        # Encuentra todos los movimientos disponibles para el turno que recibe, 
        #tanto para la dama como para el peon, y devuelve una lista con los posibles movicoste_p4ra_ctos o saltos(comer pieza)
        movimientos_disponibles = []
        saltos_disponibles = []
        for m in range(8):
            for n in range(8):
                if tablero[m][n][0] == "c": # si es pieza peon 
                    if juego_damas.conprobar_movimientos(tablero, m, n, m + 1, n + 1):
                        movimientos_disponibles.append([m, n, m + 1, n + 1])
                    if juego_damas.conprobar_movimientos(tablero, m, n, m + 1, n - 1):
                        movimientos_disponibles.append([m, n, m + 1, n - 1])
                    if juego_damas.comprobar_saltos(tablero, m, n, m + 1, n - 1, m + 2, n - 2):
                        saltos_disponibles.append([m, n, m + 2, n - 2])
                    if juego_damas.comprobar_saltos(tablero, m, n, m + 1, n + 1, m + 2, n + 2):
                        saltos_disponibles.append([m, n, m + 2, n + 2])
                elif tablero[m][n][0] == "C": # si es pieza REINA   
                    if juego_damas.conprobar_movimientos(tablero, m, n, m + 1, n + 1):
                        movimientos_disponibles.append([m, n, m + 1, n + 1])
                    if juego_damas.conprobar_movimientos(tablero, m, n, m + 1, n - 1):
                        movimientos_disponibles.append([m, n, m + 1, n - 1])
                    if juego_damas.conprobar_movimientos(tablero, m, n, m - 1, n - 1):
                        movimientos_disponibles.append([m, n, m - 1, n - 1])
                    if juego_damas.conprobar_movimientos(tablero, m, n, m - 1, n + 1):
                        movimientos_disponibles.append([m, n, m - 1, n + 1])
                    if juego_damas.comprobar_saltos(tablero, m, n, m + 1, n - 1, m + 2, n - 2):
                        saltos_disponibles.append([m, n, m + 2, n - 2])
                    if juego_damas.comprobar_saltos(tablero, m, n, m - 1, n - 1, m - 2, n - 2):
                        saltos_disponibles.append([m, n, m - 2, n - 2])
                    if juego_damas.comprobar_saltos(tablero, m, n, m - 1, n + 1, m - 2, n + 2):
                        saltos_disponibles.append([m, n, m - 2, n + 2])
                    if juego_damas.comprobar_saltos(tablero, m, n, m + 1, n + 1, m + 2, n + 2):
                        saltos_disponibles.append([m, n, m + 2, n + 2])
        if salto_obligatorio is False:
            saltos_disponibles.extend(movimientos_disponibles)
            return saltos_disponibles
        elif salto_obligatorio is True:
            if len(saltos_disponibles) == 0:
                return movimientos_disponibles
            else:
                return saltos_disponibles

    @staticmethod
    def comprobar_saltos(tablero, viejo_i, viejo_j, via_i, via_j, nuevo_i, nuevo_j):
        # evalua la cccionde comerse una ficha y  si ese movimiento es valido
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
    def conprobar_movimientos(tablero, viejo_i, viejo_j, nuevo_i, nuevo_j):
        # evalua la accion de avanzar en una casillla y  si ese movimiento ee valido

        if nuevo_i > 7 or nuevo_i < 0:  # si  el movimiento en la fila se sale del tablero retotna fado
            return False
        if nuevo_j > 7 or nuevo_j < 0: # si el mpvimiento e la columna se sale del tablero retorna falso 
            return False
        if tablero[viejo_i][viejo_j] == "---": # si la posiscion que se eligio para mover estaba vacia entonces retorna falso
            return False
        if tablero[nuevo_i][nuevo_j] != "---": # si la posicion a la que me quiero mover no es un espacio vacio retorna falso
            return False
        if tablero[viejo_i][viejo_j][0] == "b" or tablero[viejo_i][viejo_j][0] == "B":  
            # si la posicion a tomar es la del jugaro esnces devuelve falso poruqe solo se podria saltar esa pieza pero ttomar su ponicion 
            return False
        if tablero[nuevo_i][nuevo_j] == "---":
            # si la pocicion a la que se va ha mover esat vacia y es valida devuelve true
            return True

    @staticmethod
    def calcular_heuristicas(tablero):
        ''' Evalua todas las situciones favorables para el computador ,  la catidas de piezas y retorna '''
        resultado = 0
        contador_c_piezas = 0
        contador_b_piezas = 0
        for i in range(8):
            for j in range(8):
                if tablero[i][j][0] == "c" or tablero[i][j][0] == "C":
                    contador_c_piezas += 1

                    if tablero[i][j][0] == "c": 
                        resultado += 5
                    if tablero[i][j][0] == "C": 
                        resultado += 10
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        resultado += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        '''si hacer esta operacion me saca de los lmites de la matriz, saltar a la siguiente iteracion '''
                        continue
                    if (tablero[i + 1][j - 1][0] == "b" or tablero[i + 1][j - 1][0] == "B") and tablero[i - 1][j + 1] == "---":
                        ''' si (c) a la izquierda en diagonal allas a "b" o "B" y atras a la derecha no tienes a nadie te pueden 
                        comer asi que te resto 3  '''
                        resultado -= 3
                    if (tablero[i + 1][j + 1][0] == "b" or tablero[i + 1][j + 1] == "B") and tablero[i - 1][j - 1] == "---":
                        '''si (c) a la derecha en diagonal alla a "b" O"B"  Y Atraz a la izquierda no 
                        tieens a nadie te pueden comer asi que pierdes 3'''
                        resultado -= 3
                    if tablero[i - 1][j - 1][0] == "B" and tablero[i + 1][j + 1] == "---":
                        #si te pueden comer desde la dercha con una reina pierdes 3pts
                        resultado -= 3

                    if tablero[i - 1][j + 1][0] == "B" and tablero[i + 1][j - 1] == "---":
                        #si te pueden comer desde la izquierda con una reina pierdes 3 pts 
                        resultado -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        #si al avanzas  2 cuadros  hacia la  izquierda y te sales del tablero, saltate ala siguiene iteracion
                        continue
                    if (tablero[i + 1][j - 1][0] == "B" or tablero[i + 1][j - 1][0] == "b") and tablero[i + 2][j - 2] == "---":
                        #si a la izquierda delante  tienes una "b o B"  y atraz de ellas no hay nada sumate 6 
                        resultado += 6
                    if i + 2 > 7 or j + 2 > 7:
                        #si al avanzas  2 cuadros  hacia la  derecha y te sales del tablero, saltate ala siguiene iteracion
                        continue
                    if (tablero[i + 1][j + 1][0] == "B" or tablero[i + 1][j + 1][0] == "b") and tablero[i + 2][j + 2] == "---":
                        #si a la derecha delante  tienes una "b o B"  y atraz de ellas no hay nada sumate 6
                        resultado += 6

                elif tablero[i][j][0] == "b" or tablero[i][j][0] == "B":
                    contador_b_piezas += 1

        return resultado + (contador_c_piezas - contador_b_piezas) * 1000

    @staticmethod
    def encontrar_movimientos_del_jugador_disponibles(tablero, salto_obligatorio):#evalua el tablero EL TABLERO
        #pero esta vez para ver si los movimmientos del jugador son corectos, y  devuelvee una lista con los 
        #movimientos o saltos(comer pieza)
        movimientos_disponibles = []
        saltos_disponibles = []
        for m in range(8):
            for n in range(8):
                if tablero[m][n][0] == "b":
                    if juego_damas.verificar_movimientos_del_jugador(tablero, m, n, m - 1, n - 1):
                        movimientos_disponibles.append([m, n, m - 1, n - 1])
                    if juego_damas.verificar_movimientos_del_jugador(tablero, m, n, m - 1, n + 1):
                        movimientos_disponibles.append([m, n, m - 1, n + 1])
                    if juego_damas.comprobar_saltos_Dejugador(tablero, m, n, m - 1, n - 1, m - 2, n - 2):
                        saltos_disponibles.append([m, n, m - 2, n - 2])
                    if juego_damas.comprobar_saltos_Dejugador(tablero, m, n, m - 1, n + 1, m - 2, n + 2):
                        saltos_disponibles.append([m, n, m - 2, n + 2])
                elif tablero[m][n][0] == "B":
                    if juego_damas.verificar_movimientos_del_jugador(tablero, m, n, m - 1, n - 1):
                        movimientos_disponibles.append([m, n, m - 1, n - 1])
                    if juego_damas.verificar_movimientos_del_jugador(tablero, m, n, m - 1, n + 1):
                        movimientos_disponibles.append([m, n, m - 1, n + 1])
                    if juego_damas.comprobar_saltos_Dejugador(tablero, m, n, m - 1, n - 1, m - 2, n - 2):
                        saltos_disponibles.append([m, n, m - 2, n - 2])
                    if juego_damas.comprobar_saltos_Dejugador(tablero, m, n, m - 1, n + 1, m - 2, n + 2):
                        saltos_disponibles.append([m, n, m - 2, n + 2])
                    if juego_damas.verificar_movimientos_del_jugador(tablero, m, n, m + 1, n - 1):
                        movimientos_disponibles.append([m, n, m + 1, n - 1])
                    if juego_damas.comprobar_saltos_Dejugador(tablero, m, n, m + 1, n - 1, m + 2, n - 2):
                        saltos_disponibles.append([m, n, m + 2, n - 2])
                    if juego_damas.verificar_movimientos_del_jugador(tablero, m, n, m + 1, n + 1):
                        movimientos_disponibles.append([m, n, m + 1, n + 1])
                    if juego_damas.comprobar_saltos_Dejugador(tablero, m, n, m + 1, n + 1, m + 2, n + 2):
                        saltos_disponibles.append([m, n, m + 2, n + 2])
        if salto_obligatorio is False:
            saltos_disponibles.extend(movimientos_disponibles)
            return saltos_disponibles
        elif salto_obligatorio is True:
            if len(saltos_disponibles) == 0:
                return movimientos_disponibles
            else:
                return saltos_disponibles

    @staticmethod
    def verificar_movimientos_del_jugador(tablero, viejo_i, viejo_j, nuevo_i, nuevo_j):
        '''verifica silos movimientos qie hace el jugador son validos solo es valido si se mueve aun espacio vacio correcto'''
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
    def comprobar_saltos_Dejugador(tablero, viejo_i, viejo_j, via_i, via_j, nuevo_i, nuevo_j):
        '''comprueba si las accion de comerte una pieza es correctamente ejecutada'''
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

    def evaluar_estados(self):
        '''evalua el estado del nodo actual y elegir el mejor proximo moviminneto 
        y agregarlo a la matriz de esta clase caculando el tiempo de ejecuciiion he imprimir a donde 
        se esta moviendo'''
        t1 = time.time()
        estado_actual = Node(deepcopy(self.matriz))

        primeros_movimmientos_de_la_computadora = estado_actual.generar_hijos(True, self.salto_obligatorio)
        if len(primeros_movimmientos_de_la_computadora) == 0:
            if self.piezas_jugador > self.piezas_computadora:
                print(
                    ansi_yellow + "A la computadora no le quedan movimientos disponibles y te quedan más piezas.\ntu ganas por ahora !" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "A la computadora no le quedan movimientos disponibles.\njuego terminado !" + ansi_reset)
                exit()
        dict = {}
        for i in range(len(primeros_movimmientos_de_la_computadora)):
            hijo = primeros_movimmientos_de_la_computadora[i]
            valor = juego_damas.minimax(hijo.get_tablero(), 4, -math.inf, math.inf, False, self.salto_obligatorio)
            dict[valor] = hijo
        if len(dict.keys()) == 0:
            print(ansi_green + "La computadora se ha arrinconado..\ntu ganas!" + ansi_reset)
            exit()
        coordenada_nueva_tablero = dict[max(dict)].get_tablero() # escoge el maxima calve que esta en el dicionario
        move = dict[max(dict)].move 
        self.matriz = coordenada_nueva_tablero
        t2 = time.time()
        diff = t2 - t1
        print("La computadora se ha movido de (" + str(move[0]) + "," + str(move[1]) + ") a (" + str(move[2]) + "," + str(move[3]) + ").")
        print("en " + str(diff) + " segundos.")

    @staticmethod
    def minimax(tablero, profundidad, alpha, beta, maximizando_jugador, salto_obligatorio):
        if profundidad == 0:
            return juego_damas.calcular_heuristicas(tablero) #devuelve solo el valor de la heuristica
        estado_actual = Node(deepcopy(tablero))
        if maximizando_jugador is True:
            max_eval = -math.inf # la peor obcino para maximizar
            for hijo in estado_actual.generar_hijos(True, salto_obligatorio):
                ev = juego_damas.minimax(hijo.get_tablero(), profundidad - 1, alpha, beta, False, salto_obligatorio)
                max_eval = max(max_eval, ev) #tiene el maximo valor de la hoja en la que esta 
                alpha = max(alpha, ev)
                if beta <= alpha: # podalos las ramas inutiles
                    break
            estado_actual.set_valor(max_eval) # amacena el valor del maximo y lo devuelve
            return max_eval 
        else:
            min_eval = math.inf # toma la peor opcion posible para minimizar 
            for hijo in estado_actual.generar_hijos(False, salto_obligatorio):
                ev = juego_damas.minimax(hijo.get_tablero(), profundidad - 1, alpha, beta, True, salto_obligatorio)
                min_eval = min(min_eval, ev) #tiene el valor minimo de la hoja en la que esta
                beta = min(beta, ev) 
                if beta <= alpha:
                    break
            estado_actual.set_valor(min_eval)# amacena el valor del minimo y lo devuelve
            return min_eval

    @staticmethod
    def hacer_un_movimiento(tablero, viejo_i, viejo_j, nuevo_i, nuevo_j, letra_grande, fila_reina):
        '''hace el movimiento intercambiando la la celda con un elemto por una vacia 
         y la del destino por el elemto incluida la accion de comerse una pieza'''
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
        print(ansi_cyan + "##### BIENVENIDO A juego_damas ####" + ansi_reset)
        print("\nAlgunas reglas básicas:")
        print("1. Introduzca las coordenadas en la forma i, j.")
        print("2.Puedes salir del juego en cualquier momento presionando Enter.")
        print("3.Puede rendirse en cualquier momento presionando 's'.")
        print("Ahora que se ha familiarizado con las reglas, ¡disfrútelo!")
        while True:
            Respuesta_del_jugador = input("\nPrimero, necesitamos saber, ¿es obligatorio saltar?[Y/n]: ")
            if Respuesta_del_jugador == "Y" or Respuesta_del_jugador == "y":
                self.salto_obligatorio = True
                break
            elif Respuesta_del_jugador == "N" or Respuesta_del_jugador == "n":
                self.salto_obligatorio = False
                break
            elif Respuesta_del_jugador == "":
                print(ansi_cyan + "el juegotermino!" + ansi_reset)
                exit()
            elif Respuesta_del_jugador == "s":
                print(ansi_cyan + "Te has rendido incluso antes de que comenzara el juego.\n JAJAJA Pathetic." + ansi_reset)
                exit()
            else:
                print(ansi_red + "Entrada ilegal!" + ansi_reset)
        while True:
            self.imprimir_matriz()
            if self.turno_jugador is True:
                print(ansi_cyan + "\nTURNO DEL JUGADOR" + ansi_reset)
                self.obtener_entrada_jugador()
            else:
                print(ansi_cyan + "TURNO DE LA COMPUTADORA" + ansi_reset)
                print("Pensando...")
                self.evaluate_estados()
            if self.piezas_jugador == 0:
                self.imprimir_matriz()
                print(ansi_red + "No te quedan piezas.\nTU PIERDES! Yo gano como debe de ser" + ansi_reset)
                exit()
            elif self.piezas_computadora == 0:
                self.imprimir_matriz()
                print(ansi_green + "Computer has no pieces left.\nYOU WIN!" + ansi_reset)
                exit()
            elif self.piezas_computadora - self.piezas_jugador == 7:
                wish = input("Tienes 7 piezas menos que tu contador_b_piezasonent ¿Quieres rendirte?")
                if wish == "" or wish == "yes":
                    print(ansi_cyan + "Coward." + ansi_reset)
                    exit()
            self.turno_jugador = not self.turno_jugador


if __name__ == '__main__':# esto es para que no se ejecute atomaticamante en otro modulo, sin hacer alguna llamada 
    juego_damas = juego_damas()
    juego_damas.play()
