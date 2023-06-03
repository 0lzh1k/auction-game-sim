"""
UI for Auction Strategy Game Simulator
"""
import streamlit as st
import numpy as np
from game_logic import run_auction_simulation, create_results_dataframe, calculate_strategy_stats
from auction_simulator import get_available_strategies
from visualizations import (
    plot_bid_distribution, plot_revenue_comparison, plot_strategy_performance,
    plot_efficiency_over_time, plot_bid_vs_valuation, create_summary_metrics_display,
    plot_auction_comparison
)


if __name__ == "__main__":
    main()
