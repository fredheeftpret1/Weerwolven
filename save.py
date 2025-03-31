import datetime
import os
import sys

from handige_functies import print_story

hoofdmap = os.path.dirname(os.path.abspath(__file__))
nieuwe_map = os.path.join(hoofdmap, 'Alle opgeslagen spellen')
os.makedirs(nieuwe_map, exist_ok=True)

def slaag_op(bestand, spel):
    with open("eind_tekst.txt", "r") as f:
        print_story(f.read())
    naam_bestand = input(">> ")
    with open(bestand, "r") as file:
        text = file.read()

    spelers = spel.spelers_lijst
    rollen_tekst = ""
    spelers_namen_lijst = ""
    for speler in spelers:
        rollen_tekst += f"\n{speler.naam} was een {speler.rol}"
        spelers_namen_lijst += f"\n- {speler.naam}"

    text = text.replace("{spelers_namen}", spelers_namen_lijst)
    text = text.replace("{nacht}", str(spel.nacht))
    text = text.replace("{Winmanier}", spel.einde_tekst.replace("zijn", "waren"))
    text = text.replace("{rollen}", str(rollen_tekst))
    text = text.replace("{datum}", datetime.date.today().strftime("%d/%m/%Y"))
    with open(nieuwe_map + "\\" + naam_bestand, "w") as file:
        file.write(text)

