# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import copy


'''
    Funcion que genera conjuntos frecuentes.

    Recibe como parametro el conjunto de todas las transacciones y el soporte minimo.

    Devuelve la lista con los conjuntos frecuentes que superen el s_min y
    un diccionario con el soporte de dichos conjuntos.
'''
def generar_conjuntos_frecuentes(datos, s_min):
    # Calculamos los conjutnos frecuentes de tamaño k = 1
    L, N = genera_y_filtra_candidatos_k1(datos, s_min)
    result = []
    result.extend(L)
    # Mientras podamos seguir generando conjutnos frecuentes...
    while True:
        # Generamos la lista de conjuntos para la k actual
        cand = genera_candidatos(L)
        # Filtramos los conjuntos de la k actual, quedandonos con los que son frecuentes y que superen el s_min
        cand, nn = filtrar_candidatos(cand, datos, s_min)
        # Comprobamos si hemos generado conjuntos
        if len(cand) > 0:
            # Si tenemos conjuntos los agregamos a la lista y al diccinario.
            result.extend(cand)
            L = cand
            N.update(nn)
        else:
            # Si no hemos sido capaces de generar mas conjuntos es que ya no quedan conjuntos frecuentes por encontrar.
            break
    return (result, N)


'''
    Funcion que genera y filtra los conjuntos frecuentes de tamaño k = 1
    Se hace por separado porque no cumplen las mismas condiciones que el resto de k
    Recibe como entrada la base de transacciones y el soporte minimo.
    Devuelve la lista con los conjuntos frecuentes de tamaño k=1 que superen el s_min y
    un diccionario con el soporte de dichos conjuntos.
'''
def genera_y_filtra_candidatos_k1(datos, s_min):
    N = {}
    result = []
    # Recorremos todas las transacciones
    for x in datos:
        used = []
        # Miramos todos los objetos incluidos en la transaccion
        for y in x:
            # Solo contamos un mismo objeto una vez por transaccion, aqui comprobamos si ya lo hemos usado.
            if y in used:
                continue
            # Obtenemos el identificador unico de este conjunto
            ids = get_string_representation([y])
            # Comprobamos si es la primera vez que lo localizamos
            if [y] in result:
                # Si no es la primera vez sumamos uno al valor del soporte que ya teniamos
                N[ids] = N[ids] + 1
            else:
                # Si es la primera vez inicializamos el valor del soporte
                N[ids] = 1
                result.append([y])
                # Ademas añadimos el conjunto a la lista de conjuntos frecuentes
            used.append(y)
    final_res = []
    l_datos = len(datos)
    # Una vez tenemos todos los conjuntos debemos filtrar los que no cumplan el s_min
    for r in result:
        # Obtenemos la representacion unica del conjunto
        ids = get_string_representation(r)
        # Comprobamos si ese conjunto cumple con el s_min
        if (N[ids] / l_datos) >= s_min:
            # Si cumple lo añadimos a la lista final
            final_res.append(r)
        else:
            # Si no cumple lo borramos del diccionario y no lo añadimos a la lista final
            del N[ids]
    return (final_res, N)


'''
    Esta funcion genera los conjuntos candidatos de tamaño k+1 a partir de una lista de conjuntos de
    tamaño k
'''
def genera_candidatos(datos):
    i = 0; j= 0
    result = []
    # Recorremos todas las combinaciones sin repeticion de conjuntos
    while i < (len(datos) - 1):
        # Cojemos uno de los conjuntos
        c1 = datos[i]
        j = i + 1
        while j < len(datos):
            # Cojemos otro conjunto
            c2 = datos[j]
            # Comporbamos si los dos conjuntos se diferencian solo en el ultimo elemento
            if compara_conjuntos(c1, c2):
                # Si se diferencian solo en el ultimo elemento generamos un nuevo conjunto a patir de los dos anteriores
                c3 = copy.copy(c1)
                c3.append(c2[len(c1) - 1])
                # Comprobamos si el conjunto generado es frecuente
                if es_frecuente(datos, c3):
                    c3.sort()
                    # Si es frecuente lo añadimos a la lista
                    result.append(c3)
            j += 1
        i += 1
    return result


'''
    Funcion que filtra los condidatos que hemos obtenido.
    Comprobamos si el candidato supera el s_min.
    Devolvemos la lista de conjuntos frecuentes y el diccionario con
    los soportes de dichos conjuntos.
'''
def filtrar_candidatos(candidatos, datos, s_min):
    N = {}
    result = []
    l_datos = len(datos)
    # Recorremos la lista de condidatos
    for cand in candidatos:
        # Obtnemos su soporte
        soporte = get_soporte(cand, datos)
        # Comprobamos si el soporte ha superado el s_min
        if (soporte / l_datos) >= s_min:
            # Si lo ha superado lo añadimos a la lista de conjuntos y la diccionarios.
            idf = get_string_representation(cand)
            N[idf] = soporte
            result.append(cand)
    return (result, N)


'''
    Devuelve el soporte (en terminos absolutos) de un conjunto
'''
def get_soporte(c1, datos):
    result = 0
    # Recorremos todas las transacciones
    for x in datos:
        cop = True
        # Recorremos todos los elementos del conjunto
        for y in c1:
            # Miramos si el elemento esta en la transaccion
            if y not in x:
                # Si no esta dejamos de mirar el resto de elementos
                cop = False
                break
        # Miramos si tenemos que sumar una aparicion
        if cop:
            result += 1
    return result


'''
    Funcion que nos dice si un conjutno de tamaño k+1 es frecuente en funcion de
    una lista de conjutnos de tamaño k.
    Esto se hace mirando que todos los subconjuntos de ramaño k del conjunto de tamaño k+1
    esten en la lista de conjuntos frecuentes de tamaño k.
'''
def es_frecuente(datos, c1):
    k = len(c1) -1
    n = c1[k]
    '''
        Sabemos que el conjunto c1 se ha formado a partir de conjuntos
        dentro de datos y que el unico valor que varia es el ultimo, asi
        que creamos un conjunto de tamaño k y vamos cambiando elementos
        por el ultimo. Si todos los subconjuntos existen en datos es que
        es frecuente, si alguno no existe, no lo es.
    '''
    for i in range(0, k):
        # Creamos una copia de tamaño k
        aux = copy.copy(c1[:k])
        # cambiamos un elemento del conjunto por el ultimo
        aux[i] = n
        # Ordenamos el conjunto
        aux.sort()
        # Comprobamos si existe
        if aux not in datos:
            # Si no existe es que el conjunto no es frecuente
            return False
    # Si llegamos aqui es que todos los subconjuntos son frecuentes
    return True


'''
    Funcion que devuelve una representacion unica de un conjunto.
    Se obtiene concatenando la representacion de sus elementos separados por comas.
    EJ: [1,2,3] -> '1,2,3'
'''
def get_string_representation(c1):
    return ','.join(str(x) for x in c1)


'''
    Funcion que compara si dos conjuntos se diferencian solo en el ultimo elemento
'''
def compara_conjuntos(c1, c2):
    l = len(c1)
    # Si el conjutno es de tamaño k=1 siempre se cumple
    if l < 2:
        return True
    # Comprobamos si los dos conjutnos son iguales sin incluir el ultimo elemento
    if c1[:l -1 ] == c2[:l -1]:
        # Comprobamos si los conjuntos tienen o no el ultimo elemento igual
        if c1[-1 ] != c2[-1]:
            return True
    return False