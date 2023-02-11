"""
Bidding strategies for auction agents.
"""

import numpy as np
from typing import Dict, Any


class BiddingStrategy:
    
    def __init__(self, strategy_name: str):
        self.strategy_name = strategy_name
    
    def calculate_bid(self, valuation: float, auction_type: str, num_bidders: int, **kwargs) -> float:
        if self.strategy_name == "truthful":
            return self._truthful_bid(valuation, auction_type)
        elif self.strategy_name == "aggressive":
            return self._aggressive_bid(valuation, auction_type, num_bidders)
        elif self.strategy_name == "conservative":
            return self._conservative_bid(valuation, auction_type, num_bidders)
        elif self.strategy_name == "random":
            return self._random_bid(valuation)
        elif self.strategy_name == "optimal_first_price":
            return self._optimal_first_price_bid(valuation, num_bidders)
        else:
            return self._truthful_bid(valuation, auction_type)
    
    def _truthful_bid(self, valuation: float, auction_type: str) -> float:
        return valuation
    
    def _aggressive_bid(self, valuation: float, auction_type: str, num_bidders: int) -> float:
        if auction_type == "second_price":
            return valuation
        else:
            return min(valuation * 1.1, valuation)
    
    def _conservative_bid(self, valuation: float, auction_type: str, num_bidders: int) -> float:
        if auction_type == "second_price":
            return valuation
        else:
            shade_factor = 0.3 + (0.2 * (num_bidders - 1) / 10)
            return valuation * (1 - shade_factor)
    
    def _random_bid(self, valuation: float) -> float:
        return np.random.uniform(0, valuation)
    
    def _optimal_first_price_bid(self, valuation: float, num_bidders: int) -> float:
        if num_bidders <= 1:
            return valuation
        
        optimal_factor = (num_bidders - 1) / num_bidders
        return valuation * optimal_factor


def get_strategy_description(strategy_name: str) -> str:
    descriptions = {
        "truthful": "Bid exactly your true valuation (optimal for second-price auctions)",
        "aggressive": "Bid higher than normal (risky in first-price auctions)",
        "conservative": "Bid well below valuation to ensure profit if you win",
        "random": "Bid randomly between 0 and your valuation",
        "optimal_first_price": "Use game-theoretic optimal strategy for first-price auctions"
    }
    return descriptions.get(strategy_name, "Unknown strategy")


def get_available_strategies() -> Dict[str, str]:
    return {
        "truthful": get_strategy_description("truthful"),
        "aggressive": get_strategy_description("aggressive"),
        "conservative": get_strategy_description("conservative"),
        "random": get_strategy_description("random"),
        "optimal_first_price": get_strategy_description("optimal_first_price")
    }
