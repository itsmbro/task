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



# Funzione per il Blocco Note
def show_notebook():
    st.title("Blocco Note")
    note = st.text_area("Scrivi la tua nota", "", height=200)
    
    # Salva la nota su un file di testo
    if st.button("Salva nota"):
        if note != "":
            # Crea un nome dinamico per il file con data e ora
            file_name = f"nota_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            
            # Salva la nota in un file
            try:
                with open(file_name, "w") as file:
                    file.write(note)
                st.success(f"Nota salvata con successo! Nome file: {file_name}")
            except Exception as e:
                st.error(f"Errore nel salvataggio della nota: {e}")
        else:
            st.warning("Non hai scritto nulla!")

# Funzione per la To-Do List
def show_todo_list():
    st.title("To-Do List")
    
    # Aggiungi una nuova voce alla lista
    task = st.text_input("Aggiungi un'attività", "")
    
    if st.button("Aggiungi alla lista"):
        if task != "":
            if "tasks" not in st.session_state:
                st.session_state["tasks"] = []
            st.session_state["tasks"].append(task)
            st.success("Attività aggiunta con successo!")
        else:
            st.warning("Scrivi un'attività da aggiungere!")
    
    # Visualizza le attività
    if "tasks" in st.session_state:
        st.write("### Attività da fare:")
        for idx, task in enumerate(st.session_state["tasks"], 1):
            task_done = st.checkbox(f"Completata {task}", key=idx)
            if task_done:
                st.session_state["tasks"].remove(task)
                st.success(f"Attività '{task}' completata!")
            else:
                st.write(f"{idx}. {task}")





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
