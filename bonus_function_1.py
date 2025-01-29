import os
from collections import defaultdict
from src.data_loader import load_json

def journal_with_most_drugs(graph):
    """
    Trouve le journal qui mentionne le plus de médicaments différents.

    Args:
        graph (dict): Graphe contenant les relations entre médicaments, journaux et dates.

    Returns:
        str: Nom du journal qui mentionne le plus de médicaments différents.
    """
    journal_drug_count = defaultdict(set)  # Pour stocker les médicaments mentionnés par chaque journal

    for drug, data in graph.items():
        for journal, dates in data["journal"].items():
            journal_drug_count[journal].add(drug)

    # Calculer le journal avec le plus grand nombre de médicaments
    max_journal = max(journal_drug_count, key=lambda j: len(journal_drug_count[j]))
    return max_journal, len(journal_drug_count[max_journal])

journal, drug_count = journal_with_most_drugs(load_json(os.path.join("output/result.json")))
print(f"Le journal qui mentionne le plus de médicaments est '{journal}' avec {drug_count} médicaments.")
