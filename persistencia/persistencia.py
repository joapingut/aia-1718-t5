# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import numpy as np


'''
    Funcion para leer el archivo con las trasacciones
    Devuelve una lista con las transacciones.
'''
def read_data(filename):
    # Abrimos el archivo
    f = open(filename, 'r', encoding='utf-8')
    line = f.readline()
    result = []
    # Vamos leyendo cada linea
    while line:
        # Los objetos estan separados por espacios
        spll = line.split(' ')
        nnl = []
        # Convertimos cada numero en un integer y lo añadimos a la lista
        for sp in spll:
            try:
                nun = int(sp)
                nnl.append(nun)
            except ValueError:
                None
        # Si la linea tiene elementos los añadimos a la lista final
        if len(nnl) > 0:
            result.append(nnl)
        line = f.readline()
    return result
