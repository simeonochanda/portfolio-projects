from turtle import pd
from panel import Row
import streamlit as st
import process
import pickle
import pandas as pd

#loading the best model and vectorizer
vect = pickle.load(open('Output/n_gram.pkl', 'rb'))
model = pickle.load(open('Output/n_gram_lr.pkl', 'rb')) 

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    #transforming the data
    df_cleaned = df.iloc[:, 0].apply(process.process, stem='p')
    #df_cleaned = df.iloc[:, 0].apply(process.process, args=(Row,), stem='p')
    transformed_message = vect.transform(df_cleaned)
    #predicting the message
    prediction = model.predict(transformed_message)
    #displaying the result
    st.write("Cleaned Data:")
    df_combined = pd.DataFrame({
    'Original Data': df.iloc[:, 0],
    'Cleaned Data': df_cleaned,
    'Predicted Sentiment': prediction,
    })
    st.dataframe(df_combined)
    #st.dataframe(transformed_message_dense)
    #st.dataframe(transformed_message)
    
    st.markdown("### Download Cleaned Data")
    st.write("Click below to download the cleaned dataset:")
    csv = df_combined.to_csv(index=False)
    st.download_button("Download CSV", csv, mime='text/csv', key="download_button")









