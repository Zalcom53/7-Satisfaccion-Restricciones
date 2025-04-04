#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py



"""

import csps
import time


class Nreinas(csps.ProblemaCSP):
    """
    El problema de las n-reinas.

    Esta clase permite instanciar un problema de n reinas, sea n un
    numero entero mayor a 3 (para 3 y para 2 no existe solución al
    problema).

    """

    def __init__(self, n=4):
        """
        Inicializa las n--reinas para n reinas, por lo que:
        """
        self.X = set(range(1, n + 1))
        self.D = {x: set(range(1, n + 1)) for x in self.X}
        self.N = {x: self.X.difference({x}) for x in self.X}   

    def restriccion_binaria(self, x_i, v_i, x_j, v_j):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        """
        return v_i != v_j and abs(v_i - v_j) != abs(x_i - x_j)

def prueba_reinas(n, consistencia=1, max_iter=100):
    
    problema = Nreinas(n)

    print("\n" + "-" * 20 + f"\nPara {n} reinas")
    print(f"Usando grafo de restricciones con consistencia {consistencia}")
    print("-" * 20)
    
    t0 = time.time()    
    asig = csps.asignacion_completa(problema, consistencia=consistencia, verbose=False)
    t_lapso = time.time() - t0
    
    print("Se asignaron las siguientes variables:")
    print([asig[i] for i in range(1, n + 1)])
    print("Se realizaron {} backtrackings".format(problema.backtracking))
    print("Se tardó {:.2f} segundos".format(t_lapso))


if __name__ == "__main__":
    
    N = 101
    N_ITER = 10_000
    #prueba_reinas(N, 0, N_ITER)
    prueba_reinas(N, 1, N_ITER)
    prueba_reinas(N, 2, N_ITER)

