import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the datasets
medal_df = pd.read_csv("Olympics_2024_Medals_Table.csv")
competition_df = pd.read_csv("Olympics_2024.csv")
historical_df = pd.read_csv("Olympics_Historical_Data.csv")  # Contains historical data for all countries and athletes

# Streamlit App Layout
st.title("Olympics 2024 Interactive Medal, Competition, and Historical Analysis")

# Sidebar for navigation
st.sidebar.image("logo.jpg", use_column_width=True)
st.sidebar.title("Options")
section = st.sidebar.radio("Select", ["Medal Analysis", "Competitions Analysis", "Historical Trends", "Additional Information"])

# Medal Analysis Section
if section == "Medal Analysis":
    st.write("### Olympics Medal Table")
    st.dataframe(medal_df)

    # Medal Proportions using Plotly
    st.write("#### Medal Proportions for Each Country")
    medal_df['Gold %'] = medal_df['GOLD'] / medal_df['TOTAL'] * 100
    medal_df['Silver %'] = medal_df['SILVER'] / medal_df['TOTAL'] * 100
    medal_df['Bronze %'] = medal_df['BRONZE'] / medal_df['TOTAL'] * 100

    fig = px.bar(medal_df, x='TEAM', y=['Gold %', 'Silver %', 'Bronze %'], 
                 title='Medal Proportions for Each Country', barmode='stack',
                 color_discrete_map={'Gold %': '#FFD700', 'Silver %': '#C0C0C0', 'Bronze %': '#CD7F32'},
                 labels={'value': 'Percentage', 'TEAM': 'Country'})
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig)

    # Country Comparison - User selects countries
    st.write("## Compare Countries")
    selected_countries = st.multiselect("Select Countries to Compare", medal_df['TEAM'].unique(), default=medal_df['TEAM'].unique()[0:2])
    comparison_df = medal_df[medal_df['TEAM'].isin(selected_countries)]
    
    fig_compare = px.bar(comparison_df, x='TEAM', y=['GOLD', 'SILVER', 'BRONZE'], barmode='group',
                         color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'],
                         title='Comparison of Selected Countries')
    st.plotly_chart(fig_compare)

    # Correlation Between Medal Types
    st.write("## Correlation Between Medal Types")
    corr = medal_df[['GOLD', 'SILVER', 'BRONZE']].corr()
    fig_corr = px.imshow(corr, text_auto=True, title="Correlation Matrix of Medals",
                         color_continuous_scale='Blues')
    st.plotly_chart(fig_corr)

    # Detailed Analysis - Select a Country
    st.write("## Country and Medal-wise Analysis")
    country = st.selectbox("Select a Country for Detailed Analysis", medal_df['TEAM'].unique())
    country_data = medal_df[medal_df['TEAM'] == country]

    fig_pie = go.Figure(data=[go.Pie(labels=['Gold', 'Silver', 'Bronze'], 
                                     values=[country_data['GOLD'].values[0], 
                                             country_data['SILVER'].values[0], 
                                             country_data['BRONZE'].values[0]], 
                                     marker=dict(colors=['#FFD700', '#C0C0C0', '#CD7F32']))])
    fig_pie.update_layout(title=f"Medal Distribution for {country}")
    st.plotly_chart(fig_pie)

    # Dynamic Medal-wise Analysis
    st.write("## Top Countries by Medal Type")
    medal_type = st.selectbox("Select Medal Type for Analysis", ['GOLD', 'SILVER', 'BRONZE'])
    top_countries = medal_df.sort_values(by=medal_type, ascending=False).head(10)

    fig_top = px.bar(top_countries, x='TEAM', y=medal_type, title=f"Top 10 Countries by {medal_type} Medals",
                     color_discrete_sequence=[f'#FFD700' if medal_type == 'GOLD' else '#C0C0C0' if medal_type == 'SILVER' else '#CD7F32'])
    st.plotly_chart(fig_top)

    # Summary Statistics
    st.write("## Static Analysis - Summary Statistics")
    st.write("#### Total Medals Overview")
    st.write(medal_df[['GOLD', 'SILVER', 'BRONZE', 'TOTAL']].sum())

    st.write("#### Top Countries by Medal Type")
    top_gold = medal_df[medal_df['GOLD'] == medal_df['GOLD'].max()]['TEAM'].values[0]
    top_silver = medal_df[medal_df['SILVER'] == medal_df['SILVER'].max()]['TEAM'].values[0]
    top_bronze = medal_df[medal_df['BRONZE'] == medal_df['BRONZE'].max()]['TEAM'].values[0]
    st.write(f"Top Gold Medal Winner: {top_gold}")
    st.write(f"Top Silver Medal Winner: {top_silver}")
    st.write(f"Top Bronze Medal Winner: {top_bronze}")

# Competitions Analysis Section
elif section == "Competitions Analysis":
    st.write("### Olympics Competitions Dataset")
    st.dataframe(competition_df)

    # Analysis 1: Competition-Wise Medal Distribution
    st.write("## Competition-Wise Medal Distribution")
    selected_competition = st.selectbox("Select Competition", competition_df['Competitions'].unique())
    comp_data = competition_df[competition_df['Competitions'] == selected_competition]

    fig_comp = px.bar(comp_data, x='NOC', y=['Gold', 'Silver', 'Bronze'], 
                      barmode='stack', title=f"Medal Distribution in {selected_competition}",
                      color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
    st.plotly_chart(fig_comp)

    # Analysis 2: Top Performing Countries in Each Competition
    st.write("## Top Performing Countries in Each Competition")
    top_performing = comp_data.sort_values(by='Total', ascending=False).head(3)
    st.write(f"### Top 3 Countries in {selected_competition}")
    st.dataframe(top_performing[['Rank', 'NOC', 'Gold', 'Silver', 'Bronze', 'Total']])

    # Country-Wise Performance Across Competitions
    st.write("## Country-Wise Performance Across Competitions")
    selected_country = st.selectbox("Select Country", competition_df['NOC'].unique())
    country_data = competition_df[competition_df['NOC'] == selected_country]

    fig_country = px.bar(country_data, x='Competitions', y=['Gold', 'Silver', 'Bronze'], 
                         barmode='group', title=f"{selected_country}'s Performance Across Competitions",
                         color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
    st.plotly_chart(fig_country)

# Historical Trends Section with Athlete Details
elif section == "Historical Trends":
    st.write("## Historical Trends in Medal Wins and Athlete Details")
    
    # Select Country and show historical data for each
    selected_country_trend = st.selectbox("Select Country for Historical Trend", historical_df['Country'].unique())
    country_trend_data = historical_df[historical_df['Country'] == selected_country_trend]

    # Show medal trends over time
    fig_trend = px.line(country_trend_data, x='Year', y='Total Medals', 
                        title=f"Medal Wins for {selected_country_trend} Over Time", markers=True,
                        color_discrete_sequence=['#FFD700'])
    st.plotly_chart(fig_trend)

    # Show athletes and their medals
    st.write(f"### Athletes from {selected_country_trend} with Most Medals")
    athletes = historical_df[historical_df['Country'] == selected_country_trend][['Gold', 'Silver', 'Bronze']].drop_duplicates()
    st.dataframe(athletes)

    # Medal Trends by Competition Type
    st.write("## Medal Trends by Competition Type")
    selected_comp_trend = st.selectbox("Select Competition for Trend", historical_df['Competition'].unique())
    competition_trend_data = historical_df[historical_df['Competition'] == selected_comp_trend]

    fig_comp_trend = px.line(competition_trend_data, x='Year', y='Total Medals', 
                             title=f"Medal Wins in {selected_comp_trend} Over Time", markers=True,
                             color_discrete_sequence=['#C0C0C0'])
    st.plotly_chart(fig_comp_trend)

    # Show detailed information for all countries
    st.write("## All Countries Medal Information")
    all_countries_data = historical_df[['Country', 'Year', 'Gold', 'Silver', 'Bronze']].drop_duplicates()
    st.dataframe(all_countries_data)

    # India specific details
    # st.write("## India's Detailed Medal and Athlete Information")
    # india_data = historical_df[historical_df['Country'] == 'India']
    # st.dataframe(india_data[['Year', 'Gold', 'Silver', 'Bronze']])

# Additional Information Section
elif section == "Additional Information":
    st.write("## Additional Information and Insights")
    st.write("### Fun Facts about Olympics 2024:")
    st.write("""
        - The 2024 Olympics will be held in Paris, marking 100 years since the city last hosted the Summer Games in 1924.
        - Over 10,000 athletes from more than 200 countries are expected to compete.
        - Skateboarding, surfing, and sport climbing are set to return as part of the official program.
        - The Olympic Village will be built to be entirely sustainable.
    """)
    
    st.write("### Interesting Facts and Statistics")
    st.write("1. **Country with the Most Total Medals:**")
    st.write(medal_df.loc[medal_df['TOTAL'].idxmax()]['TEAM'])
    st.write("2. **Competition with the Highest Medal Count:**")
    st.write(competition_df.loc[competition_df['Total'].idxmax()]['Competitions'])
    
    # Historical Data Insight
    st.write("### Historical Insights")
    st.write("Historical data shows trends in medal distribution and athlete performance. Use this section to explore more detailed information about the evolution of Olympic performances over time.")

    # Provide links to external resources
    st.write("### Useful Resources")
    st.markdown("""
        - [Official Olympics Website](https://www.olympics.com)
        - [Olympic Medal History](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table)
        - [Athlete Profiles](https://www.olympic.org/athletes)
    """)

# End of App
st.write("Thank you for using the Olympics 2024 Interactive Analysis tool!")
