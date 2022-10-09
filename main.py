#!/usr/bin/env python
# encoding: utf-8

import json
from flask import Flask
from pymongo import MongoClient

# Iniciar un objeto de tipo aplicación de Flask que nos permite crear la API
app = Flask(__name__)

# URI del cluster de MongoAtlas
CONNECTION_STRING = "mongodb+srv://dbUser:mongoPassword@cluster1.qvlldes.mongodb.net/?retryWrites=true&w=majority"
# Hacer la conexión al MongoAtlas con el URI dado
client = MongoClient(CONNECTION_STRING)
# Acceder a la base de datos deseada
db = client['casos_covid']
# Obtener la collection que nos interesa
covid_collection = db['covid_fallecidos']

# TODO: Poner una explicación de los que se puede hacer con esta API en esta ruta
@app.route('/', methods=["GET"])
def getAll():
    return json.dumps(covid_collection.find_one(), default=str)

# Obtener el total de casos en un año dado
@app.route('/year/<int:year>', methods=["GET"])
def getCasosYear(year):
    return json.dumps(covid_collection.count_documents({ "AÑO": year }), default=str)

# Total de casos por los tres años
@app.route('/years/', methods=["GET"])
def getCasosAllYears():
    return {
            "2020": covid_collection.count_documents({ "AÑO": 2020 }),
            "2021": covid_collection.count_documents({ "AÑO": 2021 }),
            "2022": covid_collection.count_documents({ "AÑO": 2022 })
            }

# Obtener la cantidad de casos por cierta condición medica
# @app.route('/<string:condicion>', methods=["GET"])
# def getCasosAllCondiciones(year):
#     return json.dumps(covid_collection.count_documents({ "AÑO": year }), default=str)

# Cantidad de casos por cada condicón médica
@app.route('/condicion', methods=["GET"])
def getCasosAllCondiciones():
    list_condiciones = ["INTUBADO",
                      "NEUMONIA",
                      "DIABETES",
                      "EPOC",
                      "ASMA",
                      "INMUSUPR",
                      "HIPERTENSION",
                      "OTRA_COM",
                      "CARDIOVASCULAR",
                      "OBESIDAD",
                      "RENAL_CRONICA",
                      "TABAQUISMO"]

    return_dict = dict()

    for condicion in list_condiciones:
        return_dict[condicion] = covid_collection.count_documents({ condicion: 2 })

    return return_dict

# Total de casos por cada edad
@app.route('/edad', methods=["GET"])
def getCasosAllEdades():
    list_edades = covid_collection.distinct('EDAD')

    return_dict = dict()

    for edad in list_edades:
        return_dict[edad] = covid_collection.count_documents({ "EDAD": edad })

    return return_dict

# Total de casos por cada entidad
@app.route('/entidad', methods=["GET"])
def getCasosAllEntidades():
    list_entidades = covid_collection.distinct('ENTIDAD_RES')

    return_dict = dict()

    for entidad in list_entidades:
        return_dict[entidad] = covid_collection.count_documents({ "ENTIDAD_RES": entidad })

    return return_dict

# Total de casos por cada sexo
@app.route('/sexo', methods=["GET"])
def getCasosAllSexos():
    return {
            "MUJERES": covid_collection.count_documents({ "SEXO": 1 }),
            "HOMBRES": covid_collection.count_documents({ "SEXO": 2 }),
            }

if __name__ == '__main__':
    app.run()

