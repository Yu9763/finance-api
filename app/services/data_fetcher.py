import yfinance as yf
import pandas as pd

def data_fetch(symboles: list[str], period: str = "6mo") :
    try:
        tickers_string = " ".join(symboles)
        data = yf.download(tickers=tickers_string, period=period, interval="1d", progress=False)

        if data.empty:
            return pd.DataFrame()
        if isinstance(data.columns, pd.MultiIndex):
            if 'Adj Close' in data.columns.levels[0]:
                data = data['Adj Close']
            elif 'Close' in data.columns.levels[0]:
                data = data['Close']
            else:
                raise ValueError(f"'Adj Close' ou 'Close' non trouvées : {data.columns}")
        else:
            if 'Adj Close' in data.columns:
                data = pd.DataFrame(data['Adj Close'])
            elif 'Close' in data.columns:
                data = pd.DataFrame(data['Close'])
            else:
                raise ValueError(f"'Adj Close' ou 'Close' non trouvées : {data.columns}")

        # Assure que les colonnes correspondent aux symboles
        if len(symboles) == 1:
            data.columns = symboles

        return data

    except Exception as e:
        raise ValueError(f"Erreur lors de la récupération des données pour {symboles} : {e}")
