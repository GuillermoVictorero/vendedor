import numpy as np#Para manejar arreglos y matrices
import random#generar numero al azar

class NodoCiudad:
    """
    Clase que representa un nodo que contiene la ciudad actual de un recorrido.
    
    Atributos
    ---------
    __padre : NodoCiudad 
        Nodo que representa la ciudad anterior del recorrido
    __hijos : NodoCiudad[]
        Lista de nodos que representan ciudades aun no visitadas
    __id : int
        Numero que identifica a la ciudad en la matriz de distancias

    Metodos
    -------
    getHijos()
        Retorna los hijos
    getId()
        Retorna el id
    getPadre()
        Retorna el padre
    """

    __padre = None
    __hijos = None
    __id = None

    def __init__(self, id, padre, hijos):
        """
        Crea el nodo y sus hijos recursivamente

        Parametros
        ----------
        id : int
            El identificador del Nodo
        Padre : NodoCiudad
            El nodo padre
        hijos : int[]
            Lista de los identificadores de las ciudades por recorrer
        """

        self.__id = id
        self.__padre = padre
        self.__hijos = np.array([])
        for i in range(len(hijos)):
            newHijos = np.delete(hijos,i,0)#Se remueve el nodo de la lista una vez recorrido
            self.__hijos = np.append(self.__hijos, NodoCiudad(hijos[i],self,newHijos))
       
    def getHijos(self):
        """
        Retorna los hijos del nodo
        
        Retorna
        -------
        NodoCiudad[]
            Los hijos del nodo
        """

        return self.__hijos
    def getId(self):
        """
        Retorna el id de la ciudad
        
        Retorna
        -------
        int
            El id de la ciudad
        """

        return self.__id
    def getPadre(self):
        """
        Retorna el padre

        Retorna
        -------
        NodoCiudad
            El padre
        """

        return self.__padre

class ArbolNario:
    """
    Clase que representa un arbol donde cada nodo tiene N hijos. Cada hoja del arbol es un posible recorrido por 
    todas las ciudades.
    
    
    Atributos
    ---------
    __raiz : NodoCiudad 
        Nodo que representa la raiz del arbol y la primera ciudad recorrida

    Metodos
    -------
    getRaiz()
        Retorna la raiz
    """

    __raiz = None

    def __init__(self, id, n):
        """
        Crea la lista de identificadores de las ciudades y el nodo raiz, el cual recursivamente crea el resto del arbol.

        Parametros
        ----------
        id : int
            El identificador de la primera ciudad.
        n : int
            La cantidad de ciudades
        """

        hijos = np.delete(np.arange(n),id,0)#Se remueve el nodo de la lista una vez recorrido
        self.__raiz = NodoCiudad(id,None,hijos)
    def getRaiz(self):
        """
        Retorna la raiz

        Retorna
        -------
        NodoCiudad
            La raiz
        """

        return self.__raiz

def generarMatriz(n):
    """Crea y retorna una matriz con las distancias entre las ciudades.

    Parametros
    ----------
    n : int
        La cantidad de ciudades

    Retorna
    -------
    int[][]
        La matriz con las distancias entre las ciudades.
    """

    dist = np.random.randint(0,50,size=(n,n))#Hasta 50 ya que se va a sumar con la transpuesta duplicando los valores
    dist = dist + dist.T#Para hacer la matriz simetrica
    np.fill_diagonal(dist, 0)#La distancia entre una ciudad y si misma es 0
    return dist

def encontrarMejor(padre, hijos, dist):
    """Encuentra la ciudad mas cercana no recorrida a la ciudad actual.

    Parametros
    ----------
    padre : NodoCiudad
        Nodo que representa la ciudad actual
    hijos : NodoCiudad[]
        Lista de nodos que representan ciudades aun no visitadas
    dist : 
        La matriz con la disntancia entre las ciudades

    Retorna
    -------
    NodoCiudad
        El nodo que representa la ciudad mas cercana.
    """

    #el valor minimo original tiene que ser un valor muy alto
    minimo = 999
    #aqui almacenaremos la posicion del mejor hijo en el arreglo hijos[]
    mejor = 0
    #se van a recorrer todos los hijos que posee el padre
    for i in range(len(hijos)):
        #si la distancia de el hijo actual es menor a la menor distancia que hemos encontrado, ese hijo sera nuestro nuevo mejor hijo
        if dist[hijos[i].getId()][padre] < minimo:
            minimo = dist[hijos[i].getId()][padre]
            mejor = i
    #ahora tenemos que retornar el nodo con el mejor hijo
    return hijos[mejor]

def calcularRecorrido(nodo, dist):
    """Ordena las ciudades recorridas y la distancia entre ellas.

    Parametros
    ----------
    nodo : NodoCiudad
        Nodo que representa la ultima ciudad recorrida
    dist : 
        La matriz con la disntancia entre las ciudades

    Retorna
    -------
    string
        Texto que representa las ciudades recorridas en orden y la distancia entre ellas.
    """

    recorrido = []
    #Obtenemos el recorrido siguiendo la referencia al padre desde el ultimo nodo.
    while(nodo.getPadre() is not None):
        recorrido.append(nodo.getId())
        nodo = nodo.getPadre()
    #El ciclo termina antes de agregar al padre, por lo que se agrega.
    recorrido.append(nodo.getId())
    camino = ""
    #Se recorre el arreglo a la inversa para empezar con la primera ciudad
    for i in range(len(recorrido)-1, 0, -1):
        #Por cada ciudad se calcula la distancia con la siguiente
        camino += "[" + str(recorrido[i]) + "] -> " + str(dist[recorrido[i]][recorrido[i-1]]) + " -> "
    #La ultima ciudad no tiene siguiente
    camino += "[" + str(recorrido[0]) + "]"
    return camino      

def buscarRecorrido(n):
    """Encuentra una solucion al problema del vendedor viajero mediante el algoritmo Hill Climbing.

    Parametros
    ----------
    n : int
        Cantidad de ciudades

    Retorna
    -------
    string
        Texto que representa las ciudades reocrridas en orden y la distancia entre ellas.
    """
    #se llama la función para generar una matriz de tamaño N x N
    dist = generarMatriz(n)
    #se imprime la matriz por pantalla
    print(dist)
    #empezamos con la ciudad 0, abajo hay una linea de codigo que se podría utilizar para en vez escoger una ciudad aleatoria
    #primCiudad = random.randrange(0, n)
    primCiudad = 0
    #se imprime la ciudad por la que se comienza
    print(primCiudad)
    
    arbol = ArbolNario(primCiudad,n)
    nodo = arbol.getRaiz()

    while(nodo.getHijos().size > 0):
        hijos = nodo.getHijos()
        nodo = encontrarMejor(nodo.getId(), hijos, dist)
    return calcularRecorrido(nodo, dist)

print(buscarRecorrido(4))