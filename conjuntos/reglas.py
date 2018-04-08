# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import copy
from conjuntos.conjuntos import get_string_representation

def genera_reglas(conjuntos, N, datos, c_min=None, lift=None):
    result = []
    for x in conjuntos:
        if len(x) < 2:
            continue
        ids = get_string_representation(x)
        for y in x:
            causa = copy.copy(x)
            causa.remove(y)
            causa.sort()
            consecuete = y
            confianza = calcula_confinaza(causa, consecuete, datos)
            if c_min is not None:
                cc = (confianza[0]/confianza[1])
                if cc < c_min:
                    continue
            soporte = N[ids]
            if lift is not None:
                ids_y = get_string_representation([consecuete])
                p_y = N[ids_y]
                if ((confianza[0]/confianza[1]) / p_y) >= lift:
                    result.append((causa, consecuete, soporte, confianza))
            else:
                result.append((causa, consecuete, soporte, confianza))
    return result


def calcula_confinaza(causa, consecuente, datos):
    total = 0
    cumple = 0
    for x in datos:
        existe = True
        for y in causa:
            if y not in x:
                existe = False
                break
        if existe:
            total += 1
            if consecuente in x:
                cumple += 1
    return (cumple, total)


def representa_regla(regla, total_d):
    c_1, c_2 = regla[3]
    return str(regla[0]) + ' -> ' + str(regla[1]) + ' (s=' + str(regla[2] / total_d) + ', c=' + str(c_1 / c_2) + ')'