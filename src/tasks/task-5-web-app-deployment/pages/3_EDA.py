import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

APP_TITLE = 'Philippines - Urban Vulnerability Levels'
st.set_page_config(page_title='EDA', layout='wide')


# Load the DATA and cache.
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

dfs = get_data('src/tasks/task-5-web-app-deployment/data/model')

df_dweg = pd.DataFrame(dfs['dweg'])
df_disaster = pd.DataFrame(dfs['disaster'])
df_industry = pd.DataFrame(dfs['industry_II'])
df_health = pd.DataFrame(dfs['health'])
df_poverty = pd.DataFrame(dfs['poverty'])


def main():
    # Colors:
    # Blue = #182D40
    # Light Blue = #82a6c0
    # Green = #4abd82

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
        text-decoration-line: underline;
        text-decoration-color: green;
        text-underline-offset: 8px;
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
    st.write("For the Omdena Philippines Chapter - Vulnerability Analysis, we collected data from two main sources, Department of Trade and Industry (DTI) and the Philippine Statistics Authority (PSA).The final data was then segregated into following 5 pillars.")
    st.write("- Economy")
    st.write("- Disaster")
    st.write("- Industry")
    st.write("- Health")
    st.write("- Poverty")
    st.write("Each of the above pillars are then assigned with features taken from the collected dataset.This assignment is on the basis of United Nations Sustainable Development Goals and meta data information from DTI and PSA websites.")
    st.write("Let's have closer look on the data.")


# Boxplot Section
    st.markdown('#### Pillar wise data distribution of features')
    st.write("Here you can see the boxplots and outlier analysis for each of the feature under the respective pillars")
    col1,col2= st.columns(2)
    with col1:
        st.markdown('###### Economy')    
        features = df_dweg.columns.to_list()[1:6]
        fig = make_subplots(rows=1,cols=5)
        for i, feature in enumerate(features):
            fig.add_trace(go.Box(y=df_dweg[feature],name=feature),row=1,col=i+1,)
        fig.update_layout(width=1300,height=500,showlegend=False,hovermode=False)
        col1.write(fig)

    col1,col2= st.columns(2)
    with col1:
        st.markdown('###### Disaster')    
        features = df_disaster.columns.to_list()[1:6]
        fig = make_subplots(rows=1,cols=5)
        for i, feature in enumerate(features):
            fig.add_trace(go.Box(y=df_disaster[feature],name=feature),row=1,col=i+1)
        fig.update_layout(width=1300,height=500,showlegend=False,hovermode=False)
        col1.write(fig)

    col1,col2= st.columns(2)
    with col1:
        st.markdown('###### Industry')    
        features = df_industry.columns.to_list()[1:6]
        fig = make_subplots(rows=1,cols=5)
        for i, feature in enumerate(features):
            fig.add_trace(go.Box(y=df_industry[feature],name=feature),row=1,col=i+1)
        fig.update_layout(width=1300,height=500,showlegend=False,hovermode=False)
        col1.write(fig)

    
    col1,col2= st.columns(2)
    with col1:
        st.markdown('###### Health')    
        features = df_health.columns.to_list()[1:6]
        fig = make_subplots(rows=1,cols=5)
        for i, feature in enumerate(features):
            fig.add_trace(go.Box(y=df_health[feature],name=feature),row=1,col=i+1)
        fig.update_layout(width=1300,height=500,showlegend=False,hovermode=False)
        col1.write(fig)

    col1,col2= st.columns(2)
    with col1:
        st.markdown('###### Poverty')    
        features = df_poverty.columns.to_list()[1:6]
        fig = make_subplots(rows=1,cols=5)
        for i, feature in enumerate(features):
            fig.add_trace(go.Box(y=df_poverty[feature],name=feature),row=1,col=i+1)
        fig.update_layout(width=1300,height=500,showlegend=False,hovermode=False)
        col1.write(fig)
    
    st.markdown("As the main task of this project, muncipalities of Philippines are gauged on the aforementioned 5 pillars. To achieve this we used Clustering Machine Learning Algorithm and divided the municipalities in to 3 categories of vulnerabilities.")
    st.markdown("Low, Medium and High. Let's deep dive into the cluster analysis.")


# Pie Chart Section
    eco_plot= pd.DataFrame(df_dweg['Vulnerability'].value_counts())
    dis_plot= pd.DataFrame(df_disaster['Vulnerability'].value_counts())
    ind_plot= pd.DataFrame(df_industry ['Vulnerability'].value_counts())
    health_plot= pd.DataFrame(df_health['Vulnerability'].value_counts())
    poverty_plot= pd.DataFrame(df_poverty['Vulnerability'].value_counts())

    st.markdown('#### Cluster Profiles')
    st.markdown("Here are some Pie Charts showing the pillar wise vulnerability distribution as a Percentage of number of municipalities.")
    col1, col2,col3= st.columns(3)
    with col1:
        st.markdown("###### Economy")
        fig= px.pie(eco_plot,names=eco_plot.index, values=eco_plot.Vulnerability)
        fig.update_layout(width=550,height=450)
        col1.write(fig)
    with col2:
        st.markdown("###### Disaster")
        fig= px.pie(dis_plot,names=dis_plot.index, values=dis_plot.Vulnerability)
        fig.update_layout(width=550,height=450)
        col2.write(fig)
    with col3:
        st.markdown("###### Industry")
        fig= px.pie(ind_plot,names=ind_plot.index, values=ind_plot.Vulnerability)
        fig.update_layout(width=550,height=450)
        col3.write(fig)      

    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("###### Health")
        fig= px.pie(health_plot,names=health_plot.index, values=health_plot.Vulnerability)
        fig.update_layout(width=550,height=450)
        col1.write(fig)   
    with col2:
        st.markdown("###### Poverty")
        fig= px.pie(poverty_plot,names=poverty_plot.index, values=poverty_plot.Vulnerability)
        fig.update_layout(width=550,height=450)
        col2.write(fig)
    with col3:
        col3.write("")


#Barplot Section
    st.markdown("#### Feature and Cluster Analysis")
    st.markdown("Here are some bar plots showing mean of feature indices wise group by vulnerabilities.")
    eco_plot= pd
    col1, col2,col3= st.columns(3)
    with col1:
        st.markdown("###### Economy")
        feature_option = df_dweg.drop(['Cluster_Id','Vulnerability'],axis=1).columns.to_list()
        feature = st.selectbox('Feature Selection',feature_option[1:])
        eco_bar = pd.DataFrame(df_dweg[feature].groupby(df_dweg['Vulnerability']).mean())
        fig = px.bar (eco_bar,y=eco_bar.index,x=feature,color=eco_bar.index,color_discrete_sequence=['red','lightblue','blue'])
        fig.update_layout(width=550,height=450)
        st.write(fig)

    with col2:
        st.markdown("###### Disaster")
        feature_option = df_disaster.drop(['Cluster_Id','Vulnerability'],axis=1).columns.to_list()
        feature = st.selectbox('Feature Selection',feature_option[1:])
        dis_bar = pd.DataFrame(df_disaster[feature].groupby(df_disaster['Vulnerability']).mean())
        fig = px.bar (dis_bar,y=dis_bar.index,x=feature,color=dis_bar.index,color_discrete_sequence=['red','lightblue','blue'])
        fig.update_layout(width=550,height=450)
        st.write(fig)

    with col3:
        st.markdown("###### Industry")
        feature_option = df_industry.drop(['Cluster_Id','Vulnerability'],axis=1).columns.to_list()
        feature = st.selectbox('Feature Selection',feature_option[1:])
        ind_bar = pd.DataFrame(df_industry[feature].groupby(df_industry['Vulnerability']).mean())
        fig = px.bar (ind_bar,y=ind_bar.index,x=feature,color=ind_bar.index,color_discrete_sequence=['red','lightblue','blue'])
        fig.update_layout(width=550,height=450)
        st.write(fig)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("###### Health")
        feature_option = df_health.drop(['Cluster_Id','Vulnerability'],axis=1).columns.to_list()
        feature = st.selectbox('Feature Selection',feature_option[1:])
        health_bar = pd.DataFrame(df_health[feature].groupby(df_health['Vulnerability']).mean())
        fig = px.bar (health_bar,y=health_bar.index,x=feature,color=health_bar.index,color_discrete_sequence=['red','lightblue','blue'])
        fig.update_layout(width=550,height=450)
        col1.write(fig)

    with col2:
        st.markdown("###### Poverty")
        feature_option = df_poverty.drop(['Cluster_Id','Vulnerability'],axis=1).columns.to_list()
        feature = st.selectbox('Feature Selection',feature_option[1:])
        pov_bar = pd.DataFrame(df_poverty[feature].groupby(df_poverty['Vulnerability']).mean())
        fig = px.bar (pov_bar,y=pov_bar.index,x=feature,color=pov_bar.index,color_discrete_sequence=['red','lightblue','blue'])
        fig.update_layout(width=550,height=450)
        col2.write(fig)

    with col3:
        st.markdown("")



if __name__ == "__main__":
    main()
