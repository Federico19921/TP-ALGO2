"""
C4.5 es un algoritmo de aprendizaje automático que genera árboles de decisión. Este algoritmo es una extensión de 
ID3 y fue desarrollado por Ross Quinlan. C4.5 es capaz de manejar datos faltantes y puede ser utilizado para 
problemas de clasificación y regresión. Este bloque de código implementa el algoritmo C4.5 para la construcción de un RandomForest.

Este módulo contiene funciones y clases relacionadas con la construcción y poda de árboles de decisión.
"""

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
    Calcula la entropía de un conjunto de datos usando la definición de Shannon.

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

    filas = imputacionValoresFaltantes(filas) # Manejamos valores faltantes antes de construir el arbol de desicion
  #  filas = manejoAtributosContinuos(filas) 
    ordenarValoresUnicos(filas)  # Ordenamos valores unicos (para atributos continuos #C4.5)

    if len(filas) == 0: return ArbolDecision()
    puntuacionActual = funcionEvaluacion(filas)

    mejorGanancia = 0.0
    mejorAtributo = None
    mejoressets = None

    numColumnas = len(filas[0]) - 1  # la ultima columna es la columna de resultado/objetivo 
    
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




###### NUEVAS FUNCIONES ######

            
def ordenarValoresUnicos(filas):
    """
    Ordena los valores únicos de un atributo continuo en orden ascendente.

    Args:
        filas (list): Lista de filas de datos.

    Returns:
        list: Lista de valores únicos ordenados en orden ascendente.
    """
    valores_unicos_ordenados = []
    for atributo in range(len(filas[0]) - 1):
        if isinstance(filas[0][atributo], int) or isinstance(filas[0][atributo], float):
            valores = sorted(set(fila[atributo] for fila in filas))
            valores_unicos_ordenados.append(valores)
    return valores_unicos_ordenados


# Manejo de atributos continuos y valores faltantes:
def mejorUmbral(atributo, datos_entrenamiento):
    """
    Encuentra el mejor umbral para un atributo continuo utilizando el criterio de ganancia de información.

    Args:
        atributo (int): Índice del atributo a evaluar.
        datos_entrenamiento (list): Lista de filas de datos de entrenamiento.

    Returns:
        float: Mejor umbral encontrado.
    """
    valores = sorted(set(fila[atributo] for fila in datos_entrenamiento))
    mejor_ganancia = 0
    mejor_umbral = None
    for i in range(1, len(valores)):
        umbral = (valores[i - 1] + valores[i]) / 2
        conjunto_izquierdo, conjunto_derecho = [], []
        for fila in datos_entrenamiento:
            if fila[atributo] <= umbral:
                conjunto_izquierdo.append(fila)
            else:
                conjunto_derecho.append(fila)
        if len(conjunto_izquierdo) == 0 or len(conjunto_derecho) == 0:
            continue
        ganancia = ganancia_informacion(atributo, datos_entrenamiento)
        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_umbral = umbral
    return mejor_umbral

def manejoAtributosContinuos(filas):
    """
    Maneja atributos continuos dividiendo el conjunto de datos en dos conjuntos basados en umbrales.

    Args:
        filas (list): Lista de filas de datos de entrenamiento.

    Returns:
        list: Lista de filas de datos de entrenamiento con atributos continuos manejados.
    """
    filas_nuevas = []
    for atributo in range(len(filas[0]) - 1):
        if isinstance(filas[0][atributo], int) or isinstance(filas[0][atributo], float):
            umbral = mejorUmbral(atributo, filas)
            filas_izquierda, filas_derecha = [], []
            for fila in filas:
                if fila[atributo] <= umbral:
                    filas_izquierda.append(fila)
                else:
                    filas_derecha.append(fila)
            filas_nuevas.extend(filas_izquierda)
            filas_nuevas.extend(filas_derecha)
    return filas_nuevas

def imputacionValoresFaltantes(filas): # decidimos usar la media de la columna para reemplazar los valores faltantes (o sea, imputar los valores faltantes con el valor que resulta de calcular la media de la columna)
    """
    Imputa valores faltantes en el conjunto de datos.

    Args:
        filas (list): Lista de filas de datos de entrenamiento.

    Returns:
        list: Lista de filas de datos de entrenamiento con valores faltantes imputados.
    """
    columnas = len(filas[0])
    for i in range(columnas):
        # Encontramos la media de la columna actual
        valores = [fila[i] for fila in filas if fila[i] is not None and fila[i].isdigit()]
        if valores:
            media_columna = sum(map(int, valores)) / len(valores)
            # Y rellenamos los valores faltantes con la media de la columna
            for j in range(len(filas)):
                if filas[j][i] is None:
                    filas[j][i] = media_columna
    return filas


# Criterio de division (Gain Ratio):
def gainRatio(atributo, datos_entrenamiento): 
    """
    Calcula el Gain Ratio para un atributo.

    Args:
        atributo (int): Índice del atributo a evaluar.
        datos_entrenamiento (list): Lista de filas de datos de entrenamiento.

    Returns:
        float: Valor del Gain Ratio.
    """
    ganancia = ganancia_informacion(atributo, datos_entrenamiento)
    split_info = calcularSplitInfo(atributo, datos_entrenamiento)
    return ganancia / split_info if split_info != 0 else 0

def calcularSplitInfo(atributo, datos_entrenamiento):

    """
    Calcula el Split Information para un atributo.

    Args:
        atributo (int): Índice del atributo a evaluar.
        datos_entrenamiento (list): Lista de filas de datos de entrenamiento.

    Returns:
        float: Valor del Split Information.
    """    

    from math import log2

    valores_atributo = set(fila[atributo] for fila in datos_entrenamiento)
    total_filas = len(datos_entrenamiento)
    split_info = 0
    for valor in valores_atributo:
        p = sum(1 for fila in datos_entrenamiento if fila[atributo] == valor) / total_filas
        split_info -= p * log2(p) if p > 0 else 0 
    return split_info

# Costos asimétricos y datos ponderados:
# IMPLEMENTAR estas funcionalidades según lo requerido por el TPF.
