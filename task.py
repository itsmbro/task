import streamlit as st
import pandas as pd
import calendar
import datetime
import os
import json

# Funzione per salvare la nota nel file JSON
def save_note_to_json(note_content, file_name):
    # Controlla se esiste il file notes.json
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as f:
            notes_data = json.load(f)
    else:
        notes_data = []

    # Aggiungi la nuova nota
    notes_data.append({"file_name": file_name, "note": note_content})

    # Salva tutte le note nel file JSON
    with open("notes.json", "w") as f:
        json.dump(notes_data, f, indent=4)



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



def show_notebook():
    st.title("Blocco Note")
    note = st.text_area("Scrivi la tua nota", "", height=200)
    
    # Salva la nota su un file di testo
    if st.button("Salva nota"):
        if note != "":
            # Crea un nome dinamico per il file con data e ora
            file_name = f"nota_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            
            # Salva la nota in un file di testo
            try:
                with open(file_name, "w") as file:
                    file.write(note)
                st.success(f"Nota salvata con successo! Nome file: {file_name}")
                
                # Salva la nota anche nel file JSON
                save_note_to_json(note, file_name)
                
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

def show_saved_notes():
    st.title("Note Salvate")

    # Leggi le note salvate dal file JSON
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as f:
            notes_data = json.load(f)
        
        if notes_data:
            for idx, note in enumerate(notes_data):
                # Visualizza il nome del file e il contenuto della nota
                st.subheader(f"Nota: {note['file_name']}")
                st.text_area("Contenuto della nota", note['note'], height=150, disabled=True)

                # Pulsante per eliminare la nota
                if st.button(f"Elimina {note['file_name']}", key=idx):
                    # Elimina la nota dal file di testo
                    try:
                        os.remove(note['file_name'])  # Rimuove il file di testo
                        st.success(f"File '{note['file_name']}' eliminato con successo.")
                    except Exception as e:
                        st.error(f"Errore nell'eliminare il file: {e}")
                    
                    # Elimina la nota dal file JSON
                    notes_data = [n for n in notes_data if n['file_name'] != note['file_name']]

                    # Riscrive il file JSON senza la nota eliminata
                    with open("notes.json", "w") as f:
                        json.dump(notes_data, f, indent=4)

                    st.success(f"Nota '{note['file_name']}' eliminata con successo!")

                    # Ricarica le note salvate
                    break
                st.write("---")
        else:
            st.warning("Non ci sono note salvate.")
    else:
        st.warning("Nessuna nota salvata.")





def main():
    st.sidebar.title("Navigazione")
    tab = st.sidebar.radio("Scegli una funzionalità", ("Calendario", "Blocco Note", "To-Do List", "Note Salvate"))
    
    if tab == "Calendario":
        show_calendar()
    elif tab == "Blocco Note":
        show_notebook()
    elif tab == "To-Do List":
        show_todo_list()
    elif tab == "Note Salvate":
        show_saved_notes()


if __name__ == "__main__":
    main()
