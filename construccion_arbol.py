"""
Este módulo contiene funciones y clases relacionadas con la construcción y poda de árboles de decisión.
"""

import csv 
import collections 
from clasificacion import clasificar

def dividirConjunto(filas, columna, valor): 
    """
    Divide un conjunto de filas en dos conjuntos según el valor de una columna específica.

    Args:
        filas (list): Lista de filas a dividir.
        columna (int): Índice de la columna a evaluar.
        valor: Valor de la columna para realizar la división.

    Returns:
        tuple: Tupla con dos listas, la primera contiene las filas donde el valor de la columna es igual al valor dado,
               la segunda contiene las filas donde el valor de la columna es diferente al valor dado.
    """
    lista1 = [fila for fila in filas if fila[columna] == valor]
    lista2 = [fila for fila in filas if fila[columna] != valor]
    return (lista1, lista2)

def conteosUnicos(filas):
    """
    Calcula el conteo de ocurrencias únicas de la última columna en un conjunto de filas.

    Args:
        filas (list): Lista de filas.

    Returns:
        dict: Diccionario donde las claves son los valores únicos de la última columna y los valores son las ocurrencias de cada valor.
    """
    resultados = {}
    for fila in filas:
        r = fila[-1]
        if r not in resultados:
            resultados[r] = 0
        resultados[r] += 1
    return resultados

def entropia(filas):
    """
    Calcula la entropía de un conjunto de datos.

    Args:
        filas (list): Lista de filas.

    Returns:
        float: Valor de la entropía.
    """
    from math import log2

    resultados = conteosUnicos(filas)

    ent = 0.0
    total_filas = len(filas)
    for r in resultados.values():
        p = r / total_filas
        ent -= p * log2(p) if p > 0 else 0  # Evita logaritmos de 0
    return ent

def ganancia_informacion(atributo, datos_entrenamiento):
    """
    Calcula la ganancia de información para cada variable.

    Args:
        atributo (int): Índice del atributo a evaluar.
        datos_entrenamiento (list): Lista de filas de datos de entrenamiento.

    Returns:
        float: Valor de la ganancia de información.
    """
    entropia_total = entropia(datos_entrenamiento)
    valores_atributo = set(fila[atributo] for fila in datos_entrenamiento)
    entropia_atributo = 0
    for valor in valores_atributo:
        subset = [fila for fila in datos_entrenamiento if fila[atributo] == valor]
        p = len(subset) / len(datos_entrenamiento)
        entropia_atributo += p * entropia(subset)

    return entropia_total - entropia_atributo

class ArbolDecision:
    def __init__(self, col = -1, valor = None, ramaVerdadera = None, ramaFalsa = None, resultados = None):
        """
        Clase que representa un árbol de decisión.

        Args:
            col (int): Índice de la columna utilizada para dividir el árbol.
            valor: Valor de la columna utilizado para dividir el árbol.
            ramaVerdadera (ArbolDecision): Rama verdadera del árbol.
            ramaFalsa (ArbolDecision): Rama falsa del árbol.
            resultados (dict): Diccionario con los resultados de las hojas del árbol.
        """
        self.col = col
        self.valor = valor
        self.ramaVerdadera = ramaVerdadera
        self.ramaFalsa = ramaFalsa
        self.resultados = resultados  # None para nodos, no None para hojas

def crearArbolDecisionDesde(filas, funcionEvaluacion = entropia):
    """
    Crea y devuelve un árbol de decisión binario.

    Args:
        filas (list): Lista de filas de datos de entrenamiento.
        funcionEvaluacion (function): Función de evaluación utilizada para calcular la ganancia de información.

    Returns:
        ArbolDecision: Árbol de decisión creado.
    """
    if len(filas) == 0: return ArbolDecision()
    puntuacionActual = funcionEvaluacion(filas)

    mejorGanancia = 0.0
    mejorAtributo = None
    mejoressets = None

    numColumnas = len(filas[0]) - 1  # la última columna es la columna de resultado/objetivo 
    
    for col in range(0, numColumnas):
        valoresColumna = [fila[col] for fila in filas]
        
        for valor in valoresColumna:
            (set1, set2) = dividirConjunto(filas, col, valor)

            # Ganancia -- Entropía o Gini
            p = float(len(set1)) / len(filas)
            ganancia = puntuacionActual - p * funcionEvaluacion(set1) - (1 - p) * funcionEvaluacion(set2)
            if ganancia > mejorGanancia and len(set1) > 0 and len(set2) > 0:
                mejorGanancia = ganancia
                mejorAtributo = (col, valor)
                mejoressets = (set1, set2)

    if mejorGanancia > 0:
        ramaVerdadera = crearArbolDecisionDesde(mejoressets[0])
        ramaFalsa = crearArbolDecisionDesde(mejoressets[1])
        return ArbolDecision(col=mejorAtributo[0], valor=mejorAtributo[1], ramaVerdadera=ramaVerdadera, ramaFalsa=ramaFalsa)
    else:
       # print(filas)
        return ArbolDecision(resultados=conteosUnicos(filas))

def podarArbol(arbol, minGanancia, funcionEvaluacion=entropia, notificar=False):
    """
    Poda el árbol de decisión según una ganancia mínima.

    Args:
        arbol (ArbolDecision): Árbol de decisión a podar.
        minGanancia (float): Valor mínimo de ganancia para realizar la poda.
        funcionEvaluacion (function): Función de evaluación utilizada para calcular la ganancia de información.
        notificar (bool): Indica si se debe imprimir un mensaje de notificación al podar una rama.

    Returns:
        None
    """
    # llamada recursiva para cada rama
    if arbol.ramaVerdadera.resultados == None: podarArbol(arbol.ramaVerdadera, minGanancia, funcionEvaluacion, notificar)
    if arbol.ramaFalsa.resultados == None: podarArbol(arbol.ramaFalsa, minGanancia, funcionEvaluacion, notificar)

    if arbol.ramaVerdadera.resultados != None and arbol.ramaFalsa.resultados != None:
        ramaVerdadera, ramaFalsa = [], []

        for v, c in arbol.ramaVerdadera.resultados.items(): ramaVerdadera += [[v]] * c
        for v, c in arbol.ramaFalsa.resultados.items(): ramaFalsa += [[v]] * c

        p = float(len(ramaVerdadera)) / len(ramaVerdadera + ramaFalsa)
        delta = funcionEvaluacion(ramaVerdadera + ramaFalsa) - p * funcionEvaluacion(ramaVerdadera) - (1 - p) * funcionEvaluacion(ramaFalsa)
        if delta < minGanancia: 
            if notificar: print('Se podó una rama: ganancia = %f' % delta)      
            arbol.ramaVerdadera, arbol.ramaFalsa = None, None
            arbol.resultados = conteosUnicos(ramaVerdadera + ramaFalsa)



# #### FUNCIONES DE APOYO (DONDE SERIA ADECUADO PONERLAS? ME HACE RUIDO QUE ESTEN EN ESTE MODULO) ####
            
def graficar(arbolDecision): #FORMATO DE SALIDA
    '''Grafica el árbol de decisión obtenido.'''
    def aCadena(arbolDecision, indent=''):
        if arbolDecision.resultados != None:  # nodo hoja
            return str(arbolDecision.resultados)
        else:
            if isinstance(arbolDecision.valor, int) or isinstance(arbolDecision.valor, float):
                decision = 'Columna %s: x >= %s?' % (arbolDecision.col, arbolDecision.valor)
            else:
                decision = 'Columna %s: x == %s?' % (arbolDecision.col, arbolDecision.valor)
            ramaVerdadera = indent + 'sí -> ' + aCadena(arbolDecision.ramaVerdadera, indent + '\t\t')
            ramaFalsa = indent + 'no  -> ' + aCadena(arbolDecision.ramaFalsa, indent + '\t\t')
            return (decision + '\n' + ramaVerdadera + '\n' + ramaFalsa)

    print(aCadena(arbolDecision))

def cargarCSV(archivo):  # CUAL ES EL MEJOR LUGAR PARA PONER ESTA FUNCION?
    '''Carga un archivo CSV y convierte todos los flotantes e enteros en tipos de datos básicos.'''
    def convertirTipos(s):
        s = s.strip()
        try:
            return float(s) if '.' in s else int(s)
        except ValueError:
            return s    

    lector = csv.reader(open(archivo, 'rt'))
    return [[convertirTipos(item) for item in fila] for fila in lector]



