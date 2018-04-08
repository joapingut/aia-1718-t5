# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import persistencia.persistencia as pers
import conjuntos.conjuntos as conj
import conjuntos.reglas as regl


data = pers.read_data('data/retail.dat')
print("Calculando...")
frecuentes, N = conj.generar_conjuntos_frecuentes(data, 0.079)
print(frecuentes)
reglas = regl.genera_reglas(frecuentes, N, data, c_min=0.5)
l_data = len(data)
for reg in reglas:
    print(regl.representa_regla(reg, l_data))



