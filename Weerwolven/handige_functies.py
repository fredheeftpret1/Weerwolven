import time
import json
import datetime

WACHT_TIJD = 1

def krijg_teksten():
    # Geef het pad van je JSON-bestand op
    json_bestand = 'teksten.json'

    # Open en laad het JSON-bestand
    try:
        with open(json_bestand, 'r', encoding='utf-8') as bestand:
            data = json.load(bestand)
            return data

    except FileNotFoundError:
        print(f'Fout: Het bestand "{json_bestand}" is niet gevonden.')
    except json.JSONDecodeError:
        print('Fout: Het bestand bevat geen geldige JSON.')

def print_story(tekst):
    tekst = tekst.split("\n")
    for zin in tekst:
        time.sleep(WACHT_TIJD)
        print(zin)
    time.sleep(WACHT_TIJD)

def print_story_confirmation(tekst, mogelijkheden):
    print_story(tekst)

    while True:
        try:
            bevestiging = int(input())
            if 1 <= bevestiging < int(mogelijkheden + 1):  # Controleer of het binnen het bereik ligt
                return int(bevestiging)
            else:
                print(f"Gelieve een geldige keuze te maken (1 t/m {mogelijkheden}).")
        except ValueError:
            print("Ongeldige invoer. Voer een geheel getal in.")


def clear_console():
    print("\n" * 100)

def deelbaar_door(x: int, y: int) -> bool:
    return x % y == 0

def reverse(tekst: str) -> str:
    reversed = ""
    for letter in tekst:
        reversed = letter + reversed
    return reversed

def num_input(prompt: str) -> int:
    return int(input(prompt))


