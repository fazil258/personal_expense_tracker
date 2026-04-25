import pandas as pd

def enrich_with_category(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:

    desc_category_map = dict(
        zip(df_b['description'], df_b['category'])
    )
    desc_type_map = dict(
        zip(df_b['description'], df_b['transaction_type'])
    )
    
    df_a = df_a.copy()
    df_a['category'] = df_a['description'].map(desc_category_map)
    df_a['transaction_type'] = df_a['description'].map(desc_type_map)
    
    return df_a
