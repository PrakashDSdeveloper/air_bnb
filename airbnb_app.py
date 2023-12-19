import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
import pandas as pd
import seaborn as sns
from plotly.subplots import make_subplots
from streamlit_folium import st_folium

with st.sidebar:
    selected = option_menu(
        menu_title='Airbnb Analysis',
        options=['Home','GeoVisual Analysis','About'],
        icons=['house','globe','exclamation-lg'],
        menu_icon="cast", default_index=0, orientation="verical",
        styles={'nav-link':{'font-size':'20px','margin':'-2px','font-color':'#6739b7'},
                'nav-link-selected':{'font-color':'white','background':'#FF0000'}}
    )
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #e1d7f2;
background-size :cover;
}
[data-testid="stSidebar"]{
background-image: url("https://cdn.pixabay.com/photo/2014/04/02/14/04/airplane-306074_960_720.png");
background-position :center;
background-repeat: no-repeat;

}
[data-testid="stHeader"]{
background-color: #FF0000;
background-position :center;

}
[data-baseweb="tab"]{
background-color: #e1d7f2;
}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
if selected == 'Home':

    '''**Project Overview: Analyzing Airbnb Data using MongoDB Atlas**

**Objective:**
The primary goal of this project is to conduct a comprehensive analysis of Airbnb data using MongoDB Atlas. The focus includes data cleaning and preparation, interactive geospatial visualizations, and dynamic plots to extract insights into pricing variations, availability patterns, and location-based trends.

**Project Tasks:**

1. **MongoDB Atlas Account Setup:**
   - Visit the MongoDB Atlas website and initiate the account registration process.
   - Create a new project within MongoDB Atlas during the registration.
   
2. **Cluster Configuration:**
   - Set up a cluster within the MongoDB Atlas project.
   - Choose the appropriate cloud provider and region for hosting the data.
   - Configure cluster specifications to meet project requirements and create the cluster.

3. **Data Loading:**
   - Access the MongoDB Atlas dashboard.
   - In the left-hand navigation menu, navigate to "Database Access" to create a user with necessary permissions.
   - Configure "Network Access" to implement IP whitelisting or other security measures.
   - Import the Airbnb sample data into the cluster through the "Collections" tab on the cluster view.

4. **Data Cleaning and Preparation:**
   - Address missing values, duplicates, and perform data type conversions to ensure accuracy in analysis.

5. **Streamlit Web Application Development:**
   - Create a Streamlit web application featuring interactive maps that showcase the distribution of Airbnb listings.
   - Allow users to explore prices, ratings, and other relevant factors through the interactive interface.

6. **Price Analysis and Visualization:**
   - Utilize dynamic plots and charts to analyze pricing variations based on location, property type, and seasons.

7. **Availability Pattern Analysis:**
   - Visualize occupancy rates and demand fluctuations across seasons to gain insights into availability patterns.

8. **Location-Based Insights:**
   - Extract and visualize data for specific regions or neighborhoods to uncover location-based trends.

9. **Interactive Visualizations:**
   - Develop interactive visualizations that empower users to filter and drill down into the data for a more detailed analysis.'''

if selected == 'GeoVisual Analysis':
    # st.set_page_config(page_title="Airbnb_Data_Analysis", layout="wide")

    # st.title(':rainbow[AirBnb Geospatial Analysis]')

    data = pd.read_csv(r'Data_Set\airbnb_dataset.csv')

    aggregated = data.groupby(['country','city']).count()

    tab1,tab2 = st.tabs(['Geospatial Analysis','Exploratory Data Analysis'])

    with tab1:
        country = st.selectbox('Select a Country',options=data['country'].unique())

        if country == 'Australia':
            city = st.selectbox('Select a City',options=['Sydney'])

        elif country == 'China':
            city = st.selectbox('Select a City',options=['Hong Kong'])

        elif country == 'Hong Kong':
            city = st.selectbox('Select a City',options=['Hong Kong'])

        elif country == 'Portugal':
            city = st.selectbox('Select a City',options=['Porto','Other (International)'])

        elif country == 'Brazil':
            city = st.selectbox('Select a City',options=['Rio De Janeiro'])

        elif country == 'Canada':
            city = st.selectbox('Select a City',options=['Montreal'])
        
        elif country == 'Turkey':
            city = st.selectbox('Select a City',options=['Istanbul'])

        elif country == 'Spain':
            city = st.selectbox('Select a City',options=['Barcelona'])

        elif country == 'United States':
            city = st.selectbox('Select a City',options=['Kauai','Maui','New York','Oahu','The Big Island','Other (Domestic)'])

        sep1,sep2 = st.columns(2)

        with sep1:
            min_price = st.text_input('Select a Minimum Price (Minimum value : 9)')
        
        with sep2:
            max_price = st.text_input('Select a Maximum Price (Maximum value : 11,681)')

        st.divider() 

        if country and city and min_price and max_price:
            try:
                query_df = data.query(f'country == "{country}" and city == "{city}" and price>={min_price} and price<={max_price}')
                reset_index = query_df.reset_index(drop = True)
            
                # Creating map using folium
                base_latitude = reset_index.loc[0,'latitude']
                base_longitude = reset_index.loc[0,'longitude']

                base_map = folium.Map(location=[base_latitude,base_longitude], zoom_start=12)

                for index, row in reset_index.iterrows():
                    lat,lon = row['latitude'],row['longitude']
                    id = row['id']
                    name = row['name']
                    price = row['price']
                    review = row['review_score']
                    popup_text = f"ID: {id} | Name: {name} | Price: ${price} | Rating: {review}/10"
                    folium.Marker(location=[lat, lon], popup=popup_text).add_to(base_map)

                # call to render Folium map in Streamlit
                st_data = st_folium(base_map, width=1200,height = 600)

                st.divider()

                st.subheader(':red[Top Hotels Recommendations] 🏰')
                
                df = reset_index.sort_values(by=['price','review_score'],ascending = False)

                new_df = df[['id','url','name','city','country','amenities','price','review_score','no_of_reviews']]

                st.dataframe(new_df.head(),hide_index = True,width=1175,height=218)

                st.divider() 

                st.subheader(':red[Top Hotels by Price and Ratings]')

                query_top = data.query(f'country == "{country}" and city == "{city}"')

                query_1 = query_top.sort_values(by = ['price','review_score'],ascending = False)

                new_df1 = query_1[['id','url','name','city','country','amenities','price','review_score','no_of_reviews']]

                st.dataframe(new_df1.head(),hide_index=True,width = 1175, height = 220)

                st.divider()

                st.subheader(':red[Enter the ID to know more about the Hotel and Availability]')

                id_input = st.text_input('Enter a ID')

                if id_input:
                    new_query = reset_index.query(f'country == "{country}" and city == "{city}" and price>={min_price} and price<={max_price} and id == {id_input}')
                    new_table = new_query[['id','url','name','amenities','price','availability_30','availability_60','availability_90','availability_365','review_score','no_of_reviews']] 
                    st.dataframe(new_table,hide_index = True, width = 1175, height = 78)

                    st.divider()

            except:
                st.info('No results found')

    with tab2:

        col1,col2 = st.columns(2)

        option = st.selectbox('Exploratory Data Analysis',('Select an Analysis','Countrywise Price Analysis', 'Distribution of Price', 'Box plot Visaliztion : Distribution of Price','Scatter Plot Visualization :  Price and Availability'))

        st.divider() 

        if option == 'Countrywise Price Analysis':
            fig = px.histogram(data,x = 'city',animation_frame='country',color = 'country')
            fig.update_layout(width=1200,height=500, title="Animated Histogram by City",xaxis_title="City",yaxis_title="Count")
            st.plotly_chart(fig)

            col1,col2 = st.columns(2)

            with col1:
            
                country_df = data[['country','city']].value_counts()
                new_country_df = pd.DataFrame(country_df,columns = ['Number of Hotels'])
                st.dataframe(new_country_df,width=450,height=528)

            with col2:
        
                grouped = data.groupby(['country','city']).agg({'price':'mean','review_score':'mean'}).sort_values(by=['price','review_score'],ascending = False)
                grouped = grouped.round()
                st.dataframe(grouped,width = 600,height = 528)
            st.divider() 


        elif option == 'Distribution of Price':

            country = st.selectbox('Select any Country',options=data['country'].unique())

            if country == 'Australia':
                city = st.selectbox('Select any City',options=['Sydney'])

            elif country == 'Brazil':
                city = st.selectbox('Select any City',options=['Rio De Janeiro'])

            elif country == 'Canada':
                city = st.selectbox('Select any City',options=['Montreal'])

            elif country == 'China':
                city = st.selectbox('Select any City',options=['Hong Kong'])

            elif country == 'Hong Kong':
                city = st.selectbox('Select any City',options=['Hong Kong'])

            elif country == 'Portugal':
                city = st.selectbox('Select any City',options=['Porto'])

            elif country == 'Spain':
                city = st.selectbox('Select any City',options=['Barcelona'])

            elif country == 'Turkey':
                city = st.selectbox('Select any City',options=['Istanbul'])

            elif country == 'United States':
                city = st.selectbox('Select any City',options=['Kauai','Maui','New York','Oahu','The Big Island'])

            st.divider() 

            country_price_wise = data.query(f'country == "{country}" and city == "{city}"')

            plt.figure(figsize=(8,3.5))
            fig1 = sns.displot(country_price_wise['price'])
            st.pyplot(fig1)

            if country_price_wise["price"].skew() > 0:
                st.write(f'Since the value is Positive : {country_price_wise["price"].skew()}, the curve is skewed Positively to the right side')
            elif country_price_wise["price"].skew() < 0:
                st.write(f'Since the value is Negative : {country_price_wise["price"].skew()}, the curve is skewed Negatively to the left side')
            
            st.divider() 

        elif option == 'Box plot Visaliztion : Distribution of Price':
            fig2 = px.box(data,x = 'country', y = 'price',color = 'country',width=1200, height=650)
            st.plotly_chart(fig2)

            st.divider() 

        elif option == 'Scatter Plot Visualization :  Price and Availability':
            subplots = make_subplots(rows=4, cols=1,subplot_titles = ('Availability 30', 'Availability 60', 'Availability 90', 'Availability 365'))
            scatter_plots1 = go.Scatter(x = data['price'],y = data['availability_30'],mode='markers', name = 'Availability 30')
            subplots.add_trace(scatter_plots1, row=1, col=1)
            
            scatter_plots2 = go.Scatter(x = data['price'],y = data['availability_60'],mode='markers',name = 'Availability 60')
            subplots.add_trace(scatter_plots2, row=2, col=1)

            scatter_plots3 = go.Scatter(x = data['price'],y = data['availability_90'],mode='markers',name = 'Availability 90')
            subplots.add_trace(scatter_plots3, row=3, col=1)

            scatter_plots4 = go.Scatter(x = data['price'],y = data['availability_365'],mode='markers',name = 'Availability 365')
            subplots.add_trace(scatter_plots4, row=4, col=1)

            subplots.update_layout(height=750,width = 1200) 
            st.plotly_chart(subplots)

            st.divider() 


if selected == 'About':
    st.subheader(":red[About this project]")
    st.write('')
    st.write('')
    st.write('This project aims to provide a robust framework for analyzing Airbnb data, from establishing the MongoDB Atlas environment to creating insightful visualizations and interactive dashboards. The focus is on enhancing user exploration and understanding of pricing, availability patterns, and location-based trends within the Airbnb dataset.')
    st.write("") 
    st.write('Linked In url : www.linkedin.com/in/prakash-t-n-894307282')     
