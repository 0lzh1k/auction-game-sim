"""
Game logic for Auction Strategy Game Simulator
"""
from auction_simulator import Agent, AuctionSimulator, get_available_strategies
from typing import Dict, Any, List
import pandas as pd
import numpy as np

def run_auction_simulation(auction_type: str, num_bidders: int, num_simulations: int,
                          valuation_dist: str, valuation_params: Dict[str, float],
                          strategies: List[str]):
    simulator = AuctionSimulator()
    results = simulator.run_simulation(
        auction_type=auction_type,
        num_bidders=num_bidders,
        num_simulations=num_simulations,
        valuation_distribution=valuation_dist,
        valuation_params=valuation_params,
        strategies=strategies
    )
    return results

def create_results_dataframe(auction_results: List[Any]) -> pd.DataFrame:
    data = []
    for i, result in enumerate(auction_results):
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