import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import pickle as pkl
import folium as flm
from streamlit_folium import st_folium
from PIL import Image

APP_TITLE = 'Mapping Urban Vulnerability areas'
st.set_page_config(page_title='Home', layout='wide')

# Load the Model DATA and cache
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


# Load the Map DATA and cache
@st.cache_data
def get_map_data(url):
    # gdf = gpd.read_parquet(url)
    df1 = pd.read_csv(url)
    # df1 = pd.DataFrame(df1.iloc[:, :-1])  # remove last column
    df1 = pd.DataFrame(df1)
    return df1


# Load the Noah DATA and cache
# @st.cache_data
# def get_data_noah(folder):
#     """
#     Load the data in a function so we can cache the files.

#     Returns:
#         pd.Dataframe: Returns a data frame.
#     """
#     data_folder = folder
#     files = [f for f in os.listdir(data_folder) if f.endswith('.parquet')]
#     gdfs = {}
#     for file in files:
#         gdf_name = os.path.splitext(file)[0]
#         gdf = gpd.read_parquet(os.path.join(data_folder, file))
#         gdfs[gdf_name] = gdf.set_index(gdf.columns[0])
#     return gdfs
    

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

    # Load data and create data frames for the Model
    # data = get_data('src/tasks/task-5-web-app-deployment/data/model')
    # df_disaster = data['disaster']
    # df_dweg = data['dweg']
    # df_health = data['health']
    # df_industry = data['industry_II']
    # df_poverty = data['poverty']

    map_url = 'src/tasks/task-5-web-app-deployment/data/all_data.csv'
    df1 = get_map_data(map_url)
    st.dataframe(df1)

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
            map = flm.Map(location=[lat[0], lon[0]], zoom_start=8, scrollWheelZoom=False)
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

        # map.save('map1.html')
        st_map = st_folium(map, width=1600)
        return st_map

    col1, col2 = st.columns(2)
    with col1:
        st.write("This map sponsored by Omdena and United Nations (Habitat) provides information regarding vulnerable areas in the Philippines. It shows previous data around 3 indexes: Poverty, Health and Climate Disaster vulnerability and aims to aid NGOs, government officials and citizens in better understanding the Philippines and its most vulnerable areas. The tool also projects to the future by predicting areas at most risk with the goal of providing entities with an effective tool that would help them appropriately distribute resources and aid. ")

    with col2:
        st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type spvuimen book. It has survived not only five centuries, but also the leap into elvutronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more rvuently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
    df1 = df1.assign(Country='Philippines')
    # st.dataframe(df1)
    # st.dataframe(df_disaster)

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
            'Select Province', prov_list, len(prov_list) - 1,
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

if __name__ == "__main__":
    main()
