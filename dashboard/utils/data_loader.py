import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv("/Users/dianacarolinamunozhurtado/Desktop/API Security/APIs Dependencies /stream/data/deprecated_deps_per_api_lang_classification.csv")

    #/Users/dianacarolinamunozhurtado/Desktop/API Security/APIs Dependencies /stream/data/deprecated_deps_per_api_lang_classification.csv
    
    
    if 'commit_date_norm' in df.columns:
        df['commit_date'] = pd.to_datetime(df['commit_date_norm']).dt.date
    elif 'commit_date' in df.columns:
        df['commit_date'] = pd.to_datetime(df['commit_date']).dt.date
    else:
        st.error("Not found")
        return pd.DataFrame()
    
    return df

def get_data():
    return load_data()