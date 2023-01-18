"""
Visualization functions for auction simulation results.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import List, Dict, Any
import streamlit as st


def plot_bid_distribution(results: List[Any], auction_type: str) -> go.Figure:

    all_bids = []
    for result in results:
        all_bids.extend(result.all_bids)
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=all_bids,
        nbinsx=30,
        name="Bids",
        opacity=0.7
    ))
    
    fig.update_layout(
        title=f"Distribution of Bids - {auction_type.replace('_', ' ').title()} Auction",
        xaxis_title="Bid Amount ($)",
        yaxis_title="Frequency",
        showlegend=False
    )
    
    return fig


def plot_revenue_comparison(simulation_results: Dict[str, Any]) -> go.Figure:
    revenues = simulation_results.get('all_revenues', [])
    
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=revenues,
        name="Revenue Distribution",
        boxpoints='outliers'
    ))
    
    avg_revenue = np.mean(revenues)
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Average: ${avg_revenue:.2f}"
    )
    
    fig.update_layout(
        title="Revenue Distribution",
        yaxis_title="Revenue ($)",
        showlegend=False
    )
    
    return fig


def plot_strategy_performance(df: pd.DataFrame) -> go.Figure:
    strategy_stats = df.groupby('winner_strategy').agg({
        'winner_payoff': ['mean', 'count'],
        'payment': 'mean'
    }).round(2)
    
    strategies = strategy_stats.index.tolist()
    win_counts = strategy_stats[('winner_payoff', 'count')].tolist()
    avg_payoffs = strategy_stats[('winner_payoff', 'mean')].tolist()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Win Count by Strategy', 'Average Payoff by Strategy'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Win counts
    fig.add_trace(
        go.Bar(x=strategies, y=win_counts, name="Wins"),
        row=1, col=1
    )
    
    # Average payoffs
    fig.add_trace(
        go.Bar(x=strategies, y=avg_payoffs, name="Avg Payoff", marker_color='orange'),
        row=1, col=2
    )
    
    fig.update_layout(
        title="Strategy Performance Analysis",
        showlegend=False
    )
    
    return fig


def plot_efficiency_over_time(results: List[Any]) -> go.Figure:
    efficiencies = [r.efficiency for r in results]
    simulation_nums = list(range(1, len(efficiencies) + 1))
    
    window_size = min(50, len(efficiencies) // 10)
    if window_size > 1:
        moving_avg = pd.Series(efficiencies).rolling(window=window_size).mean()
    else:
        moving_avg = efficiencies
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=simulation_nums,
        y=efficiencies,
        mode='markers',
        name='Efficiency',
        opacity=0.5,
        marker=dict(size=4)
    ))
    
    if window_size > 1:
        fig.add_trace(go.Scatter(
            x=simulation_nums,
            y=moving_avg,
            mode='lines',
            name=f'Moving Average ({window_size} sims)',
            line=dict(color='red', width=2)
        ))
    
    fig.update_layout(
        title="Auction Efficiency Over Time",
        xaxis_title="Simulation Number",
        yaxis_title="Efficiency (1 = Perfect)",
        yaxis=dict(range=[0, 1.1])
    )
    
    return fig


