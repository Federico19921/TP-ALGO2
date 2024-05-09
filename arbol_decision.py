'''
El programa define una clase llamada ArbolBinario que representa un árbol binario. 
Un árbol binario está compuesto por nodos, donde cada nodo tiene un dato y puede tener hasta 
dos hijos: un hijo izquierdo y un hijo derecho.

El programa también define una clase llamada NodoAB que representa un nodo en el árbol binario. 
Cada nodo tiene un dato y puede tener referencias a sus hijos izquierdo y derecho.

La clase ArbolBinario tiene varios métodos que permiten realizar operaciones en el árbol binario, 
como insertar nodos, obtener la altura del árbol y recorrer los nodos en diferentes órdenes.
'''

# **** INICIO BLOQUE DE IMPORTACION DE LIBRERIAS ****
from typing import Any, Optional, TypeVar 
from collections.abc import Callable
from functools import wraps
# **** FIN BLOQUE DE IMPORTACION DE LIBRERIAS ****

# **** INICIO BLOQUE DE DEFINICION DE CLASES ****
T = TypeVar('T')

class NodoAB:
    def __init__(self, dato: T, si: "Optional[ArbolBinario[T]]" = None, sd: "Optional[ArbolBinario[T]]" = None):
        self.dato = dato
        self.si: ArbolBinario[T] = ArbolBinario() if si is None else si 
        self.sd: ArbolBinario[T] = ArbolBinario() if sd is None else sd 
 
    def __str__(self): 
        return str(self.dato)
    
class ArbolBinario:
    """
    Esta clase representa un árbol binario.

    Un árbol binario está compuesto por nodos, donde cada nodo tiene un dato y puede tener hasta dos hijos: 
    un hijo izquierdo (si) y un hijo derecho (sd).

    Los nodos se organizan de manera jerárquica, donde la raíz es el nodo principal y los demás nodos se 
    encuentran en niveles inferiores.

    Los métodos disponibles en esta clase permiten realizar operaciones como insertar nodos, obtener la altura 
    del árbol, recorrer los nodos en diferentes órdenes, entre otros.

    """

    def __init__(self):
        self.raiz: Optional[NodoAB[T]] = None
        
    class _Decoradores:
        @classmethod
        def valida_es_vacio(cls, f: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(f)
            def wrapper(self, *args: Any, **kwargs: Any) -> Any:
                if self.es_vacio():
                    raise TypeError('Arbol Vacio')
                return f(self, *args, **kwargs)
            return wrapper
        
    @staticmethod
    def crear_nodo(dato: T, si: "Optional[ArbolBinario[T]]" = None, sd: "Optional[ArbolBinario[T]]" = None) -> "ArbolBinario[T]":
        """
        Crea un nuevo nodo con el dato especificado y los hijos opcionales.

        Args:
            dato: El dato del nodo.
            si: El hijo izquierdo del nodo (opcional).
            sd: El hijo derecho del nodo (opcional).

        Returns:
            Un nuevo árbol binario con el nodo creado.

        """
        t = ArbolBinario()
        t.raiz = NodoAB(dato, si, sd)
        return t

    def es_vacio(self) -> bool: 
        """
        Verifica si el árbol está vacío.

        Returns:
            True si el árbol está vacío, False de lo contrario.

        """
        return self.raiz is None
    
    @_Decoradores.valida_es_vacio
    def si(self) -> "ArbolBinario[T]":
        """
        Devuelve el hijo izquierdo del árbol.

        Returns:
            El hijo izquierdo del árbol.

        Raises:
            TypeError: Si el árbol está vacío.

        """
        assert self.raiz is not None
        return self.raiz.si
    
    @_Decoradores.valida_es_vacio
    def sd(self) -> "ArbolBinario[T]":
        """
        Devuelve el hijo derecho del árbol.

        Returns:
            El hijo derecho del árbol.

        Raises: 
            AssertionError: Si el árbol está vacío.

        """
        assert self.raiz is not None # verificar que el arbol no esté vacio si no lanzar excepcion AssertionError
        return self.raiz.sd
    
    def es_hoja(self) -> bool:
        """
        Verifica si el árbol es una hoja.

        Returns:
            True si el árbol es una hoja, False de lo contrario.

        """
        return not self.es_vacio() and self.si().es_vacio() and self.sd().es_vacio()

    @_Decoradores.valida_es_vacio
    def dato(self) -> T:
        """
        Devuelve el dato del nodo raíz del árbol.

        Returns:
            El dato del nodo raíz del árbol.

        Raises:
            TypeError: Si el árbol está vacío.

        """
        assert self.raiz is not None
        return self.raiz.dato
    
    @_Decoradores.valida_es_vacio
    def insertar_si(self, si: "ArbolBinario[T]"):
        """
        Inserta un árbol como hijo izquierdo del árbol actual.

        Args:
            si: El árbol a insertar como hijo izquierdo.

        Raises:
            TypeError: Si el árbol está vacío.

        """
        assert self.raiz is not None
        self.raiz.si = si

    @_Decoradores.valida_es_vacio
    def insertar_sd(self, sd: "ArbolBinario[T]"):
        """
        Inserta un árbol como hijo derecho del árbol actual.

        Args:
            sd: El árbol a insertar como hijo derecho.

        Raises:
            TypeError: Si el árbol está vacío.

        """
        assert self.raiz is not None
        self.raiz.sd = sd

    def set_raiz(self, nodo: NodoAB[T]):
        """
        Establece el nodo especificado como raíz del árbol.

        Args:
            nodo: El nodo a establecer como raíz.

        """
        self.raiz = nodo
        
    def altura(self) -> int:
        """
        Calcula la altura del árbol.

        Returns:
            La altura del árbol.

        """
        if self.es_vacio():
            return 0
        else:
            return 1 + max(self.si().altura(), self.sd().altura())
        
    def __len__(self) -> int:
        """
        Calcula la cantidad de nodos en el árbol.

        Returns:
            La cantidad de nodos en el árbol.

        """
        if self.es_vacio():
            return 0
        else:
            return 1 + len(self.si()) + len(self.sd())
    
    def __str__(self):
        """
        Devuelve una representación en cadena del árbol.

        Returns:
            Una representación en cadena del árbol.

        """
        def mostrar(t: ArbolBinario[T], nivel: int):
            tab = '.' * 4
            indent = tab * nivel
            if t.es_vacio():
                return indent + 'AV\n'
            else:
                out = indent + str(t.dato()) + '\n'
                out += mostrar(t.si(), nivel + 1)
                out += mostrar(t.sd(), nivel + 1)
                return out
            
        return mostrar(self, 0)

    def inorder(self) -> list[T]:
        """
        Realiza un recorrido inorder del árbol.

        Returns:
            Una lista con los datos de los nodos en el recorrido inorder.

        """
        if self.es_vacio():
            return []
        else:
            return self.si().inorder() + [self.dato()] + self.sd().inorder()
    
    def inorder_tail(self) -> list[T]:
        """
        Realiza un recorrido inorder del árbol utilizando una implementación tail recursive.

        Returns:
            Una lista con los datos de los nodos en el recorrido inorder.

        """
        def inorder_tail_helper(node: "ArbolBinario[T]", acc: list[T]) -> list[T]:
            if node.es_vacio():
                return acc
            else:
                acc = inorder_tail_helper(node.si(), acc)
                acc.append(node.dato())
                return inorder_tail_helper(node.sd(), acc)

        return inorder_tail_helper(self, [])

    def preorder(self) -> list[T]: 
        """
        Realiza un recorrido preorder del árbol.

        Returns:
            Una lista con los datos de los nodos en el recorrido preorder.

        """
        if self.es_vacio():
            return []
        else:
            return [self.dato()] + self.si().preorder() + self.sd().preorder()

    def posorder(self) -> list[T]: 
        """
        Realiza un recorrido posorder del árbol.

        Returns:
            Una lista con los datos de los nodos en el recorrido posorder.

        """
        if self.es_vacio():
            return []
        else:
            return self.si().posorder() + self.sd().posorder() + [self.dato()]

    def bfs(self) -> list[T]: 
        """
        Realiza un recorrido BFS (Breadth-First Search) del árbol.

        Returns:
            Una lista con los datos de los nodos en el recorrido BFS.

        """
        if self.es_vacio():
            return []

        queue = [self]
        result = []

        while queue:
            node = queue.pop(0)
            result.append(node.dato())

            if not node.si().es_vacio():
                queue.append(node.si())
            if not node.sd().es_vacio():
                queue.append(node.sd())

        return result

    def nivel(self, x: T) -> int: 
            """
            Devuelve el nivel en el que se encuentra el nodo con el dato especificado.

            Args:
                x: El dato del nodo a buscar.

            Returns:
                El nivel en el que se encuentra el nodo con el dato especificado.

            """
            if self.es_vacio(): # Si el árbol está vacío
                return -1 # Devolver -1 porque el dato no se encuentra en el árbol

            queue = [(self, 0)] # Inicializar la cola con el nodo raíz y el nivel 0

            while queue: # Mientras la cola no esté vacía
                node, level = queue.pop(0) # Obtener el nodo y el nivel actual

                if node.dato() == x: # Si el dato del nodo es igual al dato especificado
                    return level # Devolver el nivel actual

                if not node.si().es_vacio(): # Si el hijo izquierdo no es vacío
                    queue.append((node.si(), level + 1)) # Agregar el hijo izquierdo a la cola
                if not node.sd().es_vacio(): # Si el hijo derecho no es vacío
                    queue.append((node.sd(), level + 1)) # Agregar el hijo derecho a la cola

            return -1 # El dato no se encuentra en el árbol por lo que se devuelve -1. 
                      # -1 es un valor inválido para el nivel 
                      # Usmaos -1 para indicar que el dato no se encuentra en el árbol.

    def copy(self) -> "ArbolBinario[T]": 
        """
        Crea una copia del árbol.

        Returns:
            Una copia del árbol.

        """
        if self.es_vacio():  # Si el árbol está vacío
            return ArbolBinario()  # Devolver un árbol binario vacío

        # Crear una nueva instancia de ArbolBinario con la raíz del árbol actual
        arbol_copia = ArbolBinario(self.raiz.dato)

        # Copiar los subárboles izquierdo y derecho recursivamente
        arbol_copia.insertar_si(self.si().copy())
        arbol_copia.insertar_sd(self.sd().copy())

        return arbol_copia  # Devolver la copia del árbol

    def espejo(self) -> "ArbolBinario[T]": 
        """
        Crea un árbol espejo del árbol actual.

        Returns:
            Un árbol espejo del árbol actual.

        """
        if self.es_vacio():  # Si el árbol está vacío
            return ArbolBinario()  # Devolver un árbol binario vacío

        # Crear una nueva instancia de ArbolBinario con la raíz del árbol actual
        arbol_espejo = ArbolBinario(self.raiz.dato)

        # Crear el árbol espejo recursivamente intercambiando los subárboles izquierdo y derecho
        arbol_espejo.insertar_si(self.sd().espejo())
        arbol_espejo.insertar_sd(self.si().espejo())

        return arbol_espejo  # Devolver el árbol espejo
        
    def sin_hojas(self): 
        """
        Elimina todas las hojas del árbol.

        """
        if self.es_vacio():  # Si el árbol está vacío
            return

        if self.es_hoja():  # Si el árbol es una hoja
            self.set_raiz(None)  # Eliminar la raíz del árbol
            return

        # Eliminar las hojas de los subárboles izquierdo y derecho recursivamente
        if self.si().es_hoja():
            self.insertar_si(None)
        else:
            self.si().sin_hojas()

        if self.sd().es_hoja():
            self.insertar_sd(None)
        else:
            self.sd().sin_hojas()
