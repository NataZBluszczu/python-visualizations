
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Zadanie 3: Dashboard", layout="wide")
st.title("Zaawansowany Dashboard Analityczny")

@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv", sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')

df = load_data()

num_cols = df.select_dtypes(include=['number']).columns.tolist()
cat_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()

st.sidebar.header("Konfiguracja Dashboardu")

with st.sidebar.expander("1. Wybór Zmiennych", expanded=True):
    val_x = st.selectbox("Zmienna X (Główna):", num_cols, index=0)
    val_y = st.selectbox("Zmienna Y (dla Scatter Plot):", num_cols, index=1 if len(num_cols) > 1 else 0)
    
    group_col = st.selectbox("Grupowanie:", ["Brak"] + cat_cols)
    grouping = None if group_col == "Brak" else group_col

with st.sidebar.expander("2. Typ i Styl Wykresu", expanded=True):
    chart_type = st.radio("Rodzaj wykresu:", ["Wykres punktowy (Scatter)", "Histogram", "Wykres pudełkowy (Boxplot)"])
    
    base_color = st.color_picker("Wybierz kolor markerów (gdy brak grupowania):", "#1DB954")
    show_grid = st.checkbox("Pokaż siatkę pomocniczą", value=True)

df_plot = df.sample(2000, random_state=42) if len(df) > 2000 else df

tab_viz, tab_stat = st.tabs(["Wizualizacja Danych", "Podsumowanie Statystyczne"])

with tab_viz:
    st.subheader(f"Analiza: {chart_type}")
    
    fig = None
    
    if chart_type == "Wykres punktowy (Scatter)":
        fig = px.scatter(
            df_plot, x=val_x, y=val_y, 
            color=grouping,
            color_discrete_sequence=[base_color] if not grouping else None,
            opacity=0.7,
            title=f"Zależność: {val_x} vs {val_y}"
        )
        
    elif chart_type == "Histogram":
        fig = px.histogram(
            df_plot, x=val_x, 
            color=grouping,
            color_discrete_sequence=[base_color] if not grouping else None,
            nbins=40,
            barmode='overlay',
            title=f"Rozkład zmiennej: {val_x}"
        )
        
    elif chart_type == "Wykres pudełkowy (Boxplot)":
        fig = px.box(
            df_plot, x=grouping, y=val_x, 
            color=grouping,
            color_discrete_sequence=[base_color] if not grouping else None,
            title=f"Wykres pudełkowy: {val_x}" + (f" wg {grouping}" if grouping else "")
        )

    if fig:
        fig.update_xaxes(showgrid=show_grid)
        fig.update_yaxes(showgrid=show_grid)
        st.plotly_chart(fig, use_container_width=True)

with tab_stat:
    st.subheader("Podsumowanie dla wybranych zmiennych numerycznych")
    st.dataframe(df[[val_x, val_y]].describe(), use_container_width=True)
    
    with st.expander("Pokaż macierz korelacji dla wszystkich zmiennych numerycznych"):
        corr = df[num_cols].corr()
        st.dataframe(corr.style.background_gradient(cmap='Greens'))