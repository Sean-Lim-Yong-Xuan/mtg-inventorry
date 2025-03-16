import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb+srv://Cluster0:123@cluster0.wi9dl.mongodb.net/"
client = MongoClient(MONGO_URI)

#Choosing the database and the collection
#db = client["mtgdb"]
#collection = db["cards"]


#client = MongoClient("mongodb+srv://Sean:12345@magicdahtebahse.lfcpi.mongodb.net/")
db = client["mtgdb"]
collection = db["allmtgcards"]

# Streamlit App
st.title("🃏 MTG Card Inventory")

# Fetch Data
#def load_data():
    #cards = list(collection.find({}, {"_id":0}))
    #df = pd.DataFrame(cards)
    #return df

#df = load_data()
allmtgcards = list(collection.find({}, {"_id": 0}))  # Exclude ObjectId

def display_data_from_mongodb():
    """Displays data from MongoDB in Streamlit."""
    try:
        collection = db.get_collection("allmtgcards")  # Replace with your collection name
        data = list(collection.find())
        if data:
            df = pd.DataFrame(data)
            df = df.drop(columns=['_id'], errors='ignore') #remove mongodb's _id
            st.dataframe(df)
        else:
            st.info("No data found in MongoDB.")
    except Exception as e:
        st.error(f"Error retrieving data from MongoDB: {e}")

#Fetching data...
allmtgcards = list(collection.find({}, {"_id": 0}))

if allmtgcards:
    df = pd.DataFrame(allmtgcards)
    st.dataframe(df)
    # Search bar
    search_query = st.text_input("Search for a card:", "")
    
    # Filter options
    card_types = df["type"].dropna().unique().tolist()
    subtypes = df["subtype"].dropna().unique().tolist()
    colors = df["color"].dropna().unique().tolist()
    
    selected_type = st.multiselect("Filter by Type:", card_types)
    selected_subtype = st.multiselect("Filter by Subtype:", subtypes)
    selected_colors = st.multiselect("Filter by Color:", colors)
    
    # Apply filters
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_query, case=False, na=False)]
    if selected_type:
        filtered_df = filtered_df[filtered_df["type"].isin(selected_type)]
    if selected_subtype:
        filtered_df = filtered_df[filtered_df["subtype"].isin(selected_subtype)]
    if selected_colors:
        filtered_df = filtered_df[filtered_df["color"].isin(selected_colors)]
    
    st.write(f"### Showing {len(filtered_df)} results")
    st.dataframe(filtered_df)
    
    # Visualization
    chart_option = st.selectbox("Select a chart type:", ["Color Distribution", "Type Distribution", "Subtype Distribution"])
    
    if chart_option == "Color Distribution":
        fig = px.bar(filtered_df["color"].value_counts().reset_index(), x="index", y="Color", title="Color Distribution")
    elif chart_option == "Type Distribution":
        fig = px.bar(filtered_df["type"].value_counts().reset_index(), x="index", y="Type", title="Type Distribution")
    elif chart_option == "Subtype Distribution":
        fig = px.bar(filtered_df["subtype"].value_counts().reset_index(), x="index", y="Subtype", title="Subtype Distribution")
    
    st.plotly_chart(fig)
