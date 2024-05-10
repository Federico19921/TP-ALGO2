"""
Este módulo contiene funciones y clases relacionadas con la construcción y poda de árboles de decisión.
Incluye funciones y clases que permiten generar arboles de decision a traves del uso del algoritmo C4.5, una extension del algoritmo ID3.

Ademas de la construccion de arboles de decision, el modulo ofrece funcionalidades para manejar datos faltantes, trabajar con atributos continuos, 
calcular ganancias de informacion y ratios de ganancia, entre otras operaciones relacionadas con el aprendizaje automatico. 
El modulo tambien proporciona herramientas para la poda de arboles de decision segun criterios especificos, lo que permite optimizar la 
estructura del arbol para mejorar la generalizacion del modelo.
"""

from typing import Optional
from clasificacion import clasificar
from math import log2

def dividirConjunto(filas: list[list[any]], columna: int, valor: any) -> tuple[list[list[any]],list[list[any]]]: 
    """
    Divide un conjunto de filas en dos conjuntos según el valor de una columna específica.
    """
    lista1 = [fila for fila in filas if fila[columna] == valor]
    lista2 = [fila for fila in filas if fila[columna] != valor]
    return (lista1, lista2)

def conteosUnicos(filas: list[list[any]]) -> dict:
    """
    Calcula el conteo de ocurrencias únicas de la última columna en un conjunto de filas.
    """
    resultados = {}
    for fila in filas:
        r = fila[-1]
        if r not in resultados:
            resultados[r] = 0
        resultados[r] += 1
    return resultados

def entropia(filas: list[list[any]]) -> float:
    """
    Calcula la entropía de un conjunto de datos usando la definición de Shannon.
    """
    from math import log2

    resultados = conteosUnicos(filas)

    ent = 0.0
    total_filas = len(filas)
    for r in resultados.values():
        p = r / total_filas
        ent -= p * log2(p) if p > 0 else 0  # Evita logaritmos de 0
    return ent

def ganancia_informacion(atributo: int, datos_entrenamiento: list[list[any]]) -> float:
    """
    Calcula la ganancia de información para cada variable.
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
        """
        self.col = col
        self.valor = valor
        self.ramaVerdadera = ramaVerdadera
        self.ramaFalsa = ramaFalsa
        self.resultados = resultados  # None para nodos, no None para hojas

def crearArbolDecisionDesde(filas: list[list[any]], max_profundidad = Optional[int], min_ganancia = Optional[float], min_muestras_nodo = 1) -> "ArbolDecision":
    """
    Crea y devuelve un árbol de decisión binario.
    """

    filas = imputacionValoresFaltantes(filas) # Manejamos valores faltantes antes de construir el arbol de desicion
    ordenarValoresUnicos(filas)  # Ordenamos valores unicos (para atributos continuos #C4.5)

    if len(filas) == 0: 
        return ArbolDecision()

    if len(filas) < min_muestras_nodo:
        return ArbolDecision(resultados=conteosUnicos(filas))

    if nodo_puro(filas):
        return ArbolDecision(resultados=conteosUnicos(filas))

    if max_profundidad is not None and max_profundidad <= 0:
        return ArbolDecision(resultados=conteosUnicos(filas))  
    
    
    puntuacionActual = entropia(filas)

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
            ganancia = puntuacionActual - p * entropia(set1) - (1 - p) * entropia(set2)

            if ganancia < min_ganancia:
                continue

            if ganancia > mejorGanancia and len(set1) > 0 and len(set2) > 0:
                mejorGanancia = ganancia
                mejorAtributo = (col, valor)
                mejoressets = (set1, set2)

    if mejorGanancia > 0:
        ramaVerdadera = crearArbolDecisionDesde(mejoressets[0],max_profundidad -1, min_ganancia,  min_muestras_nodo = 1)
        ramaFalsa = crearArbolDecisionDesde(mejoressets[1], max_profundidad -1, min_ganancia, min_muestras_nodo = 1)
        return ArbolDecision(col=mejorAtributo[0], valor=mejorAtributo[1], ramaVerdadera=ramaVerdadera, ramaFalsa=ramaFalsa)
    else:
       # print(filas)
        return ArbolDecision(resultados=conteosUnicos(filas))
    
def nodo_puro(filas: list[list[any]]) -> bool:
    clase_primera_fila = filas[0][-1]  # Clase de la última columna en la primera fila
    for fila in filas:
        if fila[-1] != clase_primera_fila:
            return False
    return True

def podarArbol(arbol: "ArbolDecision", minGanancia:float, notificar=False) -> None:
    """
    Poda el árbol de decisión según una ganancia mínima.
    """
    # llamada recursiva para cada rama
    if arbol.ramaVerdadera.resultados == None: 
        podarArbol(arbol.ramaVerdadera, minGanancia, notificar)
    if arbol.ramaFalsa.resultados == None: 
        podarArbol(arbol.ramaFalsa, minGanancia, notificar)

    if arbol.ramaVerdadera.resultados != None and arbol.ramaFalsa.resultados != None:
        ramaVerdadera, ramaFalsa = [], []

        for v, c in arbol.ramaVerdadera.resultados.items(): ramaVerdadera += [[v]] * c
        for v, c in arbol.ramaFalsa.resultados.items(): ramaFalsa += [[v]] * c

        p = float(len(ramaVerdadera)) / len(ramaVerdadera + ramaFalsa)
        delta = entropia(ramaVerdadera + ramaFalsa) - p * entropia(ramaVerdadera) - (1 - p) * entropia(ramaFalsa)
        if delta < minGanancia: 
            if notificar: print('Se podó una rama: ganancia = %f' % delta)      
            arbol.ramaVerdadera, arbol.ramaFalsa = None, None
            arbol.resultados = conteosUnicos(ramaVerdadera + ramaFalsa)

###### NUEVAS FUNCIONES ######
            
def ordenarValoresUnicos(filas: list[list[any]]) ->  list[list[any]]:
    """
    Ordena los valores únicos de un atributo continuo en orden ascendente.
    """
    valores_unicos_ordenados = []
    for atributo in range(len(filas[0]) - 1):
        if isinstance(filas[0][atributo], int) or isinstance(filas[0][atributo], float):
            valores = sorted(set(fila[atributo] for fila in filas))
            valores_unicos_ordenados.append(valores)
    return valores_unicos_ordenados


# Manejo de atributos continuos y valores faltantes:
def mejorUmbral(atributo:int, datos_entrenamiento: list[list[any]]) -> float:
    """
    Encuentra el mejor umbral para un atributo continuo utilizando el criterio de ganancia de información.
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

def manejoAtributosContinuos(filas: list[list[any]]) -> list[list[any]]:
    """
    Maneja atributos continuos dividiendo el conjunto de datos en dos conjuntos basados en umbrales.
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

def imputacionValoresFaltantes(filas: list[list[any]]) -> list[list[any]]: # decidimos usar la media de la columna para reemplazar los valores faltantes (o sea, imputar los valores faltantes con el valor que resulta de calcular la media de la columna)
    """
    Imputa valores faltantes en el conjunto de datos.
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
def gainRatio(atributo:int, datos_entrenamiento: list[list[any]]) -> float: 
    """
    Calcula el Gain Ratio para un atributo.
    """
    ganancia = ganancia_informacion(atributo, datos_entrenamiento)
    split_info = calcularSplitInfo(atributo, datos_entrenamiento)
    return ganancia / split_info if split_info != 0 else 0

def calcularSplitInfo(atributo:int, datos_entrenamiento: list[list[any]]) -> float:

    """
    Calcula el Split Information para un atributo.
    """    

    valores_atributo = set(fila[atributo] for fila in datos_entrenamiento)
    total_filas = len(datos_entrenamiento)
    split_info = 0
    for valor in valores_atributo:
        p = sum(1 for fila in datos_entrenamiento if fila[atributo] == valor) / total_filas
        split_info -= p * log2(p) if p > 0 else 0 
    return split_info

# Costos asimétricos y datos ponderados:
# IMPLEMENTAR estas funcionalidades según lo requerido por el TPF.
