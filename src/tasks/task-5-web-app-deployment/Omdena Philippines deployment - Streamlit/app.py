import numpy as np
import pandas as pd
import pickle
import streamlit as st


# Load and read the pickle file generated from the ML python notebook
pickle_in = open('model.pkl','rb')
kmeans=pickle.load(pickle_in)

# Function to call the predict fuction from the ML model. 
# This function takes input the of the 5 indices and outputs the predicted cluster
def predict_cluster(DW_EG_ind,Disaster_ind,Industry_II_ind,Healthcare_ind,Poverty_ind):
    prediction=kmeans.predict([[DW_EG_ind,Disaster_ind,Industry_II_ind,Healthcare_ind,Poverty_ind]])
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
    result=""
    if st.button("Predict"):
        result = predict_cluster(DW_EG_ind,Disaster_ind,Industry_II_ind,Healthcare_ind,Poverty_ind)
    st.success('The predicted cluster is {}'.format(result))

if __name__ == "__main__":
    main()



