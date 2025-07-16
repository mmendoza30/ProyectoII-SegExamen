# Punto de entrada del proyecto
import os

from GestorBaseDatos import GestorBaseDatos
from ProcesadorEDA import ProcesadorEDA
from Visualizador import Visualizador


#Gestor de Bases de Datos
GestorDB = GestorBaseDatos()
GestorDB.CargaDatos("C:/Users/Fabiola/Documents/CUC/BigData/Programacion II/Proyecto II/la_liga_insights/data/partidos-laliga-2024-2025.csv")
df = GestorDB.ObtencionDatos()

#ProcesadorEDA
ProcesadorEDA = ProcesadorEDA(df)
print(ProcesadorEDA.mostrar_resumen_descriptivo())
print(ProcesadorEDA.matriz_correlacion())
