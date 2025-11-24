import pandas as pd
import numpy as np
import pytest
from pandas.testing import assert_series_equal
from app.services.financial_calc import (
    rendement_journalier,
    volatilite,
    ratio_sharp
)

@pytest.fixture
def prix_dataframe_simple():
    return pd.DataFrame({
        'SYM_A': [100.0, 110.0, 99.0]
    })

@pytest.fixture
def rendements_dataframe_simple():
    return pd.DataFrame({
        'SYM_A': [0.0, 0.1, -0.1] 
    })

def test_rendement_journalier_calcul_correct(prix_dataframe_simple, rendements_dataframe_simple):
    rendements_obtenus = rendement_journalier(prix_dataframe_simple)
    
    try:
        assert_series_equal(
            rendements_obtenus['SYM_A'], 
            rendements_dataframe_simple['SYM_A'],
            check_names=True,
            atol=1e-6
        )
    except AssertionError as e:
        pytest.fail(f"Le calcul de rendement est incorrect. Détails : {e}")

    assert rendements_obtenus['SYM_A'].iloc[0] == 0.0

def test_volatilite_calcul_et_annualisation_corrects(rendements_dataframe_simple):
    ecart_type_attendu = np.std(rendements_dataframe_simple['SYM_A'], ddof=1)
    
    volatilite_attendue = ecart_type_attendu * np.sqrt(252)
    
    volatilite_obtenue = volatilite(rendements_dataframe_simple)

    assert np.isclose(volatilite_obtenue['SYM_A'], volatilite_attendue), \
        "La volatilité annualisée n'est pas calculée correctement."
    assert volatilite_obtenue['SYM_A'] > 0

def test_ratio_sharp_formule_correcte(rendements_dataframe_simple):
    taux_sans_risque = 0.02
    
    moyenne_quotidienne = rendements_dataframe_simple['SYM_A'].mean()
    rendement_annuel_attendu = moyenne_quotidienne * 252
    
    volatilite_annuelle = volatilite(rendements_dataframe_simple)['SYM_A']
    
    ratio_sharpe_attendu = (rendement_annuel_attendu - taux_sans_risque) / volatilite_annuelle
    
    ratio_sharpe_obtenu = ratio_sharp(rendements_dataframe_simple, RISK_FREE_RATE=taux_sans_risque)
    
    assert np.isclose(ratio_sharpe_obtenu['SYM_A'], ratio_sharpe_attendu), \
        "Le Ratio de Sharpe n'est pas calculé correctement selon la formule standard."