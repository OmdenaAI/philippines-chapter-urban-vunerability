import streamlit as st
import pandas as pd
import pickle as pkl
import folium as flm
from streamlit_folium import st_folium

APP_TITLE = 'Mapping Urban Vulnerability areas'
st.set_page_config(page_title='Home', layout='wide')


# Load the DATA and cache.
@st.cache_data
def get_data(url):
    df = pd.read_csv(url)
    return df


url = 'src/tasks/task-5-web-app-deployment/data/merged_model_output.csv'
df = get_data(url)


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

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Sub Header Left')
        st.write('Column One')
        st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
    with col2:
        st.subheader('Sub Header Right')
        st.write('Column One')
        st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
    st.dataframe(df)
    
    # Load and read the pickle file generated from the ML python notebook
    pickle_in = open('src/tasks/task-5-web-app-deployment/model_km.pkl', 'rb')
    kmeans = pkl.load(pickle_in)

    # Function to call the predict fuction from the ML model. 
    # This function takes input the of the 5 indices and outputs the predicted cluster
    def predict_cluster(DW_EG_ind,Disaster_ind,Industry_II_ind,Healthcare_ind,Poverty_ind):
        prediction = kmeans.predict([[DW_EG_ind,Disaster_ind,Industry_II_ind,Healthcare_ind,Poverty_ind]])
        return prediction

    #Main Function
    def main():
        st.title("Cluster Prediction")
        html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;">Municipality Cluster Prediction Application </h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)

        # Take input of the 4 indices
        DW_EG_ind = st.text_input("Decent Work & Economic Growth Index","Type Here")
        Disaster_ind = st.text_input("Disaster Index","Type Here")
        Industry_II_ind = st.text_input("Industry & Infrastructure Index","Type Here")
        Healthcare_ind = st.text_input("Healthcare Index","Type Here")
        Poverty_ind = st.text_input("Poverty Index","Type Here")
        result = ""
        if st.button("Predict"):
            result = predict_cluster(DW_EG_ind,Disaster_ind,Industry_II_ind,Healthcare_ind,Poverty_ind)

if __name__ == "__main__":
    main()
