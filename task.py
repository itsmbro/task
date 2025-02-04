import streamlit as st
import calendar
import datetime

# Funzione per il Calendario
def show_calendar():
    st.title("Calendario")
    
    # Mostra mese corrente
    today = datetime.date.today()
    month = st.selectbox("Seleziona mese", list(calendar.month_name[1:]), index=today.month - 1)
    year = st.selectbox("Seleziona anno", list(range(today.year, today.year + 5)), index=0)
    
    month_number = list(calendar.month_name[1:]).index(month) + 1
    
    st.write(f"Calendario per {month} {year}")
    
    # Mostra calendario mensile
    cal = calendar.monthcalendar(year, month_number)
    for week in cal:
        st.write(" | ".join([str(day).rjust(2) if day != 0 else " " for day in week]))

# Funzione per il Blocco Note
def show_notebook():
    st.title("Blocco Note")
    note = st.text_area("Scrivi la tua nota", "", height=200)
    
    # Salva la nota su un file di testo
    if st.button("Salva nota"):
        if note != "":
            with open("blocco_note.txt", "w") as file:
                file.write(note)
            st.success("Nota salvata con successo!")
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

# Creazione del layout con più tab
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
