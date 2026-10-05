# BeautyFlow AI

BeautyFlow ist ein mehrsprachiger Prototyp für Anfragen und Terminabläufe in fiktiven Beauty-Studios. Ein Sprachmodell strukturiert Kundenanfragen; Python wendet Geschäftsregeln an und leitet sensible oder nicht abgedeckte Fälle an Menschen weiter.

> Das Modell interpretiert. Der Workflow entscheidet. Menschen kümmern sich um Ausnahmen.

Alle Studioangaben und Geschäftsdaten in diesem Repository sind erfunden. Das Projekt dient zum Lernen und ist kein echter Buchungsdienst.

## Funktionsweise

```text
Kundennachricht -> Gemini-Extraktion -> Validierung -> Python-Datums- und Sicherheitsregeln
                                                          -> fundierte Antwort oder menschliche Prüfung
```

- Verarbeitet Nachrichten auf Deutsch, Englisch und Spanisch.
- Nutzt nachvollziehbare Python-Regeln zur Datumsauflösung und Weiterleitung.
- Bezieht Antworten aus `knowledge_base.json`; fehlende Preise werden nicht erfunden und Termine nicht automatisch bestätigt.
- Leitet Gesundheitsfragen, Beschwerden und nicht unterstützte Fälle zur Prüfung an einen Menschen weiter.
- Enthält Offline-Prüfungen für den Workflow in `test_workflow.py`.

## Lokal starten

Python 3.10 oder neuer installieren und die Abhängigkeiten einrichten:

```text
python -m pip install google-genai python-dotenv
```

Eine lokale `.env`-Datei in diesem Ordner mit deinem Gemini-API-Schlüssel anlegen:

```text
GEMINI_API_KEY=your_key_here
```

Die `.env`-Datei privat halten. Sie wird durch `.gitignore` von Git ausgeschlossen. Den Schlüssel niemals in dieses Repository, die Website oder einen öffentlichen Chat kopieren.

Offline-Prüfungen ausführen (ohne API-Aufruf):

```text
python test_workflow.py
```

Eine Beispielnachricht ausführen (verwendet die Gemini-API):

```text
python beautyflow.py "Hi, I want to book a classic facial this Friday evening."
```

## Portfolio-Website

`index.html` im Stammverzeichnis enthält eine interaktive deutsche Buchungsdemo mit vier Beispielstudios, Behandlungen, Preisen, freien und belegten Zeitfenstern, einer lokalen Bestätigungsvorschau und einer beispielhaften Preisberatung.

## Grenzen des Prototyps

- Studios, Preise, Adressen und Kalender sind fiktive Beispieldaten.
- Die Buchungsbestätigung wird nur im Browser angezeigt; es wird keine E-Mail gesendet und kein Termin gespeichert.
- Die Chat-Antworten und Foto-Einschätzungen sind illustrative Demos. Die Fotos werden nicht hochgeladen und nicht von einer KI analysiert.
- Es gibt keine Verbindung zu echten Studio-Kalendern, CRM-Systemen oder E-Mail-Diensten.
- Für einen echten Dienst müssten Studios ihre Daten pflegen und Kalender, E-Mail sowie eine sichere KI-Schnittstelle angebunden werden.

