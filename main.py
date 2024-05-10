
import clasificacion
import muestreo
from cargadoraCSV import CargadorCsv
import graficadora
import Algoritmo

def main():
    archivo_csv = "weather.csv"
    csv_loader = CargadorCsv(archivo_csv)
    datos_entrenamiento = csv_loader.cargarCSV()
    
    # Realizar selección aleatoria de características
    atributos = ['Outlook', 'Temperature', 'Humidity', 'Wind']
    cantidad_seleccion = round(len(atributos) / 2)  # Aproximadamente la mitad de los atributos
    atributos_seleccionados = muestreo.seleccion_aleatoria_caracteristicas(atributos, cantidad_seleccion)
   

    numero_arboles = 4 #PROBEMOS CON 4 ARBOLES
    instancia = ['Sunny', 'Cool', 'High', 'Strong'] # EJEMPLO DE INSTANCIA A CLASIFICAR
    
    print("Atributos seleccionados aleatoriamente:", atributos_seleccionados)

    # Crear una lista para almacenar las predicciones de cada árbol
    predicciones_arboles = []


    # Aplicar bootstrapping y construir árboles de decisión
    for _ in range(numero_arboles):
        tamano_muestra = len(datos_entrenamiento)
        muestra_bootstrap = muestreo.bootstrapping(datos_entrenamiento, tamano_muestra)
        arbol_decision = Algoritmo.crearArbolDecisionDesde(muestra_bootstrap, 3,0.05)

        print(f"Árbol de decisión {_ + 1}:")
        graficadora.graficar(arbol_decision) # Graficar el árbol de decisión para esta iteracion i de 10

        predicciones_arboles.append(clasificacion.clasificar(instancia, arbol_decision)) # Clasificar la instancia con el arbol de decision actual y agregar la predicción a la lista de predicciones_arboles

    # Combinar las predicciones de todos los árboles
    prediccion_final = muestreo.combinar_predicciones(predicciones_arboles)
    print("Predicción final:", prediccion_final) # UNA DE LAS POSIBLES SALIDAS FUE: {'Yes': 10} donde 'Yes' es la clase con mayor votación y 10 es el número de votos para esa clase que significa que la clase Yes fue seleccionada por todos los árboles en el bosque de decisión un total de 10 veces.

if __name__ == '__main__':
    main()
