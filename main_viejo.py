# Por ahora lo mantenemos en el repo por las dudas pero sepamos que esto quedó en el pasado. 

import Algoritmo
import clasificacion
import muestreo

# CON BOOTSTRAP
def main():
    datos_entrenamiento = Algoritmo.cargarCSV('weather.csv')  

    #   SELECCION ALEATORIA DE ATRIBUTOS
    atributos = ['Outlook', 'Temperature', 'Humidity', 'Wind']
    cantidad_seleccion = round(len(atributos) / 2)  # Aproximadamente la mitad de los atributos
    atributos_seleccionados = muestreo.seleccion_aleatoria_caracteristicas(atributos, cantidad_seleccion)
    print("Atributos seleccionados aleatoriamente:", atributos_seleccionados)

    
    # Aplicar bootstrapping al conjunto de datos de entrenamiento
    tamano_muestra = len(datos_entrenamiento)
    muestra_bootstrap = muestreo.bootstrapping(datos_entrenamiento, tamano_muestra)
    
    # Construir árbol de decisión con la muestra bootstrap
    arbol_decision = Algoritmo.crearArbolDecisionDesde(muestra_bootstrap)
    
    # Graficar el árbol de decisión
    Algoritmo.graficar(arbol_decision)
    
    # Ejemplo de clasificación
    print(clasificacion.clasificar(['Sunny', 'Cool', 'High', 'Strong'], arbol_decision)) # SALIDA: {'Yes': 1}
    
    # Calcular la ganancia de información para cada atributo
    ig_outlook = Algoritmo.ganancia_informacion(0, muestra_bootstrap)
    ig_temperatura = Algoritmo.ganancia_informacion(1, muestra_bootstrap)
    ig_humedad = Algoritmo.ganancia_informacion(2, muestra_bootstrap)
    ig_wind = Algoritmo.ganancia_informacion(3, muestra_bootstrap)

    print(f'IG(Outlook): {ig_outlook}')
    print(f'IG(Temperatura): {ig_temperatura}')
    print(f'IG(Humedad): {ig_humedad}')
    print(f'IG(Wind): {ig_wind}')


# ------------------------------------
    # ALGUNAS SALIDAS CON BOOTSTRAP:
# ------------------------------------

    '''

TEST 1:
Columna 2: x == high?
sí -> Columna 0: x == overcast?
                sí -> {'yes': 2}
                no  -> {'no': 4}
no  -> Columna 0: x == rainy?
                sí -> Columna 3: x == strong?
                                sí -> {'no': 1}
                                no  -> {'yes': 2}
                no  -> {'yes': 5}
{'yes': 5}
IG(Outlook): 0.19996253177061118
IG(Temperatura): 0.026233709947067974
IG(Humedad): 0.23612234796179488
IG(Wind): 0.04533417202914447


TEST 2:
Columna 0: x == sunny?
sí -> {'no': 2}
no  -> Columna 3: x == strong?
                sí -> Columna 0: x == overcast?
                                sí -> {'yes': 3}
                                no  -> {'no': 1}
                no  -> {'yes': 8}
{'yes': 8}
IG(Outlook): 0.47101421941018534
IG(Temperatura): 0.05421400772308038
IG(Humedad): 0.12010175780898513
IG(Wind): 0.0021385824944688547
    
    
TEST 3:
Columna 3: x == strong?
sí -> Columna 0: x == rainy?
                sí -> {'no': 3}
                no  -> Columna 1: x == hot?
                                sí -> {'no': 1}
                                no  -> {'yes': 2}
no  -> Columna 2: x == normal?
                sí -> {'yes': 7}
                no  -> {'no': 1}
{'no': 1}
IG(Outlook): 0.24674981977443933
IG(Temperatura): 0.0031848530446492163
IG(Humedad): 0.19282928390562004
IG(Wind): 0.23612234796179488
    '''
    

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




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
 # SIN BOOTSTRAP
'''
def main():
    datos_entrenamiento = construccion_arbol.cargarCSV('weather.csv')  
    
    # Construir árbol de decisión con el conjunto de datos de entrenamiento original
    arbol_decision = construccion_arbol.crearArbolDecisionDesde(datos_entrenamiento)
    
    # Graficar el árbol de decisión
    construccion_arbol.graficar(arbol_decision)
    
    # Ejemplo de clasificación
    print(clasificacion.clasificar(['Sunny', 'Cool', 'High', 'Strong'], arbol_decision)) # SALIDA: {'Yes': 1}
    
    # Calcular la ganancia de información para cada atributo
    ig_outlook = construccion_arbol.ganancia_informacion(0, datos_entrenamiento)
    ig_temperatura = construccion_arbol.ganancia_informacion(1, datos_entrenamiento)
    ig_humedad = construccion_arbol.ganancia_informacion(2, datos_entrenamiento)
    ig_wind = construccion_arbol.ganancia_informacion(3, datos_entrenamiento)

    print(f'IG(Outlook): {ig_outlook}')
    print(f'IG(Temperatura): {ig_temperatura}')
    print(f'IG(Humedad): {ig_humedad}')
    print(f'IG(Wind): {ig_wind}')


    SALIDA SIN BOOTSTRAP:

    Columna 0: x == overcast?
sí -> {'yes': 4}
no  -> Columna 2: x == high?
                sí -> Columna 0: x == sunny?
                                sí -> {'no': 3}
                                no  -> Columna 3: x == weak?
                                                sí -> {'yes': 1}
                                                no  -> {'no': 1}
                no  -> Columna 3: x == weak?
                                sí -> {'yes': 3}
                                no  -> Columna 0: x == rainy?
                                                sí -> {'no': 1}
                                                no  -> {'yes': 1}
{'yes': 1}
IG(Outlook): 0.24674981977443933
IG(Temperatura): 0.02922256565895487
IG(Humedad): 0.15183550136234159
IG(Wind): 0.04812703040826949

'''
