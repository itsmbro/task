
import streamlit as st
import openai
import json
import requests
import base64
import re
import random

# Configurazione API
openai.api_key = st.secrets["OPENAI_API_KEY"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

# Configurazione GitHub
GITHUB_USER = "itsmbro"
GITHUB_REPO = "task"
GITHUB_BRANCH = "main"
GITHUB_FILE_PATH = "task.py"

# Funzione per caricare il file task.py da GitHub
def load_task_file():
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{GITHUB_FILE_PATH}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Errore nel caricamento di {GITHUB_FILE_PATH} da GitHub.")
        return ""

# Funzione per aggiornare il file task.py su GitHub
def save_task_file(updated_content):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Otteniamo il valore SHA del file attuale
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    # Encoding in base64
    content_base64 = base64.b64encode(updated_content.encode()).decode()

    data = {
        "message": "Aggiornamento automatico di task.py",
        "content": content_base64,
        "branch": GITHUB_BRANCH
    }
    
    if sha:
        data["sha"] = sha  # Necessario per aggiornare il file esistente

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        st.success("✅ task.py aggiornato con successo su GitHub!")
    else:
        st.error(f"Errore nell'aggiornamento di GitHub: {response.json()}")

# Funzione per generare il prompt iniziale
def generate_initial_prompt(task_code):
    return (
        "Sei uno sviluppatore esperto. Il tuo compito è aggiornare e migliorare uno script Python chiamato task.py.\n"
        "Il codice attuale di task.py è il seguente:\n\n"
        "00000000\n"
        f"{task_code}\n"
        "00000000\n\n"
        "Se vuoi modificare parti del codice, rispondi con il formato esatto:\n\n"
        "00000000\n"
        "<NUOVO CODICE COMPLETO DA SOSTITUIRE>\n"
        "00000000\n\n"
        "Il codice generato deve:\n"
        "1. Mantenere le funzioni necessarie per interagire con ChatGPT.\n"
        "2. Includere eventuali miglioramenti o nuove funzionalità richieste dall'utente.\n"
        "3. Non rimuovere sezioni essenziali per il funzionamento dello script.\n\n"
        "Se il codice attuale è corretto, rispondi solo con 'Nessuna modifica necessaria'.\n\n"
        "come ultima cosa ti notifico che quando tu generi il codice per mostrarlo con un formato diverso utilizzi questa sintassi: '''python <codice aggiornato> '''. In questo modo l'aggiornamento dello script includerà anche gli apici e la scritta Python che però non deve essere inclusa quindi evita di metterla  In questo modo l'aggiornamento dello script includerà anche gli apici e la scritta Python che però non deve essere inclusa quindi evita di metterla. Ora procediamo con le modifiche!"
    )

# Funzione per aggiornare task.py dalle risposte di ChatGPT
def update_task_file_from_response(response_text, task_code):
    match = re.search(r'00000000\n(.*?)\n00000000', response_text, re.DOTALL)
    if match:
        try:
            new_code = match.group(1).strip()
            if new_code.lower() != "nessuna modifica necessaria":
                save_task_file(new_code)
            return new_code
        except Exception as e:
            st.error(f"Errore nell'analisi del codice generato: {e}")
    return task_code

# UI con Streamlit
st.title("🔄 Task.py Updater")

# Carichiamo task.py da GitHub
task_code = load_task_file()

# Mostriamo il codice attuale
st.subheader("📄 Codice attuale di task.py:")
st.code(task_code, language="python")

# Input utente
user_input = st.text_area("✍️ Inserisci la tua richiesta di modifica:", "")

if st.button("🔄 Genera aggiornamento"):
    if user_input:
        # Creiamo la richiesta per ChatGPT
        messages = [
            {"role": "system", "content": generate_initial_prompt(task_code)},
            {"role": "user", "content": user_input}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7
            )
            bot_response = response["choices"][0]["message"]["content"]

            # Aggiorniamo il file se necessario
            updated_code = update_task_file_from_response(bot_response, task_code)

            # Mostriamo il nuovo codice
            st.subheader("🔄 Nuovo codice generato:")
            st.code(updated_code, language="python")

        except Exception as e:
            st.error(f"Errore nella comunicazione con OpenAI: {str(e)}")
    else:
        st.warning("Inserisci una richiesta per aggiornare il codice.")

# Frasi random
random_phrases = ['Ciao, come posso aiutarti oggi?', 'Spero che tu stia passando una bella giornata!', 'Ricorda, ogni giorno è una nuova opportunità.', 'Sei sulla strada giusta, continua così!', 'Non dimenticare di fare una pausa e rilassarti ogni tanto.']

if st.button('Mostra frase random'):
    st.write(random.choice(random_phrases))
