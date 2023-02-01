import numpy as np
from typing import Dict, Any


class Agent:
    
    def __init__(self, agent_id: int, valuation: float, strategy: str = "truthful"):
        self.agent_id = agent_id
        self.valuation = valuation
        self.strategy = strategy
        self.bid = 0.0
        self.payoff = 0.0
        self.won = False
    
    def place_bid(self, auction_type: str, num_bidders: int, **kwargs) -> float:
        from .strategies import BiddingStrategy
        
        strategy_obj = BiddingStrategy(self.strategy)
        self.bid = strategy_obj.calculate_bid(
            valuation=self.valuation,
            auction_type=auction_type,
            num_bidders=num_bidders,
            **kwargs
        )
        return self.bid
    
    def calculate_payoff(self, payment: float) -> float:
        if self.won:
            self.payoff = self.valuation - payment
        else:
            self.payoff = 0.0
        return self.payoff
    
    def reset(self):
        self.bid = 0.0
        self.payoff = 0.0
        self.won = False
    
    def __repr__(self):
        return f"Agent({self.agent_id}, v={self.valuation:.2f}, bid={self.bid:.2f})"
