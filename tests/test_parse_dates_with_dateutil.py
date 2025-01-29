import unittest
import pandas as pd
import os, sys

# Ajoute le dossier 'src' au chemin d'importation pour permettre l'accès aux modules qu'il contient.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from data_cleaner import parse_dates_with_dateutil


# Tester la fonction parse_dates_with_dateutil
class TestParseDatesWithDateutil(unittest.TestCase):
    def setUp(self):
        # DataFrame avec les dates spécifiées pour les tests
        self.df = pd.DataFrame({
            "dates": ["1 January 2020", "25/05/2020", "02/01/2019", "2020-01-01", "2020-01-34","invalid_date", None]
        })
    
    def test_parse_dates(self):
        # Exécute la fonction avec les données de test
        df_result = parse_dates_with_dateutil(self.df.copy(), ["dates"])

        # Vérifie les dates correctement parsées
        self.assertEqual(str(df_result["dates"][0]), "2020-01-01")  # "1 January 2020"
        self.assertEqual(str(df_result["dates"][1]), "2020-05-25")  # "25/05/2020"
        self.assertEqual(str(df_result["dates"][2]), "2019-01-02")  # "02/01/2019"
        self.assertEqual(str(df_result["dates"][3]), "2020-01-01")  # "2020-01-01"

    def test_invalid_dates_with_default(self):
        # Teste les dates invalides avec une valeur par défaut
        default_date = "1900-01-01"
        df_result = parse_dates_with_dateutil(self.df.copy(), ["dates"], default_value=default_date)
        
        # Vérifie que les dates invalides sont remplacées par la valeur par défaut
        self.assertEqual(df_result["dates"][4], default_date)  # "2020-01-34"
        self.assertEqual(df_result["dates"][5], default_date)  # "invalid_date"
        self.assertEqual(df_result["dates"][6], default_date)  # None
    
    def test_invalid_dates_without_default(self):
        # Teste les dates invalides sans valeur par défaut
        df_result = parse_dates_with_dateutil(self.df.copy(), ["dates"])

        # Vérifie que les dates invalides restent None
        self.assertIsNone(df_result["dates"][4])  # "2020-01-34"
        self.assertIsNone(df_result["dates"][5])  # "invalid_date"
        self.assertIsNone(df_result["dates"][6])  # None

if __name__ == "__main__":
    unittest.main()
