
def nunique_per_cat(df):
    cat_cols = [(col, df[col].nunique()) for col in df.columns if df[col].dtype == 'object']
    return cat_cols


def min_max_for_cols(df):
    for col in df.select_dtypes(include=[int, float]).columns:
        print(f"{col} - min: {df[col].min()}, max: {df[col].max()}")