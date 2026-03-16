# CommunityBoard

Lokalt anslagstavla för funktionshinderrörelsen. En enkel GTK4/Adwaita-app för att dela aktiviteter, stödgrupper, jobb och lediga tjänster i ditt närområde.

## Funktioner

- Skapa och visa inlägg med titel, beskrivning och kontaktinfo
- Kategorisering: Aktiviteter, Stöd, Jobb, Lediga tjänster
- Sök bland inlägg
- Filtrera per kategori
- Lokal JSON-lagring (ingen server behövs)
- Svenska som huvudspråk

## Installation

### Beroenden

- Python 3.8+
- GTK4
- libadwaita
- PyGObject

#### Ubuntu/Debian

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
```

#### Fedora

```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

#### Arch Linux

```bash
sudo pacman -S python-gobject gtk4 libadwaita
```

### Installera appen

```bash
pip install .
```

## Användning

```bash
communityboard
```

Eller kör direkt:

```bash
python -m communityboard.app
```

Data sparas i `~/.local/share/communityboard/inlagg.json`.

## Licens

GPL-3.0
