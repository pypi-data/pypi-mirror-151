import pandas as pd

def unpack_column(result: pd.DataFrame, column: str='errors'):
    return pd.concat([result, result[column].apply(lambda row: pd.Series(row[0]) if len(row) >0 else pd.Series(dtype='int64')).fillna("")], axis=1).drop(columns=[column])