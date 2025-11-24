import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import pandas as pd

client = TestClient(app)

@pytest.fixture
def mock_df_prices():
    data = {
        "AAPL": [100, 101, 102],
        "MSFT": [200, 202, 204]
    }
    return pd.DataFrame(data)

# --- Test endpoint /calculate ---
def test_calculate_success(mock_df_prices):
    with patch("app.services.data_fetcher.data_fetch", return_value=mock_df_prices):
        response = client.get("/calculate?symbols=AAPL,MSFT&period=6mo")
        assert response.status_code == 200
        json_data = response.json()
        assert "sharpe_ratios" in json_data
        assert "volatility" in json_data
        assert json_data["query_symbols"] == ["AAPL", "MSFT"]

def test_calculate_no_symbols():
    response = client.get("/calculate?symbols=&period=6mo")
    assert response.status_code == 400
    assert "Veuillez fournir au moins un symbole" in response.json()["detail"]

def test_calculate_data_empty():
    with patch("app.services.data_fetcher.data_fetch", return_value=pd.DataFrame()):
        response = client.get("/calculate?symbols=AAPL&period=6mo")
        assert response.status_code == 404
        assert "Impossible de récupérer les données" in response.json()["detail"]


# --- Test endpoint /metrics_image ---
def test_metrics_image_success(mock_df_prices):
    with patch("app.services.data_fetcher.data_fetch", return_value=mock_df_prices), \
         patch("app.services.visualization.plot_cum_rendement_et_volatilite", return_value="fake_base64_string"):
        response = client.get("/metrics_image?symbols=AAPL,MSFT&period=6mo")
        assert response.status_code == 200
        json_data = response.json()
        assert "image_base64" in json_data
        assert json_data["image_base64"] == "fake_base64_string"

def test_metrics_image_no_symbols():
    response = client.get("/metrics_image?symbols=&period=6mo")
    assert response.status_code == 400
    assert "Veuillez fournir au moins un symbole" in response.json()["detail"]

def test_metrics_image_data_empty():
    with patch("app.services.data_fetcher.data_fetch", return_value=pd.DataFrame()):
        response = client.get("/metrics_image?symbols=AAPL&period=6mo")
        assert response.status_code == 404
        assert "Impossible de récupérer les données" in response.json()["detail"]
