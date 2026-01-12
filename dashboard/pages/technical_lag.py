import streamlit as st
import pandas as pd
from utils.data_loader import get_data
from utils.plots_lag import plot_ecosystem_lag_matplotlib, plot_adoption_lag_matplotlib
from threading import RLock

_lock = RLock()

@st.cache_data(ttl=3600)
def prepare_lag_data():
    raw = get_data()
    df_adopt = raw["lag_csv"].copy()
    
    json_data = raw["lag_json"]
    
    
    commits = []
    
    if isinstance(json_data, dict):
       
        for key in ["results", "data", "commits", "items"]:
            if key in json_data and isinstance(json_data[key], list):
                commits = json_data[key]
                break
    elif isinstance(json_data, list):
        commits = json_data
   

 
    repo_map = {}
    for c in commits:
        if not isinstance(c, dict):
            continue
        api_id = c.get("api_spec_id")
        if api_id is None:
            continue
        repo_full = c.get("repo", "unknown")
        repo_name = repo_full.split("/")[-1] if "/" in repo_full else repo_full
        repo_map[api_id] = repo_name

    df_adopt["repo"] = df_adopt["api_spec_id"].map(repo_map)
    df_adopt["dependency_name"] = df_adopt["dependency_vuln"].apply(lambda x: str(x).split("_")[0])

    df_adopt_ok = df_adopt[
        (df_adopt["adopted"] == True) & 
        (df_adopt["adoption_lag_days"].notna())
    ].copy()

    # df_eco
    eco_rows = []
    for c in commits:
        if not isinstance(c, dict):
            continue
        api_id = c.get("api_spec_id")
        repo = repo_map.get(api_id, "unknown")
        vulns = c.get("dependencies_with_vulnerabilities", {})
        if not isinstance(vulns, dict):
            continue
        for ecosystem, deps in vulns.items():
            if not isinstance(deps, list):
                continue
            for dep in deps:
                if not isinstance(dep, dict):
                    continue
                lag = dep.get("technical_lag_avg_days")
                if lag is not None and pd.notna(lag):
                    eco_rows.append({
                        "api_spec_id": api_id,
                        "repo": repo,
                        "ecosystem_technical_lag_days": lag
                    })

    df_eco = pd.DataFrame(eco_rows)
    
    return df_eco, df_adopt_ok


#  ────────────────────────────────────────────────────────────────
df_eco, df_adopt_ok = prepare_lag_data()


st.title("Technical Lag and Adoption Lag")


if df_eco.empty and df_adopt_ok.empty:
    st.warning("No data found.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Ecosystem Lag", "Adoption Lag", "Summary"])

with tab1:
    if not df_eco.empty:
        with _lock:
            fig1 = plot_ecosystem_lag_matplotlib(df_eco)
        st.plotly_chart(fig1, use_container_width=True)  
    else:
        st.info("No data for Ecosystem Technical Lag")

with tab2:
    if not df_adopt_ok.empty:
        with _lock:
            fig2 = plot_adoption_lag_matplotlib(df_adopt_ok)
        st.plotly_chart(fig2, use_container_width=True)  
    else:
        st.info("No data for Project Adoption Lag")

with tab3:
    repos_con_vuln = df_eco['repo'].nunique() if not df_eco.empty and 'repo' in df_eco.columns else 0
    repos_adoptaron = df_adopt_ok['repo'].nunique() if not df_adopt_ok.empty and 'repo' in df_adopt_ok.columns else 0
    
    ecosystem_median = f"{df_eco['ecosystem_technical_lag_days'].median():.1f}" if not df_eco.empty else "N/A"
    adoption_median = f"{df_adopt_ok['adoption_lag_days'].median():.1f}" if not df_adopt_ok.empty else "N/A"

    st.markdown(f"""
    ### Summary
    - **Repos with detected vulnerabilities**: {repos_con_vuln}  
    - **Repos that adopted at least one fix**: {repos_adoptaron}  
    - **Repos that never adopted any fix**: {repos_con_vuln - repos_adoptaron}  
    - **Ecosystem lag median (all)**: {ecosystem_median} days  
    - **Adoption lag median (only adopted)**: {adoption_median} days
    """)