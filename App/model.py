"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from math import radians, cos, sin, asin, sqrt
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landing_points': None,
                    'connections': None,
                    'points_values': None,
                    'pais_values': None,
                    'paths': None,
                    'components': None
                    }

        analyzer['landing_points'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIds)
        analyzer['points_values'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        analyzer['pais_values'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        
        return analyzer
    
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Construccion de modelos
def addpointtable(analyzer, point):
    value=pointvalue(point)
    m.put(analyzer["points_values"], point["landing_point_id"],value)

def pointvalue(point):
    value = {'id': None, "name": None, "latitude":None, "longitude":None}
    value['id'] = point["landing_point_id"]
    value['name'] = point["name"]
    value["latitude"]=point["latitude"]
    value["longitude"]=point["longitude"]
    return value

def addpaistable(analyzer, pais):
    value=paisvalue(pais, analyzer)
    m.put(analyzer["pais_values"], pais["CountryName"], value)

def paisvalue(pais, analyzer):
    value = {'CapitalName': None, "capitalvertex": None, "Population":None, "Internet_users":None}
    value["CapitalName"] = pais["CapitalName"]
    value["capitalvertex"]=addpaisvertex(pais, analyzer)
    value["Population"] = pais["Population"]
    value["Internet_users"] = pais["Internet users"]
    return value

def addpaisvertex(pais, analyzer):
    points=m.valueSet(analyzer['points_values'])
    capital=pais["CapitalName"]
    vertex=0
    for point in lt.iterator(points):
        ciudad=point["name"].split(",")[0]
        ciudad=ciudad.strip()
        if ciudad==capital:
            vertex=point["id"]
            return vertex

def addLandConnection(analyzer, lastpoint, point, cable):
    try:
        origin = formatpoint(lastpoint, cable)
        destination = formatpoint(point, cable)
        long1=float(m.get(analyzer["points_values"], lastpoint)["value"]["longitude"])
        lat1=float(m.get(analyzer["points_values"], lastpoint)["value"]["latitude"])
        long2=float(m.get(analyzer["points_values"], point)["value"]["longitude"])
        lat2=float(m.get(analyzer["points_values"], point)["value"]["latitude"])
        distance = haversine(long1, lat1, long2, lat2)
        #añadir vertice
        addpoint(analyzer, origin)
        addpoint(analyzer, destination)
        #añadir arcos
        addconnection(analyzer, origin, destination, distance)
        #lista cables
        addCableLand(analyzer, lastpoint, cable)
        addCableLand(analyzer, point, cable)
        return analyzer
    except Exception as exp:
        error.reraise(exp, "model:addpointconnection")
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def addpoint(analyzer, point):
    try:
        if not gr.containsVertex(analyzer["connections"], point):
            gr.insertVertex(analyzer["connections"], point)
        return analyzer
    except Exception as exp:
        error.reraise(exp, "model:addpoint")

def addCableLand(analyzer, point, cable):
    entry = m.get(analyzer["landing_points"], point)
    if entry is None:
        lstcables= lt.newList(cmpfunction=comparecables)
        lt.addLast(lstcables, cable["cable_name"])
        m.put(analyzer["landing_points"], point, lstcables)
    else:
            lstcables= entry["value"]
            info = cable["cable_name"]
            if not lt.isPresent(lstcables, info):
                lt.addLast(lstcables, info)
def addCableConnections(analyzer):
    lstpoints=m.keySet(analyzer["landing_points"])
    for key in lt.iterator(lstpoints):
        lstcables = m.get(analyzer["landing_points"], key)["value"]
        prevout=None
        for cable in lt.iterator(lstcables):
            cable = key+ "-"+ cable
            if prevout is not None:
                addconnection(analyzer, prevout, cable, 0)
                addconnection(analyzer, cable, prevout, 0)
            prevout = cable
    None

def addconnection(analyzer, origin, destination, distance):
    edge = gr.getEdge(analyzer["connections"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["connections"], origin, destination, distance)
    return analyzer

def printpaises(analyzer):
    paises=m.valueSet(analyzer["pais_values"])
    for pais in lt.iterator(paises):
        #print(pais)
        None
# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

def vertexComponents(analyzer, verta, vertb):
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    numero=scc.connectedComponents(analyzer['components'])
    try:
        connect=scc.stronglyConnected(analyzer['components'], verta, vertb)
        if connect:
            print("el numero de vertices es: " + str(numero))
            return "estan conectados"
    except:
        print("el numero de vertices es: " + str(numero))
        return "NO estan conectados"


def servedRoutes(analyzer):
    lstvert = m.keySet(analyzer["landing_points"])
    maxvert = None
    maxdeg = 0
    for vert in lt.iterator(lstvert):
        lstroutes = m.get(analyzer["landing_points"], vert)["value"]
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg

def minimumCostPath(analyzer,origin, destination):
    capital1=m.get(analyzer["pais_values"], origin)["value"]["capitalvertex"]
    capitalvertex=m.get(analyzer["landing_points"], capital1)["value"]
    cable_name=lt.getElement(capitalvertex, 0)
    capitalpais1=capital1+"-"+cable_name
    print(capitalpais1)



    capital2=m.get(analyzer["pais_values"], destination)["value"]["capitalvertex"]
    capitalvertex2=m.get(analyzer["landing_points"], capital2)["value"]
    cable_name2=lt.getElement(capitalvertex2, 0)
    capitalpais2=capital2+"-"+cable_name2
    print(capitalpais2)

    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], capitalpais1)
    path = djk.pathTo(analyzer['paths'], capitalpais2)
    return path




# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareIds(stop, keyvaluestop):
    """
    Compara dos crimenes
    """

    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def formatpoint(point, cable):
    name = point+'-'
    name = name + cable['cable_name']
    return name 
def comparecables(cable1, cable2):
    """
    Compara dos rutas
    """
    if (cable1 == cable2):
        return 0
    elif (cable1 > cable2):
        return 1
    else:
        return -1
