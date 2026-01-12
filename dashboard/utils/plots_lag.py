import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt # type: ignore
import streamlit as st



def plot_ecosystem_lag_matplotlib(df_eco):
    fig = plt.figure(figsize=(12, 7))  # un poco más pequeño que 16×9 para web

    order = df_eco.groupby("repo")["ecosystem_technical_lag_days"].median().sort_values(ascending=False).index
    data_to_plot = [df_eco[df_eco["repo"] == repo]["ecosystem_technical_lag_days"].dropna().values 
                    for repo in order]

    bp = plt.boxplot(data_to_plot,
                     patch_artist=True,
                     widths=0.6,
                     vert=True,
                     labels=order,
                     boxprops=dict(facecolor="lightblue", color="black", linewidth=1.2),
                     medianprops=dict(color="red", linewidth=2),
                     whiskerprops=dict(color="black", linewidth=1.2),
                     capprops=dict(color="black", linewidth=1.2),
                     flierprops=dict(marker="o", markersize=3, markerfacecolor="gray", 
                                     markeredgecolor="black", alpha=0.6))

    for patch in bp['boxes']:
        patch.set_facecolor("#8fb9d9")

    plt.title(f"Ecosystem Technical Lag per Repository\n{len(df_eco)} Detected Vulnerabilities",
              fontsize=16, pad=20, fontweight="bold")
    plt.xlabel("Repository", fontsize=12)
    plt.ylabel("Days (Ecosystem Technical Lag)", fontsize=12)
    plt.xticks(rotation=60, ha="right", fontsize=9)
    plt.yscale("log")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()

    return fig


# =========================================================================
# 2. Project Adoption Lag boxplot
# =========================================================================

def plot_adoption_lag_matplotlib(df_adopt_ok):
    fig = plt.figure(figsize=(12, 7))

    order = df_adopt_ok.groupby("repo")["adoption_lag_days"].median().sort_values(ascending=False).index
    data_to_plot = [df_adopt_ok[df_adopt_ok["repo"] == repo]["adoption_lag_days"].dropna().values 
                    for repo in order]

    bp = plt.boxplot(data_to_plot,
                     patch_artist=True,
                     widths=0.6,
                     vert=True,
                     labels=order,
                     boxprops=dict(facecolor="lightblue", color="black", linewidth=1.2),
                     medianprops=dict(color="red", linewidth=2),
                     whiskerprops=dict(color="black", linewidth=1.2),
                     capprops=dict(color="black", linewidth=1.2),
                     flierprops=dict(marker="o", markersize=3, markerfacecolor="gray", 
                                     markeredgecolor="black", alpha=0.6))

    for patch in bp['boxes']:
        patch.set_facecolor("#8fb9d9")

    plt.title(f"Project Adoption Lag per Repository\n{len(df_adopt_ok)} patched vulnerabilities",
              fontsize=16, pad=20, fontweight="bold")
    plt.xlabel("Repository", fontsize=12)
    plt.ylabel("Days (Project Adoption Lag)", fontsize=12)
    plt.xticks(rotation=60, ha="right", fontsize=9)
    plt.yscale("log")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()

    # ticks personalizados (como tenías)
    plt.gca().yaxis.set_major_formatter(plt.ScalarFormatter())
    plt.yticks([1, 10, 100, 500, 1000])

    return fig
    

