import streamlit as st
import sys
import os

# Agregar 'src' al path para importar los módulos personalizados
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar las clases necesarias
from GestorBaseDatos import GestorBaseDatos
from ProcesadorEDA import ProcesadorEDA
from GraficosStreamlit import VisualizadorStreamlit

def cargar_datos(archivo_path):

    #Carga los datos
    gestor_db = GestorBaseDatos()
    gestor_db.CargaDatos(archivo_path)
    df = gestor_db.ObtencionDatos()

    # Procesar datos
    procesador = ProcesadorEDA(df)
    df_limpio = procesador.limpiar_datos()

    # Crear visualizador
    visualizador = VisualizadorStreamlit(df_limpio)

    return gestor_db, visualizador, df_limpio


# Barra lateral
def barra_lateral():
    st.sidebar.header('**Menú**')
    opcion_principal = st.sidebar.radio('**Haz clic en:**', ['Visualizaciones', 'Base de Datos'])

    if opcion_principal == 'Visualizaciones':
        opcion_graficos = st.sidebar.selectbox('Selecciona una opción:',
                                          ['Histograma', 'Scatter', 'Barras Vertical', 'Barras Horizontal'])
        return opcion_principal, opcion_graficos
    elif opcion_principal == 'Base de Datos':
        opcion_db = st.sidebar.selectbox('Selecciona una opción:',
                                         ['Partidos de local', 'Partidos de visita',
                                          'Partidos por temporada','Partidos con goles minimos','Tiros a puerta puerta'])
        return opcion_principal, opcion_db


def mostrar_visualizaciones(visualizador, opcion_elegida):
    st.title(f"Gráfico: {opcion_elegida}")

    if opcion_elegida == "Histograma":
        visualizador.histograma('goles_local')
    elif opcion_elegida == "Scatter":
        visualizador.scatter('goles_local', 'goles_visita')
    elif opcion_elegida == "Barras Vertical":
        visualizador.grafico_barras('goles_local')
    elif opcion_elegida == "Barras Horizontal":
        visualizador.barras_horizontal("faltas_local")

# Función para mostrar consultas de base de datos
def mostrar_base_datos(gestor_db, opcion_elegida):
    st.title(f'Consulta: {opcion_elegida}')

    if opcion_elegida == 'Partidos con goles minimos':
        goles_minimos = st.number_input('Ingresa el número mínimo de goles:', min_value=0, value=2)
        if st.button('Buscar Partidos con Goles Mínimos'):
            resultados = gestor_db.get_partidos_con_goles_minimos(goles_minimos)
            st.write(f"**Partidos con al menos {goles_minimos} goles en total:** {len(resultados)}")
            if resultados:
                for partido in resultados:
                    # Mostrar  los resultados
                    st.write(f"**Equipo Local:** {partido.equipo_local}")
                    st.write(f"**Equipo Visitante:** {partido.equipo_visita}")
                    st.write(f"**Goles Local:** {partido.goles_local}")
                    st.write(f"**Goles Visitante:** {partido.goles_visita}")
                    st.write("---")
            else:
                st.warning(f"No se encontraron partidos con al menos {goles_minimos} goles.")

    if opcion_elegida == 'Tiros a puerta puerta':
        a_puerta = st.number_input('Ingresa el número mínimo de tiros a puerta:', min_value=0, value=2)
        if st.button('Buscar Partidos con Tiros a Puerta'):
            resultados = gestor_db.get_por_a_puerta(a_puerta)
            st.write(f"**Partidos con al menos {a_puerta} tiros a puerta (local o visitante):** {len(resultados)}")
            if resultados:
                # Mostrar detalles
                for partido in resultados:
                    st.write(f"**Equipo Local:** {partido.equipo_local}")
                    st.write(f"**Equipo Visitante:** {partido.equipo_visita}")
                    st.write(f"**Tiros a Puerta Local:** {partido.tiros_a_puerta_local}")
                    st.write(f"**Tiros a Puerta Visitante:** {partido.tiros_a_puerta_visita}")
                    st.write("---")
            else:
                st.warning(f"No se encontraron partidos con al menos {a_puerta} tiros a puerta.")

    elif opcion_elegida == 'Partidos de local':
        equipo = st.text_input('Ingresa el nombre del equipo:', 'Real Madrid')
        if st.button('Buscar Partidos como Local'):
            resultados = gestor_db.get_por_equipo_local(equipo)
            st.write(f"**Partidos donde {equipo} jugó como local:** {len(resultados)}")
            if resultados:
                st.write(f"Se encontraron {len(resultados)} partidos donde {equipo} jugó como local.")
            else:
                st.warning(f"No se encontraron partidos donde {equipo} jugara como local.")

    elif opcion_elegida == 'Partidos de visita':
        equipo = st.text_input('Ingresa el nombre del equipo:', 'Barcelona')
        if st.button('Buscar Partidos como Visitante'):
            resultados = gestor_db.get_por_equipo_visita(equipo)
            st.write(f"**Partidos donde {equipo} jugó como visitante:** {len(resultados)}")
            if resultados:
                st.write(f"Se encontraron {len(resultados)} partidos donde {equipo} jugó como visitante.")
            else:
                st.warning(f"No se encontraron partidos donde {equipo} jugara como visitante.")

    elif opcion_elegida == 'Partidos por temporada':
        temporada = st.number_input('Ingresa la temporada:', min_value=2020, max_value=2030, value=2024)
        if st.button('Buscar Partidos por Temporada'):
            resultados = gestor_db.get_por_temporada(temporada)
            st.write(f"**Partidos en la temporada {temporada}:** {len(resultados)}")
            if resultados:
                st.write(f"Se encontraron {len(resultados)} partidos en la temporada {temporada}.")
            else:
                st.warning(f"No se encontraron partidos para la temporada {temporada}.")
# Main
def main():
    st.set_page_config(
        page_title='Liga Española',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    # Llamar a la barra lateral
    opcion_principal, opcion_elegida = barra_lateral()

    # Título
    with st.container():
        st.title('Liga Española 2024-2025')
    # Ruta del archivo
    archivo = "C:/Users/rmont/Downloads/proyecto II progamacion/final/ProyectoII-SegExamen/Proyecto II/la_liga_insights/data/partidos-laliga-2024-2025.csv"

    try:
        # Cargar datos
        gestor_db, visualizador, df_limpio = cargar_datos(archivo)

        # Mostrar info
        st.sidebar.markdown("---")
        st.sidebar.write(f"**Total de partidos:** {len(df_limpio)}")

        # Mostrar contenido
        if opcion_principal == 'Visualizaciones':
            mostrar_visualizaciones(visualizador, opcion_elegida)
        elif opcion_principal == 'Base de Datos':
            mostrar_base_datos(gestor_db, opcion_elegida)

    except FileNotFoundError:
        st.error(f"❌ No se pudo encontrar el archivo: {archivo}")
        st.info("Verifica que la ruta del archivo sea correcta")
    except ImportError as e:
        st.error(f"❌ Error al importar módulos: {e}")
        st.info("Verifica que todos los archivos estén en el directorio correcto")
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        st.info("Revisa la consola para más detalles del error")


if __name__ == "__main__":
    main()