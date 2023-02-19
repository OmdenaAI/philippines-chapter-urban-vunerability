import streamlit as st
import pandas as pd
import numpy as np
import missingno as msno
import altair as alt
import io

APP_TITLE = 'Mapping Urban Vulnerability areas'
st.set_page_config(page_title='EDA', layout='wide')


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
        st.markdown('#### df.info()')
        buffer = io.StringIO()
        df.info(buf=buffer)
        s1 = buffer.getvalue()

        st.text(s1)

    with col2:
        st.subheader('Sub Header Right')
        st.write('Column One')
        st.markdown('#### df.head(10)')
        st.dataframe(df.head(10))
        st.markdown('#### df.shape')
        st.dataframe(df.shape)
        st.markdown('#### msno.matrix(df)')
        g = msno.matrix(df)
        st.pyplot(g.figure)


if __name__ == "__main__":
    main()
