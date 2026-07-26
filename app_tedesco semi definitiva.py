import streamlit as st

# Inizializza lo stato di autenticazione
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Schermata di login se non autenticato
if not st.session_state.authenticated:
    st.title("Accesso Riservato")
    st.write("Inserisci la password per accedere all'applicazione.")
    
    password_input = st.text_input("Password", type="password")
    
    if st.button("Accedi"):
        if password_input == "lala31":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Password errata. Riprova.")
            
    st.stop()  Blocca l'esecuzione del resto dell'app finché non si effettua il login

# --- INIZIO DELL'APPLICAZIONE PRINCIPALE ---
st.title("Der Deutsche Meister")
# Il resto del tuo codice e della logica dell'app continua qui sotto...

"""Der Deutsche Meister — corso enciclopedico A1–B2.

Avvio: streamlit run app.py
"""
from __future__ import annotations

import html
import json
import random
from dataclasses import dataclass

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Der Deutsche Meister | A1–B2",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .stApp { background: #f6f8fc; color: #152033; }
      [data-testid="stSidebar"] { background: #fff; border-right: 1px solid #e3e9f2; }
      .hero { padding: 1.6rem 1.8rem; border-radius: 18px; color: white;
              background: linear-gradient(118deg,#112a46,#146c94 58%,#0b8e75); margin: .2rem 0 1.25rem; }
      .hero h1 { margin: 0; font-size: 2.05rem; }
      .hero p { margin: .35rem 0 0; opacity: .92; }
      .card { background: white; border: 1px solid #e3e9f2; border-radius: 14px; padding: 1.05rem 1.2rem;
              box-shadow: 0 2px 10px rgba(24,44,74,.045); margin: .65rem 0; }
      .chapter { border-left: 5px solid #168aab; }
      .chapter h3 { margin: 0 0 .55rem; color: #12345a; }
      .chapter p { line-height: 1.62; margin: .25rem 0; }
      .level { display:inline-block; color:#fff; font-weight:750; padding:.2rem .7rem; border-radius:99px; margin-bottom:.55rem; }
      .A1{background:#16835b}.A2{background:#2563b8}.B1{background:#b66308}.B2{background:#bd3535}
      .note { background:#edf8ff; border-radius:10px; padding:.75rem 1rem; border:1px solid #cbe8f4; }
      .source { color:#617186; font-size:.9rem; }
      .smallcaps { color:#5c6c80; text-transform:uppercase; letter-spacing:.06em; font-size:.75rem; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Interfaccia localizzata. Il tedesco rimane sempre la lingua-obiettivo.
# ---------------------------------------------------------------------------
LANGUAGES = {"Italiano": "it", "Türkçe": "tr", "English": "en", "Español": "es"}
UI = {
    "it": {
        "tagline": "Percorso formativo di tedesco, cultura e tedesco professionale",
        "language": "Lingua dell'interfaccia", "menu": "Percorso didattico", "theory": "Teoria e laboratorio",
        "test": "Test del corso · 40 domande", "roadmap": "Obiettivi e metodo", "new": "Nuova prova casuale",
        "check": "Correggi le 40 risposte", "choose": "Scegli una risposta", "available": "Parole disponibili",
        "correct": "Corretto", "wrong": "La tua risposta", "solution": "Soluzione corretta", "score": "Punteggio",
        "unanswered": "non risposte", "exam": "Esame integrale · 40 domande", "pronunciation": "Clicca un termine tedesco per ascoltarne la pronuncia",
        "bank": "Banca quesiti", "questions": "quesiti unici", "meaning": "Significato", "forms": "Forme principali",
        "credits": "Allineato ai descrittori QCER; materiale didattico originale, non un esame ufficiale.",
        "author": "Ideato e sviluppato da Roberto Salerno", "word_forms": "Singolare → plurale",
        "subjects": "Enciclopedia disciplinare", "subject_topic": "Tema", "germany_states": "I 16 Bundesländer: lettura geografica",
        "verb_glossary": "Super-glossario · 150 verbi", "verb_intro": "Ogni verbo è una scheda sonora: clicca l'infinito per ascoltarlo, poi confronta presente, Präteritum, Partizip II e ausiliare. Filtra per rendere il ripasso mirato.", "filter": "Filtra per infinito o significato",
        "pace": "Ritmo consigliato", "pace_text": "1. Studia due capitoli e ascolta gli esempi.  \n2. Ripeti a voce alta parole e frasi.  \n3. Completa la prova da 40 quesiti.  \n4. Usa gli errori come lista di ripasso, poi genera una nuova prova.",
        "integrated": "Competenze integrate", "integrated_text": "Ogni livello combina grammatica, lessico, lettura, produzione scritta e comunicazione quotidiana/professionale. Le attività B1–B2 introducono in modo esplicito candidatura, team, istruzioni e argomentazione.",
        "quiz_note": "🧩 La prova alterna scelta e completamenti con banca di parole. Nessuna risposta è preselezionata e l'ordine delle opzioni cambia a ogni nuova prova.",
        "about": "Metodo, fonti e uso", "method_title": "Un libro digitale, non una lista di regole", "method_text": "La sequenza A1–B2 unisce competenze del QCER a scenari di vita, formazione e lavoro. A1–A2 costruiscono scambio quotidiano e routine; B1 allena spiegazione, candidatura e lavoro in team; B2 lavora su registro, fonti, argomentazione e testi specialistici.", "sources": "Riferimenti pedagogici", "pronunciation_how": "Come funziona la pronuncia", "pronunciation_text": "Ogni lemma nei glossari e tutti gli esempi della teoria sono cliccabili: il browser usa la sintesi vocale impostata su de-DE. Se sul dispositivo è disponibile più di una voce tedesca, viene utilizzata quella di sistema.", "source_note": "Nota: il corso è materiale di pratica originale. I riferimenti orientano il livello e le competenze, ma non sostituiscono le informazioni ufficiali di un ente certificatore.",
        "state": "Stato federato", "capital": "Capitale", "region": "Regione", "can_do": "Obiettivo pratico", "test_summary": "40/40 estratti senza ripetizioni", "verb_count": "verbi", "sidebar_summary": "4 corsi × 40 domande · esame integrale × 40", "source_links": "- [Goethe-Institut — livelli A1–C2 e descrittori QCER](https://www.goethe.de/ins/de/it/uun/dln/ger.html)\n- [IHK — formazione linguistica e candidatura professionale](https://events.mnr.ihk.de/b?p=FB426)",
    },
    "en": {
        "tagline": "A structured path through German, culture and professional German",
        "language": "Interface language", "menu": "Learning path", "theory": "Theory and workshop",
        "test": "Course test · 40 questions", "roadmap": "Goals and method", "new": "Create a new random test",
        "check": "Mark all 40 answers", "choose": "Choose an answer", "available": "Word bank",
        "correct": "Correct", "wrong": "Your answer", "solution": "Correct solution", "score": "Score",
        "unanswered": "unanswered", "exam": "Integrated exam · 40 questions", "pronunciation": "Click a German term to hear its pronunciation",
        "bank": "Question bank", "questions": "unique questions", "meaning": "Meaning", "forms": "Principal forms",
        "credits": "Aligned with CEFR descriptors; original learning material, not an official examination.",
        "author": "Conceived and developed by Roberto Salerno", "word_forms": "Singular → plural",
        "subjects": "Subject encyclopedia", "subject_topic": "Topic", "germany_states": "The 16 German federal states: geographical reading",
        "verb_glossary": "Master glossary · 150 verbs", "verb_intro": "Each verb is a sound card: click the infinitive to hear it, then compare present, Präteritum, Partizip II and auxiliary. Filter for focused revision.", "filter": "Filter by infinitive or meaning",
        "pace": "Suggested pace", "pace_text": "1. Study two chapters and listen to the examples.  \n2. Repeat words and sentences aloud.  \n3. Complete the 40-question test.  \n4. Use mistakes as a revision list, then generate a new test.",
        "integrated": "Integrated skills", "integrated_text": "Each level combines grammar, vocabulary, reading, written production and everyday/professional communication. B1–B2 activities explicitly introduce applications, teamwork, instructions and argumentation.",
        "quiz_note": "🧩 The test mixes multiple choice and word-bank completions. No answer is preselected, and option order changes with every new test.",
        "about": "Method, sources and use", "method_title": "A digital book, not a list of rules", "method_text": "The A1–B2 sequence connects CEFR competences to life, study and work scenarios. A1–A2 build everyday exchange and routines; B1 practises explanation, applications and teamwork; B2 develops register, sources, argument and specialist texts.", "sources": "Pedagogical references", "pronunciation_how": "How pronunciation works", "pronunciation_text": "Every glossary entry and every theory example is clickable: the browser uses the de-DE speech voice. If more than one German voice is available, the system voice is used.", "source_note": "Note: this is original practice material. The references orient the level and competences, but do not replace information issued by a certifying body.",
        "state": "Federal state", "capital": "Capital", "region": "Region", "can_do": "Practical goal", "test_summary": "40/40 drawn without repetition", "verb_count": "verbs", "sidebar_summary": "4 courses × 40 questions · integrated exam × 40", "source_links": "- [Goethe-Institut — A1–C2 levels and CEFR descriptors](https://www.goethe.de/ins/de/en/uun/dln/ger.html)\n- [IHK — language training and professional applications](https://events.mnr.ihk.de/b?p=FB426)",
    },
    "es": {
        "tagline": "Itinerario de alemán, cultura y comunicación profesional",
        "language": "Idioma de la interfaz", "menu": "Itinerario didáctico", "theory": "Teoría y taller",
        "test": "Prueba del curso · 40 preguntas", "roadmap": "Objetivos y método", "new": "Generar una prueba aleatoria",
        "check": "Corregir las 40 respuestas", "choose": "Elige una respuesta", "available": "Banco de palabras",
        "correct": "Correcto", "wrong": "Tu respuesta", "solution": "Solución correcta", "score": "Puntuación",
        "unanswered": "sin responder", "exam": "Examen integral · 40 preguntas", "pronunciation": "Haz clic en un término alemán para oír su pronunciación",
        "bank": "Banco de preguntas", "questions": "preguntas únicas", "meaning": "Significado", "forms": "Formas principales",
        "credits": "Alineado con los descriptores del MCER; material original, no es un examen oficial.",
        "author": "Ideado y desarrollado por Roberto Salerno", "word_forms": "Singular → plural",
        "subjects": "Enciclopedia temática", "subject_topic": "Tema", "germany_states": "Los 16 estados federados alemanes: lectura geográfica",
        "verb_glossary": "Superglosario · 150 verbos", "verb_intro": "Cada verbo es una ficha sonora: haz clic en el infinitivo para oírlo y compara presente, Präteritum, Partizip II y auxiliar. Filtra para repasar con precisión.", "filter": "Filtrar por infinitivo o significado",
        "pace": "Ritmo recomendado", "pace_text": "1. Estudia dos capítulos y escucha los ejemplos.  \n2. Repite en voz alta palabras y frases.  \n3. Completa la prueba de 40 preguntas.  \n4. Usa los errores como lista de repaso y genera una prueba nueva.",
        "integrated": "Competencias integradas", "integrated_text": "Cada nivel combina gramática, léxico, lectura, producción escrita y comunicación cotidiana/profesional. Las actividades B1–B2 introducen explícitamente solicitudes, trabajo en equipo, instrucciones y argumentación.",
        "quiz_note": "🧩 La prueba alterna selección y completamientos con banco de palabras. Ninguna respuesta está preseleccionada y el orden de opciones cambia en cada prueba nueva.",
        "about": "Método, fuentes y uso", "method_title": "Un libro digital, no una lista de reglas", "method_text": "La secuencia A1–B2 conecta competencias del MCER con situaciones de vida, formación y trabajo. A1–A2 construyen intercambios cotidianos; B1 practica explicación, solicitudes y equipo; B2 desarrolla registro, fuentes, argumentación y textos especializados.", "sources": "Referencias pedagógicas", "pronunciation_how": "Cómo funciona la pronunciación", "pronunciation_text": "Cada entrada del glosario y cada ejemplo teórico son clicables: el navegador usa la voz de síntesis de de-DE. Si hay varias voces alemanas disponibles, se usa la del sistema.", "source_note": "Nota: el curso es material de práctica original. Las referencias orientan el nivel y las competencias, pero no sustituyen la información oficial de una entidad certificadora.",
        "state": "Estado federado", "capital": "Capital", "region": "Región", "can_do": "Objetivo práctico", "test_summary": "40/40 seleccionadas sin repetición", "verb_count": "verbos", "sidebar_summary": "4 cursos × 40 preguntas · examen integral × 40", "source_links": "- [Goethe-Institut — niveles A1–C2 y descriptores del MCER](https://www.goethe.de/ins/de/es/uun/dln/ger.html)\n- [IHK — formación lingüística y candidatura profesional](https://events.mnr.ihk.de/b?p=FB426)",
    },
    "tr": {
        "tagline": "Almanca, kültür ve meslekî iletişim için yapılandırılmış eğitim yolu",
        "language": "Arayüz dili", "menu": "Öğrenme yolu", "theory": "Kuram ve atölye",
        "test": "Kurs testi · 40 soru", "roadmap": "Hedefler ve yöntem", "new": "Yeni rastgele test oluştur",
        "check": "40 cevabı değerlendir", "choose": "Bir cevap seçin", "available": "Kelime havuzu",
        "correct": "Doğru", "wrong": "Cevabınız", "solution": "Doğru çözüm", "score": "Puan",
        "unanswered": "cevaplanmadı", "exam": "Bütünleşik sınav · 40 soru", "pronunciation": "Telaffuzunu duymak için Almanca terime tıklayın",
        "bank": "Soru bankası", "questions": "benzersiz soru", "meaning": "Anlam", "forms": "Temel biçimler",
        "credits": "CEFR tanımlayıcılarıyla uyumludur; özgün öğrenme materyalidir, resmî sınav değildir.",
        "author": "Roberto Salerno tarafından tasarlanmış ve geliştirilmiştir", "word_forms": "Tekil → çoğul",
        "subjects": "Alan ansiklopedisi", "subject_topic": "Konu", "germany_states": "Almanya'nın 16 eyaleti: coğrafi okuma",
        "verb_glossary": "Ana sözlük · 150 fiil", "verb_intro": "Her fiil sesli bir karttır: duymak için mastara tıklayın; ardından şimdiki zaman, Präteritum, Partizip II ve yardımcı fiili karşılaştırın. Odaklı tekrar için filtreleyin.", "filter": "Mastar veya anlama göre filtrele",
        "pace": "Önerilen tempo", "pace_text": "1. İki bölüm çalışın ve örnekleri dinleyin.  \n2. Kelimeleri ve cümleleri sesli tekrar edin.  \n3. 40 soruluk testi tamamlayın.  \n4. Hataları tekrar listesi olarak kullanın, sonra yeni bir test oluşturun.",
        "integrated": "Bütünleşik beceriler", "integrated_text": "Her seviye dil bilgisi, kelime hazinesi, okuma, yazılı üretim ve günlük/meslekî iletişimi birleştirir. B1–B2 etkinlikleri başvuru, ekip çalışması, talimatlar ve tartışmayı açıkça ele alır.",
        "quiz_note": "🧩 Test, çoktan seçmeli sorularla kelime havuzlu tamamlama sorularını birleştirir. Hiçbir cevap önceden seçilmez ve seçeneklerin sırası her yeni testte değişir.",
        "about": "Yöntem, kaynaklar ve kullanım", "method_title": "Kural listesi değil, dijital bir kitap", "method_text": "A1–B2 dizisi CEFR becerilerini yaşam, eğitim ve iş senaryolarıyla birleştirir. A1–A2 günlük iletişimi kurar; B1 açıklama, başvuru ve ekip çalışmasını; B2 ise üslup, kaynaklar, tartışma ve uzmanlık metinlerini geliştirir.", "sources": "Eğitsel kaynaklar", "pronunciation_how": "Telaffuz nasıl çalışır", "pronunciation_text": "Sözlüklerdeki her madde ve kuram örnekleri tıklanabilir: tarayıcı de-DE konuşma sesini kullanır. Birden çok Almanca ses varsa sistem sesi kullanılır.", "source_note": "Not: Kurs özgün alıştırma materyalidir. Kaynaklar seviyeyi ve becerileri yönlendirir; sertifikalandırma kuruluşunun resmî bilgisinin yerini almaz.",
        "state": "Eyalet", "capital": "Başkent", "region": "Bölge", "can_do": "Pratik hedef", "test_summary": "40/40 soru tekrarsız seçildi", "verb_count": "fiil", "sidebar_summary": "4 kurs × 40 soru · bütünleşik sınav × 40", "source_links": "- [Goethe-Institut — A1–C2 seviyeleri ve CEFR tanımlayıcıları](https://www.goethe.de/ins/de/tr/uun/dln/ger.html)\n- [IHK — dil eğitimi ve meslekî başvuru](https://events.mnr.ihk.de/b?p=FB426)",
    },
}


def tx(key: str) -> str:
    return UI[st.session_state.get("language", "it")][key]


def tr(item: dict, language: str) -> str:
    return item.get(language) or item.get("it") or item.get("en") or "—"


PLURAL_FORMS = {
    # Percorsi A1–B2
    "der Name": "die Namen", "die Sprache": "die Sprachen", "das Land": "die Länder", "die Stadt": "die Städte",
    "die Familie": "die Familien", "der Beruf": "die Berufe", "das Haus": "die Häuser", "die Wohnung": "die Wohnungen",
    "das Zimmer": "die Zimmer", "der Tisch": "die Tische", "der Stuhl": "die Stühle", "das Buch": "die Bücher",
    "der Kaffee": "die Kaffees", "das Brot": "die Brote", "das Wasser": "die Wasser", "der Apfel": "die Äpfel",
    "der Tag": "die Tage", "die Woche": "die Wochen", "der Monat": "die Monate", "das Jahr": "die Jahre",
    "der Termin": "die Termine", "die Reise": "die Reisen", "der Bahnhof": "die Bahnhöfe", "die Fahrkarte": "die Fahrkarten",
    "das Wetter": "—", "die Gesundheit": "—", "der Arzt": "die Ärzte", "die Apotheke": "die Apotheken",
    "die Arbeit": "die Arbeiten", "der Kollege": "die Kollegen", "die Pause": "die Pausen", "die Rechnung": "die Rechnungen",
    "das Geld": "—", "die Bank": "die Banken", "der Markt": "die Märkte", "die Kleidung": "—",
    "der Schlüssel": "die Schlüssel", "die Küche": "die Küchen", "das Werkzeug": "die Werkzeuge", "das Auto": "die Autos",
    "die Erfahrung": "die Erfahrungen", "die Meinung": "die Meinungen", "der Vorschlag": "die Vorschläge", "die Lösung": "die Lösungen",
    "das Problem": "die Probleme", "der Vorteil": "die Vorteile", "der Nachteil": "die Nachteile", "die Entscheidung": "die Entscheidungen",
    "die Ausbildung": "die Ausbildungen", "die Bewerbung": "die Bewerbungen", "der Lebenslauf": "die Lebensläufe", "das Anschreiben": "die Anschreiben",
    "das Vorstellungsgespräch": "die Vorstellungsgespräche", "die Stelle": "die Stellen", "die Abteilung": "die Abteilungen", "die Aufgabe": "die Aufgaben",
    "die Sicherheit": "die Sicherheiten", "die Umwelt": "die Umwelten", "die Veranstaltung": "die Veranstaltungen", "die Nachricht": "die Nachrichten",
    "die Voraussetzung": "die Voraussetzungen", "die Auswirkung": "die Auswirkungen", "die Herausforderung": "die Herausforderungen", "die Entwicklung": "die Entwicklungen",
    "die Maßnahme": "die Maßnahmen", "die Verantwortung": "die Verantwortungen", "die Vereinbarung": "die Vereinbarungen", "die Rückmeldung": "die Rückmeldungen",
    "die Beschwerde": "die Beschwerden", "die Stellungnahme": "die Stellungnahmen", "die Behauptung": "die Behauptungen", "der Zusammenhang": "die Zusammenhänge",
    "der Standpunkt": "die Standpunkte", "der Schwerpunkt": "die Schwerpunkte", "der Nachweis": "die Nachweise", "die Forschung": "die Forschungen",
    "die Ressource": "die Ressourcen", "die Verhandlung": "die Verhandlungen", "die Umsetzung": "die Umsetzungen", "die Genehmigung": "die Genehmigungen",
    # Enciclopedia disciplinare
    "der Motor": "die Motoren", "das Getriebe": "die Getriebe", "die Kupplung": "die Kupplungen", "die Bremse": "die Bremsen",
    "der Reifen": "die Reifen", "die Batterie": "die Batterien", "die Zündkerze": "die Zündkerzen", "der Turbolader": "die Turbolader",
    "der Ölfilter": "die Ölfilter", "der Drehmomentschlüssel": "die Drehmomentschlüssel", "der Messschieber": "die Messschieber", "die Hebebühne": "die Hebebühnen",
    "die Wartung": "die Wartungen", "der Defekt": "die Defekte", "der Prozessor": "die Prozessoren", "der Arbeitsspeicher": "die Arbeitsspeicher",
    "die Festplatte": "die Festplatten", "die Grafikkarte": "die Grafikkarten", "das Mainboard": "die Mainboards", "der Bildschirm": "die Bildschirme",
    "die Tastatur": "die Tastaturen", "die Maus": "die Mäuse", "das Betriebssystem": "die Betriebssysteme", "die Datei": "die Dateien",
    "der Ordner": "die Ordner", "das Netzwerk": "die Netzwerke", "das Passwort": "die Passwörter", "die Sicherung": "die Sicherungen",
    "die Datenschutzregel": "die Datenschutzregeln", "die Hauptstadt": "die Hauptstädte", "das Bundesland": "die Bundesländer", "die Grenze": "die Grenzen",
    "die Bevölkerung": "die Bevölkerungen", "die Fläche": "die Flächen", "die Küste": "die Küsten", "das Gebirge": "die Gebirge",
    "der Fluss": "die Flüsse", "das Klima": "die Klimata", "die Landwirtschaft": "die Landwirtschaften", "die Industrie": "die Industrien",
    "der Handel": "die Handelsbeziehungen", "die Demokratie": "die Demokratien", "die Verfassung": "die Verfassungen", "die Wahl": "die Wahlen",
    "die Migration": "die Migrationen", "die Europäische Union": "—", "die Nachhaltigkeit": "—", "die Zahl": "die Zahlen",
    "die Gleichung": "die Gleichungen", "das Ergebnis": "die Ergebnisse", "die Summe": "die Summen", "die Differenz": "die Differenzen",
    "das Produkt": "die Produkte", "der Quotient": "die Quotienten", "der Bruch": "die Brüche", "der Prozentsatz": "die Prozentsätze",
    "die Maßeinheit": "die Maßeinheiten", "die Länge": "die Längen", "das Gewicht": "die Gewichte", "die Temperatur": "die Temperaturen",
    "die Geschwindigkeit": "die Geschwindigkeiten", "der Kopf": "die Köpfe", "das Auge": "die Augen", "das Ohr": "die Ohren",
    "der Hals": "die Hälse", "die Schulter": "die Schultern", "der Rücken": "die Rücken", "der Arm": "die Arme",
    "die Hand": "die Hände", "der Bauch": "die Bäuche", "das Bein": "die Beine", "der Fuß": "die Füße",
    "der Schmerz": "die Schmerzen", "das Fieber": "—", "die Untersuchung": "die Untersuchungen", "das Rezept": "die Rezepte",
}


def plural_form(item: dict) -> str | None:
    return PLURAL_FORMS.get(item["de"])


def word_with_plural(item: dict) -> str:
    plural = plural_form(item)
    return item["de"] if not plural else f"{item['de']} → {plural}"


def speakable_grid(items: list[dict], language: str, columns: int = 4, detail_key: str = "it") -> None:
    """Una sola griglia HTML: ogni lemma è un vero pulsante SpeechSynthesis."""
    cells = []
    for item in items:
        word = html.escape(word_with_plural(item))
        detail = html.escape(tr(item, language) if detail_key == "translation" else item.get(detail_key, item.get("it", "")))
        plural = plural_form(item)
        speech_word = json.dumps(item["de"] if not plural or plural == "—" else f"{item['de']}. {plural}")
        cells.append(
            f'<button class="term" onclick="say({speech_word}, this)" title="{html.escape(tx("pronunciation"))}">'
            f'<span class="de">{word} <b>🔊</b></span><span class="translation">{detail}</span></button>'
        )
    rows = max(1, (len(items) + columns - 1) // columns)
    component = f"""
    <html><head><meta charset="utf-8"><style>
      *{{box-sizing:border-box}} body{{margin:0;padding:2px;font-family:system-ui,-apple-system,Segoe UI,sans-serif}}
      .grid{{display:grid;grid-template-columns:repeat({columns},minmax(0,1fr));gap:9px}}
      .term{{border:1px solid #dce7f0;border-radius:11px;background:#fff;padding:11px 10px;text-align:left;cursor:pointer;min-height:68px}}
      .term:hover{{border-color:#0d7c9c;background:#effbff;transform:translateY(-1px)}}
      .de{{display:block;font-weight:750;color:#12365d;font-size:14px}} .translation{{display:block;color:#64748b;font-size:12px;margin-top:5px}}
      @media(max-width:620px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
    </style></head><body><div class="grid">{''.join(cells)}</div>
    <script>
      function germanVoice() {{
        return speechSynthesis.getVoices().find(v => v.lang.toLowerCase().startsWith('de')) || null;
      }}
      function say(word, button) {{
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(word);
        u.lang = 'de-DE'; u.rate = .78; u.pitch = 1;
        const voice = germanVoice(); if (voice) u.voice = voice;
        const original = button.innerHTML;
        u.onstart = () => {{ button.style.borderColor = '#0d7c9c'; }};
        u.onend = u.onerror = () => {{ button.style.borderColor = ''; button.innerHTML = original; }};
        button.innerHTML = button.innerHTML.replace('🔊', '🔉');
        window.speechSynthesis.speak(u);
      }}
      window.speechSynthesis.onvoiceschanged = () => germanVoice();
    </script>
    </body></html>"""
    # Il componente mantiene il gesto di clic nel documento che esegue la voce;
    # questo è necessario perché i browser autorizzino la sintesi vocale.
    components.html(component, height=max(100, rows * 81 + 8), scrolling=False)


# ---------------------------------------------------------------------------
# Percorso: spiegazioni nate per ciascuna lingua di app, con esempi tedeschi.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Topic:
    title: str
    it: str
    en: str
    es: str
    tr: str
    examples: tuple[str, ...]


COURSES: dict[str, dict] = {
    "A1": {
        "colour": "A1",
        "title": {"it": "Fondamenta e vita quotidiana", "en": "Foundations and daily life", "es": "Fundamentos y vida cotidiana", "tr": "Temeller ve günlük yaşam"},
        "can": {"it": "Presentarti, capire istruzioni semplici e gestire scambi quotidiani brevi.", "en": "Introduce yourself, understand simple instructions and manage short everyday exchanges.", "es": "Presentarte, entender instrucciones sencillas y resolver intercambios cotidianos breves.", "tr": "Kendini tanıtmak, basit yönergeleri anlamak ve kısa günlük konuşmaları yürütmek."},
        "topics": [
            Topic("1 · La frase principale", "Il verbo coniugato occupa la seconda posizione logica: il primo elemento può essere il soggetto, il tempo o un luogo. Questa regola costruisce la frase tedesca fin dall'inizio.", "The finite verb takes the second logical slot. Time or place may come first; the subject then follows the verb. Build this pattern before adding longer sentences.", "El verbo conjugado va en la segunda posición lógica. Si se adelanta el tiempo o el lugar, el sujeto pasa detrás del verbo.", "Çekimli fiil mantıksal olarak ikinci sıradadır. Zaman veya yer öne alınırsa özne fiilden sonra gelir.", ("Ich lerne heute Deutsch.", "Heute lerne ich Deutsch.")),
            Topic("2 · Persone, sein e haben", "Pronomi personali, saluti e i due verbi più frequenti servono per identità, età, possesso e presentazioni. Impara le forme come blocchi sonori e usale in dialoghi brevi.", "Personal pronouns plus sein and haben let you state identity, age and possession. Practise complete answer turns rather than isolated endings.", "Los pronombres y sein/haben permiten hablar de identidad, edad y posesión. Practica respuestas completas, no solo terminaciones.", "Kişi zamirleri ile sein ve haben; kimlik, yaş ve sahiplik için temel araçlardır. Ekleri tek başına değil, tam cevaplarla çalışın.", ("Ich bin neu hier.", "Wir haben heute Unterricht.")),
            Topic("3 · Articoli e accusativo", "Ogni sostantivo si studia con articolo e plurale. All'accusativo cambia in modo visibile soprattutto il maschile: der → den, ein → einen.", "Learn every noun with gender and plural. In the accusative, masculine articles visibly change: der becomes den and ein becomes einen.", "Aprende cada sustantivo con artículo y plural. En acusativo cambia sobre todo el masculino: der pasa a den.", "Her ismi artikeli ve çoğuluyla öğrenin. Akkusativde özellikle eril artikel değişir: der → den.", ("Der Mann kauft einen Kaffee.", "Ich sehe die Frau.")),
            Topic("4 · Negazione e domande", "kein nega un nome senza articolo determinativo; nicht nega una qualità, un verbo o una parte precisa della frase. Le W‑Fragen chiedono informazione; nelle domande sì/no il verbo apre la frase.", "Use kein for an indefinite or zero-article noun and nicht for a verb, quality or a selected part of a sentence. Yes/no questions start with the verb.", "kein niega un sustantivo sin artículo definido; nicht niega verbo, cualidad o parte concreta. En preguntas sí/no el verbo va primero.", "kein belirsiz ya da artikelsiz ismi, nicht ise fiili veya niteliği olumsuzlar. Evet/hayır sorularında fiil baştadır.", ("Ich habe keine Zeit.", "Kommst du aus Italien?")),
            Topic("5 · Verbi modali e separabili", "Con können, müssen e wollen l'infinito va alla fine. I prefissi separabili si staccano nella principale: una parentesi verbale che tornerà utile a tutti i livelli.", "With modal verbs, the lexical infinitive moves to the end. In a main clause a separable prefix moves to the end too—your first verb bracket.", "Con los modales el infinitivo léxico va al final. En la principal, el prefijo separable también se desplaza al final.", "Modal fiillerle asıl fiilin mastarı sona gider. Ayrılabilen önek de ana cümlede sona gider; bu ilk fiil parantezidir.", ("Ich kann heute kommen.", "Wir kaufen am Samstag ein.")),
            Topic("6 · Tempo, numeri e routine", "L'unità A1 chiude con orari, date, acquisti e routine. Non memorizzare liste isolate: pronuncia a voce alta quantità, appuntamenti e prezzi in mini-scenari.", "Finish A1 with time, dates, shopping and routines. Say quantities, appointments and prices aloud inside mini-scenarios, not as detached lists.", "Termina A1 con horas, fechas, compras y rutinas. Di en voz alta cantidades, citas y precios dentro de miniescenarios.", "A1'i saatler, tarihler, alışveriş ve rutinlerle bitirin. Miktarları, randevuları ve fiyatları küçük senaryolarda sesli söyleyin.", ("Es ist Viertel nach acht.", "Der Termin ist am Montag.")),
        ],
    },
    "A2": {
        "colour": "A2",
        "title": {"it": "Autonomia nelle situazioni note", "en": "Independence in familiar situations", "es": "Autonomía en situaciones conocidas", "tr": "Bilinen durumlarda bağımsızlık"},
        "can": {"it": "Raccontare esperienze, orientarti, descrivere persone e lavorare con situazioni quotidiane.", "en": "Report experiences, find your way, describe people and handle routine situations.", "es": "Contar experiencias, orientarte, describir personas y manejar situaciones cotidianas.", "tr": "Deneyimleri anlatmak, yön bulmak, insanları betimlemek ve rutin durumları yönetmek."},
        "topics": [
            Topic("1 · Perfekt e biografia", "Il Perfekt unisce ausiliare e Partizip II. Costruisci una linea del tempo personale: ieri, la settimana scorsa, un viaggio, un imprevisto.", "The Perfekt combines an auxiliary and a past participle. Use a personal timeline to distinguish events and choose haben or sein.", "El Perfekt combina auxiliar y participio. Usa una línea temporal personal para elegir haben o sein y contar hechos.", "Perfekt, yardımcı fiil ve Partizip II'yi birleştirir. Kişisel zaman çizelgesiyle haben/sein seçimini çalışın.", ("Ich habe lange gearbeitet.", "Wir sind nach Berlin gefahren.")),
            Topic("2 · Dativo e accusativo", "Il caso dipende dalla funzione o dalla preposizione, non dalla traduzione italiana. Prima riconosci: chi riceve? che cosa? Poi scegli articolo e pronome.", "Case follows function or preposition, not a word-for-word translation. Ask who receives something and what is transferred before choosing the article.", "El caso depende de la función o de la preposición, no de una traducción literal. Identifica primero receptor y objeto.", "Hâl, bire bir çeviriye değil işleve veya edata bağlıdır. Önce alıcıyı ve aktarılan şeyi belirleyin.", ("Ich gebe dem Kind den Ball.", "Das Geschenk ist für meinen Bruder.")),
            Topic("3 · Spazio e movimento", "Le Wechselpräpositionen separano Wo? (dativo) e Wohin? (accusativo). Disegna una stanza o un'officina: posiziona, sposta e descrivi oggetti.", "Two-way prepositions distinguish location (Wo? + dative) from direction (Wohin? + accusative). Map a room or workshop and narrate movements.", "Las preposiciones mixtas distinguen ubicación (Wo? + dativo) y dirección (Wohin? + acusativo). Describe y mueve objetos en un plano.", "Çift yönlü edatlar konum (Wo? + dativ) ile yönü (Wohin? + akk.) ayırır. Bir oda planında nesneleri yerleştirin ve taşıyın.", ("Das Werkzeug liegt auf dem Tisch.", "Ich lege das Werkzeug auf den Tisch.")),
            Topic("4 · Confrontare e motivare", "Comparativo, superlativo e connettori semplici permettono di scegliere, consigliare e descrivere vantaggi. Collega sempre il confronto a una ragione concreta.", "Comparatives, superlatives and simple connectors let you choose, recommend and weigh advantages. Attach every comparison to a concrete reason.", "Comparativos, superlativos y conectores sencillos permiten elegir y recomendar. Une cada comparación a una razón concreta.", "Karşılaştırma, üstünlük ve basit bağlaçlarla seçim ve öneri yapabilirsiniz. Her karşılaştırmayı somut bir nedene bağlayın.", ("Das Auto ist schneller als der Bus.", "Heute ist es am kältesten.")),
            Topic("5 · Frasi dipendenti introduttive", "weil, dass e wenn preparano l'ordine con verbo finale. A2 non richiede periodi lunghi: richiede frasi brevi ma ordinate e comprensibili.", "weil, dass and wenn introduce final-verb order. At A2, aim for short, correctly ordered clauses rather than ornate long sentences.", "weil, dass y wenn introducen el verbo al final. En A2 importa hacer subordinadas breves, ordenadas y claras.", "weil, dass ve wenn fiili sona taşır. A2'de uzun cümlelerden önce kısa ve düzenli yan cümleler kurun.", ("Ich bleibe zu Hause, weil ich krank bin.", "Ich weiß, dass er kommt.")),
            Topic("6 · Servizi, lavoro e salute", "Telefonate, appuntamenti, farmacia, lavoro e casa diventano scenari. Il lessico professionale entra sempre insieme alla cortesia: richiesta, chiarimento, conferma.", "Appointments, calls, pharmacy, work and housing become practical scenarios. Professional vocabulary always travels with polite requests, clarification and confirmation.", "Citas, llamadas, farmacia, trabajo y vivienda se convierten en escenarios. El vocabulario profesional va unido a petición, aclaración y confirmación.", "Randevular, telefonlar, eczane, iş ve konut pratik senaryolardır. Meslekî kelime dağarcığı rica, açıklama ve teyitle birlikte öğrenilir.", ("Könnten Sie das bitte wiederholen?", "Ich brauche einen Termin beim Arzt.")),
        ],
    },
    "B1": {
        "colour": "B1",
        "title": {"it": "Argomentare, lavorare, partecipare", "en": "Argue, work and participate", "es": "Argumentar, trabajar, participar", "tr": "Tartışmak, çalışmak, katılmak"},
        "can": {"it": "Spiegare problemi, raccontare esperienze e comunicare con sicurezza in studio e lavoro.", "en": "Explain problems, report experience and communicate confidently at study and work.", "es": "Explicar problemas, relatar experiencias y comunicarte con seguridad en estudios y trabajo.", "tr": "Sorunları açıklamak, deneyim aktarmak ve eğitimle işte güvenle iletişim kurmak."},
        "topics": [
            Topic("1 · Subordinate e coesione", "Le subordinate con weil, obwohl, während, damit e bevor rendono il testo logico. Pianifica la frase: connettore, soggetto, informazioni, verbo finale.", "Subordinate clauses with weil, obwohl, während, damit and bevor make a text logical. Plan connector, subject, information and final verb.", "Las subordinadas con weil, obwohl, während, damit y bevor cohesionan el texto. Planifica conector, sujeto, información y verbo final.", "weil, obwohl, während, damit ve bevor ile yan cümleler metni mantıklı kılar. Bağlaç, özne, bilgi, fiil son düzenini kurun.", ("Obwohl es regnet, fahre ich zur Arbeit.", "Ich lerne, damit ich die Prüfung bestehe.")),
            Topic("2 · Passivo e processi", "Il passivo mette al centro un processo o un risultato: ideale per istruzioni, produzione, amministrazione e descrizioni tecniche. Distingui azione (werden) e stato (sein).", "The passive foregrounds a process or result—useful in instructions, production, administration and technical descriptions. Distinguish werden from sein.", "La pasiva centra proceso o resultado; es útil en instrucciones, producción y textos técnicos. Distingue werden y sein.", "Edilgen yapı süreç ya da sonucu öne çıkarır; talimatlar ve teknik metinler için uygundur. werden ile sein ayrımını kurun.", ("Das Gerät wird repariert.", "Das Gerät ist repariert.")),
            Topic("3 · Relativi e precisione", "Le relative evitano ripetizioni e collegano informazioni. Il genere viene dal nome antecedente; il caso nasce dalla funzione interna della relativa.", "Relative clauses avoid repetition and connect information. Gender comes from the antecedent; case comes from the role inside the clause.", "Las relativas evitan repeticiones. El género viene del antecedente y el caso, de la función dentro de la relativa.", "İlgi cümleleri tekrarları önler. Cinsiyet öncül isimden, hâl ise ilgi cümlesindeki görevden gelir.", ("Das ist die Frau, die mir hilft.", "Der Mann, dem ich schreibe, arbeitet hier.")),
            Topic("4 · Opinione e discussione", "Una risposta B1 efficace contiene tesi, ragione, esempio e possibile limite. Usa denn, deshalb, trotzdem, einerseits e andererseits con moderazione.", "An effective B1 contribution has a claim, reason, example and possible limitation. Use connectors to show the logic rather than decorate the sentence.", "Una intervención B1 incluye tesis, razón, ejemplo y posible límite. Los conectores deben mostrar la lógica.", "Etkili bir B1 katkısı görüş, neden, örnek ve olası sınır içerir. Bağlaçlar süs değil mantık için kullanılır.", ("Meiner Meinung nach ist das sinnvoll.", "Deshalb schlage ich eine andere Lösung vor.")),
            Topic("5 · Bewerbung e lavoro", "Il modulo professionale tratta annuncio, Anschreiben, Lebenslauf, colloquio e comunicazione di squadra. Ogni testo deve essere concreto, verificabile e adatto al destinatario.", "The professional module covers job ads, cover letters, CVs, interviews and team communication. Make each text concrete, verifiable and audience-appropriate.", "El módulo profesional trabaja ofertas, carta, CV, entrevista y equipo. Todo texto debe ser concreto y adecuado al destinatario.", "Meslek modülü ilan, ön yazı, CV, görüşme ve ekip iletişimini kapsar. Her metin somut, doğrulanabilir ve muhataba uygun olmalıdır.", ("Ich bewerbe mich um die Stelle als …", "Im Anhang finden Sie meinen Lebenslauf.")),
            Topic("6 · Strategie d'esame B1", "Allenati con lettura globale, dettagli mirati, e-mail formale e breve presentazione orale. Dopo ogni produzione, revisiona prima il verbo e poi connettori, casi e registro.", "Train global reading, targeted detail, formal email and a short oral presentation. Review verbs first, then connectors, case and register.", "Entrena lectura global, detalles, correo formal y presentación breve. Revisa primero verbos y después conectores, casos y registro.", "Genel okuma, hedefli ayrıntı, resmî e-posta ve kısa sunum çalışın. Önce fiilleri, sonra bağlaçları, hâlleri ve üslubu gözden geçirin.", ("Könnten wir einen Termin vereinbaren?", "Zusammenfassend möchte ich betonen, dass …")),
        ],
    },
    "B2": {
        "colour": "B2",
        "title": {"it": "Precisione, registro e argomentazione", "en": "Precision, register and argument", "es": "Precisión, registro y argumentación", "tr": "Kesinlik, üslup ve sav"},
        "can": {"it": "Sostenere un punto di vista, comprendere testi complessi e scrivere in modo formale e strutturato.", "en": "Support a viewpoint, understand complex texts and write with a formal, structured style.", "es": "Defender un punto de vista, comprender textos complejos y escribir de forma formal y estructurada.", "tr": "Bir görüşü desteklemek, karmaşık metinleri anlamak ve resmî, düzenli yazmak."},
        "topics": [
            Topic("1 · Konjunktiv I e fonti", "Il Konjunktiv I segnala discorso riportato e distanza dalla fonte. Non serve a rendere il testo più difficile: serve a mostrare chi afferma cosa.", "Konjunktiv I marks reported speech and distance from a source. Its job is not complexity; it makes the origin of a claim transparent.", "El Konjunktiv I marca discurso referido y distancia respecto a la fuente. Hace transparente quién afirma qué.", "Konjunktiv I aktarılan konuşmayı ve kaynağa mesafeyi gösterir. Amaç zorluk değil, iddianın kaynağını görünür kılmaktır.", ("Die Firma erklärt, sie habe reagiert.", "Er sagte, er sei zufrieden.")),
            Topic("2 · Konjunktiv II e diplomazia", "Ipotesi, desideri, critiche caute e proposte usano würde, hätte, wäre, könnte e le forme modali. Il registro è parte del significato.", "Hypotheses, wishes, tactful criticism and proposals use würde, hätte, wäre and modal forms. Register is part of meaning.", "Hipótesis, deseos, críticas prudentes y propuestas usan würde, hätte, wäre y modales. El registro forma parte del significado.", "Varsayım, istek, nazik eleştiri ve öneriler würde, hätte, wäre ve modal biçimleri kullanır. Üslup anlamın bir parçasıdır.", ("Ich würde vorschlagen, dass wir …", "An Ihrer Stelle würde ich …")),
            Topic("3 · Argomentazione complessa", "Costruisci una tesi, definisci criteri, presenta prove e anticipa un'obiezione. I connettori doppi e le concessive servono a rendere visibile la struttura del ragionamento.", "Build a thesis, set criteria, present evidence and anticipate an objection. Paired connectors and concessions make the reasoning visible.", "Construye tesis, criterios, pruebas y una objeción prevista. Los conectores dobles y concesivos hacen visible el razonamiento.", "Tez, ölçüt, kanıt ve olası itiraz kurun. Çift bağlaçlar ve ödün cümleleri düşünce yapısını görünür kılar.", ("Zwar ist die Lösung teuer, aber sie ist nachhaltig.", "Nicht nur die Kosten, sondern auch die Qualität zählt.")),
            Topic("4 · Nominalizzazione e stile", "Testi amministrativi e tecnici comprimono azioni in nomi. Impara a espandere una nominalizzazione per capire il testo e a usarla solo quando aumenta la precisione.", "Administrative and technical texts compress actions into nouns. Learn to unpack nominalisations for reading and use them only when they improve precision.", "Los textos técnicos condensan acciones en sustantivos. Aprende a desplegarlos para comprender y úsalos solo si aportan precisión.", "İdarî ve teknik metinler eylemleri isimleştirir. Okurken açmayı, yazarken ise yalnızca kesinlik kattığında kullanmayı öğrenin.", ("Die Durchführung der Prüfung dauert …", "Wir treffen eine Entscheidung.")),
            Topic("5 · Lettura specialistica", "Affronta articoli, istruzioni, grafici e corrispondenza professionale con tre passaggi: tesi globale, segnali linguistici, verifica dei dettagli. Il glossario disciplinare serve a questo scopo.", "Approach articles, instructions, charts and professional correspondence in three passes: overall claim, linguistic signals, then details. The subject glossaries support this work.", "Aborda artículos, instrucciones, gráficos y correspondencia en tres pasos: idea global, señales lingüísticas y detalles. Los glosarios apoyan este trabajo.", "Makale, talimat, grafik ve meslekî yazışmayı üç adımda okuyun: ana fikir, dilsel işaretler, ayrıntılar. Alan sözlükleri bunu destekler.", ("Aus der Grafik geht hervor, dass …", "Im Vergleich zum Vorjahr …")),
            Topic("6 · Produzione B2 e revisione", "Produci una Stellungnahme, una Beschwerde, una sintesi e una presentazione. La revisione segue una griglia: compito, struttura, prove, coesione, accuratezza, tono.", "Produce a Stellungnahme, complaint, summary and presentation. Revise using a grid: task, structure, evidence, cohesion, accuracy and tone.", "Produce una Stellungnahme, reclamación, síntesis y presentación. Revisa: tarea, estructura, pruebas, cohesión, precisión y tono.", "Stellungnahme, şikâyet, özet ve sunum üretin. Görev, yapı, kanıt, bağdaşım, doğruluk ve tonu kontrol edin.", ("Abschließend lässt sich festhalten, dass …", "Ich bitte Sie daher um eine Stellungnahme.")),
        ],
    },
}


TOPIC_TITLES = {
    "it": {
        "A1": ["La frase principale", "Persone, sein e haben", "Articoli e accusativo", "Negazione e domande", "Verbi modali e separabili", "Tempo, numeri e routine"],
        "A2": ["Perfekt e biografia", "Dativo e accusativo", "Spazio e movimento", "Confrontare e motivare", "Frasi dipendenti introduttive", "Servizi, lavoro e salute"],
        "B1": ["Subordinate e coesione", "Passivo e processi", "Relative e precisione", "Opinione e discussione", "Bewerbung e lavoro", "Strategia d'esame B1"],
        "B2": ["Konjunktiv I e fonti", "Konjunktiv II e diplomazia", "Argomentazione complessa", "Nominalizzazione e stile", "Lettura specialistica", "Produzione B2 e revisione"],
    },
    "en": {
        "A1": ["The main clause", "People, sein and haben", "Articles and accusative", "Negation and questions", "Modal and separable verbs", "Time, numbers and routines"],
        "A2": ["Perfect tense and biography", "Dative and accusative", "Space and movement", "Comparing and giving reasons", "Introductory subordinate clauses", "Services, work and health"],
        "B1": ["Subordinate clauses and cohesion", "Passive voice and processes", "Relative clauses and precision", "Opinion and discussion", "Applications and work", "B1 exam strategy"],
        "B2": ["Konjunktiv I and sources", "Konjunktiv II and diplomacy", "Complex argument", "Nominalisation and style", "Specialist reading", "B2 production and revision"],
    },
    "es": {
        "A1": ["La oración principal", "Personas, sein y haben", "Artículos y acusativo", "Negación y preguntas", "Modales y verbos separables", "Tiempo, números y rutinas"],
        "A2": ["Perfekt y biografía", "Dativo y acusativo", "Espacio y movimiento", "Comparar y justificar", "Subordinadas iniciales", "Servicios, trabajo y salud"],
        "B1": ["Subordinadas y cohesión", "Pasiva y procesos", "Relativas y precisión", "Opinión y debate", "Solicitud y trabajo", "Estrategia de examen B1"],
        "B2": ["Konjunktiv I y fuentes", "Konjunktiv II y diplomacia", "Argumentación compleja", "Nominalización y estilo", "Lectura especializada", "Producción y revisión B2"],
    },
    "tr": {
        "A1": ["Ana cümle", "Kişiler, sein ve haben", "Artikeller ve Akkusativ", "Olumsuzluk ve sorular", "Modal ve ayrılabilen fiiller", "Zaman, sayılar ve rutinler"],
        "A2": ["Perfekt ve yaşam öyküsü", "Dativ ve Akkusativ", "Mekân ve hareket", "Karşılaştırma ve gerekçe", "Giriş düzeyi yan cümleler", "Hizmetler, iş ve sağlık"],
        "B1": ["Yan cümleler ve bağdaşım", "Edilgen yapı ve süreçler", "İlgi cümleleri ve kesinlik", "Görüş ve tartışma", "Başvuru ve iş", "B1 sınav stratejisi"],
        "B2": ["Konjunktiv I ve kaynaklar", "Konjunktiv II ve nezaket", "Karmaşık tartışma", "İsimleştirme ve üslup", "Uzmanlık okuması", "B2 üretim ve gözden geçirme"],
    },
}


# ---------------------------------------------------------------------------
# 160 lemmi, con resa specifica per ciascuna lingua dell'interfaccia.
# ---------------------------------------------------------------------------
def parse_terms(raw: str) -> list[dict]:
    terms = []
    for line in raw.strip().splitlines():
        de, it, en, es, turkish = [part.strip() for part in line.split("|")]
        terms.append({"de": de, "it": it, "en": en, "es": es, "tr": turkish})
    return terms


VOCAB_BY_LEVEL = {
    "A1": parse_terms("""
der Name|il nome|name|el nombre|isim
die Sprache|la lingua|language|el idioma|dil
das Land|il paese|country|el país|ülke
die Stadt|la città|city|la ciudad|şehir
die Familie|la famiglia|family|la familia|aile
der Beruf|la professione|profession|la profesión|meslek
das Haus|la casa|house|la casa|ev
die Wohnung|l'appartamento|flat|el piso|daire
das Zimmer|la stanza|room|la habitación|oda
der Tisch|il tavolo|table|la mesa|masa
der Stuhl|la sedia|chair|la silla|sandalye
das Buch|il libro|book|el libro|kitap
der Kaffee|il caffè|coffee|el café|kahve
das Brot|il pane|bread|el pan|ekmek
das Wasser|l'acqua|water|el agua|su
der Apfel|la mela|apple|la manzana|elma
der Tag|il giorno|day|el día|gün
die Woche|la settimana|week|la semana|hafta
der Monat|il mese|month|el mes|ay
das Jahr|l'anno|year|el año|yıl
heute|oggi|today|hoy|bugün
morgen|domani|tomorrow|mañana|yarın
gestern|ieri|yesterday|ayer|dün
früh|presto|early|temprano|erken
spät|tardi|late|tarde|geç
groß|grande|big|grande|büyük
klein|piccolo|small|pequeño|küçük
gut|buono|good|bueno|iyi
teuer|costoso|expensive|caro|pahalı
billig|economico|cheap|barato|ucuz
arbeiten|lavorare|to work|trabajar|çalışmak
wohnen|abitare|to live|vivir|ikamet etmek
lernen|imparare|to learn|aprender|öğrenmek
kaufen|comprare|to buy|comprar|satın almak
brauchen|avere bisogno|to need|necesitar|ihtiyaç duymak
sprechen|parlare|to speak|hablar|konuşmak
verstehen|capire|to understand|entender|anlamak
kommen|venire|to come|venir|gelmek
gehen|andare|to go|ir|gitmek
heißen|chiamarsi|to be called|llamarse|adı olmak
"""),
    "A2": parse_terms("""
der Termin|l'appuntamento|appointment|la cita|randevu
die Reise|il viaggio|journey|el viaje|seyahat
der Bahnhof|la stazione|station|la estación|tren istasyonu
die Fahrkarte|il biglietto|ticket|el billete|bilet
das Wetter|il tempo meteorologico|weather|el tiempo|hava durumu
die Gesundheit|la salute|health|la salud|sağlık
der Arzt|il medico|doctor|el médico|doktor
die Apotheke|la farmacia|pharmacy|la farmacia|eczane
die Arbeit|il lavoro|work|el trabajo|iş
der Kollege|il collega|colleague|el compañero|iş arkadaşı
die Pause|la pausa|break|la pausa|mola
die Rechnung|la fattura|invoice|la factura|fatura
das Geld|il denaro|money|el dinero|para
die Bank|la banca|bank|el banco|banka
der Markt|il mercato|market|el mercado|pazar
die Kleidung|l'abbigliamento|clothes|la ropa|giysi
der Schlüssel|la chiave|key|la llave|anahtar
die Küche|la cucina|kitchen|la cocina|mutfak
das Werkzeug|l'attrezzo|tool|la herramienta|alet
das Auto|l'auto|car|el coche|araba
fahren|guidare / andare|to drive / travel|conducir / viajar|sürmek / gitmek
besuchen|visitare|to visit|visitar|ziyaret etmek
erklären|spiegare|to explain|explicar|açıklamak
helfen|aiutare|to help|ayudar|yardım etmek
treffen|incontrare|to meet|encontrar|buluşmak
anrufen|telefonare|to call|llamar|telefon etmek
einladen|invitare|to invite|invitar|davet etmek
vergessen|dimenticare|to forget|olvidar|unutmak
beginnen|iniziare|to begin|empezar|başlamak
enden|finire|to end|terminar|bitmek
schneller|più veloce|faster|más rápido|daha hızlı
langsamer|più lento|slower|más lento|daha yavaş
am besten|nel modo migliore|best|mejor|en iyi
links|a sinistra|left|a la izquierda|solda
rechts|a destra|right|a la derecha|sağda
geradeaus|dritto|straight ahead|todo recto|dümdüz
oben|sopra|above|arriba|üstte
unten|sotto|below|abajo|altta
zwischen|tra|between|entre|arasında
gegenüber|di fronte|opposite|enfrente|karşısında
"""),
    "B1": parse_terms("""
die Erfahrung|l'esperienza|experience|la experiencia|deneyim
die Meinung|l'opinione|opinion|la opinión|görüş
der Vorschlag|la proposta|proposal|la propuesta|öneri
die Lösung|la soluzione|solution|la solución|çözüm
das Problem|il problema|problem|el problema|sorun
der Vorteil|il vantaggio|advantage|la ventaja|avantaj
der Nachteil|lo svantaggio|disadvantage|la desventaja|dezavantaj
die Entscheidung|la decisione|decision|la decisión|karar
die Ausbildung|la formazione|training|la formación|meslek eğitimi
die Bewerbung|la candidatura|application|la solicitud|başvuru
der Lebenslauf|il curriculum|CV|el currículum|özgeçmiş
das Anschreiben|la lettera di candidatura|cover letter|la carta de presentación|ön yazı
das Vorstellungsgespräch|il colloquio|job interview|la entrevista|iş görüşmesi
die Stelle|il posto di lavoro|position|el puesto|pozisyon
die Abteilung|il reparto|department|el departamento|departman
die Aufgabe|il compito|task|la tarea|görev
die Sicherheit|la sicurezza|safety|la seguridad|güvenlik
die Umwelt|l'ambiente|environment|el medio ambiente|çevre
die Veranstaltung|l'evento|event|el evento|etkinlik
die Nachricht|il messaggio|message|el mensaje|mesaj
begründen|motivare|to justify|justificar|gerekçelendirmek
vergleichen|confrontare|to compare|comparar|karşılaştırmak
beschreiben|descrivere|to describe|describir|betimlemek
berichten|riferire|to report|informar|rapor etmek
diskutieren|discutere|to discuss|debatir|tartışmak
zustimmen|essere d'accordo|to agree|estar de acuerdo|katılmak
ablehnen|rifiutare|to reject|rechazar|reddetmek
vermeiden|evitare|to avoid|evitar|kaçınmak
verbessern|migliorare|to improve|mejorar|iyileştirmek
erreichen|raggiungere|to achieve|alcanzar|ulaşmak
deshalb|perciò|therefore|por eso|bu nedenle
trotzdem|tuttavia|nevertheless|sin embargo|buna rağmen
außerdem|inoltre|moreover|además|ayrıca
einerseits|da una parte|on the one hand|por una parte|bir yandan
andererseits|dall'altra|on the other hand|por otra parte|öte yandan
obwohl|benché|although|aunque|rağmen
damit|affinché|so that|para que|böylece
während|mentre|while|mientras|sırasında
zuerst|prima|first|primero|önce
schließlich|infine|finally|finalmente|sonunda
"""),
    "B2": parse_terms("""
die Voraussetzung|il presupposto|requirement|el requisito|ön koşul
die Auswirkung|la conseguenza|impact|la repercusión|etki
die Herausforderung|la sfida|challenge|el desafío|zorluk
die Entwicklung|lo sviluppo|development|el desarrollo|gelişim
die Maßnahme|la misura|measure|la medida|önlem
die Verantwortung|la responsabilità|responsibility|la responsabilidad|sorumluluk
die Vereinbarung|l'accordo|agreement|el acuerdo|anlaşma
die Rückmeldung|il riscontro|feedback|la respuesta|geri bildirim
die Beschwerde|il reclamo|complaint|la reclamación|şikâyet
die Stellungnahme|il parere motivato|statement|el dictamen|görüş yazısı
die Behauptung|l'affermazione|claim|la afirmación|iddia
der Zusammenhang|il nesso|connection|la relación|bağlantı
der Standpunkt|il punto di vista|viewpoint|el punto de vista|bakış açısı
der Schwerpunkt|il punto focale|focus|el enfoque|odak noktası
der Nachweis|la prova|evidence|la prueba|kanıt
die Forschung|la ricerca|research|la investigación|araştırma
die Ressource|la risorsa|resource|el recurso|kaynak
die Verhandlung|la trattativa|negotiation|la negociación|müzakere
die Umsetzung|l'attuazione|implementation|la aplicación|uygulama
die Genehmigung|l'autorizzazione|approval|la autorización|onay
voraussetzen|presupporre|to require|requerir|gerektirmek
beeinflussen|influenzare|to influence|influir|etkilemek
beurteilen|valutare|to assess|evaluar|değerlendirmek
nachweisen|dimostrare|to demonstrate|demostrar|kanıtlamak
berücksichtigen|tenere conto di|to consider|tener en cuenta|göz önünde bulundurmak
verfügen über|disporre di|to have at one's disposal|disponer de|sahip olmak
in Betracht ziehen|prendere in considerazione|to consider|considerar|değerlendirmek
eine Entscheidung treffen|prendere una decisione|to make a decision|tomar una decisión|karar vermek
zur Verfügung stehen|essere disponibile|to be available|estar disponible|mevcut olmak
infrage stellen|mettere in discussione|to question|cuestionar|sorgulamak
zwar … aber|è vero … ma|admittedly … but|es cierto … pero|gerçi … ama
nicht nur … sondern auch|non solo … ma anche|not only … but also|no solo … sino también|yalnızca … değil, aynı zamanda
sowohl … als auch|sia … sia|both … and|tanto … como|hem … hem de
weder … noch|né … né|neither … nor|ni … ni|ne … ne de
dennoch|ciò nonostante|nonetheless|no obstante|yine de
folglich|di conseguenza|consequently|por consiguiente|sonuç olarak
hingegen|invece|whereas|en cambio|buna karşılık
insofern|in tal senso|insofar|en ese sentido|bu bakımdan
gegebenenfalls|se necessario|if necessary|en caso necesario|gerekirse
abschließend|in conclusione|in conclusion|para concluir|son olarak
"""),
}


# I 15 nuclei grammaticali per livello producono 45 varianti di controllo
# ciascuno: con 80 verifiche lessicali si arriva esattamente a 125 × 4 = 500.
GRAMMAR_FACTS = {
    "A1": [
        ("Wo steht das finite Verb im einfachen Hauptsatz?", "an zweiter Stelle", ["am Satzende", "immer an erster Stelle"]),
        ("Welche Form ist richtig? Ich ___ aus Italien.", "komme", ["kommt", "kommen"]),
        ("Welcher Artikel gehört zu Hund?", "der", ["die", "das"]),
        ("Wie lautet der Akkusativ von der Kaffee?", "den Kaffee", ["dem Kaffee", "der Kaffee"]),
        ("Welche Verneinung passt? Ich habe ___ Auto.", "kein", ["nicht", "nie"]),
        ("Wie beginnt eine Ja/Nein-Frage?", "mit dem Verb", ["mit dem Subjekt", "mit weil"]),
        ("Was ist korrekt? Heute ___ ich Deutsch.", "lerne", ["lernst", "lernen"]),
        ("Welche Pluralform ist richtig? das Kind –", "die Kinder", ["die Kinden", "der Kinder"]),
        ("Welche W-Frage fragt nach einem Ort?", "Wo?", ["Wann?", "Warum?"]),
        ("Was passiert mit einkaufen im Hauptsatz?", "Der Präfix steht am Ende.", ["Der Präfix verschwindet.", "Nichts trennt sich."]),
        ("Welche Anrede ist formell?", "Sie", ["du", "ihr"]),
        ("Welche Uhrzeit ist 08:15?", "Viertel nach acht", ["Viertel vor acht", "halb acht"]),
        ("Welche Form ist korrekt? Ich ___ einen Bruder.", "habe", ["bin", "hat"]),
        ("Wie heißt die höfliche Bitte?", "Können Sie bitte helfen?", ["Sie können bitte helfen.", "Bitte Sie helfen können."]),
        ("Welche Zahl schreibt man zusammen?", "einundzwanzig", ["zwanzigeins", "einsundzwanzig"]),
    ],
    "A2": [
        ("Welches Hilfsverb passt? Ich ___ nach Hause gegangen.", "bin", ["habe", "werde"]),
        ("Welches Hilfsverb passt? Ich ___ Deutsch gelernt.", "habe", ["bin", "werde"]),
        ("Wo? Das Buch liegt ___ Tisch.", "auf dem", ["auf den", "in den"]),
        ("Wohin? Ich lege das Buch ___ Tisch.", "auf den", ["auf dem", "bei dem"]),
        ("Welcher Modalverb drückt Pflicht aus?", "müssen", ["können", "mögen"]),
        ("Welche Perfektform ist richtig? fahren –", "gefahren", ["gefahrt", "gefahrten"]),
        ("Welche Präposition passt? Ich warte ___ den Bus.", "auf", ["mit", "bei"]),
        ("Welcher Satz ist ein Vergleich?", "Berlin ist größer als Bonn.", ["Berlin ist groß Bonn.", "Berlin größer Bonn ist."]),
        ("Welche Form ist der Superlativ von gut?", "am besten", ["am gutesten", "besser"]),
        ("Welcher Artikel steht nach mit?", "Dativ", ["Akkusativ", "Nominativ"]),
        ("Welche Ergänzung passt? Ich helfe ___ Mann.", "dem", ["den", "der"]),
        ("Welche Ergänzung passt? Ich sehe ___ Mann.", "den", ["dem", "des"]),
        ("Wie wird weil verwendet?", "Das Verb steht am Ende.", ["Das Verb steht zuerst.", "Es steht kein Verb."]),
        ("Welche Zeitangabe passt zum Perfekt?", "Gestern habe ich gearbeitet.", ["Gestern arbeite ich gehabt.", "Gestern bin ich gearbeitet."]),
        ("Welche Form ist höflich?", "Könnten Sie mir helfen?", ["Du hilfst mir?", "Sie helfen mich?"]),
    ],
    "B1": [
        ("Wo steht das Verb nach obwohl?", "am Ende der Nebensatz", ["immer auf Position eins", "direkt nach obwohl"]),
        ("Wie bildet man Vorgangspassiv?", "werden + Partizip II", ["sein + Infinitiv", "haben + Partizip II"]),
        ("Wie bildet man Zustandspassiv?", "sein + Partizip II", ["werden + Infinitiv", "haben + Partizip II"]),
        ("Welche Form ist ein Relativpronomen im Dativ?", "dem", ["den", "dessen"]),
        ("Was gehört in eine Bewerbung?", "ein Anschreiben", ["eine Speisekarte", "eine Fahrkarte"]),
        ("Welche Einleitung drückt Meinung aus?", "Meiner Meinung nach …", ["Am Bahnhof nach …", "In der Küche nach …"]),
        ("Welcher Konnektor nennt einen Grund?", "weil", ["obwohl", "während"]),
        ("Welcher Konnektor nennt ein Ziel?", "damit", ["denn", "oder"]),
        ("Welche Form ist richtig? Das Auto ___ repariert.", "wird", ["hat", "ist werden"]),
        ("Was verlangt trotz?", "Dativ", ["Akkusativ", "Genitiv immer"]),
        ("Welche Form passt: Ich interessiere mich ___ Technik.", "für", ["an", "über"]),
        ("Welche Form ist korrekt? Der Mann, ___ ich helfe, …", "dem", ["den", "dessen"]),
        ("Welche Schlussformel ist formell?", "Mit freundlichen Grüßen", ["Bis später, Alter", "Tschüsschen"]),
        ("Was bedeutet Arbeitszeugnis?", "Bewertung eines Arbeitsverhältnisses", ["Fahrkarte zur Arbeit", "Arbeitsplan für morgen"]),
        ("Welche Strategie ist beim Schreiben sinnvoll?", "erst Inhalt, dann sprachliche Revision", ["nur neue Wörter zählen", "nie den Text lesen"]),
    ],
    "B2": [
        ("Wofür wird Konjunktiv I oft genutzt?", "indirekte Rede", ["einfache Vergangenheit", "Pluralbildung"]),
        ("Welche Form drückt eine höfliche Hypothese aus?", "Ich würde vorschlagen …", ["Ich schlage gestern vor.", "Ich werde vorgeschlagen."]),
        ("Welcher Doppelkonnektor bedeutet not only … but also?", "nicht nur … sondern auch", ["weder … noch", "zwar … aber"]),
        ("Was bedeutet eine Entscheidung treffen?", "entscheiden", ["vergleichen", "ankommen"]),
        ("Welche Textsorte verlangt eine begründete Position?", "Stellungnahme", ["Einkaufsliste", "Fahrplan"]),
        ("Welcher Ausdruck leitet eine Folgerung ein?", "folglich", ["hingegen", "zwar"]),
        ("Was kennzeichnet einen guten B2-Absatz?", "These, Beleg und Schluss", ["nur ein Stichwort", "möglichst viele Ausrufezeichen"]),
        ("Welche Form ist Konjunktiv II von haben?", "hätte", ["habe", "hatte"]),
        ("Welche Form ist Konjunktiv I von sein (er)?", "sei", ["wäre", "ist"]),
        ("Was ist eine Nominalisierung?", "eine Handlung als Nomen ausdrücken", ["ein Nomen streichen", "nur Verben benutzen"]),
        ("Welche Präposition passt? abhängen ___", "von", ["für", "durch"]),
        ("Welche Wendung relativiert eine Aussage?", "Es lässt sich feststellen, dass …", ["Ich weiß alles!", "Das ist niemals wichtig."]),
        ("Wozu dient ein Gegenargument?", "die eigene Position differenziert prüfen", ["das Thema wechseln", "den Text kürzen"]),
        ("Welche Form ist korrekt? Er sagte, er ___ krank.", "sei", ["ist", "wäre gewesen immer"]),
        ("Wie funktioniert zwar … aber?", "Konzession und Kontrast", ["zwei gleiche Gründe", "eine Zeitangabe"]),
    ],
}


def question_ui(kind: str, item: dict, language: str) -> str:
    prompts = {
        "it": {"meaning": "Qual è il significato di", "cloze": "Completa la scheda di lessico: il termine tedesco per", "context": "Nel testo di lavoro manca il termine tedesco per"},
        "en": {"meaning": "What does this mean", "cloze": "Complete the vocabulary card: the German term for", "context": "The work text needs the German term for"},
        "es": {"meaning": "¿Cuál es el significado de", "cloze": "Completa la ficha: el término alemán para", "context": "En el texto de trabajo falta el término alemán para"},
        "tr": {"meaning": "Bunun anlamı nedir", "cloze": "Kelime kartını tamamlayın: bunun Almancası", "context": "İş metninde şu anlam için Almanca terim eksik"},
    }[language]
    meaning = tr(item, language)
    if kind == "meaning":
        return f"{prompts['meaning']} **„{item['de']}“**?"
    if kind == "cloze":
        return f"{prompts['cloze']} **„{meaning}“**: ___"
    return f"{prompts['context']} **„{meaning}“**: ___"


def build_question_bank() -> list[dict]:
    bank: list[dict] = []
    for level, terms in VOCAB_BY_LEVEL.items():
        for position, item in enumerate(terms):
            distractors = [x for x in terms if x["de"] != item["de"]]
            chosen = [distractors[(position * 7 + offset * 11) % len(distractors)] for offset in range(3)]
            bank.append({"id": f"{level}-m-{position}", "level": level, "type": "meaning", "item": item,
                         "answer": item, "options": [item, *chosen]})
            bank.append({"id": f"{level}-c-{position}", "level": level, "type": "cloze", "item": item,
                         "answer": item, "options": [item, *chosen]})
        for index, (question, answer, wrong) in enumerate(GRAMMAR_FACTS[level]):
            for variant, label in enumerate(("Regelcheck", "Mini-Szenario", "Prüfungsfrage"), start=1):
                bank.append({"id": f"{level}-g-{index}-{variant}", "level": level, "type": "grammar",
                             "question": f"{label} {variant}: {question}", "answer": answer, "options": [answer, *wrong]})
    return bank


QUESTION_BANK = build_question_bank()
assert len(QUESTION_BANK) == 500, "La banca deve contenere esattamente 500 quesiti"
assert len({q['id'] for q in QUESTION_BANK}) == len(QUESTION_BANK), "Gli ID devono essere unici"


def display_question(q: dict, language: str) -> tuple[str, list[str], str]:
    if q["type"] == "grammar":
        return q["question"], list(q["options"]), q["answer"]
    item = q["item"]
    if q["type"] == "meaning":
        return question_ui("meaning", item, language), [tr(option, language) for option in q["options"]], tr(q["answer"], language)
    kind = "cloze" if q["type"] == "cloze" else "context"
    return question_ui(kind, item, language), [option["de"] for option in q["options"]], q["answer"]["de"]


def make_test_key(scope: str) -> str:
    return f"test_{scope}_questions"


def load_or_refresh_test(scope: str, pool: list[dict], amount: int, refresh: bool = False) -> tuple[list[dict], int]:
    key, token_key = make_test_key(scope), f"test_{scope}_token"
    if refresh or key not in st.session_state:
        st.session_state[key] = random.sample(pool, amount)
        st.session_state[token_key] = st.session_state.get(token_key, 0) + 1
        st.session_state.pop(f"test_{scope}_submitted", None)
    return st.session_state[key], st.session_state[token_key]


def render_test(scope: str, pool: list[dict], language: str, title: str) -> None:
    head1, head2 = st.columns([4, 1])
    with head1:
        st.subheader(title)
        st.caption(f"{tx('bank')}: {len(pool)} {tx('questions')} · {tx('test_summary')}")
    with head2:
        refresh = st.button(f"🔀 {tx('new')}", key=f"refresh_{scope}", use_container_width=True)
    questions, token = load_or_refresh_test(scope, pool, 40, refresh)
    st.info(tx("quiz_note"))
    answers: dict[str, str | None] = {}
    for number, q in enumerate(questions, start=1):
        prompt, choices, correct = display_question(q, language)
        order = list(choices)
        random.Random(f"{token}:{q['id']}").shuffle(order)
        st.markdown(f"**{number}. [{q['level']}] {prompt}**")
        if q["type"] != "meaning":
            st.caption(f"{tx('available')}: " + " · ".join(order))
        choice = st.radio(tx("choose"), order, index=None, key=f"{scope}_{token}_{q['id']}", label_visibility="collapsed")
        answers[q["id"]] = choice
        st.divider()

    if st.button(f"✅ {tx('check')}", key=f"submit_{scope}", type="primary", use_container_width=True):
        st.session_state[f"test_{scope}_submitted"] = True
    if st.session_state.get(f"test_{scope}_submitted"):
        score = 0
        missing = 0
        st.markdown("### " + tx("score"))
        for number, q in enumerate(questions, start=1):
            _, _, correct = display_question(q, language)
            given = answers.get(q["id"])
            if given == correct:
                score += 1
                st.success(f"{number}. {tx('correct')}: **{correct}**")
            else:
                missing += int(given is None)
                shown = given if given is not None else "—"
                st.error(f"{number}. {tx('wrong')}: **{shown}**")
                st.success(f"{number}. {tx('solution')}: **{correct}**")
        st.metric(tx("score"), f"{score} / 40", f"{missing} {tx('unanswered')}")
        if score >= 30:
            st.balloons()


def render_course(level: str, language: str) -> None:
    course = COURSES[level]
    st.markdown(f"<span class='level {course['colour']}'>{level}</span>", unsafe_allow_html=True)
    st.header(course["title"][language])
    st.markdown(f"<div class='note'><b>{tx('can_do')}:</b> {course['can'][language]}</div>", unsafe_allow_html=True)
    tab_theory, tab_test, tab_goals = st.tabs([tx("theory"), tx("test"), tx("roadmap")])
    with tab_theory:
        st.caption("🇩🇪 " + tx("pronunciation"))
        for topic_index, topic in enumerate(course["topics"]):
            heading = f"{topic_index + 1} · {TOPIC_TITLES[language][level][topic_index]}"
            st.markdown(f"<div class='card chapter'><h3>{heading}</h3><p>{getattr(topic, language)}</p></div>", unsafe_allow_html=True)
            examples = [{"de": line, "it": "Esempio da ascoltare", "en": "Listen to the example", "es": "Escucha el ejemplo", "tr": "Örneği dinleyin"} for line in topic.examples]
            speakable_grid(examples, language, columns=2, detail_key="translation")
    with tab_test:
        render_test(level, [q for q in QUESTION_BANK if q["level"] == level], language, f"{level} · {tx('test')}")
    with tab_goals:
        st.markdown("#### " + tx("pace"))
        st.markdown(tx("pace_text"))
        st.markdown("#### " + tx("integrated"))
        st.markdown(tx("integrated_text"))


# ---------------------------------------------------------------------------
# Glossari tematici: non liste nude, ma parole per leggere e descrivere temi.
# ---------------------------------------------------------------------------
SUBJECTS = {
    "🔧 Meccanica e officina": ("Meccanica, sicurezza e processi", "Leggi un componente insieme alla sua funzione: materiale, misura, movimento, controllo e sicurezza. Il lessico serve per spiegare un guasto e seguire una procedura.", parse_terms("""
der Motor|il motore|engine|el motor|motor
das Getriebe|il cambio|gearbox|la caja de cambios|şanzıman
die Kupplung|la frizione|clutch|el embrague|debriyaj
die Bremse|il freno|brake|el freno|fren
der Reifen|il pneumatico|tyre|el neumático|lastik
die Batterie|la batteria|battery|la batería|akü
die Zündkerze|la candela|spark plug|la bujía|buji
der Turbolader|il turbocompressore|turbocharger|el turbocompresor|turboşarj
der Ölfilter|il filtro dell'olio|oil filter|el filtro de aceite|yağ filtresi
der Drehmomentschlüssel|la chiave dinamometrica|torque wrench|la llave dinamométrica|tork anahtarı
der Messschieber|il calibro|vernier caliper|el calibre|kumpas
die Hebebühne|il ponte sollevatore|car lift|el elevador|lift
die Wartung|la manutenzione|maintenance|el mantenimiento|bakım
der Defekt|il guasto|fault|la avería|arıza
prüfen|controllare|to check|comprobar|kontrol etmek
reparieren|riparare|to repair|reparar|onarmak
wechseln|sostituire|to replace|cambiar|değiştirmek
messen|misurare|to measure|medir|ölçmek
""")),
    "💻 Informatica e tecnologia": ("Hardware, rete e uso responsabile", "Organizza il lessico in input, elaborazione, memoria, rete e sicurezza. Per ogni parola, prova a descrivere funzione, collegamento e problema possibile.", parse_terms("""
der Prozessor|il processore|processor|el procesador|işlemci
der Arbeitsspeicher|la RAM|RAM|la memoria RAM|RAM
die Festplatte|il disco rigido|hard drive|el disco duro|sabit disk
die Grafikkarte|la scheda grafica|graphics card|la tarjeta gráfica|ekran kartı
das Mainboard|la scheda madre|motherboard|la placa base|anakart
der Bildschirm|lo schermo|screen|la pantalla|ekran
die Tastatur|la tastiera|keyboard|el teclado|klavye
die Maus|il mouse|mouse|el ratón|fare
das Betriebssystem|il sistema operativo|operating system|el sistema operativo|işletim sistemi
die Datei|il file|file|el archivo|dosya
der Ordner|la cartella|folder|la carpeta|klasör
das Netzwerk|la rete|network|la red|ağ
das Passwort|la password|password|la contraseña|parola
die Sicherung|il backup|backup|la copia de seguridad|yedekleme
verschlüsseln|crittografare|to encrypt|cifrar|şifrelemek
installieren|installare|to install|instalar|yüklemek
aktualisieren|aggiornare|to update|actualizar|güncellemek
die Datenschutzregel|la regola sulla privacy|data protection rule|la norma de privacidad|veri koruma kuralı
""")),
    "🗺️ Geografia e società": ("Spazio, popolazione e Germania federale", "La geografia è linguaggio per confrontare dati e spiegare relazioni: posizione, confine, clima, economia, migrazione e istituzioni. Usa le carte per formulare ipotesi, non solo per memorizzare nomi.", parse_terms("""
die Hauptstadt|la capitale|capital city|la capital|başkent
das Bundesland|lo Stato federato|federal state|el estado federado|eyalet
die Grenze|il confine|border|la frontera|sınır
die Bevölkerung|la popolazione|population|la población|nüfus
die Fläche|la superficie|area|la superficie|yüzölçümü
die Küste|la costa|coast|la costa|kıyı
das Gebirge|la catena montuosa|mountain range|la cordillera|dağ sırası
der Fluss|il fiume|river|el río|nehir
das Klima|il clima|climate|el clima|iklim
die Landwirtschaft|l'agricoltura|agriculture|la agricultura|tarım
die Industrie|l'industria|industry|la industria|sanayi
der Handel|il commercio|trade|el comercio|ticaret
die Demokratie|la democrazia|democracy|la democracia|demokrasi
die Verfassung|la costituzione|constitution|la constitución|anayasa
die Wahl|l'elezione|election|la elección|seçim
die Migration|la migrazione|migration|la migración|göç
die Europäische Union|l'Unione europea|European Union|la Unión Europea|Avrupa Birliği
die Nachhaltigkeit|la sostenibilità|sustainability|la sostenibilidad|sürdürülebilirlik
""")),
    "🧮 Matematica e scienze": ("Numeri, misure e ragionamento", "Nel tedesco tecnico chiarezza e unità di misura sono parte del risultato. Leggi prima il simbolo, poi esprimi l'operazione in una frase completa.", parse_terms("""
die Zahl|il numero|number|el número|sayı
die Gleichung|l'equazione|equation|la ecuación|denklem
das Ergebnis|il risultato|result|el resultado|sonuç
die Summe|la somma|sum|la suma|toplam
die Differenz|la differenza|difference|la diferencia|fark
das Produkt|il prodotto|product|el producto|çarpım
der Quotient|il quoziente|quotient|el cociente|bölüm
der Bruch|la frazione|fraction|la fracción|kesir
der Prozentsatz|la percentuale|percentage|el porcentaje|yüzde
die Maßeinheit|l'unità di misura|unit|la unidad de medida|ölçü birimi
die Länge|la lunghezza|length|la longitud|uzunluk
das Gewicht|il peso|weight|el peso|ağırlık
die Temperatur|la temperatura|temperature|la temperatura|sıcaklık
die Geschwindigkeit|la velocità|speed|la velocidad|hız
plus|più|plus|más|artı
minus|meno|minus|menos|eksi
geteilt durch|diviso per|divided by|dividido por|bölü
gleich|uguale|equal|igual|eşit
""")),
    "🩺 Corpo e salute": ("Corpo, benessere e consulto", "Distingui sintomo, parte del corpo e azione. In un contesto sanitario è utile dire dove fa male, da quando e con quale intensità, senza improvvisare diagnosi.", parse_terms("""
der Kopf|la testa|head|la cabeza|baş
das Auge|l'occhio|eye|el ojo|göz
das Ohr|l'orecchio|ear|la oreja|kulak
der Hals|la gola|throat|la garganta|boğaz
die Schulter|la spalla|shoulder|el hombro|omuz
der Rücken|la schiena|back|la espalda|sırt
der Arm|il braccio|arm|el brazo|kol
die Hand|la mano|hand|la mano|el
der Bauch|la pancia|stomach|el vientre|karın
das Bein|la gamba|leg|la pierna|bacak
der Fuß|il piede|foot|el pie|ayak
der Schmerz|il dolore|pain|el dolor|ağrı
das Fieber|la febbre|fever|la fiebre|ateş
die Untersuchung|la visita medica|examination|la exploración|muayene
das Rezept|la ricetta medica|prescription|la receta|reçete
krank|malato|ill|enfermo|hasta
gesund|sano|healthy|sano|sağlıklı
sich ausruhen|riposarsi|to rest|descansar|dinlenmek
""")),
}


SUBJECT_LABELS = {
    "🔧 Meccanica e officina": {"it": "Meccanica e officina", "en": "Mechanics and workshop", "es": "Mecánica y taller", "tr": "Mekanik ve atölye"},
    "💻 Informatica e tecnologia": {"it": "Informatica e tecnologia", "en": "Computing and technology", "es": "Informática y tecnología", "tr": "Bilişim ve teknoloji"},
    "🗺️ Geografia e società": {"it": "Geografia e società", "en": "Geography and society", "es": "Geografía y sociedad", "tr": "Coğrafya ve toplum"},
    "🧮 Matematica e scienze": {"it": "Matematica e scienze", "en": "Mathematics and science", "es": "Matemáticas y ciencias", "tr": "Matematik ve bilim"},
    "🩺 Corpo e salute": {"it": "Corpo e salute", "en": "Body and health", "es": "Cuerpo y salud", "tr": "Vücut ve sağlık"},
}

SUBJECT_INTROS = {
    "it": "Studia ogni termine con la sua funzione, il suo contesto e la sua pronuncia: così il glossario serve per leggere, spiegare e lavorare, non solo per tradurre.",
    "en": "Study each term with its function, context and pronunciation. This turns the glossary into a tool for reading, explaining and working—not merely translating.",
    "es": "Estudia cada término con su función, contexto y pronunciación. Así el glosario sirve para leer, explicar y trabajar, no solo para traducir.",
    "tr": "Her terimi işlevi, bağlamı ve telaffuzuyla çalışın. Böylece sözlük yalnızca çeviri için değil, okuma, açıklama ve çalışma için de kullanılır.",
}


def render_subjects(language: str) -> None:
    st.header(tx("subjects"))
    choice = st.selectbox(tx("subject_topic"), list(SUBJECTS.keys()), format_func=lambda key: SUBJECT_LABELS[key][language])
    _, _, terms = SUBJECTS[choice]
    st.subheader(SUBJECT_LABELS[choice][language])
    st.markdown(f"<div class='card chapter'><p>{SUBJECT_INTROS[language]}</p></div>", unsafe_allow_html=True)
    st.caption("🇩🇪 " + tx("pronunciation"))
    speakable_grid(terms, language, columns=4, detail_key="translation")
    if choice == "🗺️ Geografia e società":
        st.markdown("#### " + tx("germany_states"))
        st.dataframe(
            [
                ("Baden-Württemberg", "Stuttgart", "Sud-ovest"), ("Bayern", "München", "Sud"), ("Berlin", "Berlin", "Est"),
                ("Brandenburg", "Potsdam", "Est"), ("Bremen", "Bremen", "Nord-ovest"), ("Hamburg", "Hamburg", "Nord"),
                ("Hessen", "Wiesbaden", "Centro"), ("Mecklenburg-Vorpommern", "Schwerin", "Nord-est"),
                ("Niedersachsen", "Hannover", "Nord-ovest"), ("Nordrhein-Westfalen", "Düsseldorf", "Ovest"),
                ("Rheinland-Pfalz", "Mainz", "Ovest"), ("Saarland", "Saarbrücken", "Sud-ovest"),
                ("Sachsen", "Dresden", "Est"), ("Sachsen-Anhalt", "Magdeburg", "Centro-est"),
                ("Schleswig-Holstein", "Kiel", "Nord"), ("Thüringen", "Erfurt", "Centro"),
            ], columns=["Bundesland", tx("capital"), tx("region")], hide_index=True, use_container_width=True,
        )


# ---------------------------------------------------------------------------
# 150 verbi: forme principali e resa nelle quattro lingue dell'interfaccia.
# ---------------------------------------------------------------------------
def parse_verbs(raw: str) -> list[dict]:
    result = []
    for line in raw.strip().splitlines():
        fields = [part.strip() for part in line.split("|")]
        inf, present, preterite, participle, aux, it, en, es, turkish = fields
        result.append({"de": inf, "present": present, "preterite": preterite, "participle": participle, "aux": aux,
                       "it": it, "en": en, "es": es, "tr": turkish})
    return result


VERBS = parse_verbs("""
sein|ist|war|gewesen|sein|essere|to be|ser/estar|olmak
haben|hat|hatte|gehabt|haben|avere|to have|tener|sahip olmak
werden|wird|wurde|geworden|sein|diventare|to become|llegar a ser|olmak
können|kann|konnte|gekonnt|haben|potere|can|poder|ebilmek
müssen|muss|musste|gemusst|haben|dovere|must|tener que|zorunda olmak
dürfen|darf|durfte|gedurft|haben|avere il permesso|may|poder (permiso)|izinli olmak
wollen|will|wollte|gewollt|haben|volere|to want|querer|istemek
sollen|soll|sollte|gesollt|haben|dovere (consiglio)|should|deber|meli olmak
mögen|mag|mochte|gemocht|haben|piacere|to like|gustar|sevmek
gehen|geht|ging|gegangen|sein|andare|to go|ir|gitmek
kommen|kommt|kam|gekommen|sein|venire|to come|venir|gelmek
fahren|fährt|fuhr|gefahren|sein|guidare/andare|to drive/travel|conducir/viajar|sürmek/gitmek
fliegen|fliegt|flog|geflogen|sein|volare|to fly|volar|uçmak
laufen|läuft|lief|gelaufen|sein|correre|to run|correr|koşmak
schwimmen|schwimmt|schwamm|geschwommen|sein|nuotare|to swim|nadar|yüzmek
steigen|steigt|stieg|gestiegen|sein|salire|to climb|subir|çıkmak
fallen|fällt|fiel|gefallen|sein|cadere|to fall|caer|düşmek
bleiben|bleibt|blieb|geblieben|sein|rimanere|to stay|quedarse|kalmak
sehen|sieht|sah|gesehen|haben|vedere|to see|ver|görmek
hören|hört|hörte|gehört|haben|ascoltare|to hear|oír|duymak
sprechen|spricht|sprach|gesprochen|haben|parlare|to speak|hablar|konuşmak
sagen|sagt|sagte|gesagt|haben|dire|to say|decir|söylemek
fragen|fragt|fragte|gefragt|haben|chiedere|to ask|preguntar|sormak
antworten|antwortet|antwortete|geantwortet|haben|rispondere|to answer|responder|cevap vermek
schreiben|schreibt|schrieb|geschrieben|haben|scrivere|to write|escribir|yazmak
lesen|liest|las|gelesen|haben|leggere|to read|leer|okumak
verstehen|versteht|verstand|verstanden|haben|capire|to understand|entender|anlamak
denken|denkt|dachte|gedacht|haben|pensare|to think|pensar|düşünmek
wissen|weiß|wusste|gewusst|haben|sapere|to know|saber|bilmek
kennen|kennt|kannte|gekannt|haben|conoscere|to know|conocer|tanımak
glauben|glaubt|glaubte|geglaubt|haben|credere|to believe|creer|inanmak
finden|findet|fand|gefunden|haben|trovare|to find|encontrar|bulmak
suchen|sucht|suchte|gesucht|haben|cercare|to look for|buscar|aramak
brauchen|braucht|brauchte|gebraucht|haben|avere bisogno|to need|necesitar|ihtiyaç duymak
geben|gibt|gab|gegeben|haben|dare|to give|dar|vermek
nehmen|nimmt|nahm|genommen|haben|prendere|to take|tomar|almak
bringen|bringt|brachte|gebracht|haben|portare|to bring|llevar|getirmek
holen|holt|holte|geholt|haben|andare a prendere|to fetch|recoger|almaya gitmek
schicken|schickt|schickte|geschickt|haben|inviare|to send|enviar|göndermek
zeigen|zeigt|zeigte|gezeigt|haben|mostrare|to show|mostrar|göstermek
kaufen|kauft|kaufte|gekauft|haben|comprare|to buy|comprar|satın almak
verkaufen|verkauft|verkaufte|verkauft|haben|vendere|to sell|vender|satmak
bezahlen|bezahlt|bezahlte|bezahlt|haben|pagare|to pay|pagar|ödemek
kosten|kostet|kostete|gekostet|haben|costare|to cost|costar|mal olmak
arbeiten|arbeitet|arbeitete|gearbeitet|haben|lavorare|to work|trabajar|çalışmak
machen|macht|machte|gemacht|haben|fare|to do/make|hacer|yapmak
tun|tut|tat|getan|haben|fare/agire|to do|hacer|etmek
spielen|spielt|spielte|gespielt|haben|giocare|to play|jugar|oynamak
lernen|lernt|lernte|gelernt|haben|imparare|to learn|aprender|öğrenmek
studieren|studiert|studierte|studiert|haben|studiare|to study|estudiar|okumak
üben|übt|übte|geübt|haben|esercitarsi|to practise|practicar|pratik yapmak
beginnen|beginnt|begann|begonnen|haben|iniziare|to begin|empezar|başlamak
anfangen|fängt an|fing an|angefangen|haben|iniziare|to start|empezar|başlamak
aufhören|hört auf|hörte auf|aufgehört|haben|smettere|to stop|dejar de|bırakmak
öffnen|öffnet|öffnete|geöffnet|haben|aprire|to open|abrir|açmak
schließen|schließt|schloss|geschlossen|haben|chiudere|to close|cerrar|kapatmak
essen|isst|aß|gegessen|haben|mangiare|to eat|comer|yemek
trinken|trinkt|trank|getrunken|haben|bere|to drink|beber|içmek
kochen|kocht|kochte|gekocht|haben|cucinare|to cook|cocinar|pişirmek
schneiden|schneidet|schnitt|geschnitten|haben|tagliare|to cut|cortar|kesmek
waschen|wäscht|wusch|gewaschen|haben|lavare|to wash|lavar|yıkamak
putzen|putzt|putzte|geputzt|haben|pulire|to clean|limpiar|temizlemek
reparieren|repariert|reparierte|repariert|haben|riparare|to repair|reparar|onarmak
bauen|baut|baute|gebaut|haben|costruire|to build|construir|inşa etmek
schlafen|schläft|schlief|geschlafen|haben|dormire|to sleep|dormir|uyumak
aufstehen|steht auf|stand auf|aufgestanden|sein|alzarsi|to get up|levantarse|kalkmak
stehen|steht|stand|gestanden|haben|stare in piedi|to stand|estar de pie|ayakta durmak
sitzen|sitzt|saß|gesessen|haben|essere seduto|to sit|estar sentado|oturmak
liegen|liegt|lag|gelegen|haben|essere sdraiato|to lie|estar tumbado|yatmak
legen|legt|legte|gelegt|haben|posare|to lay|poner|koymak
stellen|stellt|stellte|gestellt|haben|mettere in piedi|to place|colocar|dik koymak
tragen|trägt|trug|getragen|haben|portare/indossare|to carry/wear|llevar|taşımak/giymek
ziehen|zieht|zog|gezogen|haben|tirare|to pull|tirar|çekmek
drücken|drückt|drückte|gedrückt|haben|premere|to press|pulsar|basmak
helfen|hilft|half|geholfen|haben|aiutare|to help|ayudar|yardım etmek
danken|dankt|dankte|gedankt|haben|ringraziare|to thank|agradecer|teşekkür etmek
lieben|liebt|liebte|geliebt|haben|amare|to love|amar|sevmek
lachen|lacht|lachte|gelacht|haben|ridere|to laugh|reír|gülmek
weinen|weint|weinte|geweint|haben|piangere|to cry|llorar|ağlamak
fühlen|fühlt|fühlte|gefühlt|haben|sentire|to feel|sentir|hissetmek
treffen|trifft|traf|getroffen|haben|incontrare|to meet|encontrar|buluşmak
besuchen|besucht|besuchte|besucht|haben|visitare|to visit|visitar|ziyaret etmek
einladen|lädt ein|lud ein|eingeladen|haben|invitare|to invite|invitar|davet etmek
warten|wartet|wartete|gewartet|haben|aspettare|to wait|esperar|beklemek
verlassen|verlässt|verließ|verlassen|haben|lasciare|to leave|dejar|ayrılmak
verlieren|verliert|verlor|verloren|haben|perdere|to lose|perder|kaybetmek
gewinnen|gewinnt|gewann|gewonnen|haben|vincere|to win|ganar|kazanmak
wohnen|wohnt|wohnte|gewohnt|haben|abitare|to live|vivir|ikamet etmek
reisen|reist|reiste|gereist|sein|viaggiare|to travel|viajar|seyahat etmek
ankommen|kommt an|kam an|angekommen|sein|arrivare|to arrive|llegar|varmak
abfahren|fährt ab|fuhr ab|abgefahren|sein|partire|to depart|salir|hareket etmek
planen|plant|plante|geplant|haben|pianificare|to plan|planear|planlamak
entscheiden|entscheidet|entschied|entschieden|haben|decidere|to decide|decidir|karar vermek
wählen|wählt|wählte|gewählt|haben|scegliere|to choose|elegir|seçmek
sparen|spart|sparte|gespart|haben|risparmiare|to save|ahorrar|biriktirmek
verdienen|verdient|verdiente|verdient|haben|guadagnare|to earn|ganar|kazanmak
einkaufen|kauft ein|kaufte ein|eingekauft|haben|fare la spesa|to shop|hacer compras|alışveriş yapmak
anrufen|ruft an|rief an|angerufen|haben|telefonare|to call|llamar|telefon etmek
messen|misst|maß|gemessen|haben|misurare|to measure|medir|ölçmek
prüfen|prüft|prüfte|geprüft|haben|controllare|to check|comprobar|kontrol etmek
wechseln|wechselt|wechselte|gewechselt|haben|sostituire|to change|cambiar|değiştirmek
lösen|löst|löste|gelöst|haben|allentare/risolvere|to solve|resolver|çözmek
erklären|erklärt|erklärte|erklärt|haben|spiegare|to explain|explicar|açıklamak
erzählen|erzählt|erzählte|erzählt|haben|raccontare|to tell|contar|anlatmak
beschreiben|beschreibt|beschrieb|beschrieben|haben|descrivere|to describe|describir|betimlemek
vergleichen|vergleicht|verglich|verglichen|haben|confrontare|to compare|comparar|karşılaştırmak
meinen|meint|meinte|gemeint|haben|ritenere|to mean|opinar|düşünmek
zustimmen|stimmt zu|stimmte zu|zugestimmt|haben|essere d'accordo|to agree|estar de acuerdo|katılmak
ablehnen|lehnt ab|lehnte ab|abgelehnt|haben|rifiutare|to reject|rechazar|reddetmek
empfehlen|empfiehlt|empfahl|empfohlen|haben|consigliare|to recommend|recomendar|tavsiye etmek
erlauben|erlaubt|erlaubte|erlaubt|haben|permettere|to allow|permitir|izin vermek
verbieten|verbietet|verbot|verboten|haben|vietare|to forbid|prohibir|yasaklamak
versuchen|versucht|versuchte|versucht|haben|tentare|to try|intentar|denemek
vermeiden|vermeidet|vermied|vermieden|haben|evitare|to avoid|evitar|kaçınmak
verbessern|verbessert|verbesserte|verbessert|haben|migliorare|to improve|mejorar|iyileştirmek
entwickeln|entwickelt|entwickelte|entwickelt|haben|sviluppare|to develop|desarrollar|geliştirmek
erreichen|erreicht|erreichte|erreicht|haben|raggiungere|to achieve|alcanzar|ulaşmak
erhalten|erhält|erhielt|erhalten|haben|ricevere|to receive|recibir|almak
enthalten|enthält|enthielt|enthalten|haben|contenere|to contain|contener|içermek
teilnehmen|nimmt teil|nahm teil|teilgenommen|haben|partecipare|to take part|participar|katılmak
vorbereiten|bereitet vor|bereitete vor|vorbereitet|haben|preparare|to prepare|preparar|hazırlamak
organisieren|organisiert|organisierte|organisiert|haben|organizzare|to organise|organizar|organize etmek
informieren|informiert|informierte|informiert|haben|informare|to inform|informar|bilgilendirmek
beantragen|beantragt|beantragte|beantragt|haben|richiedere formalmente|to apply for|solicitar|başvurmak
unterschreiben|unterschreibt|unterschrieb|unterschrieben|haben|firmare|to sign|firmar|imzalamak
vereinbaren|vereinbart|vereinbarte|vereinbart|haben|concordare|to arrange|acordar|kararlaştırmak
verhandeln|verhandelt|verhandelte|verhandelt|haben|negoziare|to negotiate|negociar|müzakere etmek
begründen|begründet|begründete|begründet|haben|motivare|to justify|justificar|gerekçelendirmek
behaupten|behauptet|behauptete|behauptet|haben|affermare|to claim|afirmar|iddia etmek
beurteilen|beurteilt|beurteilte|beurteilt|haben|valutare|to assess|evaluar|değerlendirmek
beeinflussen|beeinflusst|beeinflusste|beeinflusst|haben|influenzare|to influence|influir|etkilemek
berücksichtigen|berücksichtigt|berücksichtigte|berücksichtigt|haben|tenere conto|to consider|tener en cuenta|göz önünde bulundurmak
nachweisen|weist nach|wies nach|nachgewiesen|haben|dimostrare|to demonstrate|demostrar|kanıtlamak
voraussetzen|setzt voraus|setzte voraus|vorausgesetzt|haben|presupporre|to require|requerir|gerektirmek
verfügen über|verfügt über|verfügte über|verfügt|haben|disporre di|to have|disponer de|sahip olmak
umsetzen|setzt um|setzte um|umgesetzt|haben|attuare|to implement|aplicar|uygulamak
darstellen|stellt dar|stellte dar|dargestellt|haben|rappresentare|to present|representar|sunmak
feststellen|stellt fest|stellte fest|festgestellt|haben|constatare|to establish|constatar|tespit etmek
hinweisen auf|weist hin auf|wies hin auf|hingewiesen|haben|segnalare|to point out|señalar|işaret etmek
abhängen von|hängt ab von|hing ab von|abgehangen|haben|dipendere da|to depend on|depender de|bağlı olmak
beitragen zu|trägt bei zu|trug bei zu|beigetragen|haben|contribuire a|to contribute|contribuir|katkı sağlamak
drucken|druckt|druckte|gedruckt|haben|stampare|to print|imprimir|yazdırmak
ausfüllen|füllt aus|füllte aus|ausgefüllt|haben|compilare|to fill in|rellenar|doldurmak
einreichen|reicht ein|reichte ein|eingereicht|haben|presentare|to submit|presentar|teslim etmek
kündigen|kündigt|kündigte|gekündigt|haben|disdire/licenziare|to terminate|rescindir|feshetmek
einstellen|stellt ein|stellte ein|eingestellt|haben|assumere/impostare|to hire/set|contratar/ajustar|işe almak/ayarlamak
herstellen|stellt her|stellte her|hergestellt|haben|produrre|to manufacture|fabricar|üretmek
liefern|liefert|lieferte|geliefert|haben|consegnare|to deliver|entregar|teslim etmek
verbrauchen|verbraucht|verbrauchte|verbraucht|haben|consumare|to consume|consumir|tüketmek
schützen|schützt|schützte|geschützt|haben|proteggere|to protect|proteger|korumak
""")

assert len(VERBS) == 150, f"Attesi 150 verbi, trovati {len(VERBS)}"


def render_verbs(language: str) -> None:
    st.header(tx("verb_glossary"))
    st.markdown(f"<div class='card chapter'><p>{tx('verb_intro')}</p></div>", unsafe_allow_html=True)
    query = st.text_input(tx("filter"))
    query = query.casefold().strip()
    shown = [verb for verb in VERBS if not query or query in verb["de"].casefold() or query in tr(verb, language).casefold()]
    st.caption(f"{len(shown)} / {len(VERBS)} {tx('verb_count')}")
    for start in range(0, len(shown), 30):
        chunk = shown[start:start + 30]
        speakable_grid(chunk, language, columns=5, detail_key="translation")
        st.dataframe(
            [{"Infinitiv": v["de"], "Präsens (er/sie/es)": v["present"], "Präteritum": v["preterite"], "Partizip II": v["participle"], "Aux.": v["aux"], tx("meaning"): tr(v, language)} for v in chunk],
            hide_index=True, use_container_width=True,
        )


def render_about() -> None:
    st.header(tx("about"))
    st.markdown(f"<div class='card chapter'><h3>{tx('method_title')}</h3><p>{tx('method_text')}</p></div>", unsafe_allow_html=True)
    st.markdown("#### " + tx("sources"))
    st.markdown(tx("source_links"))
    st.markdown("#### " + tx("pronunciation_how"))
    st.markdown(tx("pronunciation_text"))
    st.markdown(f"<p class='source'>{tx('source_note')}</p>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Applicazione
# ---------------------------------------------------------------------------
top_info, language_column = st.columns([3, 1])
with top_info:
    st.caption("Der Deutsche Meister · Deutsch lernen A1–B2")
with language_column:
    if "interface_language_choice" not in st.session_state:
        st.session_state["interface_language_choice"] = "Italiano"
    interface_language = LANGUAGES[st.session_state["interface_language_choice"]]
    language_label = st.selectbox(
        "🌐 " + UI[interface_language]["language"],
        list(LANGUAGES.keys()),
        key="interface_language_choice",
    )
st.session_state["language"] = LANGUAGES[language_label]
language = st.session_state["language"]

sections = {
    "A1": "🟢 A1 · " + COURSES["A1"]["title"][language],
    "A2": "🔵 A2 · " + COURSES["A2"]["title"][language],
    "B1": "🟠 B1 · " + COURSES["B1"]["title"][language],
    "B2": "🔴 B2 · " + COURSES["B2"]["title"][language],
    "subjects": "📚 " + tx("subjects"),
    "verbs": "🔊 " + tx("verb_glossary"),
    "exam": "🏆 " + tx("exam"),
    "about": "ℹ️ " + tx("about"),
}
st.sidebar.markdown("### " + tx("menu"))
chosen_label = st.sidebar.radio("Sezione", list(sections.values()), label_visibility="collapsed")
section = next(key for key, value in sections.items() if value == chosen_label)
st.sidebar.divider()
st.sidebar.caption(f"{tx('bank')}: **500** {tx('questions')}")
st.sidebar.caption(tx("sidebar_summary"))
st.sidebar.caption("🔊 de-DE SpeechSynthesis")

st.markdown(f"<section class='hero'><h1>🇩🇪 Der Deutsche Meister</h1><p>{tx('tagline')} · A1–B2</p></section>", unsafe_allow_html=True)

if section in COURSES:
    render_course(section, language)
elif section == "subjects":
    render_subjects(language)
elif section == "verbs":
    render_verbs(language)
elif section == "exam":
    render_test("integrated", QUESTION_BANK, language, tx("exam"))
else:
    render_about()

st.divider()
st.caption("Der Deutsche Meister · " + tx("author") + " · " + tx("credits"))
