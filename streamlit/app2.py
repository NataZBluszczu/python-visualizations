
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Zadanie 2: Filtrowanie", layout="wide")

st.title("Interaktywny Dashboard Danych")

@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv", sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')

df = load_data()

st.sidebar.header("Ustawienia Filtrów")

cat_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()
num_cols = df.select_dtypes(include=['number']).columns.tolist()

if cat_cols:
    selected_cat_col = st.sidebar.selectbox("1. Wybierz kolumnę kategoryczną:", cat_cols)
    unique_vals = sorted(df[selected_cat_col].dropna().unique().tolist())
    
    default_vals = unique_vals[:3] if len(unique_vals) > 3 else unique_vals
    selected_vals = st.sidebar.multiselect(f"Wybierz wartości dla '{selected_cat_col}':", unique_vals, default=default_vals)
else:
    selected_vals = []
    st.sidebar.warning("Brak kolumn tekstowych/kategorycznych w zbiorze.")

if num_cols:
    selected_num_col = st.sidebar.selectbox("2. Wybierz kolumnę numeryczną:", num_cols)
    min_val = float(df[selected_num_col].min())
    max_val = float(df[selected_num_col].max())
    
    if min_val == max_val:
        range_val = (min_val, max_val)
        st.sidebar.info(f"Wszystkie wartości w '{selected_num_col}' są równe: {min_val}")
    else:
        range_val = st.sidebar.slider(f"Zakres dla '{selected_num_col}':", min_val, max_val, (min_val, max_val))
else:
    range_val = None
    st.sidebar.warning("Brak kolumn numerycznych w zbiorze.")

mask = pd.Series(True, index=df.index)

if cat_cols and selected_vals:
    mask = mask & (df[selected_cat_col].isin(selected_vals))

if num_cols and range_val:
    mask = mask & (df[selected_num_col].between(range_val[0], range_val[1]))

df_filtered = df[mask]

st.write("---")
st.subheader(f"Znaleziono rekordów: **{len(df_filtered):,}**")

if not df_filtered.empty:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.write("### Średnie wartości (Wykres słupkowy)")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.barplot(
            data=df_filtered,
            x=selected_cat_col,
            y=selected_num_col,
            palette="viridis",
            ax=ax,
            errorbar=None 
        )
        plt.xticks(rotation=45, ha='right')
        ax.set_title(f"Średnia '{selected_num_col}' dla każdej wartości z '{selected_cat_col}'", pad=15)
        ax.set_xlabel("")
        ax.set_ylabel(f"Średnia {selected_num_col}")
        
        st.pyplot(fig)
        
    with col2:
        st.write("### Podgląd danych")
        cols_to_show = list(set([selected_cat_col, selected_num_col] + list(df.columns[:3])))
        st.dataframe(df_filtered[cols_to_show], height=400, use_container_width=True)
else:
    st.warning("Brak danych spełniających kryteria filtrów. Zmień ustawienia w panelu bocznym.")