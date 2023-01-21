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


def plot_bid_vs_valuation(results: List[Any], auction_type: str) -> go.Figure:
    valuations = []
    bids = []
    strategies = []
    
    for result in results:
        valuations.append(result.winner.valuation)
        bids.append(result.winner.bid)
        strategies.append(result.winner.strategy)
    
    df = pd.DataFrame({
        'valuation': valuations,
        'bid': bids,
        'strategy': strategies
    })
    
    fig = px.scatter(
        df, 
        x='valuation', 
        y='bid',
        color='strategy',
        title=f"Bidding Behavior - {auction_type.replace('_', ' ').title()} Auction",
        labels={'valuation': 'True Valuation ($)', 'bid': 'Bid Amount ($)'}
    )
    
    max_val = max(max(valuations), max(bids))
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        name='Truthful Bidding Line',
        line=dict(dash='dash', color='gray')
    ))
    
    return fig


def create_summary_metrics_display(simulation_results: Dict[str, Any]) -> None:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_revenue = simulation_results.get('average_revenue', 0)
        st.metric("Average Revenue", f"${avg_revenue:.2f}")
    
    with col2:
        avg_efficiency = simulation_results.get('average_efficiency', 0)
        st.metric("Average Efficiency", f"{avg_efficiency:.1%}")
    
    with col3:
        num_sims = simulation_results.get('num_simulations', 0)
        st.metric("Simulations Run", f"{num_sims:,}")
    
    with col4:
        revenue_std = simulation_results.get('revenue_std', 0)
        st.metric("Revenue Std Dev", f"${revenue_std:.2f}")


def plot_auction_comparison(results_dict: Dict[str, Dict[str, Any]]) -> go.Figure:
    auction_types = list(results_dict.keys())
    avg_revenues = [results_dict[at]['average_revenue'] for at in auction_types]
    avg_efficiencies = [results_dict[at]['average_efficiency'] for at in auction_types]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Average Revenue Comparison', 'Average Efficiency Comparison')
    )
    
    fig.add_trace(
        go.Bar(x=auction_types, y=avg_revenues, name="Revenue"),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=auction_types, y=avg_efficiencies, name="Efficiency", marker_color='green'),
        row=1, col=2
    )
    
    fig.update_layout(
        title="Auction Type Comparison",
        showlegend=False
    )
    
    return fig
