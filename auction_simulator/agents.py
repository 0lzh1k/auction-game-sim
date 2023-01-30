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
    
