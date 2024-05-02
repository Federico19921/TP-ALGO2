import construccion_arbol
import clasificacion


def main():
    datosEntrenamiento = construccion_arbol.cargarCSV('weather.csv')  
    arbolDecision = construccion_arbol.crearArbolDecisionDesde(datosEntrenamiento)
    construccion_arbol.graficar(arbolDecision)
    print(clasificacion.clasificar(['Sunny', 'Cool', 'High', 'Strong'], arbolDecision)) #  SALIDA: {'Yes': 1}

    datos_entrenamiento = construccion_arbol.cargarCSV('weather.csv')

    ig_outlook = construccion_arbol.ganancia_informacion(0, datos_entrenamiento)
    ig_temperatura = construccion_arbol.ganancia_informacion(1, datos_entrenamiento)
    ig_humedad = construccion_arbol.ganancia_informacion(2, datos_entrenamiento)
    ig_wind = construccion_arbol.ganancia_informacion(3, datos_entrenamiento)

    print(f'IG(Outlook): {ig_outlook}')
    print(f'IG(Temperatura): {ig_temperatura}')
    print(f'IG(Humedad): {ig_humedad}')
    print(f'IG(Wind): {ig_wind}')

if __name__ == '__main__':

	# Todos los ejemplos hacen los siguientes pasos:
	# 	1. Cargar datos de entrenamiento
	# 	2. Dejar que el árbol de decisión crezca
	# 	4. Graficar el árbol de decisión
	# 	5. Clasificar sin datos faltantes
	# 	6. Clasificar con datos faltantes
	#  FALTA	(7.) Podar el árbol de decisión según un nivel mínimo de ganancia 
	#  FALTA	(8.) Graficar el árbol podado

    main()
