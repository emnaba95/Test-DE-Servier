import pandas as pd
from dateutil import parser

def remove_duplicates(df):
    """
    Supprime les doublons d'un DataFrame.

    Args:
        df (pd.DataFrame): Le DataFrame à traiter.

    Returns:
        pd.DataFrame: DataFrame sans doublons.
    """
    return df.drop_duplicates()


def clean_text_columns(df, exclude_columns=None):
    """
    Nettoie les colonnes de type texte en supprimant les espaces inutiles 
    et en convertissant le contenu en minuscules, tout en ayant la possibilité d'eclure certaines colonnes.

    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer.
        exclude_columns (list, optional): Liste des colonnes à exclure du nettoyage. 
                                          Par défaut, aucune colonne n'est exclue.

    Returns:
        pd.DataFrame: DataFrame avec colonnes de texte nettoyées.
    """
    # Liste des colonnes à exclure du nettoyage
    if exclude_columns is None:
        exclude_columns = []

    for col in df.select_dtypes(include=['object']).columns:
        if col not in exclude_columns:
            # Appliquer le nettoyage uniquement sur les colonnes non exclues
            df[col] = df[col].str.strip()  # Supprime les espaces en début/fin
            df[col] = df[col].str.lower()  # Convertit en minuscules
    
    return df

def parse_dates_with_dateutil(df, date_columns, default_value=None):
    """
    Uniformiser les dates des différentes sources de données
    Utilise dateutil.parser pour détecter et convertir automatiquement les dates.

    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer.
        date_columns (list): Colonnes contenant les dates à convertir.
        default_value (any, optional): Valeur par défaut pour les dates non convertibles.

    Returns:
        pd.DataFrame: DataFrame avec dates formatées.
    """
    for col in date_columns:
        def safe_parse(date):
            try:
                # Utilisation de dateutil.parser avec l'option dayfirst (convention européenne)
                return parser.parse(date, dayfirst=True).date() 
            except (ValueError, TypeError):
                return default_value

        df[col] = df[col].apply(safe_parse)
    
    return df


def resolve_duplicates(df, subset):
    """
    Résout les doublons dans un DataFrame en utilisant des colonnes spécifiques.
    Fusion entre les lignes en doublons.

    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer.
        subset (list): Liste des colonnes à utiliser pour identifier les doublons.
    
    Returns:
        pd.DataFrame: Le DataFrame sans doublons, en fusionannt les eventuels doublons ayant des données manquantes.
    """
    # Sauvegarder l'ordre original des colonnes
    original_columns = df.columns.tolist()
    
    # Identifier les lignes avec des doublons sur les colonnes spécifiées
    duplicates = df[df.duplicated(subset=subset, keep=False)]
    
    # Créer une liste pour stocker les lignes fusionnées
    resolved_rows = []
    keys_processed = set()
    
    # Grouper par les colonnes spécifiées (subset)
    for _, group in duplicates.groupby(subset):
        key = tuple(group[subset].iloc[0])
        if key not in keys_processed:
            # Fusionner les lignes en conservant les valeurs non nulles
            merged_row = group.ffill().bfill().iloc[0]  # Prioriser les valeurs non nulles
            resolved_rows.append(merged_row)
            keys_processed.add(key)
    
    # Convertir les lignes résolues en DataFrame
    resolved_df = pd.DataFrame(resolved_rows)
    
    # Supprimer les doublons et ajouter les lignes résolues
    df = df.drop_duplicates(subset=subset, keep=False)
    df = pd.concat([df, resolved_df], ignore_index=True)
    
    # Réorganiser les colonnes dans l'ordre original
    df = df[original_columns] 
    
    return df

def clean_data_pipeline(df, date_columns=None, exclude_columns=None, unique_subset=None):
    """
    Pipeline pour nettoyer un DataFrame en appliquant toutes les étapes nécessaires.

    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer.
        date_columns (list, optional): Liste des colonnes contenant des dates à convertir.
        exclude_columns (list, optional): Liste des colonnes à exclure du nettoyage textuel.
        unique_subset (list, optional): Colonnes à utiliser pour identifier et résoudre les doublons.

    Returns:
        pd.DataFrame: DataFrame nettoyé après application des étapes de nettoyage (duplication, texte, dates).
    """

    # Supprimer les doublons
    df = remove_duplicates(df)
    # Résoudre les doublons spécifiques (proposition de règle à valider)
    if unique_subset:
        df = resolve_duplicates(df, unique_subset)
    # Nettoyer les colonnes texte
    if exclude_columns:
        df = clean_text_columns(df, exclude_columns)
    # Nettoyer les colonnes date
    if date_columns:
        df = parse_dates_with_dateutil(df, date_columns)
    
    return df


def save_cleaned_data(df, output_path):
    """
    Enregistre un DataFrame nettoyé au format CSV.

    Args:
        df (pd.DataFrame): Le DataFrame à enregistrer.
        output_path (str): Chemin complet pour enregistrer le fichier CSV.

    Raises:
        ValueError: Si une erreur survient lors de l'enregistrement.
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"Fichier nettoyé enregistré : {output_path}")
    except Exception as e:
        raise ValueError(f"Erreur lors de l'enregistrement du fichier : {e}")
