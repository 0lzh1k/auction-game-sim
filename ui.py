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

def main():
    st.set_page_config(
        page_title="Auction Strategy Game Simulator",
        page_icon="🏆",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    Explore game theory principles through interactive auction simulations. 
    This tool demonstrates how different bidding strategies perform under various auction formats.
    """)
    with st.sidebar:
        st.header("Simulation Configuration")
        auction_type = st.selectbox(
            "Auction Type",
            ["first_price", "second_price"],
            format_func=lambda x: x.replace("_", " ").title(),
            help="Choose between First-Price (pay your bid) and Second-Price/Vickrey (pay second-highest bid) auctions"
        )
        num_bidders = st.slider(
            "Number of Bidders",
            min_value=2,
            max_value=20,
            value=5,
            help="More bidders generally increase competition and revenue"
        )
        num_simulations = st.slider(
            "Number of Simulations",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="More simulations provide more reliable statistical results"
        )
        st.subheader("Valuation Distribution")
        valuation_dist = st.selectbox(
            "Distribution Type",
            ["uniform", "normal"],
            help="How bidders' private valuations are distributed"
        )
        if valuation_dist == "uniform":
            val_low = st.number_input("Minimum Valuation", value=0.0, min_value=0.0)
            val_high = st.number_input("Maximum Valuation", value=100.0, min_value=0.1)
            if val_high <= val_low:
                st.error("Maximum valuation must be greater than minimum valuation!")
                val_high = val_low + 1
            valuation_params = {"low": val_low, "high": val_high}
        else:
            val_mean = st.number_input("Mean Valuation", value=50.0, min_value=0.0)
            val_std = st.number_input("Standard Deviation", value=15.0, min_value=1.0)
            valuation_params = {"mean": val_mean, "std": val_std}
        st.subheader("Bidding Strategies")
        available_strategies = list(get_available_strategies().keys())
        strategy_config = st.selectbox(
            "Strategy Assignment",
            ["all_same", "mixed", "custom"],
            format_func=lambda x: {
                "all_same": "All Same Strategy",
                "mixed": "Random Mix",
                "custom": "Custom Assignment"
            }[x]
        )
        if strategy_config == "all_same":
            default_strategy = st.selectbox(
                "Strategy for All Bidders",
                available_strategies,
                help="All bidders will use this strategy"
            )
            strategies = [default_strategy] * num_bidders
        elif strategy_config == "mixed":
            strategies = np.random.choice(available_strategies, num_bidders).tolist()
            st.write("Randomly assigned strategies: " + ", ".join(strategies))
        else:
            strategies = []
            for i in range(min(num_bidders, 5)):
                strategy = st.selectbox(
                    f"Bidder {i+1} Strategy",
                    available_strategies,
                    key=f"strategy_{i}"
                )
                strategies.append(strategy)
            while len(strategies) < num_bidders:
                strategies.append(strategies[0])
        run_simulation = st.button("Run Simulation", type="primary")
    if run_simulation:
        results = run_auction_simulation(
            auction_type, num_bidders, num_simulations,
            valuation_dist, valuation_params, strategies
        )
        st.success(f"Completed {num_simulations} simulations!")
        st.subheader("Summary Metrics")
        create_summary_metrics_display(results)
        st.subheader("Results Visualization")
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Revenue Analysis", "Strategy Performance", "Bidding Behavior", 
            "Efficiency Trends", "Bid Distributions"
        ])
        with tab1:
            st.plotly_chart(plot_revenue_comparison(results), use_container_width=True)
            revenues = results['all_revenues']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Min Revenue", f"${min(revenues):.2f}")
            with col2:
                st.metric("Median Revenue", f"${np.median(revenues):.2f}")
            with col3:
                st.metric("Max Revenue", f"${max(revenues):.2f}")
        with tab2:
            df_results = create_results_dataframe(results['results'])
            st.plotly_chart(plot_strategy_performance(df_results), use_container_width=True)
            st.subheader("Strategy Performance Table")
            strategy_stats = calculate_strategy_stats(df_results)
            st.dataframe(strategy_stats, use_container_width=True)
        with tab3:
            st.plotly_chart(plot_bid_vs_valuation(results['results'], auction_type), use_container_width=True)
        with tab4:
            st.plotly_chart(plot_efficiency_over_time(results['results']), use_container_width=True)
        with tab5:
            st.plotly_chart(plot_bid_distribution(results['results'], auction_type), use_container_width=True)
    else:
        st.info("Configure the simulation and click 'Run Simulation' to begin.")

if __name__ == "__main__":
    main()
