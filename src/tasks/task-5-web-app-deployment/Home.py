import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import pickle as pkl
import folium as flm
from streamlit_folium import st_folium

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
        .row-widget.stSelectbox {
        padding: 10px;
        background: #ffffff;
        border-radius: 7px;
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
        .css-12w0qpk.e1tzin5v2 {
        background: #d2d2d2;
        padding: 5px 10px;
        }
        label.css-18ewatb.e16fv1kl2 {
        font-variant: small-caps;
        font-size: 1em;
        }
        .css-1xarl3l.e16fv1kl1 {
        float: right;
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
        p.res {
        font-size: 1.2rem;
        font-weight: bold;
        background-color: #fff;
        padding: 5px;
        border: 1px tomato solid;
        }
        .css-1vq4p4l h2 {
        font-size: 1.6rem;
        }
        .row-widget.stSelectbox {
        border-radius: 0;
        border: 1px tomato solid;
        }
        .st-bu {
        font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # st.image('src/tasks/task-5-web-app-deployment/assets/header.png')
    st.title(APP_TITLE)
    st.write('**Under Construction** - Please be aware we are currently building this app, so it will change over the next few weeks. Thank you for your patience.')

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
        Disaster, Eclnomy, Health, Industry, Poverty = 'src/tasks/task-5-web-app-deployment/pckls/disaster.pkl', 'src/tasks/task-5-web-app-deployment/pckls/dweg.pkl', 'src/tasks/task-5-web-app-deployment/pckls/health.pkl', 'src/tasks/task-5-web-app-deployment/pckls/industry_II.pkl', 'src/tasks/task-5-web-app-deployment/pckls/poverty.pkl'

        models = {'Disaster': Disaster, 'Eclnomy': Eclnomy,
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
            if cluster == 0:
                return 'Medium'
            elif cluster == 1:
                return 'Low'
            else:
                return 'High'
            
            
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
        <p class="res">Level of Vulnerability: {cluster}</p>
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


    map_url = 'src/tasks/task-5-web-app-deployment/data/mapping_data.parquet'
    df1 = get_map_data(map_url)

    noah_folder = 'src/tasks/task-5-web-app-deployment/data/noah'
    
    geodata = get_data_noah(noah_folder)
    gdf_StormSurgeAdvisory1_1 = geodata['StormSurgeAdvisory1_1'][0]
    gdf_StormSurgeAdvisory1_2 = geodata['StormSurgeAdvisory1_1'][1]
    gdf_StormSurgeAdvisory1_3 = geodata['StormSurgeAdvisory1_1'][2]

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

        # loop through the dataframes and create a GeoJSON layer for each row
        for df, fg, clr in [(gdf_StormSurgeAdvisory1_1, fg1, 'blue'), (gdf_StormSurgeAdvisory1_2, fg2, 'orange'), (gdf_StormSurgeAdvisory1_3, fg3, 'red')]:
            for _, r in df.iterrows():
                simple_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
                geo_j = simple_geo.to_json()
                geo_j = flm.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': clr})
                fg.add_child(geo_j)
                map.add_child(fg)
                

            parent_group = flm.FeatureGroup(name='Storm Surge Group')

            # create a control group for the feature groups
            toggleable_group = flm.plugins.FeatureGroupSubGroup(parent_group, name='Toggleable Layers')

            toggleable_group.add_to(parent_group)
            # add the control group to the map
            parent_group.add_to(map)

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

        # create layer control and add it to the map
        layer_ctrl = flm.LayerControl(collapsed=False)
        layer_ctrl.add_to(map)

        st_map = st_folium(map, width=1600)
        return st_map
    
    # Set columns.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Create lists for dropdowns.
        prov_list = list(df1['Province'].unique())
        prov_list.sort()
        province = st.selectbox(
            'Province', prov_list, len(prov_list) - 1,
            help='Select the Province'
        )
    with col2:
        st.write('place holder')

    with col3:
        st.write('place holder')

    with col4:
        st.write('place holder')
    with st.container():
        map_ph(df1, province)

if __name__ == "__main__":
    main()
    