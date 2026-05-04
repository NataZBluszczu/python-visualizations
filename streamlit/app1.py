import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. TYTUŁ APLIKACJI
st.title("Eksplorator Danych - Zadanie 1")

# 2. WCZYTANIE DANYCH (Bezpośrednio z pliku)
# sep=None pozwala Pandasowi samemu odgadnąć, czy masz przecinki czy średniki
df = pd.read_csv("dataset.csv", sep=None, engine='python', encoding='utf-8')

st.divider()

# 3. PODSTAWOWE INFORMACJE O ZBIORZE
st.write("### Informacje o zbiorze danych")
st.write(f"**Liczba wierszy:** {df.shape[0]}")
st.write(f"**Liczba kolumn:** {df.shape[1]}")
st.write("**Dostępne kolumny:**")
st.write(list(df.columns))

st.write("### Podgląd danych")
st.dataframe(df.head())

st.divider()

# 4. WYBÓR KOLUMNY I HISTOGRAM
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
        
        # Tworzenie wykresu
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(
            data=df, 
            x=selected_col, 
            bins=30, 
            kde=True, 
            ax=ax, 
            color='#1DB954', # Zostawiłem zielony ze Spotify, żeby było ładniej!
            edgecolor='black'
        )
        ax.set_title(f"Histogram: {selected_col}", fontsize=14, pad=10)
        ax.set_xlabel(selected_col, fontsize=12)
        ax.set_ylabel("Częstotliwość", fontsize=12)
        
        # Wyświetlenie wykresu w Streamlit
        st.pyplot(fig)