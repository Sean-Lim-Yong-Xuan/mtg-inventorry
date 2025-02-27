import streamlit as st
from tokenize import String
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# MongoDB Connection
MONGO_URI = "mongodb+srv://Sean:12345@magicdahtebahse.lfcpi.mongodb.net/"
client = MongoClient(MONGO_URI)

#Choosing the database and the collection
db = client["mtgdb"]
collection = db["otj-list"]

# Streamlit App
st.title ("🃏 MTG Card Inventory")

# Fetch Data
cards = list(collection.find({}, {"_id": 0}))

def display_data_from_mongodb():
    """Displays data from MongoDB in Streamlit."""
    try:
        collection = db.get_collection("cards") 
        data = list(collection.find())
        if data:
            df = pd.DataFrame(data)
            df = df.drop(columns=['_id'], errors='ignore') #remove mongodb's _id
            st.dataframe(df)
        else:
            st.info("No data found in MongoDB.")
    except Exception as e:
        st.error(f"Error retrieving data from MongoDB: {e}")
