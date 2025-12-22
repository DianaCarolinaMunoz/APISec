import plotly.express as px

def plot_by_language(df, language):
    
    df_lang = df[df['language'] == language]
    daily = df_lang.groupby(['commit_date', 'classification'])['dep_count'].sum().reset_index()


    
    fig = px.bar(daily, x='commit_date', y='dep_count', color='classification',
                 barmode='group', height=600,
                 title=f"Deprecated Dependencies  {language.capitalize()}",
                 color_discrete_map={
                     'Both': '#226600',
                     'Only SecSchemes': '#94c309', 
                     'Only SecDef': '#8cff66',
                     'Undef Sec (OAS)': '#f90000'
                 })
    fig.update_xaxes(tickangle=45)
    fig.update_layout(legend_title="Clasificación OpenAPI")
    return fig