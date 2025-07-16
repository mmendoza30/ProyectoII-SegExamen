import pandas as pd
from ProcesadorEDA import ProcesadorEDA
from Visualizador import Visualizador


# Cargar y limpiar el DataFrame
archivo = "C:/Users/rmont/Downloads/proyecto II progamacion/final/ProyectoII-SegExamen/Proyecto II/la_liga_insights/data/partidos-laliga-2024-2025.csv"

# Paso 1: Crear la instancia de ProcesadorEDA y cargar el DataFrame
df = pd.read_csv(archivo)
procesador = ProcesadorEDA(df)

# Paso 2: Limpiar los datos usando el método limpiar_datos
df_limpio = procesador.limpiar_datos()

# Paso 3: Crear la instancia de Visualizador y pasar el DataFrame limpio
visualizador = Visualizador(df_limpio)

# Paso 4: Llamar a los métodos de Visualizador para mostrar gráficos
# Puedes agregar o modificar los gráficos según lo que necesites
visualizador.mostrar_histograma('goles_local')  # Ejemplo de histograma
visualizador.mostrar_scatter('goles_local', 'goles_visita')  # Scatter plot
visualizador.mostrar_boxplot('goles_local')  # Boxplot para detectar outliers
visualizador.mostrar_heatmap_correlacion()  # Correlación de variables numéricas
