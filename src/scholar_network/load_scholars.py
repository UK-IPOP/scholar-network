import pandas as pd


def load() -> pd.DataFrame:
    """Loads COP scholar dataframe.

    Returns:
        df: pandas dataframe for scholars
    """
    df = pd.read_csv('../../data/COPscholars.csv')
    return df

