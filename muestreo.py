# Description: Implementación de la técnica de bootstrapping 
# para generar muestras aleatorias con repetición (o sea, un mismo elemento 
# puede ser seleccionado más de una vez)

import random 

def bootstrapping(datos_entrenamiento, tamano_muestra): # datos_entrenamiento es una lista
    muestra = [] 
    for _ in range(tamano_muestra): 
        muestra.append(random.choice(datos_entrenamiento)) # Seleccionar un elemento aleatorio de datos_entrenamiento y agregarlo a muestra
    return muestra # Devuelvo la muestra bootstrap


def seleccion_aleatoria_caracteristicas(atributos, cantidad_seleccion):
    atributos_seleccionados = random.sample(atributos, cantidad_seleccion)
    return atributos_seleccionados


def combinar_predicciones(predicciones):
    # Función para combinar las predicciones de los árboles en el bosque
    # En este caso, se implementa la votación mayoritaria para problemas de clasificación
    # Se asume que predicciones es una lista de diccionarios donde cada diccionario contiene las predicciones de un árbol
    predicciones_combinadas = {}
    for pred in predicciones:
        for clase, conteo in pred.items():
            if clase not in predicciones_combinadas:
                predicciones_combinadas[clase] = 0
            predicciones_combinadas[clase] += conteo
    # Seleccionar la clase con mayor votación como la predicción final
    clase_final = max(predicciones_combinadas, key=predicciones_combinadas.get)
    return {clase_final: predicciones_combinadas[clase_final]}
