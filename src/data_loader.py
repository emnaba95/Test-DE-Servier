import pandas as pd
import json
import os

def load_csv(file_path):
    """
    Charge un fichier CSV et retourne un DataFrame.
    
    Args:
        file_path (str): Le chemin du fichier CSV à charger.
    
    Returns:
        pd.DataFrame: Un DataFrame contenant les données du fichier CSV.
    
    Raises:
        FileNotFoundError: Si le fichier spécifié n'existe pas.
    """
    # Vérifie si le fichier existe à l'emplacement donné.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Charge le fichier CSV dans un DataFrame pandas et le retourne.
    return pd.read_csv(file_path)

def load_json(file_path):
    """
    Charge un fichier JSON et retourne un DataFrame.
    
    Args:
        file_path (str): Le chemin du fichier JSON à charger.
    
    Returns:
        pd.DataFrame: Un DataFrame contenant les données du fichier JSON.
    
    Raises:
        FileNotFoundError: Si le fichier spécifié n'existe pas.
    """
    # Vérifie si le fichier existe à l'emplacement donné.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Ouvre le fichier JSON en mode lecture.
    with open(file_path, 'r') as f:
        # Charge le contenu JSON dans une structure Python (par exemple, liste ou dictionnaire).
        data = json.load(f)
    
    # Convertit les données JSON en DataFrame pandas et le retourne.
    return pd.DataFrame(data)
