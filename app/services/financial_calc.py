import numpy as np
import pandas as pd
from app.core.config import Settings

settings = Settings()

def rendement_journalier(df_prix: pd.DataFrame) :
    rendement_data_prix = df_prix.pct_change()
    rendement_data_prix = rendement_data_prix.fillna(0)
    return rendement_data_prix

def volatilite(rendement_data_prix: pd.DataFrame) :
    deviation_standard = rendement_data_prix.std()
    annualisation = deviation_standard * np.sqrt(252)
    return annualisation

def ratio_sharp(rendement_data_prix, RISK_FREE_RATE: float = settings.RISK_FREE_RATE) :
    moyenne_rendement_quotidien = rendement_data_prix.mean()
    annualisation_moyenne = moyenne_rendement_quotidien * 252
    annualised_volatility = volatilite(rendement_data_prix)
    ratio_de_sharpe = (annualisation_moyenne - RISK_FREE_RATE) / annualised_volatility
    return ratio_de_sharpe
