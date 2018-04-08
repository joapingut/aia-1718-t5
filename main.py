# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import persistencia.persistencia as pers
import conjuntos.conjuntos as conj
import conjuntos.reglas as regl

'''
    Archivo con las pruebas
'''

'''
    Pruebas con el conjunto de transacciones test.dat
'''
print("Prueba con test.dat")
# Leemos los datos
data = pers.read_data('data/test.dat')
print("Calculando...")
# Obtenemos los conjuntos frecuentes y sus soportes
# El 0.5 es soporte minimo que vamos a buscar
frecuentes, N = conj.generar_conjuntos_frecuentes(data, 0.5)
print(frecuentes)
# Obtenemos las reglas de estos conjuntos frecuentes
# El 0.5 es la confianza minima que queremos
reglas = regl.genera_reglas(frecuentes, N, data, c_min=0.5)
l_data = len(data)
# Mostramos por pantalla las reglas que hemos obtenido
for reg in reglas:
    print(regl.representa_regla(reg, l_data))

'''
    Pruebas con el conjunto de transacciones retail.dat
'''
print("Prueba con retail.dat")
# Leemos los datos
data = pers.read_data('data/retail.dat')
print("Calculando...")
# Obtenemos los conjuntos frecuentes y sus soportes
# El 0.079 es soporte minimo que vamos a buscar
frecuentes, N = conj.generar_conjuntos_frecuentes(data, 0.079)
print(frecuentes)
# Obtenemos las reglas de estos conjuntos frecuentes
# El 0.5 es la confianza minima que queremos
reglas = regl.genera_reglas(frecuentes, N, data, c_min=0.5)
l_data = len(data)
# Mostramos por pantalla las reglas que hemos obtenido
for reg in reglas:
    print(regl.representa_regla(reg, l_data))
