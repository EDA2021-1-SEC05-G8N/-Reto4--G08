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
 """

import config as cf
import model
import csv
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos
def loadServices(analyzer, pointsfile, cablesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    cablesfile = cf.data_dir + cablesfile
    pointsfile = cf.data_dir + pointsfile
    input_file_points = csv.DictReader(open(pointsfile, encoding="utf-8"),
                                delimiter=",")
    input_file_cables = csv.DictReader(open(cablesfile, encoding="utf-8-sig"),
                                delimiter=",")
    input_file_paises = csv.DictReader(open(cf.data_dir+"countries.csv", encoding="utf-8"))

    for point in input_file_points:
        model.addpointtable(analyzer, point)
    for pais in input_file_paises:
        model.addpaistable(analyzer, pais)

    lastcable = None
    for cable in input_file_cables:
        if lastcable is not None:
            samecable = lastcable["cable_name"] == cable["cable_name"]
            if samecable:
                cableorigin = cable["origin"]
                cabledest = cable["destination"]
                model.addLandConnection(analyzer, cableorigin, cabledest, cable)
        else:
            cableorigin = cable["origin"]
            cabledest = cable["destination"]
            model.addLandConnection(analyzer, cableorigin, cabledest, cable)
        lastcable = cable
    model.addCableConnections(analyzer)
    return analyzer

# Funciones de ordenamiento
def printpaises(analyzer):
    model.printpaises(analyzer)
# Funciones de consulta sobre el catálogo

def vertexComponents(analyzer, verta, vertb):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    ###############################
    res=model.vertexComponents(analyzer, verta, vertb)
    ###############################
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("tiempo: ")
    print(delta_time)
    print("memoria: ")
    print(delta_memory)
    return res

def servedRoutes(analyzer):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    ###############################
    res=model.servedRoutes(analyzer)
    ###############################
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("tiempo: ")
    print(delta_time)
    print("memoria: ")
    print(delta_memory)
    return res

def minimumCostPath(analyzer,origin, destination):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    ###############################
    res=model.minimumCostPath(analyzer,origin, destination)
    ###############################
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("tiempo: ")
    print(delta_time)
    print("memoria: ")
    print(delta_memory)
    return res

def totalConnections(analyzer):
    return model.totalConnections(analyzer)

def totalVert(analyzer):
    return model.totalVert(analyzer)


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory


    

    