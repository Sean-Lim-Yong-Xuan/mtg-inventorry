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
otj-list = list(collection.find({}, {"_id": 0}))


