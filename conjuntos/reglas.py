# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import copy
from conjuntos.conjuntos import get_string_representation

'''
    Funcion para generar las reglas de consecuente unitario a partir de una lista de conjuntos frecuentes.
    Como no se incida nada, se obtienen todas las reglas para todos los k mayores de 1.
    Recibe como parametro:
        - Conjuntos: lista de conjuntos frecuentes
        - N: diccionario con los soportes de los conjuntos
        - datos: lista con toda las transacciones
        - c_min: opcional, confinaza minima que queremos
        - lift: opcional, si queremos un lift concreto

    El resultado es una lista de las reglas, con los siguientes campos:
        - causa: parte izquierda de la regla
        - consecuente: parte derecha de la regla
        - soporte: soporte de la regla
        - cconfianza: confanza de la regla
'''
def genera_reglas(conjuntos, N, datos, c_min=None, lift=None):
    result = []
    # Recorremos todos los conjuntos frecuentes
    for x in conjuntos:
        # Si el conjunto es de tamaño k=1 no podemos hacer reglas asi que lo ignoramos
        if len(x) < 2:
            continue
        # Obtenemos la representacion unica del conjunto frecuente
        ids = get_string_representation(x)
        # Recorremos todos los elementos del conjutno para crear reglas
        for y in x:
            # Creamos una copia de trabajo
            causa = copy.copy(x)
            # Eliminamos de la copia el elemento actual para convertirla en la causa
            causa.remove(y)
            # Ordenamos
            causa.sort()
            # Convertimos el elemento actual en el consecuente
            consecuete = y
            # Calculamos la confianza de la regla
            confianza = calcula_confinaza(causa, consecuete, datos)
            # Miramos si hemos puesto confianza minima
            if c_min is not None:
                # Calculamos el porcentaje de la confianza
                cc = (confianza[0]/confianza[1])
                # Miramos si supera la confianza minima
                if cc < c_min:
                    # Si no supera la confianza minima pasamos a la siguiente regla
                    continue
            # Sacamos el soporte del conjunto de la regla
            soporte = N[ids]
            # Comprobamos si aplicamos lift
            if lift is not None:
                # Si aplicamos lift sacamos el soporte del consecuente, que seguro que esta
                # lista de conjutnos frecuentes ya que un subconjunto de un conjunto frecuente es tambien frecuente
                ids_y = get_string_representation([consecuete])
                p_y = N[ids_y]
                # Comprobamos el lift
                if ((confianza[0]/confianza[1]) / p_y) >= lift:
                    # Si supera el lift lo agregamos a la lista
                    result.append((causa, consecuete, soporte, confianza))
            else:
                # Si no se palica lift lo agregamos siempre
                result.append((causa, consecuete, soporte, confianza))
    return result


'''
    Funcion que calcula la confianza de una regla
    Devuelve una tupla con el numero de veces que se cumple la regla y total de veces que aparece
    la causa.
'''
def calcula_confinaza(causa, consecuente, datos):
    total = 0
    cumple = 0
    # Recorremos todos los datos de las transacciones
    for x in datos:
        existe = True
        # Comprobamos todos los elementos que forman la causa
        for y in causa:
            # Comprobamos si un elemento no esta en la transaccion
            if y not in x:
                # Si no esta paramos y seguimos con el siguiente elemento
                existe = False
                break
        # Si la causa de la regla existe miramos si esta el consecuente o no
        if existe:
            total += 1
            if consecuente in x:
                # Si el consecuente tambien esta se cumple la regla
                cumple += 1
    return (cumple, total)


'''
    Funcion que crea una cadena representando una regla.
    Ej: [3, 5] -> 2 (s=0.5, c=1.0)
'''
def representa_regla(regla, total_d):
    c_1, c_2 = regla[3]
    return str(regla[0]) + ' -> ' + str(regla[1]) + ' (s=' + str(regla[2] / total_d) + ', c=' + str(c_1 / c_2) + ')'