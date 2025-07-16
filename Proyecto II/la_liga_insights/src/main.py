# Punto de entrada del proyecto
import os
from GestorBaseDatos import GestorBaseDatos
from ProcesadorEDA import ProcesadorEDA
from Visualizador import Visualizador

# Gestor de Bases de Datos
GestorDB = GestorBaseDatos()
GestorDB.CargaDatos("C:/Users/rmont/Downloads/proyecto II progamacion/final/ProyectoII-SegExamen/Proyecto II/la_liga_insights/data/partidos-laliga-2024-2025.csv")
df = GestorDB.ObtencionDatos()

# Ejecutar metodos de las clases en GestorBaseDatos
print("Pruebas del GestorBaseDatos:\n")
print("1. Partido por ID:", GestorDB.get_partido(1))
print("2. Partidos como local:", len(GestorDB.get_por_equipo_local("Real Madrid")))
print("3. Partidos como visitante:", len(GestorDB.get_por_equipo_visita("Barcelona")))
print("4. Partidos por temporada:", len(GestorDB.get_por_temporada(2024)))
print("5. Todos los partidos de un equipo:", len(GestorDB.get_por_equipo("Real Madrid")))
print("6. Partidos con 5+ tiros a puerta:", len(GestorDB.get_por_a_puerta(5)))
print("6. Partidos con goles minimos:", len(GestorDB.get_partidos_con_goles_minimos(5)))


# ProcesadorEDA
ProcesadorEDA = ProcesadorEDA(df)
print("\nResumen descriptivo:\n")
print(ProcesadorEDA.mostrar_resumen_descriptivo())
print("\nBloxPlot:\n")
print(ProcesadorEDA.outliers('corners_local'))
print("\nMatriz de correlación:\n")
print(ProcesadorEDA.matriz_correlacion())