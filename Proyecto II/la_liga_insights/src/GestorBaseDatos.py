
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

    def CargaDatos(self,dataset):
        df = pd.read_csv(dataset)
        df["fecha"] = pd.to_datetime(df["fecha"])

        datos = df.to_dict(orient="records")
        self.session.bulk_insert_mappings(partidos, datos)
        self.session.commit()

    def ObtencionDatos(self):
        df = pd.read_sql_query("SELECT * FROM partidos", self.engine)
        return df

    def get_partido(self,id):
        query = "Select * from partidos where id_partido = :id_partido"
        result = self.cursor.execute(query,{"id_partido":id})
        return result.fetchall()

    def get_por_equipo_local(self,equipo):
        query = "Select * from partidos where equipo_local = :equipo"
        result = self.cursor.execute(query,{"equipo_local":equipo})
        return result.fetchall()

    def get_por_equipo_visita(self,equipo):
        query = "Select * from partidos where equipo_visita = :equipo"
        result = self.cursor.execute(query,{"equipo_visita":equipo})
        return result.fetchall()

    def get_por_temporada(self,temporada):
        query = "Select * from partidos where temporada = :temporada"
        result = self.cursor.execute(query,{"temporada":temporada})
        return result.fetchall()

    def get_por_visita(self,visita):
        query = "Select * from partidos where visita = :visita"
        result = self.cursor.execute(query,{"visita":visita})
        return result.fetchall()

    def get_por_a_puerta(self,a_puerta):
        query = "Select * from partidos where a_puerta = :a_puerta"
        result = self.cursor.execute(query,{"a_puerta":a_puerta})
        return result.fetchall()



