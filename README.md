# BeautyFlow

BeautyFlow ist ein Portfolio-Prototyp für die Suche nach Beauty-Studios. Die Website zeigt sechs fiktive Studios in Berlin, Beispielpreise und einen Buchungsablauf zum Ausprobieren.

**Alle Studios, Kontaktdaten, Preise, Bewertungen und freien Zeiten sind erfunden. Die Seite nimmt keine echten Buchungen an und verschickt keine E-Mails.** Das Vorhaben ist derzeit ein Kundinnen-Marktplatz. Ein Marketing- oder Social-Media-Planer für Salons gehört nicht zu diesem Prototyp.

## Website und KI-Suche

Die Website liegt auf [GitHub Pages](https://alexandragoia.github.io/beautyflow/).

- `catalog.json` liefert dieselben Beispieldaten an Website und KI.
- `index.html` zeigt Studios, filtert Angebote und führt durch eine unverbindliche Buchungsdemo.
- Wenn die API verbunden ist, kann Gemini eine freie Nachricht wie „French Nails am Freitag, bis 50 €“ in Behandlung, Postleitzahl, Budget und Datum übersetzen. Die Website setzt erkannte Angaben in die Suche ein und wählt den gewünschten Tag im Buchungskalender vor.
- `web_api.py` ist das Python-Backend. Es hält den Gemini-Schlüssel geheim, begrenzt Anfragen und gibt nur kurze Antworten sowie geprüfte Suchfilter zurück.
- `search_logic.py` verwirft ungültige oder nicht unterstützte Filter.
- `api-config.js` enthält nur die optionale öffentliche Adresse des API-Servers. Ein geheimer Gemini-Schlüssel gehört niemals in diese Datei.
- Demo-Konto, Treuepunkte, Favoriten und letzte Demo-Auswahl bleiben auf diesem Gerät im Browser. E-Mail-Adressen und Chatverläufe werden nicht gespeichert.

Ist `api-config.js` leer, läuft BeautyFlow ohne Server: Die lokale Suche erkennt einfache Angaben und beantwortet Preis-/Dauerfragen aus dem fiktiven Katalog. Das ist keine verbundene KI.

## Optionale Erweiterung mit einer KI-API

Diese Erweiterung ist für die lokale Portfolio-Demo nicht erforderlich. Sie verbindet freie Texteingaben mit Gemini. GitHub Pages führt kein Python aus; dafür wäre ein zusätzlich gehosteter API-Dienst nötig. Hosting und Gemini können je nach Anbieter und Nutzung Kosten verursachen. Die Einstellungen in `render.yaml` sind nur vorbereitet und werden nicht verwendet, solange `api-config.js` leer bleibt.

1. In Render ein neues **Blueprint** aus diesem GitHub-Repository erstellen.
2. Im Render-Dienst die geheime Umgebungsvariable `GEMINI_API_KEY` setzen. Den Schlüssel nicht in GitHub, die Website oder einen Chat eintragen.
3. Nach dem Start sollte `https://DEIN-DIENST.onrender.com/health` den Status `ok` anzeigen.
4. Die Dienstadresse in `api-config.js` bei `window.BEAUTYFLOW_API_URL` eintragen und die Datei speichern.
5. Nach dem GitHub-Pages-Neustart die Website öffnen. Der Chat zeigt dann „KI-API konfiguriert“.

Die API erlaubt standardmäßig nur Anfragen von der BeautyFlow-Seite und lokalen Entwicklungsadressen. Sie begrenzt Nachrichtenlänge und Anfragehäufigkeit und speichert keine Chatverläufe. Nachrichten werden bei verbundener API an BeautyFlow und Gemini gesendet; bitte keine persönlichen oder vertraulichen Daten eingeben. Fotos bleiben im Browser und werden nicht analysiert.

### Lokal starten

Python 3.10 oder neuer installieren und im Projektordner ausführen:

```text
python -m pip install -r requirements.txt
```

Eine lokale Datei `.env` mit dem privaten Schlüssel anlegen:

```text
GEMINI_API_KEY=dein_privater_schluessel
```

API starten:

```text
uvicorn web_api:app --reload --port 8001
```

In `api-config.js` die lokale Adresse `http://127.0.0.1:8001` eintragen. Die Website in einem zweiten Terminal starten:

```text
python -m http.server 8000
```

Dann `http://127.0.0.1:8000` öffnen. Nicht über `file://` starten.

## Separates Python-Lernbeispiel

`beautyflow.py` zeigt zusätzlich einen regelbasierten Ablauf für das fiktive LUMÉ Beauty Studio in Dortmund. Dieses Kommandozeilen-Beispiel nutzt die separate Datei `knowledge_base.json`; es ist nicht das Backend der Berlin-Website.

Die Offline-Prüfungen ausführen:

```text
python test_workflow.py
python test_search.py
```

## Was noch nicht echt ist

- Es gibt keine echten Studios, Konten, Zahlungen oder gespeicherten Buchungen.
- Die angezeigten Bewertungen und Rabatte sind Beispiele.
- Es gibt keine Verbindung zu Studio-Kalendern, CRM-Systemen oder E-Mail-Diensten.
- Fotos werden weder hochgeladen noch durch eine KI ausgewertet.
- Eine Social-Media-Planung für Salons ist ein mögliches späteres, separates Produkt.
