"""Der Deutsche Meister — corso enciclopedico A1–B2.

Avvio: streamlit run app.py
"""
from __future__ import annotations

import html
import json
import os
import random
from dataclasses import dataclass

import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta
from pathlib import Path
from typing import Any
import re

# Il corso è autosufficiente: non richiede moduli Python locali aggiuntivi.
# Questa scelta evita errori ModuleNotFoundError nelle pubblicazioni Streamlit
# dove viene caricato soltanto il file principale.

Unit = dict[str, Any]


UNITS: dict[str, tuple[Unit, ...]] = {
    "A1": (
        {
            "title": "Costruire la frase: il principio V2",
            "outcome": "Formulare e capire affermazioni brevi cambiando il focus senza perdere l'ordine tedesco.",
            "sections": (
                ("Mappa", "In una frase principale il primo campo (**Vorfeld**) contiene un solo blocco di informazione; segue il verbo finito, poi il resto: `Heute | lerne | ich Deutsch.` Il blocco iniziale puÃ² essere soggetto, tempo, luogo o oggetto. Non Ã¨ una regola della *seconda parola*: `Am Wochenende` Ã¨ un unico blocco."),
                ("Procedura", "1. Scegli che cosa vuoi mettere in evidenza. 2. Mettilo nel Vorfeld. 3. Coniuga il verbo e mettilo subito dopo. 4. Aggiungi soggetto e complementi. Confronta: `Ich arbeite heute zu Hause.` / `Heute arbeite ich zu Hause.` / `Zu Hause arbeite ich heute.`"),
                ("Contrasto utile", "La domanda sÃ¬/no non ha un Vorfeld: il verbo apre la frase, `Arbeitest du heute?` Le domande con parola interrogativa invece mantengono il modello: `Wann arbeitest du heute?` Non dire *Heute ich arbeite*: il soggetto non puÃ² rimanere davanti al verbo quando il tempo occupa il Vorfeld."),
                ("Allenamento", "Trasforma `Ich fahre um acht Uhr zur Arbeit.` mettendo prima `Um acht Uhr`, poi `Zur Arbeit`. Infine rispondi in una frase completa a `Wo wohnst du?`. Prima di parlare, indica a voce: Vorfeld â€“ verbo â€“ resto."),
                ("Autocontrollo", "In `Morgen besucht meine Schwester ihre Freundin` il verbo Ã¨ `besucht`; `Morgen` Ã¨ tutto il primo campo. Se riesci a individuare questi due elementi in ogni frase, stai applicando la regola."),
            ),
        },
        {
            "title": "IdentitÃ , persone e verbi ad alta frequenza",
            "outcome": "Presentarsi, parlare di persone e possesso usando con sicurezza pronomi, sein, haben e verbi regolari.",
            "sections": (
                ("Mappa", "Impara il nome insieme al pronome e alla forma verbale: `ich bin`, `du bist`, `er/sie/es ist`, `wir sind`, `ihr seid`, `sie/Sie sind`; `ich habe`, `du hast` ecc. La maiuscola in `Sie` segnala la forma di cortesia; il verbo Ã¨ plurale: `Kommen Sie aus Italien?`"),
                ("Forma e uso", "Per i verbi regolari togli `-en` e aggiungi `-e, -st, -t, -en, -t, -en`: `ich arbeite, du arbeitest, er arbeitet ...` Dopo radici in `-t/-d` compare spesso una `-e-` di appoggio: `du arbeitest`. L'etÃ  si esprime con `sein`: `Ich bin 30 Jahre alt`, non con *haben*."),
                ("Blocchi pronti", "Memorizza frasi che puoi adattare: `Ich heiÃŸe â€¦ und komme aus â€¦`; `Ich wohne in â€¦`; `Ich bin von Beruf â€¦`; `Ich habe zwei Geschwister.` In una conversazione, chiedi una sola informazione per volta e reagisci: `Ah, interessant!` / `Ich auch.`"),
                ("Allenamento", "Scrivi una carta d'identitÃ  di cinque frasi e poi cambiala dal punto di vista di una terza persona: `Das ist Elena. Sie ist â€¦` Alterna `er`, `sie` ed `es`, perchÃ© *sie* puÃ² voler dire lei o loro: il verbo risolve l'ambiguitÃ  (`sie ist` / `sie sind`)."),
                ("Autocontrollo", "Completa senza guardare: `Wir ___ aus Rom, aber wir ___ in Berlin.` Soluzione: `sind / wohnen`. Se puoi dire le forme di *sein* senza tradurre, hai una base solida per tutti i tempi successivi."),
            ),
        },
        {
            "title": "Nomi, articoli e accusativo",
            "outcome": "Riconoscere soggetto e oggetto diretto e scegliere correttamente gli articoli piÃ¹ frequenti.",
            "sections": (
                ("Mappa", "Ogni nome entra nel quaderno con tre dati: `der Tisch â€“ die Tische â€“ il tavolo`; `die Lampe â€“ die Lampen`; `das Buch â€“ die BÃ¼cher`. Il genere Ã¨ lessicale: non indovinarlo dalla traduzione. Tutti i nomi comuni iniziano con la maiuscola."),
                ("Schema", "Al nominativo: `der/die/das/die`. All'accusativo cambia in modo evidente il maschile: `den/die/das/die`; con l'indeterminativo `einen/eine/ein/â€“`. Quindi: `Der Mann kauft einen Kaffee.` Il soggetto Ã¨ `der Mann`; ciÃ² che compra Ã¨ `einen Kaffee`."),
                ("Quando serve", "Cerca l'accusativo dopo verbi come `haben, brauchen, sehen, kaufen, finden, mÃ¶gen` e dopo preposizioni come `fÃ¼r, ohne, durch, gegen, um`. Non affidarti soltanto all'ordine: `Den Kaffee kauft der Mann` mantiene lo stesso significato perchÃ© `den` segnala l'oggetto."),
                ("Allenamento", "Etichetta in `Ich suche den Bahnhof` chi agisce e che cosa Ã¨ cercato. Poi crea quattro frasi, una per ogni genere, con `Ich habe â€¦` e sostituisci l'articolo definito con quello indeterminativo quando Ã¨ possibile."),
                ("Autocontrollo", "Dopo `Ich sehe â€¦`, scegli `den neuen Film`, `die neue Stadt`, `das neue Museum`, `die neuen HÃ¤user`. Nota: il cambiamento piÃ¹ visibile Ã¨ nel maschile; non aggiungere `-n` al nome singolare."),
            ),
        },
        {
            "title": "Chiedere, negare e ottenere informazioni",
            "outcome": "Gestire piccoli scambi: fare domande chiare, rispondere e negare correttamente.",
            "sections": (
                ("Mappa", "Le W-Fragen richiedono un'informazione: `Wer? Was? Wo? Wohin? Woher? Wann? Wie? Warum?` La formula Ã¨ `W-Wort + verbo + soggetto + resto`: `Wo wohnst du?` Le domande sÃ¬/no iniziano invece con il verbo: `Wohnst du in KÃ¶ln?`"),
                ("Kein o nicht?", "Usa `kein` per negare un nome senza articolo determinativo: `Ich habe kein Auto`, `Wir kaufen keine Milch`. `kein` si comporta come `ein` e si declina: `keinen Kaffee`. Usa `nicht` per verbo, aggettivo, avverbio o un dettaglio: `Ich komme nicht.` / `Das ist nicht teuer.` / `Ich wohne nicht in Bonn.`"),
                ("Risposte naturali", "Una risposta completa riprende il verbo: `Kommst du morgen? â€“ Ja, ich komme morgen.` Per correggere una supposizione, contrasta il dettaglio: `Nein, nicht morgen, sondern am Freitag.` Le particelle `ja, nein, doch` sono importanti: `doch` contraddice una frase negativa, `Du sprichst nicht Deutsch. â€“ Doch!`"),
                ("Allenamento", "Trasforma `Du hast Zeit` in domanda sÃ¬/no, poi crea tre W-Fragen con informazioni diverse. Negare: `Ich habe Zeit` â†’ `Ich habe keine Zeit`; `Ich lerne heute` â†’ `Ich lerne heute nicht.` Spiega a voce perchÃ© la parola negativa cambia."),
                ("Autocontrollo", "La frase *Ich habe nicht Geld* Ã¨ errata: per il nome non determinato serve `kein Geld`. In `Ich kaufe keinen Computer` l'accusativo maschile Ã¨ segnalato da `keinen`."),
            ),
        },
        {
            "title": "La parentesi verbale: modali e prefissi separabili",
            "outcome": "Esprimere capacitÃ , obbligo e intenzione e comprendere frasi in cui un elemento verbale va alla fine.",
            "sections": (
                ("Mappa", "Con `kÃ¶nnen, mÃ¼ssen, wollen, dÃ¼rfen, sollen, mÃ¶gen/mÃ¶chten` il modale Ã¨ coniugato in seconda posizione e l'infinito resta alla fine: `Ich muss heute arbeiten.` Questa Ã¨ la prima forma della **Satzklammer**, la parentesi verbale."),
                ("Prefissi", "Nei verbi separabili il prefisso va alla fine nella principale: `aufstehen â†’ Ich stehe um sieben auf`; `anrufen â†’ Sie ruft ihre Mutter an`. Nel dizionario il separabile Ã¨ spesso indicato con un accento: `AUFstehen`. Non separare verbi non separabili come `besuchen`: `Ich besuche â€¦`, non *suche â€¦ be*."),
                ("Scelte di registro", "`mÃ¶chte` Ã¨ la richiesta o desiderio cortese: `Ich mÃ¶chte einen Termin.` Non Ã¨ identico a `wollen`, che esprime volontÃ  piÃ¹ diretta: `Ich will gehen.` Per un cartello o un regolamento, `mÃ¼ssen` comunica obbligo; `dÃ¼rfen` permesso o divieto (`Hier darf man nicht rauchen`)."),
                ("Allenamento", "Completa: `Am Samstag ___ wir im Supermarkt ___. (einkaufen)`; `Du ___ deinen Ausweis ___. (mitbringen / mÃ¼ssen)`. Evidenzia il verbo finito con un colore e il secondo elemento verbale con un altro."),
                ("Autocontrollo", "In `Kannst du mir helfen?` il soggetto Ã¨ dopo il verbo perchÃ© Ã¨ una domanda; `helfen` Ã¨ in fondo. Se il secondo pezzo non Ã¨ alla fine, ricontrolla la frase."),
            ),
        },
        {
            "title": "Tempo, numeri e routine: parlare con precisione",
            "outcome": "Fissare appuntamenti, indicare date, orari e frequenza senza tradurre parola per parola.",
            "sections": (
                ("Mappa", "Per il tempo usa blocchi memorizzabili: `am Montag`, `um 8 Uhr`, `von 9 bis 17 Uhr`, `im Mai`, `heute Morgen`, `jeden Tag`. Metti normalmente il tempo nel Vorfeld o prima dei complementi di luogo: `Am Montag arbeite ich im BÃ¼ro.`"),
                ("Orari e numeri", "I numeri da 21 in poi invertono unitÃ  e decine: `einundzwanzig`, `fÃ¼nfundvierzig`. `halb acht` significa le 7:30, cioÃ¨ la metÃ  **prima** delle otto; `Viertel nach sieben` 7:15 e `Viertel vor sieben` 6:45. Per fissare un incontro, usa anche la forma digitale: `um sieben Uhr dreiÃŸig`."),
                ("Routine", "I verbi di routine rendono la grammatica automatica: `aufstehen, frÃ¼hstÃ¼cken, anfangen, fahren, arbeiten, einkaufen, schlafen`. Collega le frasi con `dann` e `danach`, ricordando V2: `Dann fahre ich zur Arbeit.`"),
                ("Allenamento", "Descrivi una giornata con sei frasi: inizia almeno due frasi con un'indicazione di tempo e usa un verbo separabile. Poi fissa un appuntamento: giorno, ora, luogo, durata e conferma: `Passt dir â€¦? â€“ Ja, das passt.`"),
                ("Autocontrollo", "Scrivi 7:30 in due modi e controlla il significato di `halb neun`. Se pensi alle 8:30, trasferisci la logica italiana: in tedesco Ã¨ 8:30 solo `halb neun`."),
            ),
        },
        {
            "title": "Possesso, istruzioni e cortesia",
            "outcome": "Parlare di ciÃ² che appartiene a qualcuno e dare istruzioni semplici nel registro adeguato.",
            "sections": (
                ("Mappa", "`mein, dein, sein, ihr, unser, euer, Ihr` non concordano con il possessore ma con la cosa posseduta: `sein Bruder`, `seine Schwester`, `sein Kind`. Al maschile accusativo: `meinen Ausweis`. Osserva `euer â†’ eure/eurem`, dove spesso cade la seconda `e`."),
                ("Imperativo", "Con `du`: radice senza `-st`, `Komm!`, `Lies!`, `Nimm!`; con `ihr`: forma di `ihr`, `Kommt!`; con `Sie`: infinito + pronome, `Kommen Sie bitte!` Le istruzioni professionali e pubbliche preferiscono la forma cortese o l'infinito da cartello: `Bitte warten`, `Nicht rauchen`."),
                ("Cortesia", "Aggiungi `bitte`, `bitte mal`, `kÃ¶nnen Sie â€¦?` per una richiesta. Un imperativo nudo puÃ² suonare brusco fuori da una situazione familiare. Formula sicura: `KÃ¶nnen Sie bitte Ihren Namen sagen?`"),
                ("Allenamento", "Descrivi una borsa con cinque oggetti: `Das ist mein â€¦ / Das sind meine â€¦` Poi trasforma istruzioni dirette in cortesi: `Ã–ffnen Sie die TÃ¼r.` â†’ `KÃ¶nnen Sie bitte die TÃ¼r Ã¶ffnen?`"),
                ("Autocontrollo", "`ihre Adresse` puÃ² significare la sua (di lei), la loro o la Sua: il contesto e la maiuscola chiariscono. Verifica sempre il nome posseduto prima di scegliere la desinenza."),
            ),
        },
    ),
    "A2": (
        {
            "title": "Raccontare il passato con il Perfekt",
            "outcome": "Riferire esperienze, spostamenti e tappe biografiche usando ausiliare e participio in modo affidabile.",
            "sections": (
                ("Mappa", "Il Perfekt Ã¨ `haben/sein` coniugato in seconda posizione + `Partizip II` alla fine: `Ich habe gearbeitet.` / `Wir sind gefahren.` Nei dialoghi quotidiani Ã¨ il principale tempo del passato. La parentesi verbale torna: ausiliare all'inizio della struttura, participio in chiusura."),
                ("Costruzione", "Regolari: `ge- + radice + -t` (`gemacht`); molti irregolari: `ge- + radice + -en` (`gesehen, geschrieben`). I verbi in `-ieren` non prendono `ge-`: `studiert`. I prefissi inseparabili `be-, emp-, ent-, er-, ge-, miss-, ver-, zer-` non lo prendono: `besucht, verstanden`. Impara ogni verbo forte in tre forme: `fahren â€“ fuhr â€“ ist gefahren`."),
                ("Haben o sein?", "Di solito `sein` con movimento da un luogo a un altro o cambiamento di stato: `gehen, kommen, fahren, aufstehen, einschlafen, bleiben`. Non basta il movimento fisico: `Ich habe getanzt` usa `haben`. Se il verbo ha oggetto, in genere usa `haben`: `Ich habe das Auto gefahren.`"),
                ("Allenamento", "Racconta ieri in quattro sequenze: inizio, spostamento, attivitÃ , fine. Evidenzia l'ausiliare e cerchia il participio. Trasforma `Wir fahren nach Hamburg` in Perfekt e spiega perchÃ© scegli `sein`."),
                ("Autocontrollo", "`Ich habe nach Hause gegangen` Ã¨ errato: `Ich bin nach Hause gegangen`. PerÃ² `Ich habe den ganzen Tag gearbeitet` Ã¨ corretto anche se sei andato al lavoro: conta il verbo, non il contesto."),
            ),
        },
        {
            "title": "Dativo, accusativo e destinatario dell'azione",
            "outcome": "Dire chi riceve qualcosa e che cosa viene trasferito, comprendendo articoli e pronomi piÃ¹ comuni.",
            "sections": (
                ("Mappa", "Pensa al modello `jemandem etwas geben`: persona/destinatario al dativo, cosa all'accusativo. `Ich gebe dem Kind den Ball.` Articoli definiti al dativo: `dem, der, dem, den + -n` al plurale: `mit den Kindern`. Indeterminativi: `einem, einer, einem`."),
                ("Verbi da imparare in coppia", "Dativo + accusativo: `geben, schicken, zeigen, erklÃ¤ren, bringen, kaufen`. Solo dativo: `helfen, danken, gefallen, gehÃ¶ren, antworten`. Non dire *ich helfe dich*: `Ich helfe dir`. Impara il verbo con una frase-tipo, non con la sola traduzione."),
                ("Ordine", "Con due nomi, spesso dativo prima di accusativo: `Ich gebe meiner Kollegin die Unterlagen.` Con pronome personale, normalmente il pronome va prima: `Ich gebe ihr die Unterlagen.` Se entrambi sono pronomi: `Ich gebe sie ihr` (accusativo prima del dativo)."),
                ("Allenamento", "Completa una mini-consegna: chi invia che cosa a chi? `Der Chef schickt â€¦` Cambia poi i nomi in pronomi: `Der Chef schickt die E-Mail der Kollegin` â†’ `Er schickt sie ihr.`"),
                ("Autocontrollo", "Chiediti sempre due cose: *a chi?* = dativo; *che cosa?* = accusativo. Se il verbo Ã¨ `helfen`, non serve un secondo oggetto: `Kannst du mir helfen?`"),
            ),
        },
        {
            "title": "Luogo e movimento: le WechselprÃ¤positionen",
            "outcome": "Distinguere posizione e direzione per descrivere abitazione, cittÃ , spostamenti e indicazioni.",
            "sections": (
                ("Mappa", "`an, auf, hinter, in, neben, Ã¼ber, unter, vor, zwischen` possono reggere dativo o accusativo. La domanda decide: **Wo?** posizione â†’ dativo, `Das Bild hÃ¤ngt an der Wand`; **Wohin?** destinazione/cambiamento di posto â†’ accusativo, `Ich hÃ¤nge das Bild an die Wand`."),
                ("Non Ã¨ il movimento", "Non chiederti semplicemente se qualcuno si muove. `Ich laufe im Park` risponde *dove?* quindi dativo, anche se cammino. `Ich laufe in den Park` risponde *verso dove?* quindi accusativo. Questa coppia Ã¨ la prova migliore."),
                ("Preposizioni fisse", "Altre preposizioni richiedono sempre una forma: dativo `aus, bei, mit, nach, seit, von, zu`; accusativo `durch, fÃ¼r, gegen, ohne, um`. Le destinazioni-cittÃ  senza articolo usano `nach Berlin`; edifici/persone spesso `zu`: `zum Arzt`, `zur Arbeit`."),
                ("Allenamento", "Disegna una stanza semplice e descrivi tre oggetti con `wo?`; poi spostane due con `wohin?`. Produci coppie: `Das Handy liegt auf dem Tisch. â€“ Ich lege das Handy auf den Tisch.`"),
                ("Autocontrollo", "`in dem` diventa spesso `im`; `in das` diventa `ins`; `an dem` â†’ `am`, `an das` â†’ `ans`. La contrazione non cambia il caso: `im` Ã¨ dativo, `ins` accusativo."),
            ),
        },
        {
            "title": "Confrontare, motivare e collegare le idee",
            "outcome": "Esprimere preferenze e differenze, dando una ragione in frasi chiare e collegate.",
            "sections": (
                ("Mappa", "Comparativo: aggettivo + `-er` + `als`: `Berlin ist grÃ¶ÃŸer als Bonn.` Uguaglianza: `so â€¦ wie`: `Der Kurs ist so interessant wie â€¦` Superlativo attributivo: `der beste Kurs`; avverbiale: `am besten`. Alcuni sono irregolari: `gut â€“ besser â€“ am besten`, `viel â€“ mehr â€“ am meisten`."),
                ("Tre modi per la causa", "`weil` apre una subordinata e manda il verbo alla fine: `Ich lerne Deutsch, weil ich in Deutschland arbeite.` `denn` coordina e conserva V2: `â€¦, denn ich arbeite â€¦` `deshalb` occupa il Vorfeld della nuova principale: `Ich arbeite in Deutschland. Deshalb lerne ich Deutsch.`"),
                ("Scelta", "Usa `weil` quando la ragione appartiene alla stessa frase; `deshalb` quando vuoi presentarla come conseguenza nella frase seguente. Evita di mettere due verbi finiti nello stesso segmento: dopo `weil` il verbo coniugato deve chiudere la subordinata."),
                ("Allenamento", "Confronta due cittÃ  o due lavori con tre frasi: una con `als`, una con `so â€¦ wie`, una con superlativo. Poi dai la stessa ragione con `weil`, `denn` e `deshalb` e osserva dove va il verbo."),
                ("Autocontrollo", "*weil ich lerne Deutsch* Ã¨ errato: `weil ich Deutsch lerne`. *Deshalb ich lerne Deutsch* Ã¨ errato: `Deshalb lerne ich Deutsch`, perchÃ© anche qui vale V2."),
            ),
        },
        {
            "title": "Subordinate essenziali: dass, weil, wenn, obwohl",
            "outcome": "Collegare eventi, opinioni, condizioni e contrasti con una struttura di frase stabile.",
            "sections": (
                ("Mappa", "Una congiunzione subordinante apre una frase dipendente e sposta il verbo finito alla fine: `Ich weiÃŸ, dass der Kurs heute beginnt.` Nel blocco principale il verbo resta al suo posto. Segna sempre la virgola: Ã¨ parte della grammatica tedesca scritta."),
                ("Funzioni", "`dass` introduce contenuto/opinione: `Ich finde, dass â€¦`; `weil` causa; `wenn` condizione o evento ripetuto/futuro: `Wenn ich Zeit habe, â€¦`; `obwohl` contrasto: `Obwohl es regnet, gehe ich spazieren.` Per un fatto singolo nel passato usa spesso `als`: `Als ich klein war, â€¦`"),
                ("Doppia parentesi", "Con un modale o Perfekt, gli elementi verbali si accumulano alla fine: `â€¦, weil ich morgen arbeiten muss`; `â€¦, weil ich lange gearbeitet habe`. Non aggiungere una coniugazione all'inizio della subordinata."),
                ("Allenamento", "Unisci coppie di frasi con `dass`, `weil`, `wenn`, `obwohl`. Poi inizia la frase con la subordinata: `Wenn ich Zeit habe, lerne ich.` Nota la virgola e l'inversione nella principale (`lerne ich`, non *ich lerne*)."),
                ("Autocontrollo", "Trova il verbo finito in `Ich bleibe zu Hause, weil ich krank bin.` Ãˆ `bin`, e chiude la subordinata. In una subordinata breve Ã¨ facile; allenati anche con quelle lunghe."),
            ),
        },
        {
            "title": "Vita pratica: servizi, salute e comunicazione formale",
            "outcome": "Gestire appuntamenti, richieste e problemi quotidiani con frasi comprensibili e registro adeguato.",
            "sections": (
                ("Mappa", "In un servizio pubblico o sanitario chiarisci sempre: chi sei, perchÃ© contatti, qual Ã¨ il problema, che cosa chiedi e quali dati offri. Formula sicura: `Guten Tag, mein Name ist â€¦ Ich mÃ¶chte einen Termin vereinbaren, weil â€¦`"),
                ("Lessico in azione", "Impara le combinazioni: `einen Termin vereinbaren/verschieben/absagen`, `ein Formular ausfÃ¼llen`, `einen Antrag stellen`, `eine Krankmeldung abgeben`, `ein Rezept bekommen`. Il verbo dÃ  la struttura; il nome isolato non basta per usare la parola."),
                ("Passato frequente", "Nel parlato `sein, haben` e i modali compaiono anche al PrÃ¤teritum: `Ich hatte`, `ich war`, `ich konnte`, `ich musste`. Sono piÃ¹ rapidi e naturali di *ich habe gehabt* nei dialoghi. Il Perfekt resta invece normale per molti altri verbi."),
                ("Allenamento", "Scrivi un messaggio di 60â€“80 parole per spostare un appuntamento: saluto, riferimento, motivazione, nuova proposta, ringraziamento e formula di chiusura. Poi esercita a voce una telefonata con una domanda di chiarimento: `KÃ¶nnten Sie das bitte wiederholen?`"),
                ("Autocontrollo", "Una richiesta non Ã¨ un ordine: preferisci `KÃ¶nnten Sie â€¦?`, `Ich hÃ¤tte gern â€¦`, `WÃ¤re es mÃ¶glich, â€¦?` Se manca una delle cinque informazioni della mappa, il destinatario deve fare una domanda in piÃ¹."),
            ),
        },
        {
            "title": "Pronomi e verbi riflessivi",
            "outcome": "Parlare di sÃ©, routine e relazioni usando i pronomi nel caso giusto e riconoscendo i verbi riflessivi.",
            "sections": (
                ("Mappa", "Accusativo: `mich, dich, ihn, sie, es, uns, euch, sie/Sie`; dativo: `mir, dir, ihm, ihr, ihm, uns, euch, ihnen/Ihnen`. Sostituisci un nome giÃ  noto per evitare ripetizioni: `Ich sehe den Arzt. Ich sehe ihn.`"),
                ("Riflessivo", "Alcuni verbi richiedono il pronome riflessivo: `sich freuen, sich interessieren, sich erinnern, sich treffen`. Spesso l'accusativo: `Ich freue mich`; talvolta dativo con un altro oggetto: `Ich wasche mir die HÃ¤nde` (le mani sono l'accusativo, la persona il dativo)."),
                ("Posizione", "Nella principale il pronome breve va presto dopo il verbo: `Ich treffe mich heute mit Anna.` Con modale: `Ich mÃ¶chte mich heute mit Anna treffen.` Impara `sich` insieme alla preposizione quando necessaria: `sich freuen auf/Ã¼ber`, `sich interessieren fÃ¼r`."),
                ("Allenamento", "Trasforma cinque nomi in pronomi: `Ich rufe meine Mutter an` â†’ `Ich rufe sie an`. Poi descrivi la mattina con tre riflessivi e crea una domanda: `Worauf freust du dich?`"),
                ("Autocontrollo", "Non ogni azione su di sÃ© Ã¨ riflessiva come in italiano: si dice `Ich wasche meine Haare` oppure `Ich wasche mir die Haare`, non necessariamente *ich wasche mich die Haare*. Controlla il verbo nel dizionario."),
            ),
        },
    ),
    "B1": (
        {
            "title": "Coesione: subordinare, connettere, sintetizzare",
            "outcome": "Costruire un testo coerente con cause, condizioni, scopi e conseguenze.",
            "sections": (
                ("Mappa", "A B1 non basta una successione di frasi corrette: il lettore deve vedere il rapporto logico. Alterna congiunzioni (`weil, obwohl, falls, wÃ¤hrend`) e avverbi connettivi (`deshalb, trotzdem, auÃŸerdem, dann`). Le prime spostano il verbo alla fine; i secondi occupano il Vorfeld e mantengono V2."),
                ("Scopo", "Con lo stesso soggetto usa `um â€¦ zu + infinito`: `Ich lerne, um die PrÃ¼fung zu bestehen.` Con soggetti diversi usa `damit`: `Ich erklÃ¤re es langsam, damit alle es verstehen.` Dopo `ohne â€¦ zu` esprimi assenza di azione; dopo `statt/anstatt â€¦ zu`, alternativa."),
                ("Condizione e concessione", "`falls` Ã¨ una condizione prudente: `Falls Sie Fragen haben, â€¦`; `wenn` Ã¨ piÃ¹ generale. `obwohl` introduce un ostacolo reale, mentre `trotzdem` apre una nuova principale: `Obwohl es regnet, â€¦` / `Es regnet. Trotzdem â€¦`"),
                ("Allenamento", "Prendi un testo di cinque frasi semplici su un problema al lavoro. Aggiungi almeno una causa, una conseguenza, una condizione e uno scopo. Rileggi e segna ogni verbo finito: deve essere nel posto previsto dalla struttura scelta."),
                ("Autocontrollo", "Se usi `deshalb`, il verbo viene subito dopo: `Deshalb kann ich â€¦`; se usi `weil`, il verbo chiude: `weil ich â€¦ kann`. Il significato Ã¨ simile, la grammatica no."),
            ),
        },
        {
            "title": "Passivo e descrizione dei processi",
            "outcome": "Spiegare procedure, regole e fasi di lavoro mettendo in primo piano l'azione o il risultato.",
            "sections": (
                ("Mappa", "Il Vorgangspassiv descrive un processo: `werden + Partizip II`: `Die Rechnung wird geprÃ¼ft.` Il soggetto grammaticale Ã¨ ciÃ² che subisce l'azione. Al passato: `wurde geprÃ¼ft`; al Perfekt: `ist geprÃ¼ft worden`. Con modale: `Die Rechnung muss geprÃ¼ft werden.`"),
                ("Agente", "Se serve, indica chi agisce con `von` per persone/istituzioni: `Der Antrag wird von der BehÃ¶rde bearbeitet`; `durch` per mezzo/cause: `durch ein Programm`. Spesso l'agente non Ã¨ importante: Ã¨ proprio il motivo per scegliere il passivo."),
                ("Stato", "`sein + Partizip II` non Ã¨ un processo ma un risultato: `Die TÃ¼r ist geÃ¶ffnet` = la porta Ã¨ aperta. `Die TÃ¼r wird geÃ¶ffnet` = qualcuno la sta aprendo. Questa distinzione evita molte frasi ambigue in istruzioni e report."),
                ("Allenamento", "Scrivi cinque passaggi per un processo noto (prenotazione, consegna, ricetta): prima attivo, poi passivo. Inserisci un modale e un indicatore di sequenza: `Zuerst â€¦, anschlieÃŸend â€¦, zum Schluss â€¦`."),
                ("Autocontrollo", "*Die Rechnung wird geprÃ¼ft worden* Ã¨ errato. Presente: `wird geprÃ¼ft`; Perfekt: `ist geprÃ¼ft worden`. Ricorda: nel Perfekt passivo l'ausiliare Ã¨ `sein` e `worden` resta alla fine."),
            ),
        },
        {
            "title": "Relative: aggiungere informazione con precisione",
            "outcome": "Unire frasi e descrivere persone, oggetti e luoghi evitando ripetizioni.",
            "sections": (
                ("Mappa", "La relativa segue un nome e comincia con pronome relativo: `der, die, das, die`; il verbo finito va alla fine: `Das ist die Kollegin, die heute beginnt.` Il genere e il numero vengono dal nome antecedente; il caso dipende dalla funzione nella relativa."),
                ("Come scegliere", "`Der Mann, der dort steht` (soggetto); `der Mann, den ich kenne` (oggetto); `der Mann, dem ich helfe` (dativo). Fai due domande: qual Ã¨ l'antecedente? Che funzione ha il pronome nella relativa? Non scegliere il caso dal nome nella frase principale."),
                ("Forme utili", "Con preposizione: `Die Firma, bei der ich arbeite`; `Das Thema, Ã¼ber das wir sprechen`. Per intere frasi o parole come `alles, etwas, nichts`, spesso `was`: `Alles, was du sagst, ist wichtig.` Luoghi: `der Ort, wo â€¦` Ã¨ comune parlato; nello scritto formale preferisci `an dem/in dem â€¦`."),
                ("Allenamento", "Unisci: `Ich suche eine Wohnung. Die Wohnung liegt zentral.` Poi: `Das ist die Frau. Ich habe der Frau geschrieben.` Spiega a voce perchÃ© nella seconda relativa serve il dativo."),
                ("Autocontrollo", "La virgola apre e chiude la relativa. In `Die Unterlagen, die ich gestern geschickt habe, sind angekommen` il verbo `habe` chiude la relativa, mentre `sind` regge la principale."),
            ),
        },
        {
            "title": "Esprimere e sostenere un'opinione",
            "outcome": "Partecipare a una discussione rispettosa, distinguendo tesi, ragione, esempio e concessione.",
            "sections": (
                ("Mappa", "Una risposta B1 convincente segue un filo: **tesi** (`Meiner Meinung nach â€¦`), **ragione** (`Das liegt daran, dass â€¦`), **esempio** (`Zum Beispiel â€¦`), **conseguenza** (`Deshalb â€¦`) e, se utile, **concessione** (`Zwar â€¦, aber â€¦` / `Einerseits â€¦, andererseits â€¦`)."),
                ("Registro", "Distingui fatto, opinione e certezza: `Die Statistik zeigt â€¦` non equivale a `Ich finde â€¦`; `wahrscheinlich, vermutlich, mÃ¶glicherweise` riducono l'affermazione. Per dissentire: `Da bin ich nicht ganz deiner Meinung, weil â€¦` oppure `Ich verstehe deinen Punkt, aber â€¦`"),
                ("Parole di confronto", "Usa `nicht nur â€¦ sondern auch`, `sowohl â€¦ als auch`, `weder â€¦ noch` con elementi paralleli. Evita di mettere molti connettori senza relazione: ogni connettore deve rendere visibile un preciso passaggio di pensiero."),
                ("Allenamento", "Scegli un tema quotidiano (lavoro da casa, trasporti, smartphone) e parla per 90 secondi usando la mappa. Poi aggiungi un'obiezione e una risposta. Registra l'audio e verifica se hai dato almeno un esempio concreto."),
                ("Autocontrollo", "Un'opinione senza ragione non Ã¨ un'argomentazione. Se togli `weil/denn/da` e non cambia nulla, forse hai espresso solo una preferenza: aggiungi una prova o una conseguenza."),
            ),
        },
        {
            "title": "Candidatura, comunicazione di lavoro e riconoscimento",
            "outcome": "Scrivere una candidatura essenziale e comunicare in modo chiaro in contesti professionali tedeschi.",
            "sections": (
                ("Mappa", "Un `Lebenslauf` Ã¨ cronologico, sobrio e verificabile; un `Anschreiben` seleziona ciÃ² che Ã¨ rilevante per l'annuncio: motivo, competenze con esempio, disponibilitÃ . Una e-mail professionale ha oggetto informativo, saluto, richiesta/azione, ringraziamento e `Mit freundlichen GrÃ¼ÃŸen`."),
                ("Lessico azionabile", "Preferisci verbi concreti: `organisieren, betreuen, prÃ¼fen, dokumentieren, koordinieren, verantworten`. Non scrivere *ich bin sehr motiviert* e basta: `In meiner bisherigen TÃ¤tigkeit habe ich â€¦ koordiniert; deshalb kann ich â€¦` collega prova e risultato."),
                ("Colloquio", "Rispondi con struttura breve: situazione â€“ compito â€“ azione â€“ risultato. Chiedi chiarimenti con `KÃ¶nnten Sie bitte erlÃ¤utern, â€¦?` e conferma: `Habe ich Sie richtig verstanden, dass â€¦?` Il registro resta formale finchÃ© non viene proposto il `du`."),
                ("Riconoscimento: confine importante", "IHK FOSA Ã¨ un ente per la valutazione dell'equivalenza di molte qualifiche professionali estere nell'area IHK, non un fornitore di corsi di tedesco. Le esigenze linguistiche dipendono da professione, datore di lavoro, autorizzazioni e misura prevista: il corso prepara a leggere e scrivere documenti, non garantisce requisiti legali."),
                ("Allenamento", "Adatta tre righe di CV a un annuncio: usa una competenza, un'attivitÃ , un risultato. Poi scrivi un'e-mail per chiedere informazioni su una candidatura, senza allegare dati personali sensibili in un esercizio."),
            ),
        },
        {
            "title": "Strategia B1 nelle quattro abilitÃ ",
            "outcome": "Affrontare lettura, ascolto, scrittura e orale con una procedura ripetibile e controllare gli errori ad alto impatto.",
            "sections": (
                ("Mappa", "Il livello B1 richiede autonomia su temi familiari e testi chiari. Non studiare grammatica separata dalle abilitÃ : ogni unitÃ  deve produrre un testo, una breve interazione, comprensione globale e comprensione mirata."),
                ("Leggere e ascoltare", "Prima guarda compito, titolo e parole-chiave; poi cerca l'idea globale; alla seconda lettura/ascolto cerca prove puntuali. Non fermarti su ogni parola sconosciuta: deduci da connettori, contesto, prefissi e parti del discorso."),
                ("Scrivere e parlare", "Pianifica in 60 secondi: destinatario, scopo, tre punti, chiusura. Dopo il testo controlla nell'ordine: 1 verbo e ordine, 2 caso/preposizione, 3 genere/plurale, 4 connettori, 5 registro. Nell'orale usa riparazioni: `Ich meine â€¦`, `Anders gesagt â€¦`, `KÃ¶nnen Sie die Frage bitte wiederholen?`"),
                ("Allenamento", "Per un argomento B1, prepara una lista di 12 parole chiave e parla due minuti senza leggere un copione. Poi scrivi una e-mail di 100 parole sullo stesso argomento. Confronta: il messaggio risponde davvero al compito?"),
                ("Autocontrollo", "Un test pratica il formato, ma l'obiettivo Ã¨ trasferire la lingua. Tieni un quaderno degli errori con: frase sbagliata, correzione, regola personale e una nuova frase tua."),
            ),
        },
        {
            "title": "Aggettivi, genitivo e gruppi nominali",
            "outcome": "Comprendere e produrre sintagmi nominali piÃ¹ precisi in descrizioni e testi formali.",
            "sections": (
                ("Mappa", "La desinenza dell'aggettivo segnala genere, numero e caso. Strategia: prima individua articolo e caso, poi applica il modello. Dopo articolo determinativo molte informazioni sono giÃ  sull'articolo: `der gute Plan / den guten Plan / mit dem guten Plan`; dopo `ein` l'aggettivo completa ciÃ² che l'articolo non mostra: `ein guter Plan`, `ein gutes Angebot`."),
                ("Genitivo", "Indica soprattutto possesso o relazione: `die Adresse des Kunden`, `die Dauer der Schulung`. Maschile/neutro: `des + -(e)s` al nome; femminile/plurale: `der`. Nel parlato spesso `von + dativo`, ma il genitivo Ã¨ comune nei testi formali e nei titoli."),
                ("N-Deklination", "Alcuni nomi maschili prendono `-n/-en` in quasi tutti i casi: `der Kunde, den Kunden, dem Kunden`; `der Mensch, dem Menschen`. Imparali come gruppo nominale, non come eccezione isolata."),
                ("Allenamento", "Espandi `Plan`: `der neue Plan`, `mit dem neuen Plan`, `ein neuer Plan`, `wegen des neuen Plans`. Poi descrivi un documento con tre gruppi nominali e rileggi prima gli articoli, poi le desinenze."),
                ("Autocontrollo", "Non cercare di ricordare decine di finali senza contesto. Se sai riconoscere caso e articolo, l'aggettivo diventa un controllo visibile, non un indovinello."),
            ),
        },
    ),
    "B2": (
        {
            "title": "Riportare fonti: Konjunktiv I e discorso indiretto",
            "outcome": "Distinguere tra ciÃ² che affermi e ciÃ² che riferisci, attribuendo correttamente informazioni e posizioni.",
            "sections": (
                ("Mappa", "Il Konjunktiv I segnala discorso indiretto: `Der Bericht erklÃ¤rt, die Kosten seien gestiegen.` Le forme piÃ¹ riconoscibili sono `sei, habe, werde, kÃ¶nne, mÃ¼sse`. Non rende un'informazione falsa: marca distanza e fonte, essenziale in notizie, verbali e sintesi."),
                ("Procedura", "1. Nomina la fonte (`laut dem Bericht`, `die Sprecherin sagt â€¦`). 2. Trasforma il verbo quando la forma Ã¨ riconoscibile. 3. Mantieni tempo e significato con coerenza. Se Konjunktiv I e indicativo coincidono, si usa spesso Konjunktiv II: `Sie sagten, sie hÃ¤tten â€¦`"),
                ("Non confondere", "`Er sagt, er kommt spÃ¤ter` Ã¨ discorso diretto riportato in stile quotidiano; `Er sagt, er komme spÃ¤ter` Ã¨ marcato e formale. `Er kÃ¤me spÃ¤ter` puÃ² essere forma sostitutiva o, in un altro contesto, ipotesi: cerca sempre la fonte e l'intenzione comunicativa."),
                ("Allenamento", "Trasforma cinque informazioni di una breve notizia: `Die Firma: â€žWir erÃ¶ffnen im Mai.â€œ` â†’ `Die Firma teilt mit, sie werde im Mai erÃ¶ffnen.` Inserisci per ogni frase una fonte e non aggiungere inferenze personali."),
                ("Autocontrollo", "Una sintesi corretta separa `il testo afferma` da `io penso`. Sottolinea i verbi di fonte (`berichten, erklÃ¤ren, betonen, behaupten`) e controlla che il lettore sappia sempre a chi attribuire ogni tesi."),
            ),
        },
        {
            "title": "Konjunktiv II: ipotesi, desideri e diplomazia",
            "outcome": "Formulare scenari non reali, richieste attenuate, proposte e rimpianti con il registro appropriato.",
            "sections": (
                ("Mappa", "Presente/ipotesi: `wÃ¼rde + infinito` Ã¨ produttivo: `Ich wÃ¼rde den Vorschlag prÃ¼fen.` Forme frequenti da sapere: `hÃ¤tte, wÃ¤re, kÃ¶nnte, mÃ¼sste, sollte, dÃ¼rfte, mÃ¶chte`. Condizione: `Wenn ich mehr Zeit hÃ¤tte, wÃ¼rde ich â€¦`"),
                ("Passato", "Per un'ipotesi o un rimpianto nel passato: `hÃ¤tte/wÃ¤re + Partizip II`: `Ich hÃ¤tte frÃ¼her Bescheid geben sollen.` / `Wir wÃ¤ren gern gekommen.` Con modale: `Ich hÃ¤tte das erledigen kÃ¶nnen.`"),
                ("Diplomazia", "Il Konjunktiv II attenua: `KÃ¶nnten Sie â€¦?`, `WÃ¤re es mÃ¶glich, â€¦?`, `Ich wÃ¼rde vorschlagen, â€¦` Non usare troppi condizionali se vuoi essere chiaro: dopo una richiesta, indica azione e scadenza in modo diretto ma cortese."),
                ("Allenamento", "Scrivi tre coppie realtÃ /ipotesi: `Ich habe keine Zeit. â€“ Wenn ich Zeit hÃ¤tte, â€¦` Poi riformula tre ordini come richieste professionali. Infine esprimi un rimpianto per una riunione mancata."),
                ("Autocontrollo", "`wÃ¼rde` non sostituisce automaticamente ogni forma: per `sein, haben, modali` le forme semplici (`wÃ¤re, hÃ¤tte, kÃ¶nnte`) sono in genere piÃ¹ naturali. Scegli la forma che il lettore riconosce subito."),
            ),
        },
        {
            "title": "Argomentazione complessa e uso responsabile delle fonti",
            "outcome": "Scrivere e discutere una posizione articolata, valutando alternative e distinguendo fatti, esempi e interpretazioni.",
            "sections": (
                ("Mappa", "Una Stellungnahme B2 ha: questione e tesi, due o tre argomenti sviluppati, controargomento trattato lealmente, valutazione e conclusione. Ogni paragrafo compie una funzione sola. Collegamenti possibili: `zunÃ¤chst, darÃ¼ber hinaus, allerdings, demgegenÃ¼ber, folglich, abschlieÃŸend`."),
                ("QualitÃ  della prova", "Un esempio illustra; un dato supporta; una fonte attribuisce; nessuno dei tre dimostra tutto da solo. Formula con precisione: `Die Grafik legt nahe â€¦`, `Die Autorin argumentiert â€¦`, `Daraus folgt nicht zwingend, dass â€¦` Evita causalitÃ  assolute quando hai solo una correlazione."),
                ("Concessione", "Rafforza la tesi riconoscendo un limite: `Zwar â€¦, jedoch â€¦`; `Auch wenn â€¦, bleibt â€¦`; `Es ist einzurÃ¤umen, dass â€¦` La concessione non Ã¨ un riempitivo: deve rispondere a una vera possibile obiezione."),
                ("Allenamento", "Scegli una domanda con due soluzioni. Crea una tabella mentale: criterio, vantaggio, rischio, prova/esempio. Scrivi 180â€“220 parole e verifica che ogni conclusione risponda a un argomento giÃ  presentato."),
                ("Autocontrollo", "Conta i connettori, ma soprattutto nomina il rapporto che ciascuno esprime. Se `allerdings` potrebbe essere sostituito da qualunque parola senza cambiare il senso, riscrivi il passaggio logico."),
            ),
        },
        {
            "title": "Nominalizzazione, stile e densitÃ  informativa",
            "outcome": "Leggere e produrre testo formale senza perdere chiarezza, scegliendo consapevolmente tra frase verbale e nominale.",
            "sections": (
                ("Mappa", "Il tedesco formale usa spesso nomi da verbi/aggettivi: `entscheiden â†’ die Entscheidung`, `prÃ¼fen â†’ die PrÃ¼fung`, `mÃ¶glich â†’ die MÃ¶glichkeit`. Con preposizioni: `bei der PrÃ¼fung`, `nach der Entscheidung`, `zur Verbesserung`. Questo concentra informazioni, ma puÃ² appesantire il testo."),
                ("Trasformare", "Verbo: `Die BehÃ¶rde prÃ¼ft den Antrag.` Nominale: `Die PrÃ¼fung des Antrags durch die BehÃ¶rde â€¦` La seconda forma funziona in titoli, verbali e documenti; la prima Ã¨ spesso piÃ¹ leggibile in un'e-mail. Non nominalizzare per sembrare piÃ¹ avanzato: prima assicurati che il responsabile dell'azione e il messaggio restino chiari."),
                ("Attributi", "La densitÃ  nasce anche da composti e attributi: `die betriebliche WeiterbildungsmaÃŸnahme`, `die im April eingereichten Unterlagen`. Scomponi dal nucleo a destra: `WeiterbildungsmaÃŸnahme` Ã¨ il nucleo, `betriebliche` lo qualifica."),
                ("Allenamento", "Riscrivi un breve avviso in due registri: e-mail chiara con verbi, nota formale con due nominalizzazioni. Poi accorcia una frase che contiene piÃ¹ di due nomi astratti: una frase piÃ¹ semplice puÃ² essere piÃ¹ professionale."),
                ("Autocontrollo", "Controlla le maiuscole: i nomi nominalizzati sono maiuscoli (`beim Lesen`, `etwas Neues`). Se una frase non dice chi deve agire, sostituisci almeno una nominalizzazione con un verbo attivo."),
            ),
        },
        {
            "title": "Lettura specialistica, composti e dati",
            "outcome": "Orientarsi in articoli, istruzioni, grafici e corrispondenza professionale individuando tesi, struttura e dettagli rilevanti.",
            "sections": (
                ("Mappa", "Leggi in tre passaggi: 1. scopo, titolo, mittente e struttura; 2. tesi e segnali logici; 3. dati/dettagli richiesti dal compito. Leggere ogni parola dall'inizio Ã¨ inefficiente e fa perdere il filo dei testi B2."),
                ("Composti", "In un composto, l'ultima parola Ã¨ il nucleo: `Arbeitszeitgesetz` = legge (`Gesetz`) su tempo (`Zeit`) di lavoro (`Arbeit`). Dividi a destra, poi ricostruisci. Cerca anche elementi di raccordo: `Krankenversicherung`, `Betriebsratssitzung`."),
                ("Grafici", "Distingui valore, confronto e interpretazione: `Der Anteil stieg von â€¦ auf â€¦`; `liegt bei â€¦`; `ist im Vergleich zu â€¦ hÃ¶her`; `dies kÃ¶nnte darauf hindeuten, dass â€¦`. Un grafico mostra dati, non cause automatiche. Specifica unitÃ , periodo e gruppo di riferimento."),
                ("Allenamento", "Scegli un testo di lavoro di una pagina. Scrivi una frase per scopo, tre parole chiave per paragrafo, una domanda al testo e un riassunto di 80 parole. Per un composto lungo, indica prima il nucleo e poi i modificatori."),
                ("Autocontrollo", "Dopo la lettura verifica: quale informazione Ã¨ esplicita? Quale Ã¨ un'inferenza mia? Una sintesi B2 affidabile mantiene questa distinzione anche quando usa parole diverse dall'originale."),
            ),
        },
        {
            "title": "Produzione B2: progettare, rivedere, presentare",
            "outcome": "Produrre testi e interventi articolati rispondendo con precisione a compito, destinatario, struttura e registro.",
            "sections": (
                ("Mappa", "Prima di scrivere o parlare definisci: genere testuale, destinatario, obiettivo, punti obbligatori, posizione e prove. Una `Beschwerde` chiede rimedio; una `Stellungnahme` valuta; una sintesi attribuisce fonti; una presentazione guida ascoltatori con struttura esplicita."),
                ("Architettura", "Testo: apertura che inquadra, paragrafi con frase-guida, conclusione proporzionata. Presentazione: `ZunÃ¤chst â€¦, anschlieÃŸend â€¦, zum Schluss â€¦`; chiudi con sintesi e domanda. Le formule fisse aiutano solo se il contenuto dopo di esse Ã¨ specifico e pertinente."),
                ("Revisione in passaggi", "Fai piÃ¹ riletture: 1 compito e completezza, 2 logica/ordine dei paragrafi, 3 fonti ed esempi, 4 verbi e casi, 5 lessico e registro, 6 ortografia/punteggiatura. Nella produzione orale, registra una prova e ascolta pause, chiarezza e ripetizioni."),
                ("Allenamento", "Scrivi una risposta B2 con un limite di parole e una lista di controllo. Riducila poi del 15% senza togliere tesi o prove: scoprirai ripetizioni e formule vuote. Presenta il testo in due minuti senza leggerlo integralmente."),
                ("Autocontrollo", "Un testo grammaticalmente ricco non supera un compito se manca un punto richiesto o usa il registro sbagliato. Controlla prima la comunicazione, poi la finezza linguistica."),
            ),
        },
        {
            "title": "Verbi con preposizione e pronominaladverbien",
            "outcome": "Usare combinazioni verbali naturali, domandare e riprendere temi/oggetti con da-/wo- e gestire il caso retto.",
            "sections": (
                ("Mappa", "Impara il blocco intero: `warten auf + Akk`, `teilnehmen an + Dat`, `sich interessieren fÃ¼r + Akk`, `abhÃ¤ngen von + Dat`, `bitten um + Akk`. La preposizione non si traduce meccanicamente e decide il caso. Un verbo memorizzato senza preposizione Ã¨ incompleto."),
                ("Cose e persone", "Per una cosa/tema: `Ich warte darauf.` / `Worauf wartest du?` Per una persona: `Ich warte auf ihn.` / `Auf wen wartest du?` Con vocali iniziali compare `r`: `darauf, worÃ¼ber, daran`. `wofÃ¼r` e `dafÃ¼r` sono una sola parola, non *fÃ¼r was* nello scritto curato."),
                ("Posizione", "La preposizione resta legata al suo complemento; con una subordinata spesso appare `daran, dass â€¦`: `Ich denke daran, dass â€¦` In molti casi Ã¨ piÃ¹ naturale l'infinito con `daran, â€¦ zu`: `Ich denke daran, die Unterlagen zu schicken.`"),
                ("Allenamento", "Crea cartoncini fronte/retro: `sich bewerben â€“ um + Akk â€“ Ich bewerbe mich um â€¦`; `sprechen â€“ mit + Dat â€“ WorÃ¼ber sprechen wir?` Trasforma cinque ripetizioni di un nome-cosa in `da-` e cinque domande in `wo-`."),
                ("Autocontrollo", "Chiedi prima: il riferimento Ã¨ una persona o una cosa? Poi: quale preposizione e quale caso richiede il verbo? Questa sequenza risolve gran parte degli errori B2 con complementi verbali."),
            ),
        },
    ),
}


LABELS = {
    "it": {
        "open": "Approfondimento da manuale", "outcome": "Obiettivo operativo", "note": "L'approfondimento esteso Ã¨ redatto in italiano; la teoria essenziale sopra resta disponibile nella lingua dell'interfaccia.",
    },
    "en": {
        "open": "Textbook deepening", "outcome": "Practical outcome", "note": "The extended deepening is written in Italian; the core theory above remains available in the interface language.",
    },
    "es": {
        "open": "ProfundizaciÃ³n de manual", "outcome": "Objetivo prÃ¡ctico", "note": "La profundizaciÃ³n ampliada estÃ¡ escrita en italiano; la teorÃ­a esencial anterior sigue disponible en el idioma de la interfaz.",
    },
    "tr": {
        "open": "Ders kitabÄ± derinleÅŸtirmesi", "outcome": "UygulamalÄ± hedef", "note": "GeniÅŸletilmiÅŸ derinleÅŸtirme Ä°talyanca yazÄ±lmÄ±ÅŸtÄ±r; yukarÄ±daki temel kuram arayÃ¼z dilinde kullanÄ±labilir.",
    },
}


def render_textbook_unit(st: Any, level: str, topic_index: int, language: str) -> None:
    """Render one expanded textbook unit below the existing concise theory card."""
    unit = UNITS[level][topic_index]
    labels = LABELS[language]
    with st.expander(f"ðŸ“˜ {labels['open']} Â· {unit['title']}", expanded=False):
        if language != "it":
            st.caption(labels["note"])
        st.markdown(f"**{labels['outcome']}.** {unit['outcome']}")
        for heading, text in unit["sections"]:
            st.markdown(f"**{heading}.**  \n{text}")

LEVELS = ("A1", "A2", "B1", "B2")
STORAGE_FILE = Path(__file__).with_name("learner_progress.json")


@dataclass(frozen=True)
class Mission:
    id: str
    level: str
    title: str
    can_do: str
    grammar: str
    lexis: str
    input_task: str
    output_task: str
    challenge: str
    checkpoint: str
    minutes: int


# Ogni missione porta da un input comprensibile a una piccola prestazione.
# Ãˆ piÃ¹ utile di una lunga lista di argomenti: lo studente sa cosa deve saper fare.
MISSIONS = (
    Mission("a1-01", "A1", "Presentarsi con naturalezza", "presentarti, fare domande semplici e reagire a una risposta", "sein, heiÃŸen, kommen; verbo in posizione 2", "identitÃ , paesi, lingue, numeri", "Ascolta o leggi tre mini-profili e sottolinea: nome, origine, lingua, professione.", "Registra o pronuncia un autoritratto di 45 secondi: nome, cittÃ , lavoro/studio, due gusti e una domanda all'interlocutore.", "Cambia l'ordine: Heute wohne ich in â€¦ / In meiner Freizeit â€¦", "Riesci a produrre 6 frasi intere senza leggere?", 35),
    Mission("a1-02", "A1", "Gestire la giornata", "raccontare una routine e fissare un appuntamento", "verbi regolari, separabili e modali", "orari, giorni, routine, appuntamenti", "Leggi un'agenda e ricostruisci a che ora iniziano e finiscono tre attivitÃ .", "Invia un messaggio di 4â€“5 frasi per proporre, accettare o spostare un appuntamento.", "Usa prima il tempo: Am Dienstag kann ich â€¦", "In ogni frase il verbo coniugato Ã¨ davvero al secondo posto?", 40),
    Mission("a1-03", "A1", "Muoversi e acquistare", "chiedere ciÃ² che vuoi, prezzi e indicazioni", "accusativo; mÃ¶chten, kÃ¶nnen; imperativo cortese", "negozi, cibo, trasporti, quantitÃ ", "Leggi tre cartelli e scegli il servizio o il binario appropriato.", "Fai due turni di dialogo: in panetteria e alla fermata. Usa bitte, gern, noch einmal.", "Aggiungi una domanda di chiarimento: Wo genau? / Wie viel kostet das?", "Sai distinguere der da den in almeno tre frasi?", 40),
    Mission("a1-04", "A1", "Descrivere persone e luoghi", "descrivere un ambiente e parlare di ciÃ² che possiedi", "articoli possessivi, negazione kein/nicht, dativo con mit", "casa, famiglia, mobili, aggettivi frequenti", "Confronta due annunci di appartamento e trova quattro differenze.", "Descrivi la tua stanza o un appartamento ideale in 6 frasi; includi una frase negativa.", "Inserisci mit + dativo: Ich wohne mit â€¦", "Il testo contiene informazioni, non solo una lista di nomi?", 40),
    Mission("a2-01", "A2", "Raccontare esperienze", "dire cosa Ã¨ successo, quando e con chi", "Perfekt con haben/sein; participi", "viaggi, weekend, esperienze", "Ordina sei eventi di un weekend usando prima, dann, danach, schlieÃŸlich.", "Racconta un fine settimana in 80â€“100 parole e fai una domanda finale a un amico.", "Usa almeno due verbi di movimento con sein.", "I participi sono alla fine della frase?", 45),
    Mission("a2-02", "A2", "Spiegare un problema", "descrivere un guasto o una difficoltÃ  e chiedere aiuto", "dativo; preposizioni locali; weil", "salute, casa, officina, assistenza", "Leggi tre richieste di assistenza e abbina problema e soluzione.", "Scrivi un messaggio a un servizio clienti: problema, quando Ã¨ iniziato, cosa chiedi.", "Aggiungi una causa con weil e manda il verbo in fondo.", "Il destinatario capisce che cosa deve fare?", 45),
    Mission("a2-03", "A2", "Confrontare e consigliare", "esprimere preferenze e dare un consiglio semplice", "comparativo, superlativo, sollen, lieber", "tempo libero, salute, acquisti", "Scegli tra due offerte e giustifica la scelta con tre criteri.", "Consiglia un amico: Was soll er tun? Usa almeno due confronti.", "Usa zwar â€¦ aber in una frase, anche se non Ã¨ obbligatorio.", "Hai dato una ragione e non solo un'opinione?", 45),
    Mission("a2-04", "A2", "Parlare di progetti", "presentare intenzioni, possibilitÃ  e condizioni semplici", "futuro con werden; wenn; connettori", "lavoro, corsi, progetti, tempo", "Individua in un annuncio cinque informazioni: requisito, orario, luogo, scadenza, contatto.", "Presenta un piano per il mese prossimo in 90 secondi o 100 parole.", "Usa wenn per collegare condizione e conseguenza.", "Ogni frase lunga Ã¨ ancora comprensibile a voce?", 45),
    Mission("b1-01", "B1", "Raccontare con struttura", "narrare un evento, evidenziare il punto importante e reagire", "PrÃ¤teritum di sein/haben/modali; narrazione", "esperienze, imprevisti, emozioni", "Leggi una notizia breve e separa fatti, conseguenze e opinioni.", "Racconta un imprevisto in 130 parole: situazione, svolta, soluzione, lezione imparata.", "Inserisci almeno tre marcatori temporali variati.", "Un lettore puÃ² ricostruire chiaramente la sequenza?", 50),
    Mission("b1-02", "B1", "Lavorare e collaborare", "spiegare una procedura e coordinare attivitÃ ", "passivo presente; infinitive clauses um â€¦ zu", "lavoro, sicurezza, istruzioni, strumenti", "Trasforma quattro istruzioni dirette in una procedura neutra.", "Scrivi una procedura di lavoro sicura in 6 passaggi oppure spiega come si fa una prenotazione.", "Usa prima, danach, anschlieÃŸend, zum Schluss.", "Hai specificato chi fa cosa e in quale ordine?", 50),
    Mission("b1-03", "B1", "Argomentare con equilibrio", "dire ciÃ² che pensi e riconoscere un punto di vista diverso", "weil, obwohl, deshalb, trotzdem; frasi secondarie", "societÃ , digitale, ambiente, scuola", "Classifica otto affermazioni in fatto, opinione, esempio e conseguenza.", "Scrivi un post di forum di 150 parole: posizione, due ragioni, controargomento, conclusione.", "Collega le idee con almeno quattro connettori diversi.", "Dopo obwohl/weil il verbo finisce davvero alla fine?", 55),
    Mission("b1-04", "B1", "Capire e mediare", "trasmettere in modo semplice un'informazione tedesca a un italofono", "pronomi relativi; verbi con preposizione", "avvisi, regole, salute, viaggi", "Leggi un regolamento tedesco e individua obblighi, divieti e eccezioni.", "Spiega in italiano a un amico le tre informazioni operative piÃ¹ importanti; poi formula una domanda in tedesco per verificare se ha capito.", "Non tradurre parola per parola: raggruppa il significato.", "Hai conservato i dettagli che cambiano davvero l'azione?", 50),
    Mission("b2-01", "B2", "Difendere una posizione", "sostenere una tesi con precisione, esempi e concessioni", "connettori argomentativi; zwar â€¦ aber; Konjunktiv II", "lavoro ibrido, mobilitÃ , istruzione", "Leggi due opinioni opposte e annota tesi, argomento, prova, limite.", "Prepara un intervento di 2 minuti: tesi, due argomenti, obiezione, risposta e conclusione.", "Usa almeno una concessione: Einerseits â€¦ andererseits â€¦", "La conclusione riprende la tesi senza ripeterla uguale?", 60),
    Mission("b2-02", "B2", "Scrivere in registro formale", "scrivere una richiesta o un reclamo professionale persuasivo", "nominalizzazioni frequenti; Konjunktiv II di cortesia; struttura e-mail", "azienda, amministrazione, servizi, candidature", "Analizza due e-mail: oggetto, scopo, richiesta concreta, chiusura.", "Scrivi 180â€“220 parole a un ufficio/azienda: contesto, problema o richiesta, proposta, scadenza, chiusura.", "Evita saluti informali e indica una richiesta verificabile.", "Il registro resta formale dall'oggetto al saluto?", 65),
    Mission("b2-03", "B2", "Comprendere l'implicito", "distinguere fatti, atteggiamenti e intenzioni in testi complessi", "Konjunktiv I nel discorso indiretto; particelle e sfumature", "media, scienza, cultura, politiche pubbliche", "Leggi un commento e marca ciÃ² che Ã¨ fatto, citazione, valutazione e ironia possibile.", "Riporta a voce l'opinione di un autore senza attribuirla a te: Der Autor betont, er sei â€¦", "Confronta due fonti: in che cosa cambiano prospettiva e tono?", "Sai dire 'secondo la fonte' anche quando non sei d'accordo?", 60),
    Mission("b2-04", "B2", "Negoziare una soluzione", "interagire spontaneamente, chiarire e arrivare a un compromesso", "ipotesi con Konjunktiv II; frasi relative avanzate", "alloggio, lavoro, progetto, decisioni comuni", "Leggi un caso con interessi in conflitto e annota prioritÃ /non negoziabili di entrambe le parti.", "Fai una simulazione di 3 minuti: proposta, reazione, domanda chiarificatrice, alternativa, accordo.", "Riformula prima l'idea dell'altro: Wenn ich Sie richtig verstehe, â€¦", "Hai chiesto, reagito e costruito una soluzione; non hai solo parlato?", 65),
)


WRITING_PROMPTS = (
    {
        "level": "B1", "title": "Forum: smartphone a scuola", "words": "150â€“180",
        "brief": "In un forum scolastico si discute se gli smartphone debbano essere vietati durante le lezioni. Esprimi la tua posizione, dai due ragioni, considera un'obiezione e proponi una regola concreta.",
        "useful": "Meines Erachtens â€¦ / Ein wichtiger Vorteil/Nachteil ist â€¦ / Zwar â€¦, aber â€¦ / Deshalb schlage ich vor, dass â€¦",
    },
    {
        "level": "B1", "title": "Messaggio al gruppo", "words": "120â€“150",
        "brief": "Il tuo gruppo sta organizzando un viaggio ma il piano iniziale Ã¨ troppo costoso. Scrivi al gruppo: spiega il problema, confronta due alternative, esprimi una preferenza e chiedi una decisione.",
        "useful": "Ich habe festgestellt, dass â€¦ / Im Vergleich dazu â€¦ / WÃ¤re es mÃ¶glich, â€¦? / Wie seht ihr das?",
    },
    {
        "level": "B2", "title": "E-mail formale: corso annullato", "words": "180â€“220",
        "brief": "Un corso professionale per il quale hai giÃ  pagato Ã¨ stato annullato con poco preavviso. Scrivi all'organizzazione: indica i fatti, spiega le conseguenze, formula una richiesta precisa e proponi una soluzione accettabile.",
        "useful": "Sehr geehrte Damen und Herren, / hiermit mÃ¶chte ich mich an Sie wenden, weil â€¦ / FÃ¼r mich ergibt sich daraus â€¦ / Ich bitte Sie daher, â€¦ / Mit freundlichen GrÃ¼ÃŸen",
    },
    {
        "level": "B2", "title": "Post argomentativo: cittÃ  senza auto", "words": "180â€“220",
        "brief": "Una cittÃ  vuole limitare drasticamente il traffico privato nel centro. Scrivi un contributo per il forum: valuta vantaggi e svantaggi, rispondi a un'obiezione plausibile e difendi una misura concreta.",
        "useful": "Einerseits â€¦, andererseits â€¦ / Es lÃ¤sst sich nicht bestreiten, dass â€¦ / Dennoch Ã¼berwiegt fÃ¼r mich â€¦ / Entscheidend wÃ¤re, dass â€¦",
    },
    {
        "level": "B2", "title": "Candidatura mirata", "words": "160â€“200",
        "brief": "Hai trovato un tirocinio in Germania nel tuo settore. Scrivi un'e-mail di candidatura: motivo, competenze dimostrabili, disponibilitÃ  e domanda sul processo successivo.",
        "useful": "mit groÃŸem Interesse habe ich â€¦ / Besonders qualifiziert mich â€¦ / Ãœber die Gelegenheit zu einem GesprÃ¤ch wÃ¼rde ich mich freuen. / KÃ¶nnten Sie mir bitte mitteilen, â€¦?",
    },
    {
        "level": "B2", "title": "Sintesi e mediazione", "words": "140â€“180",
        "brief": "Un collega italiano non capisce un avviso tedesco sulla sicurezza sul lavoro. Spiega in italiano le istruzioni operative, le motivazioni e che cosa deve fare se nota un problema. Aggiungi poi due domande in tedesco per verificare la comprensione.",
        "useful": "In pratica significa che â€¦ / Ãˆ obbligatorio â€¦ / In caso di â€¦ bisogna â€¦ / Hast du verstanden, wann â€¦?",
    },
)


SPEAKING_PROMPTS = (
    {
        "level": "A2", "title": "Organizzare un appuntamento", "scenario": "Vuoi incontrare un collega sabato. Il primo orario non va bene all'altra persona.",
        "goal": "Proponi due alternative, chiedi una preferenza e conferma luogo e ora.",
        "moves": "Vorschlag: Wie wÃ¤re es mit â€¦? | Reazione: Das passt mir leider nicht. | Compromesso: Dann kÃ¶nnten wir â€¦ | Conferma: Also treffen wir uns â€¦",
    },
    {
        "level": "B1", "title": "Risolvere un problema in casa", "scenario": "Il vicino fa rumore tardi; non vuoi litigare e cerchi una soluzione.",
        "goal": "Spiega l'effetto concreto, ascolta la sua prospettiva e concorda una regola.",
        "moves": "Ich verstehe, dass â€¦ | FÃ¼r mich ist es schwierig, weil â€¦ | KÃ¶nnten wir vereinbaren, dass â€¦? | Damit wÃ¤re ich einverstanden.",
    },
    {
        "level": "B2", "title": "Lavoro ibrido", "scenario": "Nel team alcuni vogliono piÃ¹ giorni da remoto, altri temono una collaborazione peggiore.",
        "goal": "Difendi una proposta equilibrata, rispondi a un'obiezione e chiudi con un compromesso operativo.",
        "moves": "Aus meiner Sicht spricht dafÃ¼r, dass â€¦ | Ich kann den Einwand nachvollziehen. | Entscheidend wÃ¤re jedoch â€¦ | WÃ¤re ein Pilotprojekt denkbar?",
    },
    {
        "level": "B2", "title": "Trovare un alloggio", "scenario": "Con un coinquilino devi scegliere tra un appartamento economico lontano e uno costoso vicino al lavoro.",
        "goal": "Pesa criteri, fai domande di chiarimento e raggiungi una decisione comune.",
        "moves": "Wenn wir die Fahrtzeit berÃ¼cksichtigen, â€¦ | Was wÃ¤re dir wichtiger? | Unter der Bedingung, dass â€¦, wÃ¤re ich dafÃ¼r. | Dann halten wir fest, dass â€¦",
    },
)


READING_CASES = (
    {
        "level": "B1", "title": "Avviso: bicicletta e sicurezza",
        "text": "Wegen mehrerer UnfÃ¤lle wird der Fahrradraum vom 3. bis 10. Mai umgebaut. FahrrÃ¤der dÃ¼rfen in dieser Zeit nicht im Treppenhaus abgestellt werden. Bewohnerinnen und Bewohner kÃ¶nnen den provisorischen Stellplatz hinter dem GebÃ¤ude benutzen. Wer einen besonders groÃŸen FahrradanhÃ¤nger hat, soll sich bis Freitag bei der Hausverwaltung melden.",
        "questions": (
            ("Qual Ã¨ il motivo della misura?", "Mehrere UnfÃ¤lle", ("Ein neues Gesetz", "Ein Umzug")),
            ("Che cosa Ã¨ vietato temporaneamente?", "FahrrÃ¤der im Treppenhaus abstellen", ("Mit dem Fahrrad fahren", "Den Stellplatz benutzen")),
            ("Chi deve contattare l'amministrazione?", "Menschen mit einem groÃŸen FahrradanhÃ¤nger", ("Alle Bewohner", "Neue Mieter")),
        ),
    },
    {
        "level": "B2", "title": "Commento: formazione continua",
        "text": "Viele Unternehmen werben damit, lebenslanges Lernen zu fÃ¶rdern. In der Praxis werden Weiterbildungskurse jedoch oft genau dann angeboten, wenn die Arbeitsbelastung besonders hoch ist. Das Problem liegt daher weniger in mangelnder Motivation der BeschÃ¤ftigten als in der Frage, ob Lernen als private Zusatzleistung oder als Teil der Arbeitszeit verstanden wird. Wer Weiterbildung ernst nimmt, muss nicht nur digitale Plattformen bereitstellen, sondern auch Zeitfenster schaffen, in denen Fehler, Fragen und langsames Verstehen erlaubt sind.",
        "questions": (
            ("Qual Ã¨ la tesi centrale dell'autore?", "Weiterbildung braucht auch geschÃ¼tzte Arbeitszeit", ("Digitale Plattformen sind Ã¼berflÃ¼ssig", "BeschÃ¤ftigte sind unmotiviert")),
            ("Che cosa critica il testo?", "Kurse werden bei hoher Arbeitsbelastung angeboten", ("Zu viele Fehler im Unterricht", "Zu wenig Werbung")),
            ("Quale tono ha la frase finale?", "Fordernd und begrÃ¼ndend", ("Ironisch und beleidigend", "Rein beschreibend")),
        ),
    },
)


CONNECTORS = {
    "sequenza": ("zuerst", "danach", "anschlieÃŸend", "schlieÃŸlich"),
    "causa e conseguenza": ("weil", "da", "deshalb", "daher", "folglich"),
    "contrasto": ("aber", "jedoch", "trotzdem", "obwohl", "wÃ¤hrend"),
    "argomentazione": ("einerseits", "andererseits", "zwar", "dennoch", "auÃŸerdem"),
    "registro formale": ("hiermit", "daher", "bezÃ¼glich", "insbesondere", "abschlieÃŸend"),
}


def _default_state() -> dict[str, Any]:
    return {
        "version": 1,
        "profile": {"placement": None, "goal": "B2 pratico", "minutes_per_day": 35},
        "completed_missions": [],
        "mission_notes": {},
        "cards": {},
        "writing": [],
        "speaking": [],
        "exam_history": [],
        "study_days": [],
    }


def _load_state(st: Any) -> dict[str, Any]:
    key = "ddm_fluency_state"
    if key in st.session_state:
        return st.session_state[key]
    state = _default_state()
    try:
        if STORAGE_FILE.exists():
            loaded = json.loads(STORAGE_FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                state.update(loaded)
    except (OSError, json.JSONDecodeError):
        pass
    st.session_state[key] = state
    return state


def _save_state(state: dict[str, Any]) -> bool:
    try:
        STORAGE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except OSError:
        return False


def _touch_study_day(state: dict[str, Any]) -> None:
    today = date.today().isoformat()
    if today not in state["study_days"]:
        state["study_days"].append(today)


def _normalise(text: str) -> str:
    return re.sub(r"[^a-zÃ¤Ã¶Ã¼ÃŸ]", "", text.lower())


def _question_parts(question: dict[str, Any]) -> tuple[str, list[str], str]:
    """Rende interrogabili anche le domande create dalla vecchia banca."""
    if question["type"] == "grammar":
        return question["question"], list(question["options"]), question["answer"]
    item = question["item"]
    if question["type"] == "meaning":
        prompt = f"Che cosa significa **{item['de']}**?"
        return prompt, [option["it"] for option in question["options"]], question["answer"]["it"]
    prompt = f"Completa: il tedesco per **{item['it']}** Ã¨ â€¦"
    return prompt, [option["de"] for option in question["options"]], question["answer"]["de"]


def _unique_questions(question_bank: list[dict[str, Any]], level: str, amount: int, seed: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for question in question_bank:
        if question["level"] == level:
            grouped.setdefault(question["group"], []).append(question)
    chooser = random.Random(seed)
    groups = list(grouped)
    chooser.shuffle(groups)
    return [chooser.choice(grouped[group]) for group in groups[:amount]]


def _all_cards(vocab_by_level: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    for level in LEVELS:
        for index, item in enumerate(vocab_by_level.get(level, [])):
            cards.append({"id": f"{level}-{index}", "level": level, "de": item["de"], "it": item["it"]})
    return cards


def _next_review(card_state: dict[str, Any], correct: bool) -> dict[str, Any]:
    """Piccola versione trasparente dello spaced repetition: 1, 3, 7, 14 â€¦ giorni."""
    repeats = int(card_state.get("repetitions", 0))
    interval = int(card_state.get("interval", 0))
    if correct:
        repeats += 1
        interval = (1, 3, 7, 14, 30, 60)[min(repeats - 1, 5)] if interval == 0 else min(90, max(3, round(interval * 1.7)))
    else:
        repeats = 0
        interval = 1
    return {
        "repetitions": repeats,
        "interval": interval,
        "next_review": (date.today() + timedelta(days=interval)).isoformat(),
        "last_review": date.today().isoformat(),
    }


def _current_mission(state: dict[str, Any]) -> Mission:
    done = set(state["completed_missions"])
    placement = state["profile"].get("placement") or "A1"
    start = LEVELS.index(placement)
    candidates = [m for m in MISSIONS if LEVELS.index(m.level) >= start and m.id not in done]
    return candidates[0] if candidates else MISSIONS[-1]


def _render_overview(st: Any, state: dict[str, Any]) -> None:
    current = _current_mission(state)
    completed = len(state["completed_missions"])
    all_cards = state["cards"]
    due = sum(1 for card in all_cards.values() if card.get("next_review", "9999-12-31") <= date.today().isoformat())
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Missioni concluse", f"{completed}/{len(MISSIONS)}")
    c2.metric("Carte da ripassare", due)
    c3.metric("Produzioni salvate", len(state["writing"]) + len(state["speaking"]))
    c4.metric("Punto di partenza", state["profile"].get("placement") or "da definire")
    st.progress(completed / len(MISSIONS), text="Progresso del percorso comunicativo")

    with st.container(border=True):
        st.subheader(f"Oggi: {current.level} Â· {current.title}")
        st.write(f"**Alla fine saprai:** {current.can_do}")
        st.caption(f"Sessione consigliata: {current.minutes} minuti Â· Grammatica: {current.grammar}")
        left, right = st.columns(2)
        with left:
            st.markdown("**1. Comprendi**")
            st.write(current.input_task)
            st.markdown("**2. Noti la forma**")
            st.write(current.grammar)
        with right:
            st.markdown("**3. Produci**")
            st.write(current.output_task)
            st.markdown("**4. Migliora**")
            st.write(current.challenge)

        with st.form(f"mission_{current.id}"):
            understood = st.checkbox("Ho svolto l'input e so dire quale informazione cercavo.")
            produced = st.checkbox("Ho parlato o scritto senza copiare una risposta pronta.")
            checked = st.checkbox("Ho controllato forma, connettori e comprensibilitÃ .")
            note = st.text_area("Una frase che voglio ricordare", placeholder="Es.: Einerseits spart Homeoffice Zeit, andererseits â€¦")
            submit = st.form_submit_button("Concludi e salva la missione", type="primary", icon=":material/check_circle:")
        if submit:
            if not (understood and produced and checked):
                st.warning("Per segnare una missione servono input, produzione e controllo: sono le tre fasi che costruiscono autonomia.", icon=":material/flag:")
            else:
                if current.id not in state["completed_missions"]:
                    state["completed_missions"].append(current.id)
                if note.strip():
                    state["mission_notes"][current.id] = note.strip()
                _touch_study_day(state)
                _save_state(state)
                st.success("Missione registrata. La prossima volta il percorso ti proporrÃ  il passo successivo.", icon=":material/check_circle:")

    st.subheader("Micro-ripasso: connettori da usare oggi")
    groups = ["sequenza", "causa e conseguenza"] if current.level in ("A1", "A2") else ["contrasto", "argomentazione"]
    for group in groups:
        st.write(f"**{group.capitalize()}:** " + " Â· ".join(CONNECTORS[group]))


def _render_placement(st: Any, state: dict[str, Any], question_bank: list[dict[str, Any]]) -> None:
    st.subheader("Diagnostica iniziale")
    st.write("Non Ã¨ un esame e non certifica un livello. Serve a scegliere un punto di partenza utile: rispondi senza traduttore, poi usa il risultato come ipotesi da verificare nelle prime missioni.")
    if "ddm_placement_questions" not in st.session_state:
        questions: list[dict[str, Any]] = []
        for level in LEVELS:
            questions.extend(_unique_questions(question_bank, level, 4, f"placement-{level}"))
        st.session_state["ddm_placement_questions"] = questions
    questions = st.session_state["ddm_placement_questions"]
    with st.form("placement_form"):
        answers = {}
        for number, question in enumerate(questions, start=1):
            prompt, options, _ = _question_parts(question)
            st.markdown(f"**{number}. [{question['level']}] {prompt}**")
            answers[question["id"]] = st.radio("Scegli una risposta", options, index=None, key=f"placement_answer_{question['id']}", label_visibility="collapsed")
        submitted = st.form_submit_button("Valuta la diagnostica", type="primary", icon=":material/assessment:")
    if submitted:
        correct = sum(answers[q["id"]] == _question_parts(q)[2] for q in questions)
        if correct <= 4:
            level = "A1"
        elif correct <= 8:
            level = "A2"
        elif correct <= 12:
            level = "B1"
        else:
            level = "B2"
        state["profile"]["placement"] = level
        _touch_study_day(state)
        _save_state(state)
        st.success(f"Risultato: **{correct}/16**. Punto di partenza consigliato: **{level}**.", icon=":material/target:")
        st.info("Se le prime due missioni risultano troppo facili o troppo dure, cambia livello liberamente: una diagnostica non sostituisce l'osservazione reale della tua produzione.", icon=":material/info:")


def _render_path(st: Any, state: dict[str, Any]) -> None:
    st.subheader("Percorso A1 â†’ B2")
    st.caption("Ogni blocco chiude un ciclo completo: capisci, osservi, produci, controlli. Non passare oltre perchÃ© hai letto la regola: passa oltre quando sai usarla.")
    done = set(state["completed_missions"])
    for level in LEVELS:
        level_missions = [m for m in MISSIONS if m.level == level]
        number_done = sum(m.id in done for m in level_missions)
        with st.expander(f"{level} Â· {number_done}/{len(level_missions)} missioni concluse", expanded=level == (state["profile"].get("placement") or "A1")):
            for mission in level_missions:
                status = "Completata" if mission.id in done else "Da svolgere"
                with st.container(border=True):
                    st.markdown(f"**{mission.title}** Â· :{'green' if mission.id in done else 'orange'}-badge[{status}]")
                    st.write(mission.can_do)
                    st.caption(f"Lessico: {mission.lexis} Â· circa {mission.minutes} min")
                    st.write(f"**Output:** {mission.output_task}")
                    st.write(f"**Criterio di uscita:** {mission.checkpoint}")
                    if saved := state["mission_notes"].get(mission.id):
                        st.caption(f"La tua frase-ancora: {saved}")


def _render_review(st: Any, state: dict[str, Any], vocab_by_level: dict[str, list[dict[str, str]]]) -> None:
    st.subheader("Ripasso attivo e dilazionato")
    st.write("Prima prova a recuperare la parola senza guardare. Le carte corrette tornano piÃ¹ tardi; quelle incerte tornano domani. Ãˆ il recupero, non la rilettura, a rendere il lessico disponibile quando parli.")
    cards = _all_cards(vocab_by_level)
    known = state["cards"]
    today = date.today().isoformat()
    due = [card for card in cards if known.get(card["id"], {}).get("next_review", "0000-00-00") <= today]
    unseen = [card for card in cards if card["id"] not in known]
    rng = random.Random(today + str(len(known)))
    rng.shuffle(due)
    rng.shuffle(unseen)
    selected = (due + unseen)[:10]
    if not selected:
        st.success("Nessuna carta Ã¨ dovuta oggi. Torna domani o fai una missione di produzione.", icon=":material/event_available:")
        return
    st.caption(f"Sessione: {len(selected)} carte Â· dovute: {len(due)} Â· nuove: {max(0, len(selected) - len(due))}")
    with st.form("review_form"):
        answers: dict[str, str] = {}
        for card in selected:
            st.markdown(f"**[{card['level']}]** Qual Ã¨ il tedesco per: *{card['it']}*?")
            answers[card["id"]] = st.text_input("La tua risposta", key=f"review_input_{card['id']}_{today}", placeholder="Scrivi la parola, meglio con l'articolo", label_visibility="collapsed")
        submitted = st.form_submit_button("Correggi e programma il prossimo ripasso", type="primary", icon=":material/spellcheck:")
    if submitted:
        correct_count = 0
        for card in selected:
            typed = _normalise(answers[card["id"]])
            expected = _normalise(card["de"])
            base_word = _normalise(card["de"].split(" ", 1)[-1])
            correct = typed in {expected, base_word}
            known[card["id"]] = _next_review(known.get(card["id"], {}), correct)
            if correct:
                correct_count += 1
                st.success(f"{card['it']} â†’ **{card['de']}**")
            else:
                st.error(f"{card['it']} â†’ **{card['de']}** Â· scrivila una volta in una frase personale.")
        _touch_study_day(state)
        _save_state(state)
        st.metric("Recupero corretto", f"{correct_count}/{len(selected)}")
        st.caption("Accetta anche la forma senza articolo per non bloccare il flusso; quando puoi, ripeti sempre sostantivo + articolo + plurale.")


def _writing_feedback(text: str, target: str) -> list[str]:
    words = re.findall(r"[A-Za-zÃ„Ã–ÃœÃ¤Ã¶Ã¼ÃŸ]+", text)
    sentences = [piece for piece in re.split(r"[.!?]+", text) if piece.strip()]
    lower = text.lower()
    connector_hits = sum(1 for terms in CONNECTORS.values() for term in terms if re.search(rf"\b{re.escape(term)}\b", lower))
    feedback = [f"Lunghezza: **{len(words)} parole** Â· obiettivo {target}."]
    if len(sentences) < 4:
        feedback.append("Aggiungi paragrafi o frasi: una produzione B1/B2 deve sviluppare idee, non elencarle.")
    else:
        feedback.append(f"Struttura: **{len(sentences)} frasi** rilevate. Ora controlla che ogni paragrafo abbia una funzione precisa.")
    if connector_hits < 3:
        feedback.append("Coesione: usa almeno 3 connettori diversi (per esempio jedoch, deshalb, obwohl, einerseits).")
    else:
        feedback.append(f"Coesione: trovati **{connector_hits}** connettori. Verifica che esprimano davvero il rapporto logico giusto.")
    if not re.search(r"\b(ich|meiner|meines|aus meiner sicht|meines erachtens)\b", lower):
        feedback.append("Per una presa di posizione, rendi esplicita la tua voce: Meines Erachtens â€¦ / Aus meiner Sicht â€¦")
    if not re.search(r"\b(weil|obwohl|dass|wenn)\b", lower):
        feedback.append("Aggiungi almeno una subordinata con weil, obwohl, dass o wenn e ricontrolla il verbo finale.")
    return feedback


def _render_writing(st: Any, state: dict[str, Any]) -> None:
    prompt = st.selectbox("Scegli un compito", WRITING_PROMPTS, format_func=lambda item: f"{item['level']} Â· {item['title']}", key="writing_prompt")
    with st.container(border=True):
        st.caption(f"Lunghezza consigliata: {prompt['words']}")
        st.write(prompt["brief"])
        st.info(prompt["useful"], icon=":material/lightbulb:")
        st.markdown("**Pianifica prima di scrivere:** 1) scopo e destinatario; 2) posizione/richiesta; 3) due dettagli o ragioni; 4) obiezione o alternativa; 5) chiusura operativa.")
    with st.form("writing_form"):
        text = st.text_area("Il tuo testo in tedesco", height=300, placeholder="Scrivi qui una prima versione. Non puntare alla perfezione: punta a un messaggio chiaro e completo.")
        self_check = st.checkbox("Ho riletto cercando: verbo finale nelle subordinate, maiuscole dei sostantivi, registro e richiesta/conclusione.")
        submitted = st.form_submit_button("Analizza e salva la bozza", type="primary", icon=":material/edit_note:")
    if submitted:
        if not text.strip():
            st.warning("Scrivi una bozza: il feedback diventa utile solo su una produzione reale.")
            return
        feedback = _writing_feedback(text, prompt["words"])
        for item in feedback:
            st.write("- " + item)
        state["writing"].append({"date": date.today().isoformat(), "title": prompt["title"], "words": len(re.findall(r"[A-Za-zÃ„Ã–ÃœÃ¤Ã¶Ã¼ÃŸ]+", text)), "checked": self_check, "text": text})
        _touch_study_day(state)
        _save_state(state)
        st.success("Bozza salvata nel portfolio locale. Torna dopo qualche ora e riscrivila: la revisione distanziata fa emergere errori che subito non vedi.", icon=":material/save:")


def _render_speaking(st: Any, state: dict[str, Any]) -> None:
    prompt = st.selectbox("Scegli una situazione", SPEAKING_PROMPTS, format_func=lambda item: f"{item['level']} Â· {item['title']}", key="speaking_prompt")
    with st.container(border=True):
        st.write(f"**Situazione:** {prompt['scenario']}")
        st.write(f"**Obiettivo:** {prompt['goal']}")
        st.info(prompt["moves"], icon=":material/record_voice_over:")
        st.markdown("**Metodo:** prepara 30 secondi, parla per 90â€“120 secondi, riascoltati se puoi, poi ripeti una seconda volta scegliendo due miglioramenti concreti.")
    with st.form("speaking_reflection"):
        interaction = st.checkbox("Ho posto almeno una domanda e ho reagito a una risposta, non ho fatto un monologo.")
        repair = st.checkbox("Quando mi mancava una parola, ho spiegato il concetto in un altro modo invece di fermarmi.")
        structure = st.checkbox("Ho usato connettori e una conclusione/accordo chiaro.")
        fluency = st.select_slider("Quanto sei riuscito/a a restare in tedesco?", options=["meno di 30 s", "30â€“60 s", "1â€“2 min", "oltre 2 min"], value="30â€“60 s")
        note = st.text_input("Una frase da riusare", placeholder="Wenn ich Sie richtig verstehe, â€¦")
        submitted = st.form_submit_button("Registra la pratica orale", type="primary", icon=":material/mic:")
    if submitted:
        state["speaking"].append({"date": date.today().isoformat(), "title": prompt["title"], "interaction": interaction, "repair": repair, "structure": structure, "fluency": fluency, "note": note.strip()})
        _touch_study_day(state)
        _save_state(state)
        score = sum((interaction, repair, structure))
        st.success(f"Pratica registrata: {score}/3 comportamenti comunicativi osservati.", icon=":material/mic:")
        if score < 3:
            st.info("Rifai lo stesso scenario: il secondo giro Ã¨ dove trasformi formule passive in riflessi.", icon=":material/replay:")


def _render_reading(st: Any) -> None:
    case = st.selectbox("Scegli il testo", READING_CASES, format_func=lambda item: f"{item['level']} Â· {item['title']}", key="reading_case")
    st.caption("Primo passaggio: 90 secondi senza dizionario per tesi, scopo e struttura. Secondo passaggio: cerca le prove nel testo.")
    with st.container(border=True):
        st.write(case["text"])
    with st.form("reading_form"):
        answers = []
        for index, (question, answer, wrong) in enumerate(case["questions"]):
            answers.append(st.radio(question, [answer, *wrong], index=None, key=f"reading_{case['title']}_{index}"))
        submitted = st.form_submit_button("Correggi la comprensione", type="primary", icon=":material/menu_book:")
    if submitted:
        score = sum(given == item[1] for given, item in zip(answers, case["questions"]))
        st.metric("Comprensione", f"{score}/{len(case['questions'])}")
        for given, item in zip(answers, case["questions"]):
            if given != item[1]:
                st.info(f"Rileggi la frase che prova questa risposta: **{item[1]}**.")


def _render_production(st: Any, state: dict[str, Any]) -> None:
    mode = st.segmented_control("Scegli l'abilitÃ  da allenare", ["Scrittura", "Parlato", "Lettura critica"], default="Scrittura", required=True, key="production_mode", width="stretch")
    if mode == "Scrittura":
        _render_writing(st, state)
    elif mode == "Parlato":
        _render_speaking(st, state)
    else:
        _render_reading(st)


def _render_b2_mock(st: Any, state: dict[str, Any], question_bank: list[dict[str, Any]]) -> None:
    st.subheader("Mini-simulazione B2")
    st.write("Questa Ã¨ una simulazione didattica, non un esame ufficiale. Allena le quattro competenze valutate nel Goethe-Zertifikat B2: Lesen, HÃ¶ren, Schreiben e Sprechen.")
    st.link_button("Vedi struttura e materiali ufficiali Goethe B2", "https://www.goethe.de/en/spr/prf/ueb/pb2.html", icon=":material/open_in_new:")
    st.info("Per un B2 operativo non basta scegliere risposte corrette: devi comprendere testi complessi, parlare con scioltezza, sostenere una posizione e scrivere in un registro appropriato.", icon=":material/psychology:")
    if "ddm_b2_mock" not in st.session_state:
        st.session_state["ddm_b2_mock"] = _unique_questions(question_bank, "B2", 10, "b2-mini-mock")
    questions = st.session_state["ddm_b2_mock"]
    with st.expander("1. Lesen Â· 12 minuti", expanded=True):
        st.write("Usa anche il testo B2 nella sezione 'Lettura critica'. Qui controlli lessico e grammatica in contesto.")
        with st.form("b2_mock_form"):
            answers: dict[str, str | None] = {}
            for number, question in enumerate(questions, start=1):
                prompt, options, _ = _question_parts(question)
                st.markdown(f"**{number}. {prompt}**")
                answers[question["id"]] = st.radio("Risposta", options, index=None, key=f"mock_{question['id']}", label_visibility="collapsed")
            submitted = st.form_submit_button("Correggi parte di lettura", type="primary", icon=":material/fact_check:")
        if submitted:
            score = sum(answers[q["id"]] == _question_parts(q)[2] for q in questions)
            state["exam_history"].append({"date": date.today().isoformat(), "reading_score": score, "total": len(questions)})
            _touch_study_day(state)
            _save_state(state)
            st.metric("Parte oggettiva", f"{score}/{len(questions)}")
            if score < 7:
                st.warning("Rivedi gli errori per argomento e ripeti il ripasso attivo. Non usare il punteggio come etichetta del tuo livello.")
            else:
                st.success("Buona base oggettiva: ora verifica che scrittura e parlato siano altrettanto solidi.")
    with st.expander("2. HÃ¶ren Â· allenamento concreto"):
        st.write("Usa i testi e gli esempi audio del corso per ascoltare una sola volta senza leggere; poi annota tesi, due dettagli e atteggiamento del parlante. Infine confronta la trascrizione. Per materiale d'esame, usa i file ufficiali nel link sopra.")
        st.markdown("**Griglia:** ho capito (a) tema e intenzione, (b) due dettagli verificabili, (c) accordo/disaccordo o tono?")
    with st.expander("3. Schreiben Â· 35 minuti"):
        st.write("Scegli una traccia B2 nel Laboratorio di produzione. Prima pianifica 5 minuti; poi produci un testo con scopo, struttura, lessico pertinente, coesione e registro. Rivedi separatamente contenuto e forma.")
        st.markdown("**Autovalutazione B2:** posizione chiara Â· ragioni sviluppate Â· esempio pertinente Â· concessione/controargomento Â· richiesta o conclusione operativa Â· errori che non impediscono la comprensione.")
    with st.expander("4. Sprechen Â· 15 minuti"):
        st.write("Usa una situazione B2 nel Laboratorio. Prepara una presentazione breve, rispondi a un'obiezione e cerca un accordo. Se hai un partner, alternatevi nei ruoli; se sei solo, registra due versioni.")
        st.markdown("**Autovalutazione B2:** parlo senza leggere Â· collego le idee Â· reagisco Â· chiarisco fraintendimenti Â· sintetizzo un accordo.")


def _render_settings(st: Any, state: dict[str, Any]) -> None:
    st.subheader("Obiettivo e dati")
    with st.form("goal_form"):
        goal = st.selectbox("Obiettivo", ["B2 pratico", "Vivere in Germania", "Lavorare in tedesco", "Preparare Goethe B2"], index=["B2 pratico", "Vivere in Germania", "Lavorare in tedesco", "Preparare Goethe B2"].index(state["profile"].get("goal", "B2 pratico")))
        minutes = st.slider("Minuti realistici al giorno", 15, 90, int(state["profile"].get("minutes_per_day", 35)), step=5)
        submitted = st.form_submit_button("Salva obiettivo", type="primary", icon=":material/save:")
    if submitted:
        state["profile"].update({"goal": goal, "minutes_per_day": minutes})
        _save_state(state)
        st.success("Obiettivo salvato localmente.", icon=":material/save:")
    export = json.dumps(state, ensure_ascii=False, indent=2)
    st.download_button("Esporta i tuoi progressi", export, file_name="der_deutsche_meister_progressi.json", mime="application/json", icon=":material/download:")
    st.caption("I dati restano nel file locale learner_progress.json accanto all'app; non vengono inviati a servizi esterni.")


def render_fluency_lab(st: Any, question_bank: list[dict[str, Any]], vocab_by_level: dict[str, list[dict[str, str]]]) -> None:
    """Entry point chiamato da app.py; lo stato Ã¨ per utente e viene anche salvato localmente."""
    state = _load_state(st)
    st.title("Laboratorio di padronanza")
    st.caption("Un percorso per passare dal 'riconoscere una regola' al capire, rispondere, scrivere, negoziare e autocorreggersi in tedesco.")
    _render_overview(st, state)
    page = st.segmented_control(
        "Area del laboratorio",
        ["Oggi", "Diagnostica", "Percorso", "Ripasso", "Produzione", "Simulazione B2", "Obiettivo"],
        default="Oggi",
        required=True,
        key="fluency_lab_page",
        width="stretch",
        persist_state="session",
    )
    if page == "Oggi":
        return
    if page == "Diagnostica":
        _render_placement(st, state, question_bank)
    elif page == "Percorso":
        _render_path(st, state)
    elif page == "Ripasso":
        _render_review(st, state, vocab_by_level)
    elif page == "Produzione":
        _render_production(st, state)
    elif page == "Simulazione B2":
        _render_b2_mock(st, state, question_bank)
    else:
        _render_settings(st, state)



# ---------------------------------------------------------------------------
# Rilevamento tema (light / dark) per CSS adattivo
# ---------------------------------------------------------------------------
try:
    _theme_base = st.get_option("theme.base")
except Exception:
    _theme_base = "light"
IS_DARK = _theme_base == "dark"

# Palette adattiva
C = {
    "app_bg": "#0e1117" if IS_DARK else "#f6f8fc",
    "text": "#fafafa" if IS_DARK else "#152033",
    "card_bg": "#1e1e1e" if IS_DARK else "#ffffff",
    "card_border": "#2d2d2d" if IS_DARK else "#e3e9f2",
    "note_bg": "#1a2332" if IS_DARK else "#edf8ff",
    "note_border": "#2a3a4a" if IS_DARK else "#cbe8f4",
    "sidebar_bg": "#161616" if IS_DARK else "#ffffff",
    "sidebar_border": "#2d2d2d" if IS_DARK else "#e3e9f2",
    "source": "#a0a8b0" if IS_DARK else "#617186",
    "translation": "#94a3b8" if IS_DARK else "#64748b",
    "term_border": "#3a4a5a" if IS_DARK else "#dce7f0",
    "term_hover_bg": "#1a2a3a" if IS_DARK else "#effbff",
    "term_hover_border": "#0d7c9c",
    "hero_grad": "linear-gradient(118deg,#0a1a2e,#0d4a6a 58%,#085e4e)" if IS_DARK else "linear-gradient(118deg,#112a46,#146c94 58%,#0b8e75)",
}

st.set_page_config(
    page_title="Der Deutsche Meister | A1–B2",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
      .stApp {{ background: {C['app_bg']}; color: {C['text']}; }}
      [data-testid="stSidebar"] {{ background: {C['sidebar_bg']}; border-right: 1px solid {C['sidebar_border']}; }}
      .hero {{ padding: 1.6rem 1.8rem; border-radius: 18px; color: white;
              background: {C['hero_grad']}; margin: .2rem 0 1.25rem; }}
      .hero h1 {{ margin: 0; font-size: 2.05rem; }}
      .hero p {{ margin: .35rem 0 0; opacity: .92; }}
      .card {{ background: {C['card_bg']}; border: 1px solid {C['card_border']}; border-radius: 14px; padding: 1.05rem 1.2rem;
              box-shadow: 0 2px 10px rgba(0,0,0,.08); margin: .65rem 0; color: {C['text']}; }}
      .chapter {{ border-left: 5px solid #168aab; }}
      .chapter h3 {{ margin: 0 0 .55rem; color: {C['text']}; }}
      .chapter p {{ line-height: 1.62; margin: .25rem 0; }}
      .level {{ display:inline-block; color:#fff; font-weight:750; padding:.2rem .7rem; border-radius:99px; margin-bottom:.55rem; }}
      .A1{{background:#16835b}}.A2{{background:#2563b8}}.B1{{background:#b66308}}.B2{{background:#bd3535}}
      .note {{ background:{C['note_bg']}; border-radius:10px; padding:.75rem 1rem; border:1px solid {C['note_border']}; color: {C['text']}; }}
      .source {{ color:{C['source']}; font-size:.9rem; }}
      .smallcaps {{ color:{C['source']}; text-transform:uppercase; letter-spacing:.06em; font-size:.75rem; font-weight:700; }}
      .mini-table {{ width:100%; border-collapse:collapse; margin:.6rem 0 .4rem; font-size:.92rem; }}
      .mini-table th {{ background:{C['note_bg']}; color:{C['term_hover_border']}; text-align:left; padding:.4rem .6rem; border:1px solid {C['term_border']}; font-weight:700; }}
      .mini-table td {{ padding:.4rem .6rem; border:1px solid {C['term_border']}; color:{C['text']}; }}
      .summary-box {{ font-style:italic; color:{C['translation']}; border-top:1px dashed {C['term_border']}; margin-top:.65rem; padding-top:.5rem; }}

      /* Mobile optimisations */
      @media (max-width: 768px) {{
        .hero {{ padding: 1rem 1.1rem !important; border-radius: 12px; }}
        .hero h1 {{ font-size: 1.45rem !important; }}
        .hero p {{ font-size: 0.95rem; }}
        .card {{ padding: 0.85rem 0.9rem !important; margin: 0.45rem 0 !important; border-radius: 10px; }}
        .chapter h3 {{ font-size: 1.05rem; }}
        .mini-table {{ font-size: .82rem; }}
        .mini-table th, .mini-table td {{ padding: .3rem .4rem; }}
        .level {{ font-size: 0.8rem; padding: .15rem .55rem; }}
        .note {{ padding: .6rem .8rem; }}
      }}

      /* Scrollbar dark mode */
      @media (prefers-color-scheme: dark) {{
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #1e1e1e; }}
        ::-webkit-scrollbar-thumb {{ background: #4a4a4a; border-radius: 4px; }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Accesso: l'app resta bloccata finché non si inserisce la password corretta.
# La lingua è selezionabile già da questa schermata (l'inglese è il default,
# perché non è detto che chi apre l'app sappia l'italiano); la scelta resta
# poi memorizzata anche nelle schermate successive, tramite session_state.
# ---------------------------------------------------------------------------
# ``st.secrets.get`` prova a leggere il file anche quando non esiste: in una
# distribuzione locale pulita questo generava un errore prima della schermata
# di accesso. L'ambiente resta la prima alternativa; un secrets.toml, se
# presente, ha la precedenza.
APP_PASSWORD = os.environ.get("APP_PASSWORD", "lala31")
try:
    APP_PASSWORD = st.secrets["APP_PASSWORD"]
except Exception:  # nessun secrets.toml o chiave non configurata
    pass

LANGUAGES = {"English": "en", "Italiano": "it", "Türkçe": "tr", "Español": "es"}

LOGIN_TEXT = {
    "en": {
        "subtitle": "Restricted access · enter the password to continue",
        "note": "🔒 This application is protected: enter the password to unlock it.",
        "password": "Password",
        "button": "🔓 Unlock",
        "error": "Incorrect password. Try again.",
        "language": "Language",
    },
    "it": {
        "subtitle": "Accesso riservato · inserisci la password per continuare",
        "note": "🔒 Questa applicazione è protetta: inserisci la password per sbloccarla.",
        "password": "Password",
        "button": "🔓 Sblocca",
        "error": "Password errata. Riprova.",
        "language": "Lingua",
    },
    "es": {
        "subtitle": "Acceso restringido · introduce la contraseña para continuar",
        "note": "🔒 Esta aplicación está protegida: introduce la contraseña para desbloquearla.",
        "password": "Contraseña",
        "button": "🔓 Desbloquear",
        "error": "Contraseña incorrecta. Inténtalo de nuevo.",
        "language": "Idioma",
    },
    "tr": {
        "subtitle": "Kısıtlı erişim · devam etmek için şifreyi girin",
        "note": "🔒 Bu uygulama korumalıdır: kilidini açmak için şifreyi girin.",
        "password": "Şifre",
        "button": "🔓 Kilidi Aç",
        "error": "Yanlış şifre. Tekrar deneyin.",
        "language": "Dil",
    },
}


def _rerun() -> None:
    """Riavvia lo script subito dopo il login, compatibile con più versioni di Streamlit."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:  # pragma: no cover - fallback per versioni precedenti di Streamlit
        st.experimental_rerun()


def require_login() -> None:
    """Mostra una schermata di accesso (con selettore lingua) e ferma l'esecuzione finché
    la password non è corretta. La lingua scelta qui resta in session_state ed è quindi
    già impostata per il resto dell'app dopo lo sblocco."""
    if st.session_state.get("authenticated"):
        return
    if "interface_language_choice" not in st.session_state:
        st.session_state["interface_language_choice"] = "English"
    login_lang = LANGUAGES[st.session_state["interface_language_choice"]]
    lt = LOGIN_TEXT[login_lang]
    st.markdown(
        "<section class='hero'><h1>🇩🇪 Der Deutsche Meister</h1>"
        f"<p>{html.escape(lt['subtitle'])}</p></section>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <style>
        .login-wrap {{ max-width: 460px; margin: 0 auto; padding: 0 10px; }}
        @media (max-width: 480px) {{ .login-wrap {{ max-width: 100%; }} }}
        </style>
        <div class="login-wrap">
        """,
        unsafe_allow_html=True,
    )
    st.selectbox(
        "🌐 " + lt["language"],
        list(LANGUAGES.keys()),
        key="interface_language_choice",
    )
    st.markdown(
        f"<div class='note'>{html.escape(lt['note'])}</div>",
        unsafe_allow_html=True,
    )
    with st.form("login_form"):
        password = st.text_input(lt["password"], type="password", label_visibility="visible")
        submitted = st.form_submit_button(lt["button"], type="primary", use_container_width=True)
    if submitted:
        if password == APP_PASSWORD:
            st.session_state["authenticated"] = True
            _rerun()
        else:
            st.error(lt["error"])
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


require_login()


# ---------------------------------------------------------------------------
# Interfaccia localizzata. Il tedesco rimane sempre la lingua-obiettivo.
# ---------------------------------------------------------------------------
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
        "state": "Stato federato", "capital": "Capitale", "region": "Regione", "can_do": "Obiettivo pratico", "theory_rule": "Regola", "theory_why": "Perché funziona così", "theory_history": "Un po' di storia", "theory_tip": "Attenzione", "theory_summary": "In sintesi", "th_example": "Esempio", "th_meaning": "Significato", "th_function": "Funzione", "th_part": "Parte", "th_content": "Contenuto", "th_step": "Passo", "th_focus": "Aspetto", "th_word": "Parola", "th_parts": "Parti", "th_formula": "Formula", "th_question": "Domanda", "th_first_element": "Primo elemento", "th_rest": "Resto della frase", "th_conjunction": "Congiunzione", "th_preposition": "Preposizione", "th_time": "Ora", "th_expression": "Espressione", "th_verb": "Verbo", "test_summary": "40/40 estratti senza ripetizioni", "verb_count": "verbi", "sidebar_summary": "4 corsi × 40 domande · esame integrale × 40", "source_links": "- [Goethe-Institut — livelli A1–C2 e descrittori QCER](https://www.goethe.de/ins/de/it/uun/dln/ger.html)\n- [IHK — formazione linguistica e candidatura professionale](https://events.mnr.ihk.de/b?p=FB426)",
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
        "state": "Federal state", "capital": "Capital", "region": "Region", "can_do": "Practical goal", "theory_rule": "Rule", "theory_why": "Why it works this way", "theory_history": "A bit of history", "theory_tip": "Watch out", "theory_summary": "In summary", "th_example": "Example", "th_meaning": "Meaning", "th_function": "Function", "th_part": "Part", "th_content": "Content", "th_step": "Step", "th_focus": "Focus", "th_word": "Word", "th_parts": "Parts", "th_formula": "Formula", "th_question": "Question", "th_first_element": "First element", "th_rest": "Rest of the sentence", "th_conjunction": "Conjunction", "th_preposition": "Preposition", "th_time": "Time", "th_expression": "Expression", "th_verb": "Verb", "test_summary": "40/40 drawn without repetition", "verb_count": "verbs", "sidebar_summary": "4 courses × 40 questions · integrated exam × 40", "source_links": "- [Goethe-Institut — A1–C2 levels and CEFR descriptors](https://www.goethe.de/ins/de/en/uun/dln/ger.html)\n- [IHK — language training and professional applications](https://events.mnr.ihk.de/b?p=FB426)",
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
        "state": "Estado federado", "capital": "Capital", "region": "Región", "can_do": "Objetivo práctico", "theory_rule": "Regla", "theory_why": "Por qué funciona así", "theory_history": "Un poco de historia", "theory_tip": "Atención", "theory_summary": "En resumen", "th_example": "Ejemplo", "th_meaning": "Significado", "th_function": "Función", "th_part": "Parte", "th_content": "Contenido", "th_step": "Paso", "th_focus": "Aspecto", "th_word": "Palabra", "th_parts": "Partes", "th_formula": "Fórmula", "th_question": "Pregunta", "th_first_element": "Primer elemento", "th_rest": "Resto de la frase", "th_conjunction": "Conjunción", "th_preposition": "Preposición", "th_time": "Hora", "th_expression": "Expresión", "th_verb": "Verbo", "test_summary": "40/40 seleccionadas sin repetición", "verb_count": "verbos", "sidebar_summary": "4 cursos × 40 preguntas · examen integral × 40", "source_links": "- [Goethe-Institut — niveles A1–C2 y descriptores del MCER](https://www.goethe.de/ins/de/es/uun/dln/ger.html)\n- [IHK — formación lingüística y candidatura profesional](https://events.mnr.ihk.de/b?p=FB426)",
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
        "state": "Eyalet", "capital": "Başkent", "region": "Bölge", "can_do": "Pratik hedef", "theory_rule": "Kural", "theory_why": "Neden böyle işler", "theory_history": "Biraz tarih", "theory_tip": "Dikkat", "theory_summary": "Özetle", "th_example": "Örnek", "th_meaning": "Anlam", "th_function": "İşlev", "th_part": "Bölüm", "th_content": "İçerik", "th_step": "Adım", "th_focus": "Odak", "th_word": "Kelime", "th_parts": "Parçalar", "th_formula": "Kalıp", "th_question": "Soru", "th_first_element": "İlk öge", "th_rest": "Cümlenin geri kalanı", "th_conjunction": "Bağlaç", "th_preposition": "Edat", "th_time": "Saat", "th_expression": "İfade", "th_verb": "Fiil", "test_summary": "40/40 soru tekrarsız seçildi", "verb_count": "fiil", "sidebar_summary": "4 kurs × 40 soru · bütünleşik sınav × 40", "source_links": "- [Goethe-Institut — A1–C2 seviyeleri ve CEFR tanımlayıcıları](https://www.goethe.de/ins/de/tr/uun/dln/ger.html)\n- [IHK — dil eğitimi ve meslekî başvuru](https://events.mnr.ihk.de/b?p=FB426)",
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
    # Enciclopedia disciplinare — settori ampliati e nuovi
    "der Auspuff": "die Auspuffe", "die Lichtmaschine": "die Lichtmaschinen", "der Keilriemen": "die Keilriemen",
    "die Achse": "die Achsen", "der Stoßdämpfer": "die Stoßdämpfer", "die Werkstatt": "die Werkstätten",
    "der Schraubenschlüssel": "die Schraubenschlüssel", "die Zange": "die Zangen", "der Schraubenzieher": "die Schraubenzieher",
    "der Hammer": "die Hämmer", "die Schutzbrille": "die Schutzbrillen", "der Helm": "die Helme",
    "die Hydraulik": "—", "der Kolben": "die Kolben", "die Karosserie": "die Karosserien",
    "das Ersatzteil": "die Ersatzteile", "der Router": "die Router", "das WLAN": "—",
    "die Cloud": "—", "die App": "die Apps", "der Browser": "die Browser",
    "die Suchmaschine": "die Suchmaschinen", "der Server": "die Server", "die Software": "—",
    "die Hardware": "—", "der Virus": "die Viren", "die Firewall": "die Firewalls",
    "der USB-Stick": "die USB-Sticks", "der Drucker": "die Drucker", "die E-Mail": "die E-Mails",
    "der Anhang": "die Anhänge", "der Absturz": "die Abstürze", "der Kontinent": "die Kontinente",
    "der Ozean": "die Ozeane", "die Insel": "die Inseln", "die Wüste": "die Wüsten",
    "der Wald": "die Wälder", "die Region": "die Regionen", "der Bezirk": "die Bezirke",
    "die Gemeinde": "die Gemeinden", "der Bürgermeister": "die Bürgermeister", "die Regierung": "die Regierungen",
    "das Parlament": "die Parlamente", "das Gesetz": "die Gesetze", "der Bürger": "die Bürger",
    "die Staatsangehörigkeit": "die Staatsangehörigkeiten", "die Kultur": "die Kulturen", "die Religion": "die Religionen",
    "die Gesellschaft": "die Gesellschaften", "der Frieden": "—", "die Wirtschaft": "die Wirtschaften",
    "der Kreis": "die Kreise", "das Dreieck": "die Dreiecke", "das Quadrat": "die Quadrate",
    "der Winkel": "die Winkel", "der Durchmesser": "die Durchmesser", "der Radius": "die Radien",
    "der Umfang": "die Umfänge", "das Volumen": "die Volumina", "die Formel": "die Formeln",
    "der Durchschnitt": "die Durchschnitte", "die Statistik": "die Statistiken", "die Wahrscheinlichkeit": "die Wahrscheinlichkeiten",
    "das Experiment": "die Experimente", "die Energie": "die Energien", "die Kraft": "die Kräfte",
    "die Masse": "die Massen", "die Chemie": "—", "die Physik": "—",
    "die Nase": "die Nasen", "der Mund": "die Münder", "der Zahn": "die Zähne",
    "das Herz": "die Herzen", "die Lunge": "die Lungen", "der Magen": "die Mägen",
    "die Haut": "die Häute", "das Knie": "die Knie", "der Husten": "—",
    "die Erkältung": "die Erkältungen", "die Allergie": "die Allergien", "die Verletzung": "die Verletzungen",
    "die Impfung": "die Impfungen", "das Medikament": "die Medikamente", "die Tablette": "die Tabletten",
    "die Versicherung": "die Versicherungen", "das Wohnzimmer": "die Wohnzimmer", "das Schlafzimmer": "die Schlafzimmer",
    "das Badezimmer": "die Badezimmer", "der Flur": "die Flure", "der Balkon": "die Balkone",
    "der Keller": "die Keller", "die Tür": "die Türen", "das Fenster": "die Fenster",
    "das Bett": "die Betten", "der Schrank": "die Schränke", "das Sofa": "die Sofas",
    "die Lampe": "die Lampen", "der Kühlschrank": "die Kühlschränke", "die Waschmaschine": "die Waschmaschinen",
    "der Müll": "—", "die Miete": "die Mieten", "der Vermieter": "die Vermieter",
    "das Frühstück": "die Frühstücke", "das Mittagessen": "die Mittagessen", "das Abendessen": "die Abendessen",
    "die Butter": "—", "der Käse": "—", "die Milch": "—",
    "das Ei": "die Eier", "das Gemüse": "—", "das Obst": "—",
    "das Fleisch": "—", "der Fisch": "die Fische", "der Reis": "—",
    "die Suppe": "die Suppen", "der Zucker": "—", "das Salz": "—",
    "der Pfeffer": "—", "das Öl": "die Öle", "der Topf": "die Töpfe",
    "die Pfanne": "die Pfannen", "das Messer": "die Messer", "die Gabel": "die Gabeln",
    "der Löffel": "die Löffel", "der Teller": "die Teller", "das Glas": "die Gläser",
    "der Geschmack": "die Geschmäcker", "der Bus": "die Busse", "die Bahn": "die Bahnen",
    "die U-Bahn": "die U-Bahnen", "die Straßenbahn": "die Straßenbahnen", "das Fahrrad": "die Fahrräder",
    "die Haltestelle": "die Haltestellen", "das Gleis": "die Gleise", "der Fahrplan": "die Fahrpläne",
    "der Fahrschein": "die Fahrscheine", "die Verspätung": "die Verspätungen", "der Führerschein": "die Führerscheine",
    "die Ampel": "die Ampeln", "die Kreuzung": "die Kreuzungen", "der Parkplatz": "die Parkplätze",
    "der Stau": "die Staus", "die Autobahn": "die Autobahnen", "der Flughafen": "die Flughäfen",
    "das Flugzeug": "die Flugzeuge", "das Ticket": "die Tickets", "der Koffer": "die Koffer",
    "der Arbeitgeber": "die Arbeitgeber", "der Arbeitnehmer": "die Arbeitnehmer", "der Chef": "die Chefs",
    "das Büro": "die Büros", "der Vertrag": "die Verträge", "das Gehalt": "die Gehälter",
    "die Kündigung": "die Kündigungen", "der Urlaub": "die Urlaube", "die Überstunde": "die Überstunden",
    "das Amt": "die Ämter", "das Finanzamt": "die Finanzämter", "die Anmeldung": "die Anmeldungen",
    "der Antrag": "die Anträge", "das Formular": "die Formulare", "die Unterschrift": "die Unterschriften",
    "der Ausweis": "die Ausweise", "der Reisepass": "die Reisepässe", "die Steuer": "die Steuern",
    "die Frist": "die Fristen", "die Rente": "die Renten", "die Behörde": "die Behörden",
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
        speech_word = html.escape(json.dumps(item["de"] if not plural or plural == "—" else f"{item['de']}. {plural}"))
        cells.append(
            f'<button class="term" onclick="say({speech_word}, this)" title="{html.escape(tx("pronunciation"))}">'
            f'<span class="de">{word} <b>🔊</b></span><span class="translation">{detail}</span></button>'
        )
    rows = max(1, (len(items) + columns - 1) // columns)
    row_height = 92
    component = f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
      *{{box-sizing:border-box}} body{{margin:0;padding:6px;font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:{'#0e1117' if IS_DARK else '#f6f8fc'};color:{'#fafafa' if IS_DARK else '#152033'}}}
      .grid{{display:grid;grid-template-columns:repeat({columns},minmax(0,1fr));gap:10px}}
      .term{{border:1px solid {'#3a4a5a' if IS_DARK else '#dce7f0'};border-radius:12px;background:{'#1e1e1e' if IS_DARK else '#fff'};padding:14px 12px;text-align:left;cursor:pointer;min-height:76px;touch-action:manipulation;-webkit-tap-highlight-color:transparent;transition:all .15s ease}}
      .term:hover{{border-color:#0d7c9c;background:{'#1a2a3a' if IS_DARK else '#effbff'};transform:translateY(-1px)}}
      .term:active{{transform:scale(0.98)}}
      .de{{display:block;font-weight:750;color:{'#e2e8f0' if IS_DARK else '#12365d'};font-size:15px;line-height:1.35}} .translation{{display:block;color:{'#94a3b8' if IS_DARK else '#64748b'};font-size:13px;margin-top:6px;line-height:1.4}}
      @media(max-width:768px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}} .term{{padding:16px 12px;min-height:80px;border-radius:10px}} .de{{font-size:16px}} .translation{{font-size:14px}}}}
      @media(max-width:480px){{.grid{{grid-template-columns:repeat(1,minmax(0,1fr))}} .term{{padding:18px 14px;min-height:88px}} .de{{font-size:17px}} .translation{{font-size:15px}}}}
      @media(min-width:1200px){{.grid{{grid-template-columns:repeat({min(columns, 6)},minmax(0,1fr))}}}}
    </style></head><body><div class="grid">{''.join(cells)}</div>
    <script>
      function germanVoice() {{
        const voices = speechSynthesis.getVoices();
        return voices.find(v => v.lang.toLowerCase().startsWith('de')) || voices.find(v => v.lang.toLowerCase().includes('de')) || null;
      }}
      function say(word, button) {{
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(word);
        u.lang = 'de-DE'; u.rate = .78; u.pitch = 1;
        const voice = germanVoice(); if (voice) u.voice = voice;
        const original = button.innerHTML;
        u.onstart = () => {{ button.style.borderColor = '#0d7c9c'; }};
        u.onend = () => {{ button.style.borderColor = ''; button.innerHTML = original; }};
        u.onerror = () => {{ button.style.borderColor = ''; button.innerHTML = original; }};
        button.innerHTML = button.innerHTML.replace('🔊', '🔉');
        window.speechSynthesis.speak(u);
      }}
      if (speechSynthesis.onvoiceschanged !== undefined) {{
        speechSynthesis.onvoiceschanged = () => germanVoice();
      }}
    </script>
    </body></html>"""
    components.html(component, height=max(120, rows * row_height + 16), scrolling=False)


def speakable_verb_table(verbs: list[dict], language: str) -> None:
    """Tabella HTML unica per il glossario verbi: Infinitiv, Präsens, Präteritum,
    Partizip II e Aux. sono tutti pulsanti SpeechSynthesis cliccabili (sono tedesco).
    Solo la colonna del significato, nella lingua dell'app, resta testo semplice:
    non ha senso far "pronunciare" italiano/spagnolo/turco/inglese come se fosse tedesco."""
    de_columns = [
        ("de", "Infinitiv"), ("present", "Präsens (er/sie/es)"),
        ("preterite", "Präteritum"), ("participle", "Partizip II"), ("aux", "Aux."),
    ]
    header_cells = "".join(f"<th>{html.escape(label)}</th>" for _, label in de_columns) + f"<th>{html.escape(tx('meaning'))}</th>"

    body_rows = []
    for v in verbs:
        cells = []
        for key, _ in de_columns:
            word = html.escape(v[key])
            speech = html.escape(json.dumps(v[key]))
            cells.append(
                f'<td><button class="cell-term" onclick="say({speech}, this)" '
                f'title="{html.escape(tx("pronunciation"))}">{word}<b>🔊</b></button></td>'
            )
        cells.append(f'<td class="meaning">{html.escape(tr(v, language))}</td>')
        body_rows.append(f"<tr>{''.join(cells)}</tr>")

    component = f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
      *{{box-sizing:border-box}}
      body{{margin:0;padding:2px;font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:{'#0e1117' if IS_DARK else '#f6f8fc'};color:{'#fafafa' if IS_DARK else '#152033'}}}
      .tbl-wrap{{overflow-x:auto;border:1px solid {'#3a4a5a' if IS_DARK else '#dce7f0'};border-radius:12px}}
      table{{border-collapse:collapse;width:100%;font-size:13.5px}}
      th{{background:{'#1a2230' if IS_DARK else '#eef4fa'};color:{'#cbd5e1' if IS_DARK else '#33475b'};text-align:left;padding:10px 12px;font-weight:700;white-space:nowrap;border-bottom:1px solid {'#3a4a5a' if IS_DARK else '#dce7f0'}}}
      td{{padding:3px 4px;border-bottom:1px solid {'#26313f' if IS_DARK else '#eef2f6'};white-space:nowrap}}
      tr:last-child td{{border-bottom:0}}
      tr:hover td{{background:{'#161d27' if IS_DARK else '#f8fbfd'}}}
      .cell-term{{border:0;background:transparent;cursor:pointer;padding:8px 10px;border-radius:8px;font:inherit;font-weight:600;color:{'#e2e8f0' if IS_DARK else '#12365d'};touch-action:manipulation;-webkit-tap-highlight-color:transparent;white-space:nowrap}}
      .cell-term:hover, .cell-term:focus-visible{{background:{'#1e3a4a' if IS_DARK else '#e3f3fb'};color:#0d7c9c}}
      .cell-term b{{font-weight:400;opacity:.6;margin-left:4px;font-size:11px}}
      td.meaning{{padding:3px 12px;color:{'#94a3b8' if IS_DARK else '#64748b'}}}
      @media(max-width:600px){{table{{font-size:12.5px}} .cell-term{{padding:9px 8px}}}}
    </style></head><body>
    <div class="tbl-wrap"><table>
      <thead><tr>{header_cells}</tr></thead>
      <tbody>{''.join(body_rows)}</tbody>
    </table></div>
    <script>
      function germanVoice() {{
        const voices = speechSynthesis.getVoices();
        return voices.find(v => v.lang.toLowerCase().startsWith('de')) || voices.find(v => v.lang.toLowerCase().includes('de')) || null;
      }}
      function say(word, el) {{
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(word);
        u.lang = 'de-DE'; u.rate = .78; u.pitch = 1;
        const voice = germanVoice(); if (voice) u.voice = voice;
        el.style.color = '#0d7c9c';
        u.onend = () => {{ el.style.color = ''; }};
        u.onerror = () => {{ el.style.color = ''; }};
        window.speechSynthesis.speak(u);
      }}
      if (speechSynthesis.onvoiceschanged !== undefined) {{
        speechSynthesis.onvoiceschanged = () => germanVoice();
      }}
    </script>
    </body></html>"""
    row_height = 44
    height = 50 + len(verbs) * row_height + 12
    components.html(component, height=height, scrolling=False)


# ---------------------------------------------------------------------------
# Percorso: spiegazioni nate per ciascuna lingua di app, con esempi tedeschi.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Explanation:
    """Una spiegazione teorica in 4 parti, uguali per ogni argomento e ogni lingua:
    la regola, il motivo per cui funziona così, un cenno storico/di origine, un avvertimento pratico."""
    rule: str
    why: str
    history: str
    tip: str
    summary: str


@dataclass(frozen=True)
class Topic:
    title: str
    it: Explanation
    en: Explanation
    es: Explanation
    tr: Explanation
    examples: tuple[str, ...]
    table_headers: tuple[str, ...]
    table_rows: tuple[tuple[str, ...], ...]


COURSES: dict[str, dict] = {
    "A1": {
        "colour": "A1",
        "title": {"it": "Fondamenta e vita quotidiana", "en": "Foundations and daily life", "es": "Fundamentos y vida cotidiana", "tr": "Temeller ve günlük yaşam"},
        "can": {"it": "Presentarti, capire istruzioni semplici e gestire scambi quotidiani brevi.", "en": "Introduce yourself, understand simple instructions and manage short everyday exchanges.", "es": "Presentarte, entender instrucciones sencillas y resolver intercambios cotidianos breves.", "tr": "Kendini tanıtmak, basit yönergeleri anlamak ve kısa günlük konuşmaları yürütmek."},
        "topics": [
            Topic(
                "1 · La frase principale",
                Explanation(
                    rule="Nella frase principale tedesca il verbo coniugato occupa sempre la seconda posizione logica (non necessariamente la seconda parola): il primo posto può contenere il soggetto, ma anche un'indicazione di tempo, luogo o modo. Se sposti in avanti qualcos'altro, il soggetto scivola subito dopo il verbo.",
                    why="Questa regola dà al tedesco un punto fisso da cui orientarsi: chi ascolta sa già, dopo la prima informazione, dove trovare il verbo e può prevedere il resto della frase. È anche il motivo per cui puoi mettere in evidenza un elemento (oggi, in ufficio, con piacere) senza scardinare la struttura: basta spostarlo davanti e il verbo resta comunque al suo posto.",
                    history="L'ordine verbo-seconda posizione (V2) è un tratto ereditato dal proto-germanico e condiviso con l'olandese; anche l'inglese antico lo possedeva, ma l'inglese moderno lo ha quasi perso, conservandone tracce solo in frasi letterarie come «Never have I seen…». Il tedesco lo ha invece mantenuto come regola sistematica.",
                    tip="L'errore più comune di chi parla italiano è contare la seconda posizione come seconda parola anziché come secondo elemento logico: in «Heute lerne ich Deutsch», «heute» occupa da solo il primo posto, quindi «lerne» resta il secondo elemento anche se la frase ha già più parole prima del soggetto.",
                    summary="Il verbo coniugato è sempre al secondo posto logico: sposta pure altri elementi in testa, lui resta lì.",
                ),
                Explanation(
                    rule="In a German main clause, the conjugated verb always takes the second logical slot (not necessarily the second word). The first slot can hold the subject, but also a time, place or manner expression; whatever else you move to the front, the subject slides to right after the verb.",
                    why="This rule gives German a fixed anchor point: as soon as the listener hears the first piece of information, they already know where the verb will appear and can predict the rest of the sentence. It also means you can highlight an element (today, at the office, gladly) simply by moving it to the front - the verb stays exactly where it belongs.",
                    history="Verb-second (V2) order is inherited from Proto-Germanic and shared with Dutch. Old English had it too, and faint traces survive in literary inversions like «Never have I seen…», but Modern English largely lost it, while German kept it as a systematic rule.",
                    tip="The most common mistake for learners is treating «second» as the second word rather than the second logical element: in «Heute lerne ich Deutsch», «heute» alone fills the first slot, so «lerne» is still the second element even though several words now precede the subject.",
                    summary="The conjugated verb always sits in the second logical slot: move other elements to the front, it stays put.",
                ),
                Explanation(
                    rule="En la oración principal alemana, el verbo conjugado ocupa siempre la segunda posición lógica (no necesariamente la segunda palabra): el primer lugar puede llevar el sujeto, pero también una indicación de tiempo, lugar o modo. Si adelantas otra cosa, el sujeto pasa justo detrás del verbo.",
                    why="Esta regla da al alemán un punto fijo de referencia: en cuanto el oyente recibe la primera información, ya sabe dónde encontrará el verbo y puede anticipar el resto de la frase. Por eso también puedes destacar un elemento (hoy, en la oficina, con gusto) con solo adelantarlo: el verbo permanece en su sitio.",
                    history="El orden verbo-segunda posición (V2) se hereda del protogermánico y se comparte con el neerlandés; el inglés antiguo también lo tenía, y quedan huellas en inversiones literarias como «Never have I seen…», pero el inglés moderno lo perdió casi por completo, mientras el alemán lo conservó como regla sistemática.",
                    tip="El error más frecuente de un hispanohablante es contar la segunda posición como segunda palabra y no como segundo elemento lógico: en «Heute lerne ich Deutsch», «heute» ocupa por sí solo el primer lugar, así que «lerne» sigue siendo el segundo elemento aunque ya haya varias palabras antes del sujeto.",
                    summary="El verbo conjugado siempre va en la segunda posición lógica: adelanta otros elementos, él se queda ahí.",
                ),
                Explanation(
                    rule="Almanca ana cümlede çekimli fiil her zaman mantıksal olarak ikinci sıradadır (mutlaka ikinci kelime değil): ilk sırada özne olabilir, ama bir zaman, yer veya tarz ifadesi de olabilir. Başka bir öge öne alındığında özne fiilden hemen sonra gelir.",
                    why="Bu kural Almancaya sabit bir referans noktası verir: dinleyici ilk bilgiyi duyar duymaz fiilin nerede olacağını bilir ve cümlenin geri kalanını tahmin edebilir. Bu yüzden bir ögeyi (bugün, ofiste, memnuniyetle) öne alarak vurgulayabilirsin; fiil yine de yerinde kalır.",
                    history="Fiil-ikinci (V2) sıralaması Proto-Germenceden miras kalmıştır ve Felemenkçeyle paylaşılır; Eski İngilizcede de vardı ve «Never have I seen…» gibi edebi devrik cümlelerde izleri kalmıştır, ama Modern İngilizce bunu büyük ölçüde kaybetmiştir; Almanca ise sistematik bir kural olarak korumuştur.",
                    tip="En sık yapılan hata, ikinci sırayı ikinci kelime olarak değil, ikinci mantıksal öge olarak sayamamaktır: «Heute lerne ich Deutsch» cümlesinde «heute» tek başına ilk sırayı doldurur, bu yüzden özneden önce başka kelimeler olsa da «lerne» hâlâ ikinci ögedir.",
                    summary="Çekimli fiil her zaman mantıksal ikinci sıradadır: başka ögeleri öne alsan da o yerinde kalır.",
                ),
                ("Ich lerne heute Deutsch.", "Heute lerne ich Deutsch."),
                ("th_first_element", "th_verb", "th_rest"),
                (
                    ("Ich", "lerne", "heute Deutsch."),
                    ("Heute", "lerne", "ich Deutsch."),
                    ("Um 9 Uhr", "beginnt", "der Unterricht."),
                ),
            ),
            Topic(
                "2 · Persone, sein e haben",
                Explanation(
                    rule="I pronomi personali (ich, du, er/sie/es, wir, ihr, sie/Sie) accompagnano i due verbi più frequenti del tedesco, sein (essere) e haben (avere), usati per identità, età, provenienza e possesso. Entrambi sono irregolari e vanno imparati come forme intere (ich bin, du bist, er ist…), non ricavati da uno schema.",
                    why="Sein e haben non sono verbi come gli altri: più avanti serviranno anche da ausiliari per costruire altri tempi (lo vedrai con il Perfekt in A2), quindi impararli bene ora, in ogni persona, evita di doverci tornare sopra dopo. Esercita risposte intere («Ich bin Anna, ich komme aus Rom») invece delle sole desinenze isolate: la scioltezza nasce da blocchi completi, non da frammenti.",
                    history="Come il verbo essere in italiano, anche sein è fortemente irregolare (si dice «suppletivo»): i verbi più usati in assoluto in una lingua tendono a restare irregolari nel tempo invece di uniformarsi alla coniugazione regolare, proprio perché li usiamo troppo spesso perché possano «smussarsi».",
                    tip="Attenzione a non confondere il significato di base di sein (essere) con il ruolo che avrà più avanti come ausiliare: per ora concentrati solo sulle sei persone e sull'uso quotidiano, senza anticipare il Perfekt.",
                    summary="sein e haben sono irregolari: vanno imparati a memoria come blocchi interi, persona per persona.",
                ),
                Explanation(
                    rule="Personal pronouns (ich, du, er/sie/es, wir, ihr, sie/Sie) go together with German's two most frequent verbs, sein (to be) and haben (to have), used for identity, age, origin and possession. Both are irregular and must be learned as whole forms (ich bin, du bist, er ist…) rather than derived from a pattern.",
                    why="Sein and haben are not just ordinary verbs: later they will also work as auxiliaries to build other tenses (you'll meet this with the Perfekt in A2), so learning every person solidly now saves you from relearning them later. Practise full answers («Ich bin Anna, ich komme aus Rom») rather than isolated endings - fluency comes from complete chunks, not fragments.",
                    history="Like English «to be», German sein is heavily irregular, or «suppletive» - built from different historical roots for different forms. This is common across languages: the most frequently used verbs tend to stay irregular rather than level out, precisely because we use them too often to let them smooth over.",
                    tip="Don't let the base meaning of sein (to be) blend with its later role as an auxiliary - for now, focus purely on the six persons and their everyday meaning, without jumping ahead to the Perfekt.",
                    summary="sein and haben are irregular: learn them as whole forms, one person at a time.",
                ),
                Explanation(
                    rule="Los pronombres personales (ich, du, er/sie/es, wir, ihr, sie/Sie) acompañan a los dos verbos más frecuentes del alemán, sein (ser/estar) y haben (tener), usados para identidad, edad, procedencia y posesión. Ambos son irregulares y hay que aprenderlos como formas completas (ich bin, du bist, er ist…).",
                    why="Sein y haben no son verbos cualquiera: más adelante funcionarán también como auxiliares para construir otros tiempos (lo verás con el Perfekt en A2), así que aprenderlos bien ahora, en cada persona, evita tener que volver atrás después. Practica respuestas completas («Ich bin Anna, ich komme aus Rom») y no solo terminaciones sueltas: así hablas antes y corriges después.",
                    history="Como el verbo ser/estar en español, sein es muy irregular (se dice «supletivo»): los verbos más usados de una lengua tienden a quedarse irregulares con el tiempo en lugar de uniformarse, precisamente porque se usan demasiado como para «limarse».",
                    tip="Cuidado con mezclar el significado básico de sein (ser/estar) con su papel posterior como auxiliar: por ahora concéntrate solo en las seis personas y su uso cotidiano, sin adelantar el Perfekt.",
                    summary="sein y haben son irregulares: apréndelos como formas completas, persona por persona.",
                ),
                Explanation(
                    rule="Kişi zamirleri (ich, du, er/sie/es, wir, ihr, sie/Sie), Almancanın en sık kullanılan iki fiili olan sein (olmak) ve haben (sahip olmak) ile birlikte kullanılır; kimlik, yaş, köken ve sahiplik için kullanılırlar. İkisi de düzensizdir ve tam biçimleriyle ezberlenmelidir (ich bin, du bist, er ist…).",
                    why="Sein ve haben sıradan fiiller değildir: ileride başka zamanları kurmak için yardımcı fiil olarak da kullanılacaklar (A2'de Perfekt'te göreceksin), bu yüzden şimdi her kişiyi sağlam öğrenmek ileride tekrar dönmeni engeller. Sadece ekleri değil, tam cevapları çalış («Ich bin Anna, ich komme aus Rom») - akıcılık parçalardan değil bütün kalıplardan gelir.",
                    history="İngilizcedeki «to be» gibi, Almancadaki sein de güçlü biçimde düzensizdir (kaynaşık/suppletive denir): bir dilde en sık kullanılan fiiller, düzenli çekime uymak yerine zamanla düzensiz kalma eğilimindedir, çünkü çok sık kullanıldıkları için düzleşmeye fırsat bulamazlar.",
                    tip="Sein'in temel anlamını (olmak) ileride yardımcı fiil olarak üstleneceği rolle karıştırma; şimdilik sadece altı kişiyi ve günlük anlamını öğrenmeye odaklan, Perfekt'i şimdiden düşünme.",
                    summary="sein ve haben düzensizdir: her kişiyi tam biçimiyle, blok hâlinde ezberle.",
                ),
                ("Ich bin neu hier.", "Wir haben heute Unterricht."),
                ("Person", "sein", "haben"),
                (
                    ("ich", "bin", "habe"),
                    ("du", "bist", "hast"),
                    ("er / sie / es", "ist", "hat"),
                    ("wir", "sind", "haben"),
                    ("ihr", "seid", "habt"),
                    ("sie / Sie", "sind", "haben"),
                ),
            ),
            Topic(
                "3 · Articoli e accusativo",
                Explanation(
                    rule="Ogni sostantivo tedesco va imparato insieme al suo articolo (der/die/das) e al plurale, perché il genere non si indovina dal significato. All'accusativo (il caso del complemento oggetto diretto) cambia in modo visibile soprattutto il maschile: der diventa den, ein diventa einen; femminile, neutro e plurale restano identici al nominativo.",
                    why="Il tedesco usa il caso per segnalare chi fa l'azione e chi la subisce, indipendentemente dall'ordine delle parole: per questo puoi dire «Den Kaffee kauft der Mann» spostando l'oggetto davanti senza creare ambiguità, cosa impossibile in italiano senza preposizioni. Riconoscere l'accusativo maschile è il primo passo per capire questo meccanismo.",
                    history="Il tedesco eredita il sistema dei casi dal proto-indoeuropeo, che ne aveva fino a otto; l'italiano lo ha perso quasi ovunque tranne che nei pronomi (io/mi/me), mentre il tedesco lo ha conservato spostandolo dal sostantivo all'articolo: cambia den, non «Kaffeen».",
                    tip="L'errore tipico è dimenticare l'accusativo dopo i verbi transitivi più comuni (kaufen, sehen, haben, brauchen…) e lasciare l'articolo al nominativo: «Ich sehe der Mann» è sbagliato, la forma corretta è «Ich sehe den Mann».",
                    summary="Solo il maschile cambia all'accusativo (der → den): il resto resta identico al nominativo.",
                ),
                Explanation(
                    rule="Every German noun must be learned together with its article (der/die/das) and its plural, since gender cannot be guessed from meaning. In the accusative case (the direct object), the masculine changes visibly: der becomes den, ein becomes einen; feminine, neuter and plural stay identical to the nominative.",
                    why="German uses case to mark who is doing the action and who is receiving it, independently of word order - which is why «Den Kaffee kauft der Mann» can move the object to the front without creating ambiguity, something English can't do without a fixed word order. Recognising the masculine accusative is the first key to this whole mechanism.",
                    history="German inherits its case system from Proto-Indo-European, which had up to eight cases. English lost almost all of them, keeping traces only in pronouns (he/him, she/her), while German kept the system by shifting the marking onto the article rather than the noun itself: den changes, not «coffee-n».",
                    tip="The classic mistake is forgetting the accusative after common transitive verbs (kaufen, sehen, haben, brauchen…) and leaving the article in the nominative: «Ich sehe der Mann» is wrong - the correct form is «Ich sehe den Mann».",
                    summary="Only the masculine changes in the accusative (der → den): everything else matches the nominative.",
                ),
                Explanation(
                    rule="Cada sustantivo alemán debe aprenderse junto con su artículo (der/die/das) y su plural, porque el género no se adivina por el significado. En acusativo (el caso del complemento directo) cambia de forma visible sobre todo el masculino: der pasa a den, ein pasa a einen; femenino, neutro y plural quedan igual que en nominativo.",
                    why="El alemán usa el caso para marcar quién hace la acción y quién la recibe, independientemente del orden de las palabras: por eso se puede decir «Den Kaffee kauft der Mann» adelantando el objeto sin crear ambigüedad, algo que el español no puede hacer sin preposiciones como «a». Reconocer el acusativo masculino es la primera clave de este mecanismo.",
                    history="El alemán hereda el sistema de casos del protoindoeuropeo, que llegó a tener hasta ocho; el español lo perdió casi del todo salvo en los pronombres (yo/me/mí), mientras que el alemán lo conservó desplazándolo del sustantivo al artículo: cambia den, no «Kaffeen».",
                    tip="El error típico es olvidar el acusativo tras los verbos transitivos más comunes (kaufen, sehen, haben, brauchen…) y dejar el artículo en nominativo: «Ich sehe der Mann» es incorrecto; la forma correcta es «Ich sehe den Mann».",
                    summary="Solo el masculino cambia en acusativo (der → den): el resto queda igual que en nominativo.",
                ),
                Explanation(
                    rule="Her Almanca ismin artikeli (der/die/das) ve çoğulu birlikte öğrenilmelidir, çünkü cinsiyet anlamdan tahmin edilemez. Akkusativde (doğrudan nesne hâli) özellikle eril artikel görünür biçimde değişir: der → den, ein → einen; dişil, nötr ve çoğul ise nominatifle aynı kalır.",
                    why="Almanca, kim eylemi yaptığını ve kimin etkilendiğini, kelime sırasından bağımsız olarak hâl ekiyle gösterir: bu yüzden «Den Kaffee kauft der Mann» derken nesneyi öne alabilirsin, hiçbir belirsizlik oluşmaz. Eril akkusativi tanımak bu sistemi çözmenin ilk adımıdır.",
                    history="Almanca, hâl sistemini sekize kadar çıkan Proto-Hint-Avrupa dilinden miras almıştır; İngilizce bunun neredeyse tamamını kaybetmiştir, Almanca ise işaretlemeyi isimden artikele taşıyarak korumuştur: değişen den'dir, isim değil.",
                    tip="Sık yapılan hata, kaufen, sehen, haben, brauchen gibi yaygın geçişli fiillerden sonra akkusativi unutup artikeli nominatifte bırakmaktır: «Ich sehe der Mann» yanlıştır, doğrusu «Ich sehe den Mann»dır.",
                    summary="Yalnızca eril akkusativde değişir (der → den): gerisi nominatifle aynı kalır.",
                ),
                ("Der Mann kauft einen Kaffee.", "Ich sehe die Frau."),
                ("Kasus", "Maskulin", "Feminin", "Neutrum", "Plural"),
                (
                    ("Nominativ", "der", "die", "das", "die"),
                    ("Akkusativ", "den", "die", "das", "die"),
                ),
            ),
            Topic(
                "4 · Negazione e domande",
                Explanation(
                    rule="kein nega un sostantivo che non ha un articolo determinativo (o che avrebbe un articolo indeterminativo): «Ich habe keine Zeit». nicht nega invece un verbo, un aggettivo o una parte precisa della frase: «Ich komme nicht». Le W-Fragen (wo, wann, warum…) chiedono un'informazione specifica; nelle domande sì/no il verbo apre semplicemente la frase.",
                    why="Avere due negazioni diverse permette al tedesco di essere preciso su cosa viene negato: kein dice «zero esemplari di questo nome», mentre nicht può cancellare un intero fatto o solo un dettaglio, a seconda di dove lo metti. Il verbo in prima posizione nelle domande sì/no segnala subito all'ascoltatore che serve una risposta di quel tipo.",
                    history="kein nasce storicamente come forma negativa legata a nicht + ein («non un/una»), diventata nel tempo una parola negativa a sé stante per i sostantivi. Il verbo in prima posizione nelle domande sì/no è la stessa logica del V2 vista nel primo capitolo, applicata al caso in cui non c'è nessun altro elemento prima del verbo.",
                    tip="Errore frequente: usare nicht davanti a un sostantivo senza articolo («Ich habe nicht Zeit» è scorretto). Se il sostantivo non ha già un articolo determinativo, la negazione corretta è quasi sempre kein: «Ich habe keine Zeit».",
                    summary="kein nega un nome senza articolo determinativo; nicht nega tutto il resto (verbo, aggettivo, dettaglio).",
                ),
                Explanation(
                    rule="kein negates a noun with no definite article (or that would otherwise take an indefinite one): «Ich habe keine Zeit». nicht negates a verb, an adjective, or one specific part of the sentence: «Ich komme nicht». W-questions (wo, wann, warum…) ask for a specific piece of information; yes/no questions simply put the verb first.",
                    why="Having two different negation words lets German be precise about what is being negated: kein says «zero instances of this noun», while nicht can cancel an entire fact or just one detail, depending on where you place it. Putting the verb first in yes/no questions immediately signals that a yes/no answer is expected.",
                    history="kein developed historically as a negative form related to nicht + ein («not a/not one»), which over time became its own standalone negative word for nouns. The verb-first pattern in yes/no questions is the same V2 logic from the first chapter, just applied to a case where nothing else precedes the verb.",
                    tip="A common mistake is using nicht before a bare noun («Ich habe nicht Zeit» is incorrect). If the noun has no definite article already, the correct negation is almost always kein: «Ich habe keine Zeit».",
                    summary="kein negates a noun with no definite article; nicht negates everything else (verb, adjective, detail).",
                ),
                Explanation(
                    rule="kein niega un sustantivo que no lleva artículo determinado (o que llevaría uno indeterminado): «Ich habe keine Zeit». nicht niega en cambio un verbo, un adjetivo o una parte concreta de la frase: «Ich komme nicht». Las W-Fragen (wo, wann, warum…) piden una información concreta; en las preguntas de sí/no el verbo simplemente abre la frase.",
                    why="Tener dos negaciones distintas permite al alemán ser preciso sobre qué se niega: kein dice «cero ejemplares de este sustantivo», mientras que nicht puede anular un hecho entero o solo un detalle, según dónde lo coloques. Poner el verbo primero en las preguntas de sí/no avisa de inmediato al oyente de que se espera ese tipo de respuesta.",
                    history="kein surge históricamente como forma negativa ligada a nicht + ein («no un/una»), que con el tiempo se convirtió en una palabra negativa propia para los sustantivos. El verbo en primera posición en las preguntas de sí/no sigue la misma lógica del V2 vista en el primer capítulo.",
                    tip="Error frecuente: usar nicht delante de un sustantivo sin artículo («Ich habe nicht Zeit» es incorrecto). Si el sustantivo no lleva ya un artículo determinado, la negación correcta es casi siempre kein: «Ich habe keine Zeit».",
                    summary="kein niega un nombre sin artículo determinado; nicht niega todo lo demás (verbo, adjetivo, detalle).",
                ),
                Explanation(
                    rule="kein, belirli artikeli olmayan (ya da belirsiz artikel alacak) bir ismi olumsuzlar: «Ich habe keine Zeit». nicht ise bir fiili, bir sıfatı ya da cümlenin belirli bir bölümünü olumsuzlar: «Ich komme nicht». W-soruları (wo, wann, warum…) belirli bir bilgi ister; evet/hayır sorularında ise fiil cümleyi başlatır.",
                    why="İki farklı olumsuzluk biçimine sahip olmak Almancanın neyin olumsuzlandığını netleştirmesini sağlar: kein «bu isimden sıfır tane» der, nicht ise konumuna göre tüm bir olguyu ya da yalnızca bir ayrıntıyı iptal edebilir. Evet/hayır sorularında fiili başa almak, dinleyiciye hemen o tür bir cevap beklendiğini gösterir.",
                    history="kein, tarihsel olarak nicht + ein («bir tane değil») ile ilişkili bir olumsuzluk biçimi olarak doğmuş ve zamanla isimler için kendi başına bir kelime hâline gelmiştir. Evet/hayır sorularındaki fiil-başta düzeni, ilk bölümde gördüğün V2 mantığının aynısıdır.",
                    tip="Sık yapılan hata, artikelsiz bir ismin önünde nicht kullanmaktır («Ich habe nicht Zeit» yanlıştır). İsmin zaten belirli bir artikeli yoksa doğru olumsuzluk neredeyse her zaman kein'dir: «Ich habe keine Zeit».",
                    summary="kein, belirli artikeli olmayan bir ismi olumsuzlar; nicht geri kalan her şeyi (fiil, sıfat, ayrıntı) olumsuzlar.",
                ),
                ("Ich habe keine Zeit.", "Kommst du aus Italien?"),
                ("Kasus", "Maskulin", "Feminin", "Neutrum", "Plural"),
                (
                    ("Nominativ", "kein", "keine", "kein", "keine"),
                    ("Akkusativ", "keinen", "keine", "kein", "keine"),
                ),
            ),
            Topic(
                "5 · Verbi modali e separabili",
                Explanation(
                    rule="Con i verbi modali (können, müssen, wollen, dürfen, sollen, mögen) l'infinito del verbo principale va sempre alla fine della frase. Allo stesso modo, il prefisso dei verbi separabili (einkaufen, aufstehen, anrufen…) si stacca e va alla fine nella frase principale: einkaufen → «Wir kaufen … ein».",
                    why="Il verbo coniugato resta in seconda posizione (come nel primo capitolo) mentre la parte «pesante» di significato si sposta in fondo: questo crea la cosiddetta parentesi verbale, una cornice che il tedesco userà sempre più spesso man mano che le frasi si allungano. Imparare a «sentire» questa cornice fin da ora rende più facile leggere frasi lunghe più avanti.",
                    history="Anche l'inglese ha un fenomeno simile e imparentato: i phrasal verbs come «stand up», «give in», «look up» derivano dalla stessa origine germanica delle particelle separabili tedesche. La differenza è che il tedesco ha reso questo meccanismo una regola sistematica della frase principale, non solo un'abitudine lessicale.",
                    tip="Errore comune: dimenticare il prefisso separabile alla fine della frase, lasciando solo «Wir kaufen am Samstag» (incompleto). Controlla sempre che il prefisso sia arrivato in fondo: «Wir kaufen am Samstag ein».",
                    summary="Il verbo coniugato resta al secondo posto; infinito o prefisso separabile vanno sempre in fondo.",
                ),
                Explanation(
                    rule="With modal verbs (können, müssen, wollen, dürfen, sollen, mögen), the infinitive of the main verb always goes to the end of the sentence. Likewise, the prefix of separable verbs (einkaufen, aufstehen, anrufen…) detaches and moves to the end in a main clause: einkaufen → «Wir kaufen … ein».",
                    why="The conjugated verb stays in second position (as in the first chapter) while the «heavy» part of the meaning moves to the end - this creates the so-called verb bracket, a frame that German uses more and more as sentences grow longer. Learning to «feel» this frame now makes long sentences much easier to read later.",
                    history="English has a related phenomenon, historically connected: phrasal verbs like «stand up», «give in», «look up» come from the same Germanic particle-verb origin as German's separable prefixes. The difference is that German turned this into a systematic rule of main-clause structure, not just a lexical habit.",
                    tip="A common mistake is forgetting the separable prefix at the end of the sentence, leaving only «Wir kaufen am Samstag» (incomplete). Always check that the prefix made it to the end: «Wir kaufen am Samstag ein».",
                    summary="The conjugated verb stays in second place; the infinitive or separable prefix always goes to the end.",
                ),
                Explanation(
                    rule="Con los verbos modales (können, müssen, wollen, dürfen, sollen, mögen), el infinitivo del verbo principal va siempre al final de la frase. Del mismo modo, el prefijo de los verbos separables (einkaufen, aufstehen, anrufen…) se separa y va al final en la oración principal: einkaufen → «Wir kaufen … ein».",
                    why="El verbo conjugado permanece en segunda posición (como en el primer capítulo) mientras la parte «pesada» del significado se desplaza al final: esto crea el llamado marco verbal, que el alemán usa cada vez más a medida que las frases se alargan. Aprender a «sentir» este marco desde ahora facilita mucho leer frases largas más adelante.",
                    history="El español no tiene un fenómeno idéntico, pero el inglés sí guarda uno emparentado históricamente: los phrasal verbs como «stand up», «give in», «look up» vienen del mismo origen germánico que los prefijos separables alemanes. La diferencia es que el alemán convirtió esto en una regla sistemática, no solo en un hábito léxico.",
                    tip="Error común: olvidar el prefijo separable al final de la frase, dejando solo «Wir kaufen am Samstag» (incompleto). Comprueba siempre que el prefijo haya llegado al final: «Wir kaufen am Samstag ein».",
                    summary="El verbo conjugado queda en segunda posición; el infinitivo o el prefijo separable van siempre al final.",
                ),
                Explanation(
                    rule="Modal fiillerle (können, müssen, wollen, dürfen, sollen, mögen) asıl fiilin mastarı her zaman cümlenin sonuna gider. Aynı şekilde, ayrılabilen fiillerin (einkaufen, aufstehen, anrufen…) öneki ana cümlede ayrılır ve sona gider: einkaufen → «Wir kaufen … ein».",
                    why="Çekimli fiil ikinci sırada kalırken (ilk bölümde gördüğün gibi) anlamın «ağır» kısmı sona taşınır: bu, cümleler uzadıkça Almancanın giderek daha sık kullanacağı bir fiil parantezi/çerçeve yapı oluşturur. Bu çerçeveyi şimdiden «hissetmeyi» öğrenmek, uzun cümleleri okumayı çok kolaylaştırır.",
                    history="İngilizcede de tarihsel olarak akraba bir olgu vardır: «stand up», «give in», «look up» gibi phrasal verb'ler, Almancanın ayrılabilen önekleriyle aynı Germen parçacık-fiil kökeninden gelir. Fark şu ki Almanca bunu sistematik bir kural hâline getirmiştir.",
                    tip="Sık yapılan hata, ayrılabilen öneki cümle sonunda unutmaktır; «Wir kaufen am Samstag» (eksik) kalır. Önekin sona ulaştığından her zaman emin ol: «Wir kaufen am Samstag ein».",
                    summary="Çekimli fiil ikinci sırada kalır; mastar ya da ayrılabilen önek her zaman sona gider.",
                ),
                ("Ich kann heute kommen.", "Wir kaufen am Samstag ein."),
                ("Person", "können", "müssen", "wollen"),
                (
                    ("ich", "kann", "muss", "will"),
                    ("du", "kannst", "musst", "willst"),
                    ("er / sie / es", "kann", "muss", "will"),
                ),
            ),
            Topic(
                "6 · Tempo, numeri e routine",
                Explanation(
                    rule="L'unità A1 si chiude con orari, date, numeri, acquisti e routine quotidiana: qui non ci sono nuove regole grammaticali, ma vocabolario pratico da automatizzare. I numeri composti si dicono «unità-e-decina» (einundzwanzig = uno-e-venti); l'ora si esprime spesso con Viertel (quarto) e halb (mezza, riferita alla mezz'ora prima dell'ora indicata).",
                    why="Automatizzare orari, prezzi e date è ciò che permette di gestire in tempo reale conversazioni pratiche (un appuntamento, un acquisto) senza doverle tradurre parola per parola. Conviene ripetere ad alta voce numeri, appuntamenti e prezzi dentro mini-scenari invece di studiare liste isolate: si ricorda meglio ciò che si è «usato» in un contesto.",
                    history="La costruzione einundzwanzig («uno e venti») riflette un ordine più antico, comune a tutte le lingue germaniche: anche l'inglese diceva un tempo «four-and-twenty» (come nella filastrocca «four-and-twenty blackbirds»), prima di regolarizzarsi in «twenty-four». Tedesco e olandese hanno conservato l'ordine arcaico fino a oggi.",
                    tip="Attenzione a halb: «halb acht» non significa «le otto e mezza» come si potrebbe pensare per analogia con l'italiano, ma «le sette e mezza» (mezza verso le otto). È l'errore più comune di chi impara il tedesco partendo dall'italiano.",
                    summary="halb guarda avanti, non indietro: «halb acht» è le sette e mezza, non le otto e mezza.",
                ),
                Explanation(
                    rule="The A1 unit closes with times, dates, numbers, shopping and daily routine: there's no new grammar rule here, just practical vocabulary to make automatic. Compound numbers are said «unit-and-ten» (einundzwanzig = one-and-twenty), and time is often expressed with Viertel (quarter) and halb (half, referring to the half-hour before the stated hour).",
                    why="Making times, prices and dates automatic is what lets you handle real-time practical conversations (an appointment, a purchase) without mentally translating word by word. It helps to say numbers, appointments and prices aloud inside mini-scenarios rather than studying isolated lists - the brain remembers what it has actually «used» in context far better.",
                    history="The construction einundzwanzig («one-and-twenty») reflects an older order shared by all Germanic languages: English used to say «four-and-twenty» too (as in the nursery rhyme «four-and-twenty blackbirds»), before regularising to «twenty-four». German and Dutch kept the older, archaic order right up to today.",
                    tip="Watch out for halb: «halb acht» doesn't mean «half past eight» as one might assume - it means «half past seven» (halfway towards eight). This is one of the most common mistakes for learners of German.",
                    summary="halb looks forward, not back: «halb acht» is half past seven, not half past eight.",
                ),
                Explanation(
                    rule="La unidad A1 se cierra con horas, fechas, números, compras y rutina diaria: aquí no hay ninguna regla gramatical nueva, sino vocabulario práctico que hay que automatizar. Los números compuestos se dicen «unidad-y-decena» (einundzwanzig = uno-y-veinte), y la hora se expresa a menudo con Viertel (cuarto) y halb (media, referida a la media hora antes de la hora indicada).",
                    why="Automatizar horas, precios y fechas es lo que permite gestionar en tiempo real conversaciones prácticas (una cita, una compra) sin traducirlas mentalmente palabra por palabra. Conviene repetir en voz alta números, citas y precios dentro de miniescenarios en vez de estudiar listas sueltas: el cerebro recuerda mejor lo que ha «usado» en un contexto.",
                    history="La construcción einundzwanzig («uno y veinte») refleja un orden más antiguo, común a todas las lenguas germánicas: el inglés también decía antes «four-and-twenty» (como en la canción infantil «four-and-twenty blackbirds»), antes de regularizarse a «twenty-four». El alemán y el neerlandés conservaron ese orden arcaico hasta hoy.",
                    tip="Cuidado con halb: «halb acht» no significa «las ocho y media» como podría pensarse por analogía con el español, sino «las siete y media» (media hacia las ocho). Es el error más frecuente de quien aprende alemán desde una lengua románica.",
                    summary="halb mira hacia delante, no hacia atrás: «halb acht» son las siete y media, no las ocho y media.",
                ),
                Explanation(
                    rule="A1 birimi saatler, tarihler, sayılar, alışveriş ve günlük rutinle kapanır: burada yeni bir dil bilgisi kuralı yok, yalnızca otomatikleştirilmesi gereken pratik bir söz varlığı var. Bileşik sayılar «birlik-ve-onluk» şeklinde söylenir (einundzwanzig = bir-ve-yirmi); saat ise Viertel (çeyrek) ve halb (yarım, belirtilen saatten önceki yarım saati ifade eder) ile anlatılır.",
                    why="Saatleri, fiyatları ve tarihleri otomatikleştirmek, pratik konuşmaları kelime kelime çevirmeden anlık olarak yönetebilmeni sağlar. Sayıları, randevuları ve fiyatları izole listeler yerine küçük senaryolar içinde sesli tekrar etmek daha etkilidir: beyin, bir bağlamda «kullandığı» şeyi çok daha iyi hatırlar.",
                    history="einundzwanzig («bir ve yirmi») yapısı, tüm Germen dillerinde ortak olan daha eski bir düzeni yansıtır: İngilizce de eskiden «four-and-twenty» derdi, sonra «twenty-four»e düzenlileşti. Almanca ve Felemenkçe ise bu eski düzeni günümüze kadar korumuştur.",
                    tip="halb'e dikkat: «halb acht», sekiz buçuk değil, yedi buçuk anlamına gelir (sekize doğru yarım). Bu, Almanca öğrenenlerin en sık yaptığı hatalardan biridir.",
                    summary="halb ileriye bakar, geriye değil: «halb acht» yedi buçuktur, sekiz buçuk değil.",
                ),
                ("Es ist Viertel nach acht.", "Der Termin ist am Montag."),
                ("th_time", "th_expression"),
                (
                    ("08:00", "acht Uhr"),
                    ("08:15", "Viertel nach acht"),
                    ("08:30", "halb neun"),
                    ("08:45", "Viertel vor neun"),
                ),
            ),
            Topic(
                "7 · Possessivi e imperativo",
                Explanation(
                    rule="Gli articoli possessivi (mein, dein, sein, ihr, unser, euer, Ihr/ihr) concordano con la persona che possiede E con il genere/numero della cosa posseduta, non con chi possiede: «sein Buch» (il suo libro, di lui) ma «seine Tasche» (la sua borsa, di lui) - la -e finale dipende dal sostantivo, non dal possessore. L'imperativo si forma togliendo -st dalla forma «du» (du kommst → Komm!), usando la forma «wir»/«Sie» invariata per il plurale/cortesia (Kommen wir!/Kommen Sie!), e aggiungendo -t alla radice per «ihr» (Kommt!).",
                    why="I possessivi funzionano come gli articoli indeterminativi (ein/eine/einen), quindi seguono lo stesso schema di desinenze che hai già imparato con l'accusativo in A1: una volta che sai declinare «ein», sai automaticamente declinare «mein/dein/sein…». L'imperativo, dal canto suo, è la forma più diretta per dare istruzioni, ed è per questo che compare ovunque nella vita reale: cartelli, ricette, istruzioni d'uso.",
                    history="I possessivi tedeschi discendono dagli stessi pronomi personali (mein da mir/mich, dein da dir/dich…) — una parentela ancora visibile foneticamente. L'imperativo è uno dei modi verbali più antichi e conservativi delle lingue indoeuropee: la forma «tu» tende a essere la più semplice e corta in moltissime lingue, perché è il modo verbale più diretto e frequente nella comunicazione quotidiana fin dalle origini.",
                    tip="Attenzione a «euer»: quando si aggiunge una desinenza, la -e- centrale sparisce: «euer» + e (femminile) diventa «eure», non «euere». Per l'imperativo «du», ricorda che i verbi con cambio vocalico e→i/ie lo mantengono anche qui: «du sprichst» → «Sprich!», non «Sprech!».",
                    summary="I possessivi prendono le stesse desinenze di ein; l'imperativo toglie semplicemente la desinenza personale dalla radice del verbo.",
                ),
                Explanation(
                    rule="Possessive articles (mein, dein, sein, ihr, unser, euer, Ihr/ihr) agree with the person who owns something AND with the gender/number of the thing owned, not with the owner: «sein Buch» (his book) but «seine Tasche» (his bag) - the final -e depends on the noun, not on who possesses it. The imperative is formed by dropping -st from the du-form (du kommst → Komm!), using the unchanged wir/Sie form for plural/polite requests (Kommen wir!/Kommen Sie!), and adding -t to the stem for ihr (Kommt!).",
                    why="Possessives work exactly like the indefinite article (ein/eine/einen), so they follow the same ending pattern you already learned with the accusative in A1: once you can decline ein, you can automatically decline mein/dein/sein… The imperative, for its part, is the most direct way to give instructions, which is why it's everywhere in real life: signs, recipes, instruction manuals.",
                    history="German possessives descend from the same personal pronouns (mein from mir/mich, dein from dir/dich…) - a kinship still visible phonetically. The imperative is one of the oldest and most conservative verb moods in Indo-European languages: the 'you'-form tends to be the shortest, simplest form in many languages, because it's the most direct and frequent verb mood in everyday communication.",
                    tip="Watch out for euer: when an ending is added, the middle -e- disappears: euer + e (feminine) becomes eure, not euere. For the du-imperative, remember that verbs with an e→i/ie vowel change keep it here too: du sprichst → Sprich!, not Sprech!.",
                    summary="Possessives take the same endings as ein; the imperative just strips the personal ending from the verb stem.",
                ),
                Explanation(
                    rule="Los artículos posesivos (mein, dein, sein, ihr, unser, euer, Ihr/ihr) concuerdan con la persona que posee Y con el género/número de lo poseído, no con quien posee: «sein Buch» (su libro, de él) pero «seine Tasche» (su bolso, de él) - la -e final depende del sustantivo, no del poseedor. El imperativo se forma quitando -st de la forma du (du kommst → Komm!), usando la forma wir/Sie sin cambios para el plural/cortesía (Kommen wir!/Kommen Sie!), y añadiendo -t a la raíz para ihr (Kommt!).",
                    why="Los posesivos funcionan igual que el artículo indeterminado (ein/eine/einen), así que siguen el mismo esquema de terminaciones que ya aprendiste con el acusativo en A1: en cuanto sabes declinar ein, sabes automáticamente declinar mein/dein/sein… El imperativo, por su parte, es la forma más directa de dar instrucciones, por eso aparece por todas partes en la vida real: carteles, recetas, manuales de instrucciones.",
                    history="Los posesivos alemanes descienden de los mismos pronombres personales (mein de mir/mich, dein de dir/dich…): un parentesco todavía visible fonéticamente. El imperativo es uno de los modos verbales más antiguos y conservadores de las lenguas indoeuropeas: la forma 'tú' tiende a ser la más corta y simple en muchísimas lenguas, porque es el modo verbal más directo y frecuente en la comunicación cotidiana.",
                    tip="Cuidado con euer: al añadir una terminación, la -e- central desaparece: euer + e (femenino) se convierte en eure, no euere. Para el imperativo du, recuerda que los verbos con cambio vocálico e→i/ie lo mantienen también aquí: du sprichst → Sprich!, no Sprech!.",
                    summary="Los posesivos llevan las mismas terminaciones que ein; el imperativo solo quita la terminación personal de la raíz del verbo.",
                ),
                Explanation(
                    rule="İyelik artikelleri (mein, dein, sein, ihr, unser, euer, Ihr/ihr) hem sahibiyle hem de sahip olunan şeyin cinsiyeti/sayısıyla uyum sağlar, sahiple değil: «sein Buch» (onun kitabı) ama «seine Tasche» (onun çantası) - sondaki -e, sahibine değil isme bağlıdır. Emir kipi, du biçiminden -st'nin atılmasıyla (du kommst → Komm!), çoğul/nezaket için değişmeyen wir/Sie biçimiyle (Kommen wir!/Kommen Sie!) ve ihr için gövdeye -t eklenerek (Kommt!) kurulur.",
                    why="İyelikler tıpkı belirsiz artikel (ein/eine/einen) gibi çalışır, bu yüzden A1'de akkusativde öğrendiğin aynı ek düzenini izlerler: ein'i çekmeyi biliyorsan, mein/dein/sein'i de otomatik olarak çekebilirsin. Emir kipi ise talimat vermenin en doğrudan yoludur, bu yüzden gerçek hayatta her yerde karşına çıkar: tabelalar, tarifler, kullanım kılavuzları.",
                    history="Almanca iyelikler aynı kişi zamirlerinden gelir (mein, mir/mich'ten; dein, dir/dich'ten…) - hâlâ sesçe görülebilen bir akrabalık. Emir kipi, Hint-Avrupa dillerinin en eski ve en tutucu kiplerinden biridir: emir kipinin 'sen' biçimi birçok dilde en kısa ve en basit biçim olma eğilimindedir, çünkü gündelik iletişimde en doğrudan ve en sık kullanılan kiptir.",
                    tip="euer'e dikkat: bir ek eklendiğinde ortadaki -e- düşer: euer + e (dişil) eure olur, euere değil. du-emir kipinde, e→i/ie ünlü değişimi olan fiillerin bunu burada da koruduğunu unutma: du sprichst → Sprich!, Sprech! değil.",
                    summary="İyelikler ein ile aynı ekleri alır; emir kipi sadece fiil gövdesinden kişi ekini atar.",
                ),
                ("Das ist mein Bruder.", "Kommen Sie bitte herein!"),
                ("Person", "Possessiv", "th_example"),
                (
                    ("ich", "mein", "mein Buch"),
                    ("du", "dein", "dein Buch"),
                    ("er / es", "sein", "sein Buch"),
                    ("sie", "ihr", "ihr Buch"),
                    ("wir", "unser", "unser Buch"),
                    ("ihr", "euer", "euer Buch"),
                ),
            ),
        ],
    },
    "A2": {
        "colour": "A2",
        "title": {"it": "Autonomia nelle situazioni note", "en": "Independence in familiar situations", "es": "Autonomía en situaciones conocidas", "tr": "Bilinen durumlarda bağımsızlık"},
        "can": {"it": "Raccontare esperienze, orientarti, descrivere persone e lavorare con situazioni quotidiane.", "en": "Report experiences, find your way, describe people and handle routine situations.", "es": "Contar experiencias, orientarte, describir personas y manejar situaciones cotidianas.", "tr": "Deneyimleri anlatmak, yön bulmak, insanları betimlemek ve rutin durumları yönetmek."},
        "topics": [
            Topic(
                "1 · Perfekt e biografia",
                Explanation(
                    rule="Il Perfekt racconta il passato nella lingua parlata e informale: si forma con l'ausiliare (haben o sein) coniugato al presente più il Partizip II del verbo principale, che va alla fine della frase. sein si usa con i verbi di movimento o cambiamento di stato (gehen, fahren, werden…); haben con quasi tutti gli altri.",
                    why="Distinguere haben da sein non è arbitrario: sein segnala che il soggetto si è spostato o è cambiato (sono andato, sono diventato), mentre haben segnala un'azione compiuta su qualcosa (ho lavorato, ho mangiato). Riconoscere questa differenza aiuta a scegliere l'ausiliare giusto anche con verbi mai visti prima.",
                    history="Il Perfekt nasce come costruzione risultativa (avere qualcosa in uno stato compiuto) che nel tedesco parlato, specialmente nelle varietà del sud e in austriaco/svizzero, ha quasi sostituito il Präteritum (il passato semplice): è il fenomeno noto come Präteritumschwund. La divisione haben/sein ha un parallelo storico anche in italiano (essere/avere).",
                    tip="Errore frequente: usare sempre haben per abitudine dall'italiano. Controlla sempre se il verbo indica movimento o cambiamento di stato (gehen, kommen, werden, sterben, bleiben…): in quel caso serve sein, anche se in italiano useresti «avere».",
                    summary="Movimento o cambiamento di stato → sein; quasi tutto il resto → haben.",
                ),
                Explanation(
                    rule="The Perfekt tells the past in spoken and informal German: it's built with an auxiliary (haben or sein) conjugated in the present, plus the Partizip II of the main verb, which goes to the end of the sentence. sein is used with verbs of movement or change of state (gehen, fahren, werden…); haben with almost everything else.",
                    why="Choosing haben vs sein isn't arbitrary: sein signals that the subject moved or changed (I have gone, I have become), while haben signals an action performed on something (I have worked, I have eaten). Recognising this difference helps you pick the right auxiliary even for unfamiliar verbs.",
                    history="The Perfekt began as a resultative construction (having something in a completed state) that, in spoken German - especially southern, Austrian and Swiss varieties - has almost entirely replaced the Präteritum (simple past), a development known as Präteritumschwund. The haben/sein split has a historical parallel in Italian (essere/avere) and older English ('I am come').",
                    tip="A common mistake is defaulting to haben out of habit. Always check whether the verb shows movement or change of state (gehen, kommen, werden, sterben, bleiben…): in that case you need sein, even where your own language would use «have».",
                    summary="Movement or change of state → sein; almost everything else → haben.",
                ),
                Explanation(
                    rule="El Perfekt narra el pasado en el alemán hablado e informal: se forma con un auxiliar (haben o sein) conjugado en presente más el Partizip II del verbo principal, que va al final de la frase. sein se usa con verbos de movimiento o cambio de estado (gehen, fahren, werden…); haben con casi todos los demás.",
                    why="Elegir haben o sein no es arbitrario: sein indica que el sujeto se desplazó o cambió (he ido, me he vuelto), mientras que haben indica una acción realizada sobre algo (he trabajado, he comido). Reconocer esta diferencia ayuda a elegir el auxiliar correcto incluso con verbos nuevos.",
                    history="El Perfekt nace como construcción resultativa (tener algo en un estado terminado) que en el alemán hablado, sobre todo en el sur, en Austria y en Suiza, ha sustituido casi por completo al Präteritum (pasado simple): es el fenómeno llamado Präteritumschwund. La división haben/sein tiene un paralelo histórico en el propio español y en el francés antiguo.",
                    tip="Error frecuente: usar siempre haben por costumbre. Comprueba siempre si el verbo indica movimiento o cambio de estado (gehen, kommen, werden, sterben, bleiben…): en ese caso hace falta sein, aunque en español uses «haber».",
                    summary="Movimiento o cambio de estado → sein; casi todo lo demás → haben.",
                ),
                Explanation(
                    rule="Perfekt, konuşma dilinde ve gündelik Almancada geçmişi anlatır: şimdiki zamanda çekimlenmiş bir yardımcı fiil (haben ya da sein) artı cümle sonuna giden asıl fiilin Partizip II biçimiyle kurulur. sein, hareket veya durum değişikliği bildiren fiillerle (gehen, fahren, werden…) kullanılır; haben ise neredeyse geri kalan her şeyle.",
                    why="haben ile sein arasında seçim rastgele değildir: sein öznenin yer değiştirdiğini ya da değiştiğini gösterir (gittim, oldum), haben ise bir şey üzerinde yapılan eylemi gösterir (çalıştım, yedim). Bu farkı görmek, hiç karşılaşmadığın fiillerde bile doğru yardımcı fiili seçmeni sağlar.",
                    history="Perfekt, tamamlanmış bir duruma sahip olma anlamına gelen sonuçsal bir yapı olarak doğmuş, konuşma dilinde -özellikle güney Almanca, Avusturya ve İsviçre Almancasında- Präteritum'un yerini neredeyse tamamen almıştır; buna Präteritumschwund denir. haben/sein ayrımının tarihsel bir benzeri İtalyanca ve eski Fransızcada da vardır.",
                    tip="Sık yapılan hata, alışkanlıkla her zaman haben kullanmaktır. Fiilin hareket ya da durum değişikliği bildirip bildirmediğini her zaman kontrol et (gehen, kommen, werden, sterben, bleiben…): bu durumda kendi dilinde «sahip olmak» desen bile sein gerekir.",
                    summary="Hareket ya da durum değişikliği → sein; geri kalan neredeyse her şey → haben.",
                ),
                ("Ich habe lange gearbeitet.", "Wir sind nach Berlin gefahren."),
                ("th_verb", "Hilfsverb"),
                (
                    ("gehen, kommen, fahren", "sein"),
                    ("werden, bleiben, sterben", "sein"),
                    ("arbeiten, lernen, machen", "haben"),
                    ("essen, kaufen, sehen", "haben"),
                ),
            ),
            Topic(
                "2 · Dativo e accusativo",
                Explanation(
                    rule="Il caso di un sostantivo dipende dalla funzione grammaticale o dalla preposizione che lo regge, non dalla traduzione italiana. Prima individua chi riceve l'azione (dativo, di solito una persona) e che cosa viene trasferito (accusativo); poi scegli articolo e pronome di conseguenza.",
                    why="In italiano l'ordine delle parole basta a capire chi fa cosa a chi; in tedesco è il caso a farlo, quindi puoi anche invertire l'ordine (dem Kind gebe ich den Ball) senza cambiare il senso. Per questo conviene chiedersi «chi riceve?» prima di tradurre parola per parola.",
                    history="Dativo e accusativo derivano entrambi dal sistema dei casi del proto-indoeuropeo (vedi anche l'accusativo di A1): la novità di A2 è che qui il caso dipende anche da singole preposizioni (mit, bei, für, ohne…) che impongono sempre lo stesso caso, un meccanismo molto simile a quello del latino.",
                    tip="Non tradurre parola per parola le preposizioni italiane: für regge sempre l'accusativo, mit sempre il dativo, indipendentemente da come tradurresti la frase. Impara la preposizione insieme al suo caso, come un'unica unità.",
                    summary="Il caso dipende dalla preposizione, non dalla traduzione: für vuole sempre l'accusativo, mit sempre il dativo.",
                ),
                Explanation(
                    rule="The case of a noun depends on its grammatical function or on the preposition governing it, not on a word-for-word translation. First identify who receives the action (dative, usually a person) and what is being transferred (accusative); then choose the article and pronoun accordingly.",
                    why="In English, word order alone usually shows who does what to whom; in German it's the case that does this job, so you can even reverse the order (dem Kind gebe ich den Ball) without changing the meaning. That's why it helps to ask «who receives this?» before translating literally.",
                    history="Dative and accusative both descend from the Proto-Indo-European case system (see also the accusative in A1); what's new at A2 is that case here also depends on specific prepositions (mit, bei, für, ohne…) that always demand the same case - a lexical-government mechanism very similar to Latin.",
                    tip="Don't translate prepositions word for word: für always takes the accusative, mit always the dative, regardless of how you'd phrase it in English. Learn each preposition together with its case, as a single unit.",
                    summary="Case depends on the preposition, not the translation: für always takes the accusative, mit always the dative.",
                ),
                Explanation(
                    rule="El caso de un sustantivo depende de su función gramatical o de la preposición que lo rige, no de una traducción literal. Primero identifica quién recibe la acción (dativo, normalmente una persona) y qué se transfiere (acusativo); luego elige artículo y pronombre en consecuencia.",
                    why="En español el orden de las palabras suele bastar para saber quién hace qué a quién; en alemán es el caso el que cumple esa función, así que incluso puedes invertir el orden (dem Kind gebe ich den Ball) sin cambiar el sentido. Por eso conviene preguntarse '¿quién recibe esto?' antes de traducir palabra por palabra.",
                    history="El dativo y el acusativo derivan ambos del sistema de casos protoindoeuropeo (véase también el acusativo de A1); la novedad de A2 es que el caso también depende de preposiciones concretas (mit, bei, für, ohne…) que exigen siempre el mismo caso, un mecanismo muy parecido al del latín.",
                    tip="No traduzcas las preposiciones palabra por palabra: für rige siempre acusativo, mit siempre dativo, sin importar cómo lo dirías en español. Aprende cada preposición junto con su caso, como una sola unidad.",
                    summary="El caso depende de la preposición, no de la traducción: für rige siempre acusativo, mit siempre dativo.",
                ),
                Explanation(
                    rule="Bir ismin hâli, birebir çeviriye değil dilbilgisel işleve veya onu yöneten edata bağlıdır. Önce eylemi kimin aldığını (dativ, genelde bir kişi) ve neyin aktarıldığını (akkusativ) belirle; sonra artikeli ve zamiri buna göre seç.",
                    why="Türkçede kim kime ne yaptığını genelde ek ve sıralama gösterir; Almancada bunu hâl yapar, bu yüzden sırayı bile tersine çevirebilirsin (dem Kind gebe ich den Ball) ve anlam değişmez. Bu yüzden birebir çevirmeden önce «bunu kim alıyor?» diye sormak işe yarar.",
                    history="Dativ ve akkusativ, ikisi de Proto-Hint-Avrupa hâl sisteminden gelir (A1'deki akkusativ'e de bakın); A2'deki yenilik, hâlin her zaman aynı hâli isteyen belirli edatlara (mit, bei, für, ohne…) da bağlı olmasıdır - Latinceye çok benzeyen sözcüksel bir mekanizma.",
                    tip="Edatları birebir çevirme: für her zaman akkusativ, mit her zaman dativ ister, kendi dilinde nasıl söylediğinden bağımsız olarak. Her edatı hâliyle birlikte, tek bir birim olarak öğren.",
                    summary="Hâl, çeviriye değil edata bağlıdır: für her zaman akkusativ, mit her zaman dativ ister.",
                ),
                ("Ich gebe dem Kind den Ball.", "Das Geschenk ist für meinen Bruder."),
                ("th_preposition", "Kasus", "th_example"),
                (
                    ("für", "Akkusativ", "für den Mann"),
                    ("ohne", "Akkusativ", "ohne Geld"),
                    ("mit", "Dativ", "mit dem Mann"),
                    ("bei", "Dativ", "bei der Arbeit"),
                ),
            ),
            Topic(
                "3 · Spazio e movimento",
                Explanation(
                    rule="Le preposizioni a doppio uso (Wechselpräpositionen: in, an, auf, über, unter, vor, hinter, neben, zwischen) reggono il dativo quando rispondono a Wo? (stato) e l'accusativo quando rispondono a Wohin? (direzione).",
                    why="Questa alternanza permette al tedesco di distinguere con una sola preposizione due significati diversi (stare fermo vs muoversi verso) senza bisogno di verbi diversi: legen (mettere) vs liegen (stare disteso) ne è l'esempio più chiaro.",
                    history="Questa distinzione stato/direzione tramite il caso ha un parallelo diretto nel latino classico, che usava «in + ablativo» per il luogo e «in + accusativo» per la direzione — esattamente lo stesso meccanismo del tedesco, con un'altra coppia di casi.",
                    tip="Non confondere liegen/legen, stehen/stellen, sitzen/setzen: la coppia con vocale diversa segnala stato (dativo) vs movimento (accusativo). «Das Buch liegt auf dem Tisch» è diverso da «Ich lege das Buch auf den Tisch».",
                    summary="Wo? vuole il dativo (stato); Wohin? vuole l'accusativo (direzione) — stessa preposizione, caso diverso.",
                ),
                Explanation(
                    rule="Two-way prepositions (Wechselpräpositionen: in, an, auf, über, unter, vor, hinter, neben, zwischen) take the dative when they answer Wo? (a state) and the accusative when they answer Wohin? (a direction).",
                    why="This alternation lets German distinguish two different meanings (staying still vs. moving towards) with a single preposition - legen (to lay) vs liegen (to lie) is the clearest example.",
                    history="This state/direction distinction marked through case has a direct parallel in Classical Latin, which used «in + ablative» for location and «in + accusative» for direction - exactly the same mechanism as German, with a different case pair.",
                    tip="Don't confuse liegen/legen, stehen/stellen, sitzen/setzen: the pair with the different vowel marks state (dative) vs movement (accusative). «Das Buch liegt auf dem Tisch» differs from «Ich lege das Buch auf den Tisch».",
                    summary="Wo? takes the dative (state); Wohin? takes the accusative (direction) - same preposition, different case.",
                ),
                Explanation(
                    rule="Las preposiciones de doble uso (Wechselpräpositionen: in, an, auf, über, unter, vor, hinter, neben, zwischen) rigen dativo cuando responden a Wo? (un estado) y acusativo cuando responden a Wohin? (una dirección).",
                    why="Esta alternancia permite al alemán distinguir dos significados distintos (estar quieto frente a moverse hacia) con una sola preposición: legen (poner) frente a liegen (estar tumbado) es el ejemplo más claro.",
                    history="Esta distinción entre estado y dirección mediante el caso tiene un paralelo directo en el latín clásico, que usaba «in + ablativo» para el lugar e «in + acusativo» para la dirección: el mismo mecanismo que el alemán, con otro par de casos.",
                    tip="No confundas liegen/legen, stehen/stellen, sitzen/setzen: el par con la vocal distinta marca estado (dativo) frente a movimiento (acusativo). «Das Buch liegt auf dem Tisch» es distinto de «Ich lege das Buch auf den Tisch».",
                    summary="Wo? rige dativo (estado); Wohin? rige acusativo (dirección) — misma preposición, distinto caso.",
                ),
                Explanation(
                    rule="Çift yönlü edatlar (Wechselpräpositionen: in, an, auf, über, unter, vor, hinter, neben, zwischen), Wo? (durum) sorusuna cevap verdiklerinde dativ, Wohin? (yön) sorusuna cevap verdiklerinde akkusativ alır.",
                    why="Bu değişim, Almancanın tek bir edatla iki farklı anlamı (sabit durmak / hareket etmek) ayırt etmesini sağlar: legen (koymak) ile liegen (yatmak) en açık örnektir.",
                    history="Hâl yoluyla yapılan bu durum/yön ayrımının klasik Latincede doğrudan bir benzeri vardır: yer için «in + ablatif», yön için «in + akkusativ» kullanılırdı - Almancadaki mekanizmanın aynısı, başka bir hâl çiftiyle.",
                    tip="liegen/legen, stehen/stellen, sitzen/setzen'i karıştırma: farklı ünlüye sahip çift, durumu (dativ) ile hareketi (akkusativ) ayırt eder. «Das Buch liegt auf dem Tisch» ile «Ich lege das Buch auf den Tisch» farklıdır.",
                    summary="Wo? dativ alır (durum); Wohin? akkusativ alır (yön) — aynı edat, farklı hâl.",
                ),
                ("Das Werkzeug liegt auf dem Tisch.", "Ich lege das Werkzeug auf den Tisch."),
                ("th_preposition", "Wo?", "Wohin?"),
                (
                    ("in", "im Haus", "ins Haus"),
                    ("auf", "auf dem Tisch", "auf den Tisch"),
                    ("an", "an der Wand", "an die Wand"),
                ),
            ),
            Topic(
                "4 · Confrontare e motivare",
                Explanation(
                    rule="Il comparativo si forma aggiungendo -er all'aggettivo (schnell → schneller) e usando als per «di/che»; il superlativo usa am + aggettivo + -sten (am schnellsten). Alcuni aggettivi frequenti sono irregolari (gut → besser → am besten).",
                    why="Confrontare e motivare richiede di collegare sempre il paragone a una ragione concreta: questo è ciò che rende un confronto utile in una conversazione reale, non solo un esercizio grammaticale.",
                    history="Il suffisso comparativo -er e quello superlativo -(e)st risalgono a suffissi molto antichi del proto-germanico, conservati quasi identici in inglese (schneller/faster, schnellst/fastest): uno dei punti in cui tedesco e inglese restano più vicini.",
                    tip="Attenzione agli aggettivi irregolari più comuni: gut/besser/am besten, viel/mehr/am meisten, gern/lieber/am liebsten. Non provare a costruirli regolarmente con -er: vanno memorizzati.",
                    summary="Regolare: -er/am -sten. Ma gut, viel e gern sono irregolari e vanno imparati a memoria.",
                ),
                Explanation(
                    rule="The comparative is formed by adding -er to the adjective (schnell → schneller) and using als for 'than'; the superlative uses am + adjective + -sten (am schnellsten). Some frequent adjectives are irregular (gut → besser → am besten).",
                    why="Comparing and giving reasons means always attaching the comparison to a concrete reason: that's what makes a comparison useful in a real conversation, not just a grammar drill.",
                    history="The comparative suffix -er and superlative -(e)st go back to very old Proto-Germanic suffixes, preserved almost identically in English (schneller/faster, schnellst/fastest): one of the points where German and English stay closest.",
                    tip="Watch out for the most common irregular adjectives: gut/besser/am besten, viel/mehr/am meisten, gern/lieber/am liebsten. Don't try to build them with -er: they must be memorised.",
                    summary="Regular: -er/am -sten. But gut, viel and gern are irregular and must be learned by heart.",
                ),
                Explanation(
                    rule="El comparativo se forma añadiendo -er al adjetivo (schnell → schneller) y usando als para 'que'; el superlativo usa am + adjetivo + -sten (am schnellsten). Algunos adjetivos frecuentes son irregulares (gut → besser → am besten).",
                    why="Comparar y justificar significa unir siempre la comparación a una razón concreta: eso es lo que hace útil una comparación en una conversación real, no solo un ejercicio gramatical.",
                    history="El sufijo comparativo -er y el superlativo -(e)st se remontan a sufijos muy antiguos del protogermánico, conservados casi idénticos en inglés (schneller/faster, schnellst/fastest): uno de los puntos donde alemán e inglés quedan más cerca.",
                    tip="Cuidado con los adjetivos irregulares más comunes: gut/besser/am besten, viel/mehr/am meisten, gern/lieber/am liebsten. No intentes formarlos con -er: hay que memorizarlos.",
                    summary="Regular: -er/am -sten. Pero gut, viel y gern son irregulares y hay que memorizarlos.",
                ),
                Explanation(
                    rule="Karşılaştırma sıfata -er eklenerek (schnell → schneller) ve 'den/dan' için als kullanılarak kurulur; üstünlük derecesi am + sıfat + -sten (am schnellsten) ile yapılır. Bazı sık kullanılan sıfatlar düzensizdir (gut → besser → am besten).",
                    why="Karşılaştırma ve gerekçelendirme, karşılaştırmayı her zaman somut bir nedene bağlamayı gerektirir: gerçek bir konuşmada bir karşılaştırmayı yararlı kılan budur, sadece bir alıştırma değil.",
                    history="Karşılaştırma eki -er ve üstünlük eki -(e)st, İngilizcede neredeyse aynı biçimde korunan (schneller/faster, schnellst/fastest) çok eski Proto-Germen eklerine dayanır: Almanca ve İngilizcenin birbirine en yakın kaldığı noktalardan biri.",
                    tip="En yaygın düzensiz sıfatlara dikkat et: gut/besser/am besten, viel/mehr/am meisten, gern/lieber/am liebsten. Bunları -er ile düzenli kurmaya çalışma: ezberlenmeleri gerekir.",
                    summary="Düzenli: -er/am -sten. Ama gut, viel ve gern düzensizdir ve ezberlenmelidir.",
                ),
                ("Das Auto ist schneller als der Bus.", "Heute ist es am kältesten."),
                ("Positiv", "Komparativ", "Superlativ"),
                (
                    ("schnell", "schneller", "am schnellsten"),
                    ("gut", "besser", "am besten"),
                    ("viel", "mehr", "am meisten"),
                    ("gern", "lieber", "am liebsten"),
                ),
            ),
            Topic(
                "5 · Frasi dipendenti introduttive",
                Explanation(
                    rule="weil (perché), dass (che) e wenn (se/quando) introducono una subordinata in cui il verbo va alla fine, non in seconda posizione. A2 non richiede periodi lunghi: bastano frasi brevi ma con l'ordine corretto.",
                    why="Spostare il verbo alla fine segnala chiaramente che quella parte della frase dipende da un'altra: è un modo per il tedesco di marcare grammaticalmente, non solo con l'intonazione, che un'informazione è subordinata a un'altra.",
                    history="Curiosamente, l'ordine verbo-finale nelle subordinate è il pattern più antico: proto-germanico e proto-indoeuropeo tendevano a mettere il verbo alla fine. È la frase principale tedesca (V2) a essere l'innovazione più recente; le subordinate hanno conservato l'ordine arcaico.",
                    tip="Errore frequente: dimenticare di spostare il verbo alla fine dopo weil o dass. «Ich bleibe zu Hause, weil ich bin krank» è sbagliato; corretto è «weil ich krank bin».",
                    summary="Dopo weil, dass, wenn il verbo salta sempre in fondo alla frase.",
                ),
                Explanation(
                    rule="weil (because), dass (that) and wenn (if/when) introduce a subordinate clause where the verb goes to the end, not into second position. At A2 you don't need long sentences: short clauses with the correct word order are enough.",
                    why="Moving the verb to the end clearly signals that this part of the sentence depends on another: it's German's way of marking, grammatically and not just through intonation, that one piece of information is subordinate to another.",
                    history="Interestingly, verb-final order in subordinate clauses is actually the older pattern: Proto-Germanic and Proto-Indo-European tended to place the verb at the end. It's the German main clause (V2) that is the more recent innovation; subordinate clauses kept the archaic order.",
                    tip="A common mistake is forgetting to move the verb to the end after weil or dass. «Ich bleibe zu Hause, weil ich bin krank» is wrong; the correct form is «weil ich krank bin».",
                    summary="After weil, dass, wenn the verb always jumps to the end of the clause.",
                ),
                Explanation(
                    rule="weil (porque), dass (que) y wenn (si/cuando) introducen una subordinada en la que el verbo va al final, no en segunda posición. En A2 no hacen falta frases largas: bastan subordinadas breves con el orden correcto.",
                    why="Desplazar el verbo al final señala con claridad que esa parte de la frase depende de otra: es la manera que tiene el alemán de marcar gramaticalmente, no solo con la entonación, que una información es subordinada a otra.",
                    history="Curiosamente, el orden verbo final en las subordinadas es el patrón más antiguo: protogermánico y protoindoeuropeo tendían a colocar el verbo al final. Es la oración principal alemana (V2) la que resulta la innovación más reciente.",
                    tip="Error frecuente: olvidar mover el verbo al final después de weil o dass. «Ich bleibe zu Hause, weil ich bin krank» es incorrecto; lo correcto es «weil ich krank bin».",
                    summary="Después de weil, dass, wenn el verbo salta siempre al final de la frase.",
                ),
                Explanation(
                    rule="weil (çünkü), dass (ki/diye) ve wenn (eğer/-dığında), fiilin ikinci sırada değil sonda yer aldığı bir yan cümle başlatır. A2'de uzun cümlelere gerek yok: doğru sıralamayla kısa yan cümleler yeterlidir.",
                    why="Fiili sona taşımak, cümlenin bu bölümünün başka bir bölüme bağlı olduğunu açıkça gösterir: bu, Almancanın bir bilginin başka birine bağlı olduğunu yalnızca tonlamayla değil, dilbilgisel olarak da işaretleme biçimidir.",
                    history="İlginç biçimde, yan cümlelerdeki fiil-sonda düzeni aslında daha eski bir kalıptır: Proto-Germence ve Proto-Hint-Avrupa dili fiili sona koyma eğilimindeydi. Fiilin ikinci sırada olduğu (V2) Almanca ana cümle, daha yeni bir yeniliktir.",
                    tip="Sık yapılan hata, weil ya da dass'tan sonra fiili sona taşımayı unutmaktır. «Ich bleibe zu Hause, weil ich bin krank» yanlıştır; doğrusu «weil ich krank bin»dir.",
                    summary="weil, dass, wenn'den sonra fiil her zaman cümlenin sonuna atlar.",
                ),
                ("Ich bleibe zu Hause, weil ich krank bin.", "Ich weiß, dass er kommt."),
                ("th_conjunction", "th_example"),
                (
                    ("weil", "…, weil ich krank bin."),
                    ("dass", "Ich weiß, dass er kommt."),
                    ("wenn", "…, wenn es regnet."),
                ),
            ),
            Topic(
                "6 · Servizi, lavoro e salute",
                Explanation(
                    rule="Telefonate, appuntamenti, farmacia, lavoro e casa diventano scenari pratici in cui il lessico professionale si combina con formule di cortesia: richiesta (Könnten Sie…?), chiarimento (Was bedeutet…?), conferma (Habe ich das richtig verstanden?).",
                    why="In situazioni di servizio reali la cortesia non è un optional stilistico: è ciò che rende una richiesta accettabile. Per questo ogni scenario abbina sempre una funzione pratica a una forma cortese specifica, non solo al vocabolario dell'argomento.",
                    history="La formula Könnten Sie…? usa già qui il Konjunktiv II (approfondito in B2): è un esempio di come il tedesco usi il condizionale per addolcire una richiesta diretta — lo stesso meccanismo di cortesia dell'italiano ('Potrebbe…?').",
                    tip="Non limitarti al vocabolario isolato (Termin, Rezept, Bewerbung…): esercitati sempre dentro la formula di cortesia completa, perché è la combinazione delle due cose che serve in una conversazione reale.",
                    summary="La cortesia non è un extra stilistico: è ciò che rende accettabile una richiesta di servizio.",
                ),
                Explanation(
                    rule="Phone calls, appointments, the pharmacy, work and housing become practical scenarios where professional vocabulary always combines with polite formulas: a request (Könnten Sie…?), a clarification (Was bedeutet…?), a confirmation (Habe ich das richtig verstanden?).",
                    why="In real service situations politeness isn't a stylistic extra: it's what makes a request acceptable. That's why every scenario pairs a practical function with a specific polite form, not just topic vocabulary.",
                    history="The formula Könnten Sie…? already uses Konjunktiv II here (covered in depth at B2): German uses the conditional to soften a direct request - the same politeness mechanism many languages use with their own conditional ('Could you…?').",
                    tip="Don't just learn isolated vocabulary (Termin, Rezept, Bewerbung…): always practise it inside the full polite formula, since it's the combination of both that you need in a real conversation.",
                    summary="Politeness isn't a stylistic extra: it's what makes a service request acceptable.",
                ),
                Explanation(
                    rule="Llamadas, citas, farmacia, trabajo y vivienda se convierten en escenarios prácticos donde el vocabulario profesional se combina con fórmulas de cortesía: pedir (Könnten Sie…?), aclarar (Was bedeutet…?), confirmar (Habe ich das richtig verstanden?).",
                    why="En situaciones de servicio reales la cortesía no es un adorno: es lo que hace aceptable una petición. Por eso cada escenario combina una función práctica con una forma cortés concreta, no solo vocabulario del tema.",
                    history="La fórmula Könnten Sie…? ya usa aquí el Konjunktiv II (profundizado en B2): el alemán usa el condicional para suavizar una petición directa, el mismo mecanismo de cortesía que el español usa con el condicional ('¿Podría…?').",
                    tip="No te limites al vocabulario aislado (Termin, Rezept, Bewerbung…): practícalo siempre dentro de la fórmula de cortesía completa, porque es la combinación de ambas cosas lo que sirve en una conversación real.",
                    summary="La cortesía no es un adorno: es lo que hace aceptable una petición de servicio.",
                ),
                Explanation(
                    rule="Telefon görüşmeleri, randevular, eczane, iş ve konut, meslekî söz varlığının nezaket kalıplarıyla birleştiği pratik senaryolar hâline gelir: rica (Könnten Sie…?), açıklama (Was bedeutet…?), teyit (Habe ich das richtig verstanden?).",
                    why="Gerçek hizmet durumlarında nezaket stilistik bir seçenek değildir: bir talebi kabul edilebilir kılan şeydir. Bu yüzden her senaryo pratik bir işlevi belirli bir nazik biçimle eşleştirir, yalnızca konu söz varlığıyla değil.",
                    history="Könnten Sie…? kalıbı burada Konjunktiv II'yi (B2'de derinleştirilir) zaten kullanır: Almanca doğrudan bir talebi yumuşatmak için şart kipini kullanır - birçok dilin kendi şart kipiyle kullandığı aynı nezaket mekanizması.",
                    tip="Sadece izole söz varlığını (Termin, Rezept, Bewerbung…) öğrenme: bunu her zaman tam nezaket kalıbı içinde çalış, çünkü gerçek bir konuşmada işe yarayan ikisinin birleşimidir.",
                    summary="Nezaket stilistik bir ekstra değildir: bir hizmet talebini kabul edilebilir kılan şeydir.",
                ),
                ("Könnten Sie das bitte wiederholen?", "Ich brauche einen Termin beim Arzt."),
                ("th_formula",),
                (
                    ("Könnten Sie …?",),
                    ("Was bedeutet …?",),
                    ("Habe ich das richtig verstanden?",),
                ),
            ),
            Topic(
                "7 · Pronomi e verbi riflessivi",
                Explanation(
                    rule="I verbi riflessivi si usano con un pronome che rimanda al soggetto stesso (sich freuen = rallegrarsi, sich interessieren = interessarsi). Il pronome riflessivo è identico al pronome personale per ich/du/wir/ihr, ma diventa sich per la terza persona (er/sie/es/sie-Sie) in entrambi i casi, accusativo e dativo.",
                    why="Molti verbi che in italiano non sono riflessivi lo sono in tedesco (sich freuen = «essere contento», non «rallegrare se stesso» in senso letterale) e viceversa: per questo il pronome riflessivo va imparato insieme al verbo, come un'unità fissa, non dedotto dal significato italiano.",
                    history="Il pronome riflessivo sich per la terza persona deriva dal proto-germanico *sik, imparentato con il latino se/sui (da cui l'italiano «si»): è uno dei pochi punti in cui tedesco, italiano e le lingue slave condividono chiaramente la stessa radice indoeuropea per un pronome.",
                    tip="Occhio alla differenza accusativo/dativo nei riflessivi con «io/tu»: «Ich freue mich» (accusativo) ma «Ich kaufe mir etwas» (dativo, perché c'è già un oggetto diretto - etwas - e mir è il beneficiario). Per lui/lei/loro il pronome resta sempre «sich» in entrambi i casi.",
                    summary="sich resta invariato per lui/lei/loro; solo io/tu distinguono accusativo (mich/dich) e dativo (mir/dir).",
                ),
                Explanation(
                    rule="Reflexive verbs are used with a pronoun that refers back to the subject itself (sich freuen = to be glad, sich interessieren = to be interested). The reflexive pronoun is identical to the personal pronoun for ich/du/wir/ihr, but becomes sich for the third person (er/sie/es/sie-Sie) in both the accusative and the dative.",
                    why="Many verbs that aren't reflexive in English are reflexive in German (sich freuen = 'to be glad', not literally 'to make oneself happy') and vice versa: that's why the reflexive pronoun must be learned together with the verb, as a fixed unit, not guessed from the English meaning.",
                    history="The third-person reflexive pronoun sich comes from Proto-Germanic *sik, related to Latin se/sui (the source of Italian 'si' and Spanish 'se'): one of the few points where German, the Romance languages and the Slavic languages clearly share the same Indo-European root for a pronoun.",
                    tip="Watch the accusative/dative difference in the reflexives for 'I/you': 'Ich freue mich' (accusative) but 'Ich kaufe mir etwas' (dative, because there's already a direct object - etwas - and mir is the beneficiary). For he/she/they the pronoun always stays sich in both cases.",
                    summary="sich stays the same for he/she/they; only I/you distinguish accusative (mich/dich) from dative (mir/dir).",
                ),
                Explanation(
                    rule="Los verbos reflexivos se usan con un pronombre que remite al propio sujeto (sich freuen = alegrarse, sich interessieren = interesarse). El pronombre reflexivo es idéntico al pronombre personal para ich/du/wir/ihr, pero se convierte en sich para la tercera persona (er/sie/es/sie-Sie) tanto en acusativo como en dativo.",
                    why="Muchos verbos que en español no son reflexivos lo son en alemán (sich freuen = 'alegrarse') y viceversa: por eso el pronombre reflexivo hay que aprenderlo junto con el verbo, como una unidad fija, no deducirlo del significado en español.",
                    history="El pronombre reflexivo sich de la tercera persona viene del protogermánico *sik, emparentado con el latín se/sui (de donde vienen el español 'se' y el italiano 'si'): uno de los pocos puntos donde alemán, lenguas románicas y lenguas eslavas comparten claramente la misma raíz indoeuropea para un pronombre.",
                    tip="Cuidado con la diferencia acusativo/dativo en los reflexivos de 'yo/tú': 'Ich freue mich' (acusativo) pero 'Ich kaufe mir etwas' (dativo, porque ya hay un objeto directo -etwas- y mir es el beneficiario). Para él/ella/ellos el pronombre siempre queda sich en ambos casos.",
                    summary="sich no cambia para él/ella/ellos; solo yo/tú distinguen acusativo (mich/dich) de dativo (mir/dir).",
                ),
                Explanation(
                    rule="Dönüşlü fiiller, öznenin kendisine gönderme yapan bir zamirle kullanılır (sich freuen = sevinmek, sich interessieren = ilgilenmek). Dönüşlü zamir ich/du/wir/ihr için kişi zamiriyle aynıdır, ama üçüncü kişide (er/sie/es/sie-Sie) hem akkusativde hem dativde sich olur.",
                    why="Türkçede dönüşlü olmayan birçok fiil Almancada dönüşlüdür (sich freuen = sevinmek) ve tersi de olur: bu yüzden dönüşlü zamir fiille birlikte, sabit bir birim olarak öğrenilmelidir, Türkçe anlamdan tahmin edilmemelidir.",
                    history="Üçüncü kişi dönüşlü zamiri sich, Proto-Germen *sik'ten gelir, Latince se/sui ile akrabadır (İtalyanca 'si' ve İspanyolca 'se'nin kaynağı): Almanca, Roman dilleri ve Slav dillerinin bir zamir için açıkça aynı Hint-Avrupa kökünü paylaştığı ender noktalardan biridir.",
                    tip="'ben/sen' dönüşlülerinde akkusativ/dativ farkına dikkat: 'Ich freue mich' (akkusativ) ama 'Ich kaufe mir etwas' (dativ, çünkü zaten bir doğrudan nesne var -etwas- ve mir yararlanıcıdır). O/onlar için zamir her iki hâlde de her zaman sich kalır.",
                    summary="sich o/onlar için değişmez; sadece ben/sen akkusativ (mich/dich) ile dativ (mir/dir) arasında ayrım yapar.",
                ),
                ("Ich freue mich auf die Ferien.", "Er interessiert sich für Musik."),
                ("Person", "Akkusativ", "Dativ"),
                (
                    ("ich", "mich", "mir"),
                    ("du", "dich", "dir"),
                    ("er / sie / es", "sich", "sich"),
                    ("wir", "uns", "uns"),
                    ("ihr", "euch", "euch"),
                    ("sie / Sie", "sich", "sich"),
                ),
            ),
        ],
    },
    "B1": {
        "colour": "B1",
        "title": {"it": "Argomentare, lavorare, partecipare", "en": "Argue, work and participate", "es": "Argumentar, trabajar, participar", "tr": "Tartışmak, çalışmak, katılmak"},
        "can": {"it": "Spiegare problemi, raccontare esperienze e comunicare con sicurezza in studio e lavoro.", "en": "Explain problems, report experience and communicate confidently at study and work.", "es": "Explicar problemas, relatar experiencias y comunicarte con seguridad en estudios y trabajo.", "tr": "Sorunları açıklamak, deneyim aktarmak ve eğitimle işte güvenle iletişim kurmak."},
        "topics": [
            Topic(
                "1 · Subordinate e coesione",
                Explanation(
                    rule="Le congiunzioni subordinanti di B1 (weil, obwohl, während, damit, bevor…) introducono frasi con il verbo alla fine, come già in A2, ma qui il loro ruolo diventa costruire testi coesi: ogni congiunzione segnala una relazione logica precisa (causa, concessione, contemporaneità, scopo, anteriorità).",
                    why="Un testo B1 efficace non è solo grammaticalmente corretto: deve rendere espliciti i collegamenti logici tra le idee, così chi legge non deve indovinarli. Conviene pianificare la frase prima di scriverla: quale congiunzione? quale relazione voglio esprimere?",
                    history="Molte di queste congiunzioni sono storicamente fusioni di elementi più antichi: obwohl nasce da ob + wohl, damit fonde da (avverbio pronominale) + mit («con ciò»). Questo pattern — fondere un avverbio pronominale con una preposizione — è molto produttivo in tedesco (vedi anche wodurch, wobei).",
                    tip="Non confondere weil (causa) e obwohl (concessione): entrambe mandano il verbo alla fine, ma cambiano completamente la relazione logica. «Ich bin müde, weil ich gearbeitet habe» è diverso da «Ich arbeite, obwohl ich müde bin».",
                    summary="Ogni congiunzione segnala una relazione logica precisa: non sono intercambiabili solo perché mandano il verbo alla fine.",
                ),
                Explanation(
                    rule="The B1 subordinating conjunctions (weil, obwohl, während, damit, bevor…) introduce clauses with the verb at the end, as at A2, but here their role becomes building cohesive texts: each conjunction signals a precise logical relationship (cause, concession, simultaneity, purpose, anteriority).",
                    why="An effective B1 text isn't just grammatically correct: it must make the logical links between ideas explicit, so the reader doesn't have to guess them. It helps to plan the sentence before writing it: which conjunction? which relationship do I want to express?",
                    history="Many of these conjunctions are historically fusions of older elements: obwohl comes from ob + wohl, damit fuses da (a pronominal adverb) + mit ('with that'). This pattern - fusing a pronominal adverb with a preposition - is very productive in German (see also wodurch, wobei).",
                    tip="Don't confuse weil (cause) and obwohl (concession): both send the verb to the end, but they change the logical relationship completely. «Ich bin müde, weil ich gearbeitet habe» differs from «Ich arbeite, obwohl ich müde bin».",
                    summary="Each conjunction signals a precise logical relationship: they aren't interchangeable just because they all send the verb to the end.",
                ),
                Explanation(
                    rule="Las conjunciones subordinantes de B1 (weil, obwohl, während, damit, bevor…) introducen oraciones con el verbo al final, como en A2, pero aquí su papel es construir textos cohesionados: cada conjunción señala una relación lógica precisa (causa, concesión, simultaneidad, finalidad, anterioridad).",
                    why="Un texto B1 eficaz no es solo gramaticalmente correcto: debe hacer explícitos los vínculos lógicos entre las ideas. Conviene planificar la frase antes de escribirla: ¿qué conjunción? ¿qué relación quiero expresar?",
                    history="Muchas de estas conjunciones son históricamente fusiones de elementos más antiguos: obwohl nace de ob + wohl, damit fusiona da (adverbio pronominal) + mit ('con eso'). Este patrón es muy productivo en alemán (véase también wodurch, wobei).",
                    tip="No confundas weil (causa) y obwohl (concesión): ambas mandan el verbo al final, pero cambian la relación lógica por completo. «Ich bin müde, weil ich gearbeitet habe» es distinto de «Ich arbeite, obwohl ich müde bin».",
                    summary="Cada conjunción señala una relación lógica precisa: no son intercambiables solo porque manden el verbo al final.",
                ),
                Explanation(
                    rule="B1'in bağlaçları (weil, obwohl, während, damit, bevor…), A2'de olduğu gibi fiili sona taşıyan cümleler kurar, ama burada işlevleri bağdaşık metinler oluşturmaktır: her bağlaç kesin bir mantıksal ilişkiyi (neden, karşıtlık, eşzamanlılık, amaç, önce oluş) işaretler.",
                    why="Etkili bir B1 metni sadece dilbilgisel doğru olmakla kalmaz: fikirler arasındaki mantıksal bağlantıları açık hâle getirmelidir. Cümleyi yazmadan önce planlamak işe yarar: hangi bağlaç? hangi ilişkiyi ifade etmek istiyorum?",
                    history="Bu bağlaçların çoğu tarihsel olarak daha eski ögelerin kaynaşmasıdır: obwohl, ob + wohl'den doğar, damit ise da (zamirsi zarf) + mit'in kaynaşmasıdır. Bu kalıp Almancada çok üretkendir (wodurch, wobei'ye de bakın).",
                    tip="weil (neden) ile obwohl'u (karşıtlık) karıştırma: ikisi de fiili sona gönderir, ama mantıksal ilişkiyi tamamen değiştirir. «Ich bin müde, weil ich gearbeitet habe» ile «Ich arbeite, obwohl ich müde bin» farklıdır.",
                    summary="Her bağlaç kesin bir mantıksal ilişkiyi işaretler: hepsi fiili sona gönderdiği için birbirinin yerine geçmez.",
                ),
                ("Obwohl es regnet, fahre ich zur Arbeit.", "Ich lerne, damit ich die Prüfung bestehe."),
                ("th_conjunction", "th_function"),
                (
                    ("weil", "kausal"),
                    ("obwohl", "konzessiv"),
                    ("während", "temporal"),
                    ("damit", "final"),
                    ("bevor", "temporal"),
                ),
            ),
            Topic(
                "2 · Passivo e processi",
                Explanation(
                    rule="Il Vorgangspassiv (passivo di processo) si forma con werden + Partizip II e descrive un'azione in corso (Das Gerät wird repariert = viene riparato, ora). Il Zustandspassiv (passivo di stato) si forma con sein + Partizip II e descrive il risultato già raggiunto (Das Gerät ist repariert = è riparato).",
                    why="Questa distinzione è utile quando serve mettere al centro un processo o un risultato senza nominare chi lo compie: istruzioni, produzione, amministrazione. Scegliere werden o sein cambia il significato in modo netto.",
                    history="Il werden-Passiv è una grammaticalizzazione relativamente più recente: werden significava «diventare», quindi «wird repariert» significa letteralmente «diventa riparato». Il sein-Passiv è più antico e semplice: un aggettivo participiale usato come predicato.",
                    tip="Errore comune: usare sein-Passiv quando l'azione è ancora in corso. Se il tecnico sta ancora lavorando, serve wird repariert, non ist repariert (che implica lavoro già concluso).",
                    summary="werden + Partizip II = processo in corso; sein + Partizip II = risultato già raggiunto.",
                ),
                Explanation(
                    rule="The Vorgangspassiv (process passive) is formed with werden + Partizip II and describes an ongoing action (Das Gerät wird repariert = it is being repaired, now). The Zustandspassiv (state passive) is formed with sein + Partizip II and describes an already-reached result (Das Gerät ist repariert = it is repaired).",
                    why="This distinction is useful whenever you need to foreground a process or result without naming who performs it: instructions, production, administration. Choosing werden or sein changes the meaning sharply.",
                    history="The werden-passive is a relatively more recent grammaticalisation: werden meant 'to become', so 'wird repariert' literally means 'becomes repaired'. The sein-passive is older and simpler: a participial adjective used as a predicate.",
                    tip="A common mistake is using sein-passive when the action is still in progress: if the technician is still working, you need wird repariert, not ist repariert (which implies the job is finished).",
                    summary="werden + Partizip II = process under way; sein + Partizip II = result already reached.",
                ),
                Explanation(
                    rule="El Vorgangspassiv (pasiva de proceso) se forma con werden + Partizip II y describe una acción en curso (Das Gerät wird repariert = está siendo reparado, ahora). El Zustandspassiv (pasiva de estado) se forma con sein + Partizip II y describe un resultado ya alcanzado (Das Gerät ist repariert = está reparado).",
                    why="Esta distinción es útil cuando hace falta poner en el centro un proceso o un resultado sin nombrar quién lo realiza: instrucciones, producción, administración. Elegir werden o sein cambia el significado con claridad.",
                    history="La pasiva con werden es una gramaticalización relativamente más reciente: werden significaba 'llegar a ser', así que 'wird repariert' significa literalmente 'llega a estar reparado'. La pasiva con sein es más antigua y sencilla: un adjetivo participial usado como predicado.",
                    tip="Error común: usar la pasiva con sein cuando la acción todavía está en curso. Si el técnico sigue trabajando, hace falta wird repariert, no ist repariert (que implica que el trabajo ya terminó).",
                    summary="werden + Partizip II = proceso en curso; sein + Partizip II = resultado ya alcanzado.",
                ),
                Explanation(
                    rule="Vorgangspassiv (süreç edilgeni), werden + Partizip II ile kurulur ve devam eden bir eylemi anlatır (Das Gerät wird repariert = şu anda tamir ediliyor). Zustandspassiv (durum edilgeni) ise sein + Partizip II ile kurulur ve ulaşılmış bir sonucu anlatır (Das Gerät ist repariert = tamir edilmiş durumda).",
                    why="Bu ayrım, kimin yaptığını belirtmeden bir süreci ya da sonucu öne çıkarmak gerektiğinde işe yarar: talimatlar, üretim, idari metinler. werden ya da sein seçimi anlamı keskin biçimde değiştirir.",
                    history="werden-edilgeni nispeten daha yeni bir dilbilgiselleşmedir: werden 'olmak' anlamındaydı, bu yüzden 'wird repariert' tam olarak 'tamir edilmiş hâline geliyor' demektir. sein-edilgeni daha eski ve basittir: yüklem olarak kullanılan bir partisip sıfat.",
                    tip="Yaygın hata, eylem hâlâ devam ederken sein-edilgenini kullanmaktır: tamirci hâlâ çalışıyorsa wird repariert gerekir, ist repariert (işin bittiğini ima eder) değil.",
                    summary="werden + Partizip II = devam eden süreç; sein + Partizip II = ulaşılmış sonuç.",
                ),
                ("Das Gerät wird repariert.", "Das Gerät ist repariert."),
                ("Passiv", "th_formula", "th_example"),
                (
                    ("Vorgangspassiv", "werden + Partizip II", "Das Auto wird repariert."),
                    ("Zustandspassiv", "sein + Partizip II", "Das Auto ist repariert."),
                ),
            ),
            Topic(
                "3 · Relativi e precisione",
                Explanation(
                    rule="Le frasi relative evitano ripetizioni collegando informazioni su un nome già menzionato. Il pronome relativo (der/die/das…) prende genere e numero dal nome a cui si riferisce (l'antecedente), ma il caso dalla funzione che ha dentro la frase relativa stessa.",
                    why="Questo doppio criterio (genere/numero dall'esterno, caso dall'interno) richiede un piccolo calcolo mentale: guardare sia indietro (a chi ti riferisci) sia avanti (che ruolo ha in quella frase). Una volta automatizzato, permette frasi molto più precise senza ripetere il nome.",
                    history="I pronomi relativi tedeschi derivano dal sistema dei dimostrativi/articoli (der/die/das) — un'evoluzione comune a molte lingue indoeuropee. Il tedesco lo mostra in modo trasparente, dato che le forme sono quasi identiche all'articolo determinativo.",
                    tip="Errore tipico: assegnare il caso in base al primo verbo che viene in mente invece che al ruolo dentro la relativa. In «Der Mann, dem ich schreibe» il caso è dativo perché schreiben regge il dativo, non perché der Mann è maschile.",
                    summary="Genere e numero vengono da fuori (l'antecedente); il caso viene da dentro (il ruolo nella relativa).",
                ),
                Explanation(
                    rule="Relative clauses avoid repetition by attaching information to an already-mentioned noun. The relative pronoun (der/die/das…) takes its gender and number from the noun it refers to (the antecedent), but its case from the role it plays inside the relative clause itself.",
                    why="This double criterion (gender/number from outside, case from inside) requires a small mental calculation: looking both backwards (who you're referring to) and forwards (what role they play). Once automatic, it lets you write much more precise sentences without repeating the noun.",
                    history="German relative pronouns derive from the demonstrative/article system (der/die/das) - a development shared by many Indo-European languages. German shows this transparently, since the forms are almost identical to the definite article.",
                    tip="The typical mistake is assigning the case based on the first verb that comes to mind, rather than the role inside the clause: in «Der Mann, dem ich schreibe» the case is dative because schreiben governs the dative, not because der Mann is masculine.",
                    summary="Gender and number come from outside (the antecedent); the case comes from inside (the role in the clause).",
                ),
                Explanation(
                    rule="Las oraciones de relativo evitan repeticiones conectando información sobre un sustantivo ya mencionado. El pronombre relativo (der/die/das…) toma género y número del sustantivo al que se refiere (el antecedente), pero el caso de la función que cumple dentro de la propia relativa.",
                    why="Este doble criterio (género/número desde fuera, caso desde dentro) exige un pequeño cálculo mental: mirar hacia atrás (a quién te refieres) y hacia delante (qué papel cumple). Una vez automatizado, permite frases mucho más precisas sin repetir el sustantivo.",
                    history="Los pronombres relativos alemanes derivan del sistema de demostrativos/artículos (der/die/das): una evolución compartida por muchas lenguas indoeuropeas. El alemán lo muestra de forma transparente, ya que las formas son casi idénticas al artículo determinado.",
                    tip="El error típico es asignar el caso según el primer verbo que viene a la mente, no según el papel dentro de la relativa: en «Der Mann, dem ich schreibe» el caso es dativo porque schreiben rige dativo, no porque der Mann sea masculino.",
                    summary="Género y número vienen de fuera (el antecedente); el caso viene de dentro (el papel en la relativa).",
                ),
                Explanation(
                    rule="İlgi cümleleri, zaten adı geçmiş bir isme bilgi ekleyerek tekrarları önler. İlgi zamiri (der/die/das…) cinsiyetini ve sayısını atıfta bulunduğu isimden alır, ama hâlini ilgi cümlesinin içindeki rolünden alır.",
                    why="Bu çifte ölçüt (dışarıdan cinsiyet/sayı, içeriden hâl) küçük bir zihinsel hesap gerektirir: hem geriye hem ileriye bakman gerekir. Otomatikleştiğinde, ismi tekrarlamadan çok daha kesin cümleler kurmanı sağlar.",
                    history="Almanca ilgi zamirleri işaret sıfatı/artikel sisteminden (der/die/das) gelir - birçok Hint-Avrupa dilinde görülen bir gelişim. Almanca bunu şeffaf biçimde gösterir, çünkü biçimler belirli artikelle neredeyse özdeştir.",
                    tip="Tipik hata, ilgi cümlesi içindeki role değil, akla ilk gelen fiile göre hâl belirlemektir: «Der Mann, dem ich schreibe» cümlesinde hâl dativdir, çünkü schreiben dativ ister, der Mann eril olduğu için değil.",
                    summary="Cinsiyet ve sayı dışarıdan gelir (atıfta bulunulan isim); hâl içeriden gelir (yan cümledeki rol).",
                ),
                ("Das ist die Frau, die mir hilft.", "Der Mann, dem ich schreibe, arbeitet hier."),
                ("Kasus", "Maskulin", "Feminin", "Neutrum", "Plural"),
                (
                    ("Nominativ", "der", "die", "das", "die"),
                    ("Akkusativ", "den", "die", "das", "die"),
                    ("Dativ", "dem", "der", "dem", "denen"),
                ),
            ),
            Topic(
                "4 · Opinione e discussione",
                Explanation(
                    rule="Una risposta B1 efficace segue una struttura: tesi, ragione, esempio e un possibile limite. Connettori come denn, deshalb, trotzdem, einerseits…andererseits collegano questi elementi in modo esplicito, senza esagerare nel loro numero.",
                    why="I connettori non sono decorazione: ognuno corrisponde a una relazione logica precisa (denn = causa, deshalb = conseguenza, trotzdem = contrasto inatteso). Usarli con moderazione rende il discorso più chiaro; usarne troppi lo appesantisce.",
                    history="denn (causale) e dann (temporale, «poi») derivano storicamente dalla stessa parola dell'alto tedesco antico (denne), poi separata in due forme e funzioni distinte — un classico caso di biforcazione storica.",
                    tip="Non confondere denn (perché, verbo in seconda posizione) con weil (perché, verbo alla fine): «Ich bleibe, denn ich bin müde» e «Ich bleibe, weil ich müde bin» sono entrambe corrette ma con struttura diversa.",
                    summary="Un connettore per relazione logica: usarne troppi appesantisce il discorso invece di chiarirlo.",
                ),
                Explanation(
                    rule="An effective B1 answer follows a structure: claim, reason, example and a possible limitation. Connectors like denn, deshalb, trotzdem, einerseits…andererseits link these elements explicitly, without overusing them.",
                    why="Connectors aren't decoration: each corresponds to a precise logical relationship (denn = cause, deshalb = consequence, trotzdem = unexpected contrast). Using them sparingly makes speech clearer; too many weigh it down.",
                    history="denn (causal) and dann (temporal, 'then') historically derive from the same Old High German word (denne), which later split into two forms and functions - a classic case of historical bifurcation.",
                    tip="Don't confuse denn (because, verb in second position) with weil (because, verb at the end): «Ich bleibe, denn ich bin müde» and «Ich bleibe, weil ich müde bin» are both correct but structured differently.",
                    summary="One connector per logical relationship: too many weigh a text down instead of clarifying it.",
                ),
                Explanation(
                    rule="Una respuesta B1 eficaz sigue una estructura: tesis, razón, ejemplo y un posible límite. Conectores como denn, deshalb, trotzdem, einerseits…andererseits unen estos elementos de forma explícita, sin usarlos en exceso.",
                    why="Los conectores no son adorno: cada uno corresponde a una relación lógica precisa (denn = causa, deshalb = consecuencia, trotzdem = contraste inesperado). Usarlos con moderación aclara el discurso; demasiados lo recargan.",
                    history="denn (causal) y dann (temporal, 'luego') derivan de la misma palabra del alto alemán antiguo (denne), separada después en dos formas y funciones: un caso clásico de bifurcación histórica.",
                    tip="No confundas denn (porque, verbo en segunda posición) con weil (porque, verbo al final): «Ich bleibe, denn ich bin müde» y «Ich bleibe, weil ich müde bin» son ambas correctas pero con estructura distinta.",
                    summary="Un conector por relación lógica: usar demasiados recarga el discurso en vez de aclararlo.",
                ),
                Explanation(
                    rule="Etkili bir B1 cevabı şu yapıyı izler: görüş, neden, örnek ve olası bir sınır. denn, deshalb, trotzdem, einerseits…andererseits gibi bağlaçlar bu ögeleri açıkça birbirine bağlar, ama fazla kullanılmamalıdır.",
                    why="Bağlaçlar süs değildir: her biri kesin bir mantıksal ilişkiye karşılık gelir (denn = neden, deshalb = sonuç, trotzdem = beklenmedik karşıtlık). Ölçülü kullanmak konuşmayı netleştirir; çok fazlası ağırlaştırır.",
                    history="denn ve dann, Eski Yüksek Almancadaki aynı kelimeden (denne) gelir; bu kelime sonradan iki farklı biçime ve işleve ayrılmıştır - klasik bir tarihsel ayrışma örneği.",
                    tip="denn (çünkü, fiil ikinci sırada) ile weil'i (çünkü, fiil sonda) karıştırma: «Ich bleibe, denn ich bin müde» ve «Ich bleibe, weil ich müde bin» ikisi de doğrudur ama yapıları farklıdır.",
                    summary="Mantıksal ilişki başına bir bağlaç: çok fazlası konuşmayı netleştirmek yerine ağırlaştırır.",
                ),
                ("Meiner Meinung nach ist das sinnvoll.", "Deshalb schlage ich eine andere Lösung vor."),
                ("th_conjunction", "th_function"),
                (
                    ("denn", "kausal"),
                    ("deshalb", "konsekutiv"),
                    ("trotzdem", "adversativ"),
                    ("einerseits … andererseits", "kontrastiv"),
                ),
            ),
            Topic(
                "5 · Bewerbung e lavoro",
                Explanation(
                    rule="Il modulo professionale tratta annuncio di lavoro, Anschreiben (lettera di motivazione), Lebenslauf (curriculum), colloquio e comunicazione di squadra. Ogni testo deve essere concreto, verificabile e adatto al destinatario.",
                    why="In un contesto professionale la forma non è meno importante del contenuto: un'espressione troppo informale in un Anschreiben comunica involontariamente scarsa serietà, anche con ottime competenze descritte.",
                    history="Il forte grado di formularità del tedesco professionale (frasi fisse come «Mit freundlichen Grüßen») ha radici nella lunga tradizione della Kanzleisprache (lingua di cancelleria), sviluppatasi nei secoli come registro scritto ufficiale.",
                    tip="Non improvvisare la struttura del Lebenslauf o dell'Anschreiben: il tedesco professionale premia il rispetto di un formato riconoscibile più della creatività stilistica.",
                    summary="La forma conta quanto il contenuto: un formato riconoscibile vale più della creatività stilistica.",
                ),
                Explanation(
                    rule="The professional module covers job ads, the Anschreiben (cover letter), the Lebenslauf (CV), interviews and team communication. Every text must be concrete, verifiable and suited to its audience.",
                    why="In a professional context, form matters as much as content: an overly informal expression in an Anschreiben unintentionally signals a lack of seriousness, even with excellent skills described.",
                    history="The strongly formulaic nature of professional German (fixed phrases like «Mit freundlichen Grüßen») has roots in the long tradition of Kanzleisprache (chancery language), developed over centuries as an official written register.",
                    tip="Don't improvise the structure of the Lebenslauf or Anschreiben: professional German rewards a recognisable format far more than stylistic creativity.",
                    summary="Form matters as much as content: a recognisable format beats stylistic creativity.",
                ),
                Explanation(
                    rule="El módulo profesional trabaja el anuncio de empleo, el Anschreiben (carta de motivación), el Lebenslauf (currículum), la entrevista y la comunicación de equipo. Cada texto debe ser concreto, verificable y adecuado al destinatario.",
                    why="En un contexto profesional la forma importa tanto como el contenido: una expresión demasiado informal en un Anschreiben transmite involuntariamente falta de seriedad, aunque las competencias descritas sean excelentes.",
                    history="El fuerte carácter formulaico del alemán profesional (frases fijas como «Mit freundlichen Grüßen») tiene raíces en la larga tradición de la Kanzleisprache (lengua de cancillería), desarrollada durante siglos como registro escrito oficial.",
                    tip="No improvises la estructura del Lebenslauf o del Anschreiben: el alemán profesional premia seguir un formato reconocible mucho más que la creatividad estilística.",
                    summary="La forma importa tanto como el contenido: un formato reconocible vale más que la creatividad estilística.",
                ),
                Explanation(
                    rule="Meslek modülü iş ilanını, Anschreiben'i, Lebenslauf'u, mülakatı ve ekip iletişimini kapsar. Her metin somut, doğrulanabilir ve muhataba uygun olmalıdır.",
                    why="Meslekî bir bağlamda biçim, içerik kadar önemlidir: bir Anschreiben'de fazla samimi bir ifade, yetkinlikler mükemmel olsa bile istemeden ciddiyetsizlik izlenimi verir.",
                    history="Meslekî Almancanın güçlü kalıplaşmış yapısı (Mit freundlichen Grüßen gibi sabit ifadeler), yüzyıllar içinde resmî yazılı bir üslup olarak gelişen Kanzleisprache geleneğine dayanır.",
                    tip="Lebenslauf ya da Anschreiben'in yapısını doğaçlama kurma: meslekî Almanca, üslup yaratıcılığından çok tanınabilir bir formata uymayı ödüllendirir.",
                    summary="Biçim, içerik kadar önemlidir: tanınabilir bir format, üslup yaratıcılığından daha değerlidir.",
                ),
                ("Ich bewerbe mich um die Stelle als …", "Im Anhang finden Sie meinen Lebenslauf."),
                ("th_part", "th_content"),
                (
                    ("Einleitung", "Bezug auf die Stelle"),
                    ("Hauptteil", "Qualifikation und Erfahrung"),
                    ("Schluss", "Grußformel"),
                ),
            ),
            Topic(
                "6 · Strategia d'esame B1",
                Explanation(
                    rule="La prova B1 combina lettura globale, ricerca di dettagli mirati, un'e-mail formale e una breve presentazione orale. La revisione di un testo scritto segue un ordine preciso: prima il verbo, poi connettori, casi e infine il registro.",
                    why="Revisionare in questo ordine funziona perché il verbo regge tutta la struttura della frase: se è sbagliato, ogni altra correzione rischia di essere inutile. Procedere dal più strutturale al più fine fa risparmiare tempo prezioso.",
                    history="Il quadro dei livelli A1-C2 che struttura questo corso — e l'idea dei «can-do statements» che trovi a inizio di ogni modulo — nasce dal Quadro Comune Europeo di Riferimento (QCER), pubblicato dal Consiglio d'Europa nel 2001.",
                    tip="Non aspettare la fine per revisionare tutto insieme: controlla il verbo frase per frase, subito dopo averla scritta. È più facile individuare un errore isolato che ritrovarlo in un testo già concluso.",
                    summary="Revisiona in ordine fisso, dal più strutturale (verbo) al più fine (registro), non tutto insieme alla fine.",
                ),
                Explanation(
                    rule="The B1 exam combines global reading, targeted detail search, a formal email and a short oral presentation. Revising a written text follows a precise order: first the verb, then connectors, then case, and finally register.",
                    why="Revising in this order works because the verb holds up the whole sentence structure: if it's wrong, every other correction risks being pointless. Working from the most structural to the finest detail saves valuable time.",
                    history="The A1-C2 level framework structuring this course - and the idea of 'can-do statements' at the start of each module - comes from the Common European Framework of Reference (CEFR), published by the Council of Europe in 2001.",
                    tip="Don't wait until the end to revise everything at once: check the verb sentence by sentence, right after writing it. It's easier to spot an isolated mistake than to find it in an already-finished text.",
                    summary="Revise in a fixed order, from most structural (verb) to finest (register), not all at once at the end.",
                ),
                Explanation(
                    rule="La prueba B1 combina lectura global, búsqueda de detalles concretos, un correo formal y una breve presentación oral. Revisar un texto escrito sigue un orden preciso: primero el verbo, luego los conectores, después los casos y por último el registro.",
                    why="Revisar en este orden funciona porque el verbo sostiene toda la estructura de la frase: si está mal, cualquier otra corrección corre el riesgo de ser inútil. Ir de lo estructural a lo fino ahorra un tiempo valioso.",
                    history="El marco de niveles A1-C2 que estructura este curso -y la idea de los 'can-do statements' al inicio de cada módulo- procede del Marco Común Europeo de Referencia (MCER), publicado por el Consejo de Europa en 2001.",
                    tip="No esperes al final para revisarlo todo junto: comprueba el verbo frase por frase, justo después de escribirla. Es más fácil detectar un error aislado que en un texto ya terminado.",
                    summary="Revisa en un orden fijo, de lo más estructural (verbo) a lo más fino (registro), no todo junto al final.",
                ),
                Explanation(
                    rule="B1 sınavı genel okumayı, hedefli ayrıntı aramayı, resmî bir e-postayı ve kısa bir sözlü sunumu bir araya getirir. Yazılı bir metni gözden geçirmek belirli bir sırayı izler: önce fiil, sonra bağlaçlar, hâller, en son üslup.",
                    why="Bu sırayla gözden geçirmek işe yarar, çünkü fiil tüm cümle yapısını taşır: yanlışsa diğer düzeltmeler boşa gidebilir. En yapısaldan en ince ayrıntıya ilerlemek sınavda değerli zaman kazandırır.",
                    history="Bu dersi yapılandıran A1-C2 seviye çerçevesi - ve her modülün başındaki 'yapabilirim ifadeleri' fikri - Avrupa Konseyi tarafından 2001'de yayımlanan Avrupa Ortak Dil Çerçevesi'nden (CEFR) gelir.",
                    tip="Her şeyi sona bırakıp gözden geçirme: fiili cümle cümle, yazdıktan hemen sonra kontrol et. İzole bir hatayı bitmiş bir metinde bulmaktan çok daha kolaydır.",
                    summary="Sabit bir sırayla gözden geçir, en yapısaldan (fiil) en inceye (üslup): hepsini sona bırakma.",
                ),
                ("Könnten wir einen Termin vereinbaren?", "Zusammenfassend möchte ich betonen, dass …"),
                ("th_step", "th_focus"),
                (
                    ("1", "Verb"),
                    ("2", "Konnektoren"),
                    ("3", "Kasus"),
                    ("4", "Register"),
                ),
            ),
            Topic(
                "7 · Aggettivi declinati e genitivo",
                Explanation(
                    rule="Quando un aggettivo precede il sostantivo, prende una desinenza che dipende dall'articolo che lo accompagna. Con l'articolo determinativo (der/die/das) l'aggettivo prende quasi sempre -e o -en (declinazione debole); con l'articolo indeterminativo (ein/eine) o senza articolo, deve «recuperare» l'informazione di genere/caso che l'articolo non dà (declinazione forte/mista). Il genitivo (di chi?) usa des/der + una -s finale sul sostantivo maschile/neutro: des Mannes, der Frau.",
                    why="Le diverse declinazioni esistono perché il tedesco vuole che l'informazione di genere/caso compaia sempre da qualche parte nel gruppo nominale - o sull'articolo, o sull'aggettivo, mai perduta del tutto. Per questo, quando l'articolo è «debole» o assente, è l'aggettivo a «rinforzarsi» con una desinenza più marcata.",
                    history="Questo sistema a più declinazioni si è sviluppato storicamente a partire da un sistema più uniforme del proto-germanico: l'articolo determinativo, già molto informativo, «libera» l'aggettivo dal dover specificare di nuovo caso e genere, mentre in sua assenza l'aggettivo deve farlo da solo. Il genitivo è il caso più antico e più eroso nel tedesco moderno: nella lingua parlata viene spesso sostituito da von + dativo.",
                    tip="Non provare a imparare tutte le tabelle a memoria insieme: comincia con la declinazione dopo der/die/das, la più semplice (quasi sempre -e o -en), e aggiungi le altre solo quando questa è automatica.",
                    summary="Dopo der/die/das l'aggettivo prende quasi sempre -e; dopo ein deve «recuperare» da solo genere e caso.",
                ),
                Explanation(
                    rule="When an adjective comes before a noun, it takes an ending that depends on the article accompanying it. With the definite article (der/die/das), the adjective almost always takes -e or -en (weak declension); with the indefinite article (ein/eine) or no article, it has to 'make up for' the gender/case information the article doesn't provide (strong/mixed declension). The genitive (whose?) uses des/der plus a final -s on masculine/neuter nouns: des Mannes, der Frau.",
                    why="The different declensions exist because German wants the gender/case information to always show up somewhere in the noun phrase - either on the article or the adjective, never lost entirely. That's why, when the article is 'weak' or missing, it's the adjective that 'reinforces itself' with a more marked ending.",
                    history="This declension system developed historically from a more uniform Proto-Germanic system: the definite article, already highly informative, 'frees' the adjective from specifying case and gender again, while in its absence the adjective has to do so itself. The genitive is the oldest and most eroded case in Modern German: in spoken language it's often replaced by von + dative.",
                    tip="Don't try to learn all the tables by heart at once: start with the ending after der/die/das, the simplest (almost always -e or -en), and add the others only once this one is automatic.",
                    summary="After der/die/das the adjective almost always takes -e; after ein it has to 'make up for' gender and case itself.",
                ),
                Explanation(
                    rule="Cuando un adjetivo precede al sustantivo, toma una terminación que depende del artículo que lo acompaña. Con el artículo determinado (der/die/das) el adjetivo casi siempre lleva -e o -en (declinación débil); con el indeterminado (ein/eine) o sin artículo, tiene que 'compensar' la información de género/caso que falta (declinación fuerte/mixta). El genitivo (¿de quién?) usa des/der más una -s final en sustantivos masculinos/neutros: des Mannes, der Frau.",
                    why="Las distintas declinaciones existen porque el alemán quiere que la información de género/caso aparezca siempre en algún punto del grupo nominal - en el artículo o en el adjetivo, nunca del todo perdida. Por eso, cuando el artículo es 'débil' o falta, es el adjetivo el que se 'refuerza' con una terminación más marcada.",
                    history="Este sistema de declinación se desarrolló a partir de un sistema más uniforme del protogermánico: el artículo determinado, ya muy informativo, 'libera' al adjetivo de especificar de nuevo caso y género, mientras que en su ausencia el adjetivo debe hacerlo solo. El genitivo es el caso más antiguo y más erosionado en el alemán moderno: en la lengua hablada se sustituye a menudo por von + dativo.",
                    tip="No intentes aprender todas las tablas de memoria a la vez: empieza por la terminación tras der/die/das, la más sencilla (casi siempre -e o -en), y añade las otras solo cuando esta sea automática.",
                    summary="Tras der/die/das el adjetivo casi siempre lleva -e; tras ein tiene que 'compensar' él solo género y caso.",
                ),
                Explanation(
                    rule="Bir sıfat isimden önce geldiğinde, eşlik ettiği artikele bağlı bir ek alır. Belirli artikelle (der/die/das) sıfat neredeyse her zaman -e ya da -en alır (zayıf çekim); belirsiz artikelle (ein/eine) ya da artikelsiz durumda, eksik cinsiyet/hâl bilgisini kendisi 'telafi etmek' zorundadır (güçlü/karışık çekim). Genitiv (kimin?) eril/nötr isimlerde des/der artı sonda bir -s kullanır: des Mannes, der Frau.",
                    why="Farklı çekimler vardır çünkü Almanca, cinsiyet/hâl bilgisinin isim öbeğinde her zaman bir yerde görünmesini ister - ya artikelde ya sıfatta, asla tamamen kaybolmadan. Bu yüzden artikel 'zayıf' ya da yoksa, daha belirgin bir ekle 'güçlenen' sıfattır.",
                    history="Bu çekim sistemi, Proto-Germencenin daha tekdüze bir sisteminden tarihsel olarak gelişmiştir: zaten çok bilgi veren belirli artikel, sıfatı hâl ve cinsiyeti yeniden belirtmekten 'kurtarır', artikel yokken ise sıfat bunu tek başına yapar. Genitiv, Modern Almancada en eski ve en çok aşınmış hâldir: konuşma dilinde sık sık von + dativ ile değiştirilir.",
                    tip="Tüm tabloları birden ezberlemeye çalışma: en basit olan (neredeyse her zaman -e ya da -en) der/die/das'tan sonraki ekle başla, diğerlerini yalnızca bu otomatikleştiğinde ekle.",
                    summary="der/die/das'tan sonra sıfat neredeyse her zaman -e alır; ein'dan sonra cinsiyet ve hâli kendisi 'telafi etmelidir'.",
                ),
                ("Der kleine Hund schläft.", "Ich habe einen kleinen Hund."),
                ("Artikel", "Maskulin", "Feminin", "Neutrum"),
                (
                    ("der/die/das (schwach)", "-e", "-e", "-e"),
                    ("ein/eine (gemischt)", "-er", "-e", "-es"),
                ),
            ),
        ],
    },
    "B2": {
        "colour": "B2",
        "title": {"it": "Precisione, registro e argomentazione", "en": "Precision, register and argument", "es": "Precisión, registro y argumentación", "tr": "Kesinlik, üslup ve sav"},
        "can": {"it": "Sostenere un punto di vista, comprendere testi complessi e scrivere in modo formale e strutturato.", "en": "Support a viewpoint, understand complex texts and write with a formal, structured style.", "es": "Defender un punto de vista, comprender textos complejos y escribir de forma formal y estructurada.", "tr": "Bir görüşü desteklemek, karmaşık metinleri anlamak ve resmî, düzenli yazmak."},
        "topics": [
            Topic(
                "1 · Konjunktiv I e fonti",
                Explanation(
                    rule="Il Konjunktiv I (ich komme → er komme, ich habe → er habe, ich sei…) segnala il discorso riportato: chi scrive riferisce l'affermazione di un'altra fonte senza sottoscriverla come propria. È la forma standard nel giornalismo per distinguere «ciò che è stato detto» da «ciò che il narratore conferma».",
                    why="Usare il Konjunktiv I non serve a complicare il testo: serve a rendere trasparente chi afferma cosa. Se un giornale scrive «die Firma erklärt, sie habe reagiert» (congiuntivo), riporta la versione dell'azienda senza garantirne la veridicità; con l'indicativo la presenterebbe come fatto certo.",
                    history="Il Konjunktiv I discende dall'antico congiuntivo del proto-germanico, un tempo presente in tutta la coniugazione tedesca, come in latino o italiano. Nel tedesco parlato si è ristretto, sopravvivendo quasi solo in questa funzione — il discorso riportato — specialmente nello scritto giornalistico.",
                    tip="Nella lingua parlata quotidiana il Konjunktiv I viene spesso sostituito dal Konjunktiv II o da dass + indicativo: non aspettarti di sentirlo spesso in una conversazione informale, ma riconoscilo nei testi scritti formali.",
                    summary="Il Konjunktiv I riporta un'affermazione altrui senza confermarla come vera: è la firma grammaticale del «si dice che».",
                ),
                Explanation(
                    rule="Konjunktiv I (ich komme → er komme, ich habe → er habe, ich sei…) marks reported speech: the writer relays another source's statement without endorsing it. It's the standard form in journalism for distinguishing 'what was said' from 'what the narrator confirms'.",
                    why="Using Konjunktiv I isn't about complexity: it makes clear who is claiming what. If a newspaper writes 'die Firma erklärt, sie habe reagiert' (subjunctive), it reports the company's version without vouching for it; the indicative would present it as established fact.",
                    history="Konjunktiv I descends from the old Proto-Germanic subjunctive, once present throughout German conjugation, as in Latin or Italian. In spoken German it narrowed, surviving mainly in this function - reported speech - especially in journalistic writing.",
                    tip="In everyday spoken German, Konjunktiv I is often replaced by Konjunktiv II or dass + indicative: don't expect to hear it often in casual conversation, but recognise it in formal written texts.",
                    summary="Konjunktiv I reports someone else's claim without endorsing it as true: it's the grammatical signature of 'reportedly'.",
                ),
                Explanation(
                    rule="El Konjunktiv I (ich komme → er komme, ich habe → er habe, ich sei…) marca el discurso referido: quien escribe transmite la afirmación de otra fuente sin hacerla suya. Es la forma estándar en el periodismo para distinguir 'lo que se dijo' de 'lo que el narrador confirma'.",
                    why="Usar el Konjunktiv I no complica el texto: deja claro quién afirma qué. Si un periódico escribe 'die Firma erklärt, sie habe reagiert' (subjuntivo), reporta la versión de la empresa sin garantizarla; el indicativo la presentaría como hecho establecido.",
                    history="El Konjunktiv I desciende del antiguo subjuntivo protogermánico, presente en toda la conjugación alemana, como en latín o español. En el alemán hablado se restringió, sobreviviendo casi solo en esta función, especialmente en lo escrito periodístico.",
                    tip="En la lengua hablada cotidiana, el Konjunktiv I suele sustituirse por el Konjunktiv II o dass + indicativo: no esperes oírlo a menudo en una conversación informal, pero reconócelo en textos escritos formales.",
                    summary="El Konjunktiv I reporta una afirmación ajena sin avalarla como cierta: es la firma gramatical del 'según dicen'.",
                ),
                Explanation(
                    rule="Konjunktiv I (ich komme → er komme, ich habe → er habe, ich sei…) aktarılan konuşmayı işaretler: yazan kişi başka bir kaynağın ifadesini benimsemeden aktarır. Gazetecilikte 'söylenen' ile 'anlatıcının onayladığı'nı ayırmak için standart biçimdir.",
                    why="Konjunktiv I kullanmak metni karmaşıklaştırmaz: kimin neyi iddia ettiğini şeffaf kılar. Bir gazete 'die Firma erklärt, sie habe reagiert' yazarsa, şirketin versiyonunu garanti etmeden aktarır; bildirme kipi bunu kesin gerçek olarak sunardı.",
                    history="Konjunktiv I, bir zamanlar tüm Almanca çekimde -Latince ya da İtalyancada olduğu gibi- bulunan eski Proto-Germen dilek kipinden gelir. Konuşma dilinde daralmış, neredeyse yalnızca bu işlevde, özellikle gazetecilik yazısında hayatta kalmıştır.",
                    tip="Günlük konuşma dilinde Konjunktiv I çoğunlukla Konjunktiv II ya da dass + bildirme kipiyle değiştirilir: gündelik sohbette sık duymayı bekleme, ama resmî yazılı metinlerde tanı.",
                    summary="Konjunktiv I, başkasının iddiasını doğru olarak onaylamadan aktarır: 'söylenene göre'nin dilbilgisel imzasıdır.",
                ),
                ("Die Firma erklärt, sie habe reagiert.", "Er sagte, er sei zufrieden."),
                ("Person", "sein", "haben"),
                (
                    ("ich", "sei", "habe"),
                    ("du", "seist", "habest"),
                    ("er / sie / es", "sei", "habe"),
                    ("wir", "seien", "haben"),
                    ("ihr", "seiet", "habet"),
                    ("sie / Sie", "seien", "haben"),
                ),
            ),
            Topic(
                "2 · Konjunktiv II e diplomazia",
                Explanation(
                    rule="Il Konjunktiv II (würde + infinito, oppure hätte, wäre, könnte…) esprime ipotesi, desideri, critiche caute e proposte diplomatiche. La forma perifrastica con würde ha in gran parte sostituito le forme sintetiche originarie, tranne per i verbi più frequenti (sein→wäre, haben→hätte, i modali).",
                    why="Il registro non è un dettaglio: usare il Konjunktiv II invece dell'indicativo trasforma un'affermazione diretta in un suggerimento, rendendola meno impositiva. Utile in contesti professionali o delicati, dove vuoi proporre senza ordinare.",
                    history="würde è storicamente la forma di Konjunktiv II dello stesso verbo werden («diventare»), riusata come ausiliare per il condizionale di altri verbi — un processo comune tra le lingue (l'inglese 'would' ha una storia parallela). Il Konjunktiv II sintetico è quindi più antico; würde è l'innovazione che lo ha sostituito.",
                    tip="Non usare würde con sein e haben nello scritto standard: «ich würde sein» suona goffo, la forma corretta resta wäre. Riserva würde ai verbi senza una forma sintetica comune.",
                    summary="würde copre i verbi «comuni»; sein, haben e i modali preferiscono la propria forma sintetica (wäre, hätte, könnte).",
                ),
                Explanation(
                    rule="Konjunktiv II (würde + infinitive, or hätte, wäre, könnte…) expresses hypotheses, wishes, tactful criticism and diplomatic proposals. The periphrastic würde form has largely replaced the original synthetic forms, except for the most frequent verbs (sein→wäre, haben→hätte, the modals).",
                    why="Register isn't a detail: using Konjunktiv II instead of the indicative turns a direct statement into a suggestion, making it less imposing. Useful in professional or delicate contexts where you want to propose rather than order.",
                    history="würde is historically the Konjunktiv II form of werden ('to become'), reused as an auxiliary for the conditional of other verbs - a common process across languages (English 'would' has a parallel history). The synthetic Konjunktiv II is older; würde is the innovation that replaced it.",
                    tip="Don't use würde with sein and haben in standard writing: 'ich würde sein' sounds clumsy - the correct form remains wäre. Save würde for verbs without a common synthetic form.",
                    summary="würde covers 'ordinary' verbs; sein, haben and the modals keep their own synthetic form (wäre, hätte, könnte).",
                ),
                Explanation(
                    rule="El Konjunktiv II (würde + infinitivo, o hätte, wäre, könnte…) expresa hipótesis, deseos, críticas prudentes y propuestas diplomáticas. La forma perifrástica con würde ha sustituido en gran medida a las formas sintéticas originales, salvo los verbos más frecuentes (sein→wäre, haben→hätte, los modales).",
                    why="El registro no es un detalle: usar el Konjunktiv II en lugar del indicativo convierte una afirmación directa en una sugerencia, haciéndola menos impositiva. Útil en contextos profesionales o delicados donde se quiere proponer en vez de ordenar.",
                    history="würde es históricamente la forma de Konjunktiv II de werden ('llegar a ser'), reutilizada como auxiliar para el condicional de otros verbos: un proceso común entre lenguas. El Konjunktiv II sintético es más antiguo; würde es la innovación que lo sustituyó.",
                    tip="No uses würde con sein y haben en la escritura estándar: 'ich würde sein' suena forzado; la forma correcta sigue siendo wäre. Reserva würde para verbos sin una forma sintética común.",
                    summary="würde cubre los verbos 'comunes'; sein, haben y los modales prefieren su propia forma sintética (wäre, hätte, könnte).",
                ),
                Explanation(
                    rule="Konjunktiv II (würde + mastar, ya da hätte, wäre, könnte…) varsayımları, istekleri, nazik eleştirileri ve diplomatik önerileri ifade eder. würde ile kurulan çevresel biçim, en sık kullanılan fiiller (sein→wäre, haben→hätte, modaller) dışında özgün yalın biçimlerin yerini büyük ölçüde almıştır.",
                    why="Üslup bir ayrıntı değildir: bildirme kipi yerine Konjunktiv II kullanmak doğrudan bir ifadeyi bir öneriye dönüştürür, onu daha az dayatıcı kılar. Emretmek yerine önermek istediğin meslekî ya da hassas bağlamlarda yararlıdır.",
                    history="würde, tarihsel olarak werden'in kendi Konjunktiv II biçimidir ve diğer fiillerin şart kipi için yardımcı fiil olarak yeniden kullanılmıştır - diller arasında yaygın bir süreç. Yalın Konjunktiv II daha eskidir; würde onun yerini alan yeniliktir.",
                    tip="Standart yazıda sein ve haben ile würde kullanma: 'ich würde sein' beceriksizce durur; doğru biçim wäre olarak kalır. würde'yi yaygın yalın biçimi olmayan fiiller için sakla.",
                    summary="würde 'sıradan' fiilleri kapsar; sein, haben ve modaller kendi yalın biçimini (wäre, hätte, könnte) tercih eder.",
                ),
                ("Ich würde vorschlagen, dass wir …", "An Ihrer Stelle würde ich …"),
                ("th_verb", "Konjunktiv II", "mit würde"),
                (
                    ("sein", "wäre", "—"),
                    ("haben", "hätte", "—"),
                    ("kommen", "käme", "würde kommen"),
                    ("machen", "machte", "würde machen"),
                ),
            ),
            Topic(
                "3 · Argomentazione complessa",
                Explanation(
                    rule="Un'argomentazione complessa costruisce una tesi, definisce criteri, presenta prove concrete e anticipa un'obiezione. I connettori doppi (nicht nur…sondern auch, weder…noch, zwar…aber, einerseits…andererseits) rendono visibile la struttura logica del ragionamento, non solo il suo contenuto.",
                    why="Anticipare un'obiezione rende un'argomentazione più solida, non più debole: mostra che hai considerato il punto di vista opposto e hai comunque buone ragioni. zwar…aber fa esattamente questo: concede un punto per poi ribadire, con più forza, il proprio.",
                    history="Questa mossa retorica — concedere un punto per poi contrapporre l'argomento più forte — è nota fin dall'antichità classica, dove la retorica latina la formalizzava con costruzioni come quidem…sed. zwar…aber segue la stessa logica argomentativa, in tedesco.",
                    tip="Non abusare dei connettori doppi in un unico paragrafo: uno o due per risposta bastano a rendere visibile la struttura. Usarne troppi rende il testo macchinoso.",
                    summary="I connettori doppi rendono visibile la logica del ragionamento: uno o due per risposta, non di più.",
                ),
                Explanation(
                    rule="A complex argument builds a thesis, sets criteria, presents concrete evidence and anticipates an objection. Paired connectors (nicht nur…sondern auch, weder…noch, zwar…aber, einerseits…andererseits) make the logical structure of the reasoning visible, not just its content.",
                    why="Anticipating an objection makes an argument stronger, not weaker: it shows you've considered the opposing view and still have good reasons. zwar…aber does exactly this: it concedes a point, then reasserts your own with more force.",
                    history="This rhetorical move - conceding a point before countering with a stronger argument - has been known since classical antiquity, formalised in Latin rhetoric with constructions like quidem…sed. zwar…aber follows the same argumentative logic, in German.",
                    tip="Don't overuse paired connectors within a single paragraph: one or two per answer is enough to make the structure visible. Too many make the text cumbersome.",
                    summary="Paired connectors make the logic of an argument visible: one or two per answer, no more.",
                ),
                Explanation(
                    rule="Una argumentación compleja construye una tesis, fija criterios, presenta pruebas concretas y anticipa una objeción. Los conectores dobles (nicht nur…sondern auch, weder…noch, zwar…aber, einerseits…andererseits) hacen visible la estructura lógica del razonamiento, no solo su contenido.",
                    why="Anticipar una objeción hace una argumentación más sólida, no más débil: muestra que has considerado el punto de vista contrario y aun así tienes buenas razones. zwar…aber hace justo esto: concede un punto y luego reafirma el propio con más fuerza.",
                    history="Este movimiento retórico -conceder un punto antes de contraponer el argumento más fuerte- se conoce desde la antigüedad clásica, formalizado en la retórica latina con quidem…sed. zwar…aber sigue la misma lógica, en alemán.",
                    tip="No abuses de los conectores dobles en un mismo párrafo: uno o dos por respuesta bastan. Usar demasiados vuelve el texto engorroso.",
                    summary="Los conectores dobles hacen visible la lógica del razonamiento: uno o dos por respuesta, no más.",
                ),
                Explanation(
                    rule="Karmaşık bir tartışma bir tez kurar, ölçütler belirler, somut kanıtlar sunar ve bir itirazı önceden karşılar. Çift bağlaçlar (nicht nur…sondern auch, weder…noch, zwar…aber, einerseits…andererseits) akıl yürütmenin mantıksal yapısını görünür kılar.",
                    why="Bir itirazı önceden karşılamak bir tartışmayı zayıflatmaz, güçlendirir: karşıt görüşü dikkate aldığını ve yine de iyi nedenlerin olduğunu gösterir. zwar…aber tam olarak bunu yapar: bir puan verir, sonra kendi görüşünü daha güçlü sunar.",
                    history="Bir puanı kabul edip daha güçlü argümanla karşılık verme hamlesi, klasik Latin retoriğinin quidem…sed ile biçimlendirdiği antik çağdan beri bilinir. zwar…aber, Almanca içinde aynı mantığı izler.",
                    tip="Tek bir paragrafta çift bağlaçları fazla kullanma: cevap başına bir ya da iki tanesi yeterlidir. Çok fazlası metni hantallaştırır.",
                    summary="Çift bağlaçlar akıl yürütmenin mantığını görünür kılar: cevap başına bir ya da iki tane, daha fazla değil.",
                ),
                ("Zwar ist die Lösung teuer, aber sie ist nachhaltig.", "Nicht nur die Kosten, sondern auch die Qualität zählt."),
                ("th_conjunction", "th_function"),
                (
                    ("nicht nur … sondern auch", "additiv"),
                    ("weder … noch", "negativ"),
                    ("zwar … aber", "konzessiv"),
                    ("einerseits … andererseits", "kontrastiv"),
                ),
            ),
            Topic(
                "4 · Nominalizzazione e stile",
                Explanation(
                    rule="I testi amministrativi e tecnici comprimono spesso un'azione in un nome (die Durchführung invece di durchführen). Riconoscere una nominalizzazione significa saperla «srotolare» mentalmente nel verbo e nei suoi argomenti per capire davvero la frase.",
                    why="Il Nominalstil rende un testo più compatto e apparentemente più oggettivo, perché nasconde chi compie l'azione dietro un sostantivo astratto. Molto comune in ambito burocratico e scientifico, va usato con misura anche da chi scrive.",
                    history="Il Nominalstil si è affermato a partire dal linguaggio accademico e amministrativo tedesco del diciannovesimo secolo (Wissenschaftssprache/Verwaltungssprache), un registro che ha privilegiato compattezza e distacco impersonale.",
                    tip="Quando leggi un testo tecnico e fai fatica, trasforma ogni nominalizzazione nel verbo corrispondente (die Durchführung der Prüfung → wer führt die Prüfung durch?): spesso la frase diventa subito più chiara.",
                    summary="Ogni nominalizzazione si può «srotolare» in un verbo: farlo mentalmente chiarisce subito la frase.",
                ),
                Explanation(
                    rule="Administrative and technical texts often compress an action into a noun (die Durchführung instead of durchführen). Recognising a nominalisation means being able to mentally 'unroll' it into the verb and its arguments to really understand the sentence.",
                    why="Nominalstil makes a text more compact and seemingly more objective, hiding who performs the action behind an abstract noun. Very common in bureaucratic and scientific writing, but should be used with restraint even by writers.",
                    history="Nominalstil became established from 19th-century German academic and administrative language onward (Wissenschaftssprache/Verwaltungssprache), a register favouring compactness and impersonal detachment.",
                    tip="When reading a technical text and struggling, turn each nominalisation back into its verb (die Durchführung der Prüfung → wer führt die Prüfung durch?): the sentence often becomes immediately clearer.",
                    summary="Every nominalisation can be 'unrolled' into a verb: doing so mentally clarifies the sentence at once.",
                ),
                Explanation(
                    rule="Los textos administrativos y técnicos suelen comprimir una acción en un sustantivo (die Durchführung en vez de durchführen). Reconocer una nominalización significa saber 'desenrollarla' mentalmente en el verbo y sus argumentos para entender la frase.",
                    why="El Nominalstil hace un texto más compacto y aparentemente más objetivo, ocultando quién realiza la acción tras un sustantivo abstracto. Muy frecuente en lo burocrático y científico, debe usarse con mesura incluso al escribir.",
                    history="El Nominalstil se consolidó a partir del lenguaje académico y administrativo alemán del siglo XIX (Wissenschaftssprache/Verwaltungssprache), un registro que privilegió la compacidad y el distanciamiento impersonal.",
                    tip="Al leer un texto técnico y costarte entenderlo, convierte cada nominalización en su verbo (die Durchführung der Prüfung → wer führt die Prüfung durch?): la frase suele volverse mucho más clara.",
                    summary="Cada nominalización se puede 'desenrollar' en un verbo: hacerlo mentalmente aclara la frase al instante.",
                ),
                Explanation(
                    rule="İdari ve teknik metinler bir eylemi sık sık bir isme sıkıştırır (durchführen yerine die Durchführung). Bir isimleştirmeyi tanımak, cümleyi anlamak için onu zihinde fiile ve ögelerine 'açabilmek' demektir.",
                    why="Nominalstil, eylemi kimin yaptığını soyut bir isim arkasında gizleyerek metni daha kompakt ve nesnel gösterir. Bürokratik ve bilimsel alanda çok yaygındır, yazan kişi de onu ölçülü kullanmalıdır.",
                    history="Nominalstil, on dokuzuncu yüzyıl Alman akademik ve idari dilinden (Wissenschaftssprache/Verwaltungssprache) itibaren yerleşmiştir; bu üslup kompaktlığı ve kişisel olmayan mesafeyi tercih etmiştir.",
                    tip="Teknik bir metni anlamakta zorlanınca, her isimleştirmeyi fiiline dönüştürmeyi dene (die Durchführung der Prüfung → wer führt die Prüfung durch?): cümle genelde birden çok netleşir.",
                    summary="Her isimleştirme bir fiile 'açılabilir': bunu zihinde yapmak cümleyi anında netleştirir.",
                ),
                ("Die Durchführung der Prüfung dauert …", "Wir treffen eine Entscheidung."),
                ("th_verb", "Nominalisierung"),
                (
                    ("durchführen", "die Durchführung"),
                    ("entscheiden", "die Entscheidung"),
                    ("prüfen", "die Prüfung"),
                    ("vergleichen", "der Vergleich"),
                ),
            ),
            Topic(
                "5 · Lettura specialistica",
                Explanation(
                    rule="Affronta articoli, istruzioni, grafici e corrispondenza professionale in tre passaggi: prima la tesi globale, poi i segnali linguistici (connettori, tempi verbali, marcatori di opinione), infine la verifica dei dettagli che ti servono davvero.",
                    why="Leggere un testo specialistico parola per parola è inefficiente: individuare prima la struttura generale ti permette di sapere dove cercare l'informazione di cui hai bisogno, invece di scovarla per caso in frasi complesse.",
                    history="La tendenza tedesca a formare lunghi sostantivi composti viene dal sistema di composizione molto produttivo ereditato dal proto-germanico: le lingue germaniche preferiscono unire parole in un blocco unico piuttosto che concatenarle con preposizioni.",
                    tip="Di fronte a un sostantivo composto lunghissimo, scomponilo dall'ultima parola (il nucleo di significato) verso la prima (i modificatori), come faresti con le parentesi in matematica.",
                    summary="Scomponi i composti dall'ultima parola (il nucleo) verso la prima (i modificatori), come con le parentesi.",
                ),
                Explanation(
                    rule="Approach articles, instructions, charts and professional correspondence in three passes: first the overall claim, then linguistic signals (connectors, tenses, opinion markers), finally the details you actually need.",
                    why="Reading a specialist text word by word is inefficient: identifying the overall structure first tells you where to look for the information you need, instead of stumbling on it by chance in complex sentences.",
                    history="German's tendency to form long compound nouns comes from the highly productive compounding system inherited from Proto-Germanic: Germanic languages prefer joining words into a single block rather than chaining them with prepositions.",
                    tip="Faced with a very long compound noun, break it down from the last word (the core meaning) back to the first (the modifiers), exactly as with brackets in maths.",
                    summary="Break compounds down from the last word (the core) back to the first (the modifiers), like brackets in maths.",
                ),
                Explanation(
                    rule="Aborda artículos, instrucciones, gráficos y correspondencia profesional en tres pasos: primero la tesis global, luego las señales lingüísticas (conectores, tiempos verbales, marcadores de opinión), por último los detalles que necesitas.",
                    why="Leer un texto especializado palabra por palabra es ineficiente: identificar antes la estructura general permite saber dónde buscar la información necesaria, en vez de encontrarla por casualidad en frases complejas.",
                    history="La tendencia alemana a formar sustantivos compuestos largos proviene del sistema de composición muy productivo heredado del protogermánico: las lenguas germánicas prefieren unir palabras en un bloque en vez de encadenarlas con preposiciones.",
                    tip="Ante un sustantivo compuesto larguísimo, descompónlo desde la última palabra (el núcleo) hacia la primera (los modificadores), igual que con los paréntesis en matemáticas.",
                    summary="Descompón los compuestos desde la última palabra (el núcleo) hacia la primera (los modificadores), como paréntesis.",
                ),
                Explanation(
                    rule="Makaleleri, talimatları, grafikleri ve meslekî yazışmaları üç adımda ele al: önce genel tez, sonra dilsel işaretler (bağlaçlar, zamanlar, görüş belirteçleri), son olarak gerçekten ihtiyacın olan ayrıntılar.",
                    why="Uzman bir metni kelime kelime okumak verimsizdir: önce genel yapıyı belirlemek, ihtiyacın olan bilgiyi karmaşık cümlelerde rastlantıyla bulmak yerine nerede arayacağını bilmeni sağlar.",
                    history="Almancanın uzun bileşik isimler kurma eğilimi, Proto-Germenceden miras kalan üretken bileşik sisteminden gelir: Germen dilleri kelimeleri edatlarla zincirlemek yerine tek bir blokta birleştirmeyi tercih eder.",
                    tip="Çok uzun bir bileşik isimle karşılaşınca, son kelimeden (anlamın çekirdeği) ilkine doğru parçalara ayır, tıpkı matematikte parantezlerde yaptığın gibi.",
                    summary="Bileşikleri son kelimeden (çekirdek) ilkine (belirleyiciler) doğru ayır, matematikteki parantezler gibi.",
                ),
                ("Aus der Grafik geht hervor, dass …", "Im Vergleich zum Vorjahr …"),
                ("th_word", "th_parts"),
                (
                    ("Arbeitszeitgesetz", "Arbeit + Zeit + Gesetz"),
                    ("Krankenversicherung", "Kranken + Versicherung"),
                    ("Hauptbahnhof", "Haupt + Bahnhof"),
                ),
            ),
            Topic(
                "6 · Produzione B2 e revisione",
                Explanation(
                    rule="A B2 produci testi come una Stellungnahme, un Beschwerde, una sintesi o una presentazione. La revisione finale segue una griglia in sei punti: compito, struttura, prove/esempi, coesione, accuratezza grammaticale, tono/registro.",
                    why="Una griglia esplicita serve perché, rileggendo il testo tutto insieme, è facile concentrarsi solo sui dettagli e perdere di vista problemi più grandi, come una struttura poco chiara. Controllare un aspetto alla volta evita questo rischio.",
                    history="Questo approccio per griglie separate è lo stesso usato professionalmente da traduttori e correttori di bozze, coerente con la logica del QCER (visto in B1): descrivere le competenze in modo scomponibile e verificabile.",
                    tip="Non revisionare tutto insieme in un'unica lettura: fai passaggi separati, uno per punto della griglia. È lento la prima volta, ma diventa rapido con la pratica.",
                    summary="Una griglia in punti separati batte sempre una rilettura generica: un aspetto alla volta, in ordine fisso.",
                ),
                Explanation(
                    rule="At B2 you produce texts like a Stellungnahme, a Beschwerde, a summary or a presentation. The final revision follows a six-point checklist: task, structure, evidence/examples, cohesion, grammatical accuracy, tone/register.",
                    why="An explicit checklist helps because, rereading a text all at once, it's easy to focus only on small details and lose sight of bigger issues like an unclear structure. Checking one aspect at a time avoids this risk.",
                    history="This separated-checklist approach is the same one professional translators and proofreaders use, consistent with the logic of the CEFR (seen at B1): describing skills in a breakable-down, verifiable way.",
                    tip="Don't revise everything in one read-through: do separate passes, one per checklist point. It's slow at first but becomes fast with practice.",
                    summary="A checklist with separate points always beats a generic reread: one aspect at a time, in a fixed order.",
                ),
                Explanation(
                    rule="En B2 produces textos como una Stellungnahme, una Beschwerde, un resumen o una presentación. La revisión final sigue una parrilla de seis puntos: tarea, estructura, pruebas/ejemplos, cohesión, precisión gramatical, tono/registro.",
                    why="Una parrilla explícita ayuda porque, al releer el texto todo junto, es fácil centrarse solo en los detalles y perder de vista problemas mayores, como una estructura poco clara. Comprobar un aspecto cada vez evita este riesgo.",
                    history="Este enfoque de parrillas separadas es el mismo que usan profesionalmente traductores y correctores, coherente con la lógica del MCER (visto en B1): describir las competencias de forma desglosable y verificable.",
                    tip="No revises todo junto en una sola lectura: haz pasadas separadas, una por punto de la parrilla. Es lento al principio, pero se vuelve rápido con la práctica.",
                    summary="Una parrilla con puntos separados vence siempre a una relectura genérica: un aspecto cada vez, en orden fijo.",
                ),
                Explanation(
                    rule="B2'de Stellungnahme, Beschwerde, özet ya da sunum gibi metinler üretirsin. Son gözden geçirme altı maddelik bir listeyi izler: görev, yapı, kanıt/örnekler, bağdaşım, dilbilgisel doğruluk, ton/üslup.",
                    why="Açık bir liste işe yarar, çünkü metni bir bütün olarak yeniden okurken yalnızca küçük ayrıntılara odaklanıp belirsiz bir yapı gibi büyük sorunları gözden kaçırmak kolaydır. Her seferinde bir yönü kontrol etmek bu riski önler.",
                    history="Bu ayrı kontrol listeleri yaklaşımı, profesyonel çevirmenlerin kullandığıyla aynıdır ve CEFR'in (B1'de görülen) mantığıyla tutarlıdır: yetkinlikleri parçalara ayrılabilir ve doğrulanabilir biçimde tanımlamak.",
                    tip="Her şeyi tek bir okumada birlikte gözden geçirme: liste maddesi başına ayrı bir geçiş yap. İlk başta yavaştır, ama pratikle hızlanır.",
                    summary="Ayrı maddeli bir liste her zaman genel bir yeniden okumadan üstündür: sabit sırayla, bir seferinde bir yön.",
                ),
                ("Abschließend lässt sich festhalten, dass …", "Ich bitte Sie daher um eine Stellungnahme."),
                ("th_step", "th_focus"),
                (
                    ("1", "Aufgabe"),
                    ("2", "Struktur"),
                    ("3", "Kohärenz"),
                    ("4", "Grammatik"),
                    ("5", "Register"),
                ),
            ),
            Topic(
                "7 · Verbi con preposizioni fisse",
                Explanation(
                    rule="Molti verbi tedeschi si combinano sempre con la stessa preposizione, che non è necessariamente quella «logica» per un italiano (warten AUF = aspettare, letteralmente «aspettare SU»; sich interessieren FÜR = interessarsi A, letteralmente «interessarsi PER»). Per riferirsi a questi complementi con un pronome, il tedesco usa un pronome avverbiale da-/wo- fuso con la preposizione: darauf (su questo/ciò), worauf (su cosa?), invece di «auf es»/«auf was», che non esistono per le cose (solo per le persone si usa preposizione + pronome normale: auf ihn).",
                    why="Questo sistema esiste perché il tedesco non permette a una preposizione di reggere direttamente un pronome neutro riferito a una cosa (non puoi dire «auf es»): la fusione da-/wo- + preposizione risolve il problema creando un'unica parola che funziona da complemento. Riconoscere questo schema ti permette di costruire qualsiasi domanda o riferimento su un verbo con preposizione, anche uno che non hai mai visto.",
                    history="Questi composti (Pronominaladverbien) derivano dagli stessi avverbi pronominali già incontrati nei connettori di B1 (damit = da+mit, wodurch = wo+durch): fanno parte della stessa famiglia produttiva di parole, applicata qui non a una congiunzione ma a un complemento verbale.",
                    tip="Il verbo tedesco e la sua preposizione fissa vanno imparati e ripassati sempre insieme, come fossero un'unica parola (warten auf, denken an, sich freuen über): tradurre la preposizione dall'italiano porta quasi sempre all'errore.",
                    summary="Per le cose usa da-/wo- + preposizione (darauf/worauf); per le persone, preposizione + pronome normale (auf ihn).",
                ),
                Explanation(
                    rule="Many German verbs always combine with the same preposition, which isn't necessarily the 'logical' one for an English speaker (warten AUF = to wait for, literally 'to wait ON'; sich interessieren FÜR = to be interested in, literally 'to be interested FOR'). To refer back to these complements with a pronoun, German uses a da-/wo- adverbial pronoun fused with the preposition: darauf (about that), worauf (about what?), instead of 'auf es'/'auf was', which don't exist for things (only for people do you use preposition + ordinary pronoun: auf ihn).",
                    why="This system exists because German doesn't allow a preposition to directly govern a neuter pronoun referring to a thing (you can't say 'auf es'): the da-/wo- + preposition fusion solves the problem by creating a single word that works as the complement. Recognising this pattern lets you build any question or reference about a verb-plus-preposition combo, even one you've never seen before.",
                    history="These compounds (Pronominaladverbien) come from the same pronominal adverbs already met in the B1 connectors (damit = da+mit, wodurch = wo+durch): they belong to the same productive word family, applied here not to a conjunction but to a verb complement.",
                    tip="A German verb and its fixed preposition must always be learned and reviewed together, as if they were a single word (warten auf, denken an, sich freuen über): translating the preposition from English almost always leads to a mistake.",
                    summary="For things use da-/wo- + preposition (darauf/worauf); for people, preposition + ordinary pronoun (auf ihn).",
                ),
                Explanation(
                    rule="Muchos verbos alemanes se combinan siempre con la misma preposición, que no es necesariamente la 'lógica' para un hispanohablante (warten AUF = esperar, literalmente 'esperar SOBRE'; sich interessieren FÜR = interesarse POR, literalmente 'interesarse PARA'). Para referirse a estos complementos con un pronombre, el alemán usa un pronombre adverbial da-/wo- fusionado con la preposición: darauf (sobre eso), worauf (¿sobre qué?), en vez de 'auf es'/'auf was', que no existen para las cosas (solo para personas se usa preposición + pronombre normal: auf ihn).",
                    why="Este sistema existe porque el alemán no permite que una preposición rija directamente un pronombre neutro referido a una cosa (no se puede decir 'auf es'): la fusión da-/wo- + preposición resuelve el problema creando una sola palabra que funciona como complemento. Reconocer este esquema te permite construir cualquier pregunta o referencia sobre un verbo con preposición, incluso uno que no hayas visto nunca.",
                    history="Estos compuestos (Pronominaladverbien) vienen de los mismos adverbios pronominales que ya viste en los conectores de B1 (damit = da+mit, wodurch = wo+durch): pertenecen a la misma familia productiva de palabras, aplicada aquí no a una conjunción sino a un complemento verbal.",
                    tip="El verbo alemán y su preposición fija hay que aprenderlos y repasarlos siempre juntos, como si fueran una sola palabra (warten auf, denken an, sich freuen über): traducir la preposición desde el español casi siempre lleva al error.",
                    summary="Para cosas usa da-/wo- + preposición (darauf/worauf); para personas, preposición + pronombre normal (auf ihn).",
                ),
                Explanation(
                    rule="Birçok Almanca fiil her zaman aynı edatla birleşir ve bu, bir Türkçe konuşan için 'mantıklı' olan edat olmak zorunda değildir (warten AUF = beklemek, tam olarak 'ÜZERİNDE beklemek'; sich interessieren FÜR = ilgilenmek, tam olarak 'İÇİN ilgilenmek'). Bu tümleçlere bir zamirle atıfta bulunmak için Almanca, edatla kaynaşmış bir da-/wo- zarf zamiri kullanır: darauf (onun hakkında), worauf (ne hakkında?) - 'auf es'/'auf was' nesneler için yoktur (sadece kişiler için edat + sıradan zamir kullanılır: auf ihn).",
                    why="Bu sistem, Almancanın bir edatın doğrudan bir şeye atıfta bulunan nötr bir zamiri yönetmesine izin vermemesinden doğar (auf es diyemezsin): da-/wo- + edat kaynaşması, tümleç işlevi gören tek bir kelime yaratarak sorunu çözer. Bu kalıbı tanımak, hiç görmediğin bir edatlı fiil hakkında bile herhangi bir soru ya da atıf kurmanı sağlar.",
                    history="Bu bileşikler (Pronominaladverbien), B1'deki bağlaçlarda zaten gördüğün aynı zamirsi zarflardan gelir (damit = da+mit, wodurch = wo+durch): burada bir bağlaca değil bir fiil tümlecine uygulanan aynı üretken kelime ailesine aittir.",
                    tip="Almanca fiil ve onun sabit edatı her zaman tek bir kelimeymiş gibi birlikte öğrenilmeli ve tekrar edilmelidir (warten auf, denken an, sich freuen über): edatı Türkçeden çevirmek neredeyse her zaman hataya yol açar.",
                    summary="Nesneler için da-/wo- + edat (darauf/worauf); kişiler için edat + sıradan zamir (auf ihn) kullan.",
                ),
                ("Ich warte auf den Bus.", "Worauf freust du dich?"),
                ("th_verb", "th_preposition", "th_example"),
                (
                    ("warten", "auf", "Ich warte auf den Bus."),
                    ("sich freuen", "über / auf", "Ich freue mich über das Geschenk."),
                    ("denken", "an", "Ich denke an dich."),
                    ("sich interessieren", "für", "Ich interessiere mich für Musik."),
                ),
            ),
        ],
    },
}


TOPIC_TITLES = {
    "it": {
        "A1": ["La frase principale", "Persone, sein e haben", "Articoli e accusativo", "Negazione e domande", "Verbi modali e separabili", "Tempo, numeri e routine", "Possessivi e imperativo"],
        "A2": ["Perfekt e biografia", "Dativo e accusativo", "Spazio e movimento", "Confrontare e motivare", "Frasi dipendenti introduttive", "Servizi, lavoro e salute", "Pronomi e verbi riflessivi"],
        "B1": ["Subordinate e coesione", "Passivo e processi", "Relative e precisione", "Opinione e discussione", "Bewerbung e lavoro", "Strategia d'esame B1", "Aggettivi declinati e genitivo"],
        "B2": ["Konjunktiv I e fonti", "Konjunktiv II e diplomazia", "Argomentazione complessa", "Nominalizzazione e stile", "Lettura specialistica", "Produzione B2 e revisione", "Verbi con preposizioni fisse"],
    },
    "en": {
        "A1": ["The main clause", "People, sein and haben", "Articles and accusative", "Negation and questions", "Modal and separable verbs", "Time, numbers and routines", "Possessives and imperative"],
        "A2": ["Perfect tense and biography", "Dative and accusative", "Space and movement", "Comparing and giving reasons", "Introductory subordinate clauses", "Services, work and health", "Reflexive pronouns and verbs"],
        "B1": ["Subordinate clauses and cohesion", "Passive voice and processes", "Relative clauses and precision", "Opinion and discussion", "Applications and work", "B1 exam strategy", "Adjective endings and genitive"],
        "B2": ["Konjunktiv I and sources", "Konjunktiv II and diplomacy", "Complex argument", "Nominalisation and style", "Specialist reading", "B2 production and revision", "Verbs with fixed prepositions"],
    },
    "es": {
        "A1": ["La oración principal", "Personas, sein y haben", "Artículos y acusativo", "Negación y preguntas", "Modales y verbos separables", "Tiempo, números y rutinas", "Posesivos e imperativo"],
        "A2": ["Perfekt y biografía", "Dativo y acusativo", "Espacio y movimiento", "Comparar y justificar", "Subordinadas iniciales", "Servicios, trabajo y salud", "Pronombres y verbos reflexivos"],
        "B1": ["Subordinadas y cohesión", "Pasiva y procesos", "Relativas y precisión", "Opinión y debate", "Solicitud y trabajo", "Estrategia de examen B1", "Adjetivos declinados y genitivo"],
        "B2": ["Konjunktiv I y fuentes", "Konjunktiv II y diplomacia", "Argumentación compleja", "Nominalización y estilo", "Lectura especializada", "Producción y revisión B2", "Verbos con preposiciones fijas"],
    },
    "tr": {
        "A1": ["Ana cümle", "Kişiler, sein ve haben", "Artikeller ve Akkusativ", "Olumsuzluk ve sorular", "Modal ve ayrılabilen fiiller", "Zaman, sayılar ve rutinler", "İyelikler ve emir kipi"],
        "A2": ["Perfekt ve yaşam öyküsü", "Dativ ve Akkusativ", "Mekân ve hareket", "Karşılaştırma ve gerekçe", "Giriş düzeyi yan cümleler", "Hizmetler, iş ve sağlık", "Dönüşlü zamirler ve fiiller"],
        "B1": ["Yan cümleler ve bağdaşım", "Edilgen yapı ve süreçler", "İlgi cümleleri ve kesinlik", "Görüş ve tartışma", "Başvuru ve iş", "B1 sınav stratejisi", "Sıfat çekimi ve genitiv"],
        "B2": ["Konjunktiv I ve kaynaklar", "Konjunktiv II ve nezaket", "Karmaşık tartışma", "İsimleştirme ve üslup", "Uzmanlık okuması", "B2 üretim ve gözden geçirme", "Sabit edatlı fiiller"],
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


# I 18 nuclei grammaticali per livello producono 54 varianti di controllo
# ciascuno: con 80 verifiche lessicali si arriva esattamente a 134 × 4 = 536.
GRAMMAR_FACTS = {
    "A1": [
        (
            "Wo steht das finite Verb im einfachen Hauptsatz?",
            "Du schreibst eine SMS und korrigierst dich selbst: In «Heute ich lerne Deutsch» hast du das Verb falsch platziert. An welcher Position sollte es stehen?",
            "Formulieren Sie die Regel: Welche feste Position hat das konjugierte Verb in einem deutschen Aussagesatz?",
            "an zweiter Stelle", ["am Satzende", "immer an erster Stelle"],
        ),
        (
            "Welche Form ist richtig? Ich ___ aus Italien.",
            "Du stellst dich in einem Sprachcafé vor und nennst deine Herkunft. Wie ergänzt du: «Ich ___ aus Italien»?",
            "Bestimmen Sie die korrekte Verbform der ersten Person Singular von kommen im Satz: Ich ___ aus Italien.",
            "komme", ["kommt", "kommen"],
        ),
        (
            "Welcher Artikel gehört zu Hund?",
            "Im Wörterbuch findest du das Wort «Hund» ohne Artikel. Welchen Artikel notierst du dazu in deinem Vokabelheft?",
            "Welcher bestimmte Artikel ist im Nominativ dem Substantiv Hund zugeordnet?",
            "der", ["die", "das"],
        ),
        (
            "Wie lautet der Akkusativ von der Kaffee?",
            "Im Café bestellst du etwas: «Ich möchte ___ Kaffee, bitte.» Welche Form von der Kaffee brauchst du hier?",
            "Bilden Sie den Akkusativ Singular von der Kaffee.",
            "den Kaffee", ["dem Kaffee", "der Kaffee"],
        ),
        (
            "Welche Verneinung passt? Ich habe ___ Auto.",
            "Ein Freund fragt, ob du mit dem Auto kommst. Du hast keins: Wie verneinst du «Ich habe ___ Auto»?",
            "Welche Verneinungsform ist bei einem unbestimmten Substantiv wie Auto grammatisch korrekt?",
            "kein", ["nicht", "nie"],
        ),
        (
            "Wie beginnt eine Ja/Nein-Frage?",
            "Du willst wissen, ob dein Kollege heute Zeit hat, und formulierst eine Ja/Nein-Frage. Womit beginnt dieser Fragetyp im Deutschen?",
            "Welches Element steht an erster Position in einer deutschen Entscheidungsfrage (Ja/Nein-Frage)?",
            "mit dem Verb", ["mit dem Subjekt", "mit weil"],
        ),
        (
            "Was ist korrekt? Heute ___ ich Deutsch.",
            "Du erzählst von deinem Tagesplan und beginnst den Satz mit der Zeitangabe: «Heute ___ ich Deutsch.» Welche Form passt?",
            "Bestimmen Sie die korrekte Verbform der ersten Person Singular von lernen im Satz: Heute ___ ich Deutsch.",
            "lerne", ["lernst", "lernen"],
        ),
        (
            "Welche Pluralform ist richtig? das Kind -",
            "Auf dem Spielplatz zählst du: «Da sind viele ___.» Wie lautet der Plural von das Kind?",
            "Bilden Sie den Plural von das Kind.",
            "die Kinder", ["die Kinden", "der Kinder"],
        ),
        (
            "Welche W-Frage fragt nach einem Ort?",
            "Du hast dein Buch verloren und möchtest wissen, wo es ist. Welches Fragewort verwendest du?",
            "Welches W-Fragewort fragt spezifisch nach einem Ort?",
            "Wo?", ["Wann?", "Warum?"],
        ),
        (
            "Was passiert mit einkaufen im Hauptsatz?",
            "Du planst deinen Samstag: «Ich ___ am Samstag ___.» (einkaufen). Was passiert mit dem Präfix ein- im Hauptsatz?",
            "Beschreiben Sie das Verhalten des trennbaren Präfixes von einkaufen in einem einfachen Hauptsatz.",
            "Der Präfix steht am Ende.", ["Der Präfix verschwindet.", "Nichts trennt sich."],
        ),
        (
            "Welche Anrede ist formell?",
            "Du sprichst zum ersten Mal mit deiner neuen Chefin. Welche Anrede ist hier angemessen?",
            "Welches Personalpronomen wird im Deutschen als formelle Anrede verwendet?",
            "Sie", ["du", "ihr"],
        ),
        (
            "Welche Uhrzeit ist 08:15?",
            "Dein Zug fährt um 08:15 Uhr. Wie sagst du diese Uhrzeit auf Deutsch?",
            "Formulieren Sie die Uhrzeit 08:15 in Worten.",
            "Viertel nach acht", ["Viertel vor acht", "halb acht"],
        ),
        (
            "Welche Form ist korrekt? Ich ___ einen Bruder.",
            "Du erzählst von deiner Familie: «Ich ___ einen Bruder.» Welches Verb und welche Form passen hier?",
            "Bestimmen Sie die korrekte Form von haben in der ersten Person Singular: Ich ___ einen Bruder.",
            "habe", ["bin", "hat"],
        ),
        (
            "Wie heißt die höfliche Bitte?",
            "Du brauchst Hilfe von einer fremden Person auf der Straße. Wie formulierst du eine höfliche Bitte?",
            "Welche Satzstruktur entspricht einer höflichen Bitte mit einem Modalverb?",
            "Können Sie bitte helfen?", ["Sie können bitte helfen.", "Bitte Sie helfen können."],
        ),
        (
            "Welche Zahl schreibt man zusammen?",
            "Du schreibst eine Zahl in einem Brief aus: Wie schreibt man 21 auf Deutsch als ein einziges Wort?",
            "Welche Schreibweise der Zahl 21 ist im Deutschen orthographisch korrekt?",
            "einundzwanzig", ["zwanzigeins", "einsundzwanzig"],
        ),
        (
            "Welches Possessivartikel passt? Das ist ___ Bruder. (ich)",
            "Du zeigst ein Familienfoto und stellst jemanden vor: «Das ist ___ Bruder.» (du sprichst über deinen eigenen Bruder). Welche Form passt?",
            "Bestimmen Sie das korrekte Possessivartikel der ersten Person Singular vor einem maskulinen Substantiv: Das ist ___ Bruder.",
            "mein", ["meine", "meinen"],
        ),
        (
            "Wie lautet der Imperativ (Sie-Form) von kommen?",
            "Du begrüßt einen Gast an der Tür und bittest ihn höflich hereinzukommen. Wie lautet die Sie-Form des Imperativs von kommen?",
            "Bilden Sie den Imperativ der Sie-Form von kommen.",
            "Kommen Sie!", ["Komm!", "Kommt!"],
        ),
        (
            "Welche Form ist der Imperativ (du-Form) von sprechen?",
            "Du ermutigst einen Freund, lauter zu reden. Wie lautet die du-Form des Imperativs von sprechen (mit Vokalwechsel)?",
            "Bilden Sie den Imperativ der du-Form des Verbs mit Vokalwechsel sprechen.",
            "Sprich!", ["Sprech!", "Sprichst!"],
        ),
    ],
    "A2": [
        (
            "Welches Hilfsverb passt? Ich ___ nach Hause gegangen.",
            "Du erzählst, wie dein Tag gestern endete: «Ich ___ nach Hause gegangen.» Welches Hilfsverb brauchst du, weil gehen eine Bewegung ausdrückt?",
            "Bestimmen Sie das korrekte Hilfsverb im Perfekt für das Bewegungsverb gehen: Ich ___ nach Hause gegangen.",
            "bin", ["habe", "werde"],
        ),
        (
            "Welches Hilfsverb passt? Ich ___ Deutsch gelernt.",
            "Du sprichst über deine letzten Monate: «Ich ___ Deutsch gelernt.» Welches Hilfsverb passt hier, da lernen keine Bewegung ist?",
            "Bestimmen Sie das korrekte Hilfsverb im Perfekt für das Verb lernen: Ich ___ Deutsch gelernt.",
            "habe", ["bin", "werde"],
        ),
        (
            "Wo? Das Buch liegt ___ Tisch.",
            "Du beschreibst dein Arbeitszimmer: «Das Buch liegt ___ Tisch.» Es befindet sich dort, es bewegt sich nicht. Welche Form passt?",
            "Bestimmen Sie Präposition und Artikel für die Ortsangabe (Wo?): Das Buch liegt ___ Tisch.",
            "auf dem", ["auf den", "in den"],
        ),
        (
            "Wohin? Ich lege das Buch ___ Tisch.",
            "Du räumst dein Arbeitszimmer auf und legst ein Buch hin: «Ich lege das Buch ___ Tisch.» Welche Form passt, weil hier eine Bewegung stattfindet?",
            "Bestimmen Sie Präposition und Artikel für die Richtungsangabe (Wohin?): Ich lege das Buch ___ Tisch.",
            "auf den", ["auf dem", "bei dem"],
        ),
        (
            "Welcher Modalverb drückt Pflicht aus?",
            "Dein Chef sagt dir, dass ein Bericht heute fertig sein muss - keine Option, sondern eine Pflicht. Welches Modalverb passt zu dieser Situation?",
            "Welches Modalverb drückt im Deutschen eine objektive Notwendigkeit oder Pflicht aus?",
            "müssen", ["können", "mögen"],
        ),
        (
            "Welche Perfektform ist richtig? fahren -",
            "Du erzählst von einer Reise: «Wir sind letzte Woche nach Hamburg ___.» Welches Partizip II von fahren brauchst du?",
            "Bilden Sie das Partizip II des starken Verbs fahren.",
            "gefahren", ["gefahrt", "gefahrten"],
        ),
        (
            "Welche Präposition passt? Ich warte ___ den Bus.",
            "Du stehst an der Haltestelle und erklärst, was du tust: «Ich warte ___ den Bus.» Welche Präposition gehört fest zu warten?",
            "Welche Präposition regiert das Verb warten in der Bedeutung 'erwarten'?",
            "auf", ["mit", "bei"],
        ),
        (
            "Welcher Satz ist ein Vergleich?",
            "Du vergleichst zwei Städte in einem Gespräch. Welcher der folgenden Sätze drückt einen korrekten Vergleich aus?",
            "Welcher Satz zeigt die korrekte Struktur eines Komparativs mit als im Deutschen?",
            "Berlin ist größer als Bonn.", ["Berlin ist groß Bonn.", "Berlin größer Bonn ist."],
        ),
        (
            "Welche Form ist der Superlativ von gut?",
            "Du bewertest mehrere Restaurants und willst das allerbeste hervorheben. Welche Form von gut brauchst du im Superlativ?",
            "Bilden Sie den Superlativ des unregelmäßigen Adjektivs gut.",
            "am besten", ["am gutesten", "besser"],
        ),
        (
            "Welcher Artikel steht nach mit?",
            "Du schreibst einen Satz mit der Präposition mit und musst den richtigen Fall wählen. Welchen Fall verlangt mit immer?",
            "Welchen Kasus regiert die Präposition mit unabhängig vom Kontext?",
            "Dativ", ["Akkusativ", "Nominativ"],
        ),
        (
            "Welche Ergänzung passt? Ich helfe ___ Mann.",
            "Ein älterer Herr braucht Hilfe beim Tragen. Du sagst: «Ich helfe ___ Mann.» Welche Form passt, weil helfen den Dativ verlangt?",
            "Bestimmen Sie die korrekte Dativform des bestimmten Artikels im Satz: Ich helfe ___ Mann.",
            "dem", ["den", "der"],
        ),
        (
            "Welche Ergänzung passt? Ich sehe ___ Mann.",
            "Du beschreibst, was du auf der Straße bemerkst: «Ich sehe ___ Mann.» Welche Form passt, weil sehen den Akkusativ verlangt?",
            "Bestimmen Sie die korrekte Akkusativform des bestimmten Artikels im Satz: Ich sehe ___ Mann.",
            "den", ["dem", "des"],
        ),
        (
            "Wie wird weil verwendet?",
            "Du erklärst einem Anfänger die Wortstellung nach weil. Was passiert dabei mit dem konjugierten Verb?",
            "Beschreiben Sie die Verbstellung im Nebensatz nach der Konjunktion weil.",
            "Das Verb steht am Ende.", ["Das Verb steht zuerst.", "Es steht kein Verb."],
        ),
        (
            "Welche Zeitangabe passt zum Perfekt?",
            "Du erzählst von gestern und möchtest das Perfekt korrekt verwenden. Welcher der folgenden Sätze ist grammatisch richtig?",
            "Welcher Satz zeigt die korrekte Perfektbildung mit haben in Verbindung mit einer Zeitangabe der Vergangenheit?",
            "Gestern habe ich gearbeitet.", ["Gestern arbeite ich gehabt.", "Gestern bin ich gearbeitet."],
        ),
        (
            "Welche Form ist höflich?",
            "Du brauchst Hilfe von einer unbekannten Person in einem Amt. Welche der folgenden Formulierungen ist höflich und grammatisch korrekt?",
            "Welche Satzform entspricht einer höflichen Bitte mit Konjunktiv II?",
            "Könnten Sie mir helfen?", ["Du hilfst mir?", "Sie helfen mich?"],
        ),
        (
            "Welches Reflexivpronomen passt? Ich freue ___ auf die Ferien.",
            "Du erzählst, wie sehr du dich auf den Urlaub freust: «Ich freue ___ auf die Ferien.» Welches Pronomen passt zur ersten Person?",
            "Bestimmen Sie das korrekte Reflexivpronomen der ersten Person Singular im Akkusativ: Ich freue ___ auf die Ferien.",
            "mich", ["mir", "mein"],
        ),
        (
            "Welches Reflexivpronomen passt zur dritten Person?",
            "Du beschreibst, wofür sich dein Kollege interessiert. Welches Reflexivpronomen brauchst du für er/sie/es?",
            "Welches Reflexivpronomen wird in der dritten Person Singular und Plural verwendet, unabhängig vom Kasus?",
            "sich", ["ihn", "ihm"],
        ),
        (
            "Welche Form passt? Ich kaufe ___ etwas.",
            "Du gehst einkaufen und erzählst, dass du dir selbst ein Geschenk machst: «Ich kaufe ___ etwas.» Warum steht hier der Dativ?",
            "Bestimmen Sie das korrekte Reflexivpronomen im Dativ der ersten Person Singular: Ich kaufe ___ etwas.",
            "mir", ["mich", "meins"],
        ),
    ],
    "B1": [
        (
            "Wo steht das Verb nach obwohl?",
            "Du schreibst einen Nebensatz mit obwohl und überlegst, wohin das konjugierte Verb gehört. Wo steht es?",
            "Beschreiben Sie die Verbstellung im Nebensatz, der durch die konzessive Konjunktion obwohl eingeleitet wird.",
            "am Ende der Nebensatz", ["immer auf Position eins", "direkt nach obwohl"],
        ),
        (
            "Wie bildet man Vorgangspassiv?",
            "Du beschreibst, dass eine Maschine gerade repariert wird, während der Prozess noch läuft. Wie bildest du dieses Passiv?",
            "Nennen Sie die Bildungsregel des Vorgangspassivs (Passiv des Prozesses) im Deutschen.",
            "werden + Partizip II", ["sein + Infinitiv", "haben + Partizip II"],
        ),
        (
            "Wie bildet man Zustandspassiv?",
            "Die Reparatur ist bereits abgeschlossen und du beschreibst nur noch das Ergebnis. Wie bildest du dieses Passiv?",
            "Nennen Sie die Bildungsregel des Zustandspassivs (Passiv des Ergebnisses) im Deutschen.",
            "sein + Partizip II", ["werden + Infinitiv", "haben + Partizip II"],
        ),
        (
            "Welche Form ist ein Relativpronomen im Dativ?",
            "Du beschreibst eine Person, der du geholfen hast: «Der Mann, ___ ich geholfen habe, …». Welche Form passt, weil helfen den Dativ verlangt?",
            "Bestimmen Sie das Relativpronomen im Dativ Maskulinum Singular.",
            "dem", ["den", "dessen"],
        ),
        (
            "Was gehört in eine Bewerbung?",
            "Du bereitest die Unterlagen für eine Stellenbewerbung vor. Welches Dokument erklärt, warum du für die Stelle geeignet bist?",
            "Welches Element ist fester Bestandteil einer vollständigen deutschen Bewerbungsmappe?",
            "ein Anschreiben", ["eine Speisekarte", "eine Fahrkarte"],
        ),
        (
            "Welche Einleitung drückt Meinung aus?",
            "Du möchtest in einer Diskussion höflich deine persönliche Sichtweise einleiten. Welche Formulierung passt?",
            "Welche Redewendung leitet im Deutschen typischerweise eine persönliche Meinung ein?",
            "Meiner Meinung nach …", ["Am Bahnhof nach …", "In der Küche nach …"],
        ),
        (
            "Welcher Konnektor nennt einen Grund?",
            "Du erklärst, warum du zu Hause geblieben bist, und brauchst einen kausalen Konnektor. Welcher passt?",
            "Welcher der folgenden Konnektoren drückt eine kausale Beziehung (einen Grund) aus?",
            "weil", ["obwohl", "während"],
        ),
        (
            "Welcher Konnektor nennt ein Ziel?",
            "Du erklärst den Zweck einer Handlung: «Ich lerne jeden Tag, ___ ich die Prüfung bestehe.» Welcher Konnektor passt?",
            "Welcher Konnektor drückt eine finale Beziehung (einen Zweck) aus?",
            "damit", ["denn", "oder"],
        ),
        (
            "Welche Form ist richtig? Das Auto ___ repariert.",
            "Die Werkstatt arbeitet gerade an deinem Auto. Wie beschreibst du diesen laufenden Vorgang im Passiv?",
            "Bestimmen Sie die korrekte Form des Vorgangspassivs im Satz: Das Auto ___ repariert.",
            "wird", ["hat", "ist werden"],
        ),
        (
            "Was verlangt trotz?",
            "Du schreibst einen Satz mit trotz und musst den passenden Fall wählen. Welchen Fall verlangt trotz meistens?",
            "Welchen Kasus regiert die Präposition trotz im heutigen Sprachgebrauch überwiegend?",
            "Dativ", ["Akkusativ", "Genitiv immer"],
        ),
        (
            "Welche Form passt: Ich interessiere mich ___ Technik.",
            "Du erzählst von deinen Interessen: «Ich interessiere mich ___ Technik.» Welche feste Präposition gehört zu diesem Verb?",
            "Welche Präposition bildet mit sich interessieren die feste Verbindung?",
            "für", ["an", "über"],
        ),
        (
            "Welche Form ist korrekt? Der Mann, ___ ich helfe, …",
            "Du beschreibst jemanden, dem du regelmäßig hilfst. Welches Relativpronomen passt, weil helfen den Dativ verlangt?",
            "Bestimmen Sie das korrekte Relativpronomen im Dativ im Satz: Der Mann, ___ ich helfe, …",
            "dem", ["den", "dessen"],
        ),
        (
            "Welche Schlussformel ist formell?",
            "Du beendest eine formelle E-Mail an eine Behörde. Welche Schlussformel ist angemessen?",
            "Welche Grußformel entspricht dem formellen Register in offizieller Korrespondenz?",
            "Mit freundlichen Grüßen", ["Bis später, Alter", "Tschüsschen"],
        ),
        (
            "Was bedeutet Arbeitszeugnis?",
            "Nach dem Ende deiner Stelle bittet dich dein Arbeitgeber, ein bestimmtes Dokument auszustellen. Was ist ein Arbeitszeugnis?",
            "Definieren Sie den Begriff Arbeitszeugnis im deutschen Arbeitskontext.",
            "Bewertung eines Arbeitsverhältnisses", ["Fahrkarte zur Arbeit", "Arbeitsplan für morgen"],
        ),
        (
            "Welche Strategie ist beim Schreiben sinnvoll?",
            "Du hast einen Text fertig geschrieben und überlegst, wie du am effektivsten überarbeitest. Welche Reihenfolge ist sinnvoll?",
            "Welche Revisionsstrategie gilt beim akademischen und beruflichen Schreiben als sinnvoll?",
            "erst Inhalt, dann sprachliche Revision", ["nur neue Wörter zählen", "nie den Text lesen"],
        ),
        (
            "Welche Endung hat das Adjektiv nach dem bestimmten Artikel? der klein__ Hund",
            "Du beschreibst einen Hund, den du gerade siehst, mit dem bestimmten Artikel: «der klein__ Hund.» Welche Endung passt fast immer nach der/die/das?",
            "Bestimmen Sie die Adjektivendung in der schwachen Deklination nach dem bestimmten Artikel im Nominativ.",
            "-e", ["-er", "-es"],
        ),
        (
            "Welche Endung hat das Adjektiv nach ein im Maskulinum Nominativ? ein klein__ Hund",
            "Diesmal beschreibst du den Hund ohne bestimmten Artikel: «ein klein__ Hund.» Welche Endung übernimmt hier die Information, die der Artikel nicht gibt?",
            "Bestimmen Sie die Adjektivendung in der gemischten Deklination nach ein im Nominativ Maskulinum.",
            "-er", ["-e", "-es"],
        ),
        (
            "Wie lautet der Genitiv von der Mann?",
            "Du beschreibst, wem ein Auto gehört: «Das ist das Auto ___ Mannes.» Welche Form von der Mann brauchst du im Genitiv?",
            "Bilden Sie den Genitiv Singular von der Mann.",
            "des Mannes", ["dem Mann", "den Mann"],
        ),
    ],
    "B2": [
        (
            "Wofür wird Konjunktiv I oft genutzt?",
            "Ein Journalist gibt die Aussage einer Politikerin wieder, ohne sie persönlich zu bestätigen. Welche Funktion erfüllt der Konjunktiv I hier?",
            "Nennen Sie die zentrale grammatische Funktion des Konjunktiv I im heutigen Deutsch.",
            "indirekte Rede", ["einfache Vergangenheit", "Pluralbildung"],
        ),
        (
            "Welche Form drückt eine höfliche Hypothese aus?",
            "Du möchtest in einer Besprechung eine Idee vorsichtig und höflich einbringen, ohne zu direkt zu wirken. Welche Formulierung passt?",
            "Welche Konstruktion mit Konjunktiv II drückt einen höflichen, hypothetischen Vorschlag aus?",
            "Ich würde vorschlagen …", ["Ich schlage gestern vor.", "Ich werde vorgeschlagen."],
        ),
        (
            "Welcher Doppelkonnektor bedeutet not only … but also?",
            "Du möchtest zwei positive Aspekte gleichzeitig hervorheben, ohne den zweiten abzuschwächen. Welcher Doppelkonnektor passt?",
            "Welcher deutsche Doppelkonnektor entspricht semantisch der englischen Struktur not only … but also?",
            "nicht nur … sondern auch", ["weder … noch", "zwar … aber"],
        ),
        (
            "Was bedeutet eine Entscheidung treffen?",
            "In einem formellen Text liest du die nominalisierte Wendung 'eine Entscheidung treffen'. Welches einfache Verb steckt dahinter?",
            "Welches Verb entspricht der Nominalisierung eine Entscheidung treffen?",
            "entscheiden", ["vergleichen", "ankommen"],
        ),
        (
            "Welche Textsorte verlangt eine begründete Position?",
            "Du sollst in der Prüfung zu einem kontroversen Thema schriftlich begründet Position beziehen. Welche Textsorte ist das?",
            "Welche Textsorte verlangt strukturell These, Argumente und eine begründete Schlussfolgerung?",
            "Stellungnahme", ["Einkaufsliste", "Fahrplan"],
        ),
        (
            "Welcher Ausdruck leitet eine Folgerung ein?",
            "Du hast gerade zwei Prämissen dargelegt und möchtest nun die logische Konsequenz formulieren. Welcher Konnektor passt?",
            "Welcher Konnektor markiert im Deutschen eine logische Schlussfolgerung (Konsekutivität)?",
            "folglich", ["hingegen", "zwar"],
        ),
        (
            "Was kennzeichnet einen guten B2-Absatz?",
            "Du überarbeitest einen Absatz für eine schriftliche Prüfung und prüfst, ob er strukturell vollständig ist. Was sollte er enthalten?",
            "Welche drei Elemente kennzeichnen einen strukturell vollständigen argumentativen Absatz auf B2-Niveau?",
            "These, Beleg und Schluss", ["nur ein Stichwort", "möglichst viele Ausrufezeichen"],
        ),
        (
            "Welche Form ist Konjunktiv II von haben?",
            "Du formulierst einen irrealen Bedingungssatz über die Vergangenheit: «Wenn ich mehr Zeit ___, …». Welche Form von haben brauchst du?",
            "Bilden Sie den Konjunktiv II von haben in der ersten Person Singular.",
            "hätte", ["habe", "hatte"],
        ),
        (
            "Welche Form ist Konjunktiv I von sein (er)?",
            "Du gibst eine fremde Aussage in indirekter Rede wieder: «Er sagte, er ___ zufrieden.» Welche Form von sein passt im Konjunktiv I?",
            "Bilden Sie den Konjunktiv I von sein in der dritten Person Singular.",
            "sei", ["wäre", "ist"],
        ),
        (
            "Was ist eine Nominalisierung?",
            "Du liest einen bürokratischen Text und bemerkst, dass Handlungen oft als Substantive erscheinen (die Durchführung, die Prüfung). Was nennt man dieses Verfahren?",
            "Definieren Sie den Begriff Nominalisierung im Kontext der deutschen Verwaltungs- und Wissenschaftssprache.",
            "eine Handlung als Nomen ausdrücken", ["ein Nomen streichen", "nur Verben benutzen"],
        ),
        (
            "Welche Präposition passt? abhängen ___",
            "Du erklärst, dass ein Ergebnis von mehreren Faktoren bestimmt wird: «Das Ergebnis hängt ___ vielen Faktoren ab.» Welche Präposition gehört fest zu abhängen?",
            "Welche Präposition bildet mit dem Verb abhängen die feste Verbindung?",
            "von", ["für", "durch"],
        ),
        (
            "Welche Wendung relativiert eine Aussage?",
            "Du möchtest eine Schlussfolgerung vorsichtig und wissenschaftlich formulieren, ohne zu kategorisch zu klingen. Welche Wendung passt?",
            "Welche Formulierung entspricht einem vorsichtigen, akademischen Register beim Formulieren einer Schlussfolgerung?",
            "Es lässt sich feststellen, dass …", ["Ich weiß alles!", "Das ist niemals wichtig."],
        ),
        (
            "Wozu dient ein Gegenargument?",
            "In deinem Aufsatz möchtest du zeigen, dass du auch die andere Seite kennst, bevor du deine eigene Position bekräftigst. Wozu dient dabei ein Gegenargument?",
            "Welche argumentative Funktion erfüllt die bewusste Einbindung eines Gegenarguments in einem B2-Text?",
            "die eigene Position differenziert prüfen", ["das Thema wechseln", "den Text kürzen"],
        ),
        (
            "Welche Form ist korrekt? Er sagte, er ___ krank.",
            "Du berichtest, was ein Kollege dir gesagt hat, ohne die Aussage selbst zu bestätigen: «Er sagte, er ___ krank.» Welche Form passt im Konjunktiv I?",
            "Bestimmen Sie die korrekte Form des Konjunktiv I von sein in der indirekten Rede: Er sagte, er ___ krank.",
            "sei", ["ist", "wäre gewesen immer"],
        ),
        (
            "Wie funktioniert zwar … aber?",
            "Du gibst zunächst einen Nachteil zu, bevor du einen wichtigeren Vorteil hervorhebst: «Zwar ist die Lösung teuer, aber sie ist nachhaltig.» Welches rhetorische Muster ist das?",
            "Welches argumentative Muster liegt der Konstruktion zwar … aber zugrunde?",
            "Konzession und Kontrast", ["zwei gleiche Gründe", "eine Zeitangabe"],
        ),
        (
            "Welche Präposition passt zu warten?",
            "Du stehst an der Bushaltestelle und beschreibst, was du tust: «Ich warte ___ den Bus.» Welche Präposition gehört fest zu warten?",
            "Welche Präposition bildet mit dem Verb warten die feste Verbindung?",
            "auf", ["für", "bei"],
        ),
        (
            "Welches Pronominaladverb fragt nach einer Sache mit auf?",
            "Ein Freund erzählt, er freue sich auf etwas, verrät aber nicht, worauf. Wie fragst du nach?",
            "Welches Pronominaladverb bildet die Frage nach einer Sache in Verbindung mit der Präposition auf?",
            "Worauf?", ["Auf was?", "Wofür?"],
        ),
        (
            "Wie verweist man auf eine Sache statt einer Person nach an?",
            "Du hast gerade über ein Problem gesprochen und möchtest im nächsten Satz kurz darauf zurückverweisen, ohne es zu wiederholen. Wie tust du das nach der Präposition an?",
            "Welche Konstruktion ersetzt «an + Pronomen» korrekt, wenn sich der Bezug auf eine Sache (nicht eine Person) richtet?",
            "daran", ["an es", "an das"],
        ),
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
            # "meaning" e "cloze" condividono lo stesso gruppo: in una prova ne può comparire
            # al più uno, mai entrambi, per non testare due volte la stessa identica parola.
            group = f"{level}-vocab-{position}"
            bank.append({"id": f"{level}-m-{position}", "level": level, "type": "meaning", "item": item,
                         "answer": item, "options": [item, *chosen], "group": group})
            bank.append({"id": f"{level}-c-{position}", "level": level, "type": "cloze", "item": item,
                         "answer": item, "options": [item, *chosen], "group": group})
        for index, (regelcheck, scenario, exam, answer, wrong) in enumerate(GRAMMAR_FACTS[level]):
            # Le 3 varianti riguardano la stessa regola con un testo realmente diverso l'uno
            # dall'altro (non solo un'etichetta diversa): condividono comunque un unico gruppo,
            # cosi la prova ne estrae al più una, mai due o tre versioni della stessa domanda.
            group = f"{level}-grammar-{index}"
            for label, question in (("Regelcheck", regelcheck), ("Mini-Szenario", scenario), ("Prüfungsfrage", exam)):
                bank.append({"id": f"{level}-g-{index}-{label}", "level": level, "type": "grammar",
                             "question": f"{label}: {question}", "answer": answer, "options": [answer, *wrong], "group": group})
    return bank


QUESTION_BANK = build_question_bank()
assert len(QUESTION_BANK) == 536, "La banca deve contenere esattamente 536 quesiti"
assert len({q['id'] for q in QUESTION_BANK}) == len(QUESTION_BANK), "Gli ID devono essere unici"


def sample_without_duplicates(pool: list[dict], amount: int) -> list[dict]:
    """Estrae al più un quesito per ogni gruppo (stessa parola o stessa regola di grammatica).
    Cosi, in una singola prova, nessuna domanda può mai comparire due volte - nemmeno in una
    forma leggermente diversa - perché il gruppo, non il singolo quesito, è l'unità di estrazione."""
    grouped: dict[str, list[dict]] = {}
    for question in pool:
        grouped.setdefault(question["group"], []).append(question)
    group_keys = list(grouped.keys())
    random.shuffle(group_keys)
    selected_keys = group_keys[:min(amount, len(group_keys))]
    return [random.choice(grouped[key]) for key in selected_keys]


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
        st.session_state[key] = sample_without_duplicates(pool, amount)
        st.session_state[token_key] = st.session_state.get(token_key, 0) + 1
        st.session_state.pop(f"test_{scope}_submitted", None)
        st.session_state.pop(f"test_{scope}_answers", None)
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
            exp: Explanation = getattr(topic, language)
            headers_html = "".join(f"<th>{html.escape(tx(h) if h.startswith('th_') else h)}</th>" for h in topic.table_headers)
            rows_html = "".join(
                "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>"
                for row in topic.table_rows
            )
            table_html = f"<table class='mini-table'><tr>{headers_html}</tr>{rows_html}</table>" if topic.table_rows else ""
            card = (
                f"<div class='card chapter'><h3>{html.escape(heading)}</h3>"
                f"<p><span class='smallcaps'>{html.escape(tx('theory_rule'))}</span><br>{html.escape(exp.rule)}</p>"
                f"<p><span class='smallcaps'>{html.escape(tx('theory_why'))}</span><br>{html.escape(exp.why)}</p>"
                f"<p><span class='smallcaps'>{html.escape(tx('theory_history'))}</span><br>{html.escape(exp.history)}</p>"
                f"{table_html}"
                f"<div class='note'><span class='smallcaps'>{html.escape(tx('theory_tip'))}</span><br>{html.escape(exp.tip)}</div>"
                f"<div class='summary-box'><span class='smallcaps'>{html.escape(tx('theory_summary'))}</span><br>{html.escape(exp.summary)}</div>"
                f"</div>"
            )
            st.markdown(card, unsafe_allow_html=True)
            examples = [{"de": line, "it": "Esempio da ascoltare", "en": "Listen to the example", "es": "Escucha el ejemplo", "tr": "Örneği dinleyin"} for line in topic.examples]
            speakable_grid(examples, language, columns=2, detail_key="translation")
            render_textbook_unit(st, level, topic_index, language)
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
der Auspuff|lo scarico|exhaust pipe|el tubo de escape|egzoz
die Lichtmaschine|l'alternatore|alternator|el alternador|alternatör
der Keilriemen|la cinghia|drive belt|la correa|kayış
die Achse|l'asse|axle|el eje|aks
der Stoßdämpfer|l'ammortizzatore|shock absorber|el amortiguador|amortisör
die Werkstatt|l'officina|workshop|el taller|atölye
der Schraubenschlüssel|la chiave inglese|wrench|la llave inglesa|ingiliz anahtarı
die Zange|la pinza|pliers|los alicates|pense
der Schraubenzieher|il cacciavite|screwdriver|el destornillador|tornavida
der Hammer|il martello|hammer|el martillo|çekiç
die Schutzbrille|gli occhiali di protezione|safety goggles|las gafas de protección|koruyucu gözlük
die Arbeitshandschuhe|i guanti da lavoro|work gloves|los guantes de trabajo|iş eldiveni
der Helm|il casco|helmet|el casco|kask
die Hydraulik|l'idraulica|hydraulics|la hidráulica|hidrolik
der Kolben|il pistone|piston|el pistón|piston
die Karosserie|la carrozzeria|bodywork|la carrocería|kaporta
montieren|montare|to assemble|montar|monte etmek
demontieren|smontare|to disassemble|desmontar|sökmek
schmieren|lubrificare|to lubricate|lubricar|yağlamak
das Ersatzteil|il pezzo di ricambio|spare part|la pieza de repuesto|yedek parça
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
der Router|il router|router|el router|router
das WLAN|il Wi-Fi|Wi-Fi|el wifi|Wi-Fi
die Cloud|il cloud|cloud|la nube|bulut
die App|l'app|app|la aplicación|uygulama
der Browser|il browser|browser|el navegador|tarayıcı
die Suchmaschine|il motore di ricerca|search engine|el buscador|arama motoru
der Server|il server|server|el servidor|sunucu
die Software|il software|software|el software|yazılım
die Hardware|l'hardware|hardware|el hardware|donanım
der Virus|il virus|virus|el virus|virüs
die Firewall|il firewall|firewall|el cortafuegos|güvenlik duvarı
der USB-Stick|la chiavetta USB|USB stick|la memoria USB|USB bellek
der Drucker|la stampante|printer|la impresora|yazıcı
die E-Mail|l'e-mail|email|el correo electrónico|e-posta
der Anhang|l'allegato|attachment|el archivo adjunto|ek
herunterladen|scaricare|to download|descargar|indirmek
hochladen|caricare|to upload|subir|yüklemek
speichern|salvare|to save|guardar|kaydetmek
löschen|eliminare|to delete|eliminar|silmek
der Absturz|il blocco del sistema|crash|el bloqueo|çökme
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
der Kontinent|il continente|continent|el continente|kıta
der Ozean|l'oceano|ocean|el océano|okyanus
die Insel|l'isola|island|la isla|ada
die Wüste|il deserto|desert|el desierto|çöl
der Wald|la foresta|forest|el bosque|orman
die Region|la regione|region|la región|bölge
der Bezirk|il distretto|district|el distrito|ilçe
die Gemeinde|il comune|municipality|el municipio|belediye
der Bürgermeister|il sindaco|mayor|el alcalde|belediye başkanı
die Regierung|il governo|government|el gobierno|hükümet
das Parlament|il parlamento|parliament|el parlamento|parlamento
das Gesetz|la legge|law|la ley|kanun
der Bürger|il cittadino|citizen|el ciudadano|vatandaş
die Staatsangehörigkeit|la cittadinanza|citizenship|la nacionalidad|vatandaşlık
die Kultur|la cultura|culture|la cultura|kültür
die Religion|la religione|religion|la religión|din
die Gesellschaft|la società|society|la sociedad|toplum
der Frieden|la pace|peace|la paz|barış
die Wirtschaft|l'economia|economy|la economía|ekonomi
die Umwelt|l'ambiente|environment|el medio ambiente|çevre
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
der Kreis|il cerchio|circle|el círculo|daire
das Dreieck|il triangolo|triangle|el triángulo|üçgen
das Quadrat|il quadrato|square|el cuadrado|kare
der Winkel|l'angolo|angle|el ángulo|açı
der Durchmesser|il diametro|diameter|el diámetro|çap
der Radius|il raggio|radius|el radio|yarıçap
der Umfang|il perimetro|perimeter|el perímetro|çevre
das Volumen|il volume|volume|el volumen|hacim
die Formel|la formula|formula|la fórmula|formül
der Durchschnitt|la media|average|el promedio|ortalama
die Statistik|la statistica|statistics|la estadística|istatistik
die Wahrscheinlichkeit|la probabilità|probability|la probabilidad|olasılık
das Experiment|l'esperimento|experiment|el experimento|deney
die Energie|l'energia|energy|la energía|enerji
die Kraft|la forza|force|la fuerza|kuvvet
die Masse|la massa|mass|la masa|kütle
die Chemie|la chimica|chemistry|la química|kimya
die Physik|la fisica|physics|la física|fizik
addieren|addizionare|to add|sumar|toplamak
multiplizieren|moltiplicare|to multiply|multiplicar|çarpmak
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
die Nase|il naso|nose|la nariz|burun
der Mund|la bocca|mouth|la boca|ağız
der Zahn|il dente|tooth|el diente|diş
das Herz|il cuore|heart|el corazón|kalp
die Lunge|il polmone|lung|el pulmón|akciğer
der Magen|lo stomaco|stomach|el estómago|mide
die Haut|la pelle|skin|la piel|cilt
das Knie|il ginocchio|knee|la rodilla|diz
der Husten|la tosse|cough|la tos|öksürük
die Erkältung|il raffreddore|cold (illness)|el resfriado|soğuk algınlığı
die Allergie|l'allergia|allergy|la alergia|alerji
die Verletzung|la lesione|injury|la lesión|yaralanma
die Impfung|la vaccinazione|vaccination|la vacunación|aşı
die Apotheke|la farmacia|pharmacy|la farmacia|eczane
das Medikament|il farmaco|medication|el medicamento|ilaç
die Tablette|la compressa|tablet/pill|la pastilla|hap
der Termin|l'appuntamento|appointment|la cita|randevu
die Versicherung|l'assicurazione|insurance|el seguro|sigorta
sich verletzen|ferirsi|to get injured|lastimarse|yaralanmak
husten|tossire|to cough|toser|öksürmek
""")),
    "🏠 Casa e vita quotidiana": ("Ambienti, mobili e faccende", "Il lessico della casa serve per descrivere spazi, oggetti e piccole azioni ripetute ogni giorno: utile per parlare con coinquilini, padroni di casa e vicini.", parse_terms("""
die Wohnung|l'appartamento|apartment|el apartamento|daire
das Haus|la casa|house|la casa|ev
das Zimmer|la stanza|room|la habitación|oda
die Küche|la cucina|kitchen|la cocina|mutfak
das Wohnzimmer|il soggiorno|living room|el salón|oturma odası
das Schlafzimmer|la camera da letto|bedroom|el dormitorio|yatak odası
das Badezimmer|il bagno|bathroom|el baño|banyo
der Flur|il corridoio|hallway|el pasillo|koridor
der Balkon|il balcone|balcony|el balcón|balkon
der Keller|la cantina|cellar|el sótano|bodrum
die Tür|la porta|door|la puerta|kapı
das Fenster|la finestra|window|la ventana|pencere
der Tisch|il tavolo|table|la mesa|masa
der Stuhl|la sedia|chair|la silla|sandalye
das Bett|il letto|bed|la cama|yatak
der Schrank|l'armadio|wardrobe|el armario|dolap
das Sofa|il divano|sofa|el sofá|kanepe
die Lampe|la lampada|lamp|la lámpara|lamba
der Kühlschrank|il frigorifero|fridge|el frigorífico|buzdolabı
die Waschmaschine|la lavatrice|washing machine|la lavadora|çamaşır makinesi
der Müll|la spazzatura|rubbish|la basura|çöp
die Miete|l'affitto|rent|el alquiler|kira
der Vermieter|il padrone di casa|landlord|el arrendador|ev sahibi
putzen|pulire|to clean|limpiar|temizlemek
aufräumen|riordinare|to tidy up|ordenar|toplamak
waschen|lavare|to wash|lavar|yıkamak
kochen|cucinare|to cook|cocinar|pişirmek
die Nachbarn|i vicini|neighbours|los vecinos|komşular
""")),
    "🍳 Cucina, cibo e pasti": ("Alimenti, pasti e cottura", "Nomi di cibi e verbi di cucina servono per fare la spesa, leggere un menu e seguire una ricetta. Associa ogni parola a un gesto o a un pasto concreto.", parse_terms("""
das Frühstück|la colazione|breakfast|el desayuno|kahvaltı
das Mittagessen|il pranzo|lunch|el almuerzo|öğle yemeği
das Abendessen|la cena|dinner|la cena|akşam yemeği
das Brot|il pane|bread|el pan|ekmek
die Butter|il burro|butter|la mantequilla|tereyağı
der Käse|il formaggio|cheese|el queso|peynir
die Milch|il latte|milk|la leche|süt
das Ei|l'uovo|egg|el huevo|yumurta
das Gemüse|la verdura|vegetables|la verdura|sebze
das Obst|la frutta|fruit|la fruta|meyve
das Fleisch|la carne|meat|la carne|et
der Fisch|il pesce|fish|el pescado|balık
der Reis|il riso|rice|el arroz|pirinç
die Nudeln|la pasta|pasta|la pasta|makarna
die Suppe|la zuppa|soup|la sopa|çorba
der Zucker|lo zucchero|sugar|el azúcar|şeker
das Salz|il sale|salt|la sal|tuz
der Pfeffer|il pepe|pepper|la pimienta|biber
das Öl|l'olio|oil|el aceite|yağ
der Topf|la pentola|pot|la olla|tencere
die Pfanne|la padella|pan|la sartén|tava
das Messer|il coltello|knife|el cuchillo|bıçak
die Gabel|la forchetta|fork|el tenedor|çatal
der Löffel|il cucchiaio|spoon|la cuchara|kaşık
der Teller|il piatto|plate|el plato|tabak
das Glas|il bicchiere|glass|el vaso|bardak
schneiden|tagliare|to cut|cortar|kesmek
braten|friggere|to fry|freír|kızartmak
backen|cuocere al forno|to bake|hornear|fırınlamak
der Geschmack|il sapore|taste|el sabor|tat
""")),
    "🚌 Trasporti e mobilità": ("Mezzi, biglietti e tragitti", "Muoversi in una città tedesca richiede lessico preciso su mezzi, orari e imprevisti. Utile anche per capire annunci e cartelli in stazione.", parse_terms("""
der Bus|l'autobus|bus|el autobús|otobüs
die Bahn|il treno|train|el tren|tren
die U-Bahn|la metropolitana|underground|el metro|metro
die Straßenbahn|il tram|tram|el tranvía|tramvay
das Fahrrad|la bicicletta|bicycle|la bicicleta|bisiklet
das Auto|l'auto|car|el coche|araba
der Bahnhof|la stazione|train station|la estación|tren istasyonu
die Haltestelle|la fermata|stop|la parada|durak
das Gleis|il binario|platform|el andén|peron
der Fahrplan|l'orario|timetable|el horario|tarife
die Fahrkarte|il biglietto|ticket|el billete|bilet
der Fahrschein|il biglietto di viaggio|travel ticket|el boleto|yolcu bileti
die Verspätung|il ritardo|delay|el retraso|gecikme
der Führerschein|la patente|driving licence|el carné de conducir|ehliyet
die Ampel|il semaforo|traffic light|el semáforo|trafik ışığı
die Kreuzung|l'incrocio|crossroads|el cruce|kavşak
der Parkplatz|il parcheggio|car park|el aparcamiento|otopark
der Stau|l'ingorgo|traffic jam|el atasco|trafik sıkışıklığı
die Autobahn|l'autostrada|motorway|la autopista|otoyol
der Flughafen|l'aeroporto|airport|el aeropuerto|havalimanı
das Flugzeug|l'aereo|airplane|el avión|uçak
das Ticket|il biglietto aereo|flight ticket|el billete de avión|uçak bileti
der Koffer|la valigia|suitcase|la maleta|bavul
umsteigen|cambiare mezzo|to change/transfer|hacer transbordo|aktarma yapmak
einsteigen|salire a bordo|to board|subir|binmek
aussteigen|scendere|to get off|bajar|inmek
abfahren|partire|to depart|salir|kalkmak
ankommen|arrivare|to arrive|llegar|varmak
""")),
    "💼 Lavoro, ufficio e burocrazia": ("Impiego, contratti e uffici pubblici", "Il lessico burocratico tedesco segue moduli e scadenze precise: conoscere questi termini aiuta a leggere una busta paga, un contratto o una lettera dell'ufficio pubblico.", parse_terms("""
die Arbeit|il lavoro|work|el trabajo|iş
der Arbeitgeber|il datore di lavoro|employer|el empleador|işveren
der Arbeitnehmer|il dipendente|employee|el empleado|çalışan
der Kollege|il collega|colleague|el colega|meslektaş
der Chef|il capo|boss|el jefe|patron
das Büro|l'ufficio|office|la oficina|ofis
der Vertrag|il contratto|contract|el contrato|sözleşme
das Gehalt|lo stipendio|salary|el salario|maaş
die Bewerbung|la candidatura|job application|la solicitud de empleo|iş başvurusu
der Lebenslauf|il curriculum|CV|el currículum|özgeçmiş
das Vorstellungsgespräch|il colloquio|job interview|la entrevista de trabajo|iş görüşmesi
die Kündigung|il licenziamento|dismissal|el despido|işten çıkarma
der Urlaub|le ferie|holiday|las vacaciones|tatil
die Überstunde|lo straordinario|overtime|la hora extra|fazla mesai
das Amt|l'ufficio pubblico|public office|la oficina pública|resmi daire
das Finanzamt|l'ufficio delle imposte|tax office|la oficina de impuestos|vergi dairesi
die Anmeldung|la registrazione di residenza|residence registration|el empadronamiento|ikamet kaydı
der Antrag|la domanda|application|la solicitud|başvuru
das Formular|il modulo|form|el formulario|form
die Unterschrift|la firma|signature|la firma|imza
der Ausweis|il documento d'identità|ID card|el documento de identidad|kimlik
der Reisepass|il passaporto|passport|el pasaporte|pasaport
die Steuer|la tassa|tax|el impuesto|vergi
die Frist|la scadenza|deadline|el plazo|son tarih
die Rente|la pensione|pension|la pensión|emeklilik maaşı
die Behörde|l'ente pubblico|public authority|la autoridad|kurum
sich bewerben|candidarsi|to apply for a job|postularse|başvurmak
kündigen|licenziare/dimettersi|to dismiss/resign|despedir/renunciar|işten çıkarmak
""")),
}


SUBJECT_LABELS = {
    "🔧 Meccanica e officina": {"it": "Meccanica e officina", "en": "Mechanics and workshop", "es": "Mecánica y taller", "tr": "Mekanik ve atölye"},
    "💻 Informatica e tecnologia": {"it": "Informatica e tecnologia", "en": "Computing and technology", "es": "Informática y tecnología", "tr": "Bilişim ve teknoloji"},
    "🗺️ Geografia e società": {"it": "Geografia e società", "en": "Geography and society", "es": "Geografía y sociedad", "tr": "Coğrafya ve toplum"},
    "🧮 Matematica e scienze": {"it": "Matematica e scienze", "en": "Mathematics and science", "es": "Matemáticas y ciencias", "tr": "Matematik ve bilim"},
    "🩺 Corpo e salute": {"it": "Corpo e salute", "en": "Body and health", "es": "Cuerpo y salud", "tr": "Vücut ve sağlık"},
    "🏠 Casa e vita quotidiana": {"it": "Casa e vita quotidiana", "en": "Home and daily life", "es": "Casa y vida cotidiana", "tr": "Ev ve günlük yaşam"},
    "🍳 Cucina, cibo e pasti": {"it": "Cucina, cibo e pasti", "en": "Kitchen, food and meals", "es": "Cocina, comida y comidas", "tr": "Mutfak, yemek ve öğünler"},
    "🚌 Trasporti e mobilità": {"it": "Trasporti e mobilità", "en": "Transport and mobility", "es": "Transporte y movilidad", "tr": "Ulaşım ve hareketlilik"},
    "💼 Lavoro, ufficio e burocrazia": {"it": "Lavoro, ufficio e burocrazia", "en": "Work, office and bureaucracy", "es": "Trabajo, oficina y burocracia", "tr": "İş, ofis ve bürokrasi"},
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
    st.markdown(f"<div class='card chapter'><p>{html.escape(SUBJECT_INTROS[language])}</p></div>", unsafe_allow_html=True)
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
    st.markdown(f"<div class='card chapter'><p>{html.escape(tx('verb_intro'))}</p></div>", unsafe_allow_html=True)
    query = st.text_input(tx("filter"))
    query = query.casefold().strip()
    shown = [verb for verb in VERBS if not query or query in verb["de"].casefold() or query in tr(verb, language).casefold()]
    st.caption(f"{len(shown)} / {len(VERBS)} {tx('verb_count')}")
    if not shown:
        st.info("Nessun verbo trovato per questo filtro.")
        return
    for start in range(0, len(shown), 30):
        chunk = shown[start:start + 30]
        speakable_verb_table(chunk, language)


CURRICULUM_SOURCES = {
    "it": """**Allineamento usato per questo manuale**

- [Goethe-Institut — livelli A1–C2 e descrittori QCER](https://www.goethe.de/de/spr/kur/stu.html): obiettivi comunicativi e progressione per livello.
- [vhs-Lernportal — panoramica dei corsi](https://www.vhs-lernportal.de/wws/kursangebot.php) e [programma B2 Beruf: temi e grammatica](https://www.vhs-lernportal.de/wws/bin/4007242-4008690-2-dvv_grammatiklisten_b2.pdf): scenari quotidiani/professionali e strutture da A1 a B2.
- [BAMF — corsi di tedesco per il lavoro](https://www.bamf.de/DE/Themen/Integration/ZugewanderteTeilnehmende/DeutschBeruf/deutsch-beruf.html): riferimento per la componente professionale B2.
- [Anerkennung in Deutschland — FAQ sul riconoscimento](https://www.anerkennung-in-deutschland.de/html/de/service/faq.php): IHK FOSA è un contesto di riconoscimento professionale, non un programma linguistico. I requisiti vanno verificati per professione e procedura.""",
    "en": """**Curricular alignment used in this handbook**

- [Goethe-Institut — A1–C2 levels and CEFR descriptors](https://www.goethe.de/de/spr/kur/stu.html): communicative aims and level progression.
- [vhs-Lernportal — course overview](https://www.vhs-lernportal.de/wws/kursangebot.php) and [B2 Beruf topics and grammar](https://www.vhs-lernportal.de/wws/bin/4007242-4008690-2-dvv_grammatiklisten_b2.pdf): everyday/professional scenarios and structures from A1 to B2.
- [BAMF — German for work courses](https://www.bamf.de/DE/Themen/Integration/ZugewanderteTeilnehmende/DeutschBeruf/deutsch-beruf.html): reference for the professional B2 component.
- [Recognition in Germany — FAQ](https://www.anerkennung-in-deutschland.de/html/de/service/faq.php): IHK FOSA is a professional-recognition context, not a language syllabus. Verify requirements for the profession and procedure.""",
    "es": """**Alineación curricular de este manual**

- [Goethe-Institut — niveles A1–C2 y descriptores MCER](https://www.goethe.de/de/spr/kur/stu.html).
- [vhs-Lernportal — visión general](https://www.vhs-lernportal.de/wws/kursangebot.php) y [temas y gramática B2 Beruf](https://www.vhs-lernportal.de/wws/bin/4007242-4008690-2-dvv_grammatiklisten_b2.pdf).
- [BAMF — alemán para el trabajo](https://www.bamf.de/DE/Themen/Integration/ZugewanderteTeilnehmende/DeutschBeruf/deutsch-beruf.html).
- [Reconocimiento en Alemania — FAQ](https://www.anerkennung-in-deutschland.de/html/de/service/faq.php): IHK FOSA es contexto de reconocimiento, no programa lingüístico.""",
    "tr": """**Bu el kitabındaki müfredat uyumu**

- [Goethe-Institut — A1–C2 düzeyleri ve CEFR tanımlayıcıları](https://www.goethe.de/de/spr/kur/stu.html).
- [vhs-Lernportal — kurslara genel bakış](https://www.vhs-lernportal.de/wws/kursangebot.php) ve [B2 Beruf konuları ve dilbilgisi](https://www.vhs-lernportal.de/wws/bin/4007242-4008690-2-dvv_grammatiklisten_b2.pdf).
- [BAMF — meslek için Almanca](https://www.bamf.de/DE/Themen/Integration/ZugewanderteTeilnehmende/DeutschBeruf/deutsch-beruf.html).
- [Almanya'da tanınma — SSS](https://www.anerkennung-in-deutschland.de/html/de/service/faq.php): IHK FOSA dil müfredatı değil, meslekî tanınma bağlamıdır.""",
}


def render_about() -> None:
    st.header(tx("about"))
    st.markdown(f"<div class='card chapter'><h3>{html.escape(tx('method_title'))}</h3><p>{html.escape(tx('method_text'))}</p></div>", unsafe_allow_html=True)
    st.markdown("#### " + tx("sources"))
    st.markdown(tx("source_links"))
    st.markdown(CURRICULUM_SOURCES[language])
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
        st.session_state["interface_language_choice"] = "English"
    language_label = st.selectbox(
        "🌐 " + UI[LANGUAGES[st.session_state["interface_language_choice"]]]["language"],
        list(LANGUAGES.keys()),
        key="interface_language_choice",
    )
st.session_state["language"] = LANGUAGES[language_label]
language = st.session_state["language"]

sections = {
    "lab": "Laboratorio di padronanza · pratica attiva",
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
st.sidebar.caption(f"{tx('bank')}: **{len(QUESTION_BANK)}** {tx('questions')}")
st.sidebar.caption(tx("sidebar_summary"))
st.sidebar.caption("🔊 de-DE SpeechSynthesis")

st.markdown(f"<section class='hero'><h1>🇩🇪 Der Deutsche Meister</h1><p>{html.escape(tx('tagline'))} · A1–B2</p></section>", unsafe_allow_html=True)

if section == "lab":
    render_fluency_lab(st, QUESTION_BANK, VOCAB_BY_LEVEL)
elif section in COURSES:
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
