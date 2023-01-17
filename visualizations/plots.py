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


