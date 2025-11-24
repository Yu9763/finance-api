import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
import io
from app.services.financial_calc import rendement_journalier

def plot_cum_rendement_et_volatilite(df_prix: pd.DataFrame, rolling_window: int = 20) :
    df_rendements = rendement_journalier(df_prix)
    df_cum_rendement = (1 + df_rendements).cumprod() - 1
    df_volatilite = df_rendements.rolling(window=rolling_window).std() * np.sqrt(252)

    plt.figure(figsize=(12, 6))
    for s in df_cum_rendement.columns:
        plt.plot(df_cum_rendement.index, df_cum_rendement[s], label=f"{s} Rendement cumulé")
    for s in df_volatilite.columns:
        plt.plot(df_volatilite.index, df_volatilite[s], linestyle="--", label=f"{s} Volatilité")

    plt.title("Rendement cumulé et Volatilité")
    plt.xlabel("Date")
    plt.ylabel("Valeur")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close()
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64
