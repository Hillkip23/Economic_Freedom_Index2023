import streamlit as st
import pandas as pd
import altair as alt

# Load the data
try:
    df = pd.read_excel('index2023_data.xlsx')
except FileNotFoundError:
    st.error('Excel file not found. Please check the file path.')
    st.stop()

# Check the columns in the DataFrame
if '2023 Score' not in df.columns:
    st.error("The column '2023 Score' is not present in the DataFrame. Please check the column name and the formatting of the Excel file.")
    st.stop()

# Create the first tab to display the score for a selected country
def tab1():
    st.write('# Economic freedom Index by Country:')
    
    # Create a dropdown menu for selecting a country
    country = st.selectbox('Select a country', df['Country Name'].unique())

    # Filter the DataFrame to show data for the selected country
    country_data = df[df['Country Name'] == country]

    # Display the 2023 score for the selected country
    try:
        score_2023 = country_data['2023 Score'].values[0]
    except IndexError:
        st.error(f"No data found for {country}.")
        st.stop()
    st.write("This tab allows you to select a country from a dropdown menu and displays the 2023 score for that country. The score represents the level of economic freedom in the country, based on factors such as rule of law, government size, regulatory efficiency, and market openness.")
    st.write(f"2023 score for {country}: {score_2023}")

# Create the second tab to display a bar chart of top countries by economic freedom
def tab2():
    st.write('# Top countries by economic freedom:')
    st.write("This tab displays a bar chart of the top countries by economic freedom. You can use the slider to adjust the number of countries displayed on the chart. The chart shows the 2023 score for each country on the y-axis and the country name on the x-axis. The higher the score, the more economically free the country is. This tab provides a quick overview of the countries that score highest on the Index of Economic Freedom.")
    top_n = st.slider("Select the number of top countries to display:", min_value=1, max_value=50, value=10, step=1, key='slider')

    top_countries = df[['Country Name', '2023 Score']].sort_values('2023 Score', ascending=False).head(top_n)

    chart = alt.Chart(top_countries).mark_bar().encode(
        x=alt.X('2023 Score', axis=alt.Axis(title='2023 Score')),
        y=alt.Y('Country Name', sort='-x')
    )


    
    st.altair_chart(chart, use_container_width=True)

# Create the tabs
tabs = ['Country Score', 'Top Countries']
page = st.sidebar.selectbox('Select a tab', tabs)

if page == 'Country Score':
    tab1()
else:
    tab2()
