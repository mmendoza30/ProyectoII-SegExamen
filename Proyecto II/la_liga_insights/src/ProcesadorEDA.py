import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ProcesadorEDA:
    def __init__(self, df):
        self.df = df

    def mostrar_head(self):
        """Devuelve las primeras 5 filas del DataFrame"""
        return self.df.head()

    def mostrar_tail(self):
        """Devuelve las últimas 5 filas del DataFrame"""
        return self.df.tail()

    def mostrar_info(self):
        """Devuelve la información general del DataFrame"""
        return self.df.info()

    def eliminar_columnas(self, columnas_a_eliminar):
        """Elimina las columnas especificadas y actualiza el DataFrame"""
        self.df = self.df.drop(columns=columnas_a_eliminar)
        print(f"Columnas eliminadas: {columnas_a_eliminar}")
        return self.df

    def mostrar_dimensiones(self):
        """Devuelve las dimensiones del DataFrame"""
        return self.df.shape

    def mostrar_valores_nulos(self):
        """Devuelve la cantidad de valores nulos por columna"""
        return self.df.isnull().sum()

    def mostrar_resumen_descriptivo(self):
        """Devuelve el resumen descriptivo del DataFrame"""
        return self.df.describe()

    def limpiar_datos(self):
        """Elimina las columnas con valores nulos"""
        self.df = self.df.dropna(axis=1, how='any')
        return self.df

    def mostrar_columnas(self):
        """Devuelve el resumen descriptivo del DataFrame"""
        return self.df.columns

    def matriz_correlacion(self, mostrar_grafico=True):
        """Genera la matriz de correlación, muestra la tabla y opcionalmente muestra un heatmap."""

        df_numerico = self.df.select_dtypes(include=[np.number]).dropna(axis=1, how='all')
        df_numerico = df_numerico.loc[:, df_numerico.nunique() > 1]

        if df_numerico.empty:
            print("No hay columnas válidas para calcular la correlación.")
            return

        # Calcular la matriz de correlación
        corr_matrix = df_numerico.corr()

        if mostrar_grafico:
            # Crear el gráfico de la matriz de correlación usando seaborn
            plt.figure(figsize=(17, 12))  # Ajustar tamaño
            sns.heatmap(corr_matrix, annot=True, cmap='viridis')  # Crear el heatmap con annot
            plt.ylim(len(corr_matrix) - 1, 0)  # Ajustar el límite del eje y para el gráfico
            plt.title("Matriz de Correlación")
            plt.tight_layout()
            plt.show()  # Mostrar el gráfico

        return corr_matrix


    def outliers(self, columna):
        """Muestra un boxplot de la columna a escoger."""

        # Crear el boxplot
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=self.df, x=columna, color='skyblue')
        plt.title(f"Boxplot de la columna '{columna}' con Outliers")
        plt.show()