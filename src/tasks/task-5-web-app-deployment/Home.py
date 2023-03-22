import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import folium as flm
from streamlit_folium import st_folium
from PIL import Image

APP_TITLE = 'Philippines - Urban Vulnerability Levels'
st.set_page_config(page_title='Home', layout='wide')

# Load the Model DATA and cache
@st.cache_data
def get_data(folder):
    """
    Loads the data via a function so we can cache the files.

    Args:
        folder (str): url to the folder containing the data.

    Returns:
        dict: Returns a dictionary of data frames. File name is the key. Data frame is the values.
    """
    data_folder = folder
    files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    dfs = {}
    for file in files:
        df_name = os.path.splitext(file)[0]
        df = pd.read_csv(os.path.join(data_folder, file))
        dfs[df_name] = df.set_index(df.columns[0])
    return dfs


# Load the Map DATA and cache
@st.cache_data
def get_map_data(url):
    df1 = pd.read_csv(url)
    df1 = pd.DataFrame(df1)
    return df1


# Load the Noah DATA and cache
@st.cache_data
def get_data_noah(folder, name):
    """
    Reads all files inside a directory and creates a dataframe for each file.
    The dataframe names are created from the df parameter plus an incremental number n.

    Args:
        folder (str): Path to the directory containing the files.
        name (str): Base name for the dataframes.

    Returns:
        list: A list of dataframes.
    """
    # Get all files inside the directory
    files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    
    # Create a list to store the dataframes
    dataframes = []
    
    # Loop through each file and create a dataframe for it
    for i, file in enumerate(files):
        file_path = os.path.join(folder, file)
        df_name = f'{name}_{i}'
        df = gpd.read_parquet(file_path)
        dataframes.append(df)
    
    return dataframes


# Create the landing page
def main():
    # Base Colors:
    # Blue = #182D40
    # Light Blue = #82a6c0
    # Green = #4abd82

    # Add custom CSS
    st.markdown(
        """
        <style>
        .css-k1ih3n {
            padding: 2rem 1rem 10rem;
        }
        .block-container.css-18e3th9.egzxvld2 {
        padding-top: 0;
        }
        header.css-vg37xl.e8zbici2 {
        background: none;
        }
        span.css-10trblm.e16nr0p30 {
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
        text-decoration-line: underline;
        text-decoration-color: green;
        text-underline-offset: 8px;
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
        .st-bu {
        font-weight: bold;
        }
        .css-1whk732 {
        -webkit-box-pack: end;
        justify-content: flex-end;
        flex: 1 1 0%;
        }
        .css-184tjsw p {
        word-break: break-word;
        font-size: 1rem;
        font-weight: bold;
        }
        button.css-fxzapv.edgvbvh10 {
        background-color: #2627301f;
        }
        </style>
        """, unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns((1, 1, 1))
    with col1:
        image2 = Image.open('src/tasks/task-5-web-app-deployment/assets/Omdena.png')
        st.image(image2)

    with col2:
        st.write('')

    with col3:
        image1 = Image.open('src/tasks/task-5-web-app-deployment/assets/UNHABITAT.png')
        st.image(image1)

    st.title(APP_TITLE)

    map_url = 'src/tasks/task-5-web-app-deployment/data/all_data.csv'
    df1 = get_map_data(map_url)

    url2 = 'src/tasks/task-5-web-app-deployment/data/noah'
    name = 'storm_surge'
    df_list = get_data_noah(url2, name)

    # Add map.
    def map_ph(data, name, prov):
        cond = (
            data['country'] == name
                ) & (
                data['province'] == prov
                    )

        lat = data[cond]['latitude'].tolist()
        lon = data[cond]['longitude'].tolist()
        nam = data[cond]['city_municipality'].tolist()
        vul_0 = data[cond]['vulnerability_dist'].tolist()
        vul_1 = data[cond]['vulnerability_dweg'].tolist()
        vul_2 = data[cond]['vulnerability_indu'].tolist()
        vul_3 = data[cond]['vulnerability_heal'].tolist()
        vul_4 = data[cond]['vulnerability_povt'].tolist()
        pop = data[cond]['total_population'].tolist()
        pov = data[cond]['pov_inc'].tolist()
        hop = data[cond]['hospital'].tolist()

        html = f''' <div style="font-family: monospace;font-size: 1rem;">
        <h4 style="font-size:1.05rem;">Vulnerability Info</h4>
        <ul style="list-style-type: none;margin: 0;padding: 0;">
        <li>City/Town: </li>
        <li> <b> %s</b></li>
        <li><b>Vulnerability Levels:</b></li>
        <li>Disaster: <b> %s</b></li>
        <li>Economy: <b> %s</b></li>
        <li>Industry: <b> %s</b></li>
        <li>Health: <b> %s</b></li>
        <li>Poverty: <b> %s</b></li>
        <li>Population: <b> %s</b></li>
        <li>Poverty: <b> %s</b></li>
        <li>Hospitals: <b> %s</b></li>
        </ul>  
        </div>
        '''

        if lat and lon:
            map = flm.Map(location=[lat[0], lon[0]], zoom_start=10, scrollWheelZoom=False)
        else:
            return None

        fg = flm.FeatureGroup(name='Philippines Map')

        marker_props = {'Low': {'color': 'green', 'size': 10},
                    'Medium': {'color': 'blue', 'size': 10},
                    'High': {'color': 'red', 'size': 15}}

        for lt, ln, nm, v0, v1, v2, v3, v4, po, pv, ho in zip((lat), (lon), (nam), (vul_0), (vul_1), (vul_2), (vul_3), (vul_4), (pop), (pov), (hop)):
            iframe = flm.IFrame(html = html % ((nm), (v0), (v1), (v2), (v3), (v4), (po), (pv), int((ho))), height = 290)
            popup = flm.Popup(iframe, min_width=200, max_width=650)
            props = marker_props[v0]
            marker = flm.CircleMarker(location = [lt, ln], popup = popup, fill_color=props['color'], color='None', radius=props['size'], fill_opacity = 0.5)
            fg.add_child(marker)
            map.add_child(fg)

        flm.LayerControl(collapsed=False).add_to(map)

        # map.save('map1.html')
        st_map_ph = st_folium(map, width=1600, returned_objects=['last_object_clicked'])
        return st_map_ph

    st.write("This map sponsored by Omdena and United Nations (Habitat) provides information regarding vulnerable areas in the Philippines.")
    st.write("It shows data around 5 indexes: Economy, Disaster, Industry, Health and Poverty. Its aim is to aid NGOs, government officials and citizens in better understanding the Philippines and its most vulnerable areas.")
    st.write("The tool also projects to the future by predicting areas at most risk with the goal of providing entities with an effective tool that would help them appropriately distribute resources and aid.")
    
    df1 = df1.assign(Country='Philippines')

    # Set columns
    col1, col2 = st.columns(2)

    with col1:
        # Create lists for dropdowns
        country_list = list(df1['country'].unique())
        country_list.sort()
        country = st.selectbox(
            'Select Country', country_list, len(country_list) - 1,
            help='Select the Country, and then click on the map for city statistics.'
        )
    with col2:
        # Create lists for dropdowns
        prov_list = list(df1['province'].unique())
        prov_list.sort()
        province = st.selectbox(
            'Select Province', prov_list, index=0,
            help='Select the Province, and then click on the map for city statistics.'
        )

    with st.container():
        map_ph(df1, country, province)

    col1, col2, col3 = st.columns(3)

    with col1:
        # Find the number of hospitals in the province,
        # calculate the average and display number over/under
        hospitals = int(df1.groupby(['province'])['hospitals'].sum()[province])
        prov_pop = df1.groupby(['province'])['total_population'].sum()[province]
        per_pop = int(df1['total_population'].sum() / df1['hospitals'].sum())
        act_pop = prov_pop / per_pop
        diff = int(hospitals - act_pop)
        st.metric('Hospitals by Province', hospitals, f'{diff} from national average')

    with col2:
        # prov_pop = df1.groupby(['Province'])['Population'].sum()[province]
        st.metric('Province Population', prov_pop, 'Total')

    with col3:
        tot_pop = df1['total_population'].sum()
        pop_growth = int(df1['total_population'].sum()) - 102897634
        st.metric('Total Population', tot_pop, f'{pop_growth} from last year')

    st.subheader('Geospatial layers - Storm Surge')

    col1, col2 = st.columns(2)
    with col1:
        st.image('src/tasks/task-5-web-app-deployment/assets/layered_map.png')

    with col2:
        st.text('')

if __name__ == "__main__":
    main()
    