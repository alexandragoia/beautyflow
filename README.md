# BeautyFlow AI

BeautyFlow ist ein mehrsprachiger Lern- und Portfolio-Prototyp für die Suche nach Beauty-Studios. Die Website zeigt sechs fiktive Berliner Studios, vergleicht Demo-Angebote und enthält einen Gesprächsbereich.

> Das Modell hilft beim Formulieren. Studio-Fakten kommen aus einem gemeinsamen Katalog. Buchungen bleiben in dieser Demo unverbindlich.

Alle Studios, Preise, Kontaktdaten, Bewertungen und Termine sind erfundene Beispieldaten. BeautyFlow ist kein echter Buchungsdienst.

## Portfolio-Website

Die GitHub-Pages-Seite liegt unter [alexandragoia.github.io/beautyflow](https://alexandragoia.github.io/beautyflow/).

- `catalog.json` ist die gemeinsame Datenquelle für die Studio-Karten und die KI-Schnittstelle.
- `index.html` lädt den Katalog und filtert die Demo-Studios nach Wunsch, Stadtteil, Budget und Behandlung.
- `web_api.py` stellt eine kleine FastAPI-Schnittstelle bereit. Sie übermittelt die Nachricht an Gemini und gibt eine kurze, katalogbasierte Antwort zurück.
- `api-config.js` enthält nur die öffentliche URL des API-Servers. Der Gemini-Schlüssel gehört dort niemals hinein.
- Die Demo bucht keine Termine, versendet keine E-Mails und analysiert keine Fotos. Bilder bleiben im Browser.

Ist in `api-config.js` noch keine API-URL eingetragen, zeigt die Seite klar den lokalen Demo-Modus und die Suche mit Beispielstudios funktioniert weiter.

## KI-Schnittstelle bereitstellen

GitHub Pages führt kein Python aus. Die Website und das Python-Backend werden deshalb getrennt veröffentlicht. Eine Render-Konfiguration ist in `render.yaml` vorbereitet.

1. In Render ein neues **Blueprint** aus diesem GitHub-Repository anlegen. Render liest `render.yaml` und installiert die Pakete aus `requirements.txt`.
2. In den Umgebungsvariablen des Render-Dienstes `GEMINI_API_KEY` mit deinem privaten Schlüssel setzen. Den Schlüssel nie in GitHub, `api-config.js`, den Browser oder einen Chat kopieren.
3. Nach dem Start sollte die Adresse `https://DEIN-DIENST.onrender.com/health` den Status `ok` anzeigen.
4. Die öffentliche Basisadresse des Dienstes in `api-config.js` als `window.BEAUTYFLOW_API_URL` eintragen und die Änderung speichern. GitHub Pages aktualisiert die Website danach automatisch.
5. Die Demo-Seite neu laden. Im Chatkopf erscheint **Gemini verbunden · Demo**. Eine Beispielanfrage sollte zusätzlich eine Antwort des API-Servers liefern.

Die erlaubten Browser-Adressen sind standardmäßig die BeautyFlow-GitHub-Seite und lokale Entwicklungsadressen. Für einen anderen Veröffentlichungsort kann `CORS_ORIGINS` im Hosting angepasst werden. Die Schnittstelle begrenzt Nachrichtenlänge und Anfragehäufigkeit; sie speichert keine Chatverläufe. Der kostenlose Hosting-Tarif kann nach Ruhezeit kurz zum Aufwachen brauchen.

### Lokal starten

Python 3.10 oder neuer installieren und Pakete einrichten:

```text
python -m pip install -r requirements.txt
```

Eine lokale `.env`-Datei anlegen:

```text
GEMINI_API_KEY=dein_privater_schluessel
```

API lokal starten:

```text
uvicorn web_api:app --reload --port 8001
```

Für die lokale Website `api-config.js` auf `http://127.0.0.1:8001` einstellen. Dann `index.html` in einem zweiten Terminal über einen lokalen Webserver öffnen (zum Beispiel `python -m http.server 8000`). Keine API-URL mit `file://` öffnen.

## Python-Workflow als separates Lernbeispiel

`beautyflow.py` zeigt einen zweiten, regelbasierten Ablauf für das fiktive LUMÉ Beauty Studio in Dortmund:

```text
Kundennachricht -> Gemini-Extraktion -> Validierung -> Python-Datums- und Sicherheitsregeln
                                                          -> Antwort oder menschliche Prüfung
```

Er verarbeitet Deutsch, Englisch und Spanisch. Preise und Leistungen stammen für dieses Kommandozeilen-Beispiel aus `knowledge_base.json`. Das ist getrennt von den sechs Website-Beispielen und wird nicht von der Website-API verwendet.

Offline-Prüfungen für diesen Workflow ausführen:

```text
python test_workflow.py
```

Beispielnachricht (verwendet Gemini):

```text
python beautyflow.py "Hi, I want to book a classic facial this Friday evening."
```

## Grenzen und Datenschutz der Demo

- Alle Studios, Dienstleistungen, Preise, Kontaktdaten, Bewertungen und Verfügbarkeiten sind fiktiv.
- Bei aktivierter API wird der eingegebene Nachrichtentext zur Antwort an den BeautyFlow-Server und Gemini übermittelt. Bitte keine persönlichen oder sensiblen Daten eingeben.
- Fotos werden in dieser Version nicht hochgeladen und nicht von KI analysiert.
- Eine Buchungsbestätigung erscheint nur im Browser. Es wird kein Termin gespeichert und keine E-Mail versandt.
- Favoriten, Punkte, Rabatte und Bewertungen sind illustrative Frontend-Daten; es gibt keine echten Konten oder Zahlungen.
- Es gibt keine Verbindung zu echten Studio-Kalendern, CRM-Systemen oder E-Mail-Diensten.
