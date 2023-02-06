import numpy as np
from typing import List, Tuple, Dict, Any
from .agents import Agent


class AuctionResult:
    
    def __init__(self, winner: Agent, payment: float, all_bids: List[float], 
                 revenue: float, efficiency: float):
        self.winner = winner
        self.payment = payment
        self.all_bids = all_bids
        self.revenue = revenue
        self.efficiency = efficiency


class Auction:
    
    def __init__(self, auction_type: str):
        self.auction_type = auction_type
        self.agents = []
        self.result = None
    
    def add_agents(self, agents: List[Agent]):
        self.agents = agents
    
    def run_auction(self) -> AuctionResult:
        if not self.agents:
            raise ValueError("No agents in auction")
        
        for agent in self.agents:
            agent.reset()
        
        bids = []
        for agent in self.agents:
            bid = agent.place_bid(self.auction_type, len(self.agents))
            bids.append(bid)
        
        winner, payment = self._determine_winner_and_payment(bids)
        
        for agent in self.agents:
            if agent == winner:
                agent.won = True
                agent.calculate_payoff(payment)
            else:
                agent.calculate_payoff(0)
        
        efficiency = self._calculate_efficiency(winner)
        
        self.result = AuctionResult(
            winner=winner,
            payment=payment,
            all_bids=bids,
            revenue=payment,
            efficiency=efficiency
        )
        
        return self.result
    
   
    def _first_price_winner_payment(self, bids: List[float]) -> Tuple[Agent, float]:
        winner_idx = np.argmax(bids)
        winner = self.agents[winner_idx]
        payment = bids[winner_idx]
        return winner, payment
    
    def _second_price_winner_payment(self, bids: List[float]) -> Tuple[Agent, float]:
        sorted_indices = np.argsort(bids)[::-1]
        winner_idx = sorted_indices[0]
        winner = self.agents[winner_idx]
        
        if len(bids) > 1:
            payment = bids[sorted_indices[1]]
        else:
            payment = 0
        
        return winner, payment
    
    def _calculate_efficiency(self, winner: Agent) -> float:
        highest_valuation_agent = max(self.agents, key=lambda x: x.valuation)
        return 1.0 if winner == highest_valuation_agent else 0.0


class AuctionSimulator:
    
    def __init__(self):
        self.results_history = []
    
    def run_simulation(self, auction_type: str, num_bidders: int, num_simulations: int,
                      valuation_distribution: str = "uniform", 
                      valuation_params: Dict[str, float] = None,
                      strategies: List[str] = None) -> Dict[str, Any]:
        if valuation_params is None:
            valuation_params = {"low": 0, "high": 100}
        
        if strategies is None:
            strategies = ["truthful"] * num_bidders
        
        results = []
        
        for sim in range(num_simulations):
            valuations = self._generate_valuations(
                num_bidders, valuation_distribution, valuation_params
            )
            
            agents = []
            for i in range(num_bidders):
                strategy = strategies[i % len(strategies)]
                agent = Agent(i, valuations[i], strategy)
                agents.append(agent)
            
            auction = Auction(auction_type)
            auction.add_agents(agents)
            result = auction.run_auction()
            results.append(result)
        
        aggregated = self._aggregate_results(results, auction_type)
        self.results_history.extend(results)
        
        return aggregated
    
    def _generate_valuations(self, num_bidders: int, distribution: str, 
                           params: Dict[str, float]) -> List[float]:
        if distribution == "uniform":
            low = params.get("low", 0)
            high = params.get("high", 100)
            return np.random.uniform(low, high, num_bidders).tolist()
        elif distribution == "normal":
            mean = params.get("mean", 50)
            std = params.get("std", 15)
            valuations = np.random.normal(mean, std, num_bidders)
            return np.maximum(valuations, 0).tolist()
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
    
    def _aggregate_results(self, results: List[AuctionResult], auction_type: str) -> Dict[str, Any]:
        revenues = [r.revenue for r in results]
        efficiencies = [r.efficiency for r in results]
        
        strategy_wins = {}
        strategy_payoffs = {}
        
        for result in results:
            winner_strategy = result.winner.strategy
            strategy_wins[winner_strategy] = strategy_wins.get(winner_strategy, 0) + 1
            
            pass
        
        return {
            "auction_type": auction_type,
            "num_simulations": len(results),
            "average_revenue": np.mean(revenues),
            "revenue_std": np.std(revenues),
            "average_efficiency": np.mean(efficiencies),
            "efficiency_std": np.std(efficiencies),
            "all_revenues": revenues,
            "all_efficiencies": efficiencies,
            "results": results
        }
