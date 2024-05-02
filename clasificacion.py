

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

def clasificar(observaciones, arbol, datosFaltantes=False):
    '''
    Clasifica las observaciones según el árbol.

    Parámetros:
    - observaciones: una lista de observaciones a clasificar.
    - arbol: el árbol de decisión utilizado para la clasificación.
    - datosFaltantes: un valor booleano que indica si se deben manejar datos faltantes en las observaciones.

    Retorna:
    - Un diccionario con los resultados de la clasificación para cada observación.
    '''

    def clasificarSinDatosFaltantes(observaciones, arbol):
        '''Clasifica las observaciones según el árbol sin manejar datos faltantes.'''
        if arbol.resultados != None:  # hoja
            return arbol.resultados
        else:
            v = observaciones[arbol.col]
            rama = None
            if isinstance(v, int) or isinstance(v, float):
                if v >= arbol.valor: rama = arbol.ramaVerdadera
                else: rama = arbol.ramaFalsa
            else:
                if v == arbol.valor: rama = arbol.ramaVerdadera
                else: rama = arbol.ramaFalsa
        return clasificarSinDatosFaltantes(observaciones, rama)

    def clasificarConDatosFaltantes(observaciones, arbol):
        '''Clasifica las observaciones según el árbol con manejo de datos faltantes.'''
        if arbol.resultados != None:  
            return arbol.resultados
        else:
            v = observaciones[arbol.col]
            if v == None:
                ramaVerdadera = clasificarConDatosFaltantes(observaciones, arbol.ramaVerdadera)
                ramaFalsa = clasificarConDatosFaltantes(observaciones, arbol.ramaFalsa)
                cuentaVerdadera = sum(ramaVerdadera.values())
                cuentaFalsa = sum(ramaFalsa.values())
                pVerdadera = float(cuentaVerdadera) / (cuentaVerdadera + cuentaFalsa)
                pFalsa = float(cuentaFalsa) / (cuentaVerdadera + cuentaFalsa)
                resultado = collections.defaultdict(int)  
                for k, v in ramaVerdadera.items(): resultado[k] += v * pVerdadera
                for k, v in ramaFalsa.items(): resultado[k] += v * pFalsa
                return dict(resultado)
            else:
                rama = None
                if isinstance(v, int) or isinstance(v, float):
                    if v >= arbol.valor: rama = arbol.ramaVerdadera
                    else: rama = arbol.ramaFalsa
                else:
                    if v == arbol.valor: rama = arbol.ramaVerdadera
                    else: rama = arbol.ramaFalsa
            return clasificarConDatosFaltantes(observaciones, rama)

    if datosFaltantes: 
        return clasificarConDatosFaltantes(observaciones, arbol)
    else: 
        return clasificarSinDatosFaltantes(observaciones, arbol)
