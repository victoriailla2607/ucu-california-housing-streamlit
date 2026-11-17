"""Exploración interactiva del dataset California Housing (censo de 1990)."""

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.datasets import fetch_california_housing


@st.cache_data(show_spinner="Cargando California Housing…")
def cargar_datos():
    """Combina las ocho características y el target, conservando sus nombres."""
    california = fetch_california_housing()
    df_california = pd.DataFrame(california.data, columns=california.feature_names)
    df_california["MedHouseVal"] = california.target
    return df_california


def filtrar_datos(df_california, edades, latitud_minima):
    """Aplica ambos filtros con límites inclusivos, sin modificar el original."""
    return df_california.loc[
        df_california["HouseAge"].between(*edades)
        & df_california["Latitude"].ge(latitud_minima)
    ].copy()


def main():
    st.set_page_config(page_title="California Housing · UCU", page_icon="🏡", layout="wide")
    st.caption("UCU · PROGRAMACIÓN PARA ANÁLISIS DE DATOS")
    st.title("Viviendas de California")
    st.markdown(
        "Explorá cómo cambian los valores de vivienda según la edad y la ubicación. "
        "Cada fila representa un **grupo de bloques censales**, no una vivienda individual."
    )
    st.caption("Fuente: censo de California de 1990, distribuido por scikit-learn.")

    try:
        df_california = cargar_datos()
    except (OSError, ValueError) as error:
        st.error("No se pudo cargar el dataset. Revisá la conexión y volvé a intentarlo.")
        with st.expander("Detalle de la carga"):
            st.code(str(error))
        if st.button("Reintentar carga"):
            cargar_datos.clear()
            st.rerun()
        st.stop()

    edad_min = int(df_california["HouseAge"].min())
    edad_max = int(df_california["HouseAge"].max())
    lat_min = float(df_california["Latitude"].min())
    lat_max = float(df_california["Latitude"].max())

    st.sidebar.markdown("## Filtros\nAjustá la selección; las estadísticas y los gráficos se actualizan juntos.")
    edades = st.sidebar.slider(
        "Edad mediana de las casas (años)", edad_min, edad_max, (edad_min, edad_max)
    )
    # La consigna menciona checkbox y number_input: se incluyen ambos.
    aplicar_latitud = st.sidebar.checkbox("Aplicar filtro de latitud", value=True, key="filtro_latitud")
    latitud = st.sidebar.number_input(
        "Latitud mínima", min_value=lat_min, max_value=lat_max,
        value=lat_min, step=0.01, format="%.2f", disabled=not aplicar_latitud,
    )
    df_filtrado = filtrar_datos(df_california, edades, latitud if aplicar_latitud else lat_min)
    st.sidebar.caption(f"{len(df_filtrado):,} de {len(df_california):,} grupos censales seleccionados.")

    exploracion, preparacion = st.tabs(["Exploración interactiva", "Carga y calidad de datos"])
    with preparacion:
        st.subheader("Primeras cinco filas del dataset original")
        st.dataframe(df_california.head(5), hide_index=True, width="stretch")
        st.subheader("Tipos de datos")
        st.write(df_california.dtypes.astype(str).rename("Tipo de dato"))
        st.subheader("Valores faltantes por columna")
        faltantes = df_california.isna().sum().rename("Valores faltantes")
        st.dataframe(faltantes, width="stretch")
        st.write(f"Total de valores faltantes: {int(faltantes.sum())}.")
        st.subheader("Diccionario de variables")
        st.dataframe(pd.DataFrame({
            "Variable": list(df_california.columns),
            "Descripción": [
                "Mediana de ingresos (decenas de miles de USD)",
                "Mediana de la edad de las casas (años)",
                "Promedio de habitaciones por hogar",
                "Promedio de dormitorios por hogar",
                "Población del grupo censal",
                "Promedio de ocupantes por hogar",
                "Latitud del centro del grupo censal",
                "Longitud del centro del grupo censal",
                "Mediana del valor de vivienda (cientos de miles de USD)",
            ],
        }), hide_index=True, width="stretch")

    with exploracion:
        st.subheader("Resumen de la selección")
        if df_filtrado.empty:
            st.warning("No hay grupos censales que cumplan ambos filtros. Ampliá la edad o reducí la latitud mínima.")
            st.info("La mediana, el rango y los gráficos no se calculan para una selección vacía.")
        else:
            valores = df_filtrado["MedHouseVal"]
            mediana = float(valores.median())
            rango = float(valores.max() - valores.min())
            grupos, valor, amplitud = st.columns(3)
            grupos.metric("Grupos censales", f"{len(df_filtrado):,}")
            valor.metric("Mediana · MedHouseVal", f"{mediana:.3f}")
            amplitud.metric("Rango · máximo − mínimo", f"{rango:.3f}")
            st.caption(
                f"MedHouseVal se expresa en cientos de miles de USD: mediana equivalente a USD {mediana * 100_000:,.0f}; "
                f"rango equivalente a USD {rango * 100_000:,.0f}. Valores históricos, sin ajuste por inflación."
            )
            izquierda, derecha = st.columns(2)
            with izquierda:
                histograma = px.histogram(
                    df_filtrado, x="MedHouseVal", nbins=40,
                    title="Distribución del valor de vivienda",
                    labels={"MedHouseVal": "Valor mediano (100.000 USD)"},
                    color_discrete_sequence=["#167D8D"],
                )
                histograma.update_layout(yaxis_title="Grupos censales", bargap=0.06)
                st.plotly_chart(histograma, width="stretch")
            with derecha:
                dispersion = px.scatter(
                    df_filtrado, x="MedInc", y="MedHouseVal", opacity=0.35,
                    title="Ingresos y valor de vivienda", render_mode="webgl",
                    labels={"MedInc": "Ingreso mediano (10.000 USD)", "MedHouseVal": "Valor mediano (100.000 USD)"},
                    hover_data=["HouseAge", "Latitude", "Longitude"],
                    color_discrete_sequence=["#167D8D"],
                )
                st.plotly_chart(dispersion, width="stretch")
            st.caption("Los gráficos incluyen todos los registros filtrados. Una asociación visual no demuestra causalidad.")
            if st.checkbox("Mostrar mapa geográfico", value=False, key="mostrar_mapa"):
                st.subheader("Ubicación de los grupos seleccionados")
                st.map(df_filtrado.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}), size=20)
            st.subheader("Datos filtrados")
            st.dataframe(df_filtrado, hide_index=True, width="stretch")
            st.download_button(
                "Descargar selección en CSV", df_filtrado.to_csv(index=False).encode("utf-8"),
                file_name="california_housing_filtrado.csv", mime="text/csv",
            )

    with st.expander("Cómo interpretar estos datos"):
        st.markdown(
            "- El dataset contiene agregados de grupos censales de 1990.\n"
            "- `MedHouseVal` está limitado superiormente cerca de 5,00001 (aproximadamente USD 500.001).\n"
            "- `MedInc` es ingreso mediano y `AveOccup` es ocupación promedio por hogar.\n"
            "- Los filtros se combinan con **Y** e incluyen sus límites.\n"
            "- Esta aplicación es exploratoria: no entrena un modelo ni estima precios actuales."
        )
        st.markdown("[Documentación del dataset](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset)")


if __name__ == "__main__":
    main()
