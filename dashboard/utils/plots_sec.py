import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ────────────────────────────────────────────────
st.set_page_config(page_title="Evolution Security Schemes", layout="wide")


# ────────────────────────────────────────────────
def plot_security_by_language( df: pd.DataFrame,language: str,height: int = 550,title_suffix: str = ""):
    df_lang = df[df['language'] == language].copy()
    
    if df_lang.empty:
        st.warning(f"Not data found {language.upper()}.")
        return None
    
   
    df_lang['year_str'] = df_lang['year_str'].astype(str)
    df_lang['count'] = pd.to_numeric(df_lang['count'], errors='coerce').fillna(0).astype(int)
    
    
    colors = {
        'apiKey':          "#32AA10",
        'http_bearer':     "#0effcb",
        'http_bearer_jwt': "#78a37c",
        'oauth2':          "#568d56",
        'http_basic':      "#c4bfae",
        'openIdConnect':   "#e377c2",
        'http_other':      "#b9b5b4",
        'otros':           "#bcbd22",
        
        'unknown':         "#999999"
    }
    
    # By order
    category_order = ['apiKey', 'oauth2', 'http_bearer', 'http_basic', 
                      'openIdConnect', 'http_bearer_jwt', 'http_other', 'otros']
    
    fig = px.bar(
        df_lang,
        x="year_str",
        y="count",
        color="auth_group",
        barmode="stack",
        title=f"Security Schemes in {language.upper()}{title_suffix}",
        labels={
            "year_str": "Year",
            "count": "Number of schemes",
            "auth_group": "Security Method"
        },
        color_discrete_map=colors,
        category_orders={"auth_group": [c for c in category_order if c in df_lang['auth_group'].unique()]},
        height=height,
        text_auto=True
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of schemes defined",
        legend_title="Security Scheme",
        hovermode="x unified",
        bargap=0.18,
        font=dict(size=13),
        title_font_size=18,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_traces(
        textposition="auto",
        textfont_size=12,
        marker_line_width=0.8,
        marker_line_color="rgba(255,255,255,0.7)"
    )
    
    return fig