# -*- coding: utf-8 -*-

__author__ = 'Joaquin'

import numpy as np


def read_data(filename):
    f = open(filename, 'r', encoding='utf-8')
    line = f.readline()
    result = []
    while line:
        spll = line.split(' ')
        nnl = []
        for sp in spll:
            try:
                nun = int(sp)
                nnl.append(nun)
            except ValueError:
                None
        if len(nnl) > 0:
            result.append(nnl)
        line = f.readline()
    return result
