import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

st.header("Inflation Impact Analysis with Python") 

st.text("Inflation is the rate at which the general level of prices for goods and services rises over time, which leads to a decrease in the purchasing power of money. It indicates how much more expensive a set of goods and services has become over a certain period.")

st.subheader("Inflation Impact Analysis: Overview")




st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
Inflation occurs when there is a sustained increase in the general price level of goods and services in an economy over time. It impacts various aspects of the economy, including purchasing power, consumer behaviour, savings, and investment. Moderate inflation is typically a sign of a healthy, growing economy, as it encourages spending and investment. However, high or unpredictable inflation can erode the value of money, disrupt financial planning, and lead to economic uncertainty.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
To analyze the impact of inflation, we need to compare it with other economic indicators. So, to analyze the impact of inflation on the economy, we will compare it with the exchange rates over time. This comparison is important because exchange rates are influenced by inflation differentials between countries, such that higher inflation in a country generally leads to a weaker currency relative to countries with lower inflation.
</div>
""", unsafe_allow_html=True)

st.subheader("Inflation_Rates_Transformed Dataset")

url = "Inflation_Rates_Transformed.csv"
inflation_data = pd.read_csv(url)
st.dataframe(inflation_data.head(10),use_container_width=True)

st.subheader("USD_INR_Exchange_Rates_1980_2024 Dataset")
url = "USD_INR_Exchange_Rates_1980_2024.csv"
exchange_rate_data = pd.read_csv(url)
st.dataframe(exchange_rate_data.head(10),use_container_width=True)

# filter the inflation data for India and the United States
inflation_filtered_df = inflation_data[inflation_data['Country'].isin(['India', 'United States'])]

# pivot the inflation data to have separate columns for India and the United States inflation rates
inflation_pivot_df = inflation_filtered_df.pivot(index='Year', columns='Country', values='Inflation Rate').reset_index()

# merge the exchange rates data with the inflation data
merged_df = pd.merge(exchange_rate_data, inflation_pivot_df, on='Year')

# renaming columns
merged_df.columns = ['Year', 'Exchange Rate (INR/USD)', 'Inflation Rate (India)', 'Inflation Rate (United States)']
st.subheader("Merged Dataset")
st.dataframe(merged_df.head(),use_container_width=True)

st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
The merged dataset now contains the following columns for each year:<br>
<b>Exchange Rate (INR/USD):</b> The average exchange rate of INR to USD.<br>
<b>Inflation Rate (India):</b> The inflation rate for India.<br>
<b>Inflation Rate (United States):</b> The inflation rate for the United States.
</div>
""", unsafe_allow_html=True)

st.subheader("Exchange Rate and Inflation Trends")

def create_plot(merged_df):
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=("Trend of Exchange Rate (INR/USD)",
                                        "Trend of Inflation Rate (India)",
                                        "Trend of Inflation Rate (United States)"))

    fig.add_trace(go.Scatter(x=merged_df['Year'],
                             y=merged_df['Exchange Rate (INR/USD)'],
                             mode='lines+markers',
                             marker=dict(color='blue'),
                             name='Exchange Rate (INR/USD)'),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=merged_df['Year'],
                             y=merged_df['Inflation Rate (India)'],
                             mode='lines+markers',
                             marker=dict(color='orange'),
                             name='Inflation Rate (India)'),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=merged_df['Year'],
                             y=merged_df['Inflation Rate (United States)'],
                             mode='lines+markers',
                             marker=dict(color='green'),
                             name='Inflation Rate (United States)'),
                  row=3, col=1)

    fig.update_layout(height=800,
                      showlegend=False,
                      title_text="Trends of Exchange Rate and Inflation Rates",
                      xaxis3_title="Year",
                      template='plotly_white')

    fig.update_yaxes(title_text="Exchange Rate (INR/USD)", row=1, col=1)
    fig.update_yaxes(title_text="Inflation Rate (%)", row=2, col=1)
    fig.update_yaxes(title_text="Inflation Rate (%)", row=3, col=1)
    
    return fig


# Display the plot
if 'merged_df' in locals() or 'merged_df' in globals():
    st.plotly_chart(create_plot(merged_df), use_container_width=True)
else:
    st.error("Data not loaded. Please uncomment and configure the data loading section.")

st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
The exchange rate shows a general upward trend over the years, which indicates a depreciation of the Indian Rupee against the US Dollar. However, there are periods of both sharp increases and relative stability.<br>

India’s inflation rate has fluctuated significantly over the years, with periods of high inflation (e.g., early 2000s) and more stable inflation in recent years. The United States has generally experienced lower and more stable inflation rates compared to India, with fewer extreme fluctuations.
</div>
""", unsafe_allow_html=True)

st.subheader("Correlation Analysis")
st.text("Perform a correlation analysis to explore the relationship between the inflation rates and the exchange rates:")

correlation_matrix = merged_df[['Exchange Rate (INR/USD)',
                                'Inflation Rate (India)',
                                'Inflation Rate (United States)']].corr()

correlation_matrix

st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
<b>Findings from the correlation analysis:</b><br>
<b>Exchange Rate vs. Inflation Rate (India):</b> The correlation coefficient is approximately <b>-0.34</b>, which indicates a weak negative relationship. It suggests that as inflation in India increases, the INR tends to depreciate against the USD, though the relationship is not very strong.<br>
<b>Exchange Rate vs. Inflation Rate (United States):</b> The correlation coefficient is approximately <b>0.24</b>, which indicates a weak positive relationship. It suggests that higher inflation in the United States might be associated with a depreciation of the USD against the INR, but again, the relationship is not strong.<br>
<b>Inflation Rate (India) vs. Inflation Rate (United States):</b> The correlation between the inflation rates of India and the United States is very weak and negative <b>(-0.12)</b>, which indicates that the inflation rates in these two countries do not move together.<br>
</div>
""", unsafe_allow_html=True)

st.subheader("comparative analysis")
st.text("Performing a comparative analysis to highlight periods of significant divergence or convergence between the inflation rates and the exchange rates:")

st.subheader("Comparative Analysis: Exchange Rate vs Inflation Rates")

def create_comparison_plot(merged_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=merged_df['Year'],
        y=merged_df['Exchange Rate (INR/USD)'],
        mode='lines+markers',
        name='Exchange Rate (INR/USD)',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=merged_df['Year'],
        y=merged_df['Inflation Rate (India)'],
        mode='lines+markers',
        name='Inflation Rate (India)',
        line=dict(color='orange', width=2),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=merged_df['Year'],
        y=merged_df['Inflation Rate (United States)'],
        mode='lines+markers',
        name='Inflation Rate (United States)',
        line=dict(color='green', width=2),
        marker=dict(size=8)
    ))

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Value',
        legend_title_text='Indicators',
        template='plotly_white',
        hovermode='x unified',
        height=600
    )
    
    return fig

# Display the plot (replace merged_df with your actual dataframe)
if 'merged_df' in locals() or 'merged_df' in globals():
    st.plotly_chart(create_comparison_plot(merged_df), use_container_width=True)
else:
    st.error("Data not loaded. Please load your data first.")


st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
<b>Findings from the comparative analysis:</b><br>
<b>Early 2000s:</b> A period of high inflation in India coincides with a period of relative stability in the exchange rate. It suggests that factors other than inflation may have been driving the exchange rate during this time.<br>
<b>Late 2000s to Early 2010s:</b> The period shows some alignment between rising inflation in India and a weakening INR, which indicates that inflation could be contributing to exchange rate movements.<br>
<b>2015 Onwards:</b> The exchange rate continues to rise, while both India’s and the United States’ inflation rates remain relatively low. This divergence suggests that the exchange rate is influenced by additional factors beyond inflation, such as economic growth, monetary policy, and international trade dynamics.<br>
</div>
""", unsafe_allow_html=True)

st.subheader("Analyzing Inflation based on the Purchasing Power Parity (PPP)")

st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
Purchasing Power Parity (PPP) is an economic theory that suggests that in the long term, exchange rates between two countries should adjust so that a basket of goods costs the same in both countries when priced in a common currency. PPP is used as a method to compare the economic productivity and standards of living between different countries. If one country’s inflation rate is higher than another’s, its currency should depreciate accordingly to maintain parity in purchasing power to ensure that the same goods cost the same in both locations.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
Analyze whether the Purchasing Power Parity theory holds by comparing the relative inflation rates and exchange rate movements over time. It will provide a deeper understanding of whether the exchange rate aligns with the theoretical value based on inflation differentials.<br>

To test whether PPP holds for India and the United States, we can:<br>

1. Calculate the Expected Exchange Rate Based on PPP<br>
2. Compare the Actual Exchange Rate with the PPP-Based Expected Exchange Rate<br>
The formula for PPP-based exchange rate prediction is:<br>

<b>Expected Exchange Rate = Initial Exchange Rate × ( 1 + Inflation Rate in India / 1 + Inflation Rate in the US)</b>

Let’s calculate and visualize the PPP-based expected exchange rate versus the actual exchange rate:
</div>
""", unsafe_allow_html=True)



# Title and description
st.subheader("Purchasing Power Parity (PPP) Exchange Rate Analysis")
st.markdown("""
This analysis compares the actual exchange rate with the expected rate calculated using PPP theory:
""")
st.latex(r'''
\text{Expected Rate} = \text{Initial Rate} \times \prod_{t=1}^{T} \left( \frac{1 + \pi_{India}}{1 + \pi_{US}} \right)
''')

# Load data (replace with your actual data loading)
# merged_df = pd.read_csv('your_data.csv')

if 'merged_df' in globals():
    # Calculate PPP expected rate
    initial_exchange_rate = merged_df['Exchange Rate (INR/USD)'].iloc[0]
    merged_df['Expected Exchange Rate (PPP)'] = initial_exchange_rate * (
        (1 + merged_df['Inflation Rate (India)'] / 100) / 
        (1 + merged_df['Inflation Rate (United States)'] / 100)
    ).cumprod()

    # Create the plot
    def create_ppp_plot(df):
        fig = go.Figure()
        
        # Actual exchange rate
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Exchange Rate (INR/USD)'],
            mode='lines+markers',
            name='Actual Exchange Rate',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        # PPP expected rate
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Expected Exchange Rate (PPP)'],
            mode='lines+markers',
            name='PPP Expected Rate',
            line=dict(color='orange', width=2, dash='dash'),
            marker=dict(size=8, symbol='diamond')
        ))
        
        fig.update_layout(
            title='Actual vs. PPP Expected Exchange Rate (INR/USD)',
            xaxis_title='Year',
            yaxis_title='Exchange Rate (INR/USD)',
            legend_title='Rate Type',
            template='plotly_white',
            hovermode='x unified',
            height=600
        )
        return fig

    # Display the plot
    st.plotly_chart(create_ppp_plot(merged_df), use_container_width=True)
    
    # Show data table
    with st.expander("View Calculation Details"):
        st.dataframe(merged_df[['Year', 'Exchange Rate (INR/USD)', 
                               'Inflation Rate (India)', 'Inflation Rate (United States)', 
                               'Expected Exchange Rate (PPP)']].style.format({
            'Exchange Rate (INR/USD)': '{:.2f}',
            'Inflation Rate (India)': '{:.2f}%',
            'Inflation Rate (United States)': '{:.2f}%',
            'Expected Exchange Rate (PPP)': '{:.2f}'
        }))
        
    # Performance metrics
    latest = merged_df.iloc[-1]
    ppp_error = ((latest['Exchange Rate (INR/USD)'] - latest['Expected Exchange Rate (PPP)']) / 
                 latest['Exchange Rate (INR/USD)']) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Actual Rate", f"{latest['Exchange Rate (INR/USD)']:.2f}")
    col2.metric("Latest PPP Expected", f"{latest['Expected Exchange Rate (PPP)']:.2f}")
    col3.metric("Deviation", f"{ppp_error:.1f}%", 
                delta_color="inverse")
    
else:
    st.error("Data not loaded. Please load your merged_df dataframe.")

st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
The blue line represents the actual exchange rate (INR/USD) over time, while the orange dashed line represents the expected exchange rate based on PPP. In some periods, the actual exchange rate closely follows the expected PPP-based rate, which suggests that PPP holds. However, in other periods, there are significant deviations between the two.<br>

The PPP-based expected exchange rate shows a more rapid increase compared to the actual exchange rate. It suggests that, according to PPP, the INR should have depreciated more than it actually did. However, the actual exchange rate was consistently lower than the PPP-based expected rate, which indicates that factors other than inflation are at play.
</div>
""", unsafe_allow_html=True)

st.subheader("Conclusion")
st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
This analysis revealed that inflation in India and the United States influences the exchange rate between INR and USD. Higher inflation in India generally leads to a depreciation of the INR relative to the USD, while lower inflation in the United States contributes to a stronger USD. While inflation affects the exchange rate between INR and USD, it is only one of many factors.
</div>
""", unsafe_allow_html=True)













