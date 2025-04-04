"""
sudoku.py
------------

Los Sudokus son unos juegos de origen Japones. El juego tiene un
tablero de 9 x 9 casillas.  En cada casilla se debe asignar un número
1, 2, 3, 4, 5, 6, 7, 8 o 9.

La idea principal de juego es establecer los valores de los números en
las casillas no asignadas anteriormente si se considera que:

    a) Las casillas horizontales deben tener números diferentes entre si
    b) Las casillas verticales deben tener números diferentes entre si
    c) Las casillas que pertenecen al mismo grupo deben tener números
       diferentes entre si.

Sea (r1, c1) el renglon y la columna de una casilla y (r2, c2) el
renglon y la columna de otra casilla, se dice que las casillas
pertenecen al mismo grupo si y solo si r1//3 == r2//3 y c1//3 == c2//3
donde // es la división entera (por ejemplo 4//3 = 1 o 8//3 = 2).  Esto
aplica si se considera 0 como la primer posición.

Para más información sobre sudokus, pueden googlearlo, buscarlos en
wikipedia o comprar un librito de sudokus.

Un Sudoku se inicializa como una lista de 81 valores donde los valores
se encuentran de la manera siguiente:

    0   1   2 |  3   4   5 |  6   7   8
    9  10  11 | 12  13  14 | 15  16  17
   18  19  20 | 21  22  23 | 24  25  26
   -----------+------------+------------
   27  28  29 | 30  31  32 | 33  34  35
   36  37  38 | 39  ...

hasta llegar a la posición 81.

Los valores que puede tener la lista son del 0 al 9. Si tiene un 0
entonces es que el valor es desconocido.

"""


import csps
import time


class Sudoku(csps.ProblemaCSP):
    def __init__(self, pos_ini):
        self.X = set(range(81))
        self.D = {i: set([val]) if val > 0 else 
                     set(range(1, 10)) for (i, val) in enumerate(pos_ini)}

        self.N = {
            i: set(
                p for p in range(81) if (
                p != i and 
                ( p//9 == i//9 or p%9 == i%9 or 
                  (p//27 == i//27 and p%9//3 == i%9//3))
                )
            ) 
            for i in range(81)
        }

    def restriccion_binaria(self, xi, vi, xj, vj):
        return vi != vj
         

def imprime_sdk(s):
    """
    Imprime un sudoku en pantalla en forma más o menos graciosa. Esta
    función solo sirve para la tarea y para la revisión de la
    tarea. No modificarla por ningun motivo.

    """
    rayita = '\n-------------+----------------+---------------\n'
    c = ''
    for i in range(9):
        c += ' '.join(str(s[9 * i + j]) +
                      ("  |  " if j % 3 == 2 and j < 7 else "   ")
                      for j in range(9))
        c += rayita if i % 3 == 2 and i < 7 else '\n'
    print(c)


if __name__ == "__main__":
    # =========================================================================
    # Una forma de verificar si el código que escribiste es correcto
    # es verificando que la solución sea satisfactoria para estos dos
    # sudokus.
    # =========================================================================

    s1 = [0, 0, 3, 0, 2, 0, 6, 0, 0,
          9, 0, 0, 3, 0, 5, 0, 0, 1,
          0, 0, 1, 8, 0, 6, 4, 0, 0,
          0, 0, 8, 1, 0, 2, 9, 0, 0,
          7, 0, 0, 0, 0, 0, 0, 0, 8,
          0, 0, 6, 7, 0, 8, 2, 0, 0,
          0, 0, 2, 6, 0, 9, 5, 0, 0,
          8, 0, 0, 2, 0, 3, 0, 0, 9,
          0, 0, 5, 0, 1, 0, 3, 0, 0]

    imprime_sdk(s1)
    print("Solucionando un Sudoku dificil")
    sudoku1 = Sudoku(s1)
    t0 = time.time()
    sol1 = csps.asignacion_completa(sudoku1)
    t_lapso = time.time() - t0
    print(f"Tomo {t_lapso:.5f} segundos")
    print(f"Se realizaron {sudoku1.backtracking} backtrackings")
    imprime_sdk([sol1[i] for i in range(81)])

    print("\n\nY otro tambien dificil")
    s2 = [4, 0, 0, 0, 0, 0, 8, 0, 5,
          0, 3, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 7, 0, 0, 0, 0, 0,
          0, 2, 0, 0, 0, 0, 0, 6, 0,
          0, 0, 0, 0, 8, 0, 4, 0, 0,
          0, 0, 0, 0, 1, 0, 0, 0, 0,
          0, 0, 0, 6, 0, 3, 0, 7, 0,
          5, 0, 0, 2, 0, 0, 0, 0, 0,
          1, 0, 4, 0, 0, 0, 0, 0, 0]

    imprime_sdk(s2)
    sudoku2 = Sudoku(s2)
    t0 = time.time()
    sol2 = csps.asignacion_completa(sudoku2)
    t_lapso = time.time() - t0
    print(f"Tomo {t_lapso:.5f} segundos")
    print(f"Se realizaron {sudoku1.backtracking} backtrackings")
    imprime_sdk([sol2[i] for i in range(81)])
