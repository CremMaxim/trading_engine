import httpx
import pandas as pd

async def fetch_ohlcv(symbol: str) -> pd.DataFrame:
    url = f"http://localhost:8080/api/v1/market-data/{symbol}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Parse the JSON response into a Pandas DataFrame
        df = pd.DataFrame(data)
        
        # Convert the time column to datetime and set it as the index
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            
        # Ensure price columns are floats
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)
                
        # Ensure volume is float
        if 'volume' in df.columns:
            df['volume'] = df['volume'].astype(float)
            
        return df
