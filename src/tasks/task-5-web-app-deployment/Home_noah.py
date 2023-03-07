import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import pickle as pkl
import folium as flm
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

APP_TITLE = 'Mapping Urban Vulnerability areas'
st.set_page_config(page_title='Home', layout='wide')
print('hello')

# Load the Model DATA and cache.
@st.cache_data
def get_data(folder):
    """
    Load the data in a function so we can cache the files.

    Returns:
        pd.Dataframe: Returns a data frame.
    """
    data_folder = folder
    files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    dfs = {}
    for file in files:
        df_name = os.path.splitext(file)[0]
        df = pd.read_csv(os.path.join(data_folder, file))
        dfs[df_name] = df.set_index(df.columns[0])
    return dfs


# Load the Map DATA and cache.
@st.cache_data
def get_map_data(url):
    # gdf = gpd.read_parquet(url)
    df1 = pd.read_parquet(url)
    df1 = pd.DataFrame(df1.iloc[:, :-1])  # remove last column.
    return df1


# Load the Noah DATA and cache.
@st.cache_data
def get_data_noah(folder):
    """
    Load the data in a function so we can cache the files.

    Returns:
        pd.Dataframe: Returns a data frame.
    """
    data_folder = folder
    files = [f for f in os.listdir(data_folder) if f.endswith('.parquet')]
    gdfs = {}
    for file in files:
        gdf_name = os.path.splitext(file)[0]
        gdf = gpd.read_parquet(os.path.join(data_folder, file))
        gdfs[gdf_name] = gdf.set_index(gdf.columns[0])
    return gdfs
    

# Create the landing page.
def main():
    # Base Colors:
    # Blue = #182D40
    # Light Blue = #82a6c0
    # Green = #4abd82

    # Add custom CSS.
    st.markdown(
        """
        <style>
        .block-container.css-18e3th9.egzxvld2 {
        padding-top: 0;
        }
        header.css-vg37xl.e8zbici2 {
        background: none;
        }
        span.css-10trblm.e16nr0p30 {
        text-align: center;
        color: #2c39b1;
        }
        .css-1dp5vir.e8zbici1 {
        background-image: linear-gradient(
        90deg, rgb(130 166 192), rgb(74 189 130)
        );
        }
        .css-tw2vp1.e1tzin5v0 {
        gap: 10px;
        }
        .css-50ug3q {
        font-size: 1.2em;
        font-weight: 600;
        color: #2c39b1;
        }
        .row-widget.stRadio {
        padding: 10px;
        background: #ffffff;
        border-radius: 7px;
        }
        label.css-cgyhhy.effi0qh3, span.css-10trblm.e16nr0p30 {
        font-size: 1.1em;
        font-weight: bold;
        font-variant-caps: small-caps;
        border-bottom: 3px solid #4abd82;
        }
        label.css-18ewatb.e16fv1kl2 {
        font-variant: small-caps;
        font-size: 1em;
        }
        div[data-testid="stSidebarNav"] li div a {
        margin-left: 1rem;
        padding: 1rem;
        width: 300px;
        border-radius: 0.5rem;
        }
        div[data-testid="stSidebarNav"] li div::focus-visible {
        background-color: rgba(151, 166, 195, 0.15);
        }
        svg.e1fb0mya1.css-fblp2m.ex0cdmw0 {
        width: 2rem;
        height: 2rem;
        }
        p.results {
        font-size: 1.2rem;
        font-weight: bold;
        background-color: #fff;
        padding: 5px;
        border: 1px tomato solid;
        }
        .css-1vq4p4l h2 {
        font-size: 1.6rem;
        }
        .st-bu {
        font-weight: bold;
        }
        .css-1whk732 {
        -webkit-box-pack: end;
        justify-content: flex-end;
        flex: 1 1 0%;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # st.image('src/tasks/task-5-web-app-deployment/assets/header.png')
    st.title(APP_TITLE)

    # Load data and create data frames for the Model
    data = get_data('src/tasks/task-5-web-app-deployment/data/model')
    df_disaster = data['disaster'].iloc[: , :-2]
    df_dweg = data['dweg'].iloc[: , :-2]
    df_health = data['health'].iloc[: , :-2]
    df_industry = data['industry_II'].iloc[: , :-2]
    df_poverty = data['poverty'].iloc[: , :-2]

    # Create the sidebar and add Model
    with st.sidebar:
        st.header("Cluster Prediction")
        html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;">Municipality Cluster Prediction Application </h2>
        </div>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        Disaster, Economy, Health, Industry, Poverty = (
            'src/tasks/task-5-web-app-deployment/pckls/disaster.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/dweg.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/health.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/industry_II.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/poverty.pkl')

        models = {'Disaster': Disaster, 'Economy': Economy,
        'Health': Health, 'Industry': Industry, 'Poverty': Poverty}

        model_names = models.keys()

        option = st.selectbox(
            'Please Select the Pillar', options=model_names,
            help='Here are 5 pillars that can influence the vulnerability of a City')

        with open(models[option], 'rb') as file:
            kmeans = pkl.load(file)


        def load_df():
            """
            Loads the correct data frame the options drop down.

            Returns:
                pd.Dataframe: Returns relevant data frame.
            """
            if option == 'Disaster':
                return df_disaster
            elif option == 'Vulnerability':
                return df_dweg
            elif option == 'Health':
                return df_health
            elif option == 'Industry':
                return df_industry
            else:
                return df_poverty
        
        
        def get_cluster(city):
            """
            Create clusters for mapping to output.

            Args:
                city (str): City name.

            Returns:
                str: Vulnerability level.
            """
            x = load_df().loc[city].values.reshape(1, -1)
            cluster = kmeans.predict(x)[0]
            map_dict = {
                ('Industry', 0): 'Low',
                ('Industry', 1): 'High',
                ('Industry', 2): 'Medium',
                ('Health', 0): 'Medium',
                ('Health', 1): 'Low',
                ('Health', 2): 'High',
                ('Poverty', 1): 'Low',
                ('Poverty', 2): 'Medium',
                ('Poverty', 0): 'High',
                ('Disaster', 1): 'Medium',
                ('Disaster', 2): 'High',
                ('Disaster', 0): 'Low',
                ('Economy', 1): 'Medium',
                ('Economy', 2): 'High',
                ('Economy', 0): 'Low'}
            return map_dict.get((option, cluster), None)


        def display_sliders():
            """
            Creates sliders.

            Returns:
                st.slider: Slider values based on cluster.
            """
            sliders = {}
            for col in load_df().columns:
                min_val = load_df()[col].min()
                max_val = load_df()[col].max()
                val = load_df()[col].loc[selected_city]
                sliders[col] = st.slider(f'''**{col}**''', min_value = float(min_val), max_value = float(max_val), value = float(val))
            return sliders

        # Add a dropdown to select the city.
        selected_city = st.selectbox('Select a city:', load_df().index)

        # Display the current cluster group for the selected city.
        cluster = get_cluster(selected_city)
        result = f'''
        <p class="results">Level of Vulnerability: {cluster}</p>
        '''
        st.markdown(result, unsafe_allow_html=True)

        # Display the slider widgets.
        sliders = display_sliders()

        # Add a button to recalculate the cluster group.
        if st.button('Recalculate'):
            x = pd.DataFrame(sliders, index=[selected_city])
            new_cluster = kmeans.predict(x)[0]
            if new_cluster == 0:
                new_cluster = 'Medium'
            elif new_cluster == 1:
                new_cluster = 'Low'
            elif new_cluster == 2:
                new_cluster = 'High'
            
            result = f'''
            <p class="res">New Level of Vulnerability: {new_cluster}</p>
            '''
            st.markdown(result, unsafe_allow_html=True)

    # Map Data
    map_url = 'src/tasks/task-5-web-app-deployment/data/mapping_data.parquet'
    df1 = get_map_data(map_url)

    noah_folder = 'src/tasks/task-5-web-app-deployment/data/noah'
    
    geodata = get_data_noah(noah_folder)
    gdf_StormSurgeAdvisory1_1 = geodata['ss1']
    gdf_StormSurgeAdvisory1_2 = geodata['ss2']
    gdf_StormSurgeAdvisory1_3 = geodata['ss3']

    # Add map.
    def map_ph(data, name):
        cond = data['Province'] == name

        lat = data[cond]['Latitude'].tolist()
        lon = data[cond]['Longitude'].tolist()
        nam = data[cond]['City'].tolist()
        vul = data[cond]['Vulnerability'].tolist()
        pop = data[cond]['Population'].tolist()
        pov = data[cond]['Poverty_Incidents'].tolist()
        hop = data[cond]['Hospital'].tolist()

        html = f''' <div style="font-family: monospace;font-size: 1rem;">
        <h4 style="font-size:1.05rem;">Vulnerability Info</h4>
        <ul style="list-style-type: none;margin: 0;padding: 0;">
        <li>City/Town: </li>
        <li> <b> %s</b></li>
        <li>Vulnerability: <b> %s</b></li>
        <li>Population: <b> %s</b></li>
        <li>Poverty: <b> %s</b></li>
        <li>Hospitals: <b> %s</b></li>
        </ul>  
        </div>
        '''

        if lat and lon:
            map = flm.Map(location=[lat[0], lon[0]], zoom_start=8, scrollWheelZoom=False)
        else:
            return None

        fg = flm.FeatureGroup(name='Philippines Cities')
        fg1 = flm.FeatureGroup(name='Storm Surge 4 metres')
        fg2 = flm.FeatureGroup(name='Storm Surge 3 metres')
        fg3 = flm.FeatureGroup(name='Storm Surge 2 metres')

        marker_props = {'low': {'color': 'green', 'size': 10},
                    'medium': {'color': 'blue', 'size': 10},
                    'high': {'color': 'red', 'size': 15}}

        for lt, ln, nm, vu, po, pv, ho in zip((lat), (lon), (nam), (vul), (pop), (pov), (hop)):
            iframe = flm.IFrame(html = html % ((nm), (vu), (po), (pv), int((ho))), height = 210)
            popup = flm.Popup(iframe, min_width=200, max_width=650)
            props = marker_props[vu]
            marker = flm.CircleMarker(location = [lt, ln], popup = popup, fill_color=props['color'], color='None', radius=props['size'], fill_opacity = 0.5)
            fg.add_child(marker)
            map.add_child(fg)

        # loop through the dataframes and create a GeoJSON layer for each row
        for df, fg, clr in [(gdf_StormSurgeAdvisory1_1, fg1, 'blue'), (gdf_StormSurgeAdvisory1_2, fg2, 'orange'), (gdf_StormSurgeAdvisory1_3, fg3, 'red')]:
            for _, r in df.iterrows():
                simple_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
                geo_j = simple_geo.to_json()
                geo_j = flm.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': clr})
                fg.add_child(geo_j)
                map.add_child(fg)

        fg1.add_to(map)
        fg2.add_to(map)
        fg3.add_to(map)
        flm.LayerControl(collapsed=False).add_to(map)

        # map.save('map.html')
        st_map = st_folium(map, width=1600)
        return st_map

    tot_pop = df1['Population'].sum()
    pop_growth = int(df1['Population'].sum()) - 102897634
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("This map sponsored by Omdena and United Nations (Habitat) provides information regarding vulnerable areas in the Philippines. It shows previous data around 3 indexes: Poverty, Health and Climate Disaster vulnerability and aims to aid NGOs, government officials and citizens in better understanding the Philippines and its most vulnerable areas. The tool also projects to the future by predicting areas at most risk with the goal of providing entities with an effective tool that would help them appropriately distribute resources and aid. ")

    with col2:
        st.metric('Hospitals by Province', 52448, help='Help')

    # Set columns.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Create lists for dropdowns.
        prov_list = list(df1['Province'].unique())
        prov_list.sort()
        province = st.selectbox(
            'Select Province', prov_list, len(prov_list) - 1,
            help='Select the Province, and then click on the map for city statistics.'
        )
    with col2:
        # Find the number of hospitals in the province,
        # calculate the population in the province, calculate the
        # total population and number of people per hospital.
        # Calculate if the number of hospitals is over or under
        # the average by number of hospitals
        hospitals = int(df1.groupby(['Province'])['Hospital'].sum()[province])
        prov_pop = df1.groupby(['Province'])['Population'].sum()[province]
        per_pop = int(df1['Population'].sum() / df1['Hospital'].sum())
        act_pop = prov_pop / per_pop
        diff = int(hospitals - act_pop)
        st.metric('Hospitals by Province', hospitals, f'{diff} from national average')

    with col3:
        prov_pop = df1.groupby(['Province'])['Population'].sum()[province]
        st.metric('Province Population', prov_pop, 'Total')

    with col4:
        st.metric('Total Population', tot_pop, f'{pop_growth} from last year')
    with st.container():
        map_ph(df1, province)

if __name__ == "__main__":
    main()
