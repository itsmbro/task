import streamlit as st
import openai
import json
import requests
import base64
import re

# Configurazione delle credenziali dai secrets di Streamlit
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_USER = "itsmbro"  # Sostituisci con il tuo username GitHub
GITHUB_REPO = "task"  # Nome del repository GitHub
GITHUB_BRANCH = "main"  # Nome del branch
TASK_FILE_PATH = "task.py"  # File Python da modificare

# Configurazione API OpenAI
openai.api_key = OPENAI_API_KEY

# Funzione per caricare il file Python da GitHub
def load_task_file():
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{TASK_FILE_PATH}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        st.error("Errore nel caricamento del file da GitHub.")
        return ""

# Funzione per salvare il file Python su GitHub
def save_task_file(updated_code):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{TASK_FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Ottiene il contenuto attuale per recuperare lo SHA del file
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    # Converte il codice aggiornato in base64
    json_base64 = base64.b64encode(updated_code.encode()).decode()

    data = {
        "message": "Aggiornamento task.py",
        "content": json_base64,
        "branch": GITHUB_BRANCH
    }
    
    if sha:
        data["sha"] = sha  # Necessario per modificare un file esistente

    # Effettua la richiesta di aggiornamento
    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        st.success("File aggiornato con successo su GitHub!")
    else:
        st.error(f"Errore aggiornamento GitHub: {response.json()}")

# Funzione per ripulire il codice da Markdown e commenti indesiderati
def clean_code_from_markdown(code):
    """Rimuove i blocchi Markdown e commenti generati da GPT"""
    code = re.sub(r"```python\n(.*?)\n```", r"\1", code, flags=re.DOTALL)  # Rimuove ```python ... ```
    code = re.sub(r"```(.*?)\n```", r"\1", code, flags=re.DOTALL)  # Rimuove ``` ... ```
    code = re.sub(r"(?i)codice corretto e aggiornato", "", code).strip()  # Rimuove commenti generati da GPT
    return code

# Funzione per aggiornare il codice in base alla risposta di ChatGPT
def update_task_file_from_response(response_text, task_code):
    match = re.search(r'00000000\n(.*?)\n00000000', response_text, re.DOTALL)
    if match:
        try:
            new_code = clean_code_from_markdown(match.group(1).strip())
            if new_code.lower() != "nessuna modifica necessaria":
                save_task_file(new_code)
            return new_code
        except Exception as e:
            st.error(f"Errore nell'analisi del codice generato: {e}")
    return task_code

# Genera il prompt iniziale per ChatGPT
def generate_initial_prompt(task_code):
    return (
        "Sei un assistente esperto in sviluppo software. Devi aggiornare il file Python `task.py`.\n"
        "Il file attuale contiene il seguente codice:\n\n"
        "00000000\n"
        f"{task_code}\n"
        "00000000\n\n"
        "Quando ti viene chiesto di modificarlo, restituisci SOLO il codice aggiornato, senza altre spiegazioni.\n"
        "Assicurati che il codice restituito sia completo e funzioni correttamente.\n"
        "Non alterare parti non richieste e non fornire altro testo oltre al codice.\n"
        "Ora iniziamo!"
    )

# Carica il file da GitHub
task_code = load_task_file()
initial_prompt = generate_initial_prompt(task_code)

# Inizializza la sessione della chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": initial_prompt}]

# Mostra la cronologia dei messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente per richieste di modifica
if user_input := st.chat_input("Richiedi una modifica al codice..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Richiesta a ChatGPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.7
        )
        bot_response = response["choices"][0]["message"]["content"]

        # Aggiorna il file se necessario
        updated_code = update_task_file_from_response(bot_response, task_code)

        # Mostra la risposta nella chat
        with st.chat_message("assistant"):
            st.markdown(f"```python\n{updated_code}\n```")

        # Salva il messaggio nella sessione
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        st.error(f"Errore nella comunicazione con OpenAI: {str(e)}")
