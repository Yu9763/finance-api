from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from app.services.data_fetcher import data_fetch
from app.services.financial_calc import rendement_journalier, volatilite, ratio_sharp
from app.services.visualization import plot_cum_rendement_et_volatilite
import traceback

router = APIRouter()

@router.get("/calculate")
async def calculate(symbols: str = Query(..., description="Liste des symboles boursiers séparés par des virgules"),
                    period: str = Query("6mo", description="Période historique à télécharger (ex: 1y, 6mo, 30d)")):
    symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]
    if not symbol_list:
        raise HTTPException(status_code=400, detail="Veuillez fournir au moins un symbole boursier valide.")

    try:
        df_prix = data_fetch(symbol_list, period=period)
        if df_prix.empty:
            raise HTTPException(
                status_code=404,
                detail=f"Impossible de récupérer les données pour les symboles: {', '.join(symbol_list)}"
            )

        df_rendements = rendement_journalier(df_prix)
        annualized_volatility = volatilite(df_rendements)
        sharpe_ratios = ratio_sharp(df_rendements)

        final_volatility = {symbol: round(vol, 4) for symbol, vol in annualized_volatility.to_dict().items()}
        final_sharpe_ratios = {symbol: round(ratio, 4) for symbol, ratio in sharpe_ratios.to_dict().items()}

        return {
            "query_symbols": symbol_list,
            "period": period,
            "sharpe_ratios": final_sharpe_ratios,
            "volatility": final_volatility,
            "message": "Calculs financiers réussis."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}\n{traceback.format_exc()}")


@router.get("/metrics_image")
async def metrics_image(symbols: str = Query(...), period: str = Query("6mo")):
    symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]
    if not symbol_list:
        raise HTTPException(status_code=400, detail="Veuillez fournir au moins un symbole boursier valide.")

    try:
        df_prix = data_fetch(symbol_list, period)
        if df_prix.empty:
            raise HTTPException(status_code=404,
                                detail=f"Impossible de récupérer les données pour les symboles: {', '.join(symbol_list)}")
        img_base64 = plot_cum_rendement_et_volatilite(df_prix)
        return JSONResponse(content={"image_base64": img_base64})
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Erreur interne lors de la génération du graphique : {str(e)}")
