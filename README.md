# Untis Notifier

Prueft automatisch alle 15 Minuten den WebUntis Stundenplan und schickt
eine Push Nachricht aufs Handy sobald eine Stunde als Entfall oder
Vertretung markiert ist. Laeuft komplett kostenlos ueber GitHub Actions,
dein eigener Computer muss dafuer nicht an sein.

## Schritt 1: ntfy App installieren

1. Installiere die App **ntfy** aus dem App Store oder Play Store
2. Denk dir einen eigenen Themennamen aus, zum Beispiel `mira-stundenplan-8f3k`.
   Nimm ruhig ein paar zufaellige Zeichen mit rein, denn jeder der den
   Namen kennt kann deine Nachrichten mitlesen
3. In der App auf das Plus tippen und diesen Themennamen abonnieren

## Schritt 2: Repository erstellen

1. Erstelle ein neues, **privates** Repository auf GitHub
2. Lade alle Dateien aus diesem Projekt dort hoch

## Schritt 3: Untis Zugangsdaten

Fuer das Gymnasium Essen Werden sind Server und Schule schon bekannt:

- `UNTIS_SERVER` ist `gym-essen-werden.webuntis.com`
- `UNTIS_SCHOOL` ist `gym-essen-werden`
- `UNTIS_USERNAME` und `UNTIS_PASSWORD` sind deine normalen Login Daten
  mit denen du dich auch im Browser bei WebUntis einloggst

## Schritt 4: Secrets im Repository hinterlegen

Im Repository unter **Settings > Secrets and variables > Actions >
New repository secret** folgende fuenf Secrets anlegen:

- `UNTIS_SCHOOL`
- `UNTIS_SERVER`
- `UNTIS_USERNAME`
- `UNTIS_PASSWORD`
- `NTFY_TOPIC` (der Themenname aus Schritt 1)

## Schritt 5: Testen

Im Reiter **Actions** den Workflow **Untis Check** auswaehlen und oben
rechts auf **Run workflow** klicken. Nach ein paar Sekunden siehst du im
Log ob alles funktioniert hat. Wenn gerade eine Vertretung oder ein
Entfall ansteht, sollte kurz danach eine Nachricht auf deinem Handy
auftauchen.

Danach laeuft alles automatisch nach dem in `check.yml` hinterlegten
Zeitplan.

## Hinweise

- Das Skript merkt sich in `state.json` was es beim letzten Mal gesehen
  hat, damit du nicht wieder und wieder dieselbe Nachricht bekommst
- Die Bibliothek `webuntis` ist inoffiziell, falls Untis auf Serverseite
  etwas aendert kann es sein dass das Skript angepasst werden muss
- Wenn dein Untis Konto eine Zwei Faktor Anmeldung nutzt funktioniert der
  normale Login eventuell nicht, dann bitte kurz melden
