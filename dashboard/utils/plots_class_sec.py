
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def plot_security_by_classification(
    df_class,
    language="javascript",
    height=550
):
  
    df_lang = df_class[df_class['language'] == language].copy()
    
    if df_lang.empty:
        st.warning(f"No data for{language.capitalize()}")
        return None


    df_total = df_lang.groupby(['year', 'classification'])['scheme_count'].sum().reset_index()
    
    ordered_class = ['Both', 'Only SecSchemes', 'Only SecDef', 'Undef Sec (OAS)']
    pivot_total = df_total.pivot(index='year', columns='classification', values='scheme_count').fillna(0)
    pivot_total = pivot_total.reindex(columns=ordered_class, fill_value=0)

    
    hover_texts = []
    for year in pivot_total.index:
        year_text = []
        for cls in ordered_class:
            subset = df_lang[(df_lang['year'] == year) & (df_lang['classification'] == cls)]
            total = subset['scheme_count'].sum()
            if total == 0:
                detail = "no sec"
            else:
                detail_lines = [f"{row['auth_group']}: {int(row['scheme_count']):,}" 
                                for _, row in subset.sort_values('scheme_count', ascending=False).iterrows()]
                detail = "<br>".join(detail_lines)
            year_text.append(f"<b>{cls} ({int(total):,} schemes):</b><br>{detail or '—'}")
        hover_texts.append("<br><br>".join(year_text))
    
    fig = go.Figure()
    

   
    colors_map = {
        'Only SecSchemes': '#94c309',
        'Both':           '#226600',
        'Only SecDef':    '#8cff66',
        'Undef Sec (OAS)':'#f90000'
    }

    fig = go.Figure()

    
    ordered_class = ['Both', 'Only SecSchemes', 'Only SecDef', 'Undef Sec (OAS)']
    ordered_class = [c for c in ordered_class if c in pivot_total.columns] 

    for cls in ordered_class:
        fig.add_trace(
            go.Bar(
                x=pivot_total.index,
                y=pivot_total[cls],
                name=cls,
                marker_color=colors_map.get(cls, '#999999'),  
                hovertemplate=(
                    "<b>%{x}</b><br>" +
                    f"<b>{cls}</b>: %{{y:,}} schemes<extra></extra>"
                )
            )
        )
    
   
    fig.add_trace(go.Bar(
        x=pivot_total.index,
        y=pivot_total.sum(axis=1),
        marker=dict(color='rgba(0,0,0,0)'),
        hoverinfo="text",
        text=hover_texts,
        hovertemplate="%{text}<extra></extra>",
        showlegend=False
    ))
    
    fig.update_layout(
        title=f'Security Schemes in {language.capitalize()}',
        xaxis_title="Year",
        yaxis_title="Security Schemes",
        barmode='stack',
        height=height,
        legend_title="Classification",
        hovermode="x unified"
    )
    
    fig.update_xaxes(type='category')
    
    return fig