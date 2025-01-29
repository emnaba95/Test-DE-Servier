import os
import json
import pandas as pd
from src.data_loader import load_csv, load_json
from src.data_cleaner import clean_data_pipeline, save_cleaned_data
from src.graph_builder import graph_build

def main():

    # Chemins vers les fichiers
    base_path = "data/"
    drugs_file = os.path.join(base_path, "drugs.csv")
    pubmed_csv_file = os.path.join(base_path, "pubmed.csv")
    pubmed_json_file = os.path.join(base_path, "pubmed.json")
    clinical_trials_file = os.path.join(base_path, "clinical_trials.csv")
    
    # Chargement des données
    drugs = load_csv(drugs_file)
    pubmed_csv = load_csv(pubmed_csv_file)
    pubmed_json = load_json(pubmed_json_file)
    clinical_trials = load_csv(clinical_trials_file)
    
    # Nettoyage des données
    drugs_cleaned = clean_data_pipeline(drugs, date_columns=None,exclude_columns=['atccode'], unique_subset=None)
    pubmed_cleaned = clean_data_pipeline(pd.concat([pubmed_csv, pubmed_json], ignore_index=True), date_columns=['date'], exclude_columns=['id'], unique_subset=["title", "date"])
    clinical_trials_cleaned = clean_data_pipeline(clinical_trials, date_columns=['date'], exclude_columns=['id'], unique_subset=["scientific_title", "date"])

    # Sauvegarder les données nettoyées
    save_cleaned_data(drugs_cleaned, "output/drugs_cleaned.csv")
    save_cleaned_data(pubmed_cleaned, "output/pubmed_cleaned.csv")
    save_cleaned_data(clinical_trials_cleaned, "output/clinical_trials_cleaned.csv")

    
    # Construction du graphe
    graph = graph_build(drugs_cleaned, pubmed_cleaned, clinical_trials_cleaned)

    # Sauvegarde du résultat en JSON
    output_file = "output/result.json"
    with open(output_file, 'w') as f:
        json.dump(graph, f, indent=4, default=str)
    
    print(f"Graphe généré et sauvegardé dans {output_file}")
    

if __name__ == "__main__":
    main()
