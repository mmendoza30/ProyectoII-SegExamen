from numpy import integer
from sqlalchemy import create_engine, Column, Integer,DECIMAL, String, Date, ForeignKey, SmallInteger, column
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.ext.declarative import declarative_base
import pyodbc


print(pyodbc.drivers())
Base = declarative_base()

class partidos(Base):
    __tablename__ = 'partidos'
    id_partido = Column(Integer, primary_key=True)
    temporada = Column(SmallInteger)
    fecha = Column(Date)
    equipo_local = Column(String)
    equipo_visita = Column(String)
    goles_local = Column(SmallInteger)
    goles_visita = Column(SmallInteger)
    xg_local = Column(DECIMAL(5,2))
    xg_visita = Column(DECIMAL(5,2))
    posesion_local = Column(DECIMAL(5,2))
    posesion_visita = Column(DECIMAL(5,2))
    amarillas_local = Column(SmallInteger)
    amarillas_visita = Column(SmallInteger)
    rojas_local = Column(SmallInteger)
    rojas_visita = Column(SmallInteger)
    tiros_local = Column(SmallInteger)
    tiros_visita = Column(SmallInteger)
    tiros_a_puerta_local = Column(SmallInteger)
    tiros_a_puerta_visita = Column(SmallInteger)
    corners_local = Column(SmallInteger)
    corners_visita = Column(SmallInteger)
    faltas_local = Column(SmallInteger)
    faltas_visita = Column(SmallInteger)

class GestorBaseDatos:
    def __init__(self):
        self.engine = create_engine("sqlite:///ligaespanola.db")
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def CargaDatos(self, dataset):
        df = pd.read_csv(dataset)
        df["fecha"] = pd.to_datetime(df["fecha"])
        datos = df.to_dict(orient="records")
        self.session.bulk_insert_mappings(partidos, datos)
        self.session.commit()

    def ObtencionDatos(self):
        df = pd.read_sql_query("SELECT * FROM partidos", self.engine)
        return df

    def get_partido(self, id):
        resultado = self.session.query(partidos).filter(partidos.id_partido == id).first()
        return resultado

    def get_por_equipo_local(self, equipo):
        resultados = self.session.query(partidos).filter(partidos.equipo_local == equipo).all()
        return resultados

    def get_por_equipo_visita(self, equipo):
        resultados = self.session.query(partidos).filter(partidos.equipo_visita == equipo).all()
        return resultados

    def get_por_temporada(self, temporada):
        resultados = self.session.query(partidos).filter(partidos.temporada == temporada).all()
        return resultados

    def get_por_equipo(self, equipo):
        resultados = self.session.query(partidos).filter(
            (partidos.equipo_local == equipo) |
            (partidos.equipo_visita == equipo)
        ).all()
        return resultados

    def get_por_a_puerta(self, a_puerta):
        partidos_resultados = self.session.query(partidos).filter(
            (partidos.tiros_a_puerta_local >= a_puerta) |
            (partidos.tiros_a_puerta_visita >= a_puerta)
        ).all()
        return partidos_resultados

    def get_partidos_con_goles_minimos(self, goles_minimos):
        resultados = self.session.query(partidos).filter(
            (partidos.goles_local + partidos.goles_visita) >= goles_minimos
        ).all()
        return resultados

    def get_partidos_por_rango_fecha(self, fecha_inicio, fecha_fin):
        resultados = self.session.query(partidos).filter(
            partidos.fecha.between(fecha_inicio, fecha_fin)
        ).all()
        return resultados

    def cerrar_sesion(self):
        self.session.close()


