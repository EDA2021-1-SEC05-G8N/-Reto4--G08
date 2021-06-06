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

def connectedComponents(analyzer):
    return model.connectedComponents(analyzer)
def vertexComponents(analyzer, verta, vertb):
    return model.vertexComponents(analyzer, verta, vertb)

def servedRoutes(analyzer):
    return model.servedRoutes(analyzer)

def minimumCostPath(analyzer,origin, destination):
    return model.minimumCostPath(analyzer,origin, destination)