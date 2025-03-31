import datetime
import os

hoofdmap = os.path.dirname(os.path.abspath(__file__))
nieuwe_map = os.path.join(hoofdmap, 'Alle opgeslagen spellen')
os.makedirs(nieuwe_map, exist_ok=True)

def slaag_op(bestand, spel):
    with open(bestand, "r") as file:
        text = file.read()

    spelers = spel.spelers_lijst
    rollen_tekst = ""
    spelers_namen_lijst = ""
    for speler in spelers:
        rollen_tekst += f"\n{speler.naam} was een {speler.rol}"
        spelers_namen_lijst += f"\n- {speler.naam}"

    text = text.replace("{spelers_namen}", spelers)
    text = text.replace("{nacht}", str(spel.nacht))
    text = text.replace("{Winmanier}", spel.einde_spel.replace("zijn", "waren"))
    text = text.replace("{rollen}", str(rollen_tekst))
    text = text.replace("{datum}", datetime.date.today().strftime("%d/%m/%Y"))
    with open(nieuwe_map + datetime.date.today().strftime("%d/%m/%Y") + ".txt", "w") as file:
        file.write(text)

