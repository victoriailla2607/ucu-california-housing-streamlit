"""Pruebas con el dataset real y con el ejecutor oficial de Streamlit."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import cargar_datos, filtrar_datos
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


class DatosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = cargar_datos()

    def test_estructura_real_y_faltantes(self):
        self.assertEqual(self.df.shape, (20640, 9))
        self.assertEqual(int(self.df.isna().sum().sum()), 0)
        self.assertEqual(self.df.columns[-1], "MedHouseVal")

    def test_limites_inclusivos_y_original_intacto(self):
        fila = self.df.iloc[0]
        filtrado = filtrar_datos(self.df, (fila.HouseAge, fila.HouseAge), fila.Latitude)
        self.assertIn(0, filtrado.index)
        self.assertTrue(filtrado.HouseAge.eq(fila.HouseAge).all())
        self.assertTrue(filtrado.Latitude.ge(fila.Latitude).all())
        self.assertEqual(len(self.df), 20640)


class InterfazTest(unittest.TestCase):
    def iniciar(self):
        at = AppTest.from_file(str(APP), default_timeout=60).run()
        self.assertEqual(len(at.exception), 0)
        return at

    def test_arranque_y_resumen(self):
        at = self.iniciar()
        self.assertEqual(at.metric[0].value, "20,640")
        self.assertEqual(at.metric[1].value, f'{cargar_datos().MedHouseVal.median():.3f}')
        self.assertEqual(len(at.get("plotly_chart")), 2)
        self.assertEqual(at.tabs[1].dataframe[0].value.shape, (5, 9))

    def test_filtros_actualizan_tabla_y_metricas(self):
        at = self.iniciar()
        at.slider[0].set_value((10, 30))
        at.number_input[0].set_value(36.0).run()
        esperado = filtrar_datos(cargar_datos(), (10, 30), 36.0)
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.metric[0].value, f"{len(esperado):,}")
        self.assertEqual(at.metric[1].value, f"{esperado.MedHouseVal.median():.3f}")
        self.assertTrue(at.tabs[0].dataframe[0].value.equals(esperado))
        self.assertEqual(len(at.get("plotly_chart")), 2)

    def test_seleccion_vacia(self):
        at = self.iniciar()
        at.slider[0].set_value((1, 1))
        at.number_input[0].set_value(41.95).run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(len(at.warning), 1)
        self.assertEqual(len(at.metric), 0)
        self.assertEqual(len(at.get("plotly_chart")), 0)

    def test_desactivar_latitud_y_mapa(self):
        at = self.iniciar()
        at.number_input[0].set_value(40.0).run()
        at.checkbox(key="filtro_latitud").uncheck().run()
        self.assertEqual(at.metric[0].value, "20,640")
        self.assertTrue(at.number_input[0].disabled)
        at.checkbox(key="mostrar_mapa").check().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(len(at.get("deck_gl_json_chart")), 1)


if __name__ == "__main__":
    unittest.main()
