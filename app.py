#    Web Server App
import streamlit as st
#pip install -U streamlit
#pip install -U plotly
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer
from nltk.tokenize import word_tokenize, RegexpTokenizer
import os
import process_text
import process
from turtle import pd
from panel import Row
import pickle
import pandas as pd
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
import chardet

# Create a sidebar
st.sidebar.title("Help")

# Add help text
st.sidebar.markdown("""
Here are some tips to help you use this app:

- Enter your review in the text area.
- Click the 'Predict' button to get the prediction.
- The prediction will tell you whether the review is positive or negative.
- You can also upload a CSV file with reviews for prediction.
- you can then filter the reviews into positive or negative feedback.
- you can then download the cleaned reviews using the download button that follows.
- you can also scroll your tab downwards to view the insights and visualizations for data driven decision making""")


#creating title
st.title('REVIEW ANALYSIS PREDICTION APP')

review = st.text_area('Please enter your review for prediction')
#loading the best model and vectorizer
vect = pickle.load(open('Output/n_gram.pkl', 'rb'))
model = pickle.load(open('Output/n_gram_lr.pkl', 'rb')) 



if st.button('Predict'):
    #transforming the message
    tokens = [process_text.process_text(review, stem='p')]
    transformed_message = vect.transform(tokens)
    #predicting the message
    prediction = model.predict(transformed_message)
    #displaying the result
    if (prediction[0] == 1):
        print("positive")
        st.write(prediction)
        st.warning('positive Review')
    elif(prediction[0] == 0):
        print("negative")
        st.warning('negative Review')
        st.write(prediction)
    else:
        print("neutral")
        st.write(prediction)
st.balloons()

# Load the image
image = Image.open('C:\\Users\\ochan\\Downloads\\Visualization Image.jpg')

# Display the image
st.image(image, caption='Your Caption', use_column_width=True)

uploaded_file = st.file_uploader("Please Upload a CSV file for Prediction", type=["csv"])
if uploaded_file is not None:
        # Detect the encoding
        rawdata = uploaded_file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding'] if result is not None else None

        # Read the CSV file with the detected encoding
        uploaded_file.seek(0)  # Reset the file pointer to the beginning
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        

        # Check if the reviews column exists
        if 'reviews' in df.columns:
            df_reviews = df['reviews']
            df_reviews = df['reviews'].dropna()
            df_cleaned = df_reviews.apply(process.process, stem='p')
            transformed_message = vect.transform(df_cleaned)
            #predicting the message
            prediction = model.predict(transformed_message)
    
            #displaying the result
            st.write("Cleaned Data:")
            df_combined = pd.DataFrame({
                'Original Data': df_reviews,
                'Cleaned Data': df_cleaned,
                'Predicted Sentiment': ['positive Review' if x == 1 else 'negative Review' for x in prediction]
            })
            # Data Filtering
            st.markdown("### Data Filtering")
            sentiment_to_show = st.selectbox("Choose sentiment to display", options=["All", "positive Review", "negative Review"])
            if sentiment_to_show != "All":
                df_filtered = df_combined[df_combined['Predicted Sentiment'] == sentiment_to_show]
                st.dataframe(df_filtered)
            else:
                st.dataframe(df_combined)
            # Assuming df_combined is your DataFrame
            sentiment_counts = df_combined['Predicted Sentiment'].value_counts()
            # Word Cloud
            st.markdown("### What are the Most common Words in the reviews? ###")
            text = " ".join(review for review in df_combined['Original Data'])
            wordcloud = WordCloud(background_color='white').generate(text)

            fig, ax = plt.subplots(figsize=(10,6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)    

            # Interactive Visualizations
            st.markdown("### What is the Distribution of Review Lengths?")
            df_combined['Review Length'] = df_combined['Original Data'].str.len()
            fig = px.histogram(df_combined, x="Review Length", nbins=50)
            st.plotly_chart(fig)
            fig, ax = plt.subplots(figsize=(10,6))
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, alpha=0.8, ax=ax)

            ax.set_title('What are the Predicted Sentiment Distribution?')
            ax.set_ylabel('Number of Occurrences', fontsize=12)
            ax.set_xlabel('Sentiment', fontsize=12)

            plt.savefig("sentiment_distribution.png")
            st.pyplot(fig)
            
            #st.markdown("### What is the Relationship between Review Ratings and Review Length?")
            #fig, ax = plt.subplots(figsize=(10,6))
            #sns.scatterplot(data=df_combined, x='Review Length', y='Ratings', ax=ax)
            #ax.set_title('Relationship between Review Ratings and Review Length')
            #ax.set_ylabel('Review Ratings')
            #ax.set_xlabel('Review Length')
            #st.pyplot(fig)
            
    
            st.markdown("### Download Cleaned Data")
            st.write("Click below to download the cleaned dataset:")
            csv = df_combined.to_csv(index=False)
            st.download_button("Download CSV", csv, mime='text/csv', key="download_button")
        else:
            st.error("The uploaded file does not contain a 'reviews' column. Please Customize the column name to reviews")
