import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Eksplorator Danych - Zadanie 1")

df = pd.read_csv("dataset.csv", sep=None, engine='python', encoding='utf-8')

st.divider()


st.write("### Informacje o zbiorze danych")
st.write(f"**Liczba wierszy:** {df.shape[0]}")
st.write(f"**Liczba kolumn:** {df.shape[1]}")
st.write("**Dostępne kolumny:**")
st.write(list(df.columns))

st.write("### Podgląd danych")
st.dataframe(df.head())

st.divider()

numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

if not numeric_cols:
    st.warning("W zbiorze nie znaleziono kolumn numerycznych do wizualizacji.")
else:
    selected_col = st.selectbox(
        "Wybierz kolumnę numeryczną do wizualizacji rozkładu:",
        numeric_cols
    )

    if selected_col:
        st.write(f"### Rozkład zmiennej: **{selected_col}**")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(
            data=df, 
            x=selected_col, 
            bins=30, 
            kde=True, 
            ax=ax, 
            color='#1DB954', 
            edgecolor='black'
        )
        ax.set_title(f"Histogram: {selected_col}", fontsize=14, pad=10)
        ax.set_xlabel(selected_col, fontsize=12)
        ax.set_ylabel("Częstotliwość", fontsize=12)
        
        st.pyplot(fig)