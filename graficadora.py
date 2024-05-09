#graficar.py
# NOTA: Esto va en FUNCIONES DE APOYO (REVISAR SI QUEREMOS O NO CREAR ESE MODULO)
# Se encarga de graficar el árbol de decisión obtenido.

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
