import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def plot_by_language(df, language, group_by="year", mode=None, height=None):
    
    df_lang = df[df['language'] == language].copy()
    
    if df_lang.empty:
        st.warning(f"There are no data for the language {language.capitalize()}.")
        return None
    
    df_lang['commit_date'] = pd.to_datetime(df_lang['commit_date'])
    df_lang['dep_count'] = pd.to_numeric(df_lang['dep_count'], errors='coerce').fillna(0)
    
    if group_by == "year":
        df_lang['period'] = df_lang['commit_date'].dt.year.astype(str)
        title_suffix = "per Year"
    elif group_by == "month":
        df_lang['period'] = df_lang['commit_date'].dt.to_period('M').astype(str)
        title_suffix = "per Month"
    else:
        df_lang['period'] = df_lang['commit_date'].dt.date.astype(str)
        title_suffix = "per Day"
    
    ordered_class = ['Both', 'Only SecSchemes', 'Only SecDef', 'Undef Sec (OAS)']
    
    grouped = df_lang.groupby(['period', 'classification'], as_index=False)['dep_count'].sum()
    
    if grouped.empty:
        st.warning(f"There are no data after grouping")
        return None
    
    pivot = grouped.pivot(index='period', columns='classification', values='dep_count').fillna(0)
    pivot = pivot.reindex(columns=ordered_class, fill_value=0)
    pivot = pivot.astype(float)
    
    if pivot.sum().sum() == 0:
        st.warning(f"There are no dependencies for {language.capitalize()}.")
        return None
    
    if group_by == "year":
        current_years = pd.to_numeric(pivot.index)
        min_year = int(current_years.min())
        max_year = int(current_years.max())
        full_years = [str(y) for y in range(min_year, max_year + 1)]
        pivot = pivot.reindex(full_years, fill_value=0)
    
    pivot = pivot[pivot.sum(axis=1) > 0]
    if pivot.empty:
        return None
    
    pivot = pivot.sort_index()

    # === MODE PERCENT ===
    if mode == "percent":
        totals = pivot.sum(axis=1)
        percent_pivot = pivot.div(totals, axis=0) * 100
        percent_pivot = percent_pivot.fillna(0)
        data_pivot = percent_pivot
        y_title = "Percentage of Dependencies (%)"
        plot_title = f"Percentage Distribution in {language.capitalize()} {title_suffix}"
        barmode = 'stack'  
    else:
        data_pivot = pivot
        y_title = "Number of Dependencies"
        plot_title = f"Dependencies in {language.capitalize()} {title_suffix}"
        barmode = 'stack' if group_by == "year" else 'group'
    
    
    colors = {
        'Both':           '#226600',
        'Only SecSchemes':'#94c309',
        'Only SecDef':    '#8cff66',
        'Undef Sec (OAS)':'#f90000'
    }
    
    fig = go.Figure()
    
    for classification in ordered_class:
        fig.add_trace(go.Bar(
            x=data_pivot.index,
            y=data_pivot[classification],
            name=classification,
            marker_color=colors[classification]
        ))

    
    default_height = 400 if mode == "percent" else 600  
    fig_height = height if height is not None else default_height
    
  
    
    fig.update_layout(
        title=plot_title,
        xaxis_title="Year" if group_by == "year" else "Period",
        yaxis_title=y_title,
        height=fig_height,
        barmode=barmode,
        # height=600,
        bargap=0.2,
        # legend_title="OpenAPI Security Classification",
        # legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(tickangle=0 if group_by == "year" else 45)
    )
    
    
    if mode == "percent":
        bottom = pd.Series([0.0] * len(data_pivot), index=data_pivot.index)
        for classification in ordered_class:
            values = data_pivot[classification]
            for period, pct in values.items():
                if pct > 5:  # Solo si >5%
                    fig.add_annotation(
                        x=period,
                        y=bottom[period] + pct / 2,
                        text=f"<b>{pct:.1f}%</b>",  # ← Negrita con <b>
                        showarrow=False,
                        font=dict(size=12, color="white", family="Arial"),
                        bgcolor="rgba(0,0,0,0.4)"
                    )
                bottom[period] += pct
    
    # Total Absolute Annotations for "count" mode with "year" grouping
    if mode == "count" and group_by == "year":
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
    
    
    
    # st.write(f"Data({'Porcentage' if mode == 'percent' else 'Count'}):")
    # st.dataframe(data_pivot if mode == "percent" else pivot)
    
    return fig