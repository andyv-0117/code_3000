import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    merged = pd.merge(
        anon_df,
        aux_df,
        on=["age", "zip3", "gender"],
        how="inner"
    )
    unique_matches = merged.groupby("anon_id").filter(lambda x: len(x) == 1)
    matches = unique_matches[["anon_id", "name"]].rename(columns={"name": "matched_name"})

    return matches


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    matches = len(matches_df)
    total = len(anon_df)

    return matches / total
