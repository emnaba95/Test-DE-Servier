import os
from src.data_loader import load_json

import json

def find_related_drugs(graph, target_drug):
    """
    Trouve les médicaments mentionnés dans les mêmes journaux que le médicament donné,
    via les publications PubMed uniquement.

    Args:
        graph (dict): Graphe contenant les relations entre médicaments, journaux et dates.
        target_drug (str): Le médicament cible.

    Returns:
        set: Ensemble des médicaments mentionnés par les mêmes journaux que le médicament cible (PubMed uniquement).
    """
    if target_drug not in graph:
        print(f"Le médicament '{target_drug}' n'existe pas dans le graphe.")
        return set()

    # Récupérer les journaux où le médicament cible est mentionné via PubMed
    target_journals = set(graph[target_drug]["journal"].keys())

    # Trouver les autres médicaments mentionnés dans ces journaux via PubMed
    related_drugs = set()
    for drug, data in graph.items():
        if drug == target_drug:
            continue  # Ne pas inclure le médicament cible lui-même

        # Vérifier si un journal en commun via PubMed
        common_journals = target_journals.intersection(data["journal"].keys())
        if common_journals:
            related_drugs.add(drug)
    return sorted(related_drugs)  # Trier les résultats pour une meilleure lisibilité

# Charger le fichier JSON
graph = load_json(os.path.join("output/result.json"))

# Trouver les médicaments liés à "diphenhydramine"
target_drug = "atropine"
related_drugs = find_related_drugs(graph, target_drug)

# Afficher les résultats
if not related_drugs:
    # Message à retourner si aucun médicament n'est trouvé
    print(f"Aucun autre médicament n'est mentionné dans les mêmes journaux que '{target_drug}' (PubMed uniquement).")
else : 
    print(f"Médicaments liés à '{target_drug}' (PubMed uniquement) : {related_drugs}")
