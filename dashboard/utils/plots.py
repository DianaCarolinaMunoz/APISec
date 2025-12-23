import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def plot_by_language(df, language, group_by="year"):
    
    df_lang = df[df['language'] == language].copy()
    
    if df_lang.empty:
        st.warning(f"No hay datos para el lenguaje {language.capitalize()}.")
        return None
    
   
    df_lang['commit_date'] = pd.to_datetime(df_lang['commit_date'])
    df_lang['dep_count'] = pd.to_numeric(df_lang['dep_count'], errors='coerce').fillna(0)
    
    # 'period'
    if group_by == "year":
        df_lang['period'] = df_lang['commit_date'].dt.year.astype(str)
        title_suffix = "per Year (Stacked)"
    elif group_by == "month":
        df_lang['period'] = df_lang['commit_date'].dt.to_period('M').astype(str)
        title_suffix = "per Month (Grouped)"
    else:
        df_lang['period'] = df_lang['commit_date'].dt.date.astype(str)
        title_suffix = "per Day (Grouped)"
    
    ordered_class = ['Both', 'Only SecSchemes', 'Only SecDef', 'Undef Sec (OAS)']
    
 
    grouped = df_lang.groupby(['period', 'classification'], as_index=False)['dep_count'].sum()
    
    if grouped.empty:
        st.warning(f"There is no data after grouping for {language.capitalize()}.")
        return None
    
    # Pivot
    pivot = grouped.pivot(index='period', columns='classification', values='dep_count').fillna(0)
    pivot = pivot.reindex(columns=ordered_class, fill_value=0)
    pivot = pivot.astype(float)
    
    if pivot.sum().sum() == 0:
        st.warning(f"There is no data for {language.capitalize()}.")
        return None
    
  
    if group_by == "year":
        current_years = pd.to_numeric(pivot.index)
        min_year = int(current_years.min())
        max_year = int(current_years.max())
        full_years = [str(y) for y in range(min_year, max_year + 1)]
        pivot = pivot.reindex(full_years, fill_value=0)
    
 
    
    # if pivot.empty:
    #     st.warning(f"There is no data for {language.capitalize()}.")
    #     return None
    
    
    pivot = pivot.sort_index()
    
    # Colores
    colors = {
        'Both':           '#226600',
        'Only SecSchemes':'#94c309',
        'Only SecDef':    '#8cff66',
        'Undef Sec (OAS)':'#f90000'
    }
    
    # Crear figura
    fig = go.Figure()
    
    for classification in ordered_class:
        fig.add_trace(go.Bar(
            x=pivot.index,
            y=pivot[classification],
            name=classification,
            marker_color=colors[classification]
        ))
    
    
    if group_by == "year":
        fig.update_layout(barmode='stack')
    else:
        fig.update_layout(barmode='group')
    
 
    fig.update_layout(
        title=f"Dependencies in {language.capitalize()} {title_suffix}",
        xaxis_title="Year" if group_by == "year" else "Period",
        yaxis_title="Number of Dependencies",
        height=600,
        legend_title="OpenAPI Security Classification",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
       
    )
    
  
    if group_by == "year":
        totals = pivot.sum(axis=1)
        for period in totals.index:
            total = totals[period]
            if total > 0:
                fig.add_annotation(
                    x=period,
                    y=total,
                    text=f"<b>{int(total)}</b>",
                    showarrow=False,
                    yshift=12,
                    font=dict(size=14, color="black"),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="black",
                    borderwidth=1,
                    borderpad=4
                )
    
    # st.write("Data:")
    # st.dataframe(pivot)
    
    return fig