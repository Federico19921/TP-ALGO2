import csv

class CargadorCsv:
    def __init__(self, archivo):
        self.archivo = archivo

    def cargarCSV(self) -> list[list[any]]:
        '''Carga un archivo CSV y convierte todos los flotantes y enteros en tipos de datos básicos.'''
        def convertirTipos(s):
            s = s.strip()
            try:
                return float(s) if '.' in s else int(s)
            except ValueError:
                return s    

        try:
            with open(self.archivo, 'rt') as file:
                lector = csv.reader(file)
                return [[convertirTipos(item) for item in fila] for fila in lector]
        except FileNotFoundError:
            print(f"El archivo '{self.archivo}' no fue encontrado.")
            return []
        except Exception as e:
            print(f"Error al cargar el archivo '{self.archivo}': {e}")
            return []
