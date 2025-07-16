import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

class VisualizadorStreamlit:
    def __init__(self, df):
        self.df = df

    def _setup_grafico(self, figsize=(10, 6)):
        plt.figure(figsize=figsize)
        sns.set(style="whitegrid")

    def histograma(self, columna):
        self._setup_grafico(figsize=(12, 8))
        sns.histplot(self.df[columna], kde=True, color='skyblue', bins=20)
        plt.title(f"Distribución de '{columna}'", fontsize=16)
        plt.xlabel(columna, fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.tight_layout()
        st.pyplot(plt)  # 👈 importante
        plt.clf()

    def scatter(self, columna_x, columna_y):
        self._setup_grafico(figsize=(12, 8))
        sns.scatterplot(x=self.df[columna_x], y=self.df[columna_y],
                        color='orange', edgecolor='black', s=100)
        plt.title(f"Relación entre '{columna_x}' y '{columna_y}'", fontsize=16)
        plt.xlabel(columna_x, fontsize=12)
        plt.ylabel(columna_y, fontsize=12)
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()

    def grafico_barras(self, columna):
        self._setup_grafico(figsize=(12, 8))
        self.df[columna].value_counts().plot(
            kind='bar',
            color=sns.color_palette("Set2", n_colors=len(self.df[columna].unique()))
        )
        plt.title(f"Frecuencia de '{columna}'", fontsize=16)
        plt.xlabel(columna, fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()

    def barras_horizontal(self, columna):
        self._setup_grafico(figsize=(12, 8))
        self.df[columna].value_counts().plot(
            kind='barh',
            color=sns.color_palette("Set3", n_colors=len(self.df[columna].unique()))
        )
        plt.title(f"Frecuencia de '{columna}'", fontsize=16)
        plt.xlabel('Frecuencia', fontsize=12)
        plt.ylabel(columna, fontsize=12)
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()