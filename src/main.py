from fastapi import FastAPI, HTTPException
from src.data.client import fetch_ohlcv
from src.strategies.sma import run_sma_crossover
import httpx
import math

app = FastAPI(title="Python Quantitative Engine", version="1.0.0")

@app.get("/api/v1/backtest/sma/{symbol}")
async def backtest_sma(symbol: str, fast_window: int = 10, slow_window: int = 50):
    try:
        # 1. Fetch OHLCV data
        df = await fetch_ohlcv(symbol)
        
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
            
        if 'close' not in df.columns:
            raise HTTPException(status_code=400, detail="Data must contain 'close' column")
            
        # 2. Extract close prices and run strategy
        close_prices = df['close']
        results = run_sma_crossover(
            close_prices=close_prices,
            fast_window=fast_window,
            slow_window=slow_window
        )
        
        # Coerce any potential NaN values to None for JSON compliance
        clean_results = {
            k: (None if isinstance(v, float) and math.isnan(v) else v)
            for k, v in results.items()
        }
        
        # 3. Return results
        return clean_results
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
