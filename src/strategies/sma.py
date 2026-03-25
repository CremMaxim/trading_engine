import pandas as pd
import vectorbt as vbt

def run_sma_crossover(close_prices: pd.Series, fast_window: int = 10, slow_window: int = 50) -> dict:
    """
    Executes an SMA crossover backtest on the provided close prices.
    """
    # Calculate fast and slow Simple Moving Averages
    fast_ma = vbt.MA.run(close_prices, window=fast_window)
    slow_ma = vbt.MA.run(close_prices, window=slow_window)
    
    # Generate entries (fast > slow) and exits (fast < slow)
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)
    
    # Run the portfolio simulation
    portfolio = vbt.Portfolio.from_signals(
        close_prices,
        entries,
        exits,
        init_cash=10000.0,
        fees=0.001  # optional standard feeling 0.1% fee
    )
    
    # Extract statistics
    stats = portfolio.stats()
    
    # Handle potentially missing metrics gracefully
    d = stats.to_dict()
    
    total_return = d.get('Total Return [%]', 0.0)
    win_rate = d.get('Win Rate [%]', 0.0)
    total_trades = d.get('Total Trades', 0)
    
    return {
        "total_return": total_return,
        "win_rate": win_rate,
        "total_trades": total_trades,
        "max_drawdown": d.get('Max Drawdown [%]', 0.0),
        "sharpe_ratio": d.get('Sharpe Ratio', 0.0)
    }
