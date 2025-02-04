import streamlit as st
import pandas as pd
import calendar
import datetime
import os

# Funzione per il Calendario
def show_calendar():
    st.title("Calendario")
    
    # Mostra mese corrente
    today = datetime.date.today()  # Usa datetime.date per ottenere la data odierna
    month = st.selectbox("Seleziona mese", list(calendar.month_name[1:]), index=today.month - 1)
    year = st.selectbox("Seleziona anno", list(range(today.year, today.year + 5)), index=0)
    
    month_number = list(calendar.month_name[1:]).index(month) + 1
    st.write(f"Calendario per {month} {year}")
    
    # Crea la struttura del calendario
    cal = calendar.monthcalendar(year, month_number)
    days_of_week = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
    
    # Organizza i dati in un DataFrame
    calendar_data = []
    for week in cal:
        calendar_data.append([str(day) if day != 0 else "" for day in week])
    
    df = pd.DataFrame(calendar_data, columns=days_of_week)
    
    # Mostra il calendario in una tabella interattiva
    st.dataframe(df)

# Le altre funzioni rimangono invariate

def main():
    st.sidebar.title("Navigazione")
    tab = st.sidebar.radio("Scegli una funzionalità", ("Calendario", "Blocco Note", "To-Do List"))
    
    if tab == "Calendario":
        show_calendar()
    elif tab == "Blocco Note":
        show_notebook()
    elif tab == "To-Do List":
        show_todo_list()

if __name__ == "__main__":
    main()
