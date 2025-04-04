"""
Implementación de los algoritmos más clásicos para el problema
de satisfacción de restricciones. Se define formalmente el
problema de satisfacción de restricciones y se desarrollan los
algoritmos para solucionar el problema por búsqueda.

En particular se implementan los algoritmos de forward checking y
el de arco consistencia. Así como el algoritmo de minimos conflictos.

"""

from abc import ABC, abstractmethod
from random import choice
from collections import deque


class ProblemaCSP(ABC):
    """
    Clase abstracta para hacer un grafo de restricción

    El grafo de restricción se representa por los siguientes atributos:

    X (variables): {x1, x2, x3, ...} Un conjunto con el nombre de las variables
    
    D (Dominio): Un diccionario cuyas llaves son las variables (vertices) del grafo de restricción, y cuyo valor es un conjunto con los valores que puede tomar.

    N (Vecinos) Un diccionario cuyas llaves son las variables (vertices) del grafo de restricción, y cuyo valor es un conjunto con las variables con las que tiene restricciones binarias.

    El grafo de restricción se define por los siguientes métodos:
    __init__: Inicializa las propiedades del grafo de restricción
    
    restriccion_binaria: Verifica si se cumple la restricción binaria entre las variables xi y xj cuando a estas se le asignan los valores vi y vj respectivamente.

    Si es necesario se pueden agregar restricciones globales, pero ya no podrñan usarse las técnicas para grafos de restricciones.
    
    """

    @abstractmethod
    def __init__(self):
        """
        Inicializa las propiedades del grafo de restriccón
        
        X, D y N son propiedades obligatorias

        """
        raise NotImplementedError("Método a implementar")

    @abstractmethod
    def restriccion_binaria(self, x_i, v_i, x_j, v_j):
        """
        Verifica si se cumple la restricción binaria entre las variables xi y xj cuando a estas se le asignan los valores vi y vj respectivamente.
        
        @param x_i: La variable xi
        @param v_i: El valor vi
        @param x_j: La variable xj
        @param v_j: El valor vj
        
        @return: True si la restricción se cumple, False en otro caso
        
        """
        raise NotImplementedError("Método a implementar")


def asignacion_grafo_restriccion(csp, asignacion={}, consist=1, traza=False):
    """
    Asigación de una solución al grafo de restriccion si existe
    por búsqueda primero en profundidad.

    @param grafo: Un objeto tipo ProblemaCSP
    @param asignacion: Un diccionario con una asignación parcial o total
    @param consist: Un valor 0, 1 o 2 para grado de consistencia
    @param traza: Si True muestra el proceso de asignación

    @return: Una asignación completa (diccionario con variable:valor)
             o None si la asignación no es posible.

    """

    #  Checa si la asignación completa y devuelve el resultado de ser el caso
    if set(asignacion.keys()) == csp.X:
        return asignacion.copy()

    # Selección de variables, el código viene más adelante
    var = selecciona_variable(csp, asignacion)

    # Los valores se ordenan antes de probarlos
    for val in ordena_valores(csp, asignacion, var):

        # La funcion consistencia reduce los dominios de csp
        # esto es posible porque csp es mutable al ser un objeto ProblemaCSP
        # Si la función de consistencia regresa None si no hay asignación posible
        dominio_reducido = consistencia(csp, asignacion, var, val, consist)

        if dominio_reducido is None:
            csp.backtracking += 1
            continue
        else:
            # Se realiza la asignación de esta variable
            asignacion[var] = val

            # Solo para efectos de impresión
            if traza:
                print(((len(asignacion) - 1) * '\t') + f"{var} = {val}")

            # Se manda llamar en forma recursiva (búsqueda en profundidad)
            apn = asignacion_grafo_restriccion(csp, asignacion, consist, traza)

            # Restaura el dominio
            for valor in dominio_reducido:
                csp.D[valor].update(dominio_reducido[valor])

            # Si la asignación es completa revuelve el resultado
            if apn is not None:
                return apn
            del asignacion[var]
    csp.backtracking += 1
    return None

def asignacion_completa(csp, consistencia=1, verbose=False):
    """
    Asignación de una solución al grafo de restricción si existe
    por búsqueda primero en profundidad. Función burrito.
    
    @param csp: Un objeto tipo ProblemaCSP
    @param consist: Un valor 0, 1 o 2 para grado de consistencia
    @param verbose: Si True muestra el proceso de asignación

    @return: Una asignación completa (diccionario con variable:valor)
             o None si la asignación no es posible.
    
    """
    csp.backtracking = 0
    asign = asignacion_grafo_restriccion(
        csp, asignacion={}, consist=consistencia, traza=verbose
    )
    if verbose:
        print(f"Backtrackings: {csp.backtracking}")
        if asign is None:
            print("No hay solución")
        else:
            print("Asignación completa:")
            for var, val in asign.items():
                print(f"{var} = {val}")
    return asign
    

def selecciona_variable(csp, asg):
    """
    Selecciona la variable a explorar

    @param csp: objeto ProblemaCSP
    @param asg: Un diccionario con una asignación parcial

    @return: Una variable de csp.dominio.keys()

    """
    # Si no hay variables en la asignación parcial, se usa el grado heurístico
    if not asg:
        return max(csp.X, key=lambda x: len(csp.N[x]))
    
    # Si hay variables, entonces se selecciona la variable con el dominio más pequeño
    return min(
        [x for x in csp.X if x not in asg],
        key=lambda x: len(csp.D[x])
    )


def ordena_valores(csp, asg, x_i):
    """
    Ordena los valores del dominio de una variable de acuerdo
    a los que restringen menos los dominios de las variables
    vecinas. Para ser usada dentro de la función
    asignacion_grafo_restriccion.

    @param csp: objeto ProblemaCSP
    @param asg: un diccionario con una asignación parcial
    @param x_i: La variable con los valores a ordenar

    @return: Un iterable con los valores de csp.D[x_i] ordenados

    """
    def conflictos(v_i):
        return sum(
            csp.restriccion_binaria(x_i, v_i, x_j, v_j)
            for x_j in csp.N[x_i] if x_j not in asg
            for v_j in csp.D[x_j]
        )
    return sorted(list(csp.D[x_i]), key=conflictos, reverse=True)


def consistencia(csp, asg, x_i, v_i, consistencia):
    """
    Calcula la consistencia y reduce el dominio de las variables, de
    acuerdo al grado de la consistencia. Si la consistencia es:

        0: Reduce el dominio de la variable en cuestión
        1: Reduce el dominio de la variable en cuestion
           y las variables vecinas que tengan valores que
           se reduzcan con ella.
        2: Reduce los valores de todas las variables que tengan
           como vecino una variable que redujo su valor. Para
           esto se debe usar el algoritmo AC-3.

    @param csp: objeto tipo ProblemaCSP
    @param asg: un diccionario con una asignación parcial
    @param x_i: La variable a ordenar los valores
    @param v_i: Un valor que puede tomar x_i

    @return: Un diccionario con el dominio que se redujo (csp.D de modifica)
                o None si no hay solución (csp.D entonces no se modifica).

    """
    
    dom_red = {}
    
    # Consistencia 0, la de base
    for (x_j, v_j) in asg.items():
        if x_j in csp.N[x_i] and not csp.restriccion_binaria(x_i, v_i, x_j, v_j):
            return None
    dom_red[x_i] = {v for v in csp.D[x_i] if v != v_i}
    csp.D[x_i] = {v_i}

    # Consistencia 1, revisamos si podemos reducir el dominio de las variables vecinas
    if consistencia >= 1:
        for x_j in csp.N[x_i]:
            if x_j not in asg:
                val_set = set([])
                for v_j in csp.D[x_j]:
                    if not csp.restriccion_binaria(x_i, v_i, x_j, v_j):
                        val_set.add(v_j)
                if val_set:
                    dom_red[x_j] = val_set.copy()
                    csp.D[x_j].difference_update(val_set)
                if not csp.D[x_j]:
                    for x in dom_red:
                        csp.D[x].update(dom_red[x])
                    return None
    
    # Consistencia 2, ahora vemos los vecionos de los vecinos
    if consistencia == 2:    
        pendientes = {
            (x_i, x_j) for x_i in csp.X if x_i not in asg 
                       for x_j in csp.N[x_i] if x_j not in asg
        }
        while pendientes:
            x_a, x_b = pendientes.pop()
            val_set = set([])
            for v_a in csp.D[x_a]:
                for v_b in csp.D[x_b]:
                    if csp.restriccion_binaria(x_a, v_a, x_b, v_b):
                        break
                else:
                    val_set.add(v_a)
            if val_set:
                if x_a not in dom_red:
                    dom_red[x_a] = set({})
                dom_red[x_a].update(val_set)
                csp.D[x_a].difference_update(val_set)
                if not csp.D[x_a]:
                    for x in dom_red:
                        csp.D[x].update(dom_red[x])
                    return None
                pendientes.update(
                    {(x_a, x_j) for x_j in csp.N[x_a] if x_j not in asg}
                )
                
    return dom_red

def minimos_conflictos(csp, max_iter=10_000, paciencia=5):
    """
    Algoritmo de minimos conflictos para resolver el problema de
    satisfacción de restricciones. Este algoritmo es una heurística
    que intenta minimizar los conflictos en cada paso.

    @param csp: objeto tipo ProblemaCSP
    @param max_iter: número máximo de iteraciones
    @param paciencia: número de iteraciones sin mejora antes de reiniciar

    @return: Un diccionario con la asignación completa o None si no se encontró solución.

    """
    # Inicializa la asignación aleatoriamente
    asign = {x: choice(list(csp.D[x])) for x in csp.X}
    min_conflictos = 1e10

    for _ in range(max_iter):
        conflictos = {
            x: sum(
                not csp.restriccion_binaria(x, asign[x], x_j, asign[x_j])
                for x_j in csp.N[x]
            )
            for x in csp.X
        }
        actual = sum(conflictos.values())
        
        if actual == 0:
            return asign
        elif actual < min_conflictos:
            min_conflictos = actual
            repeticiones = 0
        elif actual == min_conflictos:
            repeticiones += 1
            if repeticiones > paciencia:
                asign = {x: choice(list(csp.D[x])) for x in csp.X}
                min_conflictos = 1e10
                repeticiones = 0
                continue
        
        x = choice([x for x in conflictos.keys() if conflictos[x] > 0])
        v = min(
            csp.D[x], 
            key=lambda v: sum(
                not csp.restriccion_binaria(x, v, x_j, asign[x_j])
                for x_j in csp.N[x]
            )
        )
        asign[x] = v
    return None