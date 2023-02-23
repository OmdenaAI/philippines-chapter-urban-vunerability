import streamlit as st
import pandas as pd
import os
import pickle as pkl
import folium as flm
from streamlit_folium import st_folium

APP_TITLE = 'Mapping Urban Vulnerability areas'
st.set_page_config(page_title='Home', layout='wide')


# Load the DATA and cache.
@st.cache_data
def get_data():
    data_folder = "src/tasks/task-5-web-app-deployment/data/model"
    files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    dfs = {}
    for file in files:
        df_name = os.path.splitext(file)[0]
        df = pd.read_csv(os.path.join(data_folder, file))
        df = df.iloc[:, :-2]  # remove last column
        dfs[df_name] = df.set_index(df.columns[0])
    return dfs


# @st.cache_data
# def get_data(url):
#     df2 = pd.read_csv(url)
#     return df2


def main():
    # Colors:
    # Blue = #182D40
    # Light Blue = #82a6c0
    # Green = #4abd82

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
        border-radius: 8px;
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

    # col1, col2 = st.columns((1, 3))
    # with col1:
    #     st.image('assets/Omdena-Logo.png')
    # with col2:
    st.image('src/tasks/task-5-web-app-deployment/assets/header.png')
    st.title(APP_TITLE)
    st.write('**Under Construction** - Please be aware we are currently building this app, so it will change over the next few weeks. Thank you for your patience.')

    data = get_data()
    df_disaster = data["disaster"]
    df_dweg = data["dweg"]
    df_health = data["health"]
    df_industry = data["industry_II"]
    df_poverty = data["poverty"]

    with st.sidebar:
        st.header("Cluster Prediction")
        html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;">Municipality Cluster Prediction Application </h2>
        </div>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        Disaster, Economy, Health, Industry, Poverty = 'src/tasks/task-5-web-app-deployment/pckls/disaster.pkl', 'src/tasks/task-5-web-app-deployment/pckls/dweg.pkl', 'src/tasks/task-5-web-app-deployment/pckls/health.pkl', 'src/tasks/task-5-web-app-deployment/pckls/industry_II.pkl', 'src/tasks/task-5-web-app-deployment/pckls/poverty.pkl'

        models = {'Disaster': Disaster, 'Economy': Economy,
        'Health': Health, 'Industry': Industry, 'Poverty': Poverty}

        model_names = models.keys()

        option = st.selectbox(
            'Please Select the Pillar', options=model_names,
            help='Here are 5 pillars that can influence the vulnerability of a City')

        with open(models[option], 'rb') as file:
            kmeans = pkl.load(file)

        # dframe = pd.read_csv('src/tasks/task-5-web-app-deployment/dframe.csv', index_col='city_municipality')


        def load_df():
            if option == 'Disaster':
                return df_disaster
            elif option == 'Economy':
                return df_dweg
            elif option == 'Health':
                return df_health
            elif option == 'Industry':
                return df_industry
            else:
                return df_poverty
        
        
        def get_cluster(city):
            x = load_df().loc[city].values.reshape(1, -1)
            cluster = kmeans.predict(x)[0]
            if cluster == 0:
                return 'Medium'
            elif cluster == 1:
                return 'Low'
            else:
                return 'High'
            
            
        def display_sliders():
            sliders = {}
            for col in load_df().columns:
                min_val = load_df()[col].min()
                max_val = load_df()[col].max()
                val = load_df()[col].loc[selected_city]
                sliders[col] = st.slider(f'''**{col}**''', min_value = float(min_val), max_value = float(max_val), value = float(val))
            return sliders

        # Add a dropdown to select the city
        selected_city = st.selectbox('Select a city:', load_df().index)

        # Display the current cluster group for the selected city
        cluster = get_cluster(selected_city)
        result = f'''
        <p class="res">Level of Vulnerability: {cluster}</p>
        '''
        st.markdown(result, unsafe_allow_html=True)

        # Display the slider widgets
        sliders = display_sliders()

        # Add a button to recalculate the cluster group
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


    # def map_ph(data, name):
    #     cond = data[data['province'] == name]

    #     lat = data[cond]['latitude'].tolist()
    #     lon = data[cond]['longitude'].tolist()
    #     nam = data[cond]['city_municipality'].tolist()
    #     eco = data[cond]['economic_dynamism'].tolist()
    #     gov = data[cond]['government_efficiency'].tolist()
    #     inf = data[cond]['infrastructure'].tolist()
    #     res = data[cond]['resiliency'].tolist()

    #     html = '''<h4>Needs Assessment Information</h4>
    #     <b>Name: %s</b> <br /><br />
    #     <b>economic_dynamism: </b> %s <br />
    #     <b>government_efficiency: </b> %s <br />
    #     <b>infrastructure: </b> %s <br />
    #     <b>resiliency: </b> %s <br />
    #     '''

    #     if lat and lon:
    #         map = flm.Map(location=[lat[0], lon[0]], zoom_start=6, zoom_control=True, zoom_end=20, scrollWheelZoom=False)
    #     else:
    #         return None

    #     fg = flm.FeatureGroup(name='Philippines Map')

    #     for lt, ln, nm, ec, go, nf, re in zip((lat), (lon), (nam), (eco), (gov), (inf), (res)):
    #         sum_values = ec + go + nf + re

    #         def marker_size(sums):
    #             marker_sized = 0
    #             if sums > 0:
    #                 marker_sized = (10 - sums) + 10
    #             marker_sized = marker_sized * map.zoom_start / 12
    #             return int(marker_sized)

    #         def marker_color(sums):
    #             norm = colors.Normalize(vmin=0, vmax=10)
    #             cmap = cm.get_cmap('YlOrRd')
    #             marker_colored = cmap(norm(sums))
    #             return marker_colored

    #         iframe = flm.IFrame(html = html % ((nm), (ec), (go), (nf), (re)), height = 165)
    #         popup = flm.Popup(iframe, min_width=200, max_width=500)
    #         marker = flm.CircleMarker(location = [lt, ln], popup = (popup), fill_color=marker_color(sum_values), color='None', radius=marker_size(sum_values, map.zoom_level), fill_opacity = 0.7)
    #         marker.add_child(flm.Popup(html = html % ((nm), (ec), (go), (nf), (re)), min_width=200, max_width=500))
    #         fg.add_child(flm.CircleMarker(location = [lt, ln], popup = (popup), fill_color=marker_color(sum_values), color='None', radius=marker_size(sum_values), fill_opacity = 0.7))
    #         map.add_child(fg)
    #         print(sum_values)
    #         print(marker_size(sum_values))
    #     # map.save('map.html')
    #     return map

    # map_ph(df2, 'philippines')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Sub Header Left')
        st.write('Column One')
        st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")

    with col2:
        st.subheader('Sub Header Right')
        st.write('Column Two')
        st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")

if __name__ == "__main__":
    main()
