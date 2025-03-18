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
    st.info("Successfully connected to MongoDB!!")
    # Search bar
    search_query = st.text_input("Search for a card:", "")
    
    # Filter options
    card_types = df["type"].dropna().unique().tolist()
    colors = df["color_identity"].dropna().unique().tolist()
    power = df["power"].dropna().unique().tolist()
    
    selected_type = st.multiselect("Filter by Type:", card_types)
    selected_colors = st.multiselect("Filter by Color:", colors)
    selected_power = st.multiselect("Filter by Power:", power)
    
    # Apply filters
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_query, case=False, na=False)]
    if selected_type:
        filtered_df = filtered_df[filtered_df["type"].isin(selected_type)]
    if selected_colors:
        filtered_df = filtered_df[filtered_df["color_identity"].isin(selected_colors)]
    if selected_power:
        filtered_df = filtered_df[filtered_df["power"].isin(selected_power)]
    
    st.write(f"### Showing {len(filtered_df)} results")
    st.dataframe(filtered_df)
    
    # Visualization
    chart_option = st.selectbox("Select a chart type:", ["Color Identity Distribution", "Type Distribution", "Power Distribution"])
    
    if chart_option == "Color Identity Distribution":
        st.write ("Data Obtained")
        fig = px.bar(filtered_df["color_identity"].value_counts().reset_index(), x="color_identity", y="count", title="Color Identity Distribution")
    elif chart_option == "Type Distribution":
        fig = px.bar(filtered_df["type"].value_counts().reset_index(), x="type", y="count", title="Type Distribution")
    elif chart_option == "Power Distribution":
        category_column = st.selectbox("count", df.columns)
        value_column = st.selectbox("power", df.columns)

        if category_column and value_column:
            try:
                # Group by category and sum the values
                grouped_df = df.groupby(category_column)[value_column].sum().reset_index()

                # Create the pie chart
                fig = px.pie(grouped_df, values=value_column, names=category_column, title=f"Pie Chart of {value_column} by {category_column}")
                #st.plotly_chart(fig)
        #fig = px.bar(filtered_df["power"].value_counts().reset_index(), x="power", y="count", title="Power Distribution")
    else:
        st.write ("No chart.")

    st.plotly_chart(fig)
