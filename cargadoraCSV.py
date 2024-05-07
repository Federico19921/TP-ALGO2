# cargarCSV.py 
# Esto va en FUNCIONES DE APOYO

import csv 

def cargarCSV(archivo):  
    '''Carga un archivo CSV y convierte todos los flotantes y enteros en tipos de datos básicos.'''
    def convertirTipos(s):
        s = s.strip()
        try:
            return float(s) if '.' in s else int(s)
        except ValueError:
            return s    

    lector = csv.reader(open(archivo, 'rt'))
    return [[convertirTipos(item) for item in fila] for fila in lector]


