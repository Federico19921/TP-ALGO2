'''
Este módulo proporciona una función para clasificar observaciones utilizando un árbol de decisión.
La función "clasificar" toma una lista de observaciones a clasificar, un árbol de decisión y un indicador
opcional para manejar datos faltantes en las observaciones.

El módulo contiene dos funciones internas, "clasificarSinDatosFaltantes" y "clasificarConDatosFaltantes",
que clasifican las observaciones según el árbol sin manejar datos faltantes y con manejo de datos faltantes, respectivamente.

La función "clasificarSinDatosFaltantes" clasifica las observaciones según el árbol sin manejar datos faltantes.
La función "clasificarConDatosFaltantes" clasifica las observaciones según el árbol con manejo de datos faltantes.

El módulo utiliza la biblioteca "collections" para crear un diccionario con los resultados de la clasificación para cada observación.
'''

import collections

def clasificar(observaciones: list[list[int]], arbol, datosFaltantes=False) -> dict:
    '''
    Clasifica las observaciones según el árbol.
    '''

    def clasificarSinDatosFaltantes(observaciones: list[list[int]], arbol) -> dict:  
        '''Clasifica las observaciones según el árbol sin manejar datos faltantes.'''
        if arbol.resultados is not None:  # hoja
            return arbol.resultados
        else:
            v = observaciones[arbol.col]
            rama = None
            if isinstance(v, int) or isinstance(v, float):
                if v >= arbol.valor:
                    rama = arbol.ramaVerdadera
                else:
                    rama = arbol.ramaFalsa
            else:
                if v == arbol.valor:
                    rama = arbol.ramaVerdadera
                else:
                    rama = arbol.ramaFalsa
        return clasificarSinDatosFaltantes(observaciones, rama)

    def clasificarConDatosFaltantes(observaciones: list[list[int]], arbol) -> dict: # Funcionalidad C4.5 - Clasificar con datos faltantes
        '''Clasifica las observaciones según el árbol con manejo de datos faltantes.
        
         Si el valor de la obser. es 'None', calculamos las probabilidades de las ramas VERDADERA y FALSA basadas 
         en las frecuencias obsers. en los nodos actuales. Luego, multiplicamos los resultados de clasificacion en cada 
         rama por estas probabilidades y los sumo para obtener el resultado final de clasificación para la obser.
         
         Si el valor de la observación no es 'None', clasificamos normalmente segun el valor de la obser.

        '''
        if arbol.resultados is not None:  
            return arbol.resultados
        else:
            v = observaciones[arbol.col]
            if v is None: # Si el valor es None (o sea, dato faltante), se propaga la clasificacion por ambas ramas
                ramaVerdadera = clasificarConDatosFaltantes(observaciones, arbol.ramaVerdadera) # Clasificar con datos faltantes por la rama verdadera
                ramaFalsa = clasificarConDatosFaltantes(observaciones, arbol.ramaFalsa) # Clasificar con datos faltantes por la rama falsa
                cuentaVerdadera = sum(ramaVerdadera.values()) # sumo los valores de la rama verdadera
                cuentaFalsa = sum(ramaFalsa.values()) # sumo los valores de la rama falsa
                pVerdadera = float(cuentaVerdadera) / (cuentaVerdadera + cuentaFalsa) # calculo la probabilidad de la rama verdadera
                pFalsa = float(cuentaFalsa) / (cuentaVerdadera + cuentaFalsa) # calculo la probabilidad de la rama falsa
                resultado = collections.defaultdict(int)   # Creo un diccionario con valores por defecto 0 para almacenar los resultados de la clasificación, esto sirve para que si no existe una clave en el diccionario, se cree con valor 0
                for k, v in ramaVerdadera.items(): # Recorro los elementos de la rama verdadera
                    resultado[k] += v * pVerdadera # voy multiplicando el valor de la rama verdadera por la probabilidad de la rama verdadera y esto lo agrego al resultado
                for k, v in ramaFalsa.items(): # recorro los elementos de la rama falsa
                    resultado[k] += v * pFalsa # voy multiplicando el valor de la rama falsa por la probabilidad de la rama falsa y esto lo agrego al resultado
                return dict(resultado) # y por ultimo devuelvo el resultado como un diccionario
            else: # Si el valor no es None, se clasifica normalmente 
                rama = None # inicializo la rama en None
                if isinstance(v, int) or isinstance(v, float): # si el valor es un nro entero o flotante 
                    if v >= arbol.valor: # si el valor es mayor o igual al valor del arbol
                        rama = arbol.ramaVerdadera # la rama es la rama Verdadera
                    else: # si no
                        rama = arbol.ramaFalsa # la rama es la rama Falsa
                else: # si el valor no es un nro entero o flotante
                    if v == arbol.valor: # si el valor es igual al valor del arbol
                        rama = arbol.ramaVerdadera  # la rama es la rama Verdadera
                    else: # si no
                        rama = arbol.ramaFalsa  # la rama es la rama Falsa
            return clasificarConDatosFaltantes(observaciones, rama) # luego, devuelvo la clasificacion con datos modo faltantes
            # todo esto se hizo para manejar los datos FALTANTES en las observaciones y clasificarlas segun el arbol de decision 

    if datosFaltantes:  # Si se deben manejar datos faltantes
        return clasificarConDatosFaltantes(observaciones, arbol) # clasificamos con datos faltantes
    else:  # Si no se deben manejar datos faltantes
        return clasificarSinDatosFaltantes(observaciones, arbol) # clasificamos sin datos faltantes