# Viviendas de California · Streamlit

Proyecto de Programación para Análisis de Datos (UCU), creado desde el [template de la asignatura](https://github.com/hchocobar/ucu-pad-project-data-analysis-with-streamlit).

Aplicación exploratoria con Pandas, scikit-learn, Streamlit y Plotly. Cada fila representa un grupo de bloques censales de California en 1990.

## Entrega

- [Repositorio público](https://github.com/victoriailla2607/ucu-california-housing-streamlit)
- Aplicación en Streamlit Community Cloud: pendiente de finalizar el despliegue.

## Ejecutar localmente

Requiere Python 3.12 o superior. Se recomienda un entorno virtual.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

La primera ejecución descarga el dataset oficial mediante `fetch_california_housing()`: requiere acceso a Internet. Las ejecuciones siguientes reutilizan la caché. Si falla la descarga, la aplicación muestra un mensaje y permite reintentar.

## Funcionalidades y correspondencia con la consigna

| Requisito | Implementación |
| --- | --- |
| DataFrame único `df_california` | Ocho características con `feature_names` más `MedHouseVal` |
| Preparación inicial | Pestaña de carga y calidad: primeras cinco filas, tipos y faltantes por columna |
| Barra lateral | Título y explicación con `st.sidebar.markdown()` |
| Edad mediana | Slider con mínimo y máximo reales de `HouseAge` y límites inclusivos |
| Latitud mínima | `number_input` y checkbox para activar o desactivar el filtro |
| Resumen descriptivo | Mediana y rango máximo menos mínimo de `MedHouseVal` sobre la selección |
| Visualización dinámica | Histograma y dispersión `MedInc` frente a `MedHouseVal`, ambos con todos los registros filtrados |
| Mapa opcional | `st.map()` con coordenadas de la selección |
| Resultados vacíos | Aviso explícito; no se muestran estadísticas indefinidas ni gráficos vacíos |
| Exportación adicional | Descarga del conjunto filtrado en CSV |

El título del template menciona Boston, pero su instrucción y función de carga especifican **California Housing**, que es el dataset utilizado aquí. La sección de latitud menciona tanto checkbox como campo numérico: se incluyen ambos, con el filtro activado inicialmente.

## Datos y unidades

El dataset incluye 20.640 grupos censales y ocho características: `MedInc`, `HouseAge`, `AveRooms`, `AveBedrms`, `Population`, `AveOccup`, `Latitude` y `Longitude`. La variable objetivo es `MedHouseVal`.

- `MedHouseVal`: cientos de miles de USD. Por ejemplo, 2,0 equivale a USD 200.000.
- `MedInc`: decenas de miles de USD.
- Los valores corresponden a 1990 y no están ajustados por inflación.
- El target tiene un límite superior cercano a 5,00001: afecta la interpretación de la distribución.
- Una asociación entre ingresos y valores de vivienda no demuestra causalidad. No se entrena un modelo predictivo.

Fuentes: [API de carga](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html) y [descripción del dataset](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset).

## Estructura

```text
app.py                       # Aplicación y funciones de carga/filtro
requirements.txt             # Dependencias
notebooks/practice.ipynb     # Análisis exploratorio reproducible
tests/test_app.py            # Pruebas con datos reales y Streamlit AppTest
```

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican estructura y faltantes del dataset, límites de filtros, métricas y tabla filtrada, selección vacía, desactivación de latitud y mapa. Requieren Internet en la primera descarga.

## Despliegue en Streamlit Community Cloud

1. Iniciar sesión en [Streamlit Community Cloud](https://share.streamlit.io/) con la cuenta de GitHub.
2. Elegir **Create app** y el repositorio `victoriailla2607/ucu-california-housing-streamlit`.
3. Seleccionar rama `main`, archivo `app.py` y Python 3.12 en las opciones avanzadas.
4. Pulsar **Deploy**. No se necesitan secretos ni claves.
5. Verificar filtros y gráficos; copiar la URL pública a la sección Entrega.

En WebAsignatura se presentan el enlace al repositorio y el enlace de la aplicación. La fecha exacta no está indicada en la consigna compartida.
