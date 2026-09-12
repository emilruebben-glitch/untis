"""
Untis Benachrichtigung

Loggt sich bei WebUntis ein, schaut sich den Stundenplan fuer die naechsten
Tage an und schickt eine Push Nachricht ueber ntfy.sh sobald eine neue
Stunde als Entfall oder Vertretung markiert ist.

Der letzte bekannte Stand wird in state.json gespeichert, damit nicht
staendig die gleiche Nachricht verschickt wird.
"""

import json
import os
import sys
from datetime import date, timedelta

import requests
import webuntis

STATE_FILE = "state.json"
DAYS_AHEAD = 7


def get_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"Fehler: Umgebungsvariable {name} fehlt")
        sys.exit(1)
    return value


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)


def send_notification(topic, title, message):
    url = f"https://ntfy.sh/{topic}"
    requests.post(
        url,
        data=message.encode("utf8"),
        headers={
            "Title": title.encode("utf8"),
            "Priority": "high",
            "Tags": "warning",
        },
        timeout=10,
    )


def period_key(period):
    # eindeutiger Schluessel pro Stunde, damit wir sie ueber mehrere
    # Durchlaeufe hinweg wiedererkennen
    return period.start.isoformat()


def period_label(period):
    if period.subjects:
        subject = ", ".join(fach.name for fach in period.subjects)
    else:
        subject = "Unbekanntes Fach"
    start = period.start.strftime("%a %d.%m. %H:%M")
    return f"{subject} am {start}"


def main():
    school = get_env("UNTIS_SCHOOL")
    server = get_env("UNTIS_SERVER")
    username = get_env("UNTIS_USERNAME")
    password = get_env("UNTIS_PASSWORD")
    ntfy_topic = get_env("NTFY_TOPIC")

    old_state = load_state()
    new_state = {}
    changes = []

    with webuntis.Session(
        server=server,
        username=username,
        password=password,
        school=school,
        useragent="UntisNotifier",
    ).login() as s:
        start = date.today()
        end = start + timedelta(days=DAYS_AHEAD)
        table = s.my_timetable(start=start, end=end)

        for period in table:
            key = period_key(period)
            code = period.code or "regular"
            new_state[key] = code

            old_code = old_state.get(key)
            if code in ("cancelled", "irregular") and code != old_code:
                kind = "Entfall" if code == "cancelled" else "Vertretung oder Aenderung"
                changes.append(f"{kind}: {period_label(period)}")

    if changes:
        message = "\n".join(changes)
        send_notification(ntfy_topic, title="Stundenplan Aenderung", message=message)
        print("Benachrichtigung gesendet:")
        print(message)
    else:
        print("Keine neuen Aenderungen gefunden.")

    save_state(new_state)


if __name__ == "__main__":
    main()
