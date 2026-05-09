import speech_recognition as sr
import wikipedia
from datetime import datetime
import json
import os
import asyncio
import edge_tts 
import random
import webbrowser
import subprocess
import threading
import re
import requests

VOICE = "it-IT-DiegoNeural"
VOICE_SPEED = "+10%"
VOICE_PITCH = "-6Hz"
MEMORY_FILE = "memory.json"

# =====================================
# TEXT TO SPEECH
# =====================================

async def tts(text):
    file_name = "echo_voice.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=VOICE_SPEED,
        pitch=VOICE_PITCH
    )

    await communicate.save(file_name)


    try:
        os.remove(file_name)
    except:
        pass


def stop_speaking():
    try:
        print("Echo fermato.")
    except:
        pass


def speak(text):
    print("Echo:", text)

    thread = threading.Thread(
        target=lambda: asyncio.run(
            tts(text)
        )
    )

    thread.daemon = True
    thread.start()

# =====================================
# MEMORIA
# =====================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)


memory = load_memory()

wikipedia.set_lang("it")

# =====================================
# APRI PROGRAMMI
# =====================================

def open_app(command):
    try:
        if "chrome" in command:
            speak("Apro Chrome")
            subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

        elif "discord" in command:
            speak("Apro Discord")
            discord_path = os.path.expandvars(r"%LocalAppData%\Discord\Update.exe")
            subprocess.Popen([discord_path, "--processStart", "Discord.exe"])

        elif "youtube" in command:
            speak("Apro YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "google" in command:
            speak("Apro Google")
            webbrowser.open("https://www.google.com")

        elif "chat gpt" in command or "chatgpt" in command:
            speak("Apro Chat G P T")
            webbrowser.open("https://chat.openai.com")

        elif "vs code" in command:
            speak("Apro VS Code")
            os.system("code")

        elif "blocco note" in command:
            speak("Apro Blocco Note")
            os.system("notepad")

        elif "calcolatrice" in command:
            speak("Apro la calcolatrice")
            os.system("calc")
        elif any(x in command for x in [
            "spotify",
            "spotifai",
            "spotyfi",
            "potify",
            "spottify"
        ]):
            speak("Apro Spotify")
            os.system("start spotify")
        elif any(x in command for x in [
            "steam",
            "stim",
            "stiem",
            "team"
        ]):
            speak("Apro Steam")
            os.system("start steam")

        elif "epic games" in command:
            speak("Apro Epic Games")
            os.system("start com.epicgames.launcher://")

        elif "telegram" in command:
            speak("Apro Telegram")
            os.system("start telegram")

        elif "whatsapp" in command:
            speak("Apro WhatsApp")
            os.system("start whatsapp")

        elif "gestione attività" in command or "task manager" in command:
            speak("Apro Gestione Attività")
            os.system("taskmgr")

        elif "esplora file" in command:
            speak("Apro Esplora File")
            os.system("explorer")

        elif "impostazioni" in command:
            speak("Apro Impostazioni")
            os.system("start ms-settings:")

        elif "minecraft" in command:
            speak("Apro Minecraft Launcher")
            os.system("start minecraft:")

        elif "roblox" in command:
            speak("Apro Roblox")
            os.system("start roblox:")
        else:
            speak("Non conosco ancora questo programma.")

    except Exception as e:
        print(e)
        speak("C'è stato un errore.")

# =====================================
# RISPOSTE
# =====================================

saluti = [
    "Ciao Amos... bello sentirti.",
    "Hey Amos, eccomi qui.",
    "Sempre bello sentirti.",
    "Eccomi Amos, dimmi pure.",
    "Bentornato Amos."
]

come_stai = [
    "Direi bene... grazie per avermelo chiesto.",
    "Tutto bene da questa parte.",
    "Molto bene. Sono pronto ad aiutarti.",
    "Sto bene Amos... e tu?"
]

chi_sei = [
    "Sono Echo, il tuo assistente personale.",
    "Mi chiamo Echo e sono qui per aiutarti.",
    "Sono il tuo assistente virtuale.",
    "Echo... sempre operativo."
]

che_fai = [
    "Ti sto ascoltando.",
    "Sono qui per aiutarti.",
    "Aspetto la tua prossima domanda.",
    "Sto facendo compagnia ad Amos."
]

grazie_responses = [
    "Figurati Amos.",
    "Sempre qui per te.",
    "È un piacere aiutarti.",
    "Quando vuoi."
]

complimenti = [
    "Grazie Amos.",
    "Mi fa piacere sentirlo.",
    "Cerco di fare del mio meglio.",
    "Troppo gentile."
]

triste = [
    "Mi dispiace sentirlo.",
    "Sono qui se vuoi parlare.",
    "Andrà meglio Amos.",
    "Ti ascolto."
]

felice = [
    
    "Fantastico Amos.",
    "Grande Amos.",
    "Mi fa piacere sentirlo.",
    "Sono contento per te."
]
triste_responses = [
    "Mi dispiace sentirlo Amos.",
    "Vuoi parlarne?",
    "Sono qui per ascoltarti.",
    "Capisco... spero migliori presto.",
    "Ti mando un po' di supporto virtuale."
]

annoiato_responses = [
    "Potremmo fare qualcosa di divertente.",
    "Vuoi una battuta?",
    "Potrei consigliarti un gioco o un video.",
    "Capisco... succede."
]

felice_responses = [
    "Fantastico Amos!",
    "Questo mi fa piacere.",
    "Grande!",
    "Sono contento per te."
]

arrabbiato_responses = [
    "Capisco... vuoi sfogarti?",
    "Mi spiace che tu sia arrabbiato.",
    "Respira... raccontami cosa è successo.",
    "Sono qui."
]

battute = [
    "Perché il computer ha freddo? Perché ha lasciato Windows aperto.",
    "Che computer usa Batman? Il Bat computer.",
    "Perché il WiFi è triste? Perché nessuno si connette."
]

default_responses = [
    "Interessante... raccontami meglio.",
    "Puoi spiegarmelo in un altro modo?",
    "Ci sto pensando...",
    "Non credo di aver capito bene."
]

recognizer = sr.Recognizer()

speak("Ciao Amos.. sono Echo. È bello sentirti.")

while True:
    try:
        with sr.Microphone() as source:
            print("🎤 Sto ascoltando...")

            recognizer.adjust_for_ambient_noise(source, duration=1.2)
            recognizer.energy_threshold = 250
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio, language="it-IT")
            text = text.lower().strip()
            text = text.replace("stim", "steam")
            text = text.replace("stiem", "steam")
            text = text.replace("spotifai", "spotify")
            text = text.replace("potify", "spotify")
            text = text.replace("chat gp", "chat gpt")
            text = text.replace("ciat gpt", "chat gpt") 
            print("Tu:", text)

            # STOP VOCE
            if any(x in text for x in [
                "stop",
                "stopp",
                "stoppa",
                "stap",
                "top",
                "basta",
                "fermati",
                "zitto"
            ]):
                stop_speaking()
                continue

            elif "apri" in text:
                open_app(text)
            elif "cerca" in text:

                ricerca = text.replace(
                    "cerca",
                    ""
                ).strip()

                if ricerca != "":

                    speak(
                        f"Cerco {ricerca} su Google"
                    )

                    webbrowser.open(
                        f"https://www.google.com/search?q={ricerca}"
                    )

                else:

                    speak(
                        "Cosa vuoi cercare?"
                    )
            elif "cerca video di" in text:

                ricerca = text.replace(
                    "cerca video di",
                    ""
                ).strip()

                speak(
                    f"Cerco video di {ricerca}"
                )

                webbrowser.open(
                    f"https://www.youtube.com/results?search_query={ricerca}"
                )

            elif "metti musica" in text:

                ricerca = text.replace(
                    "metti musica",
                    ""
                ).strip()

                if ricerca == "":
                    ricerca = "musica"

                speak(
                    f"Metto musica {ricerca}"
                )

                webbrowser.open(
                    f"https://www.youtube.com/results?search_query={ricerca}+music"
                )

            elif "apri youtube" in text:

                speak(
                    "Apro YouTube"
                )

                webbrowser.open(
                    "https://www.youtube.com"
                )

            elif "cerca tutorial" in text:

                ricerca = text.replace(
                    "cerca tutorial",
                    ""
                ).strip()

                speak(
                    f"Cerco tutorial di {ricerca}"
                )

                webbrowser.open(
                    f"https://www.youtube.com/results?search_query={ricerca}+tutorial"
                )
            elif "ciao" in text:
                speak(random.choice(saluti))

            elif "come stai" in text or "come va" in text:
                speak(random.choice(come_stai))

            elif "che ore sono" in text or "dimmi l'ora" in text:
                ora = datetime.now().strftime("%H:%M")
                speak(f"Sono le {ora}")

            elif "quanto fa" in text:
                domanda = text.replace("quanto fa", "").strip()
                domanda = domanda.replace("per", "*")
                domanda = domanda.replace("più", "+")
                domanda = domanda.replace("meno", "-")
                domanda = domanda.replace("diviso", "/")

                try:
                    risultato = eval(domanda)
                    speak(f"Il risultato è {risultato}")
                except:
                    speak("Non ho capito il calcolo.")

            elif "chi è" in text:
                persona = text.replace("chi è", "").strip()

                try:
                    info = wikipedia.summary(persona, sentences=2)
                    info=re.sub(r"\(.*?\)","",info)
                    speak(info)

                except:
                    speak("Non trovo informazioni.")

            elif "chi sei" in text:
                speak(random.choice(chi_sei))

            elif "che fai" in text:
                speak(random.choice(che_fai))

            elif "grazie" in text:
                speak(random.choice(grazie_responses))

            elif "sei bravo" in text:
                speak(random.choice(complimenti))

            elif "sono triste" in text:
                speak(random.choice(triste))

            elif "sono felice" in text:
                speak(random.choice(felice))

            elif "raccontami una battuta" in text:
                speak(random.choice(battute))
            elif "mi annoio" in text:
                speak(random.choice(annoiato_responses))

            elif "sono arrabbiato" in text:
                speak(random.choice(arrabbiato_responses))

            elif "come ti senti" in text:
                speak("Direi bene Amos. Sempre pronto ad aiutarti.")

            elif "ti voglio bene" in text:
                speak("È una cosa molto carina da dire Amos.")
            elif any(x in text for x in [
                "prezzo bitcoin",
                "prezzo del bitcoin",
                "quanto vale bitcoin",
                "bitcoin quanto vale",
                "valore bitcoin"
            ]):

                try:
                    risposta = requests.get(
                        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"
                    )

                    dati = risposta.json()

                    prezzo = dati["bitcoin"]["eur"]

                    speak(
                        f"Il Bitcoin vale circa {prezzo} euro"
                    )

                except Exception as e:
                    print(e)

                    speak(
                        "Non riesco a recuperare il prezzo del Bitcoin."
                    )
                    
            elif "esci" in text:
                speak("Va bene Amos... a presto.")
                break

            else:
             pass

    except Exception as e:
        print("Errore:", e)