import streamlit as st
import pandas as pd
import os
import pickle as pkl
from PIL import Image

APP_TITLE = 'Philippines - Urban Vulnerability Levels'
st.set_page_config(page_title='Home', layout='wide')
print('hello')

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
        background-color: #daf2bf;
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

    # Load data and create data frames for the Model
    data = get_data('src/tasks/task-5-web-app-deployment/data/model')
    df_disaster = data['disaster']
    df_dweg = data['dweg']
    df_health = data['health']
    df_industry = data['industry_II']
    df_poverty = data['poverty']

    # Create columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Cluster Predicted Outcome')
        Disaster, Economy, Health, Industry, Poverty = (
            'src/tasks/task-5-web-app-deployment/pckls/disaster.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/dweg.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/health.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/industry_II.pkl',
            'src/tasks/task-5-web-app-deployment/pckls/poverty.pkl')

        # Create a dictionary of models
        models = {'Disaster': Disaster, 'Economy': Economy,
        'Health': Health, 'Industry': Industry, 'Poverty': Poverty}

        # Create a list of model names
        model_names = models.keys()

        # Set default option
        option = 'Disaster'

        # Create a drop down menu
        with open(models[option], 'rb') as file:
            kmeans = pkl.load(file)


        def load_df():
            """
            Loads the correct data frame from the options drop down

            Returns:
                pd.Dataframe: Returns relevant data frame
            """
            if option == 'Disaster':
                return df_disaster.iloc[: , :-2]
            elif option == 'Economy':
                return df_dweg.iloc[: , :-2]
            elif option == 'Health':
                return df_health.iloc[: , :-2]
            elif option == 'Industry':
                return df_industry.iloc[: , :-2]
            elif option == 'Poverty':
                return df_poverty.iloc[: , :-2]
        
        
        def get_cluster(city):
            """
            Create clusters for mapping to output

            Args:
                city (str): City name

            Returns:
                str: Vulnerability level
            """
            x = load_df().loc[city].values.reshape(1, -1)
            cluster = kmeans.predict(x)[0]
            map_dict = {
                ('Industry', 0): 'Low',
                ('Industry', 2): 'Medium',
                ('Industry', 1): 'High',
                ('Health', 1): 'Low',
                ('Health', 0): 'Medium',
                ('Health', 2): 'High',
                ('Poverty', 0): 'Low',
                ('Poverty', 1): 'Medium',
                ('Poverty', 2): 'High',
                ('Disaster', 2): 'Low',
                ('Disaster', 0): 'Medium',
                ('Disaster', 1): 'High',
                ('Economy', 2): 'Low',
                ('Economy', 0): 'Medium',
                ('Economy', 1): 'High'}
            return map_dict.get((option, cluster), None)


        def display_sliders():
            """
            Creates sliders

            Returns:
                st.slider: Slider values based on cluster
            """
            sliders = {}
            for col in load_df().columns:
                min_val = load_df()[col].min()
                max_val = load_df()[col].max()
                val = load_df()[col].loc[selected_city]
                sliders[col] = st.slider(f'''**{col}**''', min_value = float(min_val), max_value = float(max_val), value = float(val))
            return sliders

        # Create a nested column for the city selection and the model selection.
        subcol1, subcol2 = col1.columns(2)
        subcol1.subheader('City Selection')
        # Add a dropdown to select the city.
        selected_city = subcol1.selectbox('Select a city:', load_df().index)

        subcol2.subheader('Pillar Selection')
        # Add a dropdown to select the model.
        option = subcol2.selectbox(
            'Please Select the Pillar', options=model_names,
            help='Here are 5 pillars that can influence the vulnerability of a City')

        # Display the current cluster group for the selected city in an info panel.
        cluster = get_cluster(selected_city)
        
        st.info(f'Level of Vulnerability: **{cluster}**', icon='ℹ️')
        
        # Display the slider widgets.
        sliders = display_sliders()

        st.subheader('Cluster Prediction')
        st.markdown('''<p class="predict">The slider values above can be moved to change the values in the pillars and used to re-predict the cluster group for the selected city by clicking <b>ReCalculate</b> below.</p>''', unsafe_allow_html=True)

        # Add a button to recalculate the cluster group and display in an info panel.
        if st.button('ReCalculate', use_container_width=True):
            x = pd.DataFrame(sliders, index=[selected_city])
            new_cluster = kmeans.predict(x)[0]
            map_dict = {
                ('Industry', 0): 'Low',
                ('Industry', 2): 'Medium',
                ('Industry', 1): 'High',
                ('Health', 1): 'Low',
                ('Health', 0): 'Medium',
                ('Health', 2): 'High',
                ('Poverty', 0): 'Low',
                ('Poverty', 1): 'Medium',
                ('Poverty', 2): 'High',
                ('Disaster', 2): 'Low',
                ('Disaster', 0): 'Medium',
                ('Disaster', 1): 'High',
                ('Economy', 2): 'Low',
                ('Economy', 0): 'Medium',
                ('Economy', 1): 'High'}
            new_value = map_dict.get((option, new_cluster), None)

            st.info(f'Level of Vulnerability: **{new_value}**', icon='ℹ️')

    with col2:
            st.markdown('The clustering model can help in mapping vulnerabilities of different municipalities in Philippines into different clusters on the basis of different pillars:') 
            st.markdown('- Economy') 
            st.markdown('- Disaster') 
            st.markdown('- Industry')
            st.markdown('- Health')
            st.markdown('- Poverty')
            st.markdown('This application can help us in identifying the improvements required in different areas(features) to move a particular municipality from high vulnerability cluster to low vulnerability cluster.')
            st.markdown("We collected data from two main sources, Department of Trade and Industry (DTi) and the Philippine Statistics Authority (PSA).")
            st.markdown("The DTi data was used to create the 5 indexes: Decent work and Economic growth, Disaster, Industry, Innovation and Infrastructure, Healthcare and Poverty.")
            st.markdown("The Philippine Statistics Authority data was used to create the Industry index.")
            st.markdown("The clusters were then mapped to the vulnerability levels: Low, Medium and High.")
            st.markdown("The tool also allows users to change the values of the sliders and see how the vulnerability level changes.")
            st.markdown("You can download the PDF file containing the full DTI Metadata for a better understanding of the values below.")
            with open("src/tasks/task-5-web-app-deployment/assets/dti-index-data-dict.pdf", "rb") as file:
                btn = st.download_button(
                        label="Download Pdf",
                        data=file,
                        file_name="dti-index-data-dict.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )


if __name__ == "__main__":
    main()
