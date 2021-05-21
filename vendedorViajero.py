from constants import (MIN_DISTANCIA, MAX_DISTANCIA, VALOR_GRANDE, SEC_A_MICRO, TAM_MUESTRA, MIN_CIUDAD, FALLO_CIUDAD, PASO_CIUDAD)
import numpy as np#Para manejar arreglos y matrices
import random#generar numero al azar
import timeit#Para revisar la velocidad del algoritmo
import sys#Leer linea de comando

class NodoCiudad:
    """
    Clase que representa un nodo que contiene la ciudad actual de un recorrido
    
    Atributos
    ---------
    1. __padre : NodoCiudad 
        - Nodo que representa la ciudad anterior del recorrido
    2. __hijos : NodoCiudad[]
        - Lista de nodos que representan ciudades aun no visitadas
    3. __id : int
        - Numero que identifica a la ciudad en la matriz de distancias

    Metodos
    -------
    1. getHijos() : NodoCiudad[]
        - Retorna los hijos
    2. getId() : int
        - Retorna el id
    3. getPadre() : NodoCiudad 
        - Retorna el padre
    """

    __padre = None
    __hijos = None
    __id = None

    def __init__(self, id, padre, hijos):
        """
        Crea el nodo y sus hijos recursivamente

        Parametros
        ----------
        1. id : int
            - El identificador del Nodo
        2. Padre : NodoCiudad
            - El nodo padre
        3. hijos : int[]
            - Lista de los identificadores de las ciudades por recorrer
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
        1. NodoCiudad[]
            - Los hijos del nodo
        """

        return self.__hijos
    def getId(self):
        """
        Retorna el id de la ciudad
        
        Retorna
        -------
        1. int
            - El id de la ciudad
        """

        return self.__id
    def getPadre(self):
        """
        Retorna el padre

        Retorna
        -------
        1. NodoCiudad
            - El padre
        """

        return self.__padre

class ArbolNario:
    """
    Clase que representa un arbol donde cada nodo tiene N hijos. Cada hoja del arbol es un posible recorrido por 
    todas las ciudades
    
    Atributos
    ---------
    1. __raiz : NodoCiudad 
        - Nodo que representa la raiz del arbol y la primera ciudad recorrida

    Metodos
    -------
    1. getRaiz() : NodoCiudad 
        - Retorna la raiz
    """

    __raiz = None

    def __init__(self, id, n):
        """
        Crea la lista de identificadores de las ciudades y el nodo raiz, el cual recursivamente crea el resto del arbol

        Parametros
        ----------
        1. id : int
            - El identificador de la primera ciudad
        2. n : int
            - La cantidad de ciudades
        """

        hijos = np.delete(np.arange(n),id,0)#Se remueve el nodo de la lista una vez recorrido
        self.__raiz = NodoCiudad(id,None,hijos)
    def getRaiz(self):
        """
        Retorna la raiz

        Retorna
        -------
        1. NodoCiudad
            - La raiz
        """

        return self.__raiz

def generarMatriz(n):
    """Crea y retorna una matriz con las distancias entre las ciudades

    Parametros
    ----------
    1. n : int
        - La cantidad de ciudades

    Retorna
    -------
    1. int[][]
        - La matriz con las distancias entre las ciudades
    """

    dist = np.random.randint(MIN_DISTANCIA,MAX_DISTANCIA/2,size=(n,n))#Hasta 50 ya que se va a sumar con la transpuesta duplicando los valores
    dist = dist + dist.T#Para hacer la matriz simetrica
    np.fill_diagonal(dist, 0)#La distancia entre una ciudad y si misma es 0
    return dist

def encontrarMejor(padre, hijos, dist):
    """Encuentra la ciudad mas cercana no recorrida a la ciudad actual

    Parametros
    ----------
    1. padre : NodoCiudad
        - Nodo que representa la ciudad actual
    2. hijos : NodoCiudad[]
        - Lista de nodos que representan ciudades aun no visitadas
    3. dist : 
        - La matriz con la distancia entre las ciudades

    Retorna
    -------
    1. NodoCiudad
        - El nodo que representa la ciudad mas cercana
    """

    #el valor minimo original tiene que ser un valor muy alto
    minimo = VALOR_GRANDE
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

def obtenerRecorrido(nodo, dist):
    """Ordena las ciudades recorridas y la distancia entre ellas.

    Parametros
    ----------
    1. nodo : NodoCiudad
        - Nodo que representa la ultima ciudad recorrida
    2. dist : 
        - La matriz con la distancia entre las ciudades

    Retorna
    -------
    1. string
        - Texto que representa las ciudades recorridas en orden y la distancia entre ellas
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
        camino += "[C" + str(recorrido[i]) + "] -> " + str(dist[recorrido[i]][recorrido[i-1]]) + " -> "
    #La ultima ciudad no tiene siguiente
    camino += "[C" + str(recorrido[0]) + "]"
    return camino      

def buscarRecorrido(n):
    """Encuentra una solucion al problema del vendedor viajero mediante el algoritmo Hill Climbing

    Parametros
    ----------
    1. n : int
        - Cantidad de ciudades

    Retorna
    -------
    1. string
        - Texto que representa las ciudades recorridas en orden y la distancia entre ellas
    2. float
        - Microsegundos que demoro la ejecucion del algoritmo
    """
    #se llama la función para generar una matriz de tamaño N x N
    dist = generarMatriz(n)
    #empezamos con la ciudad 0
    primCiudad = 0

    arbol = ArbolNario(primCiudad,n)
    nodo = arbol.getRaiz()

    startTime = timeit.default_timer()#Comienzo del algoritmo Hill-Climbing
    while(nodo.getHijos().size > 0):
        hijos = nodo.getHijos()
        nodo = encontrarMejor(nodo.getId(), hijos, dist) 
    exeTime = round((timeit.default_timer() - startTime)*SEC_A_MICRO,1)
    return obtenerRecorrido(nodo, dist), exeTime

if(len(sys.argv) > 1 and sys.argv[1].isnumeric()):#Revisar un numero de ciudades determinado
    ciudades = int(sys.argv[1])

    print("Solucion encontrada, comenzando en ciudad [C0].")
    print("Numero de ciudades:", ciudades)
    recorrido, tiempo = buscarRecorrido(ciudades)
    print(recorrido)
    print("Tiempo total:",tiempo,"[µs]")

else:#Tiempo promedio para varios numeros de ciudades
    ciudadesTiempo = []
    contador = 0
    muestra = TAM_MUESTRA
    for i in range(MIN_CIUDAD, FALLO_CIUDAD, PASO_CIUDAD):
        ciudadesTiempo.append([i,0])#Se agrega la ciudad
        for j in range(0,muestra):
            recorrido, tiempo = buscarRecorrido(i)
            ciudadesTiempo[contador][1] += tiempo#Se suma el tiempo a la ciudad correpondiente
        ciudadesTiempo[contador][1] /= muestra#Se divide para obtener el promedio
        contador += 1
    print(ciudadesTiempo)