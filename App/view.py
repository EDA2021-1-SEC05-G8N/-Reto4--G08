"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Identificar los clústeres de comunicación ")
    print("3- Identificar los puntos de conexión críticos de la red ")
    print("4- La ruta de menor distancia:")
    print("5- Identificar la Infraestructura Crítica de la Red")
    print("6- Análisis de fallas")
    print("7- Los mejores canales para transmitir")
    print("8- La mejor ruta para comunicarme")
    print("9- Graficando los Grafos")
    print("0- Salir")
    print("*******************************************")
catalog = None
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cont = controller.init()
        controller.loadServices(cont, 'landing_points.csv', "connections.csv")
        controller.printpaises(cont)
        print("numero vertices: "+ str(controller.totalVert(cont)))
        print("el numero de arcos es: "+ str(controller.totalConnections(cont)))
    elif int(inputs[0]) == 2:
        verta=input("ingrese el primer vertice: ")
        vertb=input("ingrese el segundo vertice: ")
        connect = controller.vertexComponents(cont, verta, vertb)
        print("los vertices " + connect)
    elif int(inputs[0]) == 3:
        maxvert, maxdeg = controller.servedRoutes(cont)
        print('Vertice: ' + maxvert + '  Total de conecciones: '+ str(maxdeg))
    
    elif int(inputs[0]) == 4:
        origin=input("ingrese el primer pais: ")
        paisvertex=0
        destination=input("ingrese el segundo pais: ")
        paisvertex2=0
        path = controller.minimumCostPath(cont,origin, destination)
        if path is not None:
            pathlen = stack.size(path)
            print('El camino es de longitud: ' + str(pathlen))
            while (not stack.isEmpty(path)):
                stop = stack.pop(path)
                print(stop)
        else:
            print('No hay camino')

    else:
        sys.exit(0)
sys.exit(0)
