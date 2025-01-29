# Test Servier

Ce projet inclut un pipeline de données en Python, des requêtes SQL, et des fonctions ad hoc pour analyser les relations entre des médicaments, des journaux scientifiques, et des publications.


### Structure du projet
```
│  
├── data/                                  # Dossier contenant les données en entrée : des fichiers CSV/JSON  
│   ├── drugs.csv
│   ├── pubmed.csv
│   ├── pubmed.json
│   ├── clinical_trials.csv
│  
├── output/                                # Contient les fichiers nettoyés et les résultats générés par le pipeline.  
│   ├── clinical_tials_cleaned.csv
│   ├── drugs_cleaned.csv
│   ├── pubmed_cleaned.csv
│   ├── result.json  
│  
├── sql/                                   # Contient les requêtes SQL.  
│   ├── requete_1.py                       # Requête pour calculer le chiffre d'affaires journalier.  
│   ├── requete_2.py                       # Requête pour calculer les ventes par type de produit et client.  
│  
├── src/  
│   ├── data_loader.py                     # Gestion du chargement des données  
│   ├── data_cleaner.py                    # Nettoyage des données  
│   ├── graph_builder.py                   # Construction du graphe  
│  
├── tests/  
│   ├── test_parse_dates_with_dateutil.py  # Tests unitaires pour la fonction parse_dates_with_dateutil dans data_cleaner.py  
│  
│── bonus_function_1.py                    # Identifie le journal mentionnant le plus de médicaments différents.  
│── bonus_function_2.py                    # Trouve les médicaments mentionnés dans les mêmes journaux pour PubMed uniquement, sans prendre en compte les essais cliniques.  
│── main.py                                # Point d'entrée principal  
├── README.md                              # Documentation du projet  
└── requirements.txt                       # Dépendances Python  
```

### Créez un environnement virtuel : 

- `python3 -m venv venv`  
- `source venv/bin/activate`  # Sur Linux/Mac  
- `.\venv\Scripts\activate`  # Sur Windows  

### Installez les dépendances :  

- `pip install -r requirements.txt`  

### Execution du pipeline principal :  
Lancez le pipeline de nettoyage et de génération du graphe depuis le fichier main.py :  
- `python main.py`  
Les fichiers nettoyés seront générés dans le dossier output/.  
Le graphe final sera sauvegardé sous output/result.json.  

### Exécution des tests :  
Lancez les tests unitaires :  
- `python -m unittest discover tests`  
Tests unitaires réalisés pour une seule fonction.  

### Nettoyage des données :  
Le module data_cleaner.py est responsable du nettoyage et de la préparation des données brutes.  
Voici les principales étapes du pipeline :  

- Suppression des doublons :  
  - La fonction remove_duplicates élimine les doublons simples du DataFrame.  
  - La fonction resolve_duplicates fusionne les doublons complexes en priorisant les valeurs non nulles sur un sous-ensemble de colonnes spécifiées.  
  Dans ce travail, deux enregistrements ayant le même titre à la même date sont considérés comme identiques et fusionnés en un seul. Exemple : les lignes 7 et 8 de clinical_trials.csv.  

- Nettoyage des colonnes texte :  
  - La fonction clean_text_columns supprime les espaces inutiles et convertit les textes en minuscules.  
- Uniformisation des dates :  
  - La fonction parse_dates_with_dateutil utilise dateutil pour convertir les dates dans un format standardisé.
- Pipeline global :  
  - La fonction clean_data_pipeline orchestre toutes ces étapes en appliquant :  
    La suppression et la résolution des doublons.  
    Le nettoyage des colonnes texte.  
    La conversion des dates.  
    Retourne un DataFrame nettoyé, prêt à être analysé ou exporté.  
- Exportation des données nettoyées :  
  - save_cleaned_data sauvegarde le DataFrame final au format CSV.  

#### Améliorations à faire :

- Suppression des colonnes inutiles : Conserver uniquement les colonnes nécessaires (drug, title, date, journal) pour réduire la taille des fichiers et optimiser les performances.
- Traiter les valeurs manquantes :
  - Remplacer les valeurs manquantes par des valeurs par défaut ou calculées.
  - Suppression des lignes incomplètes : Si les valeurs manquantes sont trop nombreuses ou si les colonnes sont critiques pour l'analyse, les lignes concernées peuvent être supprimées.

### Les requêtes SQL demandées se situe dans le dossier SQL

### Exécution des fonctions bonus :

- Fonction pour identifier le journal mentionnant le plus de médicaments :  
  - `python bonus_function_1.py`  
Sortie : Nom du journal et le nombre de médicaments.  

- Fonction pour trouver les médicaments liés à un journal donné (PubMed uniquement) :  
  - `python bonus_function_2.py`  
Vous pouvez modifier le nom du médicament cible directement dans le fichier bonus_function_2.py.  


###  Gestion d'une plus grande quantité de données

Afin de traiter une grand volumétrie de données, la gestion mémoire, l’optimisation du stockage, et l’exécution distribuée deviennent essentielles.  
L’utilisation de formats comme Parquet ou Avro permet une meilleure compression et un accès plus rapide aux données. Pour le traitement, remplacer Pandas par PySpark permet d'exécuter les calculs en parallèle et d'éviter les limitations mémoire en chargeant les fichiers en chunks.  
Pour optimiser les requêtes, il est essentiel de réduire les jointures, d'utiliser des index et des précalculs, tout en limitant les opérations coûteuses en mémoire comme groupby et merge.  
L’automatisation du pipeline avec Apache Airflow permet une exécution efficace et une ingestion incrémentale des nouvelles données.  
Enfin, pour gérer des volumétries massives, il est préférable d’adopter une infrastructure distribuée, en exploitant un cluster Spark/Hadoop ou des bases analytiques comme BigQuery, offrant une scalabilité et une exécution optimisée des requêtes.  
