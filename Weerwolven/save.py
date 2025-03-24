import datetime
import os

hoofdmap = os.path.dirname(os.path.abspath(__file__))
nieuwe_map = os.path.join(hoofdmap, 'Alle opgeslagen spellen')
os.makedirs(nieuwe_map, exist_ok=True)

def slaag_op(bestand, spelers, nacht_nummer, win_manier, rollen):
    with open(bestand, "r") as file:
        text = file.read()

    spelers = "\n       - ".join(spelers)
    rollen_tekst = ""
    for speler in rollen:
        rollen_tekst += f"\n{speler} was een {rollen[speler]}"
    text = text.replace("{spelers_namen}", spelers)
    text = text.replace("{nacht}", str(nacht_nummer))
    text = text.replace("{Winmanier}", win_manier.replace("zijn", "waren"))
    text = text.replace("{rollen}", str(rollen_tekst))
    text = text.replace("{datum}", datetime.date.today().strftime("%d/%m/%Y"))
    with open(nieuwe_map + datetime.date.today().strftime("%d/%m/%Y") + ".txt", "w") as file:
        file.write(text)

