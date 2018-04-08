# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import copy


def generar_conjuntos_frecuentes(datos, s_min):
    k = 1
    L, N = genera_y_filtra_candidatos_k1(datos, s_min)
    result = []
    result.extend(L)
    while True:
        cand = genera_candidatos(L)
        cand, nn = filtrar_candidatos(cand, datos, s_min)
        if len(cand) > 0:
            result.extend(cand)
            L = cand
            N.update(nn)
        else:
            break
    return (result, N)


def genera_y_filtra_candidatos_k1(datos, s_min):
    N = {}
    result = []
    for x in datos:
        used = []
        for y in x:
            if y in used:
                continue
            ids = get_string_representation([y])
            if [y] in result:
                N[ids] = N[ids] + 1
            else:
                N[ids] = 1
                result.append([y])
            used.append(y)
    final_res = []
    l_datos = len(datos)
    for r in result:
        ids = get_string_representation(r)
        if (N[ids] / l_datos) >= s_min:
            final_res.append(r)
        else:
            del N[ids]
    return (final_res, N)


def genera_candidatos(datos):
    i = 0; j= 0
    result = []
    while i < (len(datos) - 1):
        c1 = datos[i]
        j = i + 1
        while j < len(datos):
            c2 = datos[j]
            if compara_conjuntos(c1, c2):
                c3 = copy.copy(c1)
                c3.append(c2[len(c1) - 1])
                c3.sort()
                if es_frecuente(datos, c3):
                    result.append(c3)
            j += 1
        i += 1
    return result


def filtrar_candidatos(candidatos, datos, s_min):
    N = {}
    result = []
    l_datos = len(datos)
    for cand in candidatos:
        soporte = get_soporte(cand, datos)
        if (soporte / l_datos) >= s_min:
            idf = get_string_representation(cand)
            N[idf] = soporte
            result.append(cand)
    return (result, N)


def get_soporte(c1, datos):
    result = 0
    for x in datos:
        cop = True
        for y in c1:
            if y not in x:
                cop = False
                break
        if cop:
            result += 1
    return result


def es_frecuente(datos, c1):
    k = len(c1) -1
    n = c1[k]
    for i in range(0, k):
        aux = copy.copy(c1[:k])
        aux[i] = n
        aux.sort()
        if aux not in datos:
            return False
    return True


def get_string_representation(c1):
    return ','.join(str(x) for x in c1)


def compara_conjuntos(c1, c2):
    l = len(c1)
    if l < 2:
        return True
    return c1[:l -1 ] == c2[:l -1]