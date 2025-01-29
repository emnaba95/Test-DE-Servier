from collections import defaultdict

def graph_build(drugs, pubmed, clinical_trials):
    """
    Construit un graphe des mentions de médicaments dans différents journaux,
    PubMed et Clinical Trials.

    Args:
        drugs (pd.DataFrame): DataFrame contenant les colonnes "drug".
        pubmed (pd.DataFrame): DataFrame contenant les colonnes "title", "journal", et "date".
        clinical_trials (pd.DataFrame): DataFrame contenant les colonnes "scientific_title", "journal", et "date".
        output_file (str): Chemin du fichier JSON où enregistrer le graphe.

    Returns:
        dict: Graphe structuré par médicament, contenant les journaux (groupés par date), les publications PubMed
              et Clinical Trials.
    """
    # Initialisation du graphe
    graph = {}

    # Parcourir chaque médicament
    for drug_name, original_drug in zip(drugs['drug'], drugs['drug']):
        # Initialisation des sections du graphe pour le médicament
        graph[original_drug] = {
            "journal": defaultdict(list),  # Les journaux groupés par date
            "pubmed": [],                  # Liste des articles PubMed
            "clinical_trials": []          # Liste des essais cliniques
        }

        # Vérifier les mentions dans PubMed
        for _, pub in pubmed.iterrows():
            if drug_name in pub['title']:
                # Ajouter la mention au groupe des journaux
                graph[original_drug]["journal"][pub['journal']].append(pub['date'])

                # Ajouter les détails de la publication dans "pubmed"
                entry = {
                    "title": pub['title'],
                    "date": pub['date']
                }
                if entry not in graph[original_drug]["pubmed"]:  # Éviter les doublons
                    graph[original_drug]["pubmed"].append(entry)

        # Vérifier les mentions dans Clinical Trials
        for _, trial in clinical_trials.iterrows():
            if drug_name in trial['scientific_title']:
                # Ajouter la mention au groupe des journaux
                graph[original_drug]["journal"][trial['journal']].append(trial['date'])

                # Ajouter les détails de l'essai clinique dans "clinical_trials"
                entry = {
                    "title": trial['scientific_title'],
                    "date": trial['date']
                }
                if entry not in graph[original_drug]["clinical_trials"]:  # Éviter les doublons
                    graph[original_drug]["clinical_trials"].append(entry)

        # Supprimer les doublons dans les journaux (dates)
        for journal in graph[original_drug]["journal"]:
            graph[original_drug]["journal"][journal] = list(set(graph[original_drug]["journal"][journal]))
    return graph



