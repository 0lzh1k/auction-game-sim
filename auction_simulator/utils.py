import numpy as np
import pandas as pd
from typing import List, Dict, Any


def generate_random_valuations(num_bidders: int, distribution: str = "uniform", 
                             low: float = 0, high: float = 100, 
                             mean: float = 50, std: float = 15) -> List[float]:

    if distribution == "uniform":
        return np.random.uniform(low, high, num_bidders).tolist()
    elif distribution == "normal":
        valuations = np.random.normal(mean, std, num_bidders)
        return np.maximum(valuations, 0).tolist()
    else:
        raise ValueError(f"Unknown distribution: {distribution}")




def results_to_dataframe(results: List[Any]) -> pd.DataFrame:

    data = []
    for i, result in enumerate(results):
        data.append({
            'simulation_id': i,
            'winner_id': result.winner.agent_id,
            'winner_valuation': result.winner.valuation,
            'winner_strategy': result.winner.strategy,
            'winner_bid': result.winner.bid,
            'payment': result.payment,
            'revenue': result.revenue,
            'efficiency': result.efficiency,
            'winner_payoff': result.winner.payoff
        })
    
    return pd.DataFrame(data)


def calculate_strategy_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    stats = {}
    
    for strategy in df['winner_strategy'].unique():
        strategy_data = df[df['winner_strategy'] == strategy]
        
        stats[strategy] = {
            'win_rate': len(strategy_data) / len(df),
            'avg_payoff': strategy_data['winner_payoff'].mean(),
            'avg_bid': strategy_data['winner_bid'].mean(),
            'avg_valuation': strategy_data['winner_valuation'].mean(),
            'total_wins': len(strategy_data)
        }
    
    return stats


def calculate_auction_efficiency(results: List[Any]) -> Dict[str, float]:
    efficiencies = [r.efficiency for r in results]
    
    return {
        'average_efficiency': np.mean(efficiencies),
        'efficiency_std': np.std(efficiencies),
        'perfect_efficiency_rate': np.mean([e == 1.0 for e in efficiencies])
    }


def format_currency(amount: float) -> str:
    return f"${amount:.2f}"


def format_percentage(value: float) -> str:
    return f"{value * 100:.1f}%"
