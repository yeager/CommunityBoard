"""Datahantering för CommunityBoard - JSON-baserad lagring."""

import json
import os
from datetime import datetime

KATEGORIER = ["Aktiviteter", "Stöd", "Jobb", "Lediga tjänster"]

DATA_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "communityboard")
DATA_FILE = os.path.join(DATA_DIR, "inlagg.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def ladda_inlagg():
    """Ladda alla inlägg från JSON-fil."""
    _ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return _skapa_exempeldata()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def spara_inlagg(inlagg):
    """Spara alla inlägg till JSON-fil."""
    _ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(inlagg, f, ensure_ascii=False, indent=2)


def skapa_inlagg(titel, text, kategori, kontakt=""):
    """Skapa ett nytt inlägg och spara."""
    inlagg = ladda_inlagg()
    nytt = {
        "id": len(inlagg) + 1,
        "titel": titel,
        "text": text,
        "kategori": kategori,
        "kontakt": kontakt,
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    inlagg.insert(0, nytt)
    spara_inlagg(inlagg)
    return nytt


def ta_bort_inlagg(inlagg_id):
    """Ta bort ett inlägg baserat på ID."""
    inlagg = ladda_inlagg()
    inlagg = [i for i in inlagg if i["id"] != inlagg_id]
    spara_inlagg(inlagg)


def _skapa_exempeldata():
    """Skapa exempelinlägg för att visa hur appen fungerar."""
    exempel = [
        {
            "id": 1,
            "titel": "Rullstolsbasket varje tisdag",
            "text": "Välkommen att spela rullstolsbasket med oss! Alla nivåer välkomna. Vi har extra rullstolar att låna.",
            "kategori": "Aktiviteter",
            "kontakt": "anna@exempel.se",
            "datum": "2026-03-15 10:00",
        },
        {
            "id": 2,
            "titel": "Stödgrupp för synskadade",
            "text": "Vi träffas varannan onsdag för att dela erfarenheter och stötta varandra. Fika ingår!",
            "kategori": "Stöd",
            "kontakt": "erik@exempel.se",
            "datum": "2026-03-14 14:30",
        },
        {
            "id": 3,
            "titel": "Personlig assistent sökes",
            "text": "Söker personlig assistent i Göteborg, deltid 20h/vecka. Erfarenhet av LSS är meriterande.",
            "kategori": "Jobb",
            "kontakt": "maria@exempel.se",
            "datum": "2026-03-13 09:15",
        },
        {
            "id": 4,
            "titel": "Kommunen anställer tillgänglighetsrådgivare",
            "text": "Stockholms stad söker en tillgänglighetsrådgivare. Heltid, tillsvidare. Egen erfarenhet av funktionsnedsättning är meriterande.",
            "kategori": "Lediga tjänster",
            "kontakt": "rekrytering@stockholm.se",
            "datum": "2026-03-12 11:00",
        },
        {
            "id": 5,
            "titel": "Simgrupp för alla",
            "text": "Anpassad simning i Eriksdalsbadet. Lördagar kl 10-11. Instruktörer med specialkompetens finns på plats.",
            "kategori": "Aktiviteter",
            "kontakt": "simgruppen@exempel.se",
            "datum": "2026-03-11 16:45",
        },
    ]
    spara_inlagg(exempel)
    return exempel
